# -*- coding: utf-8 -*-
"""成片"打斗感"实测：幅度与打击声。

配合 scripts/motion-audit.py 使用。两者分工：
  motion-audit.py  管"有没有在动"（逐秒运动能量、最长近静止区间、最高点落位、帧复制）
  fight-metrics.py 管"动得够不够大、打没打实"（强度分布、爆发比例、峰均比、音频峰值）

用法：
    python fight-metrics.py <成片1.mp4> [成片2.mp4 ...]
    python fight-metrics.py <成片.mp4> --ref <参照片.mp4>     # 与参照片并排对照
    python fight-metrics.py --selftest                        # 合成片自检

判据见 references/pacing.md 第三节与第七节。依赖 ffmpeg / ffprobe 在 PATH 中。

指标口径：
  运动能量   = 相邻帧差分图的平均灰度（0-255），越高动得越大
  高强度帧   = 运动能量 > 8.0 的帧占比
  爆发帧     = 运动能量 > 2× 全片中位数的帧占比
  逐秒峰均比 = 每一秒内最高一帧 ÷ 该秒均值，衡量"一顿一顿"的程度
  音频峰值   = 逐秒采样峰值，距满刻度越小说明打击声越实

阈值是**经验阈值**：由一条参照片与两次实测标定，绑定在 720×1280 / 24fps 这一档。
换分辨率、帧率或画幅后，运动能量的绝对值会变，门槛需要重新标定；比例关系可沿用。
把它当"排序与对照工具"比当"绝对及格线"更可靠——最有力的用法是和一条公认有打斗感的
参照片并排跑，看两者的强度分布差几倍。
"""
import math
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile

HI = 8.0            # 高强度帧阈值（运动能量）
HI_RATIO = 0.20     # 经验阈值：高强度帧占比
BURST_RATIO = 0.09  # 经验阈值：爆发帧占比
PEAK_MEAN_RATIO = 2.9
MAX_ENERGY = 50.0
AUDIO_HEADROOM = 3.0


def require_ffmpeg():
    missing = [b for b in ("ffmpeg", "ffprobe") if shutil.which(b) is None]
    if missing:
        print("缺少依赖：%s 不在 PATH 中。" % "、".join(missing))
        print("安装 ffmpeg 后再试（macOS: brew install ffmpeg；Windows: winget install ffmpeg；")
        print("Debian/Ubuntu: sudo apt install ffmpeg），或把可执行文件目录加入 PATH。")
        return False
    return True


def run(cmd, binary=False, cwd=None):
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, cwd=cwd)
    return p.stdout if binary else p.stdout.decode("utf-8", "replace")


def motion_series(video):
    """逐帧运动能量。临时文件写进独立临时目录，避免污染工作目录。"""
    with tempfile.TemporaryDirectory() as td:
        name = "motion.txt"
        run(["ffmpeg", "-v", "error", "-i", video,
             "-vf", "tblend=all_mode=difference,signalstats,metadata=print:file=%s" % name,
             "-an", "-f", "null", "-"], cwd=td)
        series, t = [], None
        path = os.path.join(td, name)
        if not os.path.exists(path):
            return series
        for line in open(path, encoding="utf-8", errors="replace"):
            m = re.match(r"frame:\s*(\d+)\s+pts:\d+\s+pts_time:([0-9.]+)", line)
            if m:
                t = float(m.group(2))
                continue
            m2 = re.search(r"lavfi\.signalstats\.YAVG=([0-9.]+)", line)
            if m2 and t is not None:
                series.append((t, float(m2.group(1))))
                t = None
        return series


def audio_series(video, sr=8000):
    raw = run(["ffmpeg", "-v", "error", "-i", video, "-vn", "-ac", "1", "-ar", str(sr),
               "-f", "s16le", "-"], binary=True)
    n = len(raw) // 2
    if n == 0:
        return []
    samples = struct.unpack("<%dh" % n, raw[:n * 2])
    out = []
    for i in range(0, n, sr):
        chunk = samples[i:i + sr]
        if not chunk:
            break
        rms = math.sqrt(sum(float(s) * s for s in chunk) / len(chunk)) / 32768.0
        db = 20 * math.log10(rms) if rms > 1e-9 else -99.0
        peak = max(abs(min(chunk)), abs(max(chunk))) / 32768.0
        pdb = 20 * math.log10(peak) if peak > 1e-9 else -99.0
        out.append((i / float(sr), db, pdb))
    return out


def pct(vals, p):
    """线性插值百分位。"""
    if not vals:
        return 0.0
    s = sorted(vals)
    if len(s) == 1:
        return s[0]
    pos = (len(s) - 1) * p
    lo = int(math.floor(pos))
    hi = min(lo + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (pos - lo)


def measure(path):
    series = motion_series(path)
    audio = audio_series(path)
    if not series:
        return None
    vals = [v for _, v in series]
    med = pct(vals, .5)
    sec_vals = {}
    for t, v in series:
        sec_vals.setdefault(int(t), []).append(v)
    ratios = [max(a) / (sum(a) / len(a) if sum(a) / len(a) > 0.01 else 0.01)
              for _, a in sorted(sec_vals.items())]
    pdb = [p for _, _, p in audio]
    db = [d for _, d, _ in audio]
    return {
        "mean": sum(vals) / len(vals), "med": med, "p90": pct(vals, .9),
        "max": max(vals),
        "hi": sum(1 for v in vals if v > HI) / float(len(vals)),
        "burst": sum(1 for v in vals if v > 2 * med) / float(len(vals)),
        "ratio": sum(ratios) / len(ratios) if ratios else 0,
        "ratio_max": max(ratios) if ratios else 0,
        "quiet": [s for s, a in sorted(sec_vals.items())
                  if sum(a) / len(a) < sum(vals) / len(vals) / 3.0],
        "rms": sum(db) / len(db) if db else -99,
        "peak_db": max(pdb) if pdb else -99,
        "strong": sum(1 for p in pdb if p > -3.0),
        "frames": len(vals),
    }


def show(name, m):
    if not m:
        print("%s：读不出数据（文件不可解码，或没有视频流）" % name)
        return
    print("=" * 70)
    print(name)
    print("=" * 70)
    print("运动能量  均值 %.2f  中位 %.2f  P90 %.2f  最大 %.2f" % (m["mean"], m["med"], m["p90"], m["max"]))
    print("高强度帧（>%.1f）  %.1f%%   %s" % (HI, m["hi"] * 100, "达到经验阈值" if m["hi"] >= HI_RATIO else "低于经验阈值"))
    print("爆发帧（>2x中位）  %.1f%%   %s" % (m["burst"] * 100, "达到经验阈值" if m["burst"] >= BURST_RATIO else "低于经验阈值"))
    print("逐秒峰均比  %.2f（最高 %.2f）   %s" % (m["ratio"], m["ratio_max"], "达到经验阈值" if m["ratio"] >= PEAK_MEAN_RATIO else "低于经验阈值"))
    print("单帧最大  %.1f   %s" % (m["max"], "达到经验阈值" if m["max"] >= MAX_ENERGY else "低于经验阈值"))
    print("声音  RMS 均值 %.1f dB  峰值 %.1f dB（距满刻度 %.1f dB）  强打击点 %d 个" % (m["rms"], m["peak_db"], -m["peak_db"], m["strong"]))
    print("  打击声 %s" % ("达到经验阈值" if -m["peak_db"] <= AUDIO_HEADROOM and m["strong"] >= 2 else "低于经验阈值——听不出打实了"))
    print("近静止秒 %s" % (m["quiet"] if m["quiet"] else "无"))


def selftest():
    tmp = tempfile.mkdtemp(prefix="fight-metrics-selftest-")
    clip = os.path.join(tmp, "selftest.mp4")
    vf = ("color=c=black:s=320x240:r=24:d=2[v0];"
          "testsrc2=s=320x240:r=24:d=3[v1];"
          "[v0][v1]concat=n=2:v=1:a=0[v]")
    p = subprocess.run(["ffmpeg", "-v", "error", "-y",
                        "-f", "lavfi", "-i", "sine=frequency=440:duration=5",
                        "-filter_complex", vf, "-map", "[v]", "-map", "0:a", "-shortest",
                        "-pix_fmt", "yuv420p", clip],
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    ok = p.returncode == 0 and os.path.exists(clip)
    if not ok:
        # 退化路径：只合画面，不加音轨
        p = subprocess.run(["ffmpeg", "-v", "error", "-y", "-filter_complex", vf,
                            "-map", "[v]", "-pix_fmt", "yuv420p", clip],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        ok = p.returncode == 0 and os.path.exists(clip)
    if not ok:
        print("自检失败：无法合成测试片。")
        print(p.stdout.decode("utf-8", "replace")[:800])
        return 1
    print("自检片已生成：%s" % clip)
    print("预期结果：五项读数都能算出来并给出判定，不报错。\n")
    show("selftest", measure(clip))
    shutil.rmtree(tmp, ignore_errors=True)
    return 0


def main():
    args = [a for a in sys.argv[1:]]
    if not args:
        print(__doc__)
        return 2
    if "--selftest" in args:
        if not require_ffmpeg():
            return 2
        return selftest()
    bad = [a for a in args if a.startswith("-") and a != "--ref"]
    if bad:
        print("未知参数：%s" % "、".join(bad))
        print(__doc__)
        return 2
    if "--ref" in args:
        i = args.index("--ref")
        target, ref = args[:i], args[i + 1:]
        if not target or not ref:
            print("--ref 需要同时给出待检片与参照片。")
            return 2
        print("### 对照标尺：参照片 ###\n")
        for p in ref:
            show("参照：" + os.path.basename(p), measure(p))
        print("\n### 待检成片 ###\n")
        for p in target:
            show(os.path.basename(p), measure(p))
        return 0
    for p in args:
        show(os.path.basename(p), measure(p))
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

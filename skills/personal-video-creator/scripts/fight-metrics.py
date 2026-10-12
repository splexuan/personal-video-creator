# -*- coding: utf-8 -*-
"""成片"打斗感"实测：幅度与打击声。

配合 scripts/motion-audit.py 使用。两者分工：
  motion-audit.py  管"有没有在动"（逐秒运动能量、最长近静止区间、最高点落位、帧复制）
  fight-metrics.py 管"动得够不够大、打没打实"（强度分布、爆发比例、峰均比、音频峰值）

用法：
    python fight-metrics.py <成片1.mp4> [成片2.mp4 ...]
    python fight-metrics.py <成片.mp4> --ref <参照片.mp4>     # 与参照片并排对照

判据见 references/pacing.md 第三节与第七节。依赖 ffmpeg / ffprobe 在 PATH 中。

指标口径：
  运动能量   = 相邻帧差分图的平均灰度（0-255），越高动得越大
  高强度帧   = 运动能量 > 8.0 的帧占比（参照片标尺 24.3%）
  爆发帧     = 运动能量 > 2× 全片中位数的帧占比（参照片标尺 9.3%）
  逐秒峰均比 = 每一秒内最高一帧 ÷ 该秒均值，衡量"一顿一顿"的程度（参照片标尺 2.96）
  音频峰值   = 逐秒采样峰值，距满刻度越小说明打击声越实（参照片 1.6 dB）
"""
import math
import os
import re
import struct
import subprocess
import sys

HI = 8.0          # 高强度帧阈值（运动能量）
HI_RATIO = 0.20   # 及格线：高强度帧占比
BURST_RATIO = 0.09
PEAK_MEAN_RATIO = 2.9
MAX_ENERGY = 50.0
AUDIO_HEADROOM = 3.0


def run(cmd, binary=False):
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return p.stdout if binary else p.stdout.decode("utf-8", "replace")


def motion_series(video, tag="a"):
    # ffmpeg 的 file= 输出不认带盘符的绝对路径（会把盘符当成协议名），
    # 必须给相对路径，因此临时文件统一落在当前工作目录。
    out = "fight_tmp_%s.txt" % tag
    if os.path.exists(out):
        os.remove(out)
    run(["ffmpeg", "-v", "error", "-i", video,
         "-vf", "tblend=all_mode=difference,signalstats,metadata=print:file=%s" % out,
         "-an", "-f", "null", "-"])
    series, t = [], None
    if os.path.exists(out):
        for line in open(out, encoding="utf-8", errors="replace"):
            m = re.match(r"frame:\s*(\d+)\s+pts:\d+\s+pts_time:([0-9.]+)", line)
            if m:
                t = float(m.group(2))
                continue
            m2 = re.search(r"lavfi\.signalstats\.YAVG=([0-9.]+)", line)
            if m2 and t is not None:
                series.append((t, float(m2.group(1))))
                t = None
        os.remove(out)
    return series


def audio_series(video, sr=8000):
    raw = run(["ffmpeg", "-v", "error", "-i", video, "-ac", "1", "-ar", str(sr),
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
    s = sorted(vals)
    return s[min(len(s) - 1, int(len(s) * p))]


def measure(path):
    series = motion_series(path)
    audio = audio_series(path)
    if not series:
        return None
    vals = [v for _, v in series]
    med = pct(vals, .5)
    sec_mean, sec_peak = {}, {}
    for t, v in series:
        s = int(t)
        sec_mean.setdefault(s, []).append(v)
        sec_peak.setdefault(s, []).append(v)
    sm = [(s, sum(a) / len(a)) for s, a in sorted(sec_mean.items())]
    sp = [(s, max(a)) for s, a in sorted(sec_peak.items())]
    ratios = [pk / (mn if mn > 0.01 else 0.01) for (_, mn), (_, pk) in zip(sm, sp)]
    db = [d for _, d, _ in audio]
    pdb = [p for _, _, p in audio]
    return {
        "mean": sum(vals) / len(vals), "med": med, "p90": pct(vals, .9),
        "max": max(vals),
        "hi": sum(1 for v in vals if v > HI) / float(len(vals)),
        "burst": sum(1 for v in vals if v > 2 * med) / float(len(vals)),
        "ratio": sum(ratios) / len(ratios) if ratios else 0,
        "ratio_max": max(ratios) if ratios else 0,
        "quiet": [s for s, m in sm if m < sum(vals) / len(vals) / 3.0],
        "rms": sum(db) / len(db) if db else -99,
        "peak_db": max(pdb) if pdb else -99,
        "strong": sum(1 for p in pdb if p > -3.0),
        "frames": len(vals),
    }


def show(name, m):
    if not m:
        print("%s：读不出数据（检查 ffmpeg 是否在 PATH）" % name)
        return
    print("=" * 70)
    print(name)
    print("=" * 70)
    print("运动能量  均值 %.2f  中位 %.2f  P90 %.2f  最大 %.2f" % (m["mean"], m["med"], m["p90"], m["max"]))
    print("高强度帧（>%.1f）  %.1f%%   %s" % (HI, m["hi"] * 100, "通过" if m["hi"] >= HI_RATIO else "不足"))
    print("爆发帧（>2x中位）  %.1f%%   %s" % (m["burst"] * 100, "通过" if m["burst"] >= BURST_RATIO else "不足"))
    print("逐秒峰均比  %.2f（最高 %.2f）   %s" % (m["ratio"], m["ratio_max"], "通过" if m["ratio"] >= PEAK_MEAN_RATIO else "不足"))
    print("单帧最大  %.1f   %s" % (m["max"], "通过" if m["max"] >= MAX_ENERGY else "不足"))
    print("声音  RMS 均值 %.1f dB  峰值 %.1f dB（距满刻度 %.1f dB）  强打击点 %d 个" % (m["rms"], m["peak_db"], -m["peak_db"], m["strong"]))
    print("  打击声 %s" % ("通过" if -m["peak_db"] <= AUDIO_HEADROOM and m["strong"] >= 2 else "不足——听不出打实了"))
    print("近静止秒 %s" % (m["quiet"] if m["quiet"] else "无"))


def main():
    args = [a for a in sys.argv[1:]]
    if not args:
        print(__doc__)
        return 2
    if "--ref" in args:
        i = args.index("--ref")
        target, ref = args[:i], args[i + 1:]
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
motion-audit.py —— 成片运动密度客观测量

用途：判断一条"本该一直在动"的短片（打斗、追逐、群战）是否节奏失败。
对应方法：references/pacing.md 第七节（成片实测）。

依赖：ffmpeg 需在 PATH 中；有 ffprobe 更准，没有时自动退回解析 ffmpeg -i 的输出。

用法：
    python motion-audit.py <video.mp4> [--threshold 1.5] [--ratio 0.333] [--event 7-9]
    python motion-audit.py --selftest          # 用合成片自检整条链路

输出：
    1) 逐秒运动能量表（含直方条）
    2) 全片统计（均值 / 中位数 / 分位）
    3) 最长"近静止"连续区间 —— 超过 2 秒即判定节奏失败
    4) 运动能量最高点所在秒 —— 应落在决胜段；落在别处说明重音配错
    5) 帧复制检查（mpdecimate）—— 保留帧数 == 总帧数，说明"慢"是内容本身造成的

判据（详见 pacing.md）：
    - 任何连续 >= 2 秒、运动能量持续低于（全片均值 x ratio）的区间 -> 节奏失败
    - 全片运动能量最高点应当落在决胜段落

注意：阈值是**经验阈值**，由少量样本标定，且随分辨率、帧率、画幅漂移。
它擅长排序（哪一段最静、重音落在哪里），不宜当成跨片对比的绝对及格线。
"""

import os
import re
import shutil
import statistics
import subprocess
import sys
import tempfile


def require_ffmpeg():
    missing = [b for b in ("ffmpeg",) if shutil.which(b) is None]
    if missing:
        print("缺少依赖：%s 不在 PATH 中。" % "、".join(missing))
        print("安装 ffmpeg 后再试（macOS: brew install ffmpeg；Windows: winget install ffmpeg；")
        print("Debian/Ubuntu: sudo apt install ffmpeg），或把可执行文件目录加入 PATH。")
        print("安装后可用 --selftest 验证：python motion-audit.py --selftest")
        return False
    return True


def require_file(video):
    if not os.path.isfile(video):
        print("找不到文件：%s" % video)
        return False
    return True


def run(cmd, cwd=None):
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd)
    return p.stdout.decode("utf-8", "replace")


def probe(video):
    """优先 ffprobe；没有 ffprobe（剪映等只带 ffmpeg）时退回解析 ffmpeg -i 的输出。"""
    info = {}
    if shutil.which("ffprobe"):
        out = run(["ffprobe", "-v", "error",
                   "-select_streams", "v:0",
                   "-show_entries", "format=duration",
                   "-show_entries", "stream=width,height,r_frame_rate,nb_frames",
                   "-of", "default=noprint_wrappers=1", video])
        for line in out.splitlines():
            if "=" in line:
                k, v = line.split("=", 1)
                info[k.strip()] = v.strip()
    if not info.get("width"):
        out = run(["ffmpeg", "-hide_banner", "-i", video])
        m = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", out)
        if m:
            info["duration"] = str(int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)))
        m = re.search(r",\s*(\d{2,5})x(\d{2,5})[\s,\[]", out)
        if m:
            info["width"], info["height"] = m.group(1), m.group(2)
        m = re.search(r"(\d+(?:\.\d+)?)\s*fps", out)
        if m:
            info["r_frame_rate"] = m.group(1) + "/1"
    return info


def motion_series(video):
    """逐帧运动能量：相邻帧差分图的平均灰度（0-255）。"""
    with tempfile.TemporaryDirectory() as td:
        # 在临时目录里用相对文件名，避开 ffmpeg 把路径里的盘符冒号当成选项分隔符
        outfile = os.path.join(td, "motion.txt")
        run(["ffmpeg", "-v", "error", "-i", video,
             "-vf", "tblend=all_mode=difference,signalstats,"
                    "metadata=print:file=motion.txt",
             "-an", "-f", "null", "-"], cwd=td)
        if not os.path.exists(outfile):
            return []
        series = []
        cur = None
        for line in open(outfile, encoding="utf-8", errors="replace"):
            line = line.rstrip("\n")
            head = re.match(r"frame:(\d+)\s+pts:\d+\s+pts_time:([0-9.]+)", line)
            if head:
                cur = [float(head.group(2)), None]
                series.append(cur)
                continue
            if line.startswith("lavfi.signalstats.YAVG=") and cur is not None and cur[1] is None:
                cur[1] = float(line.split("=", 1)[1])
        return [s for s in series if s[1] is not None]


def duplicate_check(video):
    """用 mpdecimate 判断是否存在被复制的近重复帧。返回 None 表示这套 ffmpeg 不支持，别当成"零重复"。"""
    out = run(["ffmpeg", "-v", "info", "-i", video,
               "-vf", "mpdecimate=hi=64*8:lo=64*5:frac=0.28,showinfo",
               "-an", "-f", "null", "-"])
    if "No such filter" in out or "Error opening output" in out:
        return None
    kept = len(re.findall(r"n:\s*\d+.*pts_time", out))
    return kept or None


def selftest():
    """合成一条 6 秒片子：前 3 秒全静止，后 3 秒有运动，验证整条链路。"""
    tmp = tempfile.mkdtemp(prefix="motion-audit-selftest-")
    clip = os.path.join(tmp, "selftest.mp4")
    vf = ("color=c=black:s=320x240:r=24:d=3[v0];"
          "testsrc2=s=320x240:r=24:d=3[v1];"
          "[v0][v1]concat=n=2:v=1:a=0[v]")
    p = subprocess.run(["ffmpeg", "-v", "error", "-y",
                        "-filter_complex", vf, "-map", "[v]",
                        "-pix_fmt", "yuv420p", clip],
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if p.returncode != 0 or not os.path.exists(clip):
        print("自检失败：无法合成测试片。")
        print(p.stdout.decode("utf-8", "replace")[:800])
        return 1
    print("自检片已生成：%s" % clip)
    print("预期结果：前 3 秒被标为近静止，第 3 秒后出现运动。\n")
    rc = audit(clip)
    shutil.rmtree(tmp, ignore_errors=True)
    return rc


def audit(video, threshold=None, ratio=0.333, event=None):
    info = probe(video)
    total_frames = 0
    try:
        total_frames = int(float(info.get("nb_frames", "0") or 0))
    except ValueError:
        total_frames = 0
    fps = 24.0
    raw_fps = info.get("r_frame_rate", "")
    if "/" in raw_fps:
        try:
            num, den = raw_fps.split("/")
            if float(den) != 0:
                fps = float(num) / float(den)
        except ValueError:
            pass
    duration = info.get("duration", "?")
    if not total_frames:
        try:
            total_frames = int(round(float(duration) * fps))
        except (TypeError, ValueError):
            total_frames = 0

    print("=" * 62)
    print("文件  : %s" % os.path.basename(video))
    print("规格  : %sx%s  %s fps  时长 %s s  总帧 %s"
          % (info.get("width", "?"), info.get("height", "?"),
             info.get("r_frame_rate", "?"), duration, total_frames or "?"))
    print("=" * 62)

    series = motion_series(video)
    if not series:
        print("未能计算运动能量：文件可能没有视频流，或编码无法解码。")
        return 1

    values = [v for _, v in series]
    # 单帧尖峰＝切镜或闪帧：两侧帧都很低，只有这一帧暴涨。计阈值与峰值前先剔掉，
    # 否则切镜会被当成"运动最高点"，把重音判定和近静止判定一起带偏。
    med_all = statistics.median(values)
    cuts = set()
    for i in range(1, len(values) - 1):
        v = values[i]
        if v > max(med_all * 6, 25) and min(values[i - 1], values[i + 1]) < v / 4:
            cuts.add(i)
    clean = [v for i, v in enumerate(values) if i not in cuts]
    mean = sum(clean) / len(clean)
    med = statistics.median(clean)
    ordered = sorted(clean)
    p10 = ordered[len(clean) // 10]
    p90 = ordered[len(clean) * 9 // 10]
    cut = threshold if threshold is not None else mean * ratio

    print()
    print("全片运动能量：均值 %.2f  中位数 %.2f  P10 %.2f  P90 %.2f  最大 %.2f"
          % (mean, med, p10, p90, max(values)))
    print("近静止判定阈值：%.2f  (= 均值 x %.3f%s)"
          % (cut, ratio, "，已由 --threshold 覆盖" if threshold is not None else ""))
    print("口径：经验阈值，随分辨率与帧率漂移；用于排序与定位，不做跨片绝对比较。")
    if cuts:
        print("检测到 %d 处切镜/闪帧（%s），已从均值、阈值与最高点判定中排除。"
              % (len(cuts), "、".join("%.2fs" % series[i][0] for i in sorted(cuts))))
    print()

    secs = {}
    for i, (t, v) in enumerate(series):
        if i in cuts:
            continue
        secs.setdefault(int(t), []).append(v)
    print("秒  |  均值 |  峰值 | 直方（每 # = 0.5 单位）")
    for s in sorted(secs):
        bucket = secs[s]
        m = sum(bucket) / len(bucket)
        flag = "  <<< 近静止" if m < cut else ""
        print("%3d | %6.2f | %6.2f | %s%s" % (s, m, max(bucket), "#" * int(m * 2), flag))

    best = (0, 0.0, 0.0)
    run_len = 0
    start = 0.0
    for i, (t, v) in enumerate(series):
        if i in cuts:
            continue
        if v < cut:
            if run_len == 0:
                start = t
            run_len += 1
            if run_len > best[0]:
                best = (run_len, start, t)
        else:
            run_len = 0

    peak_t, peak_v = max(((t, v) for i, (t, v) in enumerate(series) if i not in cuts),
                         key=lambda x: x[1])

    print()
    print("-" * 62)
    print("结论")
    print("-" * 62)
    print("最长近静止区间：%.2f 秒（%.2fs -> %.2fs）" % (best[0] / fps, best[1], best[2]))
    if best[0] / fps >= 2.0:
        print("  [失败] 超过 2 秒 —— 节奏失败，回到 pacing.md 第二节补动作密度。")
    elif best[0] / fps >= 1.0:
        print("  [警告] 1-2 秒 —— 若落在决胜段，仍建议拆细该段描述。")
    else:
        print("  [通过] 全片没有明显的静止区间。")

    print("运动能量最高点：%.2f 秒（%.2f）" % (peak_t, peak_v))
    if event:
        a, b = event
        seg = [v for t, v in series if a <= t <= b]
        seg_mean = sum(seg) / len(seg) if seg else 0.0
        inside = a <= peak_t <= b
        print("事件段 %.1f–%.1f 秒：均值 %.2f" % (a, b, seg_mean))
        if inside:
            print("  重音落位：[通过] 最高点落在事件段内。")
        else:
            print("  重音落位：[错位] 最高点在 %.2f 秒，事件段最平 —— 运镜或无关动作抢了重音，"
                  "把运镜挪到事件前，或让它在事件后 0.5 秒再启动。" % peak_t)
    else:
        print("  检查这一秒是不是决胜段落。若最高点是转场、布料掠过或无关动作，说明重音配错。")

    kept = duplicate_check(video)
    if kept is None:
        print("帧复制检查：跳过 —— 当前 ffmpeg 没有 mpdecimate 滤镜（剪映等精简版常见），"
              "无法判断是否存在重复帧。")
    else:
        print("帧复制检查：mpdecimate 保留 %s 帧 / 总 %s 帧" % (kept, total_frames or "?"))
        if total_frames and kept >= total_frames:
            print("  [说明] 无重复帧 —— '慢' 不是编码或补帧造成的，是内容本身的动作密度不足。")
        elif total_frames:
            print("  [说明] 存在 %d 帧近乎重复，可能叠加了播放端的减速或补帧。" % (total_frames - kept))

    print()
    print("注意：本测量只能判断『动得够不够』，不能判断『打得对不对』。")
    print("      受力方向、接触点与人体结构仍需按 action-craft.md 看画面核对。")
    print("      情感戏、静态风景、长镜头等本就不追求高运动量的类型不适用本判据。")
    return 0


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    if "--selftest" in sys.argv:
        if not require_ffmpeg():
            return 2
        return selftest()

    video = None
    threshold = None
    ratio = 0.333
    event = None
    i = 1
    while i < len(sys.argv):
        a = sys.argv[i]
        if a == "--threshold" and i + 1 < len(sys.argv):
            threshold = float(sys.argv[i + 1]); i += 2; continue
        if a == "--ratio" and i + 1 < len(sys.argv):
            ratio = float(sys.argv[i + 1]); i += 2; continue
        if a == "--event" and i + 1 < len(sys.argv):
            m = re.fullmatch(r"([0-9.]+)[-–~]([0-9.]+)", sys.argv[i + 1])
            if not m:
                print("--event 格式应为 7-9（秒）"); return 2
            event = (float(m.group(1)), float(m.group(2))); i += 2; continue
        if a.startswith("-"):
            print("未知参数：%s" % a)
            print(__doc__)
            return 2
        video = a
        i += 1

    if not video:
        print(__doc__)
        return 2
    if not require_ffmpeg() or not require_file(video):
        return 2
    return audit(video, threshold, ratio, event)


if __name__ == "__main__":
    sys.exit(main())

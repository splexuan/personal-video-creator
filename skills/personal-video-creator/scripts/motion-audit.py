#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
motion-audit.py —— 成片运动密度客观测量

用途：判断一条"本该一直在动"的短片（打斗、追逐、群战）是否节奏失败。
对应方法：references/pacing.md 第六节。

依赖：ffmpeg / ffprobe 需在 PATH 中。本脚本只用标准库。

用法：
    python motion-audit.py <video.mp4> [--threshold 1.5] [--ratio 0.333]

输出：
    1) 逐秒运动能量表（含直方条）
    2) 全片统计（均值 / 中位数 / 分位）
    3) 最长"近静止"连续区间 —— 超过 2 秒即判定节奏失败
    4) 运动能量最高点所在秒 —— 应落在决胜段；落在别处说明重音配错
    5) 帧复制检查（mpdecimate）—— 保留帧数 == 总帧数，说明"慢"是内容本身造成的

判据（详见 pacing.md）：
    - 任何连续 >= 2 秒、运动能量持续低于（全片均值 x ratio）的区间 -> 节奏失败
    - 全片运动能量最高点应当落在决胜段落
"""

import os
import re
import sys
import statistics
import subprocess
import tempfile


def run(cmd, cwd=None):
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd)
    return p.stdout.decode("utf-8", "replace")


def probe(video):
    out = run(["ffprobe", "-v", "error",
               "-select_streams", "v:0",
               "-show_entries", "format=duration",
               "-show_entries", "stream=width,height,r_frame_rate,nb_frames",
               "-of", "default=noprint_wrappers=1", video])
    info = {}
    for line in out.splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            info[k.strip()] = v.strip()
    return info


def motion_series(video, tag_field="lavfi.signalstats.YAVG"):
    """逐帧运动能量：相邻帧差分图的平均灰度（0-255）。"""
    with tempfile.TemporaryDirectory() as td:
        # 在临时目录里用相对文件名，避开 ffmpeg 把路径里的盘符冒号当成选项分隔符
        outfile = os.path.join(td, "motion.txt")
        # tblend=difference 求相邻帧差分，signalstats 给出差分图的 YAVG
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
            if line.startswith(tag_field + "=") and cur is not None and cur[1] is None:
                cur[1] = float(line.split("=", 1)[1])
        return [s for s in series if s[1] is not None]


def duplicate_check(video):
    """用 mpdecimate 判断是否存在被复制的近重复帧。"""
    out = run(["ffmpeg", "-v", "info", "-i", video,
               "-vf", "mpdecimate=hi=64*8:lo=64*5:frac=0.28,showinfo",
               "-an", "-f", "null", "-"])
    kept = len(re.findall(r"n:\s*\d+.*pts_time", out))
    return kept


def flat_script_element_hits(video, ffmpeg_bin="ffmpeg"):
    return None  # 占位：稿件层面的检查由人工按 pacing.md 第三节执行


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2

    video = sys.argv[1]
    threshold = None
    ratio = 0.333
    for i, a in enumerate(sys.argv):
        if a == "--threshold" and i + 1 < len(sys.argv):
            threshold = float(sys.argv[i + 1])
        if a == "--ratio" and i + 1 < len(sys.argv):
            ratio = float(sys.argv[i + 1])

    info = probe(video)
    total_frames = int(float(info.get("nb_frames", "0") or 0))
    fps = 24.0
    raw_fps = info.get("r_frame_rate", "")
    if "/" in raw_fps:
        try:
            num, den = raw_fps.split("/")
            if float(den) != 0:
                fps = float(num) / float(den)
        except ValueError:
            pass
    print("=" * 62)
    print("文件  : %s" % os.path.basename(video))
    print("规格  : %sx%s  %s fps  时长 %s s  总帧 %s"
          % (info.get("width", "?"), info.get("height", "?"),
             info.get("r_frame_rate", "?"), info.get("duration", "?"),
             total_frames or "?"))
    print("=" * 62)

    series = motion_series(video)
    if not series:
        print("未能计算运动能量，请确认 ffmpeg 可用且文件可解码。")
        return 1

    values = [v for _, v in series]
    mean = sum(values) / len(values)
    med = statistics.median(values)
    p10 = sorted(values)[len(values) // 10]
    p90 = sorted(values)[len(values) * 9 // 10]
    cut = threshold if threshold is not None else mean * ratio

    print()
    print("全片运动能量：均值 %.2f  中位数 %.2f  P10 %.2f  P90 %.2f  最大 %.2f"
          % (mean, med, p10, p90, max(values)))
    print("近静止判定阈值：%.2f  (= 均值 x %.3f%s)"
          % (cut, ratio, "，已由 --threshold 覆盖" if threshold is not None else ""))
    print()

    # 逐秒表
    secs = {}
    for t, v in series:
        secs.setdefault(int(t), []).append(v)
    print("秒  |  均值 |  峰值 | 直方（每 # = 0.5 单位）")
    for s in sorted(secs):
        a = secs[s]
        m = sum(a) / len(a)
        flag = "  <<< 近静止" if m < cut else ""
        print("%3d | %6.2f | %6.2f | %s%s" % (s, m, max(a), "#" * int(m * 2), flag))

    # 最长近静止区间
    best = (0, 0.0, 0.0)
    run_len = 0
    start = 0.0
    for t, v in series:
        if v < cut:
            if run_len == 0:
                start = t
            run_len += 1
            if run_len > best[0]:
                best = (run_len, start, t)
        else:
            run_len = 0

    # 最高点
    peak_t, peak_v = max(series, key=lambda x: x[1])

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
    print("  检查这一秒是不是决胜段落。若最高点是转场、布料掠过或无关动作，说明重音配错。")

    kept = duplicate_check(video)
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


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""离线测试：不依赖 ffmpeg，用桩函数喂数据，验证两个实测脚本的解析与统计。

用途：装了 ffmpeg 之前也能验证代码没坏；改过解析逻辑后先跑这个。
    python scripts/test_scripts.py
"""

import importlib.util
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"),
                                                  os.path.join(HERE, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


MOTION_TXT = "".join(
    "frame:%d pts:%d pts_time:%.3f\n"
    "lavfi.signalstats.YAVG=%.3f\n" % (i, i * 1000, i / 24.0, v)
    for i, v in enumerate(
        [0.4] * 24 + [9.0] * 24 + [3.0] * 24 + [2.0] * 24
    )
)


def stub_motion(mod, values):
    """替掉 ffmpeg 调用：把运动能量表写进 cwd，再让原函数照常解析。"""
    text = "".join(
        "frame:%d pts:%d pts_time:%.3f\n"
        "lavfi.signalstats.YAVG=%.3f\n" % (i, i * 1000, i / 24.0, v)
        for i, v in enumerate(values)
    )

    class FakeRun:
        def __call__(self, cmd, cwd=None, binary=False, **kw):
            if cmd[0] == "ffmpeg" and any("metadata=print" in str(c) for c in cmd):
                target = "motion.txt"
                for c in cmd:
                    if "file=" in str(c):
                        target = str(c).split("file=")[1]
                with open(os.path.join(cwd or ".", target), "w", encoding="utf-8") as f:
                    f.write(text)
                return "" if not binary else b""
            if cmd[0] == "ffmpeg" and any("mpdecimate" in str(c) for c in cmd):
                return "".join("[Parsed_showinfo_1 @ 0x1] n:%5d pts: 1 pts_time:0.1\n" % i
                               for i in range(len(values)))
            return "" if not binary else b"\x00\x00" * 8000

    mod.run = FakeRun()
    mod.probe = lambda video: {"width": "720", "height": "1280",
                               "r_frame_rate": "24/1", "nb_frames": str(len(values)),
                               "duration": str(len(values) / 24.0)}


def test_offline():
    ok = True

    # ---- motion-audit ----
    ma = load("motion-audit")
    values = [0.4] * 24 + [9.0] * 24 + [3.0] * 24 + [2.0] * 24
    stub_motion(ma, values)
    series = ma.motion_series("dummy.mp4")
    assert len(series) == len(values), "运动能量帧数解析错误"
    assert abs(series[30][1] - 9.0) < 1e-6, "运动能量取值解析错误"
    rc = ma.audit("dummy.mp4")
    assert rc == 0, "audit 返回非 0"
    print("[通过] motion-audit：逐帧解析、近静止区间、最高点、帧复制检查")

    # ---- fight-metrics ----
    fm = load("fight-metrics")
    stub_motion(fm, values)
    m = fm.measure("dummy.mp4")
    assert m is not None, "measure 返回空"
    assert m["frames"] == len(values), "帧数不符"
    assert 0 <= m["hi"] <= 1 and 0 <= m["burst"] <= 1, "占比越界"
    assert m["max"] >= m["med"], "最大值小于中位数"
    assert fm.pct([1, 2, 3, 4], 0.5) == 2.5, "百分位未插值"
    fm.show("dummy", m)
    print("[通过] fight-metrics：五项读数、百分位插值、报告输出")

    # ---- 缺依赖时的行为 ----
    if ma.require_ffmpeg() is False:
        print("[通过] 缺失 ffmpeg 时给出安装指引而不是抛异常")
        print("[跳过] 真实解码路径需要 ffmpeg，请在有 ffmpeg 的机器上跑 --selftest")
    else:
        print("[通过] 本机有 ffmpeg，可继续跑 --selftest 做端到端验证")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(test_offline())

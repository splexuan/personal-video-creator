#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""离线测试：不依赖 ffmpeg，用桩函数喂数据，验证两个实测脚本的解析与统计。

用途：装了 ffmpeg 之前也能验证代码没坏；改过解析逻辑后先跑这个。
    python scripts/test_scripts.py
"""

import importlib.util
import os
import re
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

    # ---- lint-prompt ----
    lp = load("lint-prompt")
    bad, _, _ = lp.lint(lp.BAD, images=2, action=True)
    good, _, _ = lp.lint(lp.GOOD, images=2, action=True)
    bad_fail = {r[1] for r in bad if r[0] == lp.FAIL}
    good_fail = [r for r in good if r[0] == lp.FAIL]
    assert {"残留", "时间戳", "素材指派"} <= bad_fail, "lint 漏报了反例：%s" % bad_fail
    assert not good_fail, "lint 对正例误报：%s" % good_fail
    # 真实稿件回归：fixtures 里每条都记录预期结论
    import os
    fix_dir = os.path.join(HERE, "fixtures")
    # (images, 预期 FAIL 数, 必含 FAIL 类别, 必含 WARN 类别, 说明)
    expect = {
        "english-annotations.txt": (None, 0, set(), set(), "英文机位注释不算占位符"),
        "rework-duration.txt": (None, 0, set(), set(), "复刻稿里的「参考视频 30 秒」不当作声明时长"),
        "nested-timeline.txt": (None, 0, set(), set(), "镜头内嵌套子时间线不报断档"),
        "leftover-placeholder.txt": (None, 7, {"残留"}, {"时间戳", "负向约束"}, "模板说明与占位符必须报出来"),
        "broken-timeline.txt": (None, 2, {"时间戳"}, set(), "断档与总时长不符各报一条"),
        "zh-subtitle.txt": (1, 0, set(), set(), "合法画面字幕不算字段标题、不与约束冲突"),
        "conflict-subtitle.txt": (None, 1, {"约束冲突"}, set(), "「不要字幕」与正文【】字幕必须对撞"),
        "conflict-dialogue-music.txt": (None, 2, {"约束冲突"}, set(), "「不要台词／不要音乐」与正文内容必须对撞"),
        "over-long-duration.txt": (None, 0, set(), {"平台上限"}, "45 秒超出单次 4–30 秒给警告"),
    }
    for name, (imgs, want_fail, cats, warns, why) in expect.items():
        body = open(os.path.join(fix_dir, name), encoding="utf-8").read()
        res, _, _ = lp.lint(body, images=imgs)
        got_cats = {r[1] for r in res if r[0] == lp.FAIL}
        got_warns = {r[1] for r in res if r[0] == lp.WARN}
        got = sum(1 for r in res if r[0] == lp.FAIL)
        assert got == want_fail and cats <= got_cats and warns <= got_warns, \
            "%s 预期 FAIL=%d 含 %s、WARN 含 %s，实际 FAIL=%d %s / WARN %s" % (
                name, want_fail, cats, warns, got, got_cats, got_warns)
        print("[通过] 回归 %-26s FAIL=%d  %s" % (name, got, why))

    # 参考图超过上限 30 张必须判 FAIL
    over, _, _ = lp.lint("@图片1 男主。@图片2 女主。12 秒。不要字幕。", images=40)
    assert any(r[0] == lp.FAIL and r[1] == "平台上限" for r in over), "参考图 40 张未报 FAIL"
    print("[通过] 回归 参考图 40 张              FAIL=1  超上限必须拦下")

    # ---- 新增检查：单元总数、一句多运镜 ----
    res, _, _ = lp.lint(open(os.path.join(fix_dir, "action-no-units.txt"), encoding="utf-8").read(),
                        images=0, action=True)
    warns = {r[1] for r in res if r[0] == lp.WARN}
    assert "密度声明" in warns, "动作稿没写单元总数时未告警"
    res, _, _ = lp.lint(open(os.path.join(fix_dir, "two-moves-one-shot.txt"), encoding="utf-8").read(),
                        images=1)
    warns = {r[1] for r in res if r[0] == lp.WARN}
    assert "运镜" in warns, "一句多运镜未告警"
    print("[通过] 定向回归：缺单元总数、一句多运镜都能报出")

    # ---- 目录一致性：catalog 与 index 的条数、★ 数必须对得上 ----
    lib = os.path.join(os.path.dirname(HERE), "references", "external-library")
    cat = open(os.path.join(lib, "catalog.md"), encoding="utf-8").read()
    total = stars = 0
    for sec in re.split(r"\n## ", cat)[1:]:
        name = sec.split("\n")[0]
        m = re.match(r"(.+)（(\d+) 条）", name)
        assert m, "分类标题缺少条数：%s" % name
        rows = [l for l in sec.split("\n")
                if l.startswith("| ") and not l.startswith("| 编号") and not l.startswith("| ---")]
        assert len(rows) == int(m.group(2)), "%s 标题写 %s 条，实际 %d 行" % (name, m.group(2), len(rows))
        total += len(rows)
        stars += sum(1 for r in rows if "★" in r.split("|")[1])
    assert total == 852, "目录合计应为 852，实际 %d" % total
    assert stars == 66, "★ 应为 66 条，实际 %d" % stars
    assert "未分类" not in cat.replace("原「未分类」", ""), "catalog 仍有未分类条目"
    idx = open(os.path.join(lib, "index.md"), encoding="utf-8").read()
    assert "| 未分类 |" not in idx, "index 仍有未分类行"
    assert sum(int(x) for x in re.findall(r"\| \d+ \| (\d+) \| `samples", idx)) == 852, "index 候选总数合计不是 852"
    print("[通过] 目录一致性：852 条、66 条 ★、分类计数与索引一致")

    # ---- evals 结构 ----
    import json
    ev = json.load(open(os.path.join(os.path.dirname(HERE), "evals", "evals.json"), encoding="utf-8"))
    skill_md = open(os.path.join(os.path.dirname(HERE), "SKILL.md"), encoding="utf-8").read()
    assert ev["skill_name"] in skill_md, "evals 的 skill_name 与 SKILL.md 不一致"
    ids = [e["id"] for e in ev["evals"]]
    assert len(ids) == len(set(ids)), "评测 id 有重复：%s" % ids
    assert len(ids) >= 8, "评测条目过少：%d" % len(ids)
    for e in ev["evals"]:
        assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", e["id"]), "id 不是 kebab-case：%s" % e["id"]
        assert 1 <= int(e["stage"]) <= 6, "%s 的 stage 越界" % e["id"]
        assert e["prompt"].strip() and e["expected_output"].strip(), "%s 缺 prompt/expected_output" % e["id"]
        assert len(e["expectations"]) >= 3, "%s 的 expectations 少于 3 条" % e["id"]
        assert all(isinstance(x, str) and x.strip() for x in e["expectations"]), "%s 有空的 expectation" % e["id"]
    print("[通过] evals：%d 条，id 唯一、stage 1-6、每条 ≥3 条可判定期望" % len(ids))

    # ---- 缺依赖时的行为 ----
    if ma.require_ffmpeg() is False:
        print("[通过] 缺失 ffmpeg 时给出安装指引而不是抛异常")
        print("[跳过] 真实解码路径需要 ffmpeg，请在有 ffmpeg 的机器上跑 --selftest")
    else:
        print("[通过] 本机有 ffmpeg，可继续跑 --selftest 做端到端验证")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(test_offline())

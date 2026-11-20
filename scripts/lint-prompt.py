#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lint-prompt.py —— 提示词交付前的机械检查

只查"不需要判断力、但最容易漏掉"的项目，判断力留给提示词自检与看片。

检查项：
  1 模板残留：使用说明、提示语、方括号占位符
  2 时间戳：是否连续、有无断档或重叠、结束时间是否等于声明时长
  3 素材标签：编号是否从 1 连续、数量是否与实际上传数一致、有没有无依据的 @1 写法
  4 多素材指派：有没有用"分别是"句式（官方点名的失败写法）
  5 字段标题：是否还在用 【】，与画面字幕同符号
  6 负向约束：是否集中在结尾，而不是散在前半段
  7 空栏目：只剩字段名、没有内容的行
  8 动作片（--action）：禁用静态词、动作动词粗估

用法：
    python lint-prompt.py draft.txt
    python lint-prompt.py draft.txt --duration 12 --images 2 --action
    python lint-prompt.py --selftest

退出码：0 = 无阻断问题；1 = 有 FAIL；2 = 参数或文件错误。

边界：本脚本只判"形式"，不判"好不好看"。密度是否真够、受力对不对、身份会不会漂，
仍需 prompt-self-check 与成片核对；动作动词计数只是粗估，不等于动作单元数。
"""

import os
import re
import sys

PASS, WARN, FAIL = "PASS", "WARN", "FAIL"


def read(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def extract_ranges(text):
    """返回 [(start, end, 原文), ...]，支持 [mm:ss-mm:ss]、0-4s、第 3 秒到第 7 秒。"""
    found = []

    for m in re.finditer(r"\[\s*(\d{1,2}):(\d{2})\s*[-–—~至]\s*(\d{1,2}):(\d{2})\s*\]", text):
        a = int(m.group(1)) * 60 + int(m.group(2))
        b = int(m.group(3)) * 60 + int(m.group(4))
        found.append((a, b, m.group(0)))

    # 0-4s / 0—4 秒 / 8 秒到 11 秒；单位可以只写在后一个数字后
    for m in re.finditer(r"(\d{1,3}(?:\.\d+)?)\s*(?:s|秒)?\s*[-–—~至]\s*(\d{1,3}(?:\.\d+)?)\s*(?:s|秒)", text):
        a, b = float(m.group(1)), float(m.group(2))
        if b > a and b <= 1800:          # 排除 2008-2012 这类年份
            found.append((a, b, m.group(0)))

    for m in re.finditer(r"第\s*(\d+(?:\.\d+)?)\s*秒\s*(?:到|至|—|-|~)\s*第?\s*(\d+(?:\.\d+)?)\s*秒", text):
        found.append((float(m.group(1)), float(m.group(2)), m.group(0)))

    seen, uniq = set(), []
    for a, b, raw in found:
        key = (round(a, 2), round(b, 2))
        if key in seen:
            continue
        seen.add(key)
        uniq.append((a, b, raw))
    return uniq


def declared_duration(text):
    for pat in (r"(?:总时长|全片时长|成片时长|时长|片长)\s*[：:为]?\s*(\d+(?:\.\d+)?)\s*秒",
                r"(\d+(?:\.\d+)?)\s*秒\s*的"):
        m = re.search(pat, text)
        if m:
            return float(m.group(1)), m.group(0)
    m = re.search(r"(\d+(?:\.\d+)?)\s*秒", text)
    if m:
        return float(m.group(1)), m.group(0)
    return None, None


def check_residue(text):
    out = []
    pairs = ((r"模板使用说明", FAIL, "模板使用说明未删"),
             (r"删除这句说明|删除本行|按本片需要填写|填完后删除", FAIL, "模板提示语未删"),
             (r"\[\[?[^\]\n]{1,24}\]\]?", FAIL, "方括号占位符残留"))
    for pat, level, msg in pairs:
        for m in re.finditer(pat, text):
            hit = m.group(0)
            inner = hit.strip("[]")
            # 时间戳、镜号、英文区间不算占位符
            if re.fullmatch(r"[\d:.\-–—~ ]+s?", inner) or re.fullmatch(r"[A-Za-z0-9 .\-_/]+", inner):
                continue
            # markdown 链接 [文字](地址) 不算占位符
            if text[m.end():m.end() + 1] == "(":
                continue
            line = text[:m.start()].count("\n") + 1
            out.append((level, "残留", "%s（第 %d 行：%s）" % (msg, line, hit[:30])))
    if not any(r[1] == "残留" for r in out):
        out.append((PASS, "残留", "无模板说明、提示语与占位符"))
    return out


def check_timeline(text, duration):
    out = []
    ranges = extract_ranges(text)
    if not ranges:
        out.append((WARN, "时间戳", "未发现时间戳；单镜连续描述可忽略，多段结构应补"))
        return out

    total = len(ranges)
    maximal = [r for r in ranges
               if not any(o is not r and o[0] <= r[0] and r[1] <= o[1] and (o[1] - o[0]) > (r[1] - r[0])
                          for o in ranges)]
    nested = total - len(maximal)
    ranges = sorted(maximal, key=lambda r: r[0])
    if nested:
        out.append((PASS, "时间戳", "有 %d 段子时间线嵌套在镜头内，不参与首尾相接检查" % nested))
    if ranges[0][0] > 0.01:
        out.append((WARN, "时间戳", "首段从 %.1fs 开始，不是 0" % ranges[0][0]))

    for prev, cur in zip(ranges, ranges[1:]):
        if cur[0] > prev[1] + 0.01:
            out.append((FAIL, "时间戳", "断档：%.1fs → %.1fs（%s 与 %s 之间）" % (prev[1], cur[0], prev[2], cur[2])))
        elif cur[0] < prev[1] - 0.01:
            out.append((WARN, "时间戳", "重叠：%s 与 %s" % (prev[2], cur[2])))

    end = max(r[1] for r in ranges)
    if duration is None:
        out.append((WARN, "时间戳", "结尾 %.1fs，但没找到声明时长" % end))
    elif abs(end - duration) > 0.5:
        out.append((FAIL, "时间戳", "结尾 %.1fs ≠ 声明 %.1fs，差 %.1fs" % (end, duration, end - duration)))
    else:
        out.append((PASS, "时间戳", "%d 段首尾相接，合计 %.1fs" % (len(ranges), end)))
    return out


def check_labels(text, images):
    out = []
    pat = re.compile(r"@\s*(图片|Image|视频|Video|音频|Audio)\s*(\d+)", re.I)
    buckets = {}
    for m in pat.finditer(text):
        buckets.setdefault(m.group(1).lower(), set()).add(int(m.group(2)))

    img = buckets.get("图片", set()) | buckets.get("image", set())
    if img:
        if min(img) < 1:
            out.append((FAIL, "素材标签", "编号从 0 开始：%s" % sorted(img)))
        if sorted(img) != list(range(1, max(img) + 1)):
            out.append((WARN, "素材标签", "编号不连续：%s" % sorted(img)))
        if images is not None and len(img) != images:
            out.append((FAIL, "素材标签", "标签 %d 个，实际上传 %d 张" % (len(img), images)))
        elif images is None:
            out.append((WARN, "素材标签", "图像标签 %d 个，未给 --images 无法核对数量" % len(img)))
        else:
            out.append((PASS, "素材标签", "图像标签 %d 个，与实际上传一致" % len(img)))
    else:
        out.append((PASS if images in (None, 0) else FAIL, "素材标签",
                    "没有图像标签" if images in (None, 0) else "声明了 %d 张参考图，但正文没有任何 @图片N" % images))

    bad = re.findall(r"@\s*(?:\d+|图\s*\d+)(?![\d])", text)
    if bad:
        out.append((WARN, "素材标签", "疑似无依据写法 %s，应为 @图片1 / @Image1" % "、".join(sorted(set(bad))[:3])))
    if re.search(r"分别(是|为)", text):
        out.append((FAIL, "素材指派", "出现\"分别是\"句式；官方点名会混淆角色，改成一素材一行"))
    return out


def check_headings(text):
    out = []
    if "【" in text or "】" in text:
        n = text.count("【")
        out.append((WARN, "字段标题", "仍有 %d 处 【】；它与画面字幕同符号，建议改 ▍字段" % n))
    else:
        out.append((PASS, "字段标题", "未使用 【】"))
    lines = text.split("\n")
    field = re.compile(r"^\s*[^\s：:#\-*>|▍]{1,14}\s*[：:]\s*$")
    empty = []
    for i, line in enumerate(lines):
        if not field.match(line):
            continue
        nxt = next((l for l in lines[i + 1:] if l.strip()), None)
        if nxt is None or field.match(nxt):
            empty.append(i + 1)
    if empty:
        out.append((WARN, "空栏目", "第 %s 行只剩字段名" % "、".join(map(str, empty[:6]))))
    else:
        out.append((PASS, "空栏目", "无空字段"))
    return out


def check_constraints(text):
    out = []
    lines = text.split("\n")
    idx = [i for i, l in enumerate(lines)
           if re.search(r"不要|禁止|避免|不得|不出现|无字幕|无 BGM|无BGM", l)]
    if not idx:
        out.append((WARN, "负向约束", "没有找到负向约束句；确无需要可忽略"))
    else:
        ratio = (max(idx) + 1) / max(len(lines), 1)
        if ratio < 0.6:
            out.append((WARN, "负向约束", "约束句最早出现在 %.0f%% 处、最晚 %.0f%%，建议集中到结尾" % ((idx[0] + 1) * 100 / len(lines), ratio * 100)))
        else:
            out.append((PASS, "负向约束", "%d 处，集中在结尾" % len(idx)))
    return out


STATIC_WORDS = r"停住|停下|站定|愣住|凝住|对峙|保持.{0,6}(?:姿势|不动)|纹丝不动|站着不动|双方不动"
ACTION_VERBS = re.compile(r"打中|打空|出拳|踢|踹|摔|撞|抓|拽|推|拉|扑|翻滚|滚落|甩|抡|"
                          r"锁喉|膝顶|肘击|转身|侧身|后撤|倒地|滑出|滑坐|飞起|跃起|冲刺")


def check_action(text):
    out = []
    hits = [(text[:m.start()].count("\n") + 1, m.group(0)) for m in re.finditer(STATIC_WORDS, text)]
    if hits:
        out.append((WARN, "静态词", "%d 处：%s（节奏的顿宜改写成\"换一种运动\"）"
                    % (len(hits), "、".join("第%d行「%s」" % h for h in hits[:5]))))
    else:
        out.append((PASS, "静态词", "未出现停/愣/站定/对峙类写法"))

    n = len(ACTION_VERBS.findall(text))
    if n:
        out.append((PASS, "动作密度", "动作动词粗估 %d 个；这是下限参考，单元总数仍需按稿人工数" % n))
    else:
        out.append((WARN, "动作密度", "没数到动作动词，确认是否写成了动作提纲"))
    return out


def lint(text, duration=None, images=None, action=False):
    declared, raw = declared_duration(text)
    if duration is None:
        duration = declared
    results = []
    results += check_residue(text)
    results += check_timeline(text, duration)
    results += check_labels(text, images)
    results += check_headings(text)
    results += check_constraints(text)
    if action:
        results += check_action(text)
    return results, declared, raw


def report(name, results, declared, raw, duration, images, action):
    print("=" * 66)
    print("文件：%s" % name)
    print("声明时长：%s   参考图：%s   模式：%s"
          % ("%g 秒（%s）" % (duration, raw) if duration else "未识别",
             "未给" if images is None else "%d 张" % images,
             "动作片" if action else "普通"))
    print("=" * 66)
    for level, cat, msg in results:
        print("[%-4s] %s：%s" % (level, cat, msg))
    fails = sum(1 for r in results if r[0] == FAIL)
    warns = sum(1 for r in results if r[0] == WARN)
    print("-" * 66)
    if fails:
        print("FAIL %d / WARN %d —— 先改 FAIL，再决定 WARN 里哪些是真问题。" % (fails, warns))
    else:
        print("FAIL 0 / WARN %d —— 形式检查通过；画面是否成立仍要看稿和看片。" % warns)
    print("边界：本脚本只查形式，不判断好不好看、打得对不对、身份会不会漂。")
    return 1 if fails else 0


BAD = """生成一条[总时长]秒、[画幅]的动作视频，时长 12 秒。
@图片1 是男主，@图片2 是女主，@图3 是场景，两张图分别是男主和女主。
【动作链】他抱住鱼站在原地对峙，画面极短地凝住。
[00:00-00:03] 交手。
[00:05-00:08] 他愣了。
不要字幕。
"""

GOOD = """▍格式
12 秒，16:9，三个相连镜头。
▍主体
@图片1 定义男主外观；@图片2 定义女主外观。成片中始终只有这两个人。
▍时间
[00:00-00:04] 他侧身让过，脚在地砖上滑出半步。
[00:04-00:08] 对手一拳砸在卷闸上，卷闸凹进去一块。
[00:08-00:12] 他抓住对手衣领往侧面拽，两人一起撞进积水里。
▍约束
保持两人面部结构与服装一致。不要字幕，不要 BGM。
"""


def selftest():
    ok = True
    bad, _, _ = lint(BAD, images=2, action=True)
    good, _, _ = lint(GOOD, images=2, action=True)
    bad_f = [r for r in bad if r[0] == FAIL]
    good_f = [r for r in good if r[0] == FAIL]
    cats = {r[1] for r in bad_f}
    for need in ("残留", "时间戳", "素材指派"):
        if need not in cats:
            print("[失败] 反例没报出 %s" % need); ok = False
    if good_f:
        print("[失败] 正例报出 FAIL：%s" % good_f); ok = False
    if ok:
        print("[通过] 反例命中 %d 个 FAIL（%s）；正例 0 FAIL" % (len(bad_f), "、".join(sorted(cats))))
        print("[提示] 正例剩余 WARN：%s" % ([r[2] for r in good if r[0] == WARN] or "无"))
    return 0 if ok else 1


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    if "--selftest" in args:
        return selftest()

    path, duration, images, action = None, None, None, False
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--duration" and i + 1 < len(args):
            duration = float(args[i + 1]); i += 2; continue
        if a == "--images" and i + 1 < len(args):
            images = int(args[i + 1]); i += 2; continue
        if a == "--action":
            action = True; i += 1; continue
        if a.startswith("-"):
            print("未知参数：%s" % a); print(__doc__); return 2
        path = a; i += 1

    if not path or not os.path.isfile(path):
        print("找不到文件：%s" % path)
        return 2

    text = read(path)
    results, declared, raw = lint(text, duration, images, action)
    return report(os.path.basename(path), results, declared, raw, duration or declared, images, action)


if __name__ == "__main__":
    sys.exit(main())

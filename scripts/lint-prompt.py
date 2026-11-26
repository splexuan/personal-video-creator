#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lint-prompt.py —— 提示词交付前的机械检查

只查"不需要判断力、但最容易漏掉"的项目，判断力留给提示词自检与看片。

检查项：
  1 模板残留：使用说明、提示语、方括号占位符
  2 时间戳：是否连续（1 秒内缝隙给警告、更大断档判失败）、结尾是否等于声明时长
  3 素材标签：编号是否从 1 连续、数量是否与实际上传数一致、有没有无依据的 @1 写法
  4 多素材指派：有没有用"分别是"句式（官方点名的失败写法）
  5 字段标题：字段名是否还在用 【】（与画面字幕同符号；会先区分字段与字幕）
  6 画面字幕：【】 字幕是否过长（句中字数越多越容易多字、错字）
  7 空栏目：只剩字段名、没有内容的行
  8 台词：{} 内超过 30 字的句子（字幕与配音都容易出错）
  9 负向约束：是否集中在结尾，而不是散在前半段
 10 约束冲突：写了"不要字幕／不要台词／不要音乐"，正文里却还有对应内容
 11 平台上限：时长是否落在 4–30 秒、参考图是否超过 30 张（推荐 1–8）、视频/音频是否超过 10 段
 12 动作片（--action）：禁用静态词、动作动词粗估

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
    for m in re.finditer(r"(\d{1,3}(?:\.\d+)?)\s*(?:s|秒)?\s*[-–—~至]\s*(\d{1,3}(?:\.\d+)?)\s*(?:s|秒)"
                        r"(?!\s*(?:后|之后|以后|左右|以内|内))", text):
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


DUR_LABEL = r"(?:总时长|成片时长|全片时长|片长|时长|视频长度)"
DUR_EXCLUDE = re.compile(r"(?:参考|原片|样片|素材|对比)\S{0,4}$")


def declared_duration(text):
    """只认明确声明，不猜。宁可返回 None（只给 WARN），也不抓错数字触发 FAIL。"""
    for m in re.finditer(DUR_LABEL + r"\s*[：:为]?\s*(\d+(?:\.\d+)?)\s*秒", text):
        head = text[max(0, m.start() - 8):m.start()]
        if DUR_EXCLUDE.search(head):
            continue
        return float(m.group(1)), m.group(0)
    for pat in (r"(?:生成|做|制作|拍)一(?:条|支|个)\s*(\d+(?:\.\d+)?)\s*秒",
                r"(?:本次|成片|目标|完成片)\s*(?:时长)?\s*[：:为]?\s*(\d+(?:\.\d+)?)\s*秒"):
        m = re.search(pat, text)
        if m:
            return float(m.group(1)), m.group(0)
    # 兜底：取第一个未被"参考/原片/样片"修饰的 N 秒。开头通常就是规格行；
    # 时间轴里的"8—15 秒"排在后面，不会被误当成总时长。
    cands = [m for m in re.finditer(r"(\d+(?:\.\d+)?)\s*秒", text)
             if not DUR_EXCLUDE.search(text[max(0, m.start() - 8):m.start()])]
    if cands:
        m = cands[0]
        return float(m.group(1)), m.group(0)
    # 英文稿："Create a 30-second, 16:9 ..." 这种开头写法。只认靠前的数字，
    # 避免把正文里的 "hold for 2 seconds" 当成总时长。
    m = re.search(r"(\d+(?:\.\d+)?)\s*[- ]?\s*(?:second|sec)s?\b", text[:120], re.I)
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
            # 不含中文的方括号视为英文机位/风格注释，例如 [Slow Orbital + Detail]
            if not re.search(r"[\u4e00-\u9fff]", inner):
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

    if len(ranges) == 1 and ranges[0][0] > 0.01:
        out.append((WARN, "时间戳", "只识别到一段 %s 且不从 0 开始，可能是时长描述，已忽略" % ranges[0][2]))
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

    big, small = [], []
    for prev, cur in zip(ranges, ranges[1:]):
        gap = cur[0] - prev[1]
        if gap > 1.0:
            big.append((prev, cur, gap))
        elif gap > 0.01:
            small.append((prev, cur))
        elif cur[0] < prev[1] - 0.01:
            out.append((WARN, "时间戳", "重叠：%s 与 %s" % (prev[2], cur[2])))
    for prev, cur, gap in big:
        out.append((FAIL, "时间戳", "断档 %.1fs：%s 之后接 %s" % (gap, prev[2], cur[2])))
    if small:
        sample = "、".join("%s→%s" % (p1[2], c1[2]) for p1, c1 in small[:2])
        out.append((WARN, "时间戳", "%d 处 1 秒内的缝隙（%s），按平台要求应首尾相接" % (len(small), sample)))

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


def check_dialogue(text):
    out = []
    long_lines = []
    for m in re.finditer(r"\{([^{}]{1,300})\}", text):
        s = m.group(1).strip()
        if len(s) > 30:
            long_lines.append((text[:m.start()].count("\n") + 1, len(s)))
    if long_lines:
        out.append((WARN, "台词", "%d 句超过 30 字（如第 %d 行 %d 字）；字幕与配音都容易出错，建议拆短"
                    % (len(long_lines), long_lines[0][0], long_lines[0][1])))
    else:
        out.append((PASS, "台词", "无超长台词" if "{" in text else "无台词块"))
    return out


# 字段名常见词，用来把【人物锁定】这类标题与【第一章：回家】这类画面字幕区分开
FIELD_WORDS = re.compile(
    r"^(?:人物|角色|主体|主角|配角|场景|环境|空间|地点|画面|构图|镜头|分镜|景别|机位|视角|"
    r"光线|光影|摄影|运镜|风格|画风|色调|制作|素材|参考|道具|服装|造型|妆发|妆容|表演|情绪|"
    r"表情|台词|对白|字幕|文字|声音|音效|音乐|配乐|节奏|剪辑|转场|开场|结尾|目标|卖点|品牌|"
    r"布局|交互|界面|步骤|阶段|材料|结果|时长|格式|规格|比例|画幅|约束|负向|说明|要求|故事|"
    r"叙事|动作|事件|规则|世界观|氛围|质感|特效|整体|视觉|生成|提示词|概述|概览|关键|细节|"
    r"补充|输出|内容|任务|需求|限制|参数|时间线|设定|首帧|尾帧|分镜脚本|镜头语言)")
# 章节号、带冒号的字标一律按画面字幕理解
SUB_MARK = re.compile(r"[：:]|^第[一二三四五六七八九十百零\d]+[章节幕集部篇段]")


def line_of(text, pos):
    return text[:pos].count("\n") + 1


def split_brackets(text):
    """把 【…】 区分为字段标题与画面字幕，返回 (headings, subtitles)，元素为 (行号, 内容)。

    判定顺序：带冒号或章节号的算字幕 → 命中字段词表的算标题 →
    整篇有 3 处以上独立 【】 的按外部模板的字段标题处理（单条字幕很少成组出现）→ 其余算字幕。
    """
    items = []
    for m in re.finditer(r"【([^】\n]{1,40})】", text):
        inner = m.group(1).strip()
        start = text.rfind("\n", 0, m.start()) + 1
        end = text.find("\n", m.end())
        if end == -1:
            end = len(text)
        line = text[start:end]
        standalone = re.fullmatch(r"\s*【[^】\n]{1,40}】\s*", line) is not None
        items.append((line_of(text, m.start()), inner, standalone))

    n_standalone = sum(1 for it in items if it[2])
    headings, subtitles = [], []
    for ln, inner, standalone in items:
        if SUB_MARK.search(inner) or not standalone:
            subtitles.append((ln, inner))
        elif FIELD_WORDS.match(inner) or n_standalone >= 3:
            headings.append((ln, inner))
        else:
            subtitles.append((ln, inner))
    return headings, subtitles


def check_headings(text):
    out = []
    headings, subtitles = split_brackets(text)
    if headings:
        out.append((WARN, "字段标题", "%d 处字段标题仍在用 【】：%s；它与画面字幕同符号，建议改 ▍字段"
                    % (len(headings), "、".join("第%d行「%s」" % h for h in headings[:3]))))
    else:
        out.append((PASS, "字段标题", "字段没用 【】 做标题" if "【" not in text else "【】 只出现在画面字幕里"))
    if subtitles:
        longest = max(subtitles, key=lambda x: len(x[1]))
        if len(longest[1]) > 20:
            out.append((WARN, "画面字幕", "%d 处画面字幕，最长 %d 字（第 %d 行「%s」）；句中越长越容易多字或错字，建议拆短或改成画面可读"
                        % (len(subtitles), len(longest[1]), longest[0], longest[1][:18])))
        else:
            out.append((PASS, "画面字幕", "%d 处画面字幕，最长 %d 字" % (len(subtitles), len(longest[1]))))
    else:
        out.append((PASS, "画面字幕", "无画面字幕"))
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
    # 中文交付稿为主，同时兼容英文稿的 no/avoid/without 写法
    pat = re.compile(r"不要|禁止|避免|不得|不出现|无字幕|无 ?BGM|"
                     r"\b(?:no|without|avoid|never|do not|don't)\b", re.I)
    idx = [i for i, l in enumerate(lines) if pat.search(l)]
    if not idx:
        out.append((WARN, "负向约束", "没有找到负向约束句；确无需要可忽略"))
    else:
        ratio = (max(idx) + 1) / max(len(lines), 1)
        if ratio < 0.6:
            out.append((WARN, "负向约束", "约束句最早出现在 %.0f%% 处、最晚 %.0f%%，建议集中到结尾" % ((idx[0] + 1) * 100 / len(lines), ratio * 100)))
        else:
            out.append((PASS, "负向约束", "%d 处，集中在结尾" % len(idx)))
    return out


NEG_RULES = (
    ("字幕", r"(?:不要|禁止|不出现|不加|避免|没有|无)\s*(?:任何)?\s*字幕",
     r"\b(?:no|without)\s+(?:subtitles?|captions?)\b"),
    ("台词", r"(?:不要|禁止|不出现|避免|没有|无)\s*(?:任何)?\s*(?:台词|对白|口白)",
     r"\b(?:no|without)\s+(?:dialogue|lines|speech)\b"),
    ("音乐", r"(?:不要|禁止|不出现|避免|没有|无)\s*(?:任何)?\s*(?:音乐|配乐|BGM|背景音乐)",
     r"\b(?:no|without)\s+(?:music|bgm|score|soundtrack)\b"),
)

MUSIC_CONTENT = re.compile(
    r"[（(][^）)\n]{0,24}(?:音乐|配乐|BGM|bgm|钢琴|旋律|鼓点|节拍)[^）)\n]{0,24}[）)]"
    r"|(?:背景音乐|配乐|BGM|bgm)\s*(?:响起|渐入|淡出|铺底|贯穿)")
DIALOGUE = re.compile(r"\{([^{}]{1,300})\}")


def check_conflict(text):
    """负向约束与正文内容对撞：写了"不要字幕"却仍有字幕，是交付事故，判 FAIL。"""
    out = []
    headings, subtitles = split_brackets(text)
    dialogues = [m.group(1).strip() for m in DIALOGUE.finditer(text) if m.group(1).strip()]
    music = MUSIC_CONTENT.findall(text)
    evidence = {
        "字幕": (subtitles, "画面字幕"),
        "台词": (dialogues, "台词块 {}"),
        "音乐": (music, "音乐描述"),
    }
    hits = []
    for name, cn, en in NEG_RULES:
        m = re.search(cn, text) or re.search(en, text, re.I)
        if not m:
            continue
        items, label = evidence[name]
        if not items:
            continue
        first = items[0]
        loc = ("第 %d 行「%s」" % (first[0], first[1][:16])) if isinstance(first, tuple) else "「%s」" % str(first)[:16]
        hits.append((FAIL, "约束冲突", "写了「%s」，正文却仍有 %d 处%s（%s）；两者只能留一个"
                     % (m.group(0).strip(), len(items), label, loc)))
    if hits:
        out.extend(hits)
    else:
        out.append((PASS, "约束冲突", "负向约束与正文内容不冲突"))
    return out


def check_limits(text, duration, images):
    """平台硬上限：种子口径为单次 4–30 秒、图 30 张（推荐 1–8）、视频/音频各 10 段。"""
    out = []
    if duration is not None:
        if duration < 4:
            out.append((WARN, "平台上限", "声明 %.1f 秒低于单次最短 4 秒（Seedance 口径）；他入口按实际界面核对" % duration))
        elif duration > 30:
            out.append((WARN, "平台上限", "声明 %.1f 秒超出单次 4–30 秒；若用长视频模式（30–180 秒）或他入口可忽略" % duration))
        else:
            out.append((PASS, "平台上限", "时长 %.1f 秒在 4–30 秒区间内（Seedance 口径）" % duration))
    if images is not None:
        if images > 30:
            out.append((FAIL, "平台上限", "参考图 %d 张超过上限 30 张" % images))
        elif images > 8:
            out.append((WARN, "平台上限", "参考图 %d 张超出推荐 1–8 张的稳定区间" % images))
        else:
            out.append((PASS, "平台上限", "参考图 %d 张在推荐区间内" % images))

    pat = re.compile(r"@\s*(视频|Video|音频|Audio)\s*(\d+)", re.I)
    buckets = {}
    for m in pat.finditer(text):
        buckets.setdefault(m.group(1).lower(), set()).add(int(m.group(2)))
    vids = buckets.get("视频", set()) | buckets.get("video", set())
    auds = buckets.get("音频", set()) | buckets.get("audio", set())
    for label, s in (("视频", vids), ("音频", auds)):
        if len(s) > 10:
            out.append((FAIL, "平台上限", "%s素材 %d 段超过上限 10 段" % (label, len(s))))

    m = re.search(r"(\d{1,3})\s*(?:格|宫格|格栅)", text)
    if m and int(m.group(1)) > 15:
        out.append((WARN, "平台上限", "分镜栅格 %s 格，建议 <15 格（用线稿或火柴人）" % m.group(1)))
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

    if re.search(r"(?:动作单元|单元总数|单元数|写作密度)[^\n。]{0,16}\d", text) or \
       re.search(r"\d{2,3}\s*个单元", text):
        out.append((PASS, "密度声明", "已写出单元总数或写作密度"))
    else:
        out.append((WARN, "密度声明", "没写动作单元总数或写作密度；动作类应先把总数定下来再写画面（见 pacing.md 第二节）"))
    return out


MOVES = re.compile(r"推进|推近|推轨|拉远|后拉|摇镜|横移|平移|环绕|跟拍|跟摇|升降|变焦|航拍|俯冲|甩镜")
CONNECT = re.compile(r"同时|一边|一面|以及|并[同且行]|再加")


def check_camera(text):
    """一句里写两个主运镜，是画面崩掉的常见原因。"""
    hits = []
    for i, sent in enumerate(re.split(r"[。！？\n]", text), 1):
        moves = set(MOVES.findall(sent))
        if len(moves) >= 2 and CONNECT.search(sent):
            hits.append((i, "、".join(sorted(moves)), sent.strip()[:26]))
    if hits:
        i, mv, snip = hits[0]
        out = [(WARN, "运镜", "%d 处一句里出现两个主运镜（如「%s…」含 %s）；拆成相邻两拍" % (len(hits), snip, mv))]
    else:
        out = [(PASS, "运镜", "未发现一句多运镜")]
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
    results += check_dialogue(text)
    results += check_constraints(text)
    results += check_conflict(text)
    results += check_limits(text, duration, images)
    results += check_camera(text)
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
▍动作密度
动作单元 28 个，写作密度 2.3 单元/秒。
▍约束
保持两人面部结构与服装一致。不要字幕，不要 BGM。
"""

CONFLICT = """总时长 12 秒，9:16 竖屏。
▍时间
[00:00-00:04] 她拎着袋子进门。
[00:04-00:08] 她蹲下捡菜。
[00:08-00:12] 她走向客厅。
▍字幕
【第一章：回家】
▍台词
{我回来了。}
▍约束
不要字幕，不要台词，不要 BGM。
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
    # 约束冲突：写"不要字幕/不要台词"却留着字幕与台词
    conf, _, _ = lint(CONFLICT)
    conf_f = [r for r in conf if r[0] == FAIL]
    if {r[1] for r in conf_f} != {"约束冲突"} or len(conf_f) != 2:
        print("[失败] 约束冲突应报 2 条 FAIL，实际：%s" % conf_f); ok = False
    # 合法画面字幕不能被当成字段标题
    warn_cats = {r[1] for r in lint("【第一章：回家】\n{你好。}\n")[0] if r[0] == WARN}
    if "字段标题" in warn_cats:
        print("[失败] 合法画面字幕仍被当成字段标题"); ok = False
    if ok:
        print("[通过] 反例命中 %d 个 FAIL（%s）；正例 0 FAIL" % (len(bad_f), "、".join(sorted(cats))))
        print("[通过] 约束冲突报 2 条；字段标题与画面字幕已区分")
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

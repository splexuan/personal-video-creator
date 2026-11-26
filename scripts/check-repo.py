#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check-repo.py —— 仓库结构自检（不需要 ffmpeg）

把这些反复手工检查的东西固化成一条命令：
  1 相对链接是否存在
  2 锚点是否存在（按 GitHub 的 heading→slug 规则）
  3 SKILL.md frontmatter：name / description 是否齐全，name 是否与目录名一致
  4 正文里用反引号写的文件路径是否存在
  5 是否有文件没被任何 md/py 提到（可能是死文件）
  6 跨文档数量声明是否和实际文件对得上（模板数、结构分册模板数、评测条数）

用法：
    python scripts/check-repo.py            # 全量检查
    python scripts/check-repo.py --quiet    # 只打印问题

退出码：0 全部通过；1 有 FAIL。
"""

import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASS, WARN, FAIL = "PASS", "WARN", "FAIL"
RESULTS = []


def add(level, group, msg):
    RESULTS.append((level, group, msg))


def rel(p):
    return os.path.relpath(p, ROOT).replace("\\", "/")


def slug(heading):
    """近似 GitHub：小写、去标点、空格转连字符，保留中文与数字。"""
    s = heading.strip().lower()
    s = re.sub(r"[`*_]", "", s)
    s = re.sub(r"[^\w\u4e00-\u9fff\- ]", "", s)
    return s.replace(" ", "-")


def md_files():
    return [p for p in glob.glob(os.path.join(ROOT, "**", "*.md"), recursive=True)
            if "/.git/" not in p.replace("\\", "/") and "/.workbuddy/" not in p.replace("\\", "/")]


# ---------- 1 & 2 链接与锚点 ----------
def check_links(files):
    anchors = {}
    for f in files:
        s = set()
        for line in open(f, encoding="utf-8"):
            m = re.match(r"^(#{1,6})\s+(.*)$", line)
            if m:
                s.add(slug(m.group(2)))
        anchors[os.path.normpath(f)] = s

    broken, bad_anchor, total = [], [], 0
    for f in files:
        for m in re.finditer(r"\[([^\]]*)\]\(([^)]+)\)", open(f, encoding="utf-8").read()):
            target = m.group(2).strip()
            if target.startswith(("http", "mailto:")):
                continue
            path, _, anc = target.partition("#")
            if not path:
                continue
            total += 1
            full = os.path.normpath(os.path.join(os.path.dirname(f), path))
            if not os.path.exists(full):
                broken.append((rel(f), target))
            elif anc and full.endswith(".md") and anc not in anchors.get(os.path.normpath(full), set()):
                bad_anchor.append((rel(f), target))

    for f, t in broken:
        add(FAIL, "链接", "%s → %s" % (f, t))
    for f, t in bad_anchor:
        add(FAIL, "锚点", "%s → %s" % (f, t))
    if not broken and not bad_anchor:
        add(PASS, "链接", "%d 条相对链接与锚点全部有效" % total)
    return total


# ---------- 3 frontmatter ----------
def check_frontmatter():
    path = os.path.join(ROOT, "SKILL.md")
    if not os.path.exists(path):
        add(FAIL, "frontmatter", "根目录没有 SKILL.md")
        return
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        add(FAIL, "frontmatter", "SKILL.md 缺少 YAML 前置块")
        return
    block = m.group(1)
    name = re.search(r"^name:\s*(.+)$", block, re.M)
    desc = re.search(r"^description:\s*(.+)$", block, re.M)
    if not name or not name.group(1).strip():
        add(FAIL, "frontmatter", "缺 name")
    elif name.group(1).strip().strip('"') != os.path.basename(ROOT):
        add(WARN, "frontmatter", "name=%s 与目录名 %s 不一致" % (name.group(1).strip(), os.path.basename(ROOT)))
    else:
        add(PASS, "frontmatter", "name 与目录名一致")
    if not desc:
        add(FAIL, "frontmatter", "缺 description")
    else:
        d = desc.group(1).strip().strip('"')
        if len(d) < 40:
            add(WARN, "frontmatter", "description 只有 %d 字，可能触发不到" % len(d))
        elif len(d) > 1024:
            add(FAIL, "frontmatter", "description 超过 1024 字，宿主可能截断")
        else:
            add(PASS, "frontmatter", "description %d 字" % len(d))


# ---------- 4 反引号路径 ----------
def check_inline_paths(files):
    bad, n = [], 0
    for f in files:
        for m in re.finditer(r"`((?:scripts|references|assets|evals)/[^`\n]+?)`", open(f, encoding="utf-8").read()):
            p = m.group(1).strip().rstrip("。，、").split()[0]   # 去掉 `<脚本> <参数>` 里的参数
            if "*" in p or p.endswith("/") or "<" in p:
                continue
            n += 1
            if not os.path.exists(os.path.join(ROOT, p)):
                bad.append((rel(f), p))
    for f, p in bad:
        add(FAIL, "路径", "%s 提到的 `%s` 不存在" % (f, p))
    if not bad:
        add(PASS, "路径", "%d 处反引号路径都存在" % n)


# ---------- 5 死文件 ----------
def check_orphans(files):
    corpus = ""
    for f in files:
        corpus += open(f, encoding="utf-8").read()
    for f in glob.glob(os.path.join(ROOT, "scripts", "*.py")):
        corpus += open(f, encoding="utf-8", errors="replace").read()
    skip_dirs = ("archive", "evals")
    orphans = []
    for sub in ("references", "assets", "scripts"):
        for f in glob.glob(os.path.join(ROOT, sub, "**", "*"), recursive=True):
            if os.path.isdir(f) or f.endswith((".pyc",)):
                continue
            r = rel(f)
            if r.split("/")[0] in skip_dirs:
                continue
            base = os.path.basename(f)
            if base not in corpus and r not in corpus:
                orphans.append(r)
    for o in orphans:
        add(WARN, "死文件", "%s 没有被任何文档或脚本提到" % o)
    if not orphans:
        add(PASS, "死文件", "references/assets/scripts 下的文件都有引用")


# ---------- 6 数量声明 ----------
def check_counts():
    readme = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()
    tpl = glob.glob(os.path.join(ROOT, "assets", "templates", "*.txt"))
    content = len([p for p in tpl if os.path.basename(p) != "dance-reference-image.txt"])
    m = re.search(r"(\d+) 份内容模板", readme)
    if m and int(m.group(1)) != content:
        add(FAIL, "数量", "README 说 %s 份内容模板，实际 %d" % (m.group(1), content))
    else:
        add(PASS, "数量", "模板 %d 份（另有 1 份参考图提示词）" % content)

    rules = open(os.path.join(ROOT, "references", "external-library", "structural-rules.md"), encoding="utf-8").read()
    claimed = sum(int(x) for x in re.findall(r"\| \[[^\]]+\]\(structures/[^)]+\) \| [^|]+ \| (\d+) \|", rules))
    actual = sum(len(re.findall(r"^### ", open(p, encoding="utf-8").read(), re.M))
                 for p in glob.glob(os.path.join(ROOT, "references", "external-library", "structures", "*.md")))
    if claimed != actual:
        add(FAIL, "数量", "结构规则声明 %d 个模板，分册里实际 %d 个" % (claimed, actual))
    else:
        add(PASS, "数量", "外部结构模板 %d 个，与分册一致" % actual)

    ev = os.path.join(ROOT, "evals", "evals.json")
    if os.path.exists(ev):
        n = len(re.findall(r'"id":', open(ev, encoding="utf-8").read()))
        m2 = re.search(r"(\d+) 条行为评测", readme)
        if m2 and int(m2.group(1)) != n:
            add(FAIL, "数量", "README 说 %s 条评测，实际 %d" % (m2.group(1), n))
        else:
            add(PASS, "数量", "评测 %d 条" % n)


def main():
    quiet = "--quiet" in sys.argv
    files = md_files()
    check_frontmatter()
    check_links(files)
    check_inline_paths(files)
    check_orphans(files)
    check_counts()

    fails = [r for r in RESULTS if r[0] == FAIL]
    warns = [r for r in RESULTS if r[0] == WARN]
    if not quiet:
        for level, group, msg in RESULTS:
            if quiet and level == PASS:
                continue
            print("[%-4s] %-10s %s" % (level, group, msg))
    else:
        for level, group, msg in RESULTS:
            if level != PASS:
                print("[%-4s] %-10s %s" % (level, group, msg))
    print("-" * 60)
    print("FAIL %d / WARN %d —— %s" % (len(fails), len(warns),
          "有必须修的问题" if fails else "结构检查通过"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

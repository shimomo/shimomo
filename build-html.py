#!/usr/bin/env python3
# resume.md から shimomo.net 公開用の HTML を生成するスクリプト
#
#   使い方:  python3 build-html.py（通常は ./build.sh html 経由）
#   任意指定: --in <入力.md>  --out <出力.html>
#
# Markdown を正本とし（build-pdf.ps1 と同じ記法を解釈する）、
# Web 公開向けに以下を調整する。
#   ・基本情報のうち OMIT_ROWS に挙げた行（生年月日など）は出力しない
#   ・redact.json に挙げた表現（本名・前職の社名など）は伏せた表現に置き換える
#   ・各案件の「習得スキル」「コメント」は折りたたみ（details）にする
#   ・末尾に連絡先（SITE で設定）を付ける
#   ・portfolio.md があれば「作ったもの」カードを自己PR の後に差し込む
#   ・職務経歴の冒頭に、各案件の期間から作った年表を置く
#   ・ライト / ダーク両対応、スマートフォン幅対応、印刷時は折りたたみを展開

import argparse, html, re, sys, os
from datetime import date
from urllib.parse import quote

SITE = {
    "role": "バックエンド寄りのフルスタックエンジニア",
    "location": "福岡",
    "github": "https://github.com/shimomo",
    "bluesky": "https://bsky.app/profile/shimomo.net",
    "bluesky_label": "@shimomo.net",
    "email": "work@shimomo.net",   # ページ上では JS で組み立てて表示する（収集ボット対策）
    "title_suffix": "経歴と作ったもの",   # <title> と OGP に使う「名前 | ○○」の ○○
    "description": "Yuichi Shimo（shimomo）の職務経歴。PHP / Laravel を中心とした Web アプリケーションのバックエンド開発、公開 API や OSS パッケージの開発・運用。",
}
OMIT_ROWS = {"生年月日", "ポートフォリオ", "氏名", "都道府県", "GitHub"}   # Web には載せない基本情報の行（ヘッダーと重複するもの）
OMIT_VALUES = {"－", "-", "―", "なし"}                        # 値がこれだけの行も載せない
# Web 版で伏せる表現（md は実名のまま。順序どおりに置換するので、長い表現を先に書く）
REDACT_FILE = "redact.json"   # Web 版だけで伏せる表現（本名・社名など）。[[置換前, 置換後], ...] を "replace" に持つ JSON
REPLACE = []                  # main() で REDACT_FILE から読み込む
COLLAPSE_SUBS = ("習得スキル", "コメント")      # 折りたたむ ≪見出し≫
# 年表の行ラベル（案件の No. → 短い名前。無ければ見出しをそのまま使う）
SHORT_TITLES = {
    "No.1": "新型ドライブレコーダー対応",
    "No.2": "次世代安否確認システム",
    "No.3": "安否確認 新規申し込み機能",
    "No.4": "安否確認 REST API",
    "No.5": "業務改善スクリプト",
    "No.6": "勤怠管理システム",
    "No.7": "物件検索システム",
    "No.8": "アルバイト（在学中）",
}

# ---- Markdown 解析 ---------------------------------------------------------

def join_smart(a, b):
    if not a: return b
    if not b: return a
    la, fb = a[-1], b[0]
    if ord(la) > 127 and re.match(r"[A-Za-z0-9]", fb): return a + " " + b
    if re.match(r"[A-Za-z0-9).]", la) and ord(fb) > 127: return a + " " + b
    return a + b

def inline(s):
    for a, b in REPLACE: s = s.replace(a, b)
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1" loading="lazy">', s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\"'>])(https?://[^\s<）)]+)", r'<a href="\1">\1</a>', s)
    return s

def parse(lines):
    doc = {"title": "", "sections": []}
    section = case = None
    para, cur_list, last_item = [], None, None

    def target():
        nonlocal section
        if case: return case["blocks"]
        if section is None:   # h1 直後・セクション外（作成日など）
            section = {"title": "", "blocks": [], "cases": []}; doc["sections"].append(section)
        return section["blocks"]
    def flush_para():
        nonlocal para
        if para:
            acc = ""
            for seg in para: acc = join_smart(acc, seg)
            target().append(("p", acc)); para = []
    def close_list():
        nonlocal cur_list, last_item
        cur_list = last_item = None

    i, n = 0, len(lines)
    while i < n:
        raw = lines[i]; line = raw.rstrip()
        if not line.strip():
            flush_para(); close_list(); i += 1; continue
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            flush_para(); close_list()
            lv, txt = len(m.group(1)), m.group(2).strip()
            if lv == 1: doc["title"] = txt
            elif lv == 2:
                section = {"title": txt.lstrip("■").strip(), "blocks": [], "cases": []}
                doc["sections"].append(section); case = None
            elif lv == 3:
                case = {"title": txt, "meta": {}, "blocks": []}
                section["cases"].append(case)
            i += 1; continue
        if line.lstrip().startswith("|"):
            flush_para(); close_list()
            rows = []
            while i < n and lines[i].rstrip().lstrip().startswith("|"):
                rt = lines[i].strip()
                if not re.match(r"^\|[\s:\-\|]+\|$", rt):
                    rows.append([c.strip() for c in rt.strip("|").split("|")])
                i += 1
            if case and not case["meta"] and not case["blocks"]:
                case["meta"] = {r[0]: r[1] for r in rows[1:]}
            else:
                target().append(("table", rows))
            continue
        m = re.match(r"^≪(.+)≫\s*$", line)
        if m:
            flush_para(); close_list()
            target().append(("sub", m.group(1).strip())); i += 1; continue
        m = re.match(r"^\s{2,3}-\s+(.*)$", line)
        if m and cur_list:
            flush_para()
            sub = cur_list[-1][1]; sub.append(m.group(1)); last_item = (sub, len(sub) - 1)
            i += 1; continue
        m = re.match(r"^-\s+(.*)$", line)
        if m:
            flush_para()
            if cur_list is None:
                cur_list = []; target().append(("list", cur_list))
            cur_list.append([m.group(1), []]); last_item = (cur_list, len(cur_list) - 1)
            i += 1; continue
        if cur_list and re.match(r"^\s{2,}\S", raw):
            lst, idx = last_item
            if lst is cur_list: lst[idx][0] = join_smart(lst[idx][0], line.strip())
            else: lst[idx] = join_smart(lst[idx], line.strip())
            i += 1; continue
        close_list(); para.append(line.strip()); i += 1
    flush_para(); close_list()
    return doc

# ---- HTML 生成 -------------------------------------------------------------

def render_list(items):
    out = ["<ul>"]
    for text, subs in items:
        out.append(f"<li>{inline(text)}" + ("" if not subs else "<ul>" + "".join(f"<li>{inline(s)}</li>" for s in subs) + "</ul>") + "</li>")
    out.append("</ul>")
    return "\n".join(out)

def link_case_refs(h):
    """段落中の No.N を該当案件へのリンクにする"""
    return re.sub(r"(?<![\w#-])No\.(\d+)(?!\d)", r'<a href="#case-\1">No.\1</a>', h)

def render_blocks(blocks, link_refs=False):
    out = []
    for kind, val in blocks:
        if kind == "p": out.append(f"<p>{link_case_refs(inline(val)) if link_refs else inline(val)}</p>")
        elif kind == "sub": out.append(f"<h4>{inline(val)}</h4>")
        elif kind == "list": out.append(render_list(val))
        elif kind == "table":
            t = ["<table>", "<thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in val[0]) + "</tr></thead>", "<tbody>"]
            for r in val[1:]: t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t += ["</tbody>", "</table>"]; out.append("\n".join(t))
    return "\n".join(out)

def render_basic(section):
    rows = [r for _, rows in section["blocks"] if _ == "table" for r in rows[1:] if r[0] not in OMIT_ROWS and r[1].strip() not in OMIT_VALUES]
    return "<dl class=\"basic\">\n" + "\n".join(f"<div><dt>{inline(k)}</dt><dd>{inline(v)}</dd></div>" for k, v in rows) + "\n</dl>"

def render_skills(section):
    out = []
    for kind, rows in section["blocks"]:
        if kind == "p":
            out.append(f'<p class="note">{inline(rows)}</p>'); continue
        if kind != "table": continue
        header = rows[0][1:]; groups = []; cur = None
        for r in rows[1:]:
            if r[0]: cur = (r[0], []); groups.append(cur)
            cur[1].append(r[1:])
        out.append('<div class="skills">')
        for name, items in groups:
            out.append(f"<section class=\"skill-group\"><h3>{inline(name)}</h3><table><thead><tr>" + "".join(f"<th>{inline(h)}</th>" for h in header) + "</tr></thead><tbody>")
            for it in items: out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in it) + "</tr>")
            out.append("</tbody></table></section>")
        out.append("</div>")
    return "\n".join(out)

def render_works(works_doc):
    groups = [g for g in works_doc["sections"] if g["cases"]]
    if not groups: return "", ""
    out = []
    for g in groups:
        out.append(f'<h3 class="works-group">{inline(g["title"])}</h3>\n<div class="works">')
        for w in g["cases"]:
            m = w["meta"]; featured = bool(m.get("画像"))
            card = [f'<article class="work{" featured" if featured else ""}">']
            if featured: card.append(f'<div class="shot">{inline(m["画像"])}</div>')
            card.append('<div class="body">')
            card.append(f'<h4>{inline(w["title"])}</h4>')
            if m.get("説明"): card.append(f'<p>{inline(m["説明"])}</p>')
            if m.get("補足"): card.append(f'<p class="sub">{inline(m["補足"])}</p>')
            if m.get("バッジ"): card.append(f'<p class="badges">{inline(m["バッジ"])}</p>')
            if m.get("タグ"):
                tags = [t.strip() for t in re.split(r"[,、]", m["タグ"]) if t.strip()]
                card.append('<ul class="tags">' + "".join(f"<li>{inline(t)}</li>" for t in tags) + "</ul>")
            if m.get("リンク"): card.append(f'<p class="links">{inline(m["リンク"])}</p>')
            card.append("</div></article>"); out.append("\n".join(card))
        out.append("</div>")
    return works_doc["title"] or "作ったもの", "\n".join(out)

def parse_period(text):
    m = re.search(r"(\d{4})年(\d{1,2})月\s*-\s*(\d{4})年(\d{1,2})月", text or "")
    if not m: return None
    y1, m1, y2, m2 = map(int, m.groups())
    return (y1 * 12 + m1 - 1, y2 * 12 + m2)   # 月インデックス（終端は排他）

def render_timeline(cases):
    rows = []
    for i, c in enumerate(cases, 1):
        p = parse_period(c["meta"].get("期間"))
        if p: rows.append((i, c, p))
    if not rows: return ""
    start = (min(p[0] for _, _, p in rows) // 12) * 12
    end = ((max(p[1] for _, _, p in rows) + 11) // 12) * 12
    total = end - start; nyears = total // 12
    out = ['<div class="timeline">',
           '<div class="tl-axis">' + "".join(f'<span style="left:{(y * 12 - start) / total * 100:.2f}%">{y}</span>' for y in range(start // 12, end // 12)) + "</div>"]
    for i, c, (a, b) in sorted(rows, key=lambda r: (r[2][0], r[0])):
        m = re.match(r"^(No\.\d+)\s+(.*?)\s*/\s*(.*)$", c["title"])
        num, org, title = (m.group(1), m.group(2), m.group(3)) if m else ("", "", c["title"])
        short = SHORT_TITLES.get(num, title)
        contract = c["meta"].get("契約形態", "")
        kind = "parttime" if "アルバイト" in contract else ("outsourced" if "業務委託" in org or "業務委託" in contract else "employed")
        left = (a - start) / total * 100; width = max((b - a) / total * 100, 1.2)
        out.append(f'<div class="tl-row"><div class="tl-label"><span class="num">{inline(num)}</span>{inline(short)}</div>'
                   f'<div class="tl-track" style="background-size:{100 / nyears:.4f}% 100%">'
                   f'<a class="tl-bar {kind}" href="#case-{i}" style="left:{left:.2f}%;width:{width:.2f}%" title="{inline(num)} {inline(c["meta"]["期間"])}"></a></div></div>')
    out.append('<p class="tl-legend"><span class="sw employed"></span>前職（正社員）<span class="sw outsourced"></span>業務委託<span class="sw parttime"></span>アルバイト（在学中）</p></div>')
    return "\n".join(out)

def favicon():
    svg = "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🚤</text></svg>"
    return f'<link rel="icon" href="data:image/svg+xml,{quote(svg)}">'

def render_case(case, idx):
    m = re.match(r"^(No\.\d+)\s+(.*?)\s*/\s*(.*)$", case["title"])
    num, org, title = (m.group(1), m.group(2), m.group(3)) if m else ("", "", case["title"])
    out = [f'<article class="case" id="case-{idx}">',
           f'<h3><span class="num">{inline(num)}</span><span class="org">{inline(org)}</span><span class="ttl">{inline(title)}</span></h3>']
    if case["meta"]:
        out.append('<dl class="meta">' + "".join(f"<div><dt>{inline(k)}</dt><dd>{inline(v)}</dd></div>" for k, v in case["meta"].items()) + "</dl>")
    visible, hidden = [], []
    for b in case["blocks"]:
        if not hidden and b[0] == "sub" and b[1].startswith(COLLAPSE_SUBS): hidden.append(b)
        elif hidden: hidden.append(b)
        else: visible.append(b)
    out.append(render_blocks(visible))
    if hidden:
        out.append("<details><summary>習得スキル・コメント</summary>" + render_blocks(hidden) + "</details>")
    out.append("</article>")
    return "\n".join(out)

CSS = """
:root{--bg:#fff;--fg:#1a1a1a;--muted:#5d6570;--line:#d9dee3;--soft:#f5f7f9;--accent:#1f4e79;--link:#0b5cad;--code:#eef1f4}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#121417;--fg:#e6e8eb;--muted:#9aa3ad;--line:#2d333b;--soft:#1b1f24;--accent:#8ab4f8;--link:#8ab4f8;--code:#22272e}}
:root[data-theme="dark"]{--bg:#121417;--fg:#e6e8eb;--muted:#9aa3ad;--line:#2d333b;--soft:#1b1f24;--accent:#8ab4f8;--link:#8ab4f8;--code:#22272e}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font-family:"Noto Sans JP","Hiragino Kaku Gothic ProN","Hiragino Sans","Yu Gothic UI","Meiryo",system-ui,sans-serif;font-size:15px;line-height:1.75;overflow-wrap:anywhere}
a{color:var(--link)}
code{font-family:ui-monospace,Consolas,monospace;font-size:.9em;background:var(--code);padding:0 .3em;border-radius:3px}
.wrap{max-width:880px;margin:0 auto;padding:32px 16px 48px}
header.top{border-bottom:2px solid var(--fg);padding-bottom:16px;margin-bottom:8px}
header.top h1{font-size:1.9rem;margin:0 0 4px;letter-spacing:.04em}
header.top .role{color:var(--muted);margin:0 0 8px}
header.top .links{display:flex;flex-wrap:wrap;gap:8px 20px;padding:0;margin:0;list-style:none;font-size:.95rem}
nav.toc{display:flex;flex-wrap:wrap;gap:6px 16px;padding:12px 0;margin:0 0 8px;font-size:.92rem;border-bottom:1px solid var(--line)}
nav.toc a{text-decoration:none}
nav.toc a:hover{text-decoration:underline}
.updated{color:var(--muted);font-size:.85rem;margin:8px 0 0}
section.sec{margin:36px 0 0}
section.sec>h2{font-size:1.25rem;margin:0 0 16px;padding:6px 0 6px 12px;border-left:5px solid var(--accent);background:var(--soft)}
h3{font-size:1.05rem;margin:24px 0 8px}
h4{font-size:.95rem;margin:16px 0 4px;color:var(--accent)}
h4::before{content:"■";font-size:.6em;margin-right:6px;vertical-align:2px}
p{margin:0 0 12px}
ul{margin:0 0 12px;padding-left:1.4em}
li{margin:2px 0}
li>ul{margin:2px 0 4px}
li>ul>li{color:var(--muted);font-size:.95em}
table{width:100%;border-collapse:collapse;margin:0 0 16px;font-size:.93rem}
th,td{border:1px solid var(--line);padding:6px 10px;vertical-align:top;text-align:left}
th{background:var(--soft);white-space:nowrap}
dl{margin:0}
dl.basic{display:grid;grid-template-columns:1fr;gap:0;border:1px solid var(--line);border-radius:6px;overflow:hidden}
dl.basic div{display:grid;grid-template-columns:8.5em minmax(0,1fr);border-top:1px solid var(--line)}
dl.basic div:first-child{border-top:0}
dl.basic dt{background:var(--soft);padding:8px 12px;font-weight:600}
dl.basic dd{margin:0;padding:8px 12px}
.skills{display:grid;grid-template-columns:minmax(0,1fr);gap:0 24px}
.skill-group{min-width:0}
.skill-group h3{margin-top:8px}
.skills table{table-layout:fixed}
.skills th:first-child,.skills td:first-child{width:31%;overflow-wrap:break-word}
.skills th:nth-child(2),.skills td:nth-child(2){width:6em;white-space:nowrap}
.note{color:var(--muted);font-size:.9rem}
article.case{border:1px solid var(--line);border-radius:8px;padding:16px 18px;margin:0 0 20px;background:var(--bg)}
article.case h3{margin:0 0 10px;line-height:1.5;display:flex;flex-wrap:wrap;gap:4px 10px;align-items:baseline}
article.case h3 .num{display:inline-block;font-size:.8rem;font-weight:600;color:#fff;background:var(--accent);padding:0 8px;border-radius:999px}
article.case h3 .org{color:var(--muted);font-size:.9rem;font-weight:500}
article.case h3 .ttl{flex-basis:100%}
dl.meta{display:grid;grid-template-columns:1fr;gap:4px 16px;background:var(--soft);border:1px solid var(--line);border-radius:6px;padding:10px 12px;margin:0 0 14px;font-size:.9rem}
dl.meta div{display:grid;grid-template-columns:7.5em minmax(0,1fr)}
dl.meta dt{font-weight:600;color:var(--muted)}
dl.meta dd{margin:0}
details{margin:8px 0 0;border-top:1px dashed var(--line);padding-top:8px}
summary{cursor:pointer;color:var(--link);font-size:.95rem}
details[open] summary{margin-bottom:8px}
.works-group{font-size:.95rem;color:var(--muted);margin:20px 0 10px;letter-spacing:.04em}
.works-group:first-child{margin-top:0}
.works{display:grid;grid-template-columns:minmax(0,1fr);gap:14px}
article.work{border:1px solid var(--line);border-radius:8px;padding:14px 16px;display:flex;flex-direction:column;gap:6px;min-width:0}
article.work .body{display:flex;flex-direction:column;gap:6px;min-width:0;flex:1}
article.work h4{margin:0;font-size:1.02rem;color:var(--fg)}
article.work h4::before{content:none}
article.work p{margin:0}
article.work .sub{color:var(--muted);font-size:.92rem}
article.work .badges img{height:20px;vertical-align:middle;margin:2px 4px 2px 0}
article.work .tags{display:flex;flex-wrap:wrap;gap:4px;list-style:none;padding:0;margin:2px 0 0}
article.work .tags li{font-size:.78rem;background:var(--soft);border:1px solid var(--line);border-radius:999px;padding:0 8px;margin:0}
article.work .links{font-size:.9rem;margin-top:auto;padding-top:4px}
article.work.featured{grid-column:1/-1;padding:0;overflow:hidden}
article.work.featured+article.work{grid-column:1/-1}
article.work.featured .shot{background:#0b0d12;border-bottom:1px solid var(--line)}
article.work.featured .shot img{display:block;width:100%;height:auto}
article.work.featured .body{padding:14px 16px}
.timeline{--tl-label:17em;margin:0 0 24px;font-size:.85rem}
.tl-axis{position:relative;height:1.5em;margin-left:var(--tl-label);color:var(--muted)}
.tl-axis span{position:absolute;top:0;padding-left:4px;font-size:.78rem}
.tl-row{display:grid;grid-template-columns:var(--tl-label) minmax(0,1fr);align-items:center;margin:3px 0}
.tl-label{padding-right:10px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.tl-label .num{display:inline-block;font-size:.72rem;font-weight:600;color:#fff;background:var(--accent);border-radius:999px;padding:0 6px;margin-right:6px}
.tl-track{position:relative;height:22px;background-image:linear-gradient(to right,var(--line) 1px,transparent 1px);border-right:1px solid var(--line)}
.tl-bar{position:absolute;top:3px;height:16px;border-radius:3px;background:var(--accent);opacity:.9}
.tl-bar:hover{opacity:1;outline:2px solid var(--fg)}
.tl-bar.outsourced,.sw.outsourced{background:#2e8b57}
.tl-bar.parttime,.sw.parttime{background:#8a9bb0}
.tl-legend{color:var(--muted);font-size:.8rem;margin:8px 0 0 var(--tl-label)}
.sw{display:inline-block;width:12px;height:12px;border-radius:2px;background:var(--accent);vertical-align:-1px;margin:0 4px 0 12px}
.sw:first-child{margin-left:0}
@media (max-width:719px){.timeline{--tl-label:0px}.tl-row{grid-template-columns:1fr;margin:8px 0}.tl-label{white-space:normal;padding:0 0 2px}}
footer.bottom{margin-top:48px;padding-top:16px;border-top:1px solid var(--line);color:var(--muted);font-size:.85rem;text-align:center}
@media (min-width:720px){.works{grid-template-columns:repeat(2,minmax(0,1fr))}article.work.featured{flex-direction:row}article.work.featured .shot{flex:0 0 46%;border-bottom:0;border-right:1px solid var(--line)}.skills{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}dl.meta{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}dl.meta div.wide{grid-column:1/-1}}
@media print{body{font-size:11px}.tl-bar,.sw,.tl-label .num,article.case h3 .num,article.work .tags li,dl.meta,dl.basic dt,section.sec>h2{-webkit-print-color-adjust:exact;print-color-adjust:exact}.wrap{padding:0}nav.toc,footer.bottom{display:none}article.case{break-inside:avoid;border-color:#999}details{border:0}summary{display:none}}
"""

def email_link():
    """mailto を HTML 中に平文で書かず、JS で組み立てる。JS 無効時は「user [at] domain」と表示。"""
    u, d = SITE["email"].split("@", 1)
    return f'<a class="em" href="#" data-u="{u}" data-d="{d}">{u} [at] {d}</a>'

def build(doc, works=None):
    secs = {s["title"]: s for s in doc["sections"]}
    basic = secs.get("基本情報"); skills = next((s for s in doc["sections"] if "スキル" in s["title"]), None)
    career = next((s for s in doc["sections"] if s["cases"]), None)
    name = next((r[1] for _, rows in basic["blocks"] for r in rows[1:] if r[0] == "氏名"), "shimomo") if basic else "shimomo"
    for a, b in REPLACE: name = name.replace(a, b)
    doc["sections"] = [s for s in doc["sections"] if s["title"]]   # 前書き（作成日）はヘッダで扱う
    body = []
    body.append('<header class="top">')
    body.append(f'<h1>{inline(name)}</h1>')
    body.append(f'<p class="role">{inline(SITE["role"])} / {inline(SITE["location"])}</p>')
    body.append('<ul class="links">'
                f'<li>GitHub: <a href="{SITE["github"]}">{SITE["github"].replace("https://", "")}</a></li>'
                f'<li>Bluesky: <a href="{SITE["bluesky"]}">{SITE["bluesky_label"]}</a></li>'
                f'<li>Email: {email_link()}</li></ul>')
    body.append(f'<p class="updated">最終更新: {date.today().strftime("%Y年%m月%d日")}</p>')
    body.append("</header>")
    entries = []   # (id, 見出し, HTML)
    for s in doc["sections"]:
        if s is basic: h = render_basic(s)
        elif s is skills: h = render_skills(s)
        elif s is career:
            parts = [render_timeline(s["cases"])]
            for kind, val in s["blocks"]:
                parts.append(f'<p class="note">{link_case_refs(inline(val))}</p>' if kind == "p" else render_blocks([(kind, val)]))
            parts += [render_case(c, i) for i, c in enumerate(s["cases"], 1)]
            h = "\n".join(parts)
        else: h = render_blocks(s["blocks"], link_refs=True)
        entries.append((f"sec-{len(entries) + 1}", s["title"], h))
        if works and s["title"] == "自己PR":
            wt, wh = render_works(works)
            if wh: entries.append((f"sec-{len(entries) + 1}", wt, wh))
    body.append('<nav class="toc">' + "".join(f'<a href="#{sid}">{inline(t)}</a>' for sid, t, _ in entries) + '<a href="#sec-contact">連絡先</a></nav>')
    for sid, t, h in entries:
        body.append(f'<section class="sec" id="{sid}"><h2>{inline(t)}</h2>\n{h}\n</section>')
    body.append('<section class="sec" id="sec-contact"><h2>連絡先</h2><ul>'
                f'<li>Email: {email_link()}</li>'
                f'<li>Bluesky: <a href="{SITE["bluesky"]}">{SITE["bluesky_label"]}</a></li>'
                f'<li>GitHub: <a href="{SITE["github"]}">{SITE["github"].replace("https://", "")}</a></li></ul></section>')
    body.append(f'<footer class="bottom"><p>© {date.today().year} shimomo. All rights reserved.</p></footer>')
    head = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{inline(name)} | {inline(SITE["title_suffix"])}</title>
<meta name="description" content="{html.escape(SITE["description"])}">
<meta property="og:title" content="{inline(name)} | {inline(SITE["title_suffix"])}">
<meta property="og:description" content="{html.escape(SITE["description"])}">
<meta property="og:type" content="profile">
{favicon()}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap">
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
"""
    tail = """
</div>
<script>
window.addEventListener('beforeprint',function(){document.querySelectorAll('details').forEach(function(d){d.open=true;});});
document.querySelectorAll('a.em').forEach(function(a){var m=a.dataset.u+'@'+a.dataset.d;a.href='mailto:'+m;a.textContent=m;});
</script>
</body>
</html>
"""
    return head + "\n".join(body) + tail

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", default=os.path.join(here, "resume.md"))
    ap.add_argument("--out", dest="out", default=os.path.join(here, "resume.html"))
    ap.add_argument("--works", dest="works", default=os.path.join(here, "portfolio.md"))
    a = ap.parse_args()
    redact = os.path.join(here, REDACT_FILE)
    if os.path.exists(redact):
        import json
        with open(redact, encoding="utf-8") as f: REPLACE.extend(tuple(p) for p in json.load(f)["replace"])
    else:
        print(f"警告: {REDACT_FILE} がありません。本名・社名は伏せられません。", file=sys.stderr)
    with open(a.inp, encoding="utf-8") as f: lines = f.read().splitlines()
    doc = parse(lines)
    m = next((re.search(r"作成日:\s*(\S+)", l) for l in lines if l.startswith("作成日")), None)
    if m: doc["date"] = m.group(1)
    works = None
    if os.path.exists(a.works):
        with open(a.works, encoding="utf-8") as f: works = parse(f.read().splitlines())
    out = build(doc, works)
    with open(a.out, "w", encoding="utf-8") as f: f.write(out)
    print(f"HTML 生成完了: {a.out}  ({len(out.encode('utf-8')) // 1024} KB)")

if __name__ == "__main__":
    main()

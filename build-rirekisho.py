#!/usr/bin/env python3
# rirekisho.md から履歴書（JIS 様式に近い A4 2 ページ）の HTML を生成するスクリプト
#
#   使い方:  python3 build-rirekisho.py  （通常は ./build.sh rirekisho 経由。PDF 化まで行う）
#   任意指定: --in <入力.md>  --out <出力.html>
#
# md の書式は resume.md と同じ（## 見出し + 表 / 段落）。基本情報に「写真」の行が無ければ写真枠を出さない。
# 【要記入】【要確認】は
# HTML 上で黄色く強調され、build.sh が残数を警告する。

import argparse, html, os, re, sys, importlib.util
from datetime import date

here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("build_html", os.path.join(here, "build-html.py"))
bh = importlib.util.module_from_spec(spec); spec.loader.exec_module(bh)   # parse() / inline() を再利用

def esc(s):
    s = bh.inline(s)
    return re.sub(r"(【要(?:記入|確認)[^】]*】)", r'<mark>\1</mark>', s)

CSS = """
@page{size:A4;margin:12mm 14mm}
*{box-sizing:border-box}
body{font-family:"Yu Mincho","Hiragino Mincho ProN","MS Mincho",serif;font-size:10.5pt;line-height:1.5;color:#000;margin:0;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:182mm;margin:0 auto;page-break-after:always}
.page:last-child{page-break-after:auto}
h1{font-size:20pt;letter-spacing:.5em;margin:0 0 2mm;font-weight:600}
.date{text-align:right;font-size:10pt;margin:0 0 3mm}
table{border-collapse:collapse;width:100%;table-layout:fixed}
tr{page-break-inside:avoid}
th,td{border:1px solid #000;padding:1.4mm 2.2mm;vertical-align:top;text-align:left;font-weight:normal}
th{background:#f3f3f3;white-space:nowrap}
.head{display:flex;gap:4mm;align-items:flex-start;margin-bottom:4mm}
.head table{flex:1}
.photo{width:30mm;height:40mm;border:1px dashed #666;display:flex;align-items:center;justify-content:center;text-align:center;font-size:8pt;color:#666;flex:0 0 30mm;padding:2mm;overflow:hidden}
.photo:has(img){border:1px solid #000;padding:0}
.photo img{width:100%;height:100%;object-fit:cover;display:block}
.kana{font-size:8pt;color:#333}
.name{font-size:16pt}
.hist th.y,.hist th.m{text-align:center}
.hist td.y,.hist td.m{text-align:center;white-space:nowrap}
.hist td.c{text-align:center;font-weight:600}
h2{font-size:11pt;margin:5mm 0 1.5mm;font-weight:600}
.box{border:1px solid #000;padding:2.5mm 3mm;min-height:32mm}
.box p{margin:0 0 1.5mm}
mark{background:#fff3a0}
@media screen{body{background:#eee;padding:10mm 0}.page{background:#fff;padding:12mm 14mm;box-shadow:0 0 6px rgba(0,0,0,.2);margin-bottom:8mm;min-height:297mm}}
"""

def build(doc):
    secs = {s["title"]: s for s in doc["sections"] if s["title"]}
    def table(name):
        s = secs.get(name); return next((rows for k, rows in s["blocks"] if k == "table"), []) if s else []
    def paras(name):
        s = secs.get(name); return [v for k, v in s["blocks"] if k == "p"] if s else []
    basic = {r[0]: r[1] for r in table("基本情報")[1:]}
    created = next((re.search(r"作成日:\s*(\S+)", v).group(1) for s in doc["sections"] for k, v in s["blocks"] if k == "p" and "作成日" in v), date.today().strftime("%Y年%m月%d日"))

    # ---- 1 ページ目: 基本情報 + 学歴・職歴 ----
    p1 = [f"<h1>履歴書</h1><p class=\"date\">{esc(created)} 現在</p>", '<div class="head"><table><colgroup><col style="width:24mm"><col></colgroup>']
    p1.append(f'<tr><th>ふりがな</th><td class="kana">{esc(basic.get("ふりがな",""))}</td></tr>')
    p1.append(f'<tr><th>氏名</th><td class="name">{esc(basic.get("氏名",""))}</td></tr>')
    sex = f'　性別: {esc(basic["性別"])}' if basic.get("性別") else ""   # md に性別の行があるときだけ出す
    p1.append(f'<tr><th>生年月日</th><td>{esc(basic.get("生年月日",""))}（満 {esc(basic.get("年齢",""))} 歳）{sex}</td></tr>')
    p1.append(f'<tr><th>ふりがな</th><td class="kana">{esc(basic.get("住所ふりがな",""))}</td></tr>')
    p1.append(f'<tr><th>現住所</th><td>〒{esc(basic.get("郵便番号",""))}<br>{esc(basic.get("住所",""))}</td></tr>')
    p1.append(f'<tr><th>電話</th><td>{esc(basic.get("電話",""))}</td></tr>')
    p1.append(f'<tr><th>メール</th><td>{esc(basic.get("メール",""))}</td></tr>')
    photo = basic.get("写真", "").strip()
    p1.append('</table>' + (f'<div class="photo">{esc(photo)}</div>' if photo else '') + '</div>')   # 写真の行が無ければ枠ごと省く
    p1.append('<table class="hist"><colgroup><col style="width:18mm"><col style="width:10mm"><col></colgroup><tr><th class="y">年</th><th class="m">月</th><th>学歴・職歴</th></tr>')
    for y, m, c in table("学歴・職歴")[1:]:
        if not y and not m:
            p1.append(f'<tr><td class="y"></td><td class="m"></td><td class="{"c" if c in ("学歴","職歴") else ""}">{esc(c)}</td></tr>')
        else:
            p1.append(f'<tr><td class="y">{esc(y)}</td><td class="m">{esc(m)}</td><td>{esc(c)}</td></tr>')
    p1.append("</table>")

    # ---- 2 ページ目: 免許・資格 / 志望動機 / 自己PR / 本人希望 / 通勤・家族 ----
    p2 = ['<table class="hist"><colgroup><col style="width:18mm"><col style="width:10mm"><col></colgroup><tr><th class="y">年</th><th class="m">月</th><th>免許・資格</th></tr>']
    for y, m, c in table("免許・資格")[1:]:
        p2.append(f'<tr><td class="y">{esc(y)}</td><td class="m">{esc(m)}</td><td>{esc(c)}</td></tr>')
    p2.append("</table>")
    for name in ("志望動機", "自己PR", "本人希望記入欄"):
        p2.append(f"<h2>{name}</h2><div class=\"box\">" + "".join(f"<p>{esc(p)}</p>" for p in paras(name)) + "</div>")
    fam = table("通勤・家族")[1:]
    if fam:
        p2.append('<h2>通勤時間・扶養家族・配偶者</h2><table><colgroup><col style="width:52mm"><col></colgroup>' + "".join(f"<tr><th>{esc(k)}</th><td>{esc(v)}</td></tr>" for k, v in fam) + "</table>")

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>履歴書</title>
<meta name="robots" content="noindex">
<style>{CSS}</style>
</head>
<body>
<div class="page">
{chr(10).join(p1)}
</div>
<div class="page">
{chr(10).join(p2)}
</div>
</body>
</html>
"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", default=os.path.join(here, "rirekisho.md"))
    ap.add_argument("--out", dest="out", default=os.path.join(here, "rirekisho.html"))
    a = ap.parse_args()
    with open(a.inp, encoding="utf-8") as f: lines = f.read().splitlines()
    out = build(bh.parse(lines))
    with open(a.out, "w", encoding="utf-8") as f: f.write(out)
    todo = len(re.findall(r"【要(?:記入|確認)", out))
    print(f"HTML 生成完了: {a.out}  ({len(out.encode()) // 1024} KB)" + (f"  ※ 未記入・要確認 {todo} 件" if todo else ""))

if __name__ == "__main__":
    main()

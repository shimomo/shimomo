# resume.md から印刷用 PDF を生成するスクリプト
#
#   使い方:  pwsh -ExecutionPolicy Bypass -File "build-pdf.ps1"（WSL からは ./build.sh pdf）
#   任意指定: -In <入力.md>  -Out <出力.pdf>  -KeepHtml
#
# pandoc / Node を使わず、Markdown を印刷用 HTML に変換したうえで
# Chrome（なければ Edge）のヘッドレスモードで PDF 化する。
# A4・全4ページに収まる密度に調整済み。
# 文字を大きくしたい場合は下部 $style の font-size / line-height を変更する。

param(
  [string]$In  = "$PSScriptRoot\resume.md",
  [string]$Out = "$PSScriptRoot\resume.pdf",
  [switch]$KeepHtml
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $In)) { throw "入力ファイルが見つかりません: $In" }

# ---- ブラウザの検出 -------------------------------------------------------
$browsers = @(
  "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
  "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
  "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe",
  "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe"
)
$browser = $browsers | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $browser) { throw "Chrome / Edge が見つかりません。PDF 化にはどちらかが必要です。" }

# ---- Markdown -> HTML -----------------------------------------------------

function JoinSmart([string]$a, [string]$b) {
  if ([string]::IsNullOrEmpty($a)) { return $b }
  if ([string]::IsNullOrEmpty($b)) { return $a }
  $la = $a.Substring($a.Length - 1, 1)
  $fb = $b.Substring(0, 1)
  # 和文と英数字が隣接する場合のみスペースを補う
  if (($la -match '[^\x00-\x7F]') -and ($fb -match '[A-Za-z0-9]')) { return $a + ' ' + $b }
  if (($la -match '[A-Za-z0-9\)\.]') -and ($fb -match '[^\x00-\x7F]')) { return $a + ' ' + $b }
  return $a + $b
}

function Esc([string]$s) {
  $s = $s -replace '&', '&amp;' -replace '<', '&lt;' -replace '>', '&gt;'
  $s = [regex]::Replace($s, '`([^`]+)`', '<code>$1</code>')
  $s = [regex]::Replace($s, '\[([^\]]+)\]\(([^)]+)\)', '$1')
  $s = [regex]::Replace($s, '\*\*([^*]+)\*\*', '<strong>$1</strong>')
  return $s
}

$lines = Get-Content -LiteralPath $In -Encoding UTF8
$html  = New-Object System.Collections.Generic.List[string]

$i = 0
$para = New-Object System.Collections.Generic.List[string]
$listOpen = 0
$liBuf = $null
$lastWasH3 = $false
$curH2 = ''

function FlushPara {
  if ($script:para.Count -gt 0) {
    $acc = ''
    foreach ($seg in $script:para) { $acc = JoinSmart $acc $seg }
    $script:html.Add('<p>' + (Esc $acc) + '</p>')
    $script:para.Clear()
  }
}
function FlushLi {
  if ($script:liBuf -ne $null) {
    $script:html.Add('<li>' + (Esc $script:liBuf) + '</li>')
    $script:liBuf = $null
  }
}
function CloseList {
  FlushLi
  while ($script:listOpen -gt 0) { $script:html.Add('</ul>'); $script:listOpen-- }
}
function RenderTable($dataRows, [string]$cls) {
  $sb = New-Object System.Collections.Generic.List[string]
  $sb.Add("<table class=`"$cls`">")
  $r = 0
  foreach ($cells in $dataRows) {
    $tag = if ($r -eq 0) { 'th' } else { 'td' }
    $line = '<tr>'
    foreach ($c in $cells) { $line += "<$tag>" + (Esc $c) + "</$tag>" }
    $line += '</tr>'
    $sb.Add($line)
    $r++
  }
  $sb.Add('</table>')
  return $sb
}

while ($i -lt $lines.Count) {
  $raw  = $lines[$i]
  $line = $raw.TrimEnd()

  if ($line -match '^\s*$') { FlushPara; CloseList; $i++; continue }

  # 見出し
  if ($line -match '^(#{1,4})\s+(.*)$') {
    FlushPara; CloseList
    $lv = $Matches[1].Length
    $txt = $Matches[2]
    $html.Add("<h$lv>" + (Esc $txt) + "</h$lv>")
    if ($lv -eq 2) { $curH2 = $txt }
    $lastWasH3 = ($lv -eq 3)
    $i++; continue
  }

  # テーブル
  if ($line -match '^\s*\|') {
    FlushPara; CloseList
    $rows = @()
    while ($i -lt $lines.Count -and $lines[$i].TrimEnd() -match '^\s*\|') {
      $rt = $lines[$i].Trim()
      if ($rt -notmatch '^\|[\s:\-\|]+\|$') {
        $rows += ,(@($rt.Trim('|') -split '\|' | ForEach-Object { $_.Trim() }))
      }
      $i++
    }

    if ($lastWasH3) {
      # 案件のメタ情報: 表を1ブロックの帯に圧縮
      $parts = @()
      for ($k = 1; $k -lt $rows.Count; $k++) {
        $parts += '<b>' + (Esc $rows[$k][0]) + '</b> ' + (Esc $rows[$k][1])
      }
      $html.Add('<p class="meta">' + ($parts -join '<span class="sep">｜</span>') + '</p>')
    }
    elseif ($curH2 -like '*経験スキル*') {
      # スキル表: グループ境界のうち中央に最も近い位置で2段組に分割
      $header = $rows[0]
      $data   = $rows[1..($rows.Count - 1)]
      $mid = [int][Math]::Round($data.Count / 2)
      $split = -1
      foreach ($d in 1..($data.Count - 1)) {
        if ($data[$d][0] -ne '') {
          if ($split -lt 0 -or [Math]::Abs($d - $mid) -lt [Math]::Abs($split - $mid)) { $split = $d }
        }
      }
      if ($split -lt 0) { $split = $mid }

      # 注: @() での連結は配列要素をフラット化するため List で組む
      $left  = New-Object System.Collections.Generic.List[object]
      $right = New-Object System.Collections.Generic.List[object]
      $left.Add($header); $right.Add($header)
      for ($d = 0; $d -lt $data.Count; $d++) {
        if ($d -lt $split) { $left.Add($data[$d]) } else { $right.Add($data[$d]) }
      }
      $html.Add('<div class="skills">')
      foreach ($l in (RenderTable $left  'sk')) { $html.Add($l) }
      foreach ($l in (RenderTable $right 'sk')) { $html.Add($l) }
      $html.Add('</div>')
    }
    else {
      foreach ($l in (RenderTable $rows '')) { $html.Add($l) }
    }
    $lastWasH3 = $false
    continue
  }

  # ≪見出し≫
  if ($line -match '^≪(.+)≫\s*$') {
    FlushPara; CloseList
    $html.Add('<h5>' + (Esc $Matches[1]) + '</h5>')
    $lastWasH3 = $false
    $i++; continue
  }

  # 箇条書き（第2階層）
  if ($line -match '^\s{2,3}-\s+(.*)$') {
    FlushPara; FlushLi
    if ($listOpen -eq 0) { $html.Add('<ul>'); $listOpen = 1 }
    if ($listOpen -eq 1) { $html.Add('<ul class="sub">'); $listOpen = 2 }
    $liBuf = $Matches[1]; $lastWasH3 = $false
    $i++; continue
  }

  # 箇条書き（第1階層）
  if ($line -match '^-\s+(.*)$') {
    FlushPara; FlushLi
    if ($listOpen -eq 2) { $html.Add('</ul>'); $listOpen = 1 }
    if ($listOpen -eq 0) { $html.Add('<ul>'); $listOpen = 1 }
    $liBuf = $Matches[1]; $lastWasH3 = $false
    $i++; continue
  }

  # 箇条書き内の折り返し継続行
  if ($listOpen -gt 0 -and $raw -match '^\s{2,}\S') {
    $liBuf = JoinSmart $liBuf $line.Trim()
    $i++; continue
  }

  # 通常段落（折り返しは連結）
  CloseList
  $para.Add($line.Trim())
  $lastWasH3 = $false
  $i++
}
FlushPara
CloseList

$style = @'
<style>
@page { size: A4; margin: 10mm 10mm 10mm 10mm; }
* { box-sizing: border-box; }
body {
  font-family: "Yu Gothic UI","Yu Gothic","Meiryo","Hiragino Kaku Gothic ProN",sans-serif;
  font-size: 8pt; line-height: 1.38; color: #1a1a1a; margin: 0;
  -webkit-print-color-adjust: exact; print-color-adjust: exact;
}
h1 {
  font-size: 13.5pt; letter-spacing: .24em; text-align: center;
  margin: 0 0 1.2mm; padding-bottom: 1.6mm; border-bottom: 2px solid #1a1a1a; font-weight: 600;
}
h2 {
  font-size: 9.5pt; font-weight: 600; margin: 3.4mm 0 1.4mm; padding: .6mm 0 .6mm 2.2mm;
  border-left: 3.5px solid #1a1a1a; background: #f2f2f2; break-after: avoid;
}
h3 {
  font-size: 8.8pt; font-weight: 600; margin: 3.2mm 0 1.1mm; padding-bottom: .8mm;
  border-bottom: 1px solid #999; break-after: avoid;
}
h5 {
  font-size: 8pt; font-weight: 600; margin: 2mm 0 .5mm; color: #000; break-after: avoid;
}
h5::before { content: "\25a0"; font-size: 6pt; margin-right: 1.1mm; vertical-align: 1px; }
p { margin: 0 0 1.2mm; text-align: justify; }

p.meta {
  font-size: 7.6pt; line-height: 1.5; background: #f7f7f7; border: 1px solid #dcdcdc;
  padding: 1mm 1.6mm; margin: 0 0 1.4mm; text-align: left; break-inside: avoid;
}
p.meta b { font-weight: 600; }
p.meta .sep { color: #b0b0b0; margin: 0 1.2mm; }

table {
  width: 100%; border-collapse: collapse; margin: 0 0 1.6mm;
  break-inside: avoid; font-size: 7.6pt;
}
th, td { border: 1px solid #b8b8b8; padding: .8mm 1.4mm; vertical-align: top; text-align: left; }
th { background: #ededed; font-weight: 600; white-space: nowrap; }
tr > td:first-child { background: #fafafa; font-weight: 600; width: 26mm; white-space: nowrap; }
table tr > th:first-child { width: 26mm; }

.skills { display: flex; gap: 2.2mm; break-inside: avoid; margin-bottom: 1.6mm; }
.skills table { width: 50%; margin: 0; font-size: 7pt; }
.skills th, .skills td { padding: .55mm 1.1mm; }
.skills tr > td:first-child { width: 12mm; white-space: normal; }
.skills tr > th:first-child { width: 12mm; }
.skills tr > td:nth-child(3) { white-space: nowrap; }

ul { margin: 0 0 1.2mm; padding-left: 4.2mm; }
ul.sub { margin: .3mm 0; padding-left: 4.2mm; }
li { margin-bottom: .3mm; }
ul.sub > li { color: #333; font-size: 7.7pt; }
code { font-family: Consolas,monospace; font-size: 7.4pt; background: #f0f0f0; padding: 0 .7mm; }
</style>
'@

$head = '<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8"><title>職務経歴書</title>' + $style + '</head><body>'
$doc  = $head + ($html -join "`n") + '</body></html>'

# ---- HTML -> PDF ----------------------------------------------------------
# Chrome は同名ファイルをキャッシュすることがあるため、毎回一意な一時ファイルを使う
$tmpHtml = Join-Path ([System.IO.Path]::GetTempPath()) ("resume_" + [guid]::NewGuid().ToString('N') + ".html")
[System.IO.File]::WriteAllText($tmpHtml, $doc, (New-Object System.Text.UTF8Encoding($false)))

$uri = 'file:///' + ($tmpHtml -replace '\\', '/')
& $browser --headless --disable-gpu --no-pdf-header-footer --virtual-time-budget=5000 `
           --print-to-pdf="$Out" $uri 2>&1 | Out-Null

if ($KeepHtml) {
  $sideHtml = [System.IO.Path]::ChangeExtension($Out, '.html')
  Copy-Item -LiteralPath $tmpHtml -Destination $sideHtml -Force
  Write-Host "HTML: $sideHtml"
}
Remove-Item -LiteralPath $tmpHtml -Force -ErrorAction SilentlyContinue

if (Test-Path -LiteralPath $Out) {
  $kb = [int]((Get-Item -LiteralPath $Out).Length / 1KB)
  Write-Host "PDF 生成完了: $Out  ($kb KB)"
  Write-Host "使用ブラウザ: $browser"
} else {
  throw "PDF の生成に失敗しました。"
}

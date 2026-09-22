# resume.md の内容を resume.xlsx へ反映するスクリプト
#
#   使い方:  pwsh -ExecutionPolicy Bypass -File "update-xlsx.ps1"（Excel のあるマシンで実行）
#   任意指定: -Md <入力.md>  -Xlsx <更新先.xlsx>  -NoBackup
#
# Markdown を正本とし、xlsx の書式（結合セル・列幅・配色）は保ったまま値だけを差し替える。
# Excel COM を使うため Excel のインストールが必要。
#
# xlsx 側のレイアウト（変更すると本スクリプトも要修正）:
#   ・基本情報   D5 氏名 / D6 生年月日 / D7 都道府県 / S5 学歴 / S6 資格
#                D9 得意分野 / D10 得意技術 / D11 得意工程
#                D13 職務要約 / D14 自己PR / A15 ラベル・D15 リンク / AC3 作成日
#   ・スキル表   F=スキル L=経験年数 R=レベル。グループごとに行範囲が固定
#   ・案件欄     1案件 = 4行ブロック。開始行は 46,50,54,58,64,68,72,76 の8スロット
#                A=番号 B=期間 B+2=期間の長さ E=タイトル E+1=本文
#                Q=役割 Q+1=規模 S=言語 U=DB W=OS Y=FW AA〜AG=担当工程の●

param(
  [string]$Md   = "$PSScriptRoot\resume.md",
  [string]$Xlsx = "$PSScriptRoot\resume.xlsx",
  [switch]$NoBackup
)

$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $Md))   { throw "Markdown が見つかりません: $Md" }
if (-not (Test-Path -LiteralPath $Xlsx)) { throw "xlsx が見つかりません: $Xlsx" }

# スキルのグループ名 -> xlsx の行範囲
$skillRanges = [ordered]@{
  '言語'             = 19..25
  'DB'               = 26..28
  'サーバーOS'       = 29..31
  'フレームワーク'   = 32..39   # 「フレームワーク / ツール」の前方一致で判定
  '環境'             = 40..42
}
# 担当工程 -> 列
$stepCols = [ordered]@{
  '要件定義'   = 'AA'; '基本設計' = 'AB'; '詳細設計' = 'AC'; '構築・設定' = 'AD'
  '運用設計'   = 'AE'; '保守・運用' = 'AF'; '障害対応' = 'AG'
}
$slots = @(46, 50, 54, 58, 64, 68, 72, 76)

# ---- Markdown 解析 ---------------------------------------------------------

function JoinSmart([string]$a, [string]$b) {
  if ([string]::IsNullOrEmpty($a)) { return $b }
  if ([string]::IsNullOrEmpty($b)) { return $a }
  $la = $a.Substring($a.Length - 1, 1); $fb = $b.Substring(0, 1)
  if (($la -match '[^\x00-\x7F]') -and ($fb -match '[A-Za-z0-9]')) { return $a + ' ' + $b }
  if (($la -match '[A-Za-z0-9\)\.]') -and ($fb -match '[^\x00-\x7F]')) { return $a + ' ' + $b }
  return $a + $b
}
function Plain([string]$s) {
  $s = [regex]::Replace($s, '\[([^\]]+)\]\(([^)]+)\)', '$1')
  $s = [regex]::Replace($s, '\*\*([^*]+)\*\*', '$1')
  $s = $s -replace '`', ''
  return $s
}
# 狭い列（言語 / DB / OS / FW）向けに読点や括弧で改行を入れる
function WrapNarrow([string]$s) {
  if ([string]::IsNullOrWhiteSpace($s) -or $s -eq '－') { return '' }
  $s = $s -replace '、', "`n" -replace '／', "`n"
  $s = $s -replace '\s*\(', "`n("
  $s = $s -replace '（', "`n（"
  $s = $s -replace '。', "。`n"
  $s = $s -replace '[ \t]+', ' '
  return ($s -replace "`n{2,}", "`n").Trim()
}

$lines = Get-Content -LiteralPath $Md -Encoding UTF8
$doc = @{ Basic = @{}; Summary = ''; PR = ''; Skills = @(); Entries = @(); Created = '' }

$i = 0; $section = ''; $entry = $null
$paraBuf = New-Object System.Collections.Generic.List[string]
$secName = $null
$bullets = New-Object System.Collections.Generic.List[string]
$lastBullet = $null

function FlushBullet {
  if ($script:lastBullet -ne $null) { $script:bullets.Add($script:lastBullet); $script:lastBullet = $null }
}
function FlushSection {
  FlushBullet
  if ($script:secName -and $script:entry) {
    $script:entry.Sections += ,@{ Name = $script:secName; Items = @($script:bullets) }
  }
  $script:bullets = New-Object System.Collections.Generic.List[string]
  $script:secName = $null
}
function FlushPara {
  FlushBullet
  if ($script:paraBuf.Count -gt 0) {
    $acc = ''
    foreach ($seg in $script:paraBuf) { $acc = JoinSmart $acc $seg }
    $script:paraBuf.Clear()
    return (Plain $acc)
  }
  return $null
}

while ($i -lt $lines.Count) {
  $raw = $lines[$i]; $line = $raw.TrimEnd()

  if ($line -match '^作成日:\s*(.+)$') { $doc.Created = "作成日:" + $Matches[1].Trim(); $i++; continue }

  if ($line -match '^##\s+(.+)$' -and $line -notmatch '^###') {
    $p = FlushPara; if ($p) { if ($section -eq 'summary') { $doc.Summary += ($p + "`n") } elseif ($section -eq 'pr') { $doc.PR += ($p + "`n") } }
    FlushSection
    $h = $Matches[1].Trim()
    $section = switch -Regex ($h) {
      '基本情報'       { 'basic' }
      '職務要約'       { 'summary' }
      '自己PR'         { 'pr' }
      '経験スキル'     { 'skills' }
      '職務経歴'       { 'career' }
      default          { '' }
    }
    $i++; continue
  }

  if ($line -match '^###\s+No\.(\d+)\s+(.*)$') {
    $p = FlushPara
    if ($p -and $entry) { $entry.Intro += ($p + "`n") }
    FlushSection
    $num = $Matches[1]; $rest = (Plain $Matches[2]).Trim()
    $org = $rest; $name = ''
    if ($rest -match '^(.*?)\s+/\s+(.*)$') { $org = $Matches[1].Trim(); $name = $Matches[2].Trim() }
    $entry = @{ Num = $num; Org = $org; Name = $name; Meta = @{}; Intro = ''; Sections = @() }
    $doc.Entries += $entry
    $i++; continue
  }

  if ($line -match '^≪(.+)≫\s*$') {
    $p = FlushPara; if ($p -and $entry) { $entry.Intro += ($p + "`n") }
    FlushSection
    $secName = $Matches[1].Trim()
    $i++; continue
  }

  # 表
  if ($line -match '^\s*\|') {
    $p = FlushPara
    if ($p) {
      if ($section -eq 'summary') { $doc.Summary += ($p + "`n") }
      elseif ($section -eq 'pr')  { $doc.PR += ($p + "`n") }
      elseif ($entry)             { $entry.Intro += ($p + "`n") }
    }
    $rows = @()
    while ($i -lt $lines.Count -and $lines[$i].TrimEnd() -match '^\s*\|') {
      $rt = $lines[$i].Trim()
      if ($rt -notmatch '^\|[\s:\-\|]+\|$') { $rows += ,(@($rt.Trim('|') -split '\|' | ForEach-Object { (Plain $_).Trim() })) }
      $i++
    }
    if ($section -eq 'basic') {
      foreach ($r in $rows) { if ($r.Count -ge 2 -and $r[0] -ne '項目') { $doc.Basic[$r[0]] = $r[1] } }
    }
    elseif ($section -eq 'skills') {
      $group = ''
      foreach ($r in $rows) {
        if ($r[0] -eq '項目') { continue }
        if ($r[0] -ne '') { $group = $r[0] }
        $doc.Skills += ,@{ Group = $group; Name = $r[1]; Years = $r[2]; Level = $r[3] }
      }
    }
    elseif ($entry) {
      foreach ($r in $rows) { if ($r.Count -ge 2 -and $r[0] -ne '項目') { $entry.Meta[$r[0]] = $r[1] } }
    }
    continue
  }

  # 箇条書き
  if ($line -match '^\s{2,3}-\s+(.*)$') { FlushBullet; $lastBullet = '　－' + (Plain $Matches[1]); $i++; continue }
  if ($line -match '^-\s+(.*)$')        { FlushBullet; $lastBullet = '・'   + (Plain $Matches[1]); $i++; continue }
  if ($lastBullet -ne $null -and $raw -match '^\s{2,}\S') { $lastBullet = JoinSmart $lastBullet (Plain $line.Trim()); $i++; continue }

  if ($line -match '^\s*$') {
    $p = FlushPara
    if ($p) {
      if ($section -eq 'summary') { $doc.Summary += ($p + "`n") }
      elseif ($section -eq 'pr')  { $doc.PR += ($p + "`n") }
      elseif ($entry -and -not $secName) { $entry.Intro += ($p + "`n") }
    }
    FlushBullet
    $i++; continue
  }

  if ($line -match '^#\s') { $i++; continue }           # タイトル行
  if ($line -match '^※')  { $i++; continue }           # 注記行（xlsx には持ち込まない）

  $paraBuf.Add($line.Trim())
  $i++
}
$p = FlushPara
if ($p) { if ($section -eq 'summary') { $doc.Summary += ($p + "`n") } elseif ($section -eq 'pr') { $doc.PR += ($p + "`n") } elseif ($entry -and -not $secName) { $entry.Intro += ($p + "`n") } }
FlushSection

if ($doc.Entries.Count -gt $slots.Count) {
  throw "案件が $($doc.Entries.Count) 件あります。xlsx のスロットは $($slots.Count) 件までです。行ブロックの追加が必要です。"
}

# ---- Excel へ反映 ----------------------------------------------------------

if (-not $NoBackup) {
  $bak = [System.IO.Path]::ChangeExtension($Xlsx, ".bak.xlsx")
  Copy-Item -LiteralPath $Xlsx -Destination $bak -Force
  Write-Host "バックアップ: $bak"
}

$xl = New-Object -ComObject Excel.Application
$xl.Visible = $false; $xl.DisplayAlerts = $false; $xl.ScreenUpdating = $false
$wb = $xl.Workbooks.Open($Xlsx)
$ws = $wb.Sheets.Item(1)

try {
  if ($doc.Created) { $ws.Range("AC3").Value2 = $doc.Created }
  if ($doc.Basic['氏名'])     { $ws.Range("D5").Value2 = $doc.Basic['氏名'] }
  if ($doc.Basic['生年月日']) {
    $d = $doc.Basic['生年月日']
    if ($d -match '(\d{4})年(\d{1,2})月(\d{1,2})日') {
      # 注: Value2 に数値を代入すると PowerShell の COM バインダが
      #     直前の文字列代入で型を固定してしまい InvalidCastException になる。
      #     Excel 側で日付として解釈される文字列を渡し、セルの表示形式に任せる。
      $ws.Range("D6").Value2 = ('{0}/{1:d2}/{2:d2}' -f $Matches[1], [int]$Matches[2], [int]$Matches[3])
    }
  }
  if ($doc.Basic['都道府県']) { $ws.Range("D7").Value2 = $doc.Basic['都道府県'] }
  if ($doc.Basic['学歴'])     { $ws.Range("S5").Value2 = $doc.Basic['学歴'] }
  if ($doc.Basic['資格'])     { $ws.Range("S6").Value2 = ($doc.Basic['資格'] -replace '^－$','') }
  if ($doc.Basic['得意分野']) { $ws.Range("D9").Value2  = $doc.Basic['得意分野'] }
  if ($doc.Basic['得意技術']) { $ws.Range("D10").Value2 = $doc.Basic['得意技術'] }
  if ($doc.Basic['得意工程']) { $ws.Range("D11").Value2 = $doc.Basic['得意工程'] }

  $urlLabels = @(); $urls = @()
  foreach ($k in @('ポートフォリオ','GitHub')) {
    if ($doc.Basic[$k]) { $urlLabels += $k; $urls += $doc.Basic[$k] }
  }
  if ($urls.Count -gt 0) {
    $ws.Range("A15").Value2 = ($urlLabels -join "`n")
    $ws.Range("D15").Value2 = ($urls -join "`n")
  }

  $ws.Range("D13").Value2 = $doc.Summary.TrimEnd("`n")
  $ws.Range("D14").Value2 = $doc.PR.TrimEnd("`n")

  # スキル表
  foreach ($rng in $skillRanges.Values) {
    foreach ($r in $rng) { $ws.Range("F$r").Value2=''; $ws.Range("L$r").Value2=''; $ws.Range("R$r").Value2='' }
  }
  foreach ($g in $skillRanges.Keys) {
    $items = @($doc.Skills | Where-Object { $_.Group -like "$g*" })
    $rows = $skillRanges[$g]
    if ($items.Count -gt $rows.Count) {
      throw "スキル『$g』が $($items.Count) 件ありますが、xlsx の行数は $($rows.Count) です。行の追加が必要です。"
    }
    for ($k = 0; $k -lt $items.Count; $k++) {
      $r = $rows[$k]
      $ws.Range("F$r").Value2 = $items[$k].Name
      $ws.Range("L$r").Value2 = $items[$k].Years
      $ws.Range("R$r").Value2 = $items[$k].Level
    }
  }

  # 案件欄をすべてクリア
  foreach ($row in $slots) {
    foreach ($col in @('B','E','Q','S','U','W','Y')) { $ws.Range("$col$row").Value2 = '' }
    $ws.Range("B$($row+2)").Value2 = ''
    $ws.Range("E$($row+1)").Value2 = ''
    $ws.Range("Q$($row+1)").Value2 = ''
    foreach ($c in $stepCols.Values) { $ws.Range("$c$row").Value2 = '' }
  }

  $bodyRows = @()
  for ($n = 0; $n -lt $doc.Entries.Count; $n++) {
    $e = $doc.Entries[$n]; $r = $slots[$n]
    $m = $e.Meta

    # 期間 「2025年09月 - 2026年08月（1年）」
    $kikan = $m['期間']; $len = ''
    if ($kikan -match '^(.*?)\s*[-−]\s*(.*?)（(.+)）\s*$') {
      $ws.Range("B$r").Value2 = ($Matches[1].Trim() + "`n-`n" + $Matches[2].Trim())
      $len = $Matches[3].Trim()
    } else { $ws.Range("B$r").Value2 = $kikan }
    $ws.Range("B$($r+2)").Value2 = $len

    # タイトル（契約形態があれば所属として使う）
    $org = $e.Org
    if ($m['契約形態']) { $org = $m['契約形態'] }
    $title = $org
    if ($e.Name) { $title += "`n" + ($e.Name -replace '　', '') }
    $ws.Range("E$r").Value2 = $title

    # 役割 ／ 規模
    $rs = $m['役割 - 規模']
    if ($rs) {
      $parts = $rs -split '／', 2
      $ws.Range("Q$r").Value2      = (WrapNarrow $parts[0].Trim())
      if ($parts.Count -gt 1) { $ws.Range("Q$($r+1)").Value2 = (WrapNarrow $parts[1].Trim()) }
    }

    $ws.Range("S$r").Value2 = (WrapNarrow $m['開発言語'])
    $ws.Range("U$r").Value2 = (WrapNarrow $m['DB'])
    $ws.Range("W$r").Value2 = (WrapNarrow $m['サーバーOS'])
    $ws.Range("Y$r").Value2 = (WrapNarrow $m['FW・ツール等'])

    # 担当工程
    if ($m['担当工程']) {
      foreach ($s in ($m['担当工程'] -split '／')) {
        $s = $s.Trim()
        if ($stepCols.Contains($s)) { $ws.Range("$($stepCols[$s])$r").Value2 = '●' }
        elseif ($s) { Write-Warning "No.$($e.Num): 担当工程『$s』に対応する列がありません" }
      }
    }

    # 本文
    $sb = New-Object System.Collections.Generic.List[string]
    if ($e.Intro) { $sb.Add($e.Intro.TrimEnd("`n")) }
    foreach ($sec in $e.Sections) {
      $sb.Add('')
      $sb.Add('≪' + $sec.Name + '≫')
      foreach ($it in $sec.Items) { $sb.Add($it) }
    }
    $ws.Range("E$($r+1)").Value2 = ($sb -join "`n")
    $bodyRows += $r
  }

  # 結合セルは自動で伸びないため、必要高さを実測して行高を設定する
  $probeCol = 70
  $origW = $ws.Columns.Item($probeCol).ColumnWidth
  $probe = $ws.Cells.Item(200, $probeCol)
  $probe.WrapText = $true

  function Fit($srcAddr, $firstCol, $lastCol, $targetRow, $otherRows, $minH) {
    $w = 0; foreach ($c in $firstCol..$lastCol) { $w += $ws.Columns.Item($c).ColumnWidth }
    $ws.Columns.Item($probeCol).ColumnWidth = $w
    $f = $ws.Range($srcAddr).Font
    $probe.Font.Name = $f.Name; $probe.Font.Size = $f.Size
    $probe.Value2 = $ws.Range($srcAddr).Value2
    $ws.Rows.Item(200).AutoFit() | Out-Null
    $need = $ws.Rows.Item(200).RowHeight + 8
    $rest = 0; foreach ($rr in $otherRows) { $rest += $ws.Rows.Item($rr).RowHeight }
    $ws.Rows.Item($targetRow).RowHeight = [Math]::Max($minH, $need - $rest)
  }

  Fit "D13" 4 33 13 @() 88
  Fit "D14" 4 33 14 @() 88
  Fit "D15" 4 33 15 @() 39
  foreach ($r in $bodyRows) { Fit "E$($r+1)" 5 16 ($r+1) @(($r+2), ($r+3)) 197 }

  $probe.Value2 = ''
  $ws.Rows.Item(200).RowHeight = 13
  $ws.Columns.Item($probeCol).ColumnWidth = $origW

  $wb.Save()
  $saved = $true
  Write-Host "更新完了: $Xlsx"
  Write-Host "  案件 $($doc.Entries.Count) 件 / スキル $($doc.Skills.Count) 件を反映しました。"
}
finally {
  # 途中で失敗した場合は保存せずに閉じる（中途半端な状態を残さない）
  $wb.Close($false)
  if (-not $saved) { Write-Warning "エラーのため保存していません。xlsx は元のままです。" }
  $xl.Quit()
  [System.Runtime.InteropServices.Marshal]::ReleaseComObject($xl) | Out-Null
  [GC]::Collect()
}

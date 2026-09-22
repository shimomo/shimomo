#!/usr/bin/env bash
# 職務経歴書とポートフォリオのビルド・配置を WSL から一括で行うスクリプト
#
#   ./build.sh html     resume.md + portfolio.md から Web 版（resume.html）を生成
#   ./build.sh pdf      resume.md から送付用 PDF（resume.pdf）を生成（Windows 側の pwsh + Chrome を利用）
#   ./build.sh deploy   Web 版と assets/ を shimomo.net（さくら）へ配置し、公開内容を検証
#   ./build.sh all      html → pdf → deploy を順に実行
#
# xlsx（update-xlsx.ps1）は Excel が必要なため、このスクリプトでは扱わない。

set -euo pipefail
cd "$(dirname "$(readlink -f "$0")")"

REMOTE="sakura"                          # ~/.ssh/config のホスト名
REMOTE_DIR="/home/shimomo/www/home"      # shimomo.net のドキュメントルート
SITE_URL="https://shimomo.net"
HTML="resume.html"
PDF="resume.pdf"
REDACT="redact.json"

log()  { printf '\033[1;34m==>\033[0m %s\n' "$*"; }
fail() { printf '\033[1;31mエラー:\033[0m %s\n' "$*" >&2; exit 1; }

cmd_html() {
  log "Web 版を生成"
  python3 build-html.py
}

cmd_pdf() {
  log "PDF を生成（Windows の pwsh + Chrome）"
  command -v pwsh.exe >/dev/null || fail "pwsh.exe が見つかりません（PowerShell 7 を Windows にインストールしてください）"
  local script; script="$(wslpath -w "$PWD/build-pdf.ps1")"
  pwsh.exe -NoProfile -ExecutionPolicy Bypass -Command \
    "[Console]::OutputEncoding=[System.Text.Encoding]::UTF8; & '$script'"
  [ -f "$PDF" ] || fail "$PDF が生成されていません"
  if command -v pdfinfo >/dev/null; then
    local pages; pages="$(pdfinfo "$PDF" | awk '/^Pages:/{print $2}')"
    log "PDF: $PDF（${pages} ページ）"
    [ "$pages" -le 4 ] || echo "  注意: 4 ページを超えています。build-pdf.ps1 の font-size を下げると収まります。"
  fi
}

cmd_deploy() {
  [ -f "$HTML" ] || fail "$HTML がありません。先に ./build.sh html を実行してください"
  local stamp; stamp="$(date +%Y%m%d-%H%M%S)"
  log "配置前のバックアップ: index.html.bak.$stamp"
  ssh -o BatchMode=yes "$REMOTE" "cd '$REMOTE_DIR' && cp -p index.html index.html.bak.$stamp && mkdir -p assets"
  log "index.html と assets/ を配置"
  scp -q "$HTML" "$REMOTE:$REMOTE_DIR/index.html"
  if [ -d assets ] && [ -n "$(ls -A assets 2>/dev/null)" ]; then
    scp -q assets/* "$REMOTE:$REMOTE_DIR/assets/"
  fi
  # さくらのログインシェルは csh 系のため、リダイレクトを使う処理は sh -c で実行する
  ssh -o BatchMode=yes "$REMOTE" "sh -c 'cd $REMOTE_DIR && chmod 644 index.html && (chmod 644 assets/* 2>/dev/null || true)'"

  log "公開内容を検証"
  local tmp; tmp="$(mktemp)"
  local code; code="$(curl -s -o "$tmp" -w '%{http_code}' -H 'Cache-Control: no-cache' "$SITE_URL/")"
  [ "$code" = "200" ] || fail "$SITE_URL/ が HTTP $code を返しました"
  cmp -s "$tmp" "$HTML" || fail "公開内容がローカルの $HTML と一致しません"
  rm -f "$tmp"
  for f in assets/*; do
    [ -f "$f" ] || continue
    code="$(curl -s -o /dev/null -w '%{http_code}' "$SITE_URL/$f")"
    [ "$code" = "200" ] || fail "$SITE_URL/$f が HTTP $code を返しました"
  done
  # redact.json の置換前の文字列（本名・社名など）と「生年月日」が残っていないか
  if [ -f "$REDACT" ]; then
    while IFS= read -r word; do
      if grep -qF "$word" "$HTML"; then fail "公開してはいけない文字列が含まれています: $word"; fi
    done < <(python3 -c 'import json,sys; [print(p[0]) for p in json.load(open(sys.argv[1], encoding="utf-8"))["replace"]]' "$REDACT")
  fi
  if grep -q '生年月日' "$HTML"; then fail "生年月日が含まれています"; fi
  log "完了: $SITE_URL/（ローカルと一致、assets も配信中）"
}

case "${1:-}" in
  html)   cmd_html ;;
  pdf)    cmd_pdf ;;
  deploy) cmd_deploy ;;
  all)    cmd_html; cmd_pdf; cmd_deploy ;;
  *)      sed -n '2,9p' "$0" | sed 's/^# \{0,1\}//'; exit 1 ;;
esac

# こんにちは！👋

## 🙋‍♂️ 自己紹介
- 名前: Yuichi Shimo
- 職業: バックエンド寄りのフルスタックエンジニア
- 生息地: 福岡
- 興味: Web 開発 / スクレイピング / オープンソース
- 現在: ボートレース（競艇）の公開 API [Boatrace Open API](https://github.com/boatraceopenapi/api) を中心に、データ取得ライブラリから TypeScript 製のバックテストツール [舟券ラボ](https://github.com/shimomo/funaken-lab) まで、取得・公開・活用の一連を個人で開発中

---

## 💻 スキルセット
![php](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white)
![phpunit](https://img.shields.io/badge/PHPUnit-6C78AF?style=for-the-badge&logo=php&logoColor=white)
![psalm](https://img.shields.io/badge/Psalm-4B5EAA?style=for-the-badge&logo=php&logoColor=white)
![composer](https://img.shields.io/badge/Composer-885630?style=for-the-badge&logo=composer&logoColor=white)
![laravel](https://img.shields.io/badge/Laravel-F55247?style=for-the-badge&logo=laravel&logoColor=white)
![cakephp](https://img.shields.io/badge/CakePHP-999999?style=for-the-badge&logo=cakephp&logoColor=white)
![go](https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white)
![javascript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![typescript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![jest](https://img.shields.io/badge/Jest-C21325?style=for-the-badge&logo=jest&logoColor=white)
![vitest](https://img.shields.io/badge/Vitest-6E9F18?style=for-the-badge&logo=vitest&logoColor=white)
![vue.js](https://img.shields.io/badge/Vue.js-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white)
![react](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white)
![vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-ffd43b?style=for-the-badge&logo=pytest&logoColor=black)
![docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![pages](https://img.shields.io/badge/GitHub_Pages-000000?style=for-the-badge&logo=github&logoColor=white)
![codecov](https://img.shields.io/badge/Codecov-F01F7A?style=for-the-badge&logo=codecov&logoColor=white)
![stripe](https://img.shields.io/badge/Stripe-635BFF?style=for-the-badge&logo=stripe&logoColor=white)

---

## 🚤 ボートレース（競艇）
公式サイトのデータをスクレイパーで取得し、GitHub Actions と GitHub Pages だけで擬似的な API として公開し、そのデータで分析ツールを作る。この一連の流れを個人で回しているプロジェクト群です。組織が分かれているのは役割の違いで、中心は [boatraceopenapi](https://github.com/boatraceopenapi) です。

### 🌐 公開 API
| リポジトリ | 技術スタック |
|---|---|
| [boatraceopenapi/api](https://github.com/boatraceopenapi/api)<br>全 24 場の出走表・直前情報・結果を JSON で公開する API。サーバーを持たず、Cloudflare Workers の Cron Triggers から GitHub Actions を約 3 分間隔で起動して当日分を更新し、GitHub Pages から配信する速度重視版（[エンドポイント](https://boatraceopenapi.github.io/)） | ![php](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white) ![phpunit](https://img.shields.io/badge/PHPUnit-6C78AF?style=for-the-badge&logo=php&logoColor=white) ![psalm](https://img.shields.io/badge/Psalm-4B5EAA?style=for-the-badge&logo=php&logoColor=white) ![actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) ![pages](https://img.shields.io/badge/GitHub_Pages-000000?style=for-the-badge&logo=github&logoColor=white) |
| [turnmark/api](https://github.com/turnmark/api)<br>出走表・直前情報・結果に加えてオッズも提供する API。前日までのデータを扱う安定重視版（[エンドポイント](https://turnmark.github.io/)） | ![php](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white) ![phpunit](https://img.shields.io/badge/PHPUnit-6C78AF?style=for-the-badge&logo=php&logoColor=white) ![psalm](https://img.shields.io/badge/Psalm-4B5EAA?style=for-the-badge&logo=php&logoColor=white) ![actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) ![pages](https://img.shields.io/badge/GitHub_Pages-000000?style=for-the-badge&logo=github&logoColor=white) |

### 📦 ライブラリ
| リポジトリ | 技術スタック |
|---|---|
| [turnmark/turnmark](https://github.com/turnmark/turnmark)<br>上記 2 つの API の土台。公式サイトのスクレイパー `turnmark/scraper` と、福岡・三国・多摩川・徳山の各場公式サイト向けスクレイパーを開発するモノレポ | ![php](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white) ![phpunit](https://img.shields.io/badge/PHPUnit-6C78AF?style=for-the-badge&logo=php&logoColor=white) ![psalm](https://img.shields.io/badge/Psalm-4B5EAA?style=for-the-badge&logo=php&logoColor=white) ![actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) |
| [shimomo/boatrace](https://github.com/shimomo/boatrace)<br>次世代のデータ取得ライブラリ群 `boatrace/*`。契約（`types`）、DI コンテナ（`core`）、汎用モジュール（`support`）、公式サイト（`scraper`）とボートキャスト（`scraper-boatcast`）のスクレイパーを個別パッケージとして Packagist で公開。自分の用途に合わせて turnmark を再設計中 | ![php](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white) ![phpunit](https://img.shields.io/badge/PHPUnit-6C78AF?style=for-the-badge&logo=php&logoColor=white) ![psalm](https://img.shields.io/badge/Psalm-4B5EAA?style=for-the-badge&logo=php&logoColor=white) ![actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) |

### 📊 データ活用
| リポジトリ | 技術スタック |
|---|---|
| [shimomo/funaken-lab](https://github.com/shimomo/funaken-lab)<br>ボートレースの買い方を実際のレース結果で検証するバックテストの実験室。締切後の情報を読むと型エラーになる設計でリークを防ぎ、特払・不成立・返還を分けて払戻表で決済する（[サイト](https://shimomo.github.io/funaken-lab/)） | ![typescript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white) ![react](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black) ![vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white) ![vitest](https://img.shields.io/badge/Vitest-6E9F18?style=for-the-badge&logo=vitest&logoColor=white) ![actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) ![pages](https://img.shields.io/badge/GitHub_Pages-000000?style=for-the-badge&logo=github&logoColor=white) |
| [shimomo/tenjisagi](https://github.com/shimomo/tenjisagi)<br>スタート展示と本番の進入コースの食い違い「展示詐欺」を選手ごとに数値化したランキング（[サイト](https://shimomo.github.io/tenjisagi/)） | ![php](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white) ![actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) ![pages](https://img.shields.io/badge/GitHub_Pages-000000?style=for-the-badge&logo=github&logoColor=white) |

---

## 🏍️ オートレース
| リポジトリ | 技術スタック |
|---|---|
| [Handicapper.jp](https://handicapper.jp/)<br>オートレースの出走表・結果・オッズ・選手情報を日次で収集し、走路条件や試走タイムまで掘り下げた分析画面、2005 年以降・約 12.9 万レースの多条件検索、仮想資金の予想シミュレーターを提供する Web サービス。企画から運用まで一人で担当し、シン VPS で稼働中（コードは非公開） | ![php](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white) ![laravel](https://img.shields.io/badge/Laravel-F55247?style=for-the-badge&logo=laravel&logoColor=white) ![vue.js](https://img.shields.io/badge/Vue.js-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white) ![typescript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white) ![actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) |
| [autorace/tokyo-sports-scraper](https://github.com/autorace/tokyo-sports-scraper)<br>東京スポーツのオートレース情報を取得するスクレイピングライブラリ（PyPI: `autorace-tokyo-sports-scraper`） | ![python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![pytest](https://img.shields.io/badge/pytest-ffd43b?style=for-the-badge&logo=pytest&logoColor=black) ![actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) |
| [shimomo/autorace-news-collector](https://github.com/shimomo/autorace-news-collector)<br>オートレースの最新記事を AUTORACE.JP・日刊スポーツ・各レース場公式サイト・公式 YouTube のフィードと API から集める `shimomo/autorace-news-collector`。HTML の一覧ページはスクレイピングせず、保存・既読管理・重複排除は呼び出し側に委ねる設計 | ![php](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white) ![phpunit](https://img.shields.io/badge/PHPUnit-6C78AF?style=for-the-badge&logo=php&logoColor=white) ![psalm](https://img.shields.io/badge/Psalm-4B5EAA?style=for-the-badge&logo=php&logoColor=white) ![actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) |
| ↳ [shimomo/autorace-news](https://github.com/shimomo/autorace-news)<br>上の autorace-news-collector で 1 時間ごとに集めた見出しを、公式のお知らせ・新聞記事・動画の 3 段に分けて 1 日 1 ページで眺めるサイト。転載を禁じる配信元があるため、公開するのは見出しとリンクだけ（[サイト](https://shimomo.github.io/autorace-news/)） | ![php](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white) ![phpunit](https://img.shields.io/badge/PHPUnit-6C78AF?style=for-the-badge&logo=php&logoColor=white) ![psalm](https://img.shields.io/badge/Psalm-4B5EAA?style=for-the-badge&logo=php&logoColor=white) ![javascript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black) ![actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) ![pages](https://img.shields.io/badge/GitHub_Pages-000000?style=for-the-badge&logo=github&logoColor=white) |

---

## 🚴 競輪
| リポジトリ | 技術スタック |
|---|---|
| [shimomo/keirin-news-collector](https://github.com/shimomo/keirin-news-collector)<br>競輪の最新記事を KEIRIN.JP・新聞各紙・JKA 系サイト・競輪場 31 場の公式サイトのフィードと API から集める `shimomo/keirin-news-collector`。autorace-news-collector と同じ設計で、ソースの絞り込みと取得失敗の分離返却に対応 | ![php](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white) ![phpunit](https://img.shields.io/badge/PHPUnit-6C78AF?style=for-the-badge&logo=php&logoColor=white) ![psalm](https://img.shields.io/badge/Psalm-4B5EAA?style=for-the-badge&logo=php&logoColor=white) ![actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) |
| ↳ [shimomo/keirin-news](https://github.com/shimomo/keirin-news)<br>上の keirin-news-collector で 1 時間ごとに集めた見出しを、新聞・メディア、公式・団体、競輪場のお知らせの 3 段に分けて 1 日 1 ページで眺めるサイト。GitHub Actions の IP を 403 で拒む配信元は RSS に切り替えて読む（[サイト](https://shimomo.github.io/keirin-news/)） | ![php](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white) ![phpunit](https://img.shields.io/badge/PHPUnit-6C78AF?style=for-the-badge&logo=php&logoColor=white) ![psalm](https://img.shields.io/badge/Psalm-4B5EAA?style=for-the-badge&logo=php&logoColor=white) ![javascript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black) ![actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) ![pages](https://img.shields.io/badge/GitHub_Pages-000000?style=for-the-badge&logo=github&logoColor=white) |

---

## 🧰 ツール
| リポジトリ | 技術スタック |
|---|---|
| [shimomo/ses-filter](https://github.com/shimomo/ses-filter)<br>エンジニア求人サイト（paiza転職・Green・doda）の検索結果で、SES・派遣の求人を理由つきで畳む Chrome 拡張機能。保存した検索結果と正解ラベルで適合率・再現率を測りながら判定ルールを調整（[記事](https://zenn.dev/shimomo/articles/9f66a551c41f1a)）| ![typescript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white) ![vitest](https://img.shields.io/badge/Vitest-6E9F18?style=for-the-badge&logo=vitest&logoColor=white) |
| [shimomo/tech-trends](https://github.com/shimomo/tech-trends)<br>GitHub Trending と Zenn から、Web 系・AI 系で反応が多かったものを毎朝集めて 1 ページにまとめるサイト。前日の記録と比べて、急上昇と初登場に印を付ける（[サイト](https://shimomo.github.io/tech-trends/)） | ![typescript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white) ![vitest](https://img.shields.io/badge/Vitest-6E9F18?style=for-the-badge&logo=vitest&logoColor=white) ![actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) ![pages](https://img.shields.io/badge/GitHub_Pages-000000?style=for-the-badge&logo=github&logoColor=white) |
| [shimomo/narikiri](https://github.com/shimomo/narikiri)<br>ngrok の起動ごとに変わる URL を Stripe の Webhook エンドポイントへ同期する CLI（Homebrew 対応） | ![go](https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white) ![stripe](https://img.shields.io/badge/Stripe-635BFF?style=for-the-badge&logo=stripe&logoColor=white) |

---

## 🧪 検証と記事
新しい機能やツールの挙動を手元の再現環境で確かめ、ログをもとに記事にしたものです。

| リポジトリ | 技術スタック |
|---|---|
| [shimomo/lab-php86-clamp](https://github.com/shimomo/lab-php86-clamp)<br>PHP 8.6 で追加される `clamp()` を、公式 Docker イメージの 8.6.0RC2 で確かめた検証環境。型変換をしないことや、空配列で `ValueError` になるなど `max(min())` から置き換えると変わる点、自前の `clamp()` がある場合の影響、polyfill との差を記録（[記事](https://zenn.dev/shimomo/articles/8499e432bac303)） | ![php](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white) ![docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) |
| [shimomo/lab-laravel-vet](https://github.com/shimomo/lab-laravel-vet)<br>Composer の依存の更新を差分と AI エージェントで審査する [laravel/vet](https://github.com/laravel/vet)（v0.2.1）を、手元で配る架空の悪性パッケージで確かめた検証環境。autoload の外だけを変えた版はエージェントに中身が渡らず `PASS` になるなど、止めるものと止めないものを記録（[記事](https://zenn.dev/shimomo/articles/299809443d5505)） | ![php](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white) ![composer](https://img.shields.io/badge/Composer-885630?style=for-the-badge&logo=composer&logoColor=white) ![python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) |

---

## 🏢 所属組織
| 組織 | 役割 |
|---|---|
| [boatraceopenapi](https://github.com/boatraceopenapi) | ボートレースのデータを公開 API 化する本体。活動の中心 |
| [turnmark](https://github.com/turnmark) | 公開 API の土台となるスクレイパー群と、安定重視の API |
| [boatracevibeproject](https://github.com/boatracevibeproject) | ノリと勢いで開発する実験場。試作や小さなライブラリの置き場 |
| [autorace](https://github.com/autorace) | オートレース関連のスクレイピングと分析 |

---

## 📫 連絡先
- Web: [shimomo.net](https://shimomo.net/)
- Email: github@shimomo.net
- Bluesky: [@shimomo.net](https://bsky.app/profile/shimomo.net)

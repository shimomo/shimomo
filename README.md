# Hi there! 👋

**English** | [日本語](README.ja.md)

## 🙋‍♂️ About Me
- Name: Yuichi Shimo
- Role: Full-stack engineer with a backend focus
- Based in: Fukuoka, Japan
- Interests: Web development / Web scraping / Open source
- Currently: Building the whole pipeline for boatrace (Japanese powerboat racing) data on my own: collecting it, publishing it and putting it to use. The center is [Boatrace Open API](https://github.com/boatraceopenapi/api), a public API, and the work runs from scraping libraries to [Funaken Lab](https://github.com/shimomo/funaken-lab), a backtesting tool written in TypeScript

---

## 💻 Skills
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

## 🚤 Boatrace
Projects that scrape data from the official boatrace site, publish it as a pseudo-API using only GitHub Actions and GitHub Pages, and build analysis tools on top of that data, all run by one person. The organizations are split by role, and the main one is [boatraceopenapi](https://github.com/boatraceopenapi).

### 🌐 Public APIs
| Repository | Tech Stack |
|---|---|
| [boatraceopenapi/api](https://github.com/boatraceopenapi/api)<br>An API that publishes race cards, pre-race info and results for all 24 stadiums as JSON. It has no server: Cloudflare Workers Cron Triggers start GitHub Actions about every 3 minutes to update the day's data, and GitHub Pages serves it. This is the speed-first version ([endpoint](https://boatraceopenapi.github.io/)) | ![php](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white) ![phpunit](https://img.shields.io/badge/PHPUnit-6C78AF?style=for-the-badge&logo=php&logoColor=white) ![psalm](https://img.shields.io/badge/Psalm-4B5EAA?style=for-the-badge&logo=php&logoColor=white) ![actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) ![pages](https://img.shields.io/badge/GitHub_Pages-000000?style=for-the-badge&logo=github&logoColor=white) |
| [turnmark/api](https://github.com/turnmark/api)<br>An API that also provides odds, on top of race cards, pre-race info and results. This is the stability-first version, covering data up to the previous day ([endpoint](https://turnmark.github.io/)) | ![php](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white) ![phpunit](https://img.shields.io/badge/PHPUnit-6C78AF?style=for-the-badge&logo=php&logoColor=white) ![psalm](https://img.shields.io/badge/Psalm-4B5EAA?style=for-the-badge&logo=php&logoColor=white) ![actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) ![pages](https://img.shields.io/badge/GitHub_Pages-000000?style=for-the-badge&logo=github&logoColor=white) |

### 📦 Libraries
| Repository | Tech Stack |
|---|---|
| [turnmark/turnmark](https://github.com/turnmark/turnmark)<br>The foundation of the two APIs above. A monorepo for `turnmark/scraper`, a scraper for the official site, and scrapers for the official sites of the Fukuoka, Mikuni, Tamagawa and Tokuyama stadiums | ![php](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white) ![phpunit](https://img.shields.io/badge/PHPUnit-6C78AF?style=for-the-badge&logo=php&logoColor=white) ![psalm](https://img.shields.io/badge/Psalm-4B5EAA?style=for-the-badge&logo=php&logoColor=white) ![actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) |
| [shimomo/boatrace-php](https://github.com/shimomo/boatrace-php)<br>`boatrace/*`, the next generation of my data libraries. Contracts (`types`), the DI container (`core`), general-purpose modules (`support`), and scrapers for the official site (`scraper`) and BOATCAST (`scraper-boatcast`) are published as separate Packagist packages. A redesign of turnmark for my own use cases, in progress | ![php](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white) ![phpunit](https://img.shields.io/badge/PHPUnit-6C78AF?style=for-the-badge&logo=php&logoColor=white) ![psalm](https://img.shields.io/badge/Psalm-4B5EAA?style=for-the-badge&logo=php&logoColor=white) ![actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) |

### 📊 Using the Data
| Repository | Tech Stack |
|---|---|
| [shimomo/funaken-lab](https://github.com/shimomo/funaken-lab)<br>A backtesting lab that tests boatrace betting strategies against real race results. Reading information from after the betting deadline is a type error by design, which prevents leakage, and bets are settled from the payout table, with special payouts, unestablished bets and refunds counted separately ([site](https://shimomo.github.io/funaken-lab/)) | ![typescript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white) ![react](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black) ![vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white) ![vitest](https://img.shields.io/badge/Vitest-6E9F18?style=for-the-badge&logo=vitest&logoColor=white) ![actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) ![pages](https://img.shields.io/badge/GitHub_Pages-000000?style=for-the-badge&logo=github&logoColor=white) |
| [shimomo/tenjisagi](https://github.com/shimomo/tenjisagi)<br>A per-racer ranking of how often the course taken in the start exhibition differs from the course in the actual race, known among fans as "tenji sagi" (exhibition fraud) ([site](https://shimomo.github.io/tenjisagi/)) | ![php](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white) ![actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) ![pages](https://img.shields.io/badge/GitHub_Pages-000000?style=for-the-badge&logo=github&logoColor=white) |
| [shimomo/boatrace-motivation-viz](https://github.com/shimomo/boatrace-motivation-viz)<br>A web app that visualizes racers' motivation and condition from the weight changes on race cards. It reads data from [boatraceopenapi/api](https://github.com/boatraceopenapi/api), is exported as a static site and is served from GitHub Pages ([site](https://shimomo.github.io/boatrace-motivation-viz/)) | ![typescript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white) ![next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white) ![react](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black) ![jest](https://img.shields.io/badge/Jest-C21325?style=for-the-badge&logo=jest&logoColor=white) ![codecov](https://img.shields.io/badge/Codecov-F01F7A?style=for-the-badge&logo=codecov&logoColor=white) ![actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) ![pages](https://img.shields.io/badge/GitHub_Pages-000000?style=for-the-badge&logo=github&logoColor=white) |
| [shimomo/boatrace-replay-links](https://github.com/shimomo/boatrace-replay-links)<br>A page that builds links to BOATCAST race replays (from 2020-01-01) from a date, stadium and race number. It doesn't embed the video and only opens the replay page. Replay URLs are added every morning as static JSON, one file per day, and are also published as an API ([site](https://shimomo.github.io/boatrace-replay-links/)) | ![javascript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black) ![actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) ![pages](https://img.shields.io/badge/GitHub_Pages-000000?style=for-the-badge&logo=github&logoColor=white) |

---

## 🏍️ Autorace
| Repository | Tech Stack |
|---|---|
| [Handicapper.jp](https://handicapper.jp/)<br>A web service that collects autorace race cards, results, odds and racer data daily. It offers analysis screens that go down to track conditions and trial run times, multi-criteria search over about 129,000 races since 2005, and a prediction simulator with virtual money. I handle everything from planning to operations on my own, and it runs on a Shin VPS (the code is private) | ![php](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white) ![laravel](https://img.shields.io/badge/Laravel-F55247?style=for-the-badge&logo=laravel&logoColor=white) ![vue.js](https://img.shields.io/badge/Vue.js-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white) ![typescript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white) ![actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) |
| [autorace/tokyo-sports-scraper](https://github.com/autorace/tokyo-sports-scraper)<br>A scraping library for autorace information from Tokyo Sports (PyPI: `autorace-tokyo-sports-scraper`) | ![python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![pytest](https://img.shields.io/badge/pytest-ffd43b?style=for-the-badge&logo=pytest&logoColor=black) ![actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) |
| [shimomo/autorace-news-collector](https://github.com/shimomo/autorace-news-collector)<br>`shimomo/autorace-news-collector` collects the latest autorace articles from the feeds and APIs of AUTORACE.JP, Nikkan Sports, each stadium's official site and the official YouTube channel. It doesn't scrape HTML list pages, and leaves storage, read tracking and deduplication to the caller | ![php](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white) ![phpunit](https://img.shields.io/badge/PHPUnit-6C78AF?style=for-the-badge&logo=php&logoColor=white) ![psalm](https://img.shields.io/badge/Psalm-4B5EAA?style=for-the-badge&logo=php&logoColor=white) ![actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) |
| ↳ [shimomo/autorace-news](https://github.com/shimomo/autorace-news)<br>A site for browsing the headlines collected by autorace-news-collector above, one page per week, in three rows: official announcements, newspaper articles and videos. Some sources forbid republishing, so it only publishes headlines and links ([site](https://shimomo.github.io/autorace-news/)) | ![php](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white) ![phpunit](https://img.shields.io/badge/PHPUnit-6C78AF?style=for-the-badge&logo=php&logoColor=white) ![psalm](https://img.shields.io/badge/Psalm-4B5EAA?style=for-the-badge&logo=php&logoColor=white) ![javascript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black) ![actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) ![pages](https://img.shields.io/badge/GitHub_Pages-000000?style=for-the-badge&logo=github&logoColor=white) |

---

## 🚴 Keirin
| Repository | Tech Stack |
|---|---|
| [shimomo/keirin-news-collector](https://github.com/shimomo/keirin-news-collector)<br>`shimomo/keirin-news-collector` collects the latest keirin articles from the feeds and APIs of KEIRIN.JP, newspapers, JKA-related sites and the official sites of 31 velodromes. It shares its design with autorace-news-collector, and supports filtering by source and returning fetch failures separately | ![php](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white) ![phpunit](https://img.shields.io/badge/PHPUnit-6C78AF?style=for-the-badge&logo=php&logoColor=white) ![psalm](https://img.shields.io/badge/Psalm-4B5EAA?style=for-the-badge&logo=php&logoColor=white) ![actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) |
| ↳ [shimomo/keirin-news](https://github.com/shimomo/keirin-news)<br>A site for browsing the headlines collected by keirin-news-collector above, mostly racer news, one page per day, in three rows: newspapers and media, official bodies, and velodrome announcements. Sources that block GitHub Actions IPs with 403 are read through RSS instead ([site](https://shimomo.github.io/keirin-news/)) | ![php](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white) ![phpunit](https://img.shields.io/badge/PHPUnit-6C78AF?style=for-the-badge&logo=php&logoColor=white) ![psalm](https://img.shields.io/badge/Psalm-4B5EAA?style=for-the-badge&logo=php&logoColor=white) ![javascript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black) ![actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) ![pages](https://img.shields.io/badge/GitHub_Pages-000000?style=for-the-badge&logo=github&logoColor=white) |
| [shimomo/winticket-keirin-columns](https://github.com/shimomo/winticket-keirin-columns)<br>An unofficial Chrome extension for reordering and hiding columns in WINTICKET's keirin race cards. It can move the "memo" column, which tends to be hidden off to the right, next to the racer names. It only rearranges the table already on the page and sends no extra requests | ![javascript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black) |

---

## 🧰 Tools
| Repository | Tech Stack |
|---|---|
| [shimomo/ses-filter](https://github.com/shimomo/ses-filter)<br>A Chrome extension that collapses SES (contract staffing) and dispatch jobs, with the reason shown, in the search results of Japanese engineering job sites (paiza, Green, doda, Mynavi Tenshoku, Rikunabi NEXT). The rules are tuned by measuring precision and recall against saved search results and their correct labels ([store](https://chromewebstore.google.com/detail/pkbihcihgnknmeelpaoaoghggggjehpa) / [article](https://zenn.dev/shimomo/articles/9f66a551c41f1a?locale=en)) | ![typescript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white) ![vitest](https://img.shields.io/badge/Vitest-6E9F18?style=for-the-badge&logo=vitest&logoColor=white) |
| [shimomo/tech-trends](https://github.com/shimomo/tech-trends)<br>A site that gathers the most popular web and AI items from GitHub Trending and Zenn every morning and puts them on one page. Compared with the previous day's record, it marks items that are rising fast or appearing for the first time ([site](https://shimomo.github.io/tech-trends/)) | ![typescript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white) ![vitest](https://img.shields.io/badge/Vitest-6E9F18?style=for-the-badge&logo=vitest&logoColor=white) ![actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) ![pages](https://img.shields.io/badge/GitHub_Pages-000000?style=for-the-badge&logo=github&logoColor=white) |
| [shimomo/lapras-portfolio](https://github.com/shimomo/lapras-portfolio)<br>A setup that publishes a terminal-style portfolio page to GitHub Pages every morning from the public [LAPRAS](https://lapras.com/) API. Fork it and change the ID in `config.json` to use it, and pick up my fixes with Sync fork ([site](https://shimomo.github.io/lapras-portfolio/)) | ![typescript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white) ![vitest](https://img.shields.io/badge/Vitest-6E9F18?style=for-the-badge&logo=vitest&logoColor=white) ![actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) ![pages](https://img.shields.io/badge/GitHub_Pages-000000?style=for-the-badge&logo=github&logoColor=white) |
| [shimomo/quadview](https://github.com/shimomo/quadview)<br>A tool for watching up to four YouTube videos or live streams side by side on one screen. Swapping slots doesn't stop the other videos, and with presets (JSON) and your own YouTube Data API key, it finds today's streams on a channel and fills the slots ([site](https://shimomo.github.io/quadview/)) | ![javascript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black) ![actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) ![pages](https://img.shields.io/badge/GitHub_Pages-000000?style=for-the-badge&logo=github&logoColor=white) |
| [shimomo/narikiri](https://github.com/shimomo/narikiri)<br>A CLI that syncs the ngrok URL, which changes every time ngrok starts, to a Stripe webhook endpoint (available through Homebrew) | ![go](https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white) ![stripe](https://img.shields.io/badge/Stripe-635BFF?style=for-the-badge&logo=stripe&logoColor=white) |

---

## 🧪 Experiments and Articles
I check how new features and tools behave in reproducible local environments, then write articles from the logs. The articles are written in Japanese on Zenn, and the links open Zenn's AI-translated English version.

| Repository | Tech Stack |
|---|---|
| [shimomo/lab-php86-clamp](https://github.com/shimomo/lab-php86-clamp)<br>A test environment for `clamp()`, new in PHP 8.6, checked with the official 8.6.0RC2 Docker image. It records what changes when replacing `max(min())`, such as no type juggling and a `ValueError` on empty arrays, how existing user-defined `clamp()` functions are affected, and how it differs from the polyfill ([article](https://zenn.dev/shimomo/articles/8499e432bac303?locale=en)) | ![php](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white) ![docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) |
| [shimomo/lab-laravel-vet](https://github.com/shimomo/lab-laravel-vet)<br>A test environment for [laravel/vet](https://github.com/laravel/vet) (v0.2.1), which reviews Composer dependency updates using the diff and an AI agent, checked with a fake malicious package served locally. It records what it stops and what it doesn't, such as a version that only changes files outside autoload passing with `PASS` because their contents never reach the agent ([article](https://zenn.dev/shimomo/articles/299809443d5505?locale=en)) | ![php](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white) ![composer](https://img.shields.io/badge/Composer-885630?style=for-the-badge&logo=composer&logoColor=white) ![python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) |

---

## 🏢 Organizations
| Organization | Role |
|---|---|
| [boatraceopenapi](https://github.com/boatraceopenapi) | The core project that turns boatrace data into a public API. Most of my work happens here |
| [turnmark](https://github.com/turnmark) | The scrapers behind the public APIs, and the stability-first API |
| [boatracevibeproject](https://github.com/boatracevibeproject) | A playground built on vibes and momentum, for prototypes and small libraries |
| [autorace](https://github.com/autorace) | Scraping and analysis for autorace |

---

## 📫 Contact
- Web: [shimomo.net](https://shimomo.net/)
- Email: github@shimomo.net
- Bluesky: [@shimomo.net](https://bsky.app/profile/shimomo.net)

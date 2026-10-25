---
layout: single
author_profile: true
title: "BMForge"
lang: uk
locale: uk
language_name: Українська
translation_key: bmforge-home
permalink: /uk/
---

![Логотип BMForge](/pages/images/bmforge.png)

# BMForge

**Створюй просте. Не приховуй збоїв. Відповідай за реалізацію.**

BMForge — це інженерний контракт для агентів, які пишуть код. Він визначає, як створювати, тестувати, випускати й інтегрувати застосунки з локальним середовищем. Це **не спільна бібліотека виконання**: кожен застосунок володіє власним кодом. Окремі застосунки взаємодіють лише через задокументовані публічні API.

BMForge — ще один продукт бренду [Bear & Moose](https://osoyalce.com).

## Інженерний контракт

Перед початком реалізації прочитайте [інженерний контракт (англійською)]({{ site.baseurl }}{% link uk/pages/engineering-contract.md %}).

- **Мінімалізм за замовчуванням:** реалізуйте лише необхідне. Кожна абстракція, служба, повторна спроба й резервний механізм мають бути обґрунтовані.
- **Довіра до контрактів:** перевіряйте дані на зовнішніх межах; не дублюйте перевірки довірених внутрішніх даних на кожному рівні.
- **Помітні збої:** порушення внутрішніх припущень, недоступність обов’язкових ресурсів і невдалі операції не повинні виглядати як успіх.
- **Чіткі межі розподілених систем:** явні підтвердження й тайм-аути там, де важлива доставка; жодної вигаданої архітектури відмовостійкості.
- **Перевірка поведінки:** тестуйте визначені контракти компонентів і суттєві сценарії збоїв, а не уявні вимоги.
- **Перевірка стану:** запущені застосунки надають просту перевірку працездатності за запитом.

## Початок роботи

| Завдання Codex | З чого почати (документація англійською) |
| --- | --- |
| Створення застосунку | Кореневий `AGENTS.md`, [інженерний контракт]({{ site.baseurl }}{% link uk/pages/engineering-contract.md %}), [класифікація класів]({{ site.baseurl }}{% link uk/pages/classification.md %}), а потім вибрані [специфікації компонентів]({{ site.baseurl }}{% link pages/component-blueprints.md %}) |
| Початкове налаштування порожнього проєкту з навичками Codex | [Установлення закріплених навичок компонентів Codex]({{ site.baseurl }}{% link pages/codex-skills.md %}) |
| Реалізація або вдосконалення компонента | [Специфікації компонентів]({{ site.baseurl }}{% link pages/component-blueprints.md %}) і [життєвий цикл специфікацій]({{ site.baseurl }}{% link uk/pages/specification-lifecycle.md %}) |
| Створення DAL або класифікація коду | [Activity / Interface / Entity]({{ site.baseurl }}{% link uk/pages/classification.md %}) і [DB Server]({{ site.baseurl }}{% link pages/component-db-server.md %}) |
| Централізація констант | [Стандарт констант]({{ site.baseurl }}{% link pages/component-constants.md %}) |
| Локалізація інтерфейсів | [Локалізація застосунків]({{ site.baseurl }}{% link pages/component-localization.md %}) |
| Вибір графіків, карт і графів зв’язків | [Схвалені візуалізації]({{ site.baseurl }}{% link pages/component-visualization.md %}) |
| Експорт кадрів до анімованого GIF | [GIF-анімація]({{ site.baseurl }}{% link pages/component-gif-animation.md %}) |
| Налаштування служби | [Конфігурація виконання]({{ site.baseurl }}{% link pages/runtime-configuration.md %}) і [мережева конфігурація]({{ site.baseurl }}{% link pages/network-configuration.md %}) |
| Інтеграція з CMDB | [Відповідність CMDB]({{ site.baseurl }}{% link pages/cmdb-compliance.md %}) |
| Моніторинг стану застосунку | [Перевірки працездатності]({{ site.baseurl }}{% link pages/health-checks.md %}) |
| Установлення, оновлення або видалення | [Контракт життєвого циклу встановлення]({{ site.baseurl }}{% link pages/component-installation.md %}), [скрипти встановлення]({{ site.baseurl }}{% link pages/installation-scripts.md %}) і [відстеження змін розгортання]({{ site.baseurl }}{% link pages/deployment-impact-tracking.md %}) |
| Публікація випуску | [Налаштування випусків]({{ site.baseurl }}{% link pages/release-setup.md %}), [створення випуску]({{ site.baseurl }}{% link pages/creating-a-release.md %}), [журнал змін]({{ site.baseurl }}{% link pages/changelog-maintenance.md %}) |
| Публікація документації | [Налаштування Jekyll]({{ site.baseurl }}{% link pages/jekyll-setup.md %}), [GitHub Pages]({{ site.baseurl }}{% link pages/github-pages-publishing.md %}), [багатомовна документація]({{ site.baseurl }}{% link pages/multilingual-documentation.md %}) |

## Пакування навичок Codex

Почніть із [навички початкового налаштування проєкту]({{ site.baseurl }}{% link pages/codex-skills.md %}), щоб установити закріплені навички **проєкту, констант, локалізації та встановлення**, а також лише ті додаткові компоненти, які запросив користувач, у `.agents/skills/` нового застосунку. Проєкт отримує власний `AGENTS.md` та **сповіщення про оновлення лише для читання**, без автоматичних оновлень чи генерації застосунків.

## Специфікації компонентів

Кожен контракт визначає поведінку, **фіксований перелік схвалених модулів виконання** та приймальні перевірки. Codex адаптує **зафіксований локальний еталонний код**, а не вибирає інші фреймворки. Якщо визначених модулів недостатньо, Codex має зупинитися й отримати схвалення до зміни специфікації.

| Компонент | Стабільний ідентифікатор | Контракт (англійською) |
| --- | --- | --- |
| HTTP-сервер відображення | `bmforge.http-server` | [HTTP]({{ site.baseurl }}{% link pages/component-http.md %}) |
| ZeroMQ REQ/REP | `bmforge.zmq-server` | [ZeroMQ]({{ site.baseurl }}{% link pages/component-zmq.md %}) |
| Сервер бази даних | `bmforge.db-server` | [Канонічний DbMgr і рівні DAL]({{ site.baseurl }}{% link pages/component-db-server.md %}) |
| Git | `bmforge.git` | [Публікація й коміти]({{ site.baseurl }}{% link pages/component-git.md %}) |
| Візуалізації | `bmforge.visualization` | [Plotly.js, Leaflet, Cytoscape.js]({{ site.baseurl }}{% link pages/component-visualization.md %}) |
| GIF-анімація | `bmforge.gif-animation` | [Кодувальник GIF-кадрів Pillow]({{ site.baseurl }}{% link pages/component-gif-animation.md %}) |
| Константи | `bmforge.constants` | [Фіксовані значення за доменами]({{ site.baseurl }}{% link pages/component-constants.md %}) |
| Локалізація застосунків | `bmforge.localization` | [Англійський каталог і багатомовний інтерфейс]({{ site.baseurl }}{% link pages/component-localization.md %}) |
| Життєвий цикл встановлення | `bmforge.installation` | [Установлення, оновлення, видалення та ролі клієнта/сервера]({{ site.baseurl }}{% link pages/component-installation.md %}) |

## Простежуваність і вдосконалення

Модулі реалізації містять невеликий ідентифікатор компонента та версію специфікації, які можна прочитати статичним аналізом. [Життєвий цикл специфікацій]({{ site.baseurl }}{% link uk/pages/specification-lifecycle.md %}) визначає, як виявляти прогалини, вдосконалювати контракт, додавати регресійні перевірки й версіонувати зміни. [Журнал рішень]({{ site.baseurl }}{% link DECISIONS.md %}) фіксує ухвалені рішення та незавершену роботу.

**Поточний стан:** контракти HTTP, ZeroMQ, DB Server, Git та необов’язкових візуалізацій, канонічні шаблони DB/Git і закріплені локальні приклади є чернетками, що очікують перевірки в застосунках-споживачах. Варіанти візуалізацій ґрунтуються на зафіксованому коді MyCount і CMDB; GIF-анімація також має канонічний кодувальник Pillow та зафіксований приклад Snake Web. Пакування навичок Codex реалізовано; перевірка в реальних застосунках і сканування тегів компонентів у CMDB залишаються майбутньою роботою. Наявні декларації CMDB для файлів, баз даних і мережевих слухачів залишаються окремими від відстеження архітектурних компонентів.

---

[Журнал змін (англійською)]({{ site.baseurl }}{% link CHANGELOG.md %}) · [Репозиторій BMForge](https://github.com/NadimGhaznavi/bmforge)

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


**Створюй просте. Не приховуй збоїв. Відповідай за реалізацію.**

BMForge — це інженерний контракт для агентів, які пишуть код. Він визначає, як створювати, тестувати, випускати й інтегрувати застосунки з локальним середовищем. Це **не спільна бібліотека виконання**: кожен застосунок володіє власним кодом. Окремі застосунки взаємодіють лише через задокументовані публічні API.

BMForge — ще один продукт бренду [Bear & Moose](https://osoyalce.com).

## Початок роботи з Codex

Один раз установіть навичку **`bmforge`** у чаті Codex:

```text
$skill-installer install https://github.com/NadimGhaznavi/bmforge/tree/main/skills/bmforge
```

Потім відкрийте Codex у новому репозиторії Git і викличте `$bmforge`. Codex пояснить доступні навички, допоможе вибрати потрібні компоненти й установить їхні закріплені локальні копії. Дивіться [коротку інструкцію українською]({{ site.baseurl }}{% link uk/pages/codex-skills.md %}).

## Інженерний підхід

**Англійська є авторитетною мовою технічних контрактів і навичок для AI-агентів.** Українська версія пояснює BMForge людям, а посилання нижче ведуть до актуальних англомовних специфікацій.

Перед початком реалізації прочитайте [інженерний контракт]({{ site.baseurl }}{% link pages/engineering-contract.md %}).

- **Мінімалізм за замовчуванням:** реалізуйте лише необхідне. Кожна абстракція, служба, повторна спроба й резервний механізм мають бути обґрунтовані.
- **Довіра до контрактів:** перевіряйте дані на зовнішніх межах; не дублюйте перевірки довірених внутрішніх даних на кожному рівні.
- **Помітні збої:** порушення внутрішніх припущень, недоступність обов’язкових ресурсів і невдалі операції не повинні виглядати як успіх.
- **Чіткі межі розподілених систем:** явні підтвердження й тайм-аути там, де важлива доставка; жодної вигаданої архітектури відмовостійкості.
- **Перевірка поведінки:** тестуйте визначені контракти компонентів і суттєві сценарії збоїв, а не уявні вимоги.
- **Перевірка стану:** запущені застосунки надають просту перевірку працездатності за запитом.

## Технічна документація (англійською)

| Завдання Codex | З чого почати |
| --- | --- |
| Створення застосунку | Кореневий `AGENTS.md`, [інженерний контракт]({{ site.baseurl }}{% link pages/engineering-contract.md %}), [класифікація класів]({{ site.baseurl }}{% link pages/classification.md %}), а потім вибрані [специфікації компонентів]({{ site.baseurl }}{% link pages/component-blueprints.md %}) |
| Початок нового проєкту в Codex | [Використання BMForge з Codex]({{ site.baseurl }}{% link uk/pages/codex-skills.md %}) |
| Реалізація або вдосконалення компонента | [Специфікації компонентів]({{ site.baseurl }}{% link pages/component-blueprints.md %}) і [життєвий цикл специфікацій]({{ site.baseurl }}{% link pages/specification-lifecycle.md %}) |
| Створення DAL або класифікація коду | [Activity / Interface / Entity]({{ site.baseurl }}{% link pages/classification.md %}) і [DB Server]({{ site.baseurl }}{% link pages/component-db-server.md %}) |
| Централізація констант | [Стандарт констант]({{ site.baseurl }}{% link pages/component-constants.md %}) |
| Локалізація інтерфейсів | [Локалізація застосунків]({{ site.baseurl }}{% link pages/component-localization.md %}) |
| Вибір графіків, карт і графів зв’язків | [Схвалені візуалізації]({{ site.baseurl }}{% link pages/component-visualization.md %}) |
| Експорт кадрів до анімованого GIF | [GIF-анімація]({{ site.baseurl }}{% link pages/component-gif-animation.md %}) |
| Налаштування служби | [Конфігурація виконання]({{ site.baseurl }}{% link pages/runtime-configuration.md %}) і [мережева конфігурація]({{ site.baseurl }}{% link pages/network-configuration.md %}) |
| Інтеграція з CMDB | [Відповідність CMDB]({{ site.baseurl }}{% link pages/cmdb-compliance.md %}) |
| Моніторинг стану застосунку | [Перевірки працездатності]({{ site.baseurl }}{% link pages/health-checks.md %}) |
| Аналіз збоїв у production | [Навичка RCA](https://github.com/NadimGhaznavi/bmforge/blob/main/skills/bmforge-rca/SKILL.md): збір даних без змін на сервері, відтворення та налагодження локально |
| Установлення, оновлення або видалення | [Контракт життєвого циклу встановлення]({{ site.baseurl }}{% link pages/component-installation.md %}), [скрипти встановлення]({{ site.baseurl }}{% link pages/installation-scripts.md %}) і [відстеження змін розгортання]({{ site.baseurl }}{% link pages/deployment-impact-tracking.md %}) |
| Публікація випуску | [Налаштування випусків]({{ site.baseurl }}{% link pages/release-setup.md %}), [створення випуску]({{ site.baseurl }}{% link pages/creating-a-release.md %}), [журнал змін]({{ site.baseurl }}{% link pages/changelog-maintenance.md %}) |
| Публікація документації | [Налаштування Jekyll]({{ site.baseurl }}{% link pages/jekyll-setup.md %}), [GitHub Pages]({{ site.baseurl }}{% link pages/github-pages-publishing.md %}), [багатомовна документація]({{ site.baseurl }}{% link pages/multilingual-documentation.md %}) |

## Довідник компонентів (англійською)

Кожен контракт визначає поведінку, **фіксований перелік схвалених модулів виконання** та приймальні перевірки. Codex адаптує **зафіксований локальний еталонний код**, а не вибирає інші фреймворки. Якщо визначених модулів недостатньо, Codex має зупинитися й отримати схвалення до зміни специфікації.

| Компонент | Стабільний ідентифікатор | Контракт |
| --- | --- | --- |
| HTTP-сервер відображення | `bmforge.http-server` | [HTTP]({{ site.baseurl }}{% link pages/component-http.md %}) |
| ZeroMQ REQ/REP | `bmforge.zmq-server` | [ZeroMQ]({{ site.baseurl }}{% link pages/component-zmq.md %}) |
| Тимчасове блокування IP на хості | `bmforge.nftables` | [Набори nftables зі строком дії]({{ site.baseurl }}{% link pages/component-nftables.md %}) |
| Виявлення подій у журналах безпеки | `bmforge.fail2ban` | [Fail2ban і локальний клієнт дії (потребує ZMQ)]({{ site.baseurl }}{% link pages/component-fail2ban.md %}) |
| Сервер бази даних | `bmforge.db-server` | [Канонічний DbMgr і рівні DAL]({{ site.baseurl }}{% link pages/component-db-server.md %}) |
| Git | `bmforge.git` | [Публікація й коміти]({{ site.baseurl }}{% link pages/component-git.md %}) |
| Візуалізації | `bmforge.visualization` | [Plotly.js, Leaflet, Cytoscape.js]({{ site.baseurl }}{% link pages/component-visualization.md %}) |
| Редагування часових шкал | `bmforge.timeline` | [vis-timeline (потребує HTTP)]({{ site.baseurl }}{% link pages/component-timeline.md %}) |
| GIF-анімація | `bmforge.gif-animation` | [Кодувальник GIF-кадрів Pillow]({{ site.baseurl }}{% link pages/component-gif-animation.md %}) |
| Константи | `bmforge.constants` | [Фіксовані значення за доменами]({{ site.baseurl }}{% link pages/component-constants.md %}) |
| Локалізація застосунків | `bmforge.localization` | [Англійський каталог і багатомовний інтерфейс]({{ site.baseurl }}{% link pages/component-localization.md %}) |
| Життєвий цикл встановлення | `bmforge.installation` | [Установлення, оновлення, видалення та ролі клієнта/сервера]({{ site.baseurl }}{% link pages/component-installation.md %}) |

## Простежуваність і вдосконалення

Модулі реалізації містять невеликий ідентифікатор компонента та версію специфікації, які можна прочитати статичним аналізом. [Життєвий цикл специфікацій]({{ site.baseurl }}{% link pages/specification-lifecycle.md %}) визначає, як виявляти прогалини, вдосконалювати контракт, додавати регресійні перевірки й версіонувати зміни. [Журнал рішень]({{ site.baseurl }}{% link DECISIONS.md %}) фіксує ухвалені рішення та незавершену роботу.

**Поточний стан:** Закріплені навички Codex, шаблони випусків і перевірки оновлень у режимі лише читання вже реалізовано, зокрема додаткові навички GIF-анімації та аналізу причин збоїв (RCA). Контракти компонентів і еталонні реалізації ще перевіряються в реальних застосунках. Сканування версій компонентів у CMDB залишається запланованим.

---

[Журнал змін (англійською)]({{ site.baseurl }}{% link CHANGELOG.md %}) · [Репозиторій BMForge](https://github.com/NadimGhaznavi/bmforge)



---
title: "Публікація на GitHub Pages"
lang: uk
locale: uk
language_name: Українська
translation_key: bmforge-github-pages-publishing
permalink: /uk/pages/github-pages-publishing/
---

Публікуйте Jekyll-сайт документації проєкту з гілки `main` за допомогою GitHub Actions. Спочатку підготуйте файли сайту за [Налаштуванням Jekyll]({{ site.baseurl }}{% link uk/pages/jekyll-setup.md %}).

## Додавання процесу публікації

Скопіюйте [шаблон workflow]({{ '/templates/jekyll-gh-pages.yml' | relative_url }}) до `.github/workflows/jekyll-gh-pages.yml`. Він збирає сайт із кореня репозиторію й розгортає його після надсилання змін до `main`; можливий також ручний запуск. Гілки розробки та функцій не публікують сайт.

У **Settings → Pages** репозиторію виберіть **GitHub Actions** як джерело публікації. Workflow містить необхідні дозволи, завантаження артефакту та середовище розгортання `github-pages`. Дивіться [документацію GitHub щодо власних workflow](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

## Налаштування домену

Для власного піддомену:

1. Укажіть назву хоста в налаштуваннях Pages репозиторію.
2. Налаштуйте DNS-запис `CNAME`, який спрямовує цю назву на `<github-owner>.github.io` без шляху до репозиторію.
3. Увімкніть **Enforce HTTPS**, коли це стане доступним.
4. Додайте в корінь файл `CNAME`, що містить лише назву хоста, згідно з домовленостями наявних проєктів.

Файл `CNAME` зберігає назву хоста; публікація через GitHub Actions використовує домен, налаштований у Pages. Дивіться [інструкції GitHub щодо власного домену](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site). Для стандартної адреси GitHub Pages пропустіть `CNAME` і налаштуйте `url` та `baseurl` відповідно.

## Збирання на GitHub

GitHub Pages збирає сайт. Не додавайте Gemfile, не вимагайте локального складання Jekyll і не комітьте створений каталог `_site/`. Додайте `_site/`, `.jekyll-cache/` і `.jekyll-metadata` до `.gitignore` проєкту.

## Перевірка розгортання

- Після схваленого надсилання до `main` переконайтеся, що завдання збирання й розгортання завершилися успішно.
- Відкрийте опубліковану головну сторінку та документацію; перевірте тему, бокову панель, логотип (якщо є), посилання й HTTPS.

Окремо повідомляйте про підготовку файлів і перевірку публікації. Якщо налаштування репозиторію, DNS або розгортання недоступні, назвіть незавершену роботу, а не позначайте налаштування сайту як виконане.

---

[Повернутися до BMForge]({{ site.baseurl }}{% link uk/index.md %})

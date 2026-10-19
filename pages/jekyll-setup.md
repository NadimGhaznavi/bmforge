---
title: Jekyll Setup
lang: en
locale: en-US
language_name: English
translation_key: bmforge-project-setup
---

Set up a new project's documentation site using GitHub Pages and the shared `NadimGhaznavi/minimal-mistakes` theme. This process prepares the Jekyll configuration and English documentation files, following BMGeoIP and BMDynIP.

Record any project-specific setup requirements or exceptions in the project's own documentation.

## Configure the Site

Copy the [configuration template]({{ '/templates/_config.yml' | relative_url }}) to `_config.yml` in the new project's root. Replace every `__PLACEHOLDER__` using the following values.

| Placeholder | Value |
| --- | --- |
| `__PROJECT_SLUG__` | Repository name, such as `bmforge`; also used as the MyCount site identifier |
| `__PROJECT_TITLE__` | Human-readable project name |
| `__PROJECT_DESCRIPTION__` | One sentence describing the project's purpose |
| `__GITHUB_OWNER__` | Repository owner or organization, taken from the Git remote |
| `__SITE_HOST__` | Published hostname, without a protocol or path |
| `__SITE_BASEURL__` | Empty string for a custom domain; `/repository-name` for a GitHub Pages project URL |
| `__PROJECT_LOGO__` | Path to an existing logo under `/pages/images/`, or an empty string until one is available |
| `__AUTHOR_NAME__` | Project owner's display name |
| `__AUTHOR_LOCATION__`, `__AUTHOR_EMAIL__` | Public author details; use empty strings for omitted details |
| `__AUTHOR_WEBSITE__` | Author's website URL; remove the corresponding link entry if unused |
| `__START_YEAR__` | Year the project began |

Derive the repository values from the Git remote and the title and description from the project brief. Use owner details and a hostname already established for the project; obtain any missing values from the owner. BMGeoIP and BMDynIP use `<project-slug>.osoyalce.com` with an empty `baseurl`.

Preserve these shared defaults:

- Remote theme `NadimGhaznavi/minimal-mistakes` and skin `dark`
- MyCount endpoint `https://count.osoyalce.com/count`
- Multilingual support enabled with English (`en`) as the default language and `en-US` as the default locale
- Kramdown/GFM Markdown and Rouge highlighting
- Documentation pages using `layout: single` with the author sidebar; the template also sets `classes: wide`
- The template's plugin list and Markdown processing settings

The shared theme owns presentation. Add local layout, CSS, or JavaScript overrides only for a specific project requirement.

## Create the Documentation Root

Create this structure in the project root:

```text
_config.yml
index.md
README.md
pages/
  images/
```

Use `index.md` as the sole documentation entry point. Give it YAML front matter with a project-specific title:

```yaml
---
title: "Project Name"
layout: single
author_profile: true
lang: en
locale: en-US
language_name: English
translation_key: __PROJECT_SLUG__-home
permalink: /
---
```

Below the front matter, add the logo if available, a brief project overview, and links to the documentation that exists. Keep `README.md` to a short overview and the website link.

Put English documentation in `pages/` and shared images in `pages/images/`. Give each documentation page YAML front matter with a `title`, `lang: en`, `locale: en-US`, `language_name: English`, and a stable `translation_key` unique to that page. Make every English page reachable from `index.md`.

{% raw %}
Use `{{ site.baseurl }}{% link pages/installation.md %}` for an internal page target, substituting an existing filename. Use `{{ site.baseurl }}/pages/images/project-logo.png` for an image target. Include a `[Documentation index]({{ site.baseurl }}{% link index.md %})` link on documentation pages.
{% endraw %}

## Prepare Multilingual Support

Keep this block in `_config.yml` for every new project:

```yaml
multilingual:
  enabled: true
  default_lang: en
```

Add the English language metadata and stable translation keys during setup. Create actual translations only after the project is complete, when its interface and documentation have settled. Follow [Multilingual Documentation]({{ site.baseurl }}{% link pages/multilingual-documentation.md %}) at that stage.

## Verify the Site Files

- Check that every configuration placeholder has been replaced and the project name, repository, hostname, logo, and MyCount identifier agree.
- Check YAML front matter, English language metadata, unique translation keys, internal link targets, image paths, and navigation from `index.md`.

## Publish the Site

Follow [GitHub Pages Publishing]({{ site.baseurl }}{% link pages/github-pages-publishing.md %}) to configure the workflow, domain, and HTTPS, then verify the deployed site.

---

[Back]({{ site.baseurl }}{% link index.md %})

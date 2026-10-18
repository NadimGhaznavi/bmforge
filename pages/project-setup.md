---
title: Project Setup
lang: en
locale: en-US
language_name: English
translation_key: bmforge-project-setup
---

## Jekyll Site Setup

The project needs a `_config.yml` in the root folder. Here is an [example](/templates/_config.yml).

---

## Git Branching Setup

```sh
git checkout -b dev
git checkout -b feat/maint-0.1.0
```

---

## Project Constant File

Create a *constants* file. (e.g. `mycount/constants/DMyCount.py`)

---

## New Release Script

`scripts/new-release.sh`

- Git branching: initial setup
- `install.sh`, `upgrade.sh`, and `uninstall.sh` scripts
- `constants/DProject.py` skeleton with `VERSION` and `CMDB` variables

---
layout: single
title: BMForge
permalink: /
classes: wide
author_profile: true
lang: en
locale: en-US
language_name: English
translation_key: bmforge-home
---

<link rel="stylesheet" href="{{ '/pages/css/bmforge-home.css' | relative_url }}">

![BMForge logo]({{ site.logo | relative_url }})

**Build small. Fail visibly. Own the implementation.**

BMForge turns an application's engineering decisions into **versioned specifications, proven patterns and project-local AI agent skills**. Codex follows the owner's software development lifecycle (SDLC), rather than improvising a new stack for every project.

## From requirements to an independent application

<section class="bmforge-flow" aria-label="BMForge software development lifecycle">
  <ol class="bmforge-flow__steps">
    <li>
      <span class="bmforge-flow__step">01 · Human</span>
      <h3>Define</h3>
      <p>The owner sets requirements, architecture, scope and approval boundaries.</p>
    </li>
    <li>
      <span class="bmforge-flow__step">02 · BMForge</span>
      <h3>Specify</h3>
      <p>Contracts define processes, approved modules, component behaviour and acceptance checks.</p>
    </li>
    <li>
      <span class="bmforge-flow__step">03 · Codex</span>
      <h3>Build &amp; verify</h3>
      <p>Pinned skills guide implementation, testing, installation and release preparation in the project's own repository.</p>
    </li>
    <li>
      <span class="bmforge-flow__step">04 · Application</span>
      <h3>Run independently</h3>
      <p>The released application owns its code and operates without a BMForge runtime dependency.</p>
    </li>
  </ol>
  <p class="bmforge-flow__feedback"><strong>↶ Feedback into BMForge:</strong> Real application defects reveal gaps. Improve the specification and regression checks, then deliberately adopt updated skills in future work.</p>
</section>

## The engineering philosophy

**One standard, no legacy baggage.** Keep solutions lean, make failures visible and require approval for new technology choices. When the standard improves, older applications can be deliberately refactored to adopt it; BMForge does not grow compatibility layers to preserve outdated designs.

## Explore BMForge

[Get started with Codex]({{ site.baseurl }}{% link pages/codex-skills.md %}) · [Technical reference and component catalogue]({{ site.baseurl }}{% link pages/technical-reference.md %}) · [Engineering contract]({{ site.baseurl }}{% link pages/engineering-contract.md %})

BMForge is an engineering specification, **not a shared application framework or runtime library**. Independent applications communicate through documented public APIs.

Another [Bear & Moose](https://osoyalce.com) project. · [Source repository](https://github.com/NadimGhaznavi/bmforge)

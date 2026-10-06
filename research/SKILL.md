---
name: research
description: 针对一个问题，以高可信度的第一手来源做调研，并把结论整理成 Markdown 文件存进仓库。适用于用户想调研某个主题、收集文档或 API 事实，或把查资料的体力活交给后台 agent 时。
---

Spin up a **background agent** to do the research, so you keep working while it reads.

Its job:

1. Investigate the question against **primary sources** (official docs, source code, specs, first-party APIs), not a secondary write-up of them. Follow every claim back to the source that owns it.
2. Write the findings to a single Markdown file, citing each claim's source.
3. Save it where the repo already keeps such notes; match the existing convention, and if there is none, put it somewhere sensible and say where.

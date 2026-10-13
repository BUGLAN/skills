---
name: handoff
description: 把当前对话压缩成一份交接文档，好让另一个代理接着干。
argument-hint: "下一个会话准备用来做什么？"
disable-model-invocation: true
---

写一份交接文档（handoff document），总结当前对话，让一个全新的代理能继续这项工作。保存到用户操作系统的临时目录——不要放进当前工作区（workspace）。

文档里要包含一个 "suggested skills"（建议调用的 skill）小节，写明下一个代理应该调用 Skill 工具的哪些 skill。

不要重复其他产物（spec、plan、ADR、issue、commit、diff）里已经记录的内容，改用路径或 URL 引用它们。

脱敏：API key、密码、个人身份信息（PII）等敏感内容一律删掉。

如果用户传了参数，就把它当作对下一个会话关注点的描述，据此裁剪文档。

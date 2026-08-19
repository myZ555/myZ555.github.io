---
name: mermaid
description: 将 Markdown 文件的 1-5 级标题层级转换为 Mermaid flowchart。当用户要求根据 Markdown 标题结构生成、绘制或可视化文档结构时使用。
---

# 将 Markdown 文件的标题层级转换为 Mermaid `flowchart TD`。

## 规则

1. 只解析 1-5 级标题：`#`、`##`、`###`、`####`、`#####`。
2. 标题层级决定节点的父子关系。
3. 忽略正文、列表、引用和代码块中的内容。
4. 每个标题生成一个唯一节点 ID，标题文本作为节点名称。
5. 每个节点连接到其最近的上一级标题。
6. 输出完整的 Mermaid 代码块，保存至/Notes-site/Mermaid/<filename>.md，filename 即输入 Markdown 文件名称+当日日期。

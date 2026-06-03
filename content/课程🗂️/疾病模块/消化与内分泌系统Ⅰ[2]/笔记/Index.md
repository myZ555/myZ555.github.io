---
publish: true
---

# 索引

```dataview
TABLE
  file.tags as "标签",
  file.mtime as "最后更新"
FROM ""
WHERE file.folder = this.file.folder AND file.name != this.file.name
SORT file.ctime ASC
```

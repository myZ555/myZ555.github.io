# Mingyu Medical Notes

这是一个使用 MkDocs Material 构建的医学学习笔记站点。

## 本地开发

项目使用 `.venv` 隔离 MkDocs 及其插件依赖。首次使用或依赖发生变化时执行：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

本地预览：

```bash
.venv/bin/mkdocs serve
```

检查构建（包含链接检查）：

```bash
.venv/bin/mkdocs build --strict --site-dir /tmp/notes-site-build
```

`.venv/` 和 `site/` 都不会提交到 Git。GitHub Actions 会在干净的 CI 环境中按 `requirements.txt` 安装同样的固定版本并部署到 GitHub Pages。

## 提交前检查

```bash
git status --short
.venv/bin/mkdocs build --strict --site-dir /tmp/notes-site-build
```

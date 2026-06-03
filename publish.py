import os
import re
import shutil

# ==================== 【请在这里修改你的路径】 ====================
VAULT_DIR = "/Users/mingyu/Documents/课程🗂️"  # 👈 换成你Obsidian主库的绝对路径
# ================================================================

CONTENT_DIR = "./content"
ATTACH_DIR = os.path.join(CONTENT_DIR, "attachments")

if os.path.exists(CONTENT_DIR):
    shutil.rmtree(CONTENT_DIR)
os.makedirs(ATTACH_DIR, exist_ok=True)

print("🚀 正在 1:1 完美复刻 Obsidian 原生文件夹层级...")

published_files = []

for root, dirs, files in os.walk(VAULT_DIR):
    if ".obsidian" in root or ".git" in root:
        continue
    for file in files:
        if file.endswith(".md"):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if re.search(r"^publish:\s*true", content, re.MULTILINE):
                        # 💡 核心改动：直接计算相对路径，不添加任何多余的父级包裹
                        rel_path = os.path.relpath(file_path, VAULT_DIR)
                        dest_path = os.path.join(CONTENT_DIR, rel_path)
                        
                        # 自动在网站里创建一模一样的子文件夹结构
                        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                        shutil.copy2(file_path, dest_path)
                        published_files.append(dest_path)
                        print(f"  ✓ [同步成功]: {rel_path}")
            except Exception:
                pass

# 自动抓取附件逻辑
asset_index = {}
for root, dirs, files in os.walk(VAULT_DIR):
    if ".obsidian" in root or "node_modules" in root:
        continue
    for file in files:
        if not file.endswith(".md"):
            asset_index[file] = os.path.join(root, file)

wiki_link_regex = re.compile(r"!\[\[(.*?)\]\]")
for file_path in published_files:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    matches = wiki_link_regex.findall(content)
    for asset_name in matches:
        pure_name = asset_name.split("|")[0].strip()
        if pure_name in asset_index:
            src_asset = asset_index[pure_name]
            dest_asset = os.path.join(ATTACH_DIR, pure_name)
            if not os.path.exists(dest_asset):
                shutil.copy2(src_asset, dest_asset)

print("\n✨ 1:1 数据同步及附件抓取完全成功！")
import os
import re
import shutil

# ==================== 【请在这里修改你的路径】 ====================
VAULT_DIR = "/Users/mingyu/Documents"  # 👈 换成你Obsidian主库的绝对路径
# ================================================================

CONTENT_DIR = "./content"
ATTACH_DIR = os.path.join(CONTENT_DIR, "attachments").strip()

if os.path.exists(CONTENT_DIR):
    shutil.rmtree(CONTENT_DIR)
os.makedirs(ATTACH_DIR, exist_ok=True)

print("🚀 正在 1:1 完美复刻 Obsidian 原生文件夹层级...")

published_files = []

for root, dirs, files in os.walk(VAULT_DIR):
    # 过滤掉隐藏文件夹和博客自身的目录，防止无限套娃
    if ".obsidian" in root or ".git" in root or "my-blog" in root or "node_modules" in root:
        continue
    for file in files:
        if file.endswith(".md"):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if re.search(r"^(dg-)?publish:\s*true", content, re.MULTILINE):
                        
                        # 💡 核心拦截规则：如果是主页，无视它原本在哪个子文件夹，强行提到全站根目录
                        if file.lower() == "index.md":
                            dest_path = os.path.join(CONTENT_DIR, "index.md")
                            print(f"  👑 [总门户拦截成功]: {os.path.relpath(file_path, VAULT_DIR)} -> 全站首页")
                        else:
                            # 其他笔记依然保持 1:1 的原生跨库层级
                            rel_path = os.path.relpath(file_path, VAULT_DIR)
                            dest_path = os.path.join(CONTENT_DIR, rel_path)
                            print(f"  ✓ [跨库同步]: {rel_path}")
                        
                        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                        shutil.copy2(file_path, dest_path)
                        published_files.append(dest_path)
            except Exception as e:
                print(f"  ❌ 读取失败 {file}: {str(e)}")

# 自动抓取多库附件逻辑
asset_index = {}
for root, dirs, files in os.walk(VAULT_DIR):
    if ".obsidian" in root or "my-blog" in root or "node_modules" in root:
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

print("\n✨ 跨库合流及总主页定位完全成功！")
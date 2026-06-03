import os
import re
import shutil

# ==================== 【请在这里修改你的路径】 ====================
VAULT_DIR = "/Users/mingyu/Documents/课程🗂️"  # 👈 换成你Obsidian主库的绝对路径
# ================================================================

CONTENT_DIR = "./content"
ATTACH_DIR = os.path.join(CONTENT_DIR, "attachments")

# 1. 彻底清空并重建网站的缓存目录，确保过期的公开笔记能被彻底删除
if os.path.exists(CONTENT_DIR):
    shutil.rmtree(CONTENT_DIR)
os.makedirs(ATTACH_DIR, exist_ok=True)

print("🚀 开始全库扫描，正在安全筛选公开笔记...")

published_files = []

# 2. 扫描 Obsidian 全库，只抓取带 publish: true 的 Markdown 文件
for root, dirs, files in os.walk(VAULT_DIR):
    # 忽略 Obsidian 自身的隐藏点文件夹
    if ".obsidian" in root:
        continue
    for file in files:
        if file.endswith(".md"):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    # 正则匹配顶部 Frontmatter 是否包含 publish: true
                    if re.search(r"^publish:\s*true", content, re.MULTILINE):
                        # 统一扁平化复制到 content 根目录，Quartz 能完美识别彼此的双链
                        dest_path = os.path.join(CONTENT_DIR, file)
                        shutil.copy2(file_path, dest_path)
                        published_files.append(dest_path)
                        print(f"  ✓ [发现公开笔记]: {file}")
            except Exception:
                pass

# 3. 建立全库的附件（图片/PDF）索引，用于精准抓取
asset_index = {}
for root, dirs, files in os.walk(VAULT_DIR):
    if ".obsidian" in root or "node_modules" in root:
        continue
    for file in files:
        if not file.endswith(".md"):  # 收集所有图片、PDF 等
            asset_index[file] = os.path.join(root, file)

# 4. 分析公开笔记，把里面真正引用到的图片连带打包带走
wiki_link_regex = re.compile(r"!\[\[(.*?)\]\]")

for file_path in published_files:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    matches = wiki_link_regex.findall(content)
    for asset_name in matches:
        # 切除可能存在的别名（如 ![[pic.png|100]]）
        pure_name = asset_name.split("|")[0].strip()
        if pure_name in asset_index:
            src_asset = asset_index[pure_name]
            dest_asset = os.path.join(ATTACH_DIR, pure_name)
            if not os.path.exists(dest_asset):
                shutil.copy2(src_asset, dest_asset)
                print(f"    └─ 📎 [自动打包附件]: {pure_name}")

print("\n✨ 提取完成！本地部署缓存区已准备就绪。")
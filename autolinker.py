import os
import re

# 我们让脚本直接扫描发布用的暂存区
CONTENT_DIR = "./content"

# 匹配标题和高亮加粗
HEADING_REGEX = re.compile(r"^(#{1,6})\s+(.+)$")
MARKER_REGEX = re.compile(r"==([^=]+)==|\*\*([^*]+)\*\*")

def build_dict():
    mesh_dict = {}
    # 假设你的医学库在 content 下被命名为类似包含 "医学" 的文件夹
    # 脚本会遍历所有文件寻找医学高亮词
    for root, dirs, files in os.walk(CONTENT_DIR):
        if "my-everyday" in root: # 避开日常随笔，只从硬核库里提取词条
            continue
            
        for file in files:
            if not file.endswith(".md") or file == "index.md":
                continue
                
            current_file_title = file.replace(".md", "")
            current_heading = ""
            file_path = os.path.join(root, file)
            
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    # 抓取当前标题级别
                    heading_match = HEADING_REGEX.match(line.strip())
                    if heading_match:
                        if len(heading_match.group(1)) >= 2:
                            current_heading = heading_match.group(2).strip()
                        continue
                    
                    # 抓取被 == 或 ** 包裹的关键词
                    for match in MARKER_REGEX.findall(line):
                        keyword = match[0] if match[0] else match[1]
                        keyword = keyword.strip()
                        if len(keyword) > 1:
                            if current_heading:
                                mesh_dict[keyword] = f"[[{current_file_title}#{current_heading}]]"
                            else:
                                mesh_dict[keyword] = f"[[{current_file_title}]]"
    return mesh_dict

def inject_footnotes(mesh_dict):
    # 现在去扫描日常随笔库
    for root, dirs, files in os.walk(CONTENT_DIR):
        for file in files:
            if not file.endswith(".md"):
                continue
                
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            found_keywords = []
            for keyword, link in mesh_dict.items():
                # 如果日常随笔里出现了医学词条
                if keyword in content:
                    found_keywords.append((keyword, link))
            
            # 如果找到了关联，就在文章最末尾追加脚注
            if found_keywords:
                with open(file_path, "a", encoding="utf-8") as f:
                    f.write("\n\n---\n") # 画一条分割线
                    for idx, (kw, lnk) in enumerate(found_keywords, 1):
                        f.write(f"[^{idx}]: 🤖 **赛博巡逻队提示**：检测到特异性名词 `{kw}`，可协同参阅核心库 -> {lnk}\n")

if __name__ == "__main__":
    print("🤖 赛博巡逻队启动：正在构建医学全库哈希映射...")
    dictionary = build_dict()
    print(f"✅ 映射构建完成，共抓取 {len(dictionary)} 个原子级医学锚点。")
    print("🔍 正在扫描全站文章并静默注入跨库脚注...")
    inject_footnotes(dictionary)
    print("✨ 脚注注入完毕！")
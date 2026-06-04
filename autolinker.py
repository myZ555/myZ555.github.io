import os
import re

CONTENT_DIR = "./content"

# 匹配标题和高亮/加粗
HEADING_REGEX = re.compile(r"^(#{1,6})\s+(.+)$")
MARKER_REGEX = re.compile(r"==([^=]+)==|\*\*([^*]+)\*\*")

def build_dict():
    mesh_dict = {}
    for root, dirs, files in os.walk(CONTENT_DIR):
        # 避开日常随笔库，只从硬核医学库里提取核心词条
        if "my-everyday" in root:
            continue
            
        for file in files:
            if not file.endswith(".md") or file == "index.md":
                continue
                
            current_file_title = file.replace(".md", "")
            current_heading = ""
            file_path = os.path.join(root, file)
            
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        heading_match = HEADING_REGEX.match(line.strip())
                        if heading_match:
                            if len(heading_match.group(1)) >= 2:
                                current_heading = heading_match.group(2).strip()
                            continue
                        
                        for match in MARKER_REGEX.findall(line):
                            keyword = match[0] if match[0] else match[1]
                            keyword = keyword.strip()
                            # 过滤掉单字和脚注标记
                            if len(keyword) > 1 and not keyword.startswith("[^"):
                                if current_heading:
                                    mesh_dict[keyword] = f"[[{current_file_title}#{current_heading}]]"
                                else:
                                    mesh_dict[keyword] = f"[[{current_file_title}]]"
            except Exception:
                pass
    return mesh_dict

def inject_links(mesh_dict):
    injection_count = 0
    for root, dirs, files in os.walk(CONTENT_DIR):
        # 核心逻辑：巡逻队只去扫描日常随笔库，防止医学库自我套娃
        if "my-everyday" not in root:
            continue
            
        for file in files:
            if not file.endswith(".md") or file == "index.md":
                continue
                
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                found_keywords = {}
                for keyword, link in mesh_dict.items():
                    # 确保日常随笔里包含这个医学核心词，且该词不是随笔的文件名本身
                    if keyword in content and keyword != file.replace(".md", ""):
                        found_keywords[keyword] = link
                
                # 如果在这篇日常随笔里抓到了医学交织点
                if found_keywords:
                    rel_path = os.path.relpath(file_path, CONTENT_DIR)
                    print(f"  📌 [发现联动] -> 正在为随笔《{rel_path}》编织跨库网络...")
                    
                    # 💡 核心升级：改用高颜值的 Obsidian Callout 面板挂在最底下，确保 100% 被检索
                    callout_content = "\n\n---\n\n> [!info] 🤖 赛博巡逻队知识联动\n> 检测到本文探讨的内容在您的核心医学大盘中有系统阐述，可协同参阅：\n"
                    for kw, lnk in found_keywords.items():
                        print(f"    ➔ 匹配词条: {kw}")
                        callout_content += f"> - **{kw}** ➔ {lnk}\n"
                    
                    with open(file_path, "a", encoding="utf-8") as f:
                        f.write(callout_content)
                    injection_count += 1
            except Exception as e:
                print(f"  ❌ 扫描随笔失败 {file}: {str(e)}")
                
    print(f"\n✨ 巡逻完毕！本次共为 {injection_count} 篇日常随笔注入了高颜值跨库看板。")

if __name__ == "__main__":
    print("🤖 赛博巡逻队启动：正在构建医学全库哈希映射...")
    dictionary = build_dict()
    print(f"✅ 映射构建完成，共抓取 {len(dictionary)} 个原子级医学锚点。")
    print("🔍 正在扫描随笔并静默注入高颜值跨库看板...")
    inject_links(dictionary)
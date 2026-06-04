import os

CONTENT_DIR = "./content"

def clean_concept_name(filename):
    """
    清洗文件名：去掉开头的数字编号（如 I-4-02、11）、后缀.md、空格和特殊符号
    """
    name = filename.replace(".md", "")
    name = os.path.basename(name)
    # 移除前缀数字/字母序号，例如 "I-4-02 胃食管反流病" -> "胃食管反流病"
    name = ''.join([c for c in name if not c.isdigit()]).strip()
    name = name.lstrip('-._、 ')
    return name

def build_concept_market():
    """
    第一步：扫描医学库，把所有『文件名』登记成核心概念字典
    """
    concept_map = {}
    for root, dirs, files in os.walk(CONTENT_DIR):
        # 🛡️ 严格安全防线：彻底排除日常随笔库，不从这里提取任何概念
        if "everyday" in root.lower().replace(" ", ""):
            continue
            
        for file in files:
            if not file.endswith(".md") or file == "index.md":
                continue
                
            file_title_raw = file.replace(".md", "")
            clean_concept = clean_concept_name(file)
            
            if len(clean_concept) >= 2: # 至少两个字才算一个核心概念
                concept_map[clean_concept] = f"[[{file_title_raw}]]"
    return concept_map

def inject_internal_links(concept_map):
    """
    第二步：只在医学课程笔记内部巡逻，寻找横向章节的蛛丝马迹
    """
    injection_count = 0
    print("\n================== 🔬 课程笔记内部解耦织网 ==================")
    
    for root, dirs, files in os.walk(CONTENT_DIR):
        # 🛡️ 核心修正：如果路径包含 everyday，直接跳过！绝对不碰任何生活随笔！
        if "everyday" in root.lower().replace(" ", ""):
            continue
            
        for file in files:
            if not file.endswith(".md") or file == "index.md":
                continue
                
            file_path = os.path.join(root, file)
            current_file_clean = clean_concept_name(file)
            
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    note_text = f.read()
                
                matched_links = {}
                for concept, link in concept_map.items():
                    # 1. 别自己链接自己（例如食管癌笔记里提到食管癌）
                    if concept == current_file_clean:
                        continue
                    
                    # 2. 核心模糊逻辑：长词支持切片模糊匹配（如正文写了"胃食管反流"也能连到"胃食管反流病"）
                    fuzzy_short_concept = concept[:-1] if len(concept) >= 5 else concept
                    
                    # 3. 核心防线：正文提到了该概念，且正文中【还没有】打过指向该章节的 Obsidian 双链
                    if (concept in note_text or fuzzy_short_concept in note_text) and (link not in note_text):
                        matched_links[concept] = link
                
                # 如果这篇医学笔记撞上了本库其他章节的概念
                if matched_links:
                    rel_path = os.path.relpath(file_path, CONTENT_DIR)
                    print(f"  🔗 [内部引用发现] -> 正在为医学章节 《{rel_path}》 编织横向跨章链接...")
                    
                    callout_content = "\n\n---\n\n> [!info] 🤖 赛博巡逻队：本章横向知识关联\n> 检测到本章内容提及了其他章节的核心概念，可协同参阅：\n"
                    for concept, link in matched_links.items():
                        print(f"    ➔ 关联本库章节: {concept}")
                        callout_content += f"> - 📖 **{concept}** ➔ {link}\n"
                    
                    with open(file_path, "a", encoding="utf-8") as f:
                        f.write(callout_content)
                    injection_count += 1
            except Exception as e:
                print(f"  ❌ 扫描医学笔记失败 {file}: {str(e)}")
                
    print("===========================================================\n")
    print(f"✨ 巡逻完毕！本次共在医学课程笔记内部建立了 {injection_count} 处横向章节联动。")

if __name__ == "__main__":
    print("🤖 赛博巡逻队（内部对齐版）启动：正在清点医学全库章节...")
    market = build_concept_market()
    print(f"✅ 清点完毕，雷达字典已录入 {len(market)} 个医学专用概念。")
    inject_internal_links(market)
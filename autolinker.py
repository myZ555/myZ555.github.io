import os

CONTENT_DIR = "./content"

# 🛑 门禁 2：核心大词黑名单（医学库里天天见，不需要泛滥链接）
BLACKLIST = {"血液", "呼吸", "胸腔", "腹部", "内分泌", "生殖", "循环", "神经", "消化", "症状", "体征", "检查"}

# 🎯 门禁 3：特异性临床后缀（只有符合这些结尾的才算核心疾病概念，可选）
CLINICAL_SUFFIXES = ("病", "癌", "炎", "症", "瘤", "综合征", "危象", "溃疡", "狭窄", "梗死")

def clean_concept_name(filename):
    name = filename.replace(".md", "")
    name = os.path.basename(name)
    name = ''.join([c for c in name if not c.isdigit()]).strip()
    name = name.lstrip('-._、 ')
    return name

def build_concept_market():
    concept_map = {}
    for root, dirs, files in os.walk(CONTENT_DIR):
        if "everyday" in root.lower().replace(" ", ""):
            continue
            
        for file in files:
            if not file.endswith(".md") or file == "index.md":
                continue
                
            file_title_raw = file.replace(".md", "")
            clean_concept = clean_concept_name(file)
            
            # ====== 🔒 智能净化闸门拦截核心逻辑 =====
            
            # 闸门 A：过滤黑名单大词
            if clean_concept in BLACKLIST:
                continue
                
            # 闸门 B：字数硬性防御 —— 必须大于等于 3 个字（干掉"血液"、"呼吸"，保留"食管癌"、"高血压"）
            if len(clean_concept) < 3:
                continue
                
            # 闸门 C：特异性过滤 —— 必须是具体的疾病、病理或临床表现
            if not clean_concept.endswith(CLINICAL_SUFFIXES):
                continue
                
            # =======================================
            
            concept_map[clean_concept] = f"[[{file_title_raw}]]"
    return concept_map

def inject_internal_links(concept_map):
    injection_count = 0
    print("\n================== 🔬 课程笔记内部【高含金量】织网 ==================")
    
    for root, dirs, files in os.walk(CONTENT_DIR):
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
                    if concept == current_file_clean:
                        continue
                    
                    fuzzy_short_concept = concept[:-1] if len(concept) >= 5 else concept
                    
                    if (concept in note_text or fuzzy_short_concept in note_text) and (link not in note_text):
                        matched_links[concept] = link
                
                if matched_links:
                    rel_path = os.path.relpath(file_path, CONTENT_DIR)
                    print(f"  🔗 [强效联动发现] -> 正在为医学章节 《{rel_path}》 接入高价值横向链接...")
                    
                    callout_content = "\n\n---\n\n> [!info] 🤖 赛博巡逻队：本章核心临床联动\n> 检测到本章探讨的内容与其他章节的疾病概念强相关，可协同参阅：\n"
                    for concept, link in matched_links.items():
                        print(f"    ➔ 关联硬核章节: {concept}")
                        callout_content += f"> - 📖 **{concept}** ➔ {link}\n"
                    
                    with open(file_path, "a", encoding="utf-8") as f:
                        f.write(callout_content)
                    injection_count += 1
            except Exception as e:
                print(f"  ❌ 扫描医学笔记失败 {file}: {str(e)}")
                
    print("===========================================================\n")
    print(f"✨ 巡逻完毕！本次共在医学课程笔记内部建立了 {injection_count} 处高价值章节联动。")

if __name__ == "__main__":
    print("🤖 赛博巡逻队（疾病限定版）启动：正在清点硬核医学章节...")
    market = build_concept_market()
    print(f"✅ 清点完毕，雷达字典已录入 {len(market)} 个特异性临床疾病概念。")
    inject_internal_links(market)
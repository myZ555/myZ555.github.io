import os

CONTENT_DIR = "./content"

def clean_concept_name(filename):
    """
    清洗文件名：去掉开头的数字编号（如 I-4-02、11）、后缀.md、空格和特殊符号
    """
    name = filename.replace(".md", "")
    # 用简单的规则去掉开头的序号，比如 "I-4-02 胃食管反流病" -> "胃食管反流病"
    name = os.path.basename(name)
    # 去掉常见的前缀数字和字母
    name = ''.join([c for c in name if not c.isdigit()]).strip()
    name = name.lstrip('-._、 ')
    return name

def build_concept_market():
    """
    第一步：扫描医学库，把所有『文件名』登记成核心概念字典
    """
    concept_map = {}
    for root, dirs, files in os.walk(CONTENT_DIR):
        # 避开随笔库，只拿医学库的文件名
        if "everyday" in root.lower().replace(" ", ""):
            continue
            
        for file in files:
            if not file.endswith(".md") or file == "index.md":
                continue
                
            file_title_raw = file.replace(".md", "")
            clean_concept = clean_concept_name(file)
            
            if len(clean_concept) >= 2: # 至少两个字才算一个医学概念
                # 登记标准双链路径
                concept_map[clean_concept] = f"[[{file_title_raw}]]"
    return concept_map

def inject_intelligent_links(concept_map):
    """
    第二步：去随笔库里巡逻，只要发现随笔里包含了医学文件名（或其核心前缀），就挂上大盘联动卡片
    """
    injection_count = 0
    print("\n================== 🛰️ 概念雷达实时扫描 ==================")
    
    for root, dirs, files in os.walk(CONTENT_DIR):
        # 只去扫描随笔库
        if "everyday" not in root.lower().replace(" ", ""):
            continue
            
        for file in files:
            if not file.endswith(".md") or file == "index.md":
                continue
                
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                everyday_text = f.read()
            
            matched_links = {}
            for concept, link in concept_map.items():
                # 💡 核心模糊逻辑：
                # 1. 精确匹配：随笔里写了完整的 "胃食管反流病"
                # 2. 相关性模糊匹配：如果文件名很长（如"胃食管反流病"），用户只写了前 4 个字（"胃食管反流"），也算命中！
                fuzzy_short_concept = concept[:-1] if len(concept) >= 5 else concept
                
                if (concept in everyday_text or fuzzy_short_concept in everyday_text) and concept != file.replace(".md", ""):
                    matched_links[concept] = link
            
            # 如果这篇随笔撞上了医学库的文件名概念
            if matched_links:
                print(f"  🎯 [概念撞车成功] -> 正在为 《{file}》 接入医学大盘...")
                
                callout_content = "\n\n---\n\n> [!info] 🤖 赛博巡逻队概念联动\n> 检测到本文提及了您核心医学库中的章节概念，可直达大盘深挖主题：\n"
                for concept, link in matched_links.items():
                    print(f"    ➔ 关联医学章节: {concept}")
                    callout_content += f"> - 📚 **{concept}** ➔ {link}\n"
                
                with open(file_path, "a", encoding="utf-8") as f:
                    f.write(callout_content)
                injection_count += 1
                
    print("===========================================================\n")
    print(f"✨ 巡逻完毕！本次共为 {injection_count} 篇日常随笔精准缝合了医学大盘入口。")

if __name__ == "__main__":
    print("🤖 赛博巡逻队（概念版）启动：正在清点全库医学章节...")
    market = build_concept_market()
    print(f"✅ 清点完毕，已将 {len(market)} 个核心医学文件名录入雷达字典。")
    inject_intelligent_links(market)
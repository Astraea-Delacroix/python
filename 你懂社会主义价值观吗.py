# 标准12词顺序（固定密码本）
core_words = ["富强","民主","文明","和谐","自由","平等","公正","法治","爱国","敬业","诚信","友善"]

def core_value_decrypt():
    print("===== 社会主义核心价值观解密工具 =====")
    print("密码本：0富强 1民主 2文明 3和谐 4自由 5平等 6公正 7法治 8爱国 9敬业 10诚信 11友善\n")
    
    while True:
        cipher = input("请输入密文关键词/序号（多个用英文逗号分隔，输入q退出）：").strip()
        if cipher.lower() == "q":
            break
        
        res = []
        parts = cipher.split(",")
        for p in parts:
            p = p.strip()
            # 输入是数字序号 → 转明文
            if p.isdigit():
                idx = int(p)
                if 0 <= idx <= 11:
                    res.append(core_words[idx])
                else:
                    res.append(f"[{p}无效]")
            # 输入是关键词 → 校验并输出
            elif p in core_words:
                res.append(p)
            else:
                res.append(f"[{p}不存在]")
        
        print("解密明文：" + "，".join(res) + "\n")

if __name__ == "__main__":
    core_value_decrypt()
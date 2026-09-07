def caesar_decrypt(ciphertext: str, shift: int) -> str:
    """单指定位移解密"""
    plain = ""
    for c in ciphertext:
        if c.isupper():
            plain += chr((ord(c) - ord('A') - shift) % 26 + ord('A'))
        elif c.islower():
            plain += chr((ord(c) - ord('a') - shift) % 26 + ord('a'))
        else:
            plain += c  # 符号、数字直接保留
    return plain

def brute_force_caesar(ciphertext: str):
    """暴力破解：遍历全部26种位移"""
    print("=== 凯撒密码全位移破解结果 ===")
    for shift in range(1, 26):
        res = caesar_decrypt(ciphertext, shift)
        print(f"位移 {shift:2d} → {res}")

# ========== 使用示例 ==========
if __name__ == "__main__":
    cipher = input("请输入密文：")
    brute_force_caesar(cipher)
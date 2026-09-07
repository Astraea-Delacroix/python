import math

# 快速幂取模（RSA核心，防大数溢出）
def pow_mod(base, exp, mod):
    return pow(base, exp, mod)

# 欧几里得算法求最大公约数
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# 扩展欧几里得求模逆元（求d）
def mod_inv(a, m):
    m0, y, x = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        t = m
        m = a % m
        a = t
        t = y
        y = x - q * y
        x = t
    if x < 0:
        x += m0
    return x

# 生成RSA密钥
def rsa_gen_key(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    # 选e，常用e=65537
    e = 65537
    while gcd(e, phi) != 1:
        e += 2
    d = mod_inv(e, phi)
    return (e, n), (d, n)

# 加密
def rsa_encrypt(m, pub_key):
    e, n = pub_key
    return pow_mod(m, e, n)

# 解密
def rsa_decrypt(c, pri_key):
    d, n = pri_key
    return pow_mod(c, d, n)

# 暴力破解RSA（已知n，分解p、q）
def rsa_crack(n):
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            p = i
            q = n // i
            phi = (p - 1) * (q - 1)
            e = 65537
            d = mod_inv(e, phi)
            return p, q, d
    return None

# 示例
if __name__ == "__main__":
    # 1. 生成密钥（小质数测试）
    p, q = 61, 53
    pub, pri = rsa_gen_key(p, q)
    print("公钥(e,n):", pub)
    print("私钥(d,n):", pri)

    # 2. 加解密测试
    m = 12345
    c = rsa_encrypt(m, pub)
    print("密文:", c)
    print("解密明文:", rsa_decrypt(c, pri))

    # 3. 破解测试（已知n，求私钥）
    n = pub[1]
    p_crack, q_crack, d_crack = rsa_crack(n)
    print(f"\n破解结果 p={p_crack}, q={q_crack}, 私钥d={d_crack}")
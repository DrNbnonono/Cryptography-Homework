from math import gcd
from itertools import permutations


def modular_inverse(a, modulus):
    """计算模逆，返回 a 在 modulus 下的逆元"""
    a %= modulus
    for x in range(1, modulus):
        if (a * x) % modulus == 1:
            return x
    return None


def affine_cipher_decryption(a, b, ciphertext):
    """解密给定的仿射密码文本"""
    charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    modulus = len(charset)  # 字母表长度，26
    a_inv = modular_inverse(a, modulus)
    if a_inv is None:
        raise ValueError("a 没有模逆，非法密码！")
    
    plaintext = ""
    for char in ciphertext:
        if char in charset:
            y = charset.index(char)
            x = (a_inv * (y - b)) % modulus
            plaintext += charset[x]
        else:
            plaintext += char  # 保留非字母字符
    return plaintext


def validate_pairs(pair1, pair2):
    """检查两对字母的映射是否生成合法的密钥"""
    charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    modulus = len(charset)
    
    # 获取第一个映射对
    x1 = charset.index(pair1[0].upper())
    y1 = charset.index(pair1[1].upper())
    
    # 获取第二个映射对
    x2 = charset.index(pair2[0].upper())
    y2 = charset.index(pair2[1].upper())
    
    # 计算 a 和 b
    delta_x = (x1 - x2) % modulus
    delta_y = (y1 - y2) % modulus
    a_inv = modular_inverse(delta_x, modulus)
    if a_inv is None:
        return None, None
    a = (delta_y * a_inv) % modulus
    b = (y1 - a * x1) % modulus

    # 验证 gcd(a, 26) == 1
    if gcd(a, modulus) != 1:
        return None, None
    return a, b


def main():
    print("仿射密码解密工具")
    print("请输入密文中前六个最常见的字母（按频率降序排列，例如 S,L,Y,M,V,E）：")
    ciphertext = input("请输入密文（大写英文）：")
    crypt_freq = input("请输入密文中的高频字母（例如 S,L,Y,M,V,E）：").split(',')
    plain_freq = "E,T,A,O,I,N".split(',')

    found_any = False  # 标记是否找到合法的密钥对

    # 测试所有高频字母的合法映射组合
    for pair1 in permutations(crypt_freq, 2):
        for pair2 in permutations(plain_freq, 2):
            try:
                a, b = validate_pairs(pair1, pair2)
                if a is not None and b is not None:
                    found_any = True
                    print(f"找到合法映射对: {pair1} -> {pair2}")
                    print(f"生成密钥: a = {a}, b = {b}")
                    plaintext = affine_cipher_decryption(a, b, ciphertext)
                    print(f"解密后的明文为：{plaintext}")
            except Exception:
                continue
    
    if not found_any:
        print("没找到合法映射对，您需要手动输入映射对！")
        charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        while True:
            try:
                manual_pair1 = input("手动输入第一个映射对（如 'e,R'）: ").split(',')
                manual_pair2 = input("手动输入第二个映射对（如 'k,H'）: ").split(',')
                
                if len(manual_pair1) != 2 or len(manual_pair2) != 2 or \
                   manual_pair1[0].upper() not in charset or manual_pair1[1].upper() not in charset or \
                   manual_pair2[0].upper() not in charset or manual_pair2[1].upper() not in charset:
                    print("输入不合法，请重新输入两对字母映射。")
                    continue
                
                # 验证并计算密钥
                a, b = validate_pairs(manual_pair1, manual_pair2)
                if a is None or b is None:
                    print("选择的字母映射生成非法密钥，请重新选择！")
                    continue
                
                print(f"成功生成密钥: a = {a}, b = {b}")
                plaintext = affine_cipher_decryption(a, b, ciphertext)
                print(f"解密后的明文为：{plaintext}")
                break
            except Exception as error:
                print(f"发生错误：{error} 请重试。")


if __name__ == "__main__":
    main()

from collections import Counter

# 英文字母出现频率表 (A-Z)
ENGLISH_LETTER_FREQUENCIES = [
    0.082, 0.015, 0.028, 0.043, 0.127, 0.022, 0.020, 0.061, 0.070, 0.002,
    0.008, 0.040, 0.024, 0.067, 0.075, 0.019, 0.001, 0.060, 0.063, 0.091,
    0.028, 0.010, 0.023, 0.001, 0.020, 0.001
]

def calculate_mg_for_group(group, shift):
    """
    计算单个组在特定移位下的 M_g 值。
    :param group: 密文子串
    :param shift: 当前移位值 g (0-25)
    :return: M_g 值
    """
    n = len(group)
    if n == 0:
        return 0

    # 统计字母频数
    freqs = Counter(group)
    
    # 计算 M_g
    mg = 0
    for j in range(26):
        shifted_index = (j + shift) % 26
        mg += ENGLISH_LETTER_FREQUENCIES[j] * freqs.get(chr(shifted_index + ord('A')), 0)
    mg /= n
    return mg

def calculate_mg_values(cipher_text, group_size):
    """
    计算密文分组后所有组和所有移位方案的 M_g 值。
    :param cipher_text: 密文
    :param group_size: 分组大小
    :return: 每组移位下的 M_g 值列表
    """
    # 去掉空白字符和非字母字符
    cipher_text = ''.join(c for c in cipher_text if c.isalpha())

    # 分组，将密文划分为 group_size 个组
    groups = ['' for _ in range(group_size)]
    for i, char in enumerate(cipher_text):
        groups[i % group_size] += char

    # 对每组计算 M_g 值
    mg_results = []
    for i, group in enumerate(groups):
        mgs_for_shifts = []
        for g in range(26):  # 计算 A-Z 对应的移位
            mg = calculate_mg_for_group(group, g)
            mgs_for_shifts.append(round(mg, 3))
        mg_results.append(mgs_for_shifts)

    return mg_results

def decrypt_vigenere(cipher_text, key):
    """
    使用维吉尼亚密钥解密密文，并返回小写字母。
    :param cipher_text: 密文
    :param key: 密钥
    :return: 解密后的明文
    """
    # 去掉空白字符和非字母字符
    cipher_text = ''.join(c for c in cipher_text if c.isalpha())
    key_length = len(key)
    key_shifts = [ord(k) - ord('A') for k in key]  # 将密钥字母转换为对应的移位
    plaintext = []

    for i, c in enumerate(cipher_text):
        if c.isalpha():  # 仅处理字母
            shift = key_shifts[i % key_length]
            decrypted_char = chr((ord(c) - ord('A') - shift + 26) % 26 + ord('A'))
            plaintext.append(decrypted_char.lower())  # 转换为小写字母

    return ''.join(plaintext)

# 用户输入密文和分组设置
cipher_text = input("请输入密文: ").upper()
group_size = int(input("请输入分组大小: "))

# 计算并输出每组的 M_g 值
mg_values = calculate_mg_values(cipher_text, group_size)
for i, mgs in enumerate(mg_values):
    print(f"\n第 {i+1} 组 M_g 值:")
    for shift, mg in enumerate(mgs):
        print(f"移位 {chr(shift + ord('A'))}: {mg}")

# 询问用户密钥
while True:
    key_candidate = input("\n请输入推测出的密钥: ").upper()
    if len(key_candidate) != group_size:
        print("密钥长度不正确，请重新输入！")
    else:
        print(f"\n当前密钥为: {key_candidate}")
        confirm = input("此密钥正确吗？(Y/N): ").strip().upper()
        if confirm == "Y":
            # 使用密钥解密密文
            plaintext = decrypt_vigenere(cipher_text, key_candidate)
            print(f"\n解密完成！明文（小写，无空格）为:\n{plaintext}")
            break

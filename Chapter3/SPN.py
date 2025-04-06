import csv
from itertools import product

# 使用您提供的SPN.py中的加密函数，不做任何修改
S_BOX = {
    0x0: 0xE, 0x1: 0x4, 0x2: 0xD, 0x3: 0x1,
    0x4: 0x2, 0x5: 0xF, 0x6: 0xB, 0x7: 0x8,
    0x8: 0x3, 0x9: 0xA, 0xA: 0x6, 0xB: 0xC,
    0xC: 0x5, 0xD: 0x9, 0xE: 0x0, 0xF: 0x7
}

P_BOX = {
    1: 1, 2: 5, 3: 9, 4: 13,
    5: 2, 6: 6, 7: 10, 8: 14,
    9: 3, 10: 7, 11: 11, 12: 15,
    13: 4, 14: 8, 15: 12, 16: 16
}

def substitute(input_bits, s_box):
    """S盒替换函数"""
    output_bits = []
    for i in range(0, len(input_bits), 4):
        nibble = int(input_bits[i:i+4], 2)
        substituted = s_box[nibble]
        output_bits.append(f"{substituted:04b}")
    return ''.join(output_bits)

def permute(input_bits, p_box):
    """P盒置换函数"""
    output_bits = [''] * len(input_bits)
    for i in range(len(input_bits)):
        output_bits[p_box[i+1]-1] = input_bits[i]
    return ''.join(output_bits)

def key_schedule(key, Nr):
    """密钥调度函数 - 完全按照您提供的SPN.py实现"""
    keys = []
    for r in range(Nr + 1):
        start = 4 * r
        end = start + 16
        key_r = key[start:end]
        keys.append(key_r)
    return keys

def spn_encrypt(plaintext, key, Nr=4):
    """SPN加密函数 - 完全按照您提供的SPN.py实现"""
    keys = key_schedule(key, Nr)
    w = plaintext
    
    for r in range(Nr - 1):
        u = f"{int(w, 2) ^ int(keys[r], 2):016b}"
        v = substitute(u, S_BOX)
        w = permute(v, P_BOX)
    
    # 最后一轮
    u = f"{int(w, 2) ^ int(keys[Nr-1], 2):016b}"
    v = substitute(u, S_BOX)
    y = f"{int(v, 2) ^ int(keys[Nr], 2):016b}"
    return y

def generate_diff_pairs(x_diff, key, output_filename, sample_size=None):
    """
    生成满足x ⊕ x* = x_diff的明密文对
    :param x_diff: 输入差分，如"0000101100000000"
    :param key: 密钥，如"00111010100101001101011000111111"
    :param output_filename: 输出CSV文件名
    :param sample_size: 采样大小(为None时生成所有可能对)
    """
    # 移除空格并验证长度
    x_diff = x_diff.replace(" ", "")
    key = key.replace(" ", "")
    
    if len(x_diff) != 16:
        raise ValueError("输入差分必须是16位二进制")
    if len(key) != 32:
        raise ValueError("密钥必须是32位二进制")
    
    # 计算x_diff的整数值
    x_diff_int = int(x_diff, 2)
    
    with open(output_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['x', 'x*', 'y', 'y*', 'y_diff'])
        
        # 如果sample_size为None，生成所有可能对(注意这会很大)
        if sample_size is None:
            # 警告：这将生成65536个条目！
            print("警告：将生成所有65536个可能的明密文对...")
            x_range = range(2**16)
        else:
            # 随机采样
            import random
            x_range = random.sample(range(2**16), sample_size)
            print(f"生成{sample_size}个随机明密文对...")
        
        count = 0
        for x_int in x_range:
            x = f"{x_int:016b}"
            x_star_int = x_int ^ x_diff_int
            x_star = f"{x_star_int:016b}"
            
            y = spn_encrypt(x, key)
            y_star = spn_encrypt(x_star, key)
            y_diff = f"{int(y, 2) ^ int(y_star, 2):016b}"
            
            writer.writerow([x, x_star, y, y_star, y_diff])
            count += 1
            
            # 打印进度
            if count % 1000 == 0:
                print(f"已生成{count}对...")
    
    print(f"成功生成{count}对明密文对，保存到{output_filename}")

# 使用示例
if __name__ == "__main__":
    # 输入差分 (示例：0000 1011 0000 0000)
    x_diff = input("请输入16位输入差分(如 0000 1011 0000 0000): ").replace(" ", "")
    
    # 固定密钥 (您提供的密钥)
    key = "00111010100101001101011000111111"
    
    # 输出文件名
    output_filename = input("请输入输出CSV文件名(如 diff_pairs.csv): ")
    
    # 询问是否采样
    sample_option = input("生成所有可能对(输入A)或采样部分对(输入S)? [A/S]: ").upper()
    
    if sample_option == 'A':
        # 警告用户这将生成大量数据
        confirm = input("警告：这将生成65536个条目！确认吗? [Y/N]: ").upper()
        if confirm == 'Y':
            generate_diff_pairs(x_diff, key, output_filename)
        else:
            print("操作已取消")
    else:
        sample_size = int(input("请输入采样大小(如1000): "))
        generate_diff_pairs(x_diff, key, output_filename, sample_size)
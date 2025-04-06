import csv
import numpy as np

# S盒定义
S_BOX = {
    0x0: 0xE, 0x1: 0x4, 0x2: 0xD, 0x3: 0x1,
    0x4: 0x2, 0x5: 0xF, 0x6: 0xB, 0x7: 0x8,
    0x8: 0x3, 0x9: 0xA, 0xA: 0x6, 0xB: 0xC,
    0xC: 0x5, 0xD: 0x9, 0xE: 0x0, 0xF: 0x7
}

# 计算逆S盒
INV_S_BOX = {v: k for k, v in S_BOX.items()}

def partial_decrypt_and_verify(input_filename, s_box_inv, part1_idx=1, part2_idx=3, expected_diff1=6, expected_diff2=6):
    """
    部分解密与差分验证
    返回16x16的计数矩阵和总数据对数量
    """
    # 初始化计数矩阵 (16x16对应4位密钥)
    count_matrix = np.zeros((16, 16), dtype=int)
    total_pairs = 0
    
    # 将索引转换为对应的位置
    part1_start = part1_idx * 4
    part2_start = part2_idx * 4
    
    with open(input_filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            total_pairs += 1
            y = row['y']
            y_star = row['y*']
            
            # 提取需要处理的部分
            y_part1 = int(y[part1_start:part1_start+4], 2)
            y_part2 = int(y[part2_start:part2_start+4], 2)
            y_star_part1 = int(y_star[part1_start:part1_start+4], 2)
            y_star_part2 = int(y_star[part2_start:part2_start+4], 2)
            
            # 尝试所有可能的4位密钥组合
            for l1 in range(16):
                for l2 in range(16):
                    # 部分解密
                    v1 = l1 ^ y_part1
                    v2 = l2 ^ y_part2
                    u1 = s_box_inv[v1]
                    u2 = s_box_inv[v2]
                    
                    v1_star = l1 ^ y_star_part1
                    v2_star = l2 ^ y_star_part2
                    u1_star = s_box_inv[v1_star]
                    u2_star = s_box_inv[v2_star]
                    
                    # 计算差分
                    delta_u1 = u1 ^ u1_star
                    delta_u2 = u2 ^ u2_star
                    
                    # 检查是否符合预期差分
                    if delta_u1 == expected_diff1 and delta_u2 == expected_diff2:
                        count_matrix[l1, l2] += 1
    
    return count_matrix, total_pairs

# 使用示例
if __name__ == "__main__":
    # 用户输入
    print("差分密码攻击 - 部分密钥恢复")
    print("-" * 50)
    
    # 输入文件名
    input_filename = input("请输入密文对CSV文件名 (默认: filtered_pairs.csv): ").strip()
    if not input_filename:
        input_filename = "filtered_pairs.csv"
    
    # 选择要破解的密钥部分
    print("\n选择要破解的密钥部分 (0-3):")
    print("0 - 第一部分 (位 0-3)")
    print("1 - 第二部分 (位 4-7)")
    print("2 - 第三部分 (位 8-11)")
    print("3 - 第四部分 (位 12-15)")
    
    part1_idx = int(input("请选择第一个部分 (默认: 1): ").strip() or "1")
    part2_idx = int(input("请选择第二个部分 (默认: 3): ").strip() or "3")
    
    # 输入期望的差分值
    print("\n输入期望的差分值 (十六进制, 0-F):")
    expected_diff1 = int(input(f"第{part1_idx+1}部分期望差分 (默认: 6): ") or "6", 16)
    expected_diff2 = int(input(f"第{part2_idx+1}部分期望差分 (默认: 6): ") or "6", 16)
    
    # 执行部分解密和验证
    count_matrix, total_pairs = partial_decrypt_and_verify(
        input_filename, 
        INV_S_BOX, 
        part1_idx, 
        part2_idx, 
        expected_diff1, 
        expected_diff2
    )
    
    # 找出计数最高的密钥组合
    max_count = np.max(count_matrix)
    max_indices = np.where(count_matrix == max_count)
    best_keys = list(zip(max_indices[0], max_indices[1]))
    
    # 计算最高计数的频率
    frequency = max_count / total_pairs
    
    # 打印结果矩阵
    print("\n密钥组合计数矩阵:")
    print("   ", end="")
    for j in range(16):
        print(f"{j:3X}", end=" ")
    print()
    for i in range(16):
        print(f"{i:2X}:", end=" ")
        for j in range(16):
            print(f"{count_matrix[i,j]:3}", end=" ")
        print()
    
    # 打印最可能的密钥组合
    print(f"\n总数据对数量: {total_pairs}")
    print(f"最高计数: {max_count}")
    print(f"最高计数频率: {frequency:.6f} ({max_count}/{total_pairs})")
    print(f"最可能的密钥组合:")
    for l1, l2 in best_keys:
        print(f"L{part1_idx+1}={l1:X}, L{part2_idx+1}={l2:X}")
import numpy as np

S_BOX = {
    0x0: 0xE, 0x1: 0x4, 0x2: 0xD, 0x3: 0x1,
    0x4: 0x2, 0x5: 0xF, 0x6: 0xB, 0x7: 0x8,
    0x8: 0x3, 0x9: 0xA, 0xA: 0x6, 0xB: 0xC,
    0xC: 0x5, 0xD: 0x9, 0xE: 0x0, 0xF: 0x7
}

def calculate_diff_distribution_table(s_box):
    """
    计算S盒的差分分布表
    返回16x16的矩阵，行是输入差分，列是输出差分
    """
    # 初始化差分分布表
    diff_table = np.zeros((16, 16), dtype=int)
    
    # 遍历所有可能的输入对
    for x in range(16):
        for x_star in range(16):
            delta_x = x ^ x_star
            y = s_box[x]
            y_star = s_box[x_star]
            delta_y = y ^ y_star
            diff_table[delta_x, delta_y] += 1
    
    return diff_table

# 使用示例
if __name__ == "__main__":
    # 使用之前定义的S_BOX
    diff_table = calculate_diff_distribution_table(S_BOX)
    
    # 打印差分分布表
    print("S盒差分分布表:")
    print("    ", end="")
    for j in range(16):
        print(f"{j:3}", end=" ")
    print("\n" + "-"*67)
    
    for i in range(16):
        print(f"{i:2} |", end=" ")
        for j in range(16):
            print(f"{diff_table[i,j]:3}", end=" ")
        print()
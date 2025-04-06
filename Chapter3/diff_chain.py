import numpy as np

# 给定的S盒和P盒
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

# 添加一个辅助函数用于格式化二进制字符串
def format_binary(binary_str, group_size=4):
    """每group_size位添加一个空格"""
    if isinstance(binary_str, int):
        binary_str = format(binary_str, '016b')
    return ' '.join(binary_str[i:i+group_size] for i in range(0, len(binary_str), group_size))

# 计算差分分布表
def calculate_ddt(s_box):
    ddt = np.zeros((16, 16), dtype=int)
    for x in range(16):
        for delta_x in range(16):
            x_star = x ^ delta_x
            delta_y = s_box[x] ^ s_box[x_star]
            ddt[delta_x][delta_y] += 1
    return ddt

# 打印差分分布表
def print_ddt(ddt):
    print("\n差分分布表 (DDT):")
    print("ΔX\ΔY", end=" ")
    for j in range(16):
        print(f"{j:2X}", end=" ")
    print("\n" + "-"*50)
    for i in range(16):
        print(f"{i:2X} |", end=" ")
        for j in range(16):
            print(f"{ddt[i][j]:2}", end=" ")
        print()

# 应用P盒置换（处理16位差分）
def apply_p_box(delta_y_16bit, p_box):
    # 将16位差分转换为二进制字符串
    full_delta = format(delta_y_16bit, '016b')
    # 应用P盒置换
    permuted = ['0'] * 16
    for i in range(16):
        if full_delta[i] == '1':
            permuted[p_box[i+1]-1] = '1'
    permuted_str = ''.join(permuted)
    # 返回16位置换后的差分
    return int(permuted_str, 2)

# 将16位差分分成4个4位差分
def split_to_nibbles(delta_16bit):
    delta_bin = format(delta_16bit, '016b')
    nibbles = []
    for i in range(0, 16, 4):
        nibbles.append(int(delta_bin[i:i+4], 2))
    return nibbles

# 将4个4位差分合并为16位差分
def combine_nibbles(nibbles):
    result = 0
    for i, nibble in enumerate(nibbles):
        result |= (nibble << (12 - i*4))
    return result

# 计算16位差分通过S盒的概率
def calculate_s_box_probability(delta_x_16bit, delta_y_16bit, ddt):
    # 将16位差分分成4个4位差分
    delta_x_nibbles = split_to_nibbles(delta_x_16bit)
    delta_y_nibbles = split_to_nibbles(delta_y_16bit)
    
    # 计算每个S盒的概率
    probabilities = []
    for i in range(4):
        count = ddt[delta_x_nibbles[i]][delta_y_nibbles[i]]
        prob = count / 16
        probabilities.append(prob)
    
    # 返回总概率和每个S盒的计数
    total_prob = np.prod(probabilities)
    counts = [ddt[delta_x_nibbles[i]][delta_y_nibbles[i]] for i in range(4)]
    return total_prob, counts

# 生成差分链
def generate_differential_chain(initial_delta_x, ddt, s_box, p_box, rounds=3):
    print(f"\n生成差分链 (初始 ΔX = {format_binary(initial_delta_x)}):")
    print("-"*70)
    
    current_delta = initial_delta_x
    total_prob = 1.0
    chain = []
    
    for r in range(rounds):
        # 将16位差分分成4个4位差分
        delta_x_nibbles = split_to_nibbles(current_delta)
        
        # 计算每个S盒的可能输出差分
        possible_outputs = []
        for i in range(4):
            s_box_possible_outputs = []
            for y in range(16):
                if ddt[delta_x_nibbles[i]][y] > 0:
                    s_box_possible_outputs.append((y, ddt[delta_x_nibbles[i]][y]))
            possible_outputs.append(s_box_possible_outputs)
        
        # 检查是否所有S盒都有可能的输出差分
        if any(len(outputs) == 0 for outputs in possible_outputs):
            print(f"第{r+1}轮: 某个S盒无可能的输出差分，终止链")
            break
        
        # 选择每个S盒概率最高的输出差分
        best_delta_y_nibbles = []
        counts = []
        for outputs in possible_outputs:
            best_y, count = max(outputs, key=lambda x: x[1])
            best_delta_y_nibbles.append(best_y)
            counts.append(count)
        
        # 合并为16位输出差分
        best_delta_y = combine_nibbles(best_delta_y_nibbles)
        
        # 计算概率
        probs = [count / 16 for count in counts]
        round_prob = np.prod(probs)
        total_prob *= round_prob
        
        # 记录当前轮次的差分传播
        chain.append({
            'round': r+1,
            'delta_x': current_delta,
            'delta_y': best_delta_y,
            'counts': counts,
            'prob': round_prob
        })
        
        # 打印当前轮次信息
        print(f"第{r+1}轮:")
        print(f"  S盒输入差分 ΔX: {format_binary(current_delta)}")
        print(f"  S盒输出差分 ΔY: {format_binary(best_delta_y)}")
        
        # 改进的S盒出现次数输出格式
        s_box_counts = []
        for i, (nibble, count) in enumerate(zip(best_delta_y_nibbles, counts)):
            s_box_counts.append(f"y' = {nibble:X} : {count}次")
        print(f"  各S盒出现次数: {', '.join(s_box_counts)}")
        
        print(f"  概率: {round_prob:.6f}")
        
        # 通过P盒计算下一轮输入差分
        next_delta_x = apply_p_box(best_delta_y, p_box)
        print(f"  经P盒置换后下一轮ΔX: {format_binary(next_delta_x)}")
        print("-"*70)
        
        current_delta = next_delta_x
    
    print(f"总概率: {total_prob:.6f}")
    return chain

# 添加自动化分析函数
def automated_differential_analysis(s_box, p_box, rounds=3):
    print("\n自动化差分分析")
    print("="*80)
    print("分析所有可能的输入模式，每次只有一个4位部分包含非零值")
    print("="*80)
    
    # 计算差分分布表
    ddt = calculate_ddt(s_box)
    
    # 存储所有分析结果
    all_results = []
    
    # 测试所有可能的输入模式
    for part in range(4):  # 4个部分
        for value in range(1, 16):  # 每部分可以是1-15的值（排除0）
            # 构建16位差分，只有指定部分有值
            delta_x = [0, 0, 0, 0]
            delta_x[part] = value
            initial_delta_x = combine_nibbles(delta_x)
            
            print(f"\n测试输入差分: {format_binary(initial_delta_x)}")
            print(f"第{part+1}部分为{value:X}，其余部分为0")
            
            # 生成差分链
            chain = generate_differential_chain(initial_delta_x, ddt, s_box, p_box, rounds)
            
            # 记录结果
            if chain and len(chain) == rounds:  # 确保链完整
                final_output = None
                if chain:
                    final_output = chain[-1]['delta_y']
                    final_output_after_p = apply_p_box(final_output, p_box)
                
                result = {
                    'initial_delta_x': initial_delta_x,
                    'part': part + 1,
                    'value': value,
                    'final_output': final_output,
                    'final_output_after_p': final_output_after_p,
                    'total_prob': chain[-1]['prob'] if chain else 0
                }
                all_results.append(result)
    
    # 按总概率排序
    all_results.sort(key=lambda x: x['total_prob'], reverse=True)
    
    # 输出所有差分链的总结
    print("\n所有差分链总结:")
    print("="*100)
    print("初始差分 | 非零部分 | 值 | 最终输出 | P盒后输出 | 总概率")
    print("-"*100)
    
    for result in all_results:
        print(f"{format_binary(result['initial_delta_x'])} | 第{result['part']}部分 | {result['value']:X} | {format_binary(result['final_output'])} | {format_binary(result['final_output_after_p'])} | {result['total_prob']:.6f}")
    
    return all_results

# 主程序
if __name__ == "__main__":
    # 计算差分分布表
    ddt = calculate_ddt(S_BOX)
    print_ddt(ddt)
    
    # 提供选项
    print("\n请选择操作模式:")
    print("1. 手动输入差分")
    print("2. 自动分析所有可能的输入模式")
    
    choice = input("请输入选择 (1/2): ").strip()
    
    if choice == "1":
        # 用户输入初始差分
        while True:
            input_str = input("\n请输入初始差分ΔX (16位二进制，如0000 1101 0000 0000): ").strip().replace(" ", "")
            try:
                if len(input_str) != 16 or not all(bit in '01' for bit in input_str):
                    print("请输入16位二进制数！")
                    continue
                initial_delta_x = int(input_str, 2)
                break
            except ValueError:
                print("无效输入，请输入16位二进制数！")
        
        # 生成差分链
        chain = generate_differential_chain(initial_delta_x, ddt, S_BOX, P_BOX, rounds=3)
        
        # 输出差分链总结
        print("\n差分链总结:")
        print("轮次 | ΔX (输入) | ΔY (输出) | 概率")
        print("-"*70)
        for step in chain:
            print(f"{step['round']:2}   | {format_binary(step['delta_x'])} | {format_binary(step['delta_y'])} | {step['prob']:.6f}")
    
    elif choice == "2":
        # 自动分析
        rounds = int(input("请输入要分析的轮数 (默认3): ") or "3")
        all_results = automated_differential_analysis(S_BOX, P_BOX, rounds)
        
        # 找出概率最高的结果
        if all_results:
            best_result = max(all_results, key=lambda x: x['total_prob'])
            
            print("\n概率最高的差分链:")
            print("="*80)
            print(f"输入差分: {format_binary(best_result['initial_delta_x'])}")
            print(f"非零部分: 第{best_result['part']}部分，值为{best_result['value']:X}")
            print(f"最终输出: {format_binary(best_result['final_output'])}")
            print(f"P盒后输出: {format_binary(best_result['final_output_after_p'])}")
            print(f"总概率: {best_result['total_prob']:.6f}")
    
    else:
        print("无效选择！")
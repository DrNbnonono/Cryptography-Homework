from collections import Counter

def calculate_index_of_coincidence(text, group_size):
    """
    计算给定密文分组后的每组重合指数和平均重合指数。

    :param text: 输入密文字符串
    :param group_size: 分组大小
    :return: 每组重合指数及平均值
    """
    # 去掉空白字符，保持密文连贯
    text = text.replace(" ", "").replace("\n", "")
    
    # 分组，将密文划分为 group_size 个组
    groups = ['' for _ in range(group_size)]
    for i, char in enumerate(text):
        groups[i % group_size] += char

    # 计算各组的重合指数
    indices = []
    for group in groups:
        n = len(group)
        if n <= 1:
            indices.append(0.0)
            continue
        freqs = Counter(group)  # 统计每个字符的频率
        ic = sum(count * (count - 1) for count in freqs.values()) / (n * (n - 1))
        indices.append(ic)

    # 计算平均重合指数
    average_ic = sum(indices) / group_size if group_size > 0 else 0

    return indices, average_ic


# 用户输入密文和分组设置
cipher_text = input("请输入密文: ")
group_input = input("请输入分组大小或范围（如单个值'3'，或范围'1-5'）: ")

# 确定分组范围
if '-' in group_input:
    start, end = map(int, group_input.split('-'))
    group_sizes = range(start, end + 1)
else:
    group_sizes = [int(group_input)]

# 计算并输出结果
for group_size in group_sizes:
    indices, average_ic = calculate_index_of_coincidence(cipher_text, group_size)
    print(f"\n分组大小: {group_size}")
    print(f"各组重合指数: {[round(ic, 3) for ic in indices]}")
    print(f"平均重合指数: {round(average_ic, 3)}")

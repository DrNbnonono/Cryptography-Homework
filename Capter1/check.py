import re

def highlight_differences(str1, str2, chunk_size=50):
    """
    比较两字符串的差异并高亮不同的位置。
    :param str1: 第一个字符串
    :param str2: 第二个字符串
    :param chunk_size: 每次比较的字符串段长度，适用于处理长字符串
    """
    # 确保两段字符串长度一致
    if len(str1) != len(str2):
        print("两段文本长度不一致。找到分歧处：")
        min_len = min(len(str1), len(str2))
        for i, (char1, char2) in enumerate(zip(str1[:min_len], str2[:min_len])):
            if char1 != char2:
                print(f"不一致的位置：索引 {i}，'{str1[i]}' != '{str2[i]}'")
                return
        print(f"一致部分长度：{min_len}")
        print(f"剩余部分：\n- {str1[min_len:]}\n- {str2[min_len:]}")
        return
    
    # 分块处理长字符串
    for start in range(0, len(str1), chunk_size):
        chunk1 = str1[start:start + chunk_size]
        chunk2 = str2[start:start + chunk_size]
        
        # 高亮输出差异部分
        print("比较结果：")
        for c1, c2 in zip(chunk1, chunk2):
            if c1 == c2:
                print(c1, end="")  # 一致部分默认输出
            else:
                print(f"\033[31m{c2}\033[0m", end="")  # 不一致部分标红
        print("\n" + "-"*50)


def preprocess_input(text):
    """
    对输入字符串进行预处理，去除空格、引号等非字母字符。
    """
    return re.sub(r'[^A-Za-z]', '', text)


# 控制台输入
str1 = input("请输入第一个字符串：").strip()
str2 = input("请输入第二个字符串：").strip()

# 预处理输入（移除空格、引号等符号）
str1 = preprocess_input(str1)
str2 = preprocess_input(str2)

# 执行函数
highlight_differences(str1, str2)

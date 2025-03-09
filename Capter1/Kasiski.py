from collections import defaultdict
from math import gcd
from functools import reduce


def find_repeated_substrings_with_gcd(text, substring_length):
    """
    找到文本中所有指定长度的重复子串，计算每个子串的位置、到起点的距离和距离的最大公因数。
    """
    substrings = defaultdict(list)

    # 遍历文本，提取长度为 `substring_length` 的所有子串
    for i in range(len(text) - substring_length + 1):
        substring = text[i:i + substring_length]
        substrings[substring].append(i + 1)  # 位置从1开始，因此 `i + 1`

    # 筛选出重复出现的子串及其位置信息
    repeated_substrings = {k: v for k, v in substrings.items() if len(v) > 1}

    # 统计每个重复子串到起点的距离，并计算公因数
    results_with_gcd = {}
    for substring, positions in repeated_substrings.items():
        distances_to_start = [pos - 1 for pos in positions]  # 第一个位置减去0，到起点的距离
        distance_gcd = reduce(gcd, distances_to_start) if len(distances_to_start) > 1 else None
        results_with_gcd[substring] = {
            "positions": positions,
            "distances_to_start": distances_to_start,
            "gcd": distance_gcd,
        }

    return results_with_gcd


# 输入测试密文（保持密文连贯，无分段）
text = ("BNVSNSTHQCEELSSKKYERIFJKXUMBGYKAMQLJTYAVFBKVTDVBPVVRJYYLAOKYMPQSCGDLFSRLLPROYGESEB"
        "UUALRWXMMASAZLGLEDFJBZAVVPXWICGJXASCBYEHOSNMULKCEAHTQOKMFLEBKFXLRRFDTZXCIWBJSICBG"
        "AWDVYDHAVFJXZIBKCGJIWEAHTTOEWTUHKRQVVRGZBXYIREMMASCSPBNLHJMBLRFFJELHWEYLMISTFVVYF"
        "JCMHYUYRUFSFMGESIGRLWALSWMNUHSIMYYITCCQPZSICEHBCCMZFEGVJYOCDEMMPGHVAAUMELCMOEHVLT"
        "IPSUYILVGFLMVWDVYDBTHFRAYISYSGKVSUUHYHGGCKTMBLRX")

# 子串长度
substring_length = 3

# 执行函数
results = find_repeated_substrings_with_gcd(text, substring_length)

# 输出统计结果
for substring, data in results.items():
    print(f"子串: {substring}")
    print(f"位置: {data['positions']}")
    print(f"到起点的距离: {data['distances_to_start']}")
    print(f"距离的最大公因数: {data['gcd']}")
    print("-" * 30)

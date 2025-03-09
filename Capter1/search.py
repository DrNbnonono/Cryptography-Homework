from collections import Counter

def count_substrings(ciphertext, length, min_count):
    # 分割字符串为单个字符
    substring_counts = Counter()
    
    # 遍历字符串，提取指定长度的子串并计数
    for i in range(len(ciphertext) - length + 1):
        substring = ciphertext[i:i + length]
        substring_counts[substring] += 1
    
    # 筛选出现次数大于 min_count 的子串
    filtered_substrings = {k: v for k, v in substring_counts.items() if v > min_count}
    
    return filtered_substrings

# 示例密文
ciphertext = """BNVSNSTHQCEELSSKKYERIFJKXUMBGYKAMQLJTYAVFBKVT 
DVBPVVRJYYLAOKYMPQSCGDLFSRLLPROYGESEBUUALRWXM 
MASAZLGLEDFJBZAVVPXWICGJXASCBYEHOSNMULKCEAHTQ 
OKMFLEBKFXLRRFDTZXCIWBJSICBGAWDVYDHAVFJXZIBKC 
GJIWEAHTTOEWTUHKRQVVRGZBXYIREMMASCSPBNLHJMBLR 
FFJELHWEYLMISTFVVYFJCMHYUYRUFSFMGESIGRLWALSWM 
NUHSIMYYITCCQPZSICEHBCCMZFEGVJYOCDEMMPGHVAAUM 
ELCMOEHVLTIPSUYILVGFLMVWDVYDBTHFRAYISYSGKVSUU 
HYHGGCKTMBLRX"""

# 去掉空格和换行符
ciphertext = ciphertext.replace(" ", "").replace("\n", "")

# 调用函数，统计长度为2的字符组合，出现次数大于2
length = 3
min_count = 1
result = count_substrings(ciphertext, length, min_count)

# 输出结果
for substring, count in result.items():
    print(f"子串: {substring}, 出现次数: {count}")

from collections import Counter

# 给定的文字
text = "BNVSNSTHQCEELSSKKYERIFJKXUMBGYKAMQLJTYAVFBKVT DVBPVVRJYYLAOKYMPQSCGDLFSRLLPROYGESEBUUALRWXM MASAZLGLEDFJBZAVVPXWICGJXASCBYEHOSNMULKCEAHTQ OKMFLEBKFXLRRFDTZXCIWBJSICBGAWDVYDHAVFJXZIBKC GJIWEAHTTOEWTUHKRQVVRGZBXYIREMMASCSPBNLHJMBLR FFJELHWEYLMISTFVVYFJCMHYUYRUFSFMGESIGRLWALSWM NUHSIMYYITCCQPZSICEHBCCMZFEGVJYOCDEMMPGHVAAUM ELCMOEHVLTIPSUYILVGFLMVWDVYDBTHFRAYISYSGKVSUU HYHGGCKTMBLRX"

# 将所有字母转换为大写
text_upper = text.upper()

# 统计每个字母的出现次数
letter_counts = Counter(text_upper)

# 计算总字母数
total_letters = sum(letter_counts.values())

# 输出结果
for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    count = letter_counts.get(letter, 0)
    frequency = count / total_letters if total_letters > 0 else 0.0
    print(f"{letter}: {count} {frequency:.3f}")

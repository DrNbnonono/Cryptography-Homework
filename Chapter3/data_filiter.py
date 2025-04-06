import csv

def filter_pairs(input_filename, output_filename, parts_to_match):
    """
    过滤明密文对，保留指定部分相同的y和y*
    :param parts_to_match: 需要匹配的部分索引列表，从0开始
    """
    matched_count = 0
    
    with open(input_filename, 'r') as infile, open(output_filename, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.writer(outfile)
        writer.writerow(reader.fieldnames)
        
        for row in reader:
            y = row['y']
            y_star = row['y*']
            
            # 检查指定部分是否相同
            match = True
            for part in parts_to_match:
                start = part * 4
                end = start + 4
                if y[start:end] != y_star[start:end]:
                    match = False
                    break
            
            if match:
                writer.writerow([row['x'], row['x*'], y, y_star, row['y_diff']])
                matched_count += 1
    
    print(f"过滤后保留的数据个数: {matched_count}")
    return matched_count

# 使用示例
if __name__ == "__main__":
    # 过滤第1和第3部分相同的y和y* (索引从0开始)
    filter_pairs("second.csv", "filtered_pairs.csv", parts_to_match=[1, 3])
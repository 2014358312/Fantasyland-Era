import random

def generate_unique_colors(input_file, output_count=200):
    """
    从已有颜色文件中生成指定数量的不重复RGB颜色
    
    Args:
        input_file: 包含已有颜色的文本文件路径
        output_count: 需要生成的新颜色数量
    
    Returns:
        list: 新生成的颜色字符串列表
    """
    # 读取已有颜色并存储为集合（O(1)查找）
    existing_colors = set()
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:  # 跳过空行
                    existing_colors.add(line)
    except FileNotFoundError:
        print(f"警告: 文件 {input_file} 不存在，将从头开始生成")
    
    # 预计算总可能颜色数
    total_possible = 256 ** 3  # 16,777,216种颜色
    
    # 检查是否还有足够空间生成新颜色
    if len(existing_colors) + output_count > total_possible:
        available = total_possible - len(existing_colors)
        print(f"警告: 只剩 {available} 种可用颜色，将生成 {min(output_count, available)} 个")
        output_count = min(output_count, available)
    
    new_colors = []
    max_attempts = output_count * 100  # 防止无限循环的安全限制
    attempts = 0
    
    # 方法1: 随机生成并检查（适用于已有颜色较少的情况）
    if len(existing_colors) < total_possible * 0.1:  # 如果已有颜色少于10%
        while len(new_colors) < output_count and attempts < max_attempts:
            color_str = f"{random.randint(0, 255)};{random.randint(0, 255)};{random.randint(0, 255)}"
            if color_str not in existing_colors:
                new_colors.append(color_str)
                existing_colors.add(color_str)  # 防止新颜色之间重复
            attempts += 1
    else:
        # 方法2: 预生成所有可能颜色并过滤（适用于已有颜色较多的情况）
        print("已有颜色较多，使用优化算法...")
        
        # 将已有颜色转换为整数集合以提高比较效率
        existing_ints = set()
        for color_str in existing_colors:
            r, g, b = map(int, color_str.split(';'))
            existing_ints.add((r << 16) | (g << 8) | b)
        
        # 生成所有可能的颜色整数
        all_colors = set(range(total_possible))
        available_colors = all_colors - existing_ints
        
        # 随机选择所需数量的颜色
        selected_ints = random.sample(list(available_colors), output_count)
        
        # 转换回字符串格式
        for color_int in selected_ints:
            r = (color_int >> 16) & 255
            g = (color_int >> 8) & 255
            b = color_int & 255
            new_colors.append(f"{r};{g};{b}")
    
    if attempts >= max_attempts:
        print(f"警告: 达到最大尝试次数({max_attempts})，仅生成了{len(new_colors)}个新颜色")
    
    return new_colors

def main():
    input_filename = "新文件3.txt"  # 输入文件名
    output_filename = "新文件4.txt"      # 输出文件名
    start_prov_id = 14253
    
    # 生成200个新颜色
    new_colors = generate_unique_colors(input_filename, 200)
    
    prov_id = start_prov_id
    for i in range(len(new_colors)):
        new_colors[i] = str(prov_id) + ";" + new_colors[i] + ";land;false;plains;2"
        prov_id = prov_id + 1
    
    print(new_colors)

    # 保存到文件
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_colors))
    
    print(f"成功生成 {len(new_colors)} 个新颜色，已保存到 {output_filename}")
    
    # 可选：验证无重复
    if len(set(new_colors)) == len(new_colors):
        print("验证通过：所有新颜色均无重复")
    else:
        print("警告：检测到重复颜色")

if __name__ == "__main__":
    main()
import random

# 生成三个0-255之间的随机整数，并用分号连接
result = ';'.join(str(random.randint(0, 255)) for _ in range(3))
print(result)
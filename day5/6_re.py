import re

one = "msdfcfganhrrviwaer3234840984jnhvaj"

# 贪婪模式*：从开头匹配到结尾
pattern = re.compile('d.*r')
# findall（）方法是查找所有符合要求的结果
result = pattern.findall(one)
print(result)

pattern = re.compile('m.*h')
# match（）方法要来判断提供的字符串与正则表达式是否匹配成功（从头开始，匹配一次），
# 查看结果需要使用group（）方法或groups（）方法
result = pattern.match(one)
print(result.group())

# 非贪婪模式?：至多匹配一次
pattern = re.compile('d.?r')
result = pattern.findall(one)
print(result)

pattern = re.compile('m.?d')
result = pattern.match(one)
if result:
    print(result.group())

# =============================================
print("=" * 40)
two = "2.5.03,42,5"

pattern = re.compile('2\.5')
result = pattern.findall(two)
print(result)

pattern = re.compile('2.5')
result = pattern.findall(two)
print(result)

# ==============================================
print("=" * 40)
three = """
    mngdhauf dbnaajdf
    12345678 9999900f
    98765432 1000000F
"""
# . 可以匹配出换行之外的任意字符
pattern = re.compile("m.*f")
result = pattern.findall(three)
print(result)

# 如果想要跨行匹配，需要使用特殊修饰符
pattern = re.compile('m.*f', re.S)  # 可以匹配换行符
result = pattern.findall(three)
print(result)

# 正则是严格区分大小写的，如果要忽略大写需要添加修饰符
pattern = re.compile('m.*f', re.S | re.I)  # 可以匹配换行符，同时忽略大小写
result = pattern.findall(three)
print(result)

# ===================================================
print("=" * 40)
four = "abcd1234abcd"
pattern = re.compile('\d+')  # 匹配一个或多个数字

result = pattern.findall(four)
print(result)

# 从头开始，匹配一次
result = pattern.match(four)
if result:
    print(result)

# 从任意位置开式，匹配一次
result = pattern.search(four)
print(result)

# 替换字符串
result = pattern.sub("#", four)  # 将匹配到的数字替换为#
print(result)

# 拆分字符串
result = pattern.split(four)  # 按照匹配到的字符进行分割
print(result)

# =====================================================
print("=" * 40)
# 匹配汉字
five = "hello 你好 123"
pattern = re.compile("[\u4e00-\u9fa5]")
result = pattern.findall(five)
print(result)

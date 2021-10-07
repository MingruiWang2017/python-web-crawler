import requests

url = "http://www.baidu.com"
response = requests.get(url)

# content属性返回的类型是 bytes
data = response.content
print(response)
print(data)
str_data = data.decode('utf-8')
print(str_data)

# text属性是str类型，响应接收到unicode content后，
# 会根据HTTP header中的编码类型，转码为str
# 如果没有从header中获取到编码信息，需要设置一下response.encoding字段来解析
text_content = response.text
print(text_content)

url = "https://api.github.com/user"
res = requests.get(url)
# 返回json格式编码的相应内容
json_content = res.json()
print(json_content)

print(type(json_content))  # requests会将json自动转为dict
print(json_content["message"])

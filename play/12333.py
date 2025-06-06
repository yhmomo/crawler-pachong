file_path = "蘑菇屋：十封遗书曝光，泪崩全网林枫安暖.txt"  # 替换为你的文件路径
with open(file_path, "r", encoding='utf-8') as file:
    contents = file.readlines()

with open('1.txt', 'r') as f:
    sc = f.readlines()
# 删除指定内容
s = ''
with open(file_path, "w") as file:
    for content in contents:
        print(content)
        for sc1 in sc:
            print(sc1)
            if content == sc1:
                pass
            # s=''
            else:
                s = content
                file.write(s)
#     print(content)
#     if content in sc:
#         s=''
#     else:
#         s=content
# # target_content = "要删除的内容"  # 替换为你想要删除的内容
# # updated_content = content.replace(target_content, "")
#
# 重新写入文件

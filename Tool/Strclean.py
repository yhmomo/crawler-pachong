import re


def clean_string(input_string):
    # 检查输入是否为字符串
    if not isinstance(input_string, str):
        return input_string
    if 'http' in input_string:
        # 替换 \n 等特殊字符
        pattern = r'\n|\r|\t|\b|\f'
        cleaned_string = re.sub(pattern, '', input_string)
    else:
        cleaned_string = re.sub(r'[<>:"/\\|?*]', '', input_string)
        cleaned_string = re.sub(r'\s+', '', cleaned_string)
    return cleaned_string
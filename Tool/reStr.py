import re
from decimal import Decimal


def trim(text):
    """去除字符串中的空格和特殊字符"""
    if text is None:
        return None
    replacements = {
        "\r": "", "\t": "", "：": ":", " ": "", " ": "", "　": "",
        " ": "", "?": "", "&": "", "nbsp": "", " ": ""
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.strip()


# 中文数字映射
CN_NUM = {
    '零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
    '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
    '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5,
    '陆': 6, '柒': 7, '捌': 8, '玖': 9, '拾': 10,
    '佰': 100, '仟': 1000, '万': 10000, '亿': 100000000
}


def cn_to_arabic(cn_num):
    """将中文大写数字转换为阿拉伯数字"""
    total = 0
    unit = 1
    stack = []

    for char in reversed(cn_num):
        if char in CN_NUM:
            num = CN_NUM[char]
            if num >= 10:  # 单位
                if num > unit:
                    unit = num
                    if stack:
                        total += stack.pop()
                else:
                    unit *= num
            else:  # 数字
                stack.append(num * unit)

    if stack:
        total += stack.pop()

    return total


def get_money(text):
    """从文本中提取金额 - 增强版，支持中文大写数字"""
    # 关键词列表，用于优先提取
    keywords = [
        "预算金额", "项目金额", "金额", "报价", "投标报价", "成交金额",
        "采购预算", "总价", "合同金额", "中标金额", "控制价", "响应报价的上限（投响应报价总价）"
    ]

    # 尝试从包含关键词的行中提取
    for line in text.split('\n'):
        line = trim(line)
        if any(kw in line for kw in keywords):
            amount = extract_amount_from_line(line)
            if amount > 0:
                return amount

    # 如果没找到，再从整个文本中提取
    return extract_amount_from_line(text)


def extract_amount_from_line(line):
    """优化版金额提取，处理带逗号的数字"""
    # 模式1: 阿拉伯数字金额 (包含逗号分隔符)
    pattern1 = r'([\d,\.]+)\s*(?:万元|元|千元)'
    # 模式2: 中文大写金额
    pattern2 = r'([零一二三四五六七八九十百千万亿壹贰叁肆伍陆柒捌玖拾佰仟萬億]+)\s*[元万万千百十个位]?'
    # 模式3: 通用金额模式 (包含人民币符号)
    pattern3 = r'(?:人民币|￥)?\s*([\d,\.]+)\s*元'

    # 尝试匹配阿拉伯数字金额
    match1 = re.search(pattern1, line)
    if match1:
        amount_str = match1.group(1).replace(',', '')
        try:
            amount = Decimal(amount_str)
            if '万元' in line or '万' in line:
                amount *= Decimal('10000')
            elif '千元' in line or '千' in line:
                amount *= Decimal('1000')
            return amount
        except:
            pass

    # 尝试匹配中文大写金额
    match2 = re.search(pattern2, line)
    if match2:
        cn_num = match2.group(1)
        try:
            amount = cn_to_arabic(cn_num)
            if '万元' in line or '万' in line:
                amount *= 10000
            elif '千元' in line or '千' in line:
                amount *= 1000
            return Decimal(amount)
        except:
            pass

    # 尝试通用金额模式
    match3 = re.search(pattern3, line)
    if match3:
        amount_str = match3.group(1).replace(',', '')
        try:
            return Decimal(amount_str)
        except:
            pass

    # 最后尝试：简单数字匹配
    match4 = re.search(r'(\d+\.?\d*)', line)
    if match4:
        try:
            return Decimal(match4.group(1))
        except:
            pass

    return Decimal('0')

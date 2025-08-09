import csv

with open('A股公司供应商用年份.csv', 'r', newline='', encoding='utf-8') as infile, \
        open('data_unique.csv', 'w', newline='', encoding='utf-8') as outfile:
    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
    writer.writeheader()

    seen = set()
    for row in reader:
        key = tuple(row.values())  # 整行去重
        if key not in seen:
            seen.add(key)
            writer.writerow(row)

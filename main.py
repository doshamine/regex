import csv
from itertools import groupby
from pprint import pprint
import re

with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)


columns_num = len(contacts_list[0])
phone_pattern = r"(\+7|8)?\s*\(?(\d{3})\)?\s*-?(\d*)\s*-?(\d{2})\s*-?(\d{2})"
phone_template = r"+7(\2)\3-\4-\5"
ext_phone_pattern = phone_pattern + r"\s*\(?доб\.\s(\d+)\)?"
ext_phone_template = phone_template + r" доб.\6"

for row in contacts_list:
  columns = " ".join(row[:3]).split()
  while len(columns) < 3:
    columns += ['']
  row[:3] = columns

  row[5] = re.sub(phone_pattern, phone_template, row[5])
  row[5] = re.sub(ext_phone_pattern, ext_phone_template, row[5])


grouped_list = [list(group) for _, group in groupby(sorted(contacts_list), key=lambda x: x[:2])]
result_list = []
for group in grouped_list:
  combined_line = []
  for i in range(columns_num):
    combined_line.append('')
    for line in group:
      if line[i] != '':
        combined_line[i] = line[i]
  result_list.append(combined_line)


with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(result_list)

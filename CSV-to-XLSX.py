import csv
import re
import openpyxl

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def is_valid_phone_number(phone_number):
    phone_regex = r'^(?:\+?1[-. ]?)?(\d{3}|\(\d{3}\))[-. ]?\d{3}[-. ]?\d{4}$'
    return re.match(phone_regex, phone_number) is not None

def process_csv(input_file, output_file):
    with open(input_file, 'r') as infile:
        reader = csv.reader(infile)

        wb = openpyxl.Workbook()
        ws = wb.active

        header = next(reader)
        ws.append(header)

        for row in reader:
            if reader.line_num == 2:
                ws.append(row)
                continue

            col_b = row[1].strip()
            col_c = row[2].strip()
            col_d = row[3].strip()
            col_i = row[8].strip()
            col_j = row[9].strip()
            col_k = row[10].strip()

            if not col_b and not col_c:
                continue

            if col_d and not is_valid_email(col_d):
                row[3] = ''

            if col_i and not is_valid_phone_number(col_i):
                row[8] = ''

            if col_j and not is_valid_phone_number(col_j):
                row[9] = ''

            if col_k and not is_valid_phone_number(col_k):
                row[10] = ''

            if not (col_d or col_i or col_j or col_k):
                continue

            ws.append(row)

        wb.save(output_file)

input_file = 'test.csv'
output_file = 'output244544.xlsx'
process_csv(input_file, output_file)

import csv
import re
import streamlit as st
import openpyxl
from openpyxl.utils import get_column_letter
import os
import pandas as pd
import tempfile

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def is_valid_phone_number(phone_number):
    phone_regex = r'^(?:\+?1[-. ]?)?(\d{3}|\(\d{3}\))[-. ]?\d{3}[-. ]?\d{4}$'
    return re.match(phone_regex, phone_number) is not None

def process_file(input_file, output_file):
    file_ext = os.path.splitext(input_file)[-1].lower()

    if file_ext == '.csv':
        data = pd.read_csv(input_file)
    elif file_ext == '.xlsx':
        data = pd.read_excel(input_file, engine='openpyxl')
    else:
        raise ValueError(f"Unsupported file format: {file_ext}")

    # Process the data
    data = data.applymap(str).applymap(str.strip).replace('nan', '')

    # Remove rows with blank columns B and C
    data = data[(data.iloc[:, 1].notnull()) & (data.iloc[:, 2].notnull())]

    # Validate email format in column D
    email_col = data.columns[3]
    data.loc[data[email_col].notnull() & ~data[email_col].apply(is_valid_email), email_col] = ''

    # Validate phone number format in columns I, J, and K
    phone_columns = data.columns[8:11]
    for phone_col in phone_columns:
        invalid_phone_condition = data[phone_col].notnull() & ~data[phone_col].apply(is_valid_phone_number)
        data.loc[invalid_phone_condition, phone_col] = ''

    # Remove rows where columns D, I, J, and K are all blank
    valid_columns = [email_col] + list(phone_columns)
    data = data[data[valid_columns].apply(lambda row: any(row), axis=1)]

    # Save the output as an Excel file
    data.to_excel(output_file, index=False, engine='openpyxl')


output_file_name = st.text_input('What would you like the formatted filename to be?', value='output.xlsx')
input_file_obj = st.file_uploader('Select Unformatted CSV or Excel File', type=['csv', 'xlsx'])

if input_file_obj is not None:

    # Get the file extension
    file_ext = os.path.splitext(input_file_obj.name)[-1].lower()

    if file_ext not in ('.csv', '.xlsx'):
        st.error(f"Unsupported file format: {file_ext}. Please upload a CSV or XLSX file.")
    elif output_file_name:
        input_file_path = os.path.join(os.getcwd(), f'uploaded_file{file_ext}')
        output_file_path = os.path.join(os.getcwd(), output_file_name)

        with open(input_file_path, 'wb') as f:
            f.write(input_file_obj.getvalue())

    # Create a temporary file for the input file
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as input_file:
        input_file.write(input_file_obj.getvalue())

    # Create a temporary file for the output file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as output_file:
        process_file(input_file.name, output_file.name)



if st.button('Process File'):
    process_file(input_file_path, output_file_path)
    st.success('File processed successfully.')
    os.remove(input_file_path)

    # Download the processed file
    with open(output_file.name, 'rb') as f:
        file_content = f.read()

    download_button = st.download_button(
        label="Download Processed File",
        data=file_content,
        file_name=output_file_name,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    if download_button:
        os.remove(output_file.name)
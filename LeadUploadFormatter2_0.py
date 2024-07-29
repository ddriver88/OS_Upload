import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Check and install required packages
try:
    import streamlit as st
except ImportError:
    install('streamlit')
    import streamlit as st

try:
    import pandas as pd
except ImportError:
    install('pandas')
    import pandas as pd

try:
    from openpyxl import Workbook
except ImportError:
    install('openpyxl')
    from openpyxl import Workbook

import re
from io import BytesIO
import base64

def to_xlsx(dataframe):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    dataframe.to_excel(writer, index=False)
    writer.book.save(output)
    xlsx_data = output.getvalue()
    return xlsx_data

def is_valid_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) if email and not isinstance(email, float) else False

def is_valid_phone(phone):
    regex = r'^\+?(\d[\s-.\(\)]?){10,15}$'
    if phone and not isinstance(phone, float):
        match = re.match(regex, phone)
        return bool(match)
    return False

st.header('Club OS Mass Lead Upload Formatter')
st.markdown('This tool will remove invalid emails and phone numbers from the uploaded spreadsheet.\n - If that results in no contact information for a row in the spreadsheet then that row will be removed'
            '\n - The supplied file can be either CSV or XLSX'
            '\n - It is important to know that this program **ONLY** recognizes the [Mass Lead Upload](https://docs.google.com/spreadsheets/d/1TdDRkGD3GAybdcoGOje7oNIxfIOIIMME/edit#gid=320862359) spreadsheet. So you will have already needed to transpose the data provided by the client into this template.'

'\n### What this does:'
'\n- Accepts Location Name and populates it in Column A'
'\n- Allows User to specify output file name. **Be sure to not remove `.xlsx` as the extension**'
'\n- Verify that columns B and C are not blank. If they are, delete the row.'
'\n- If columns I, J, and K are not valid phone number formats delete the invalid data from the cell'
'\n- If columns D, I, J, and K are all blank, delete the row'
'\n- Ultimately this script should remove any invalid data in the specified cells while retaining data that is valid'
'\n### What this DOES NOT do:'
'\n- Remove phone numbers that start with `555`'
'\n- Validate that phone numbers are real. For example, `5128675309` will not be removed by this program'
'\n- Validate that emails are real. For example `TotallyFakeEmailLOL@gmail.com` will not be removed by this program'
'\n## ALWAYS DOUBLE CHECK THE OUTPUTTED FILE.'
'\nReach out to Daniel if you notice any errors.')

uploaded_file = st.file_uploader("Select Unformatted CSV or Excel File", type=['csv', 'xlsx'])

if uploaded_file:
    if uploaded_file.name.endswith('csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.dataframe(df.head())

    location_name = st.text_input("Enter Location Name:")
    output_file_name = st.text_input("Enter Output File Name:", "output.xlsx")
    removed_file_name = "removed_rows.xlsx"

    if location_name:
        df['Location Name'] = location_name

    df = df[df['First Name'].notnull() & df['Last Name'].notnull()]

    removed_rows = pd.DataFrame(columns=df.columns)  # Initialize DataFrame for removed rows

    valid_rows = []
    for index, row in df.iterrows():
        email = row['Email']
        home_phone = str(row['Home Phone']) if pd.notnull(row['Home Phone']) else None
        mobile_phone = str(row['Mobile Phone']) if pd.notnull(row['Mobile Phone']) else None
        work_phone = str(row['Work Phone']) if pd.notnull(row['Work Phone']) else None

        email_valid = is_valid_email(email)
        home_phone_valid = is_valid_phone(home_phone)
        mobile_phone_valid = is_valid_phone(mobile_phone)
        work_phone_valid = is_valid_phone(work_phone)

        if not email_valid:
            df.at[index, 'Email'] = None

        if not home_phone_valid:
            df.at[index, 'Home Phone'] = None

        if not mobile_phone_valid:
            df.at[index, 'Mobile Phone'] = None

        if not work_phone_valid:
            df.at[index, 'Work Phone'] = None

        if (email_valid or home_phone_valid or mobile_phone_valid or work_phone_valid):
            valid_rows.append(row)
        else:
            removed_rows = pd.concat([removed_rows, pd.DataFrame([row])], ignore_index=True)

    df = pd.DataFrame(valid_rows)

    if st.button("Process File"):
        xlsx_data = to_xlsx(df)
        removed_xlsx_data = to_xlsx(removed_rows)

        st.download_button(
            label="Download Processed File",
            data=xlsx_data,
            file_name=output_file_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        st.download_button(
            label="Download Removed Rows File",
            data=removed_xlsx_data,
            file_name=removed_file_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
import streamlit as st
import pandas as pd
import re
from io import BytesIO
import base64

def to_xlsx(dataframe):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    dataframe.to_excel(writer, index=False)
    writer.book.save(output)  # Update this line
    xlsx_data = output.getvalue()
    return xlsx_data


def download_link(data, filename, text):
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">{text}</a>'
    return href

def is_valid_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) if email and not isinstance(email, float) else False

def is_valid_phone(phone):
    regex = r'^\+?\d{1,4}[-.\s]?\(?\d{1,4}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$'
    if phone and not isinstance(phone, float):
        match = re.match(regex, phone)
        return match and len(re.findall(r'\d', phone)) >= 11
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

    if location_name:
        df['Location Name'] = location_name

    df = df[df['First Name'].notnull() & df['Last Name'].notnull()]

    for index, row in df.iterrows():
        email = row['Email']
        home_phone = str(row['Home Phone']) if pd.notnull(row['Home Phone']) else None
        mobile_phone = str(row['Mobile Phone']) if pd.notnull(row['Mobile Phone']) else None
        work_phone = str(row['Work Phone']) if pd.notnull(row['Work Phone']) else None

        if not is_valid_email(email):
            df.at[index, 'Email'] = None

        if not is_valid_phone(home_phone):
            df.at[index, 'Home Phone'] = None

        if not is_valid_phone(mobile_phone):
            df.at[index, 'Mobile Phone'] = None

        if not is_valid_phone(work_phone):
            df.at[index, 'Work Phone'] = None

    df = df[(df['Email'].notnull()) | (df['Home Phone'].notnull()) | (df['Mobile Phone'].notnull()) | (df['Work Phone'].notnull())]

    if st.button("Process File"):
        xlsx_data = to_xlsx(df)
        st.download_button(
            label="Download Processed File",
            data=xlsx_data,
            file_name=output_file_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",)

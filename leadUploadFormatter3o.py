import subprocess
import sys

def install(package):
    """Installs a given package via pip."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Check and install required packages (ideally use a requirements.txt in production)
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

# --------------------------------------------------
# Utility Functions
# --------------------------------------------------

@st.cache_data
def to_xlsx(dataframe: pd.DataFrame) -> bytes:
    """
    Converts a Pandas DataFrame to XLSX bytes using an in-memory buffer.
    Uses caching to avoid recomputation if the data hasn’t changed.
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        dataframe.to_excel(writer, index=False)
    return output.getvalue()

def is_valid_email(email: str) -> bool:
    """
    Checks if a given string is a valid email format.
    Returns False if email is None or not a string.
    """
    if not email or isinstance(email, float):
        return False
    regex = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(regex, email))

def is_valid_phone(phone: str) -> bool:
    """
    Checks if a given string is a valid phone format and filters out numbers
    starting with forbidden prefixes (800, 888, 555, or 111).
    """
    if not phone or isinstance(phone, float):
        return False

    # Basic format check: allows +, digits, spaces, dashes, parentheses, dots
    regex = r'^\+?[\d\s\-().]{10,15}$'
    if not re.match(regex, phone):
        return False

    # Remove non-digit characters
    digits = re.sub(r'\D', '', phone)

    # Optionally remove leading '1' if the number is longer than 10 digits
    if digits.startswith('1') and len(digits) > 10:
        digits = digits[1:]

    # Filter out numbers with forbidden prefixes
    forbidden_prefixes = ('800', '888', '555', '111')
    if any(digits.startswith(prefix) for prefix in forbidden_prefixes):
        return False

    return True

def clean_data(df: pd.DataFrame, location_name: str) -> (pd.DataFrame, pd.DataFrame):
    """
    Processes the DataFrame by:
      - Adding the Location Name (if provided)
      - Removing rows with missing 'First Name' or 'Last Name'
      - Converting phone columns to strings for uniform validation
      - Validating emails and phone numbers (invalid ones become None)
      - Removing rows that have no valid contact information
    Returns a tuple:
        (cleaned DataFrame, DataFrame of removed rows)
    """
    # Set Location Name if provided
    if location_name:
        df['Location Name'] = location_name

    # Verify required columns exist
    for col in ['First Name', 'Last Name']:
        if col not in df.columns:
            st.error(f"Missing required column: {col}")
            return None, None

    # Remove rows missing First or Last Name
    df = df[df['First Name'].notnull() & df['Last Name'].notnull()]

    # Process phone columns: ensure they are strings
    phone_cols = ['Home Phone', 'Mobile Phone', 'Work Phone']
    for col in phone_cols:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: str(x).strip() if pd.notnull(x) else None)

    # Validate email and phone columns
    if 'Email' in df.columns:
        df['Email'] = df['Email'].apply(lambda x: x if is_valid_email(x) else None)
    for col in phone_cols:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: x if is_valid_phone(x) else None)

    # Identify rows with at least one valid contact info (Email or any Phone)
    contact_cols = ['Email'] + phone_cols
    existing_contact_cols = [col for col in contact_cols if col in df.columns]
    valid_mask = df[existing_contact_cols].notnull().any(axis=1)
    removed_mask = ~valid_mask

    removed_rows = df[removed_mask].copy()
    cleaned_df = df[valid_mask].copy()

    return cleaned_df, removed_rows

# --------------------------------------------------
# Streamlit UI
# --------------------------------------------------

st.header('Club OS Mass Lead Upload Formatter')
st.markdown(
    """
    This tool will remove invalid emails and phone numbers from the uploaded spreadsheet.
    
    **What this does:**
    - Adds the specified Location Name to every row.
    - Ensures 'First Name' and 'Last Name' are present.
    - Validates Email and Phone fields (Home, Mobile, Work) and clears invalid entries.
    - Removes rows with no valid contact information.
    - Accepts CSV or Excel files (XLSX).
    
    **Important:**
    - Only spreadsheets matching the [Mass Lead Upload template](https://docs.google.com/spreadsheets/d/1TdDRkGD3GAybdcoGOje7oNIxfIOIIMME/edit#gid=320862359) are supported.
    - Always double-check the output files.
    """
)

uploaded_file = st.file_uploader("Select Unformatted CSV or Excel File", type=['csv', 'xlsx'])

if uploaded_file:
    try:
        if uploaded_file.name.lower().endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error reading file: {e}")
        df = None

    if df is not None:
        st.subheader("Preview of Uploaded Data")
        st.dataframe(df.head())

        # Inputs for location name and output filenames
        location_name = st.text_input("Enter Location Name:")
        output_file_name = st.text_input("Enter Output File Name:", "output.xlsx")
        removed_file_name = "removed_rows.xlsx"

        # Check if we already processed the file
        if "cleaned_df" not in st.session_state or "removed_rows" not in st.session_state:
            processed = False
        else:
            processed = True

        if st.button("Process File"):
            cleaned_df, removed_rows = clean_data(df, location_name)
            if cleaned_df is None:
                st.error("Processing halted due to errors in the uploaded file.")
            else:
                st.session_state.cleaned_df = cleaned_df
                st.session_state.removed_rows = removed_rows
                processed = True
                st.success(
                    f"Processing complete. {len(cleaned_df)} rows retained; {len(removed_rows)} rows removed."
                )

        # If already processed, display the download buttons
        if processed:
            # Retrieve processed data from session state
            cleaned_df = st.session_state.cleaned_df
            removed_rows = st.session_state.removed_rows

            # Convert DataFrames to XLSX bytes
            xlsx_cleaned = to_xlsx(cleaned_df)
            xlsx_removed = to_xlsx(removed_rows)

            st.download_button(
                label="Download Processed File",
                data=xlsx_cleaned,
                file_name=output_file_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            st.download_button(
                label="Download Removed Rows File",
                data=xlsx_removed,
                file_name=removed_file_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

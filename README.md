### There are three main files:
- CSV-to-CSV.py
- CSV-to-XLSX.py
- COS_LeadUploadFormatter_UI.py

The first two can only be run via the Command Line Interface (CLI) and may not be the best option. The first especially as the admin app does not accept CSV format for lead uploads.

**I would recommend using COS_LeadUploadFormatter_UI.py exclusively.**

## To Use COS_LeadUploadFormatter_UI.py
- Ensure you have [Python installed](https://www.python.org/downloads/)
- When installing, be sure to Add to Path 
  - ![image](https://user-images.githubusercontent.com/26580229/235505498-0fe01c61-1ea8-4a40-90da-3cd7624e44c8.png)
- [Download COS_LeadUploadFormatter_UI.py](https://github.com/ddriver88/OS_Upload/blob/095850f335c9fc6598fa5b7b183ae259a702b6b1/COS_LeadUploadFormatter_UI.py)
- [Open Command Prompt](https://www.howtogeek.com/235101/10-ways-to-open-the-command-prompt-in-windows-10/)
- Verify Python installation by typing `Python -v` without the quotes. The output should list the version of Python installed in step 1.
- Change directories in the command line to be the directory in which you downloaded COS_LeadUploadFormatter_UI.py
  - e.g. `cd C:\Users\{{USERNAME}}\Downloads`
- Once in the directory, install the dependencies by running the following:
  - pip install streamlit pandas re io base64
- When installation completes, the program is ready to run. Do so by typing `streamlit run .\COS_LeadUploadFormatter_UI.py`
  - Pro tip: `.\COS_LeadUploadFormatter_UI.py` is a lot to type. When executing the above step, you can press TAB to autocomplete. For example, `streamlit run .\COS` TAB should autocomplete the file name.

Once the command above is run it will open a Browser window with the UI. It is important to know that this program **ONLY** recognizes the [Mass Lead Upload](https://docs.google.com/spreadsheets/d/1TdDRkGD3GAybdcoGOje7oNIxfIOIIMME/edit#gid=320862359) spreadsheet. So you will have already needed to transpose the data provided by the client into this template.

### What this does:


## ALWAYS DOUBLE CHECK THE OUTPUTTED FILE.

Reach out to Daniel if you notice any errors.

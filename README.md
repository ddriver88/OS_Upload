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
- Download COS_LeadUploadFormatter_UI.py
- [Open Command Prompt](https://www.howtogeek.com/235101/10-ways-to-open-the-command-prompt-in-windows-10/)
- Verify Python installation by typing `Python -v` without the quotes. The output should list the version of Python installed in step 1.
- Change directories in the command line to be the directory in which you downloaded COS_LeadUploadFormatter_UI.py
  - e.g. `cd C:\Users\{{USERNAME}}\Downloads`
- Once in the directory, install the dependencies by running the following:
  - pip install streamlit pandas re io base64
- When installation completes, the program is ready to run. Do so by typing `streamlit run .\COS_LeadUploadFormatter_UI.py`
  - Pro tip: `.\COS_LeadUploadFormatter_UI.py` is a lot to type. When executing the above step, you can press TAB to autocomplete. For example, `streamlit run .\COS` TAB should autocomplete the file name.

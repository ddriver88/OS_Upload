### Latest Update:
- App now remembers state upon clicking download buttons. You no longer need to re-run the file to download the second output, e.g. removedRows.csv
- Checks if a given string is a valid phone format and filters out numbers
  starting with forbidden prefixes (800, 888, 555, or 111)

### There are three main files:
- CSV-to-CSV.py
- CSV-to-XLSX.py
- leadUploadFormatter3o.py

The first two can only be run via the Command Line Interface (CLI) and may not be the best option. The first especially as the admin app does not accept CSV format for lead uploads.

**I would recommend using leadUploadFormatter3o.py exclusively.**

## To Use COS_LeadUploadFormatter_UI.py
- Ensure you have [Python installed](https://www.python.org/downloads/release/python-380/)
- When installing, **BE SURE TO ADD TO PATH** - it's the second checkbox in the screenshot below:
- Click Customize Installation and be sure to install for all users.
  - ![image](https://user-images.githubusercontent.com/26580229/235505498-0fe01c61-1ea8-4a40-90da-3cd7624e44c8.png)
- [Download COS_LeadUploadFormatter_UI.py](https://github.com/ddriver88/OS_Upload/blob/095850f335c9fc6598fa5b7b183ae259a702b6b1/COS_LeadUploadFormatter_UI.py)

### MacOS / Linux
- Verify Python installation by typing `Python -v` without the quotes. The output should list the version of Python installed in step 1.
- `chmod +x setup.sh`
- run `./setup.sh` and all dependencies should be installed. If not, try the next step.
- Alternatively, install the dependencies manually by running the following:
  - `pip install streamlit pandas re io base64`
- When installation completes, the program is ready to run. Do so by typing `streamlit run .\LeadUploadFormatter2_0.py`
  - Pro tip: `.\leadUploadFormatter3o.py` is a lot to type. When executing the above step, you can press TAB to autocomplete. For example, `streamlit run .\Lead` TAB should autocomplete the file name.
 
### Windows
- Download [VS Code](https://code.visualstudio.com/download)
- File > Open > Folder > OS_Upload-main
- Click the LeadUploadFormatter2_0.py file to view it
- [Configure the virtual environment](https://code.visualstudio.com/docs/python/environments#_using-the-create-environment-command) (venv)
- Click the run/play button on the top right


Once the command above is run it will open a Browser window with the UI. It is important to know that this program **ONLY** recognizes the [Mass Lead Upload](https://docs.google.com/spreadsheets/d/1TdDRkGD3GAybdcoGOje7oNIxfIOIIMME/edit#gid=320862359) spreadsheet. So you will have already needed to transpose the data provided by the client into this template.

### What this does:
- Accepts Location Name and populates it in Column A
- Allows User to specify output file name. **Be sure to not remove `.xlsx` as the extension**
- Verify that columns B and C are not blank. If they are, delete the row.
- If columns I, J, and K are not valid phone number formats delete the invalid data from the cell
- If columns D, I, J, and K are all blank, delete the row
- Ultimately this script should remove any invalid data in the specified cells while retaining data that is valid
- Check out [prompt.txt](https://github.com/ddriver88/OS_Upload/blob/997de75428755cfba0498530894c756c0cd02c7b/prompt.txt) If you want to see exactly how this was created to work.

### What this DOES NOT do:
- Validate that phone numbers are real. For example, `5128675309` will not be removed by this program
- Validate that emails are real. For example `TotallyFakeEmailLOL@gmail.com` will not be removed by this program

## ALWAYS DOUBLE CHECK THE OUTPUTTED FILE.

Reach out to Daniel if you notice any errors.

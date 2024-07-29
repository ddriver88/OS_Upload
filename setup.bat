
REM Check if virtual environment directory exists
if not exist "venv" (
    REM Create virtual environment
    python -m venv venv
    echo Virtual environment created.
)

REM Activate virtual environment
call venv\Scripts\activate
echo Virtual environment activated.

REM Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt
echo Dependencies installed.

REM Run the main application
streamlit run LeadUploadFormatter2_0.py

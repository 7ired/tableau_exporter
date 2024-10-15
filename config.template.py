import os

# Tableau Server Credentials --- in order to get the personal token, go to My Account Settings in Tableau Server and create new token.
SERVER_URL = 'server'
TOKEN_NAME = 'token'
PERSONAL_ACCESS_TOKEN = 'tokenpass'
SITE_NAME = '' # 99% of cases we will leave empty

# Dashboard details
PROJECT_NAME = 'projectname'
WORKBOOK_NAME = 'workbookname'
VIEW_NAME = 'viewname'
FILTER_FIELD = 'filtername'

# Directory to save PDFs
OUTPUT_DIR = 'output_pdfs'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Filter values to loop over
FILTER_VALUES = ["value1", "value2", "value3"]  # Replace with actual filter values




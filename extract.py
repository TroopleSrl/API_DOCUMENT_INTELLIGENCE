
import pandas as pd
import docx
import html2text
from email.parser import BytesParser
from email import policy
import magic


def extract_text_from_file(file_path):
    mime = magic.Magic(mime=True)
    file_type = mime.from_file(file_path)

    if 'officedocument.wordprocessingml.document' in file_type:
        return extract_text_from_docx(file_path)
    elif 'vnd.openxmlformats-officedocument.spreadsheetml.sheet' in file_type:
        return get_xls_text(file_path)
    elif 'rfc822' in file_type:  # This is the MIME type for .eml files
        return extract_text_from_eml(file_path)
    else:
        return "Unsupported file type."

# Function to extract text from EML files
def extract_text_from_eml(file_path):
    with open(file_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)

    # Extracting the basic information
    email_subject = msg['subject']
    email_from = msg['from']
    email_to = msg['to']
    email_date = msg['date']

    # Extract the email body (handle both plain text and HTML)
    if msg.is_multipart():
        for part in msg.iter_parts():
            content_type = part.get_content_type()
            if content_type == 'text/plain':
                email_body = part.get_payload(decode=True).decode(part.get_content_charset())
            elif content_type == 'text/html':
                html_content = part.get_payload(decode=True).decode(part.get_content_charset())
                email_body = html2text.html2text(html_content)
    else:
        # If not multipart, the email is likely plain text
        email_body = msg.get_payload(decode=True).decode(msg.get_content_charset())

    # Formatting the extracted email information
    extracted_text = f"Subject: {email_subject}\nFrom: {email_from}\nTo: {email_to}\nDate: {email_date}\n\nBody:\n{email_body}"

    return extracted_text



def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs])


def get_xls_text(xls_file):
    file_text = {}  # Dictionary to hold text for each sheet in the current file
    xls = pd.ExcelFile(xls_file)
    # Loop through all sheets
    for sheet in xls.sheet_names:
        sheet_text = ''  # Accumulate text for the current sheet
        df = pd.read_excel(xls, sheet_name=sheet)
        # Format the data as described
        for index, row in df.iterrows():
            label = str(row[0])  # Assuming the first column is the label
            sheet_text += f"{label}:\n"
            for col_name, value in zip(df.columns[1:], row[1:]):  # Skip the first column
                sheet_text += f"    {col_name}: {value}\n"
            sheet_text += '\n'  # Add a blank line between entries for readability
        
        file_text[sheet] = sheet_text  # Store the formatted text for the sheet
    return file_text


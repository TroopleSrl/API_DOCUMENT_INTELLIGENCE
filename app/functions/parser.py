import io
import docx
import pandas as pd
import html2text
from email import policy
from email.parser import BytesParser

def extract_text_from_docx(file_content):
    doc = docx.Document(io.BytesIO(file_content))
    return '\n'.join([para.text for para in doc.paragraphs])

def extract_text_from_xlsx(file_content):
    text = {}  # Dictionary to hold text for all sheets
    xls = pd.ExcelFile(io.BytesIO(file_content))

    # Loop through all sheets
    for sheet in xls.sheet_names:
        sheet_text = ''  # Accumulate text for the current sheet
        df = pd.read_excel(xls, sheet_name=sheet)
        df = df.fillna('')  # Fill NaN values with empty strings

        # Format the data as described
        for index, row in df.iterrows():
            label = str(row.iloc[0])  # Assuming the first column is the label
            sheet_text += f"{label}:\n"
            for col_name, value in zip(df.columns[1:], row.iloc[1:]):  # Skip the first column
                sheet_text += f"    {col_name}: {value}\n"
            sheet_text += '\n'  # Add a blank line between entries for readability

        text[sheet] = sheet_text  # Store the formatted text for the sheet

    # Combine text from all sheets
    combined_text = ''
    for sheet_name, sheet_content in text.items():
        combined_text += f"Sheet: {sheet_name}\n{sheet_content}\n"
    return combined_text

def extract_text_from_eml(file_content):
    email_message = BytesParser(policy=policy.default).parsebytes(file_content)
    plain_message = ""

    if email_message.is_multipart():
        for part in email_message.walk():
            content_type = part.get_content_type()
            if content_type == 'text/plain':
                message = part.get_payload(decode=True)
                plain_message += message.decode('utf-8', 'ignore') if message else ""
            elif content_type == 'text/html':
                message = part.get_payload(decode=True)
                plain_message += html2text.html2text(message.decode('utf-8', 'ignore')) if message else ""
    else:
        content_type = email_message.get_content_type()
        if content_type == 'text/plain':
            message = email_message.get_payload(decode=True)
            plain_message += message.decode('utf-8', 'ignore') if message else ""
        elif content_type == 'text/html':
            message = email_message.get_payload(decode=True)
            plain_message += html2text.html2text(message.decode('utf-8', 'ignore')) if message else ""

    return plain_message

def extract_text_from_file(file_content, filename):
    if filename.lower().endswith('.docx'):
        return extract_text_from_docx(file_content)
    elif filename.lower().endswith('.xlsx'):
        return extract_text_from_xlsx(file_content)
    elif filename.lower().endswith('.eml'):
        return extract_text_from_eml(file_content)
    else:
        return "Unsupported format for local extraction."

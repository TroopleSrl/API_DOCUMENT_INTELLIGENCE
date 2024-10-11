

# import os
# import time
# import google.generativeai as genai


# genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# def upload_to_gemini(path, mime_type=None):
#   """Uploads the given file to Gemini.

#   See https://ai.google.dev/gemini-api/docs/prompting_with_media
#   """
#   file = genai.upload_file(path, mime_type=mime_type)
#   print(f"Uploaded file '{file.display_name}' as: {file.uri}")
#   return file

# def wait_for_files_active(files):
#   """Waits for the given files to be active.

#   Some files uploaded to the Gemini API need to be processed before they can be
#   used as prompt inputs. The status can be seen by querying the file's "state"
#   field.

#   This implementation uses a simple blocking polling loop. Production code
#   should probably employ a more sophisticated approach.
#   """
#   print("Waiting for file processing...")
#   for name in (file.name for file in files):
#     file = genai.get_file(name)
#     while file.state.name == "PROCESSING":
#       print(".", end="", flush=True)
#       time.sleep(10)
#       file = genai.get_file(name)
#     if file.state.name != "ACTIVE":
#       raise Exception(f"File {file.name} failed to process")
#   print("...all files ready")
#   print()

# # Create the model
# generation_config = {
#   "temperature": 0,
#   "top_p": 0.95,
#   "top_k": 40,
#   "max_output_tokens": 8192,
#   "response_mime_type": "text/plain",
# }

# model = genai.GenerativeModel(
#   model_name="gemini-1.5-pro",
#   generation_config=generation_config,
#   # safety_settings = Adjust safety settings
#   # See https://ai.google.dev/gemini-api/docs/safety-settings
#   system_instruction="You are an expert at OCR and extraction of all written text of images and scanned documents.\nYou always double check the names, numbers, dates, people, checkboxes, phones to be consistent accross the whole document. \nYou ensure the dates and names are logical. You MUST include all the text (every pages)",
# )

# start_time = time.time()

# # TODO Make these files available on the local file system
# # You may need to update the file paths
# files = [
#   upload_to_gemini("ocr.png", mime_type="image/png"),
# ]

# # Some files have a processing delay. Wait for them to be ready.
# wait_for_files_active(files)

# chat_session = model.start_chat(
#   history=[
#     {
#       "role": "user",
#       "parts": [
#         files[0],
#       ],
#     },
#   ]
# )

# response = chat_session.send_message("You're a perfect OCR scanner. Your task is to accurately analyse the images along with the possible documents and return a well-structured text of everything. Check twice the numbers, dates and names. Don't use prior knowledge. No mistakes allowed. Include everything in order.")
# end_time = time.time()
# total_time = end_time - start_time
# print(f"Total time: {total_time:.2f} seconds")
# print(response.text)
# print(response)

# import base64
# import requests
# import os

# # OpenAI API Key
# api_key = ""

# # Function to encode the image
# def encode_image(image_path):
#   with open(image_path, "rb") as image_file:
#     return base64.b64encode(image_file.read()).decode('utf-8')

# image_path = "ocr.jpg"  # Replace with your image path

# # Getting the base64 string
# base64_image = encode_image(image_path)

# headers = {
#     "Content-Type": "application/json",
#     "Authorization": f"Bearer {api_key}"
# }

# # Payload with the image and text, directly passing the base64 image in the content
# payload = {
#     "model": "gpt-4o-mini",  # Ensure this model supports image input
#     "messages": [
#         {
#             "role": "user",
#             "content": [
#                 {
#                     "type": "text",
#                     "text": "You're a perfect OCR scanner. Your task is to accurately analyze the images along with the possible documents and return a well-structured text of everything. Check twice the numbers, dates, and names. Don't use prior knowledge. No mistakes allowed. Include everything in order."
#                 },
#                 {
#                     "type": "image_url",
#                     "image_url": {
#                         "url": f"data:image/jpeg;base64,{base64_image}",
#                         "detail": "high"
#                     }
#                 }
#             ]
#         }
#     ],
#     "max_tokens": 300
# }

# # Sending the request
# response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

# # Print the response
# print(response.json())


# emails

# import email
# from email import policy
# from email.parser import BytesParser
# import html2text
# import docx
# import pandas as pd


# filepath = 'Project\Data\Your GrabPay Wallet Statement for 15 Feb 2022.eml'

# with open(filepath) as email_file:
#     email_message = email.message_from_file(email_file)
  
# if email_message.is_multipart():
#     for part in email_message.walk():
#         #print(part.is_multipart())
#         #print(part.get_content_type())
#         #print()
#         message = str(part.get_payload(decode=True))
#         plain_message = html2text.html2text(message)
#         print(plain_message)
#         print()


# ## docx

# def getText(filename):
#     doc = docx.Document(filename)
#     fullText = [para.text for para in doc.paragraphs]
#     return '\n'.join(fullText)

# ## xlsx

import pandas as pd

def get_xls_text(xls_files):
    text = {}  # Dictionary to hold text for all files and sheets
    for xls_file in xls_files:
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
        text[xls_file] = file_text  # Store the text for each file
    return text

xls_files = ['produceSales.xlsx']
xls_text = get_xls_text(xls_files)
print(xls_text)
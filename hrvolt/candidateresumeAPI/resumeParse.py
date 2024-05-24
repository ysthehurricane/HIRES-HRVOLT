# import langchain
# from langchain.document_loaders import UnstructuredPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# import pytesseract
# import re
# import os
# import fitz

# os.environ["PATH"] += os.pathsep + r"E:\HRVOLT\Hrvolt_v1\hrvolt_api_new_latest\poppler-22.04.0\Library\bin"
# os.environ["PATH"] += os.pathsep + r'C:\Program Files\Tesseract-OCR'

# tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# try:
#     pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
# except Exception as e:
#     print(e)



# def getBasicinformation(filepath):

#     current_directory = os.path.dirname(os.path.abspath(__file__))

#     basepath = "/".join(current_directory.split("\\")[:-1])

#     allfullpath = basepath + "/" + filepath

#     with fitz.open(allfullpath) as pdf_document:
#         page_texts = []
#         hyperlinks = {'Facebook': [], 'GitHub': [], 'Stack Overflow': [], 'LinkedIn': [], 'Medium': [], 'Other Links': []}
#         for page_num in range(pdf_document.page_count):
#             page = pdf_document[page_num]
#             for link in page.get_links():
#                 uri = link.get('uri')
#                 if uri:
#                     if re.search(r'(?:www\.)?facebook\.com', uri):
#                         hyperlinks['Facebook'].append(uri)
#                     elif re.search(r'(?:www\.)?github\.com', uri):
#                         hyperlinks['GitHub'].append(uri)
#                     elif re.search(r'(?:www\.)?stackoverflow\.com', uri):
#                         hyperlinks['Stack Overflow'].append(uri)
#                     elif re.search(r'(?:www\.)?linkedin\.com', uri):
#                         hyperlinks['LinkedIn'].append(uri)
#                     elif re.search(r'(?:www\.)?medium\.com', uri):
#                         hyperlinks['Medium'].append(uri)
#                     else:
#                         hyperlinks['Other Links'].append(uri)


#     # email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
#     # phone_pattern = r'\b(?:\+\d{1,2}\s?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
#     # name_pattern = r'\b([A-Za-z]+)\s+([A-Za-z]+)\b'
#     # linkedin_pattern = r'(http[s]?://(?:www\.)?linkedin\.com)'
#     # github_pattern = r'(http[s]?://(?:www\.)?github\.com)'
#     # stack_pattern = r'(http[s]?://(?:www\.)?stackoverflow\.com)'
#     # facebook_pattern = r'(http[s]?://(?:www\.)?facebook\.com)'
#     # medium_pattern = r'(http[s]?://(?:www\.)?medium\.com)'
#     # social_media_pattern = r'(http[s]?://(?:www\.)?\S+\.com)'
#     # gender_pattern = r'\b(?:male|female)\b'

#     email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
#     phone_pattern = r'\b(?:\+\d{1,2}\s?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
#     name_pattern = r'\b([A-Za-z]+)\s+([A-Za-z]+)\b'
#     linkedin_pattern = r'(http[s]?://(?:www\.)?linkedin\.com/(?:in|pub|company)/([^/]+))'
#     github_pattern = r'(http[s]?://(?:www\.)?github\.com/([^/]+))'
#     stack_pattern = r'(http[s]?://(?:www\.)?stackoverflow\.com/users/(\d+)(?:/[^/\s]+)?)'
#     facebook_pattern = r'(http[s]?://(?:www\.)?facebook\.com/(?:profile\.php\?id=)?([a-zA-Z0-9.-]+))'
#     medium_pattern = r'(http[s]?://(?:www\.)?medium\.com/@([a-zA-Z0-9._-]+))'
#     social_media_pattern = r'(?:https?://(?:www\.)?\S+\.com(?:/\S*)?|www\.\S+\.\S+)'

#     pdf_loader = UnstructuredPDFLoader(allfullpath)
#     pdf_pages = pdf_loader.load_and_split()

#     text_per_page = []

#     text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size = 1024,
#     chunk_overlap = 64
#     )

#     for i in range(0, len(pdf_pages)):

#         text_chunks = text_splitter.split_text(pdf_pages[i].page_content)
#         page_text = ''.join(text_chunks)
#         text_per_page.append(page_text)

#     fullText = ' '.join(text_per_page)

#     emailExtraction = re.findall(email_pattern, fullText)
#     phoneExtraction = re.findall(phone_pattern, fullText)
#     linkedin = re.findall(linkedin_pattern, fullText)
#     github = re.findall(github_pattern,fullText)
#     stack = re.findall(stack_pattern, fullText)
#     facebook = re.findall(facebook_pattern, fullText)
#     medium = re.findall(medium_pattern,fullText)


#     extracted_links = linkedin + stack + facebook + github + medium
#     social_media_links = list(set(re.findall(social_media_pattern, fullText)) - set(extracted_links))

#     res = {
#             'Phone_numbers': phoneExtraction,
#             'Email': emailExtraction,
#             'linkedin_link': linkedin  + hyperlinks['LinkedIn'],
#             'github_link': github  + hyperlinks['GitHub'],
#             'stack_link': stack  + hyperlinks['Stack Overflow'],
#             'facebook_link': facebook  + hyperlinks['Facebook'],
#             'medium_link': medium  + hyperlinks['Medium'],

#             } 

#     return res
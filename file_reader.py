from abc import ABC, abstractmethod
import PyPDF2
import re
import csv
import uuid
import pdfplumber
from utils.cleaner import TextCleaner
#from cleaner import TextCleaner

class FileParser(ABC):

    @abstractmethod
    def exctract_text(self):
        pass
    
    @abstractmethod
    def get_parsed_data(self):
        pass

class PdfParser(FileParser):

    cleaner = TextCleaner()

    def __init__(self, pages, path):
        super().__init__()
        self.pages = pages
        self.path = path
        self.cleaner = TextCleaner()
    
    def exctract_text(self):
        pdf = pdfplumber.open(self.path)
        pages_contents = []
        for i in self.pages:
            page = pdf.pages[i - 1]
            text = page.extract_text()
            pages_contents.append(text)
        return pages_contents

    def get_parsed_data(self):
        c = TextCleaner()
        extracted_texts = self.exctract_text()
        parsed_data = []
        for text in extracted_texts:
            text = text.split('\n')
            company_info_ind = [i for i in range(len(text)) if 'Company' in text[i]][0]
            supervisor_ind = [i for i in range(len(text)) if 'Academic Supervisor' in text[i]][0]
            title = c.text_cleaning(" ".join([text[i] for i in range(0, company_info_ind)])).lower()
            supervisor = " ".join(text[supervisor_ind].split()[2:])
            company = text[company_info_ind].split()[1]
            abstract = c.text_cleaning(" ".join([text[i] for i in range(supervisor_ind + 1, len(text) - 1)])).lower()
            if abstract[-1] == ' ':
                abstract = abstract[0:len(abstract) - 1]
            parsed_data.append({'title': title, 'abstract': abstract + title, 'supervisor' : supervisor, 'company': company})
        return parsed_data 

class WebPageParser(FileParser):

    def exctract_text(self):
        pass

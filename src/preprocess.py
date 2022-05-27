from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize
import re

import json
import os

def remove_html(text):
    bs = BeautifulSoup(text, "html.parser")
    return ' ' + bs.get_text() + ' '
 
def keep_only_letters(text):
    text=re.sub(r'[^a-zA-Z\s]','',text)
    return text
 
def convert_to_lowercase(text):
    return text.lower()

def preprocess_data():
	raw_data_path = '../data/raw/'
	for file_name in [file for file in os.listdir(raw_data_path) if file.endswith('.json')]:
		with open(raw_data_path + file_name) as json_file:
			data = json.load(json_file)
			print(data['text'])


def main():
	preprocess_data()

if __name__ == '__main__':
	main()
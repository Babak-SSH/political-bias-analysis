from nltk.tokenize import RegexpTokenizer, WhitespaceTokenizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import stem

from bs4 import BeautifulSoup
import re
import unidecode

import json
import os


w_tokenizer = WhitespaceTokenizer()
lemmatizer = stem.WordNetLemmatizer()

english_stop_words = stopwords.words('english')
english_stop_words = set(english_stop_words)

def remove_html(text):
	# remove html tags
    bs = BeautifulSoup(text, "html.parser")
    return ' ' + bs.get_text() + ' '
 
def keep_only_letters(text):
	# remove strings that have both number and letter
	text = re.sub(r'\w*\d\w*', '', text).strip()
	# remove numbers only
	text=re.sub(r'[^a-zA-Z\s]','',text)
	return text
 
def convert_to_lowercase(text):
	# convert to lowercase
    return text.lower()

def remove_misc(text):
	# replace newline and tab
	text = text.replace('\\n', ' ').replace('\n', ' ').replace('\t',' ').replace('\\', ' ')
	return text

def remove_links(text):
    # Removing all the occurrences of links that starts with https
    text = re.sub(r'http\S+', '', text)
    # Remove all the occurrences of text that ends with .com
    text = re.sub(r"\ [A-Za-z]*\.com", " ", text)
    return text

def accented_characters_removal(text):
	# convert accented characters to letters machine can understand
	text = unidecode.unidecode(text)
	return text

CONTRACTION_MAP = {
"ain't": "is not",
"aren't": "are not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he would",
"he'd've": "he would have",
"he'll": "he will",
"he'll've": "he he will have",
"he's": "he is",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how is",
"i'd": "i would",
"i'd've": "i would have",
"i'll": "i will",
"i'll've": "i will have",
"i'm": "i am",
"i've": "i have",
"isn't": "is not",
"it'd": "it would",
"it'd've": "it would have",
"it'll": "it will",
"it'll've": "it will have",
"it's": "it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she would",
"she'd've": "she would have",
"she'll": "she will",
"she'll've": "she will have",
"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so as",
"that'd": "that would",
"that'd've": "that would have",
"that's": "that is",
"there'd": "there would",
"there'd've": "there would have",
"there's": "there is",
"they'd": "they would",
"they'd've": "they would have",
"they'll": "they will",
"they'll've": "they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we would",
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what will",
"what'll've": "what will have",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"when's": "when is",
"when've": "when have",
"where'd": "where did",
"where's": "where is",
"where've": "where have",
"who'll": "who will",
"who'll've": "who will have",
"who's": "who is",
"who've": "who have",
"why's": "why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you would",
"you'd've": "you would have",
"you'll": "you will",
"you'll've": "you will have",
"you're": "you are",
"you've": "you have",
}
def expand_contractions(text, contraction_mapping =  CONTRACTION_MAP):
    # Tokenizing text into tokens.
    list_Of_tokens = text.split(' ')

    for Word in list_Of_tokens: 
         if Word in CONTRACTION_MAP: 
                # If Word is present in both dictionary & list_Of_tokens, replace that word with the key value.
                list_Of_tokens = [item.replace(Word, CONTRACTION_MAP[Word]) for item in list_Of_tokens]
                
    String_Of_tokens = ' '.join(str(e) for e in list_Of_tokens) 
    return String_Of_tokens

def removing_special_characters(text):
    # The formatted text after removing not necessary punctuations.
    Formatted_Text = re.sub(r"[^a-zA-Z0-9:$,'%.?!]+", ' ', text) 
    return Formatted_Text

def remove_stopwords(text):
	text = repr(text)
	# Text without stopwords
	No_StopWords = [word for word in word_tokenize(text) if word.lower() not in english_stop_words ]
	# Convert list of tokens_without_stopwords to String type.
	words_string = ' '.join(No_StopWords)    
	return words_string

def lemmatization(text):
	# Converting words to their root forms
	lemma = [lemmatizer.lemmatize(w,'v') for w in w_tokenizer.tokenize(text)]
	return lemma

def clean_data():
	raw_data_path = '../data/raw/'
	for file_name in [file for file in os.listdir(raw_data_path) if file.endswith('.json')]:
		data = None
		with open(raw_data_path + file_name) as json_file:
			data = json.load(json_file)

		article_text = data['text']

		if (data != None and article_text != "" and article_text != None):
			article_text = expand_contractions(article_text)
			article_text = remove_html(article_text)
			article_text = remove_links(article_text)
			article_text = removing_special_characters(article_text)
			article_text = keep_only_letters(article_text)
			article_text = convert_to_lowercase(article_text)
			article_text = remove_misc(article_text)
			article_text = remove_stopwords(article_text)

			with open('../data/clean/article'+str(data['index'])+'.json', 'w') as f:
				json.dump({'index': data['index'], 'text':article_text, 'label': data['label']}, f, 
							separators=(',', ':'), ensure_ascii=False, indent=4)

def tokenize_data():
	raw_data_path = '../data/clean/'
	for file_name in [file for file in os.listdir(raw_data_path) if file.endswith('.json')]:
		data = None
		with open(raw_data_path + file_name) as json_file:
			data = json.load(json_file)

		article_text = data['text']

		if (data != None and article_text != "" and article_text != None):
			article_text = lemmatization(article_text[1:-1])

		with open('../data/tokens/article'+str(data['index'])+'.json', 'w') as f:
				json.dump({'index': data['index'], 'text':article_text, 'label': data['label']}, f, 
							separators=(',', ':'), ensure_ascii=False, indent=4)

def main():
	clean_data()
	tokenize_data()

if __name__ == '__main__':
	main()
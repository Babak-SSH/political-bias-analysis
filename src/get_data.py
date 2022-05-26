from tkinter.ttk import Labelframe
from newsplease import NewsPlease
import json
import pandas as pd


def get_news():
	articles = []

	label_urls = pd.read_csv('../urls/labels.csv')

	print("starting download....")

	for index, row in label_urls.iterrows():
		try:
			news = NewsPlease.from_url(row['url'])
		except:
			print("{}/{} -> failed".format(row['index'], label_urls['url'].size))
			continue

		print("{}/{} -> title: {}".format(row['index'], label_urls['url'].size, news.title))

		with open('../data/raw/article'+str(row['index'])+'.json', 'w') as f:
			json.dump({'index': row['index'], 'text': news.maintext, 'label': row['label']}, f, ensure_ascii=False, indent=4)

def main():
	get_news()
	
if __name__ == "__main__":
	main()
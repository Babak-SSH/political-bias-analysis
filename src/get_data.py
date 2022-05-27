from cProfile import label
from email import parser
from tkinter.ttk import Labelframe
from newsplease import NewsPlease

import json
import pandas as pd

import argparse


import os, shutil


def clean_raw_dir():
	# clean and reset raw data dir
	folder = '../data/raw/'
	for filename in os.listdir(folder):
		file_path = os.path.join(folder, filename)
		try:
			if os.path.isfile(file_path) or os.path.islink(file_path):
				os.unlink(file_path)
			elif os.path.isdir(file_path):
				shutil.rmtree(file_path)
		except Exception as e:
			print('Failed to delete %s. Reason: %s' % (file_path, e))

def show_result():
	# showing an overview of results.
	df = pd.read_csv('../data/raw/raw_data_result.csv')
	print("=========================================================================================")
	print(df.to_string(index=False))
	print("=========================================================================================")

def get_news(count):
	label_counts = [0, 0, 0]
	limit = [0, 0, 0]

	# reading urls with thier corresponding labels.
	label_urls = pd.read_csv('../urls/labels.csv')
	url_count = label_urls['url'].size

	# starting to download the articles.
	print("getting articles....")

	for index, row in label_urls.iterrows():
		if (count > 0):
			if(sum(limit) >= count):
				break
			limit[int(row['label']-1)] += 1
			if (row['label'] == 1):
				count -= 1
			elif (limit[int(row['label']-1)] > count/2):
				limit[int(row['label']-1)] -= 1
				continue

		try:
			news = NewsPlease.from_url(row['url'])
		except:
			# if the article is unavailable or our request is rejected we will print error and continue.
			print("{}/{} -> failed".format(row['index'], url_count))
			continue

		print("{}/{} -> title: {}".format(row['index'], url_count, news.title))
		label_counts[int(row['label'])-1] += 1
	
		# write each article in a json file with its label.
		with open('../data/raw/article'+str(row['index'])+'.json', 'w') as f:
			json.dump({'index': row['index'], 'text': news.maintext, 'label': row['label']}, f, ensure_ascii=False, indent=4)

	print("\n\nsuccessfully downloaded {} out of {} articles.\n".format(sum(label_counts), url_count))

	result = pd.DataFrame([[sum(label_counts)] + label_counts], columns=['Total', 'Natural', 'Democrat', 'Republicant'])
	result.to_csv('../data/raw/raw_data_result.csv', index=False)

def main():
	usage = "getting data from urls in url/labels.csv options: -c for cleaning raw data dir, -n for number of datas to download"
	parser = parser = argparse.ArgumentParser(description=usage)
	group = parser.add_mutually_exclusive_group()
	group.add_argument("-n", "--number", type=int, default=0)
	group.add_argument("-c", "--clean", action="store_true", default=False)

	args = parser.parse_args()

	if (args.clean):
		clean_raw_dir()

	get_news(args.number)
	show_result()
	
if __name__ == "__main__":
	main()
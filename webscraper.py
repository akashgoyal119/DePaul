from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By 
import sys
import requests
from urllib.request import urlopen
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import time
import csv

results = 9999

#USE SELENIUM TO GET ALL THE website infos...
driver = webdriver.Chrome()
driver.get('https://www.zenodo.org/search?page=1&size='+str(results))
element = WebDriverWait(driver,60).until(EC.presence_of_element_located((By.TAG_NAME,"h4")))
print ('got here')

innerHTML = driver.execute_script("return document.body.innerHTML")
soup = BeautifulSoup(innerHTML,'html.parser')

all_urls = soup.find_all('h4')
if len(all_urls) == results:
	print ('correct quantity')
else:
	print ('incorrect number of results')
	driver.close()
	sys.exit()

url_list = []
for url in all_urls:
	children = url.findChildren()[0]
	url_list.append('https://www.zenodo.org'+children.get('href'))#+'#BS')

driver.quit() #have to use driver.quit instead of driver.close for some 
#reason.... 

with open('Andy-wordscraper.txt','w') as f_out:
	csv_writer = csv.writer(f_out,delimiter=',')
	for i,url in enumerate(url_list):
		#create the beautiful soup object from a single url. 
		print (url)
		try:
			opened_url = requests.get(url).text

		except Exception as e:
			print (e)
			print ('failure to open url')
			sys.exit()

		soup = BeautifulSoup(opened_url,'html.parser')

		#just get the DOI
		all_ps = soup.find_all('div',class_='well metadata')[1]
		children = all_ps.findChildren()
		items = []
		for child in children:
			if child.get('alt'):
				items.append(child.get('alt')) #gets the DOI

		#get publication date
		items.append(soup.find('time').get('datetime'))

		#get the keywords
		keywords = soup.find_all('a', class_='label-link')
		kw = []
		for word in keywords:
			url = word.get('href').split('%')
			kw.append(url[-2].replace('+',' '))
		items.append(kw)

		#get the filenames
		filenames = soup.find_all('a',class_='filename')
		f = []
		for a_file in filenames:
			f.append(a_file.string)
		items.append(f)

		#find the title
		items.append(soup.find('h1').string)

		#find authors
		authors = soup.find_all('span',class_='text-muted')
		author_list = []
		for author in authors:
			author_list.append(author.string)
		items.append(author_list)

		csv_writer.writerow(items)
		#print (items)


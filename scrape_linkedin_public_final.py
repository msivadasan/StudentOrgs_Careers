# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 17:40:22 2023
From: https://www.geeksforgeeks.org/scrape-linkedin-using-selenium-and-beautiful-soup-in-python/ , except we only try to access public data from linkedin (i.e., no logging in to any account.  (Scraping from accounts is not permitted ))
@author: Madhav Sivadasan
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv 

from selenium.webdriver.chrome.service import Service as ChromeService
service = ChromeService(executable_path='%cd%\\chromedriver.exe') # Point %cd% to the path of chromedriver.exe, which can be downloaded from https://chromedriver.chromium.org/downloads
file = open("./links.csv", "r") # links.csv has the list of LinkedIn urls
zzdata = list(csv.reader(file, delimiter=","))
file.close()
                      
allpages={} #dictionary to store the raw html 
for dd in range(1,100):    
    driver = webdriver.Chrome(service=service)
    profile_url =zzdata[dd][0]
    driver.get(profile_url)   
    start = time.time()
    # will be used in the while loop
    initialScroll = 0
    finalScroll = 1000
    while True:
        driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
        # this command scrolls the window starting from
        # the pixel value stored in the initialScroll
        # variable to the pixel value stored at the
        # finalScroll variable
        initialScroll = finalScroll
        finalScroll += 1000
        # we will stop the script for 3 seconds so that
        # the data can load
        time.sleep(3)
        # You can change it as per your needs and internet speed
        end = time.time()
        # We will scroll for 20 seconds.
        # You can change it as per your needs and internet speed
        if round(end - start) > 20:
            break
    src = driver.page_source
     
    # Now using beautiful soup
    soup = BeautifulSoup(src, 'lxml')
    allpages[dd]=soup
    x=(dd%10)
    driver.quit()
    time.sleep(10)

with open('data_1_100.txt','w', encoding='UTF8') as data: #write all the pages to a text file
      data.write(str(allpages))


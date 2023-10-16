# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 11:19:31 2023
@author: Madhav Sivadasan
"""
from bs4 import BeautifulSoup
import csv
##################################################
#Reading in soup 1 by 1
##################################################
def readin(aa, data):    
    sub1 = str(aa+1)+":"
    sub2 = str(aa+2)+":"
    # getting index of substrings
    idx1 = data.index(sub1)+ len(sub1) + 1
    idx2 = data.index(sub2)
    res = data[idx1:idx2] #All the data from 'aa+1: ' to 'aa+2:'
    soup = BeautifulSoup(res, "html.parser") # BeautifulSoup reads in the text as a soup object using html_parser, which then allows us to parse it using BeautifulSoup commands
    #Parse and extract name
    intro1 = soup.find('div', {'class': 'pv-text-details__left-panel'})
    if str(intro1)!="None":
        intro_1a_d = intro1.find("h1")
        name= intro_1a_d.get_text().strip()
    else: 
        name=" "
    #Parse and extract description in the introduction
    intro2=soup.find('div', {'class': 'text-body-medium break-words'})
    if str(intro2)!="None":
        intro_des= intro2.get_text().strip()
    else: 
        intro_des=" "
    ################################################################################
    ## Separating the page into sections -- some sections are missing on some pages ('About', 'Highlights', 'Activity', 'Experience', 'Education', 'Projects', 'Volunteering', 'Skills', 'Interests', 'People also viewed', 'People you may know', 'You might like')
    ################################################################################
    prcards=soup.findAll('section', {'data-view-name':'profile-card'})
    prdict={}
    for aa in range (0, len(prcards)):
        x=prcards[aa].find('span',{'aria-hidden':"true"}).get_text().strip()
        prdict[x]=prcards[aa]
    return(name, prdict, intro_des)


########################################################################################
##Scraped raw html file is read in
########################################################################################
import os
os.chdir(r"%cd%") # Point %cd% to the path for the data

with open('data_1_100.txt', encoding='UTF8') as f:
    data = f.read() #data is a long dictionary with all the html text for all of the urls scraped
########################################################################################


########################################################################################
### Parsing data on Experience, and saving to CSV; variables are Job Title (jtitle), Employer (jfirm), Dates employed (jdate), Employment Location (jloc)
########################################################################################
with open('cleaned_experience.csv', 'w', newline='', encoding='UTF8') as csv_file:
    csv_writer = csv.writer(csv_file)
    #########################################################################
    #Writing the variable names in the first line
    #########################################################################
    pp=["None"]*(2+4)
    pp[0]="list_id" #Essentially serial number on our list of students in data_1_100.txt
    pp[1]="name"
    i=2
    for yy in ("jtitle","jfirm", "jdate", "jloc"):
        pp[i]=yy
        i=i+1
    csv_writer.writerow(pp)
    #########################################################################
    # Writing the data with each-person-each job per line 
    #########################################################################
    for zz in range(0, 100):
        ww=readin(zz,data) # readin is a function defined above that parses data into profile cards 
        prdict=ww[1]
        keyslist=list(prdict)
        #print(zz, ww[0])
        if 'Experience' in keyslist:
            #Parses experience into a list of separate jobs; we can then parse information for each job to read the title, employer name, etc.
            jobs=prdict['Experience'].findAll('div',{'class' : 'display-flex flex-column full-width align-self-center'})
            pp[0]=zz+1
            pp[1]=ww[0]
            for aa in range(2,6):
                pp[aa]='NA'
            # Loop through each job, to extratct tile, employer name, etc.    
            for aa in range(0, len(jobs)):
                jtitles = jobs[aa].find('div', {'class': 'display-flex align-items-center mr1 t-bold'})
                if jtitles is not None:
                    pp[2]=jtitles.find('span',{'aria-hidden': "true"}).get_text().strip()
                jfirms = jobs[aa].find('span', {'class': 't-14 t-normal'})
                if jfirms is not None:
                    pp[3]=jfirms.find('span',{'aria-hidden': "true"}).get_text().strip()
                jdatesandloc= jobs[aa].findAll('span', {'class': 't-14 t-normal t-black--light'})
                for kk in range(0, len(jdatesandloc)):
                    hh=jdatesandloc[kk].find('span',{'aria-hidden': "true"}).get_text().strip()
                    ff=(hh[4:7])
                    if ff.isdigit():
                        pp[4]=hh
                    else:
                        pp[5]=hh
                csv_writer.writerow(pp) #Information for each person-job is written to a separate line in the csv file
                
########################################################################################
### Parsing data on Education, and saving to CSV; variables are Name of school (school), Degree (degree), Dates at school (date), activities and societies (activities).  The activities variable is where people mention club/frat/soririty membership
########################################################################################
with open('cleaned_education.csv', 'w', newline='', encoding='UTF8') as csv_file:
    csv_writer = csv.writer(csv_file)
    #########################################################################
    #Writing the variable names in the first line
    #########################################################################
    pp=["None"]*(2+4)
    pp[0]="list_id" #Essentially serial number on our list of students in data_1_100.txt
    pp[1]="name"
    i=2
    for yy in ("school","degree", "date", "activities"):
        pp[i]=yy
        i=i+1
    csv_writer.writerow(pp)

    #########################################################################
    # Writing the data with each-person-each job per line 
    #########################################################################
    for zz in range(0, 100):
        ww=readin(zz,data) # readin is a function defined above that parses data into profile cards 
        prdict=ww[1]
        keyslist=list(prdict)
        #print(zz, ww[0])
        if 'Education' in keyslist:
            #Parses Education  into a list of separate schools; we can then parse information for each school to read the school, degree, date, and activity.
            edegrees= prdict['Education'].findAll('div', {'class': 'display-flex flex-column full-width align-self-center'})
            for ee in range(0, len(edegrees)):
                schools= edegrees[ee].find('div', {'class': 'display-flex align-items-center mr1 hoverable-link-text t-bold'})
                dates= edegrees[ee].find('span', {'class': 't-14 t-normal t-black--light'})
                activity=edegrees[ee].find('div',{'class':'pv-shared-text-with-see-more full-width t-14 t-normal t-black display-flex align-items-center'} )
                degree= (edegrees[ee].find('span', {'class': 't-14 t-normal'}))
                pp[0]=zz+1 #To start from 1
                pp[1]=ww[0]    
                for aa in range(2,5):
                    pp[aa]='NA'
                if schools is not None:
                    pp[2]=schools.find('span',{'aria-hidden': "true"}).get_text().strip()
                if degree is not None:
                    pp[3]=degree.find('span', {'class': 'visually-hidden'}).get_text().strip()
                if dates is not None:
                    pp[4]=dates.find('span',{'aria-hidden': "true"}).get_text().strip()
                if activity is not None:
                    pp[5]=activity.find('span',{'aria-hidden': "true"}).get_text().strip()
                csv_writer.writerow(pp)



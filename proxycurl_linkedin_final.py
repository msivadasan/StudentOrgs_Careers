# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 17:40:22 2023

@author: Madhav
"""
# Proxycurl API  allows calls to LinkedIn. The pricing varies from 0.1/credit to 0.018/credit (i.e. per call).  For say 3200 calls, a $100 purchase would suffice, as it allows for 4546 calls https://nubela.co/proxycurl/dashboard/billing/buy-credits 
#https://nubela.co/proxycurl/docs?python#people-api-person-profile-endpoint
import requests
import json
import csv
import os
os.chdir(r"%cd%") #%cd% points to path for the file with list of linkedin urls
file = open("./links.csv", "r") ## A dataset with linkedin urls
zzdata = list(csv.reader(file, delimiter=","))
file.close()

api_key = 'GET_API_KEY_FROM_NUBELA' #Get API key from https://nubela.co/proxycurl/people-api 
headers = {'Authorization': 'Bearer ' + api_key}
api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'

# Code below is from help on nubela site: https://nubela.co/proxycurl/docs?python#people-api-person-profile-endpoint 
for ii in range(1,4): # Proxycurl only allows about 10 calls for free; more calls are priced: https://nubela.co/proxycurl/pricing 
    params = {
        'linkedin_profile_url': zzdata[ii][0],'fallback_to_cache': 'on-error', 'use_cache': 'if-present', 'skills': 'include', 'personal_contact_number': 'include', 'personal_email': 'include', 'inferred_salary': 'include',
        }
    response = requests.get(api_endpoint, params=params, headers=headers)
    profile_data=response.json()
    
    fname="sample"+str(ii)+".json"
    with open(fname, "w") as outfile:
        json.dump(profile_data, outfile)

#####################################################################################################################
##BASIC INFORMATION 
#After examining available fields, decided on collating only for the following:
vbs=['public_identifier', 'first_name', 'last_name', 'full_name', 'follower_count', 'occupation', 'headline', 'summary', 'country', 'country_full_name', 'city', 'state', 'languages', 'skills', 'gender', 'birth_date', 'industry', 'interests', 'personal_emails', 'personal_numbers']
#we handle 'inferred_salary' seperately as it has a min and max value
 
pdata="proxycurl_data_"+"basicinfo"+".csv"            
with open(pdata, 'w', newline='', encoding='UTF8') as csv_file:
    csv_writer = csv.writer(csv_file)
    #########################################################################
    #Writing the variable names in first line
    #########################################################################
    with open("sample1.json") as fp:
        listObj = json.load(fp)
    pp=[0]*(len(vbs)+2)
    i=0
    for yy in (vbs):
        pp[i]=yy
        i=i+1
    pp[i]="inferred_salary_max"
    pp[i+1]="inferred_salary_min"
    csv_writer.writerow(pp)
    
    #########################################################################
    # Writing the data with one person per line 
    ######################################################################### 
    for jj in range(1,4): ##We have only downloaded 4 people; need to pay for more
        nn="sample"+str(jj)+".json"
        with open(nn) as fp:
            listObj = json.load(fp)
        i=0
        for yy in (vbs):
            pp[i]=listObj[yy]
            i=i+1
        pp[i]=listObj["inferred_salary"]["min"] # We have found they (proxycurl) swapped min and max!
        pp[i+1]=listObj["inferred_salary"]["max"] 
        csv_writer.writerow(pp)
            
#####################################################################################################################
##EXPERIENCES AND EDUCATION
##Code to read in experiences and education into seperate csv files; public_identifier can be used to link basic info file with these files
for ff in ("experiences","education"):
    keyfield=ff            
    pdata="proxycurl_data_"+keyfield+".csv"            
    with open(pdata, 'w', newline='', encoding='UTF8') as csv_file:
        csv_writer = csv.writer(csv_file)
        # Code to get the names of the variables written to first row of CSV file    
        with open("sample1.json") as fp:
            listObj = json.load(fp)
        pp=[0]*(len(listObj[keyfield][0])+1)
        pp[0]='public_identifier'
        i=1
        for yy in (listObj[keyfield][0].keys()):
            pp[i]=yy
            i=i+1
        csv_writer.writerow(pp)
        
        for jj in range(1,4): ##We have only downloaded 4 people; need to pay for more
            nn="sample"+str(jj)+".json"
            with open(nn) as fp:
                listObj = json.load(fp)
            #We include the public_identifier variable in column 1, to allow linkage across datasets    
            pp[0]=listObj['public_identifier']
            for kk in range (0,len(listObj[keyfield])):
                i=1
                xx=list(listObj[keyfield][kk].keys())
                #Code to store start and end dates for jobs
                for yy in ('starts_at', 'ends_at'):
                    if listObj[keyfield][kk][yy] !=None:
                        pp[i]=str(listObj[keyfield][kk][yy]['month'] )+'/'+str(listObj[keyfield][kk][yy]['day']) +'/' + str(listObj[keyfield][kk][yy]['year'])      
                    else:
                        pp[i]="NA"
                    i=i+1
                    xx.remove(yy) #once start date and end date are removed, the rest of the variables are 1-dimesnional and easy to read in 
                #code to read in information of each job      
                for yy in (xx):
                    pp[i]=listObj[keyfield][kk][yy] 
                    i=i+1
                csv_writer.writerow(pp)
#####################################################################################################################
                
            
            
            
            
            
            
            
    
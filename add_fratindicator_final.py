# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 14:49:23 2023

@author: Madhav
"""
import os
os.chdir(r"%cd%") # Point %cd% to the path for the data

import csv
##This is the list of student frats and sororities at Michigan
file = open("./orgs_list.csv", "r", encoding="UTF8")
ndata = list(csv.reader(file, delimiter=","))
file.close()

# Make a list of cleaned frat/sorority names
xx=[""]*(len(ndata)-1)
for jj in range(0, len(ndata)-1): #first entry is the title "Organization", so start at 1 not 0
    xx[jj]=ndata[jj+1][1]
    
##Here I clean up the names to remove words that are seldom mentioned by students when indicating organization participation
for bb in ("Sorority", ",", " Inc.", "(FIJI)", "National", "International", "Fraternity", "Latin"):    
    xx[:]=[x.replace(bb, "").strip() for x in xx]
#print(xx)

#Load data on education as a pandas dataframe
import pandas as pd
lndata=pd.read_csv("./cleaned_education.csv")
dfrat=[0]*len(lndata)
fratname=["NA"]*len(lndata)
for aa in range(0, len(lndata)):
    if "University of Michigan" in lndata['school'][aa]:     
        for rr in range (0, len(xx)): #This cycles through the full list of frats and sororities, and picks any match
            if xx[rr] in str(lndata['activities'][aa]): 
                dfrat[aa]=1
                fratname[aa]=xx[rr] #Note that only the last matched fratname is retained, in case person is in multiple frats
#Add columns for frat dummy and frat name
lndata['dfrat']=dfrat
lndata['fratname']=fratname
#Convert dataframe to csv file
lndata.to_csv("./cleaned_education_with_dfrat.csv")  


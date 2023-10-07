# frats_linkedin
Project to collate LinkedIn data and check membership in a list of student organizations. 

This project involved the following steps:

(i) Collating information on student fraternities and sororities at the University of Michigan (in file orgs_list.csv).

(ii) Writing code to parse and collate information from LinkedIn, using two approaches:   
(a) Direct download using selenium and Beautiful Soup (scrape_linkedin_public_final.py), and then parsing the page information using beautiful soup commands (readin_linkedin_new.py)
(b) Downloading Linkedin information using <a href="https://nubela.co/proxycurl/linkedin" target="_blank">Proxycurl profile scraping API</a> (proxycurl_linkedin.py).

(iii) Writing code to create a dummy indicator for membership in a fraternity organization, based on the "activities" variable from the LinkedIn dataset.  I did this for the data created from the direct download approach, but this can easily be adjusted to work with other files.

---------------------------------------------------------------------------------------------
Description of code: scrape_linkedin_public_final.py 
-
This code builds on the <a href="https://www.geeksforgeeks.org/scrape-linkedin-using-selenium-and-beautiful-soup-in-python/"> blogpost </a> by Urvish Mahajan at geeksforgeeks.org, except we only try to access public data from linkedin (i.e., no logging in to any account.  (Scraping from accounts is not permitted ))



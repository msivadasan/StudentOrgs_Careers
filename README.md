# StudentOrgs_Careers
Project to collate LinkedIn data and check membership in a list of student organizations. 

This project involved the following steps:

(i) Collating information on student fraternities and sororities at the University of Michigan (in file orgs_list.csv).

(ii) Writing code to parse and collate information from LinkedIn, using two approaches:   
(a) Direct download using selenium and Beautiful Soup (scrape_linkedin_public_final.py), and then parsing the page information using beautiful soup commands (readin_linkedin_final.py)
(b) Downloading Linkedin information using <a href="https://nubela.co/proxycurl/linkedin" target="_blank">Proxycurl profile scraping API</a> (proxycurl_linkedin.py).

(iii) Writing code to create a dummy indicator for membership in a fraternity organization, based on the "activities" variable from the LinkedIn dataset.  I did this for the data created from the direct download approach, but this can easily be adjusted to work with other files.

---------------------------------------------------------------------------------------------
Description of code: scrape_linkedin_public_final.py 
-
This code builds on the <a href="https://www.geeksforgeeks.org/scrape-linkedin-using-selenium-and-beautiful-soup-in-python/"> blogpost </a> by Urvish Mahajan at geeksforgeeks.org, except I only try to access public data from LinkedIn (i.e., the code does not log in to any account, as scraping from accounts is not permitted by LinkedIn). 

The specific LinkedIn profile urls is in file links.csv.  The code loads each of the urls, and copies the full-page html source, and collates the pages into one text file (data_1_100.txt).

---------------------------------------------------------------------------------------------
Description of code: readin_linkedin_final.py 
-
This code also builds on advice in the <a href="https://www.geeksforgeeks.org/scrape-linkedin-using-selenium-and-beautiful-soup-in-python/"> blogpost </a> by Urvish Mahajan at geeksforgeeks.org. As the comments in the code clarify, converting the html text to a BeautisulSoup object allows for easy parsing of subsections in the html page.

Specifically, I inspected the raw html code carefully, to identify key formatting notation that separates the information of interest. For example:
* A string "<div class= "pv-text-details__left-panel">" denotes the start of an introduction element, and within that a string starting with "<h1" denotes the subelement with the name
* All of the key sections are in "profile-cards".  The  







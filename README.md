# StudentOrgs_Careers
Project to collate LinkedIn data and check membership in a list of student organizations. 

This project involved the following steps:

(1) Collating information on student fraternities and sororities at the University of Michigan (in file orgs_list.csv).

(2) Writing code to parse and collate information from LinkedIn, using two approaches:  
  (a) Direct download using selenium and BeautifulSoup ([scrape_linkedin_public_final.py](https://github.com/msivadasan/StudentOrgs_Careers/blob/main/scrape_linkedin_public_final.py)), and then parsing the page information using BeautifulSoup commands ([readin_linkedin_final.py](https://github.com/msivadasan/StudentOrgs_Careers/blob/main/readin_linkedin_final.py))
  (b) Downloading Linkedin information using <a href="https://nubela.co/proxycurl/linkedin" target="_blank">Proxycurl profile scraping API</a> ([proxycurl_linkedin_final.py](https://github.com/msivadasan/StudentOrgs_Careers/blob/main/proxycurl_linkedin_final.py)).

(3) Writing code ([add_fratindicator_final.py](https://github.com/msivadasan/StudentOrgs_Careers/blob/main/add_fratindicator_final.py)) to create a dummy indicator for membership in a fraternity organization and a variable with the name of the fraternity organization, based on the "activities" variable from the LinkedIn dataset.  I did this for the data created from the direct download approach, but this can easily be adjusted to work with other files.

---------------------------------------------------------------------------------------------
Description of code: [scrape_linkedin_public_final.py](https://github.com/msivadasan/StudentOrgs_Careers/blob/main/scrape_linkedin_public_final.py) 
-
This code builds on the [blogpost](https://www.geeksforgeeks.org/scrape-linkedin-using-selenium-and-beautiful-soup-in-python) by Urvish Mahajan at geeksforgeeks.org, except I only try to access public data from LinkedIn (i.e., the code does not log in to any account, as scraping from accounts is not permitted by LinkedIn). 

The specific LinkedIn profile urls are in **links.csv**.  The code loads each of the urls, copies the full-page html source, and collates the pages into one text file (data_1_100.txt).

---------------------------------------------------------------------------------------------
Description of code: [readin_linkedin_final.py](https://github.com/msivadasan/StudentOrgs_Careers/blob/main/readin_linkedin_final.py) 
-
This code also builds on advice in the [blogpost](https://www.geeksforgeeks.org/scrape-linkedin-using-selenium-and-beautiful-soup-in-python) by Urvish Mahajan at geeksforgeeks.org. As the comments in the code clarify, converting the html text to a BeautifulSoup object allows for easy parsing of subsections in the html page.

Specifically, I inspected the raw html code carefully, to identify key formatting notation that locates the information of interest. For example:
* A string "\<div class= "pv-text-details__left-panel">" denotes the start of an introduction element, and within that a string starting with "<h1" denotes the sub-element with the name of the person.
* All of the key sections are in "profile-cards".  The card elements start with "\<section data-view-name="profile-card">". The sections include: 'About', 'Highlights', 'Activity', 'Experience', 'Education', 'Projects', 'Volunteering', 'Skills', 'Interests', 'People also viewed', 'People you may know', 'You might like'. All sections are not necessarily present in every profile. For example, some people may not have a section for "highlights", and others may be missing 'Education'.
* For this project, the code collates information on name and description from the introduction section, and information from the 'Experience and 'Education' sections.
* **Experience information** (cleaned_experience.csv) For each job, I collate the following information:  
  - Serial number (list_id)
  - Name (name) 
  - Title, e.g. "Software Engineer" (jtitle)
  - Employer name, e.g., "Google" (jfirms)
  - Start to end date of job, e.g. "May 2021 to Aug 2022: 4mos"   (jdates)
  - Employment location, e.g., "Mountain View, CA" (jloc)           
* **Education information** (cleaned_education.csv) For each education element (school), I collate the following information:  
  - Serial number (list_id)
  - Name (name)
  - School, e.g., "University of Michigan - Stephen M. Ross School of Business" (school)
  - Degree, e.g., "Bachelor of Business Administration - BBA" (degree)
  - Dates, e.g., "2015 - 2019" (date)
  - Activities and societies, e.g., "Activities and societies: Pi Sigma Epsilon Business Fraternity, Asian Business Conference, Maize and Blue Games" (activities)
    
Both  the experience and education files include a serial number (list_id) and name (name) variable, to allow these to be linked to each other, and to the original **links.csv** file that had the list of urls.

---------------------------------------------------------------------------------------------
Description of code: [proxycurl_linkedin_final.py](https://github.com/msivadasan/StudentOrgs_Careers/blob/main/proxycurl_linkedin_final.py) 
-
To read in LinkedIn data using proxycurl, we need to first get an API key from [the proxycurl website](https://nubela.co/proxycurl/people-api). We are allowed only about 10 calls for free; for additional calls, payment needs to be made as per the pricing listed [here](https://nubela.co/proxycurl/pricing).     

The basic code for making the API calls was copied from the proxycurl documentation webpage [here](https://nubela.co/proxycurl/docs?python#people-api-person-profile-endpoint).  The returned information (in dictionary format) is collated into three separate files:
* **Basic information** (proxycurl_data_basicinfo.csv):  
After examining available fields, I decided to collate the following list of fields:
['public_identifier', 'first_name', 'last_name', 'full_name', 'follower_count', 'occupation', 'headline', 'summary', 'country', 'country_full_name', 'city', 'state', 'languages', 'skills', 'gender', 'birth_date', 'industry', 'interests', 'personal_emails', 'personal_numbers'].  In addition, I also read in 'inferred_salary_max' and 'inferred_salary_min'.  Interestingly there is only one inferred salary (max and min) for each person, i.e. it is not specific to each job of the person. 
* **Experience information** (proxycurl_data_experience.csv): For each job, I get information on the following:  
  - public_identifier
  - starts_at
  - ends_at
  - company
  - company_linkedin_profile_url
  - title
  - description
  - location
  - logo_url
* **Education information** (proxycurl_data_experience.csv): For each job, I get information on the following:
  - public_identifier
  - starts_at
  - ends_at
  - field_of_study
  - degree_name
  - school
  - school_linkedin_profile_url
  - description
  - logo_url
  - grade
  - activities_and_societies
The public_identifier variable appears to be unique and hence can be used to link the different datasets.
---------------------------------------------------------------------------------------------
Description of code: [add_fratindicator_final.py](https://github.com/msivadasan/StudentOrgs_Careers/blob/main/add_fratindicator_final.py) 
-
This code takes a list of fraternities and sororities (collated in step (1) of the project, in file orgs_list.csv), and then compares each of the strings to the string in "activities" in the scraped LinkedIn education file (cleaned_education), to create a dummy variable indicator (dfrat) for whether the "activities" includes any of the organizations in the org_list.csv file. We also retain the last matched fraternity name (fratname).  The resulting augmented csv file is stored as cleaned_education_with_dfrat.csv  

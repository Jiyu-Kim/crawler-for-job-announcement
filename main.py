from requests import get
from bs4 import BeautifulSoup
from extractors.wwr import extract_wwr_jobs
from extractors.programmers import extract_programmers_jobs

"""
#we work remotely > wwr.csv
keyword = "python"

wwr = extract_wwr_jobs(keyword)

#Create file
file_name_for_wwr = "wwr"
file = open(f"{keyword}.csv", "w", encoding="utf-8")
file.write("position, company, kind, region, url\n")

for job in wwr:
    file.write(f"{job['position']},{job['company']},{job['kind']},{job['kind']},{job['region']},{job['url']}\n")
    
file.close()
"""

#programmers > programmers.csv
page_num = 103
programmers = extract_programmers_jobs(page_num)

file_name_for_programmers = "programmers"
with open(f"{file_name_for_programmers}_{page_num}.csv", "w", encoding='utf-8') as file:
    #header 작성하기
    file.write("name, response_speed, company_link, company_name, position, end_date, job_type, experience, salary, location, tech_stacks\n")

    for job in programmers:
        file.write(f"{job['name']},{job['response_speed']},{job['company_link']},{job['company_name']},{job['position']},{job['end_date']},{job['job_type']},{job['experience']},{job['salary']},{job['location']},{job['tech_stacks']}\n")




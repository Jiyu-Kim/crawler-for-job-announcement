import pandas as pd #Series, DataFrame, Panel
import os
import csv, json

def save_to_file(file_name, jobs):
    """
    with open(f"{file_name}.csv", "w", encoding='utf-8') as file:
    #header
    file.write("title, company, job_type, location, link\n")

    for job in jobs:
        #file.write(f"{job[0]}, {job[1]}, {job[2]}, {job[3]}, {job[4]}\n") # List -> file.write()
        file.write(f"{jobs['title']}, {jobs['company']}, {jobs['job_type']}, {jobs['location']}, {jobs['link']}") # Dictionary > DataFrame()
    """

    #df = pd.DataFrame(jobs, columns=["title", "company", "job_type", "location", "link"]) # List -> DataFrame()
    df = pd.DataFrame(jobs, columns=["title", "company", "job_type", "location", "link"]) # Dictionary > DataFrame()
    df.to_csv(f"./results/{file_name}.csv", encoding='utf-8')



def csv_to_json(file_name):
    folder_path = 'results'
    file_name = f"{file_name}.csv"
    file_path = os.path.join(folder_path, file_name)

    jobs = []
    # Read CSV file and convert to list of dictionaries
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        #print(type(csv_reader)) <class 'csv.DictReader'>
        for job in csv_reader:
            jobs.append(job)
    
    return jobs
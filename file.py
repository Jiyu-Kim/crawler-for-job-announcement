import pandas as pd #Series, DataFrame, Panel

def save_to_file(file_name, jobs):
    """
    with open(f"{file_name}.csv", "w", encoding='utf-8') as file:
    #header
    file.write("position, company, kind, region, link\n")

    for job in jobs:
        #file.write(f"{job[0]}, {job[1]}, {job[2]}, {job[3]}, {job[4]}\n") # List -> file.write()
        file.write(f"{jobs['position']}, {jobs['company']}, {jobs['kind']}, {jobs['region']}, {jobs['link']}") # Dictionary > DataFrame()
    """

    #df = pd.DataFrame(jobs, columns=["position", "company", "kind", "region", "link"]) # List -> DataFrame()
    df = pd.DataFrame(jobs, columns=["position", "company", "kind", "region", "link"]) # Dictionary > DataFrame()
    df.to_csv(f"{file_name}.csv", encoding='utf-8')
from requests import get
from bs4 import BeautifulSoup

def extract_wwr_jobs(keyword):
    base_url = "https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term="

    response = get(f"{base_url}{keyword}")

    if response.status_code != 200:
        print("Can't request website.")
    else:
        results = []
        soup = BeautifulSoup(response.text, "html.parser") # parse HTML to Pyhton entity
        #find_all() returns a list containing the signle result
        jobs = soup.find_all('section', class_="jobs")
        for job_section in jobs:
            job_posts = job_section.find_all('li')
            job_posts.pop(-1)
            for post in job_posts:
                anchors = post.find_all('a')
                anchor = anchors[1]
                link = anchor['href']
                company, jop_type, location = anchor.find_all('span', class_='company')
                #find() returns the result
                title = anchor.find('span', class_='title')

                """
                # Dictionary > file.write() version
                job_data = {
                    'title': title.string.replace(",", " "),
                    'company': company.string.replace(",", " "),
                    'jop_type': jop_type.string.replace(",", " "),
                    'location': location.string.replace(",", " "),
                    'link': f"https://weworkremotely.com{link}"
                }
                """
                # Dictionary > DataFrame() version
                job_data = {
                    'title': title.string,
                    'company': company.string,
                    'jop_type': jop_type.string,
                    'location': location.string,
                    'link': f"https://weworkremotely.com{link}"
                }
                # List > file.write() version
                #job_data = [title.string.replace(",", " "), company.string.replace(",", " "), jop_type.string.replace(",", " "), location.string.replace(",", " "), f"https://weworkremotely.com{link}"]
                # List > DataFrame() version
                #job_data = [title.string, company.string, jop_type.string, location.string, f"https://weworkremotely.com{link}"]
                
                results.append(job_data)
        
        return results
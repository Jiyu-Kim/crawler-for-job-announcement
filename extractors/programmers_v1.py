from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from tqdm import tqdm

"""
1. 크롤링할 페이지 수를 설정한다.
2. 1에서 설정한 수만큼 페이지를 이동하면서 채용 공고문의 링크를 크롤링한다.
3. 2에서 크롤링한 공고문의 링크를 각각 들어가서 원하는 데이터를 크롤링한다.
4. 크롤링한 데이터를 csv 파일로 저장한다.
"""

#1. 크롤링할 페이지 수를 설정한다.
page_num = 5

#2. 1에서 설정한 수만큼 페이지를 이동하면서 채용 공고문의 링크를 크롤링한다.
options = Options()
options.add_experimental_option("detach", True)
service = Service(ChromeDriverManager().install()) #크롬 브라우저 버전이 업데이트 되면 그에 맞는 크롬 드라이버 설치
driver = webdriver.Chrome(service=service, options=options)
#driver.implicitly_wait(3)
time.sleep(3)

url = "https://career.programmers.co.kr/job"
driver.get(url)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
position_links = ["https://career.programmers.co.kr" + position_link['href'] for position_link in soup.find_all("a", class_="position-link")] # 채용 공고문의 링크를 저장하는 리스트

for current_page in range(page_num - 1):
    #다음 페이지로 이동
    next_page_btn = driver.find_element(By.XPATH, '//*[@id="tab_position"]/div[3]/ul/li[9]/span')
    next_page_btn.click()
    #driver.implicitly_wait(30) # driver.page_source still gets prvious page's html
    #WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'li.page-item.active > span.page-link'), str(current_page + 2))) # driver.page_source still gets prvious page's html
    time.sleep(10)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    position_links = position_links + ["https://career.programmers.co.kr" + position_link['href'] for position_link in soup.find_all("a", class_="position-link")] 

num = 1
for item in position_links:
    print(f"{num}:{item}")
    num += 1


#3. 2에서 크롤링한 공고문의 링크를 각각 들어가서 원하는 데이터를 크롤링한다.
results = []
for position_link in position_links:
    driver.get(position_link)
    driver.implicitly_wait(3)
    #time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    #결측값 대비
    name, response_speed, company_link, company_name, position, end_date, job_type, experience, salary, location = "None", "None", "None", "None", "None", "None", "None", "None", "None", "None"
    tech_stacks = []

    #element가 없을 경우 발생하는 에러 처리
    try:
        name = driver.find_element(By.XPATH, '//*[@id="career-app-legacy"]/div/div[1]/div[1]/header/div/div[2]/div/h2').text
    except:
        pass

    try:
        response_speed = driver.find_element(By.XPATH, '//*[@id="career-app-legacy"]/div/div[1]/div[1]/header/div/div[2]/div/span').text
    except:
        pass

    try:
        company_link = driver.find_element(By.XPATH, '//*[@id="career-app-legacy"]/div/div[1]/div[1]/header/div/div[2]/h4/a').get_attribute('href')
    except:
        pass

    try:
        company_name = driver.find_element(By.XPATH, '//*[@id="career-app-legacy"]/div/div[1]/div[1]/header/div/div[2]/h4/a').text
    except:
        pass

    try:
        position = driver.find_element(By.XPATH, '//*[@id="career-app-legacy"]/div/div[1]/div[1]/section/div/div[1]/div[1]/div[2]').text
    except:
        pass

    try:
        end_date = driver.find_element(By.XPATH, '//*[@id="career-app-legacy"]/div/div[1]/div[1]/section/div/div[1]/div[2]/div[2]').text
    except:
        pass

    try:
        job_type = driver.find_element(By.XPATH, '//*[@id="career-app-legacy"]/div/div[1]/div[1]/section/div/div[1]/div[3]/div[2]').text
    except:
        pass

    try:
        experience = driver.find_element(By.XPATH, '//*[@id="career-app-legacy"]/div/div[1]/div[1]/section/div/div[1]/div[4]/div[2]').text
    except:
        pass

    try:
        salary = driver.find_element(By.XPATH, '//*[@id="career-app-legacy"]/div/div[1]/div[1]/section/div/div[1]/div[5]/div[2]').text
    except:
        pass

    try:
        location = driver.find_element(By.CSS_SELECTOR, 'div.KACXxUyP7jEgxQYiU_Bq > div:nth-child(2)').text
    except:
        pass

    try:
        #리스트 형태 데이터
        tech_stacks = [tech_stack.text for tech_stack in driver.find_elements(By.CSS_SELECTOR, 'li.QdgvMJO9ZYOaiwrEUqgo.nUBs27jXBxRVUu9DLzz4')]
    except:
        pass
    #4. 데이터를 딕셔너리 형태로 저장한다.
    job_data = {
            'name': name,
            'response_speed': response_speed,
            'company_link': company_link,
            'company_name': company_name,
            'position': position,
            'end_date': end_date,
            'job_type': job_type,
            'experience': experience,
            'salary': salary,
            'location': location,
            'tech_stacks': tech_stacks
        }
    results.append(job_data)
    """
    #텍스트 형태 데이터
    try:
        name = driver.find_element(By.XPATH, '//*[@id="career-app-legacy"]/div/div[1]/div[1]/header/div/div[2]/div/h2').text
        response_speed = driver.find_element(By.XPATH, '//*[@id="career-app-legacy"]/div/div[1]/div[1]/header/div/div[2]/div/span').text
        company_link = driver.find_element(By.XPATH, '//*[@id="career-app-legacy"]/div/div[1]/div[1]/header/div/div[2]/h4/a').get_attribute('href')
        company_name = driver.find_element(By.XPATH, '//*[@id="career-app-legacy"]/div/div[1]/div[1]/header/div/div[2]/h4/a').text

        position = driver.find_element(By.XPATH, '//*[@id="career-app-legacy"]/div/div[1]/div[1]/section/div/div[1]/div[1]/div[2]').text
        end_date = driver.find_element(By.XPATH, '//*[@id="career-app-legacy"]/div/div[1]/div[1]/section/div/div[1]/div[2]/div[2]').text
        job_type = driver.find_element(By.XPATH, '//*[@id="career-app-legacy"]/div/div[1]/div[1]/section/div/div[1]/div[3]/div[2]').text
        experience = driver.find_element(By.XPATH, '//*[@id="career-app-legacy"]/div/div[1]/div[1]/section/div/div[1]/div[4]/div[2]').text
        salary = driver.find_element(By.XPATH, '//*[@id="career-app-legacy"]/div/div[1]/div[1]/section/div/div[1]/div[5]/div[2]').text

        location = driver.find_element(By.CSS_SELECTOR, 'div.KACXxUyP7jEgxQYiU_Bq > div:nth-child(2)').text
        location = driver.find_element(By.CSS_SELECTOR, 'div.KACXxUyP7jEgxQYiU_Bq > div:nth-child(2)').text
        #리스트 형태 데이터
        tech_stacks = [tech_stack.text for tech_stack in driver.find_elements(By.CSS_SELECTOR, 'li.QdgvMJO9ZYOaiwrEUqgo.nUBs27jXBxRVUu9DLzz4')]
    
    # element를 찾지 못했을 때 그냥 넘기기
    except:
        pass

    finally:
        job_data = {
            'name': name,
            'response_speed': response_speed,
            'company_link': company_link,
            'company_name': company_name,
            'position': position,
            'end_date': end_date,
            'job_type': job_type,
            'experience': experience,
            'salary': salary,
            'location': location,
            'tech_stacks': tech_stacks
        }
        results.append(job_data)
    """

driver.close()

#4. 크롤링한 데이터를 csv 파일로 저장한다.
filename = "programmers_v1"
with open(f"{filename}.csv", "w", encoding='utf-8') as file:
    #header 작성하기
    file.write("name, response_speed, company_link, company_name, position, end_date, job_type, experience, salary, location, tech_stacks\n")

    for result in results:
        file.write(f"{result['name']},{result['response_speed']},{result['company_link']},{result['company_name']},{result['position']},{result['end_date']},{result['job_type']},{result['experience']},{result['salary']},{result['location']},{result['tech_stacks']}\n")
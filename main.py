from flask import Flask
from flask import render_template
from flask import request # requests는 client가 보낸 request에 대한 정보에 접근할 수 있게 해준다.
from flask import redirect
from flask import send_file
from extractors.indeed import extract_indeed_jobs
from extractors.wwr import extract_wwr_jobs
from file import save_to_file, csv_to_json
import os, csv, json

app = Flask("JobScrpper")

db = {}

@app.route("/") # decorator(syntatic sugar)
def home():
    return render_template("home.html") # 변수 name을 home.html에 보낸다.


@app.route("/search")
def search():
    #print(request.args) #ImmutableMultiDict([('keyword', 'python')])
    keyword = request.args.get("keyword")
    if keyword == None or keyword == "":
        return redirect("/")
    else:
        folder_path = 'results'
        file_name = f"{keyword.lower()}.csv"
        file_path = os.path.join(folder_path, file_name)
        #if keyword.lower() in db:
            #jobs = db[keyword.lower()]
        if os.path.isfile(file_path):
            jobs = csv_to_json(keyword.lower())
        else:
            indeed = extract_indeed_jobs(keyword.lower())
            wwr = extract_wwr_jobs(keyword.lower())
            jobs = indeed + wwr # list
            #db[keyword.lower()] = jobs # Insert Data into DB
            save_to_file(keyword.lower(), jobs)
        return render_template("search.html", keyword=keyword, jobs=jobs, num_job=len(jobs))
    
@app.route("/export")
def export():
    keyword = request.args.get("keyword") #<a target="_blank" href="/export?keyword={{keyword}}">Export to file</a>의 query parameter를 볼 수 있다.
    folder_path = 'results'
    file_name = f"{keyword.lower()}.csv"
    file_path = os.path.join(folder_path, file_name)

    # when client does NOT enter a query parameter.
    if keyword == None or keyword == "": 
        return redirect("/")
    
    # when client doen enter a client parameter.
    else:
        if os.path.isfile(file_path) == False:
            return redirect(f"/search?keyword={keyword}")
        else:
            return send_file(f"./results/{keyword.lower()}.csv", as_attachment=True)


app.run("0.0.0.0", port=3000) # allow all inboud traffic from 0.0.0.0(internet)






from flask import Flask
from flask import render_template
from flask import request # requests는 client가 보낸 request에 대한 정보에 접근할 수 있게 해준다.
from flask import redirect
from extractors.indeed import extract_indeed_jobs
from extractors.wwr import extract_wwr_jobs


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
        print("Go home")
        return redirect("/")
    else:
        print("Start Crawling")
        if keyword.lower() in db:
            jobs = db[keyword.lower()]
        else:
            indeed = extract_indeed_jobs(keyword.lower())
            wwr = extract_wwr_jobs(keyword.lower())
            jobs = indeed + wwr # list
            db[keyword.lower()] = jobs # Insert Data into DB
        return render_template("search.html", keyword=keyword, jobs=jobs)
    
@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword == None or keyword == "":
        return redirect("/")
    else:
        if keyword is not db:
            return redirect(f"/search?keyword={keyword}")


app.run("0.0.0.0", port=3000) # allow all inboud traffic from 0.0.0.0(internet)






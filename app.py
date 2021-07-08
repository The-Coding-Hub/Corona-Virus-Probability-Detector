from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from plyer import notification 
import pickle
from datetime import datetime
app = Flask(__name__)

file = open('model.pkl', 'rb')
clf = pickle.load(file)
file.close()

def stats():
    # Getting the main html source code from the required website

    url = "https://www.mohfw.gov.in/"
    r = requests.get(url)
    htmlContent = r.content

    soup = BeautifulSoup(htmlContent, "html.parser")

    # Getting Data

    vac = soup.find("span", class_="totalvac").get_text() # "Total Vaccination" 
    vac_num = soup.find("span", class_="coviddata").get_text() # "<number>"

    data = soup.find_all("span", class_="mob-show")
    text_main = []
    for text in data:
        text_main.append(text.get_text())

    # Getting required text from the created list

    active = text_main[0]
    active_num = text_main[2]
    discharged = text_main[3]
    discharged_num = text_main[5]
    death = text_main[6]
    death_num = text_main[8]

    active = active + ": " + active_num # Active Text + Number
    discharged = discharged + ": " + discharged_num # Discharged Text + Number
    death = death + ": " + death_num # Death Text + Number
    vaccination = vac + vac_num

    return vaccination, active, discharged, death

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            myDict = request.form
            fever = int(myDict['fever'])
            age = int(myDict['age'])
            pain = int(myDict['pain'])
            runnyNose = int(myDict['runnyNose'])
            diffBreath = int(myDict['diffBreath'])
            vacStat = int(myDict['vacStat'])
            inputFeatures = [fever, pain, age, runnyNose, diffBreath, vacStat]
            infProb = clf.predict_proba([inputFeatures])[0][1]
            a = stats()
            vaccination = a[0]
            active = a[1]
            discharged = a[2]
            death = a[3]
            update_time = datetime.now().strftime("%d %b, %Y")
            return render_template('result.html', prob=round(infProb*100), update_time=update_time, vac=vaccination, active=active, discharged=discharged, death=death)
        except:
            a = stats()
            vaccination = a[0]
            active = a[1]
            discharged = a[2]
            death = a[3]
            update_time = datetime.now().strftime("%d %b, %Y")
            return render_template('error.html', update_time=update_time, vac=vaccination, active=active, discharged=discharged, death=death)
    a = stats()
    vaccination = a[0]
    active = a[1]
    discharged = a[2]
    death = a[3]
    update_time = datetime.now().strftime("%d %b, %Y")
    return render_template('index.html', update_time=update_time, vac=vaccination, active=active, discharged=discharged, death=death)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    a = stats()
    vaccination = a[0]
    active = a[1]
    discharged = a[2]
    death = a[3]
    update_time = datetime.now().strftime("%d %b, %Y")
    return render_template('contact.html', update_time=update_time, vac=vaccination, active=active, discharged=discharged, death=death)

@app.route('/about', methods=['GET', 'POST'])
def about():
    a = stats()
    vaccination = a[0]
    active = a[1]
    discharged = a[2]
    death = a[3]
    update_time = datetime.now().strftime("%d %b, %Y")
    return render_template('about.html', update_time=update_time, vac=vaccination, active=active, discharged=discharged, death=death)

if __name__ == '__main__':
	app.run(debug=False, host="0.0.0.0", port=8000)

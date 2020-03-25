import requests
import json
import numpy as np
# import plotly.express as px
import matplotlib.pyplot as plt
import settings

url = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/cases_by_particular_country.php"
country = settings.COUNTRY
querystring = {"country":country}

headers = {
    'x-rapidapi-host': "coronavirus-monitor.p.rapidapi.com",
    'x-rapidapi-key': "f26547d38cmsh691dd9b6ee44f2dp153bc3jsn2208eb4e8769"
    }

response = requests.request("GET", url, headers=headers, params=querystring).json()
data = response['stat_by_country']

total_cases = []
record_date = []
total_deaths = []
counter = 0
for d in data:
    if counter == 0:
        date = d['record_date'][5:10]
        deaths = int(d['total_deaths'].replace(',',''))
        cases = int(d['total_cases'].replace(',',''))
        total_deaths.append(deaths)
        total_cases.append(cases)
        record_date.append(date)
    else:
        new_date = d['record_date'][5:10]
        if new_date != date:
            total_deaths.append(deaths)
            total_cases.append(cases)
            record_date.append(date)
            date = new_date
        else:
            deaths = int(d['total_deaths'].replace(',',''))
            cases = int(d['total_cases'].replace(',',''))
    if d == data[-1]:
        new_date = d['record_date'][5:10]
        deaths = int(d['total_deaths'].replace(',',''))
        cases = int(d['total_cases'].replace(',',''))
        if new_date != record_date[-1]:
            total_deaths.append(deaths)
            total_cases.append(cases)
            record_date.append(new_date)

    counter += 1
    

total_cases = np.array(total_cases)
record_date = np.array(record_date)
total_deaths = np.array(total_deaths)

url2 = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/latest_stat_by_country.php"
response = requests.request("GET", url2, headers=headers, params=querystring).json()

data_latest = response['latest_stat_by_country']
new_cases = data_latest[0]['new_cases']
total_cases_latest = data_latest[0]['total_cases']
total_deaths_latest = data_latest[0]['total_deaths']

print(f'New Cases: {new_cases}')
print(f'Total Cases: {total_cases_latest}')
print(f'Total Deaths: {total_deaths_latest}')

plt.plot(record_date, total_cases, '-o')
plt.yticks(total_cases)
plt.title(country)
plt.xlabel('Date')
plt.ylabel('Cases')
plt.show()
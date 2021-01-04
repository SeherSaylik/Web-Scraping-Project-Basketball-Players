from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib import style


def create_web_df(url,tableid):
    response=requests.get(url)
    soup=BeautifulSoup(response.text,"html.parser")
    congress_table=soup.find("table",attrs={"class":tableid},)
    headers=congress_table.tr
    titles=headers.find_all("abbr")
    table=pd.read_html(str(congress_table))
    df=pd.DataFrame(table)

    keys=[]
    data={}
    for title in titles:
        keys.append(title["title"])
        data[title['title']] = []
        for row in congress_table.find_all('tr')[1:]:
            for key, a in zip(keys, row.find_all("td")[2:]):

                data[key].append(''.join(c for c in a.text if (c.isdigit() or c == ".")))
        Min = min([len(x) for x in data.values()])
        for key in data.keys():
            data[key] = list(list(map(lambda x: float(x), data[key][:Min])),)

    return data



df_shortnings=create_web_df("https://en.wikipedia.org/wiki/LeBron_James","toccolours")
df_lebron_james=create_web_df("https://en.wikipedia.org/wiki/LeBron_James","wikitable sortable")
df_giannis_antetokounmpo=create_web_df("https://en.wikipedia.org/wiki/Giannis_Antetokounmpo","wikitable sortable")
df_antony_davis=create_web_df("https://en.wikipedia.org/wiki/Anthony_Davis","wikitable sortable")
df_kawhi_leonard=create_web_df("https://en.wikipedia.org/wiki/Kawhi_Leonard","wikitable sortable")

print(df_giannis_antetokounmpo)

#Data Visualization Part

plt.plot(df_lebron_james["Points per game"],label="Lebron James")
plt.plot(df_giannis_antetokounmpo["Points per game"],label="Giannis Antetokounmpo")
plt.plot(df_antony_davis["Points per game"],label="Antony Davis")
plt.plot(df_kawhi_leonard["Points per game"],label="Kawhi Leonard")
plt.legend()
plt.xlabel('years')
plt.ylabel('PPG')
plt.show()

plt.plot(df_lebron_james["Field goal percentage"],label="Lebron James")
plt.plot(df_giannis_antetokounmpo["Field goal percentage"],label="Giannis Antetokounmpo")
plt.plot(df_antony_davis["Field goal percentage"],label="Antony Davis")
plt.plot(df_kawhi_leonard["Field goal percentage"],label="Kawhi Leonard")
plt.legend()
plt.xlabel('years')
plt.ylabel('FGP')
plt.show()
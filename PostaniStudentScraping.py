import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import mysql.connector

f = open("fakulteti.txt", "w")


url_to_scrape = 'https://www.postani-student.hr/usercontrols/uvjeticontainer.aspx?id=25192'
#Load html's plain data into a variable
response = requests.get(url_to_scrape)
#parse the data
soup = BeautifulSoup(response.text, "html.parser")

#table = soup.find('table')
#table_rows = table.find_all('tr')

#for tr in table_rows:
#    td = tr.find_all('td')
#    row = [i for i in td]
#    print(row)
mydb = mysql.connector.connect(
    host= 'localhost',
    user= 'root',
    passwd= '',
    database = 'kalkulator'
)

ocjene = soup.find(id='ucUvjeti_gdvOcjeneIzSrednjeSkole_ctl02_lblVrednovanje')

hr_vr = soup.find(id='ucUvjeti_gdvObvezniUvjeti_ctl02_lblVrednovanje')
hr_raz = soup.find(id='ucUvjeti_gdvObvezniUvjeti_ctl02_lblRazina')

mat_vr = soup.find(id='ucUvjeti_gdvObvezniUvjeti_ctl03_lblVrednovanje')
mat_raz = soup.find(id='ucUvjeti_gdvObvezniUvjeti_ctl03_lblRazina')

eng_vr = soup.find(id='ucUvjeti_gdvObvezniUvjeti_ctl04_lblVrednovanje')
eng_raz = soup.find(id='ucUvjeti_gdvObvezniUvjeti_ctl03_lblRazina')

fakulteti = []
smjerovi = []
faks = []

for i in range(24000, 25600):
    if i == 25068 or i == 25592:
        i +=1
    url = 'https://www.postani-student.hr/usercontrols/uvjeticontainer.aspx?id={}'.format(i)
    responses = requests.get(url)
    soup2 = BeautifulSoup(responses.text, "html.parser")
    h1 = soup2.h1
    h2 = soup2.find_all('h2')
    ocjene2 = soup2.find(id='ucUvjeti_gdvOcjeneIzSrednjeSkole_ctl02_lblVrednovanje')
    
    if ocjene2:
        hr_vr2 = soup2.find(id='ucUvjeti_gdvObvezniUvjeti_ctl02_lblVrednovanje')
        hr_raz2 = soup2.find(id='ucUvjeti_gdvObvezniUvjeti_ctl02_lblRazina')

        mat_vr2 = soup2.find(id='ucUvjeti_gdvObvezniUvjeti_ctl03_lblVrednovanje')
        mat_raz2 = soup2.find(id='ucUvjeti_gdvObvezniUvjeti_ctl03_lblRazina')

        eng_vr2 = soup2.find(id='ucUvjeti_gdvObvezniUvjeti_ctl04_lblVrednovanje')
        eng_raz2 = soup2.find(id='ucUvjeti_gdvObvezniUvjeti_ctl03_lblRazina')
        if ("STUDIJSKI PROGRAM VIŠE NIJE AKTIVAN" in h2[1].contents[0]):
            continue
        if (str(h1.contents[0]) not in fakulteti):
            fakulteti.append(str(h1.contents[0]))
        if ((str(h2[1].contents[0])in smjerovi) and (str(h1.contents[0]) in fakulteti)):
            continue
        else:
            smjerovi.append((str(h2[1].contents[0])))
        print(url)
        mycursor = mydb.cursor()
        print(h2[1].contents[0])
        sql = "INSERT INTO Uvjeti (Fakultet, Smjer, Matematika_razina, Hrvatski_razina, Engleski_razina, Matematika_vrednovanje, Hrvatski_vrednovanje, Engleski_vrednovanje, Vrednovanje_prosjek) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (str(h1.contents[0]), str(h2[1].contents[0]), str(mat_raz2.contents[0]), str(hr_raz2.contents[0]), str(eng_raz2.contents[0]), str(mat_vr2.contents[0]), str(hr_vr2.contents[0]), str(eng_vr2.contents[0]), str(ocjene2.contents[0]))
        print(val)
        mycursor.execute(sql, val)

        mydb.commit()

        print(mycursor.rowcount, "record inserted.")
        faks.append(str(h1.contents[0]) + " : " + str(h2[1].contents[0]))
print('\n\n\n\n')
faksici = []
for i in faks:
    n = i.find(':')
    fak = i[:n-1]
    if (fak in faksici):
        continue
    else:
        faksici.append(fak)
    print (fak)
    for j in faks:
        if fak in j:
            smjer = j[n + 2:]
            print (('"' + smjer.lower() + '|' + smjer + '",'), end = ' ')
    print ('\n\n')        
    

##print('\n\nSvi fakulteti:\n')
##i = 1
##for fakultet in fakulteti:
##    print('<option value = "' + str(i) + '"> ' + fakultet + ' </option>' )
##    i+= 1
f.close()
        





import requests 
from bs4 import BeautifulSoup
import csv 
#Getting the movies
i = 1
MovieLinks=[]
while i < 1000000:
    URL_Catalog = "https://elcinema.com/en/index/work/country/eg?page="+str(i)
    r = requests.get(URL_Catalog)  ##get the data of the URL 
    soup = BeautifulSoup(r.content, 'html5lib') 
    table = soup.find('table', attrs = {'class':'expand'})  
    tr=table.find_all('tr')
    for row in tr[1:]: 
        MovieLink=""
        td=row.find_all('td')
        if(td[2].contents[0] == "Movie" and int(td[3].contents[0])<=2021 and int(td[3].contents[0])>=2011):
            MovieLink=td[1].contents[1].attrs['href'] 
            if MovieLink[9:-1] not in MovieLinks:
                MovieLinks.append(MovieLink[9:-1])
        if(int(td[3].contents[0])<2011):
            i = 10000001
    i+=1
pass
filename = 'ids.txt'
with open(filename, 'w') as f: 
    f.write(' '.join(MovieLinks))

       
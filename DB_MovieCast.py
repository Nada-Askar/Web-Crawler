import requests 
from bs4 import BeautifulSoup
import csv 
MovieCast={}
filename = 'ids.txt'
ids = []
with open(filename, 'r') as f: 
    ids = f.read().split()
for i in ids:
    URL_Movie_1 = "https://elcinema.com/en/work/"
    URL_Movie=URL_Movie_1+i
    MovieID_1=i
    URL_Cast=URL_Movie+"/cast"
    r = requests.get(URL_Cast)  ##get the data of the URL 
    soup = BeautifulSoup(r.content, 'html5lib')     
    Cast={}
    CastDetails=soup.find_all('div',attrs={'class':'columns large-2'})
    Castrole = [c.find('h3',attrs={'class':'section-title'}).contents[0].split('\n')[1].lstrip() for c in CastDetails]
    CastMembers=soup.find_all('ul', attrs={'class':'small-block-grid-2 medium-block-grid-3 large-block-grid-6'})
    for i in range (len(CastMembers)):
        Cast[Castrole[i]] = []
        for d in CastMembers[i].find_all('div', attrs={'class':'thumbnail-wrapper'}):
            Cast[Castrole[i]].append(d.find('ul',attrs={'class':'description'}).find('li').contents[0].attrs['href'])
    MovieCast[MovieID_1]=Cast
#castids
castIDs=set()
for i in MovieCast:
    for j in MovieCast[i]:
        for k in MovieCast[i][j]:
            castIDs.add(k[11:-1])
filename = 'castids.txt'
with open(filename, 'w') as f: 
    f.write(' '.join(castIDs))
pass
import requests
from bs4 import BeautifulSoup
import csv 
import json
CastList=[]
filename = 'castids.txt'
castids = []
with open(filename, 'r') as f: 
    castids = f.read().split()
for i in castids:
    Cast={}
    URL_Cast_Member = "https://elcinema.com/en/person/"+i
    r = requests.get(URL_Cast_Member)  ##get the data of the URL 
    soup = BeautifulSoup(r.content, 'html5lib') 
    CastID=i
    Cast['CastID']=CastID
    #Name
    Cast_Name_1 = soup.find('span', attrs = {'class':'left'})  
    CastName=Cast_Name_1.contents[0]
    Cast['Name']=CastName
    #Image
    CastImage=soup.find('div', attrs={'class':"columns medium-3 large-3"}).find('a').find('img').attrs['src']
    Cast['Image']=CastImage
    #Details start
    Details=soup.find_all('div', attrs={'class':'columns large-10'})
    #Biography start
    thereis = False
    for i in Details:
        if(i.find("ul",attrs = {'class':'list-separator list-title'})) != None:
            Details = i
            thereis = True
            if Details.find("p") !=None:
                Biography=Details.find("p").text
                Cast['Biography']=Biography
            break
    #Biography end
    if(thereis):
        Details = Details.find_all("ul",attrs = {'class':'list-separator list-title'})
        for i in Details:
            #Birth Name
            if (i.contents[1].contents[0])=='Birth Name:':
                BirthName=i.contents[3].contents[0]
                Cast['BirthName']=BirthName
            #Nickname
            if(i.contents[1].contents[0]=='Nickname:'):
                Nickname=i.contents[3].contents[0]
                Cast['Nickname']=Nickname
            #Date of Birth
            if(i.contents[1].contents[0]=='Date of Birth:'):
                BirthDay=i.contents[3].contents[0].text
                BirthYear=i.contents[3].contents[2].text
                DateOfBirth=BirthDay+' '+BirthYear
                Cast['DateOfBirth']=DateOfBirth
            #Birth Country
            if(i.contents[1].contents[0]=='Birth Country:'):
                BirthCountry=i.contents[3].contents[0]
                Cast['BirthCountry']=BirthCountry
                Cast['Nationality']=BirthCountry
        #Details End
    #Social Media Accounts
    SocialMedia=soup.find('div',attrs={'class':'columns medium-9 large-5'})
    Facebook_Link=""
    Twitter_Link=""
    Instagram_Link=""
    for c in SocialMedia.find('ul',attrs={'class':'unstyled'}).find_all('a'):
        if 'facebook.com' in c.attrs['href']:
            Facebook_Link= c.attrs['href']
            Cast['FacebookLink']=Facebook_Link
        if 'instagram.com' in c.attrs['href']:
            Instagram_Link= c.attrs['href']
            Cast['InstagramLink']=Instagram_Link
        if 'twitter.com' in c.attrs['href']:
            Twitter_Link= c.attrs['href']
            Cast['TwitterLink']=Twitter_Link
    CastList.append(Cast)
#JSON
with open('Cast.json', 'w', encoding='utf-8') as n:
    json.dump(CastList, n)
## write data in CSV 
#filename = 'Cast.csv'
#with open(filename, 'w', newline='', encoding='utf-8') as f: 
    #w = csv.DictWriter(f,['CastID','Name','Image','Biography','BirthName','Nickname','DateOfBirth','BirthCountry','Nationality','FacebookLink','InstagramLink','TwitterLink']) 
    #w.writeheader() 
    #for Cast in CastList: 
        #w.writerow(Cast) 

pass
import requests
from bs4 import BeautifulSoup
import csv
import json
MoviesList = []
Movie_Genre = {}
filename = 'ids.txt'
ids = []
with open(filename, 'r') as f:
    ids = f.read().split()
for i in ids:
    MovieGenre = []
    URL_Movie_1 = "https://elcinema.com/en/work/"
    URL_Movie = URL_Movie_1+i
    r = requests.get(URL_Movie)  # get the data of the URL
    soup = BeautifulSoup(r.content, 'html5lib')
    Movies = {}
    MovieID_1 = i
    Movies['MovieID'] = MovieID_1
    Name_1 = soup.find('span', attrs={'class': 'left'})
    MovieName = Name_1.text.strip()
    Movies['Name'] = MovieName
    Duration_1 = soup.find('ul', attrs={'class': 'list-separator'})
    # Duration
    Movies['Duration'] = None
    Movies['Revenue'] = None
    Movies['Description'] = None
    Movies['Viewrship Rating'] = None
    Movies['Release Date'] = None
    MovieDuration_1 = Duration_1.contents[5].contents[0]
    if('minutes' in MovieDuration_1):
        MovieDuration = MovieDuration_1
        Movies['Duration'] = MovieDuration
    # Image
    MovieImage = soup.find('div', attrs={
                           'class': "columns small-12 medium-3 large-3"}).find('a').find('img').attrs['src']
    Movies['Image'] = MovieImage
    MovieRating = soup.find('div', attrs={'class': 'stars-orange-60'}).text
    Movies['MovieRating'] = MovieRating
    # Details start
    Details = soup.find_all('div', attrs={'class': 'columns large-10'})
    # Synopses start
    for i in Details:
        if(i.find("ul", attrs={'class': 'list-separator list-title'})) != None:
            Details = i
            break
    if(Details.find("p") != None):
        MovieDescription = Details.find(
            "p").text.lstrip().replace('...Read more', '')
        Movies['Description'] = MovieDescription
    # synopses end
    Details = Details.find_all(
        "ul", attrs={'class': 'list-separator list-title'})
    for i in Details:
        # revenue
        if (i.contents[1].contents[0] == 'Box Office:'):
            MovieTotalRevenue = i.contents[3].contents[0].split('\n')[
                1].lstrip()
            Movies['Revenue'] = MovieTotalRevenue
        # Censorship
        MovieViewrshipRating = None
        if(i.contents[1].contents[0] == 'Censorship:'):
            MovieViewrshipRating = i.contents[3].contents[0].contents[1].contents[0]
            Movies['Viewrship Rating'] = MovieViewrshipRating
        # Genres
        if(i.contents[1].contents[0] == 'Genre:'):
            Genre = i.find_all("li")
            genre = ""
            for j in range(1, len(Genre)):
                genre = Genre[j].text
                MovieGenre.append(genre)
        # MovieReleaseDate
        if(i.contents[1].contents[0] == 'Release Date:'):
            ReleaseDate = i.find_all("li")
            for i in ReleaseDate:
                if ('Egypt' in i.text.replace(']', '*').replace('[', '*').split('*')[0]):
                    MovieReleaseDate = i.text.replace(
                        ']', '*').replace('[', '*').split('*')[1]
                    if(MovieReleaseDate == "Released"):
                        Movies['Release Date'] = None
                    else:
                        Movies['Release Date'] = MovieReleaseDate
    MoviesList.append(Movies)
    Movie_Genre[MovieID_1] = MovieGenre
    # Details End
# write data in CSV
#filename = 'Movies.csv'
#with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
    #w = csv.DictWriter(f, ['MovieID', 'Name', 'Image', 'MovieRating', 'Duration',
                           #'Description', 'Revenue', 'Viewrship Rating', 'Release Date'])
    #w.writeheader()
    #for Movie in MoviesList:
        #w.writerow(Movie)
# Movies Json
with open('Movies.json', 'w', encoding='utf-8') as n:
    json.dump(MoviesList, n)
# Genre Json
with open('Genre.json', 'w', encoding='utf-8') as n:
    json.dump(Movie_Genre, n)
pass

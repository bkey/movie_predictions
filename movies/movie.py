import bomojo
import pickle
from bs4 import BeautifulSoup
from urlparse import urlparse
import urllib2
import re
import codecs

class BOMojoMovie():         
    def __init__(self):
	self.movie_title = ""
	self.release_date = ""
	self.domestic_gross = 0
	self.runtime = 0
	self.director = ""
	self.rating = ""
        self.writers = ""
        self.actors = ""
        self.distributor = ""
        self.genre = ""
        self.budget = ""

    def __init__(self, movie_data):
	self.movie_title = movie_data['movie title']
	self.release_date = movie_data['release date']
	self.domestic_gross = movie_data['domestic_total_gross']
	self.runtime = movie_data['runtime']
	self.director = movie_data['director']
	self.rating = movie_data['rating']
        self.writers = movie_data['writers']
        self.actors = movie_data['actors']
        self.distributor = movie_data['distributor']
        self.genre = movie_data['genre']
        self.budget = movie_data['budget']

    def __str__(self):
        s = ",".join([self.movie_title, str(self.release_date), str(self.domestic_gross), str(self.runtime), str(self.director).encode('ascii', 'ignore'), self.rating, self.genre, str(self.budget)])
        s = s + ',' +str(self.actors).encode('ascii', 'ignore') + "\n"
        #s = s + '\n'

        #sloooow
        return s
       
def pickle_dump_all_movies(movie_data):
    output = open('movie_data.pkl', 'wb')

    pickle.dumps(movie_data, output)

    output.close()

def pickle_load_all_movies(movie_data):
    input = open('movie_data.pkl', 'r')

    print pickle.loads(input)

#easier for stupid humans to reads ;-)
def string_dump_all_movies(movie_data):

    output = open("movie_data.csv", "wb")

    output.write('Title,ReleaseDate,DomesticTotalGross,Runtime,Director,Rating,Genre,Budget,Actors\n')

    for movie in movie_data:
        try:
            output.write(str(movie))
        except:
            print 'error writing ', movie.movie_title
            pass

    print 'write to movie_data.csv ', len(movie_data)

    output.close()


def get_from_top(bomj, movie_data):

    year = 2013

    for i in range(1,8):

        url = "http://boxofficemojo.com/yearly/chart/?page=%s&view=releasedate&view2=domestic&yr=%s" % (i,year)

        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)

        links = soup.findAll('a')

        for link in links:
            try:
                if 'movies/?id=' in link['href']:
                    if not "1 Movie:" in link.text: #ignore current #1 in country
                        print 'adding ', link.text
                        s = 'http://boxofficemojo.com%s' % link['href']
                        try:
                            movie_data.append(BOMojoMovie(bomj.parse_full_mojo_page(s)))
                        except:
                            print 'whhhaaaa?'
            except:
                #ignores a without href (why would you even want such a thing?)
                pass
    
        

if __name__ == "__main__":
    bomj = bomojo.BOMojoScraper()

    movie_data = []

    get_from_top(bomj,movie_data)

    string_dump_all_movies(movie_data)

    


    


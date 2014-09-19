# -*- coding: utf-8 -*-
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
        self.opening_wknd = 0

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
        self.opening_wknd = movie_data['opening_wknd']

    def __str__(self):
        s = ",".join([self.movie_title, str(self.release_date), str(self.domestic_gross), str(self.runtime), self.director, self.rating, self.genre, str(self.budget), str(self.opening_wknd)])
        s = s + ',' + self.actors + "\n"
        #s = s + '\n'
        
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

    with codecs.open("movie_data_priors.csv", 'w+', 'UTF-8') as f:

        f.write('Title,ReleaseDate,DomesticTotalGross,Runtime,Director,Rating,Genre,Budget,OpeningWeekend,Actors\n')

        for movie in movie_data:
            try:
                f.write(str(movie).encode('UTF-8', 'ignore'))
            except:
                print 'error writing ', movie.movie_title
                pass

    print 'write to movie_data.csv ', len(movie_data)

    f.close()


def get_from_top(bomj, year):

    movie_data = []

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
                            print 'error adding ' 
                            pass
            except:
                #ignores a without href
                pass

    return movie_data

if __name__ == "__main__":
    bomj = bomojo.BOMojoScraper()

    all_years = []

    for i in range(0,13):
        movie_data = get_from_top(bomj,2000 + i)
        for movie in movie_data:
            all_years.append(movie)
    #movie_data2013 = get_from_top(bomj,2013)
    string_dump_all_movies(all_years)

    


    


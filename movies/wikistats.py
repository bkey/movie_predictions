# -*- coding: utf-8 -*-
import re
import urllib2
import codecs
from collections import defaultdict
import csv
import json


class WikiStats():
    #e.g. http://stats.grok.se/en/201408/Johnny_Depp
    base_url = "http://stats.grok.se/en/%s/%s"
    json_url = "http://stats.grok.se/json/en/%s/%s"
    url_search = 'http://%s.wikipedia.org/w/api.php?action=query&list=search&srsearch=%s&sroffset=%d&srlimit=%d&format=yaml'
    wiki_url = "http://en.wikipedia.org/w/index.php?&title=%s"
    
    def wikify_name(self,name):
        name = name.replace(u' ',u'_').encode('utf-8')
        return urllib2.quote(name.encode('utf-8'))


    def test_wiki_page(self, wiki_name_str):
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]

        s = self.wiki_url % ( wiki_name_str )
        print wiki_name_str

        try:
            infile = opener.open(s)

            page = infile.read()
        except:
            print 'error opening page'
            return ""

        if 'Wikipedia does not have an article with this exact name' in page:
            print "No article with this exact name."
            return ""

        if 'redirected from' in page:
            print "redirected"
            return infile.url

        if 'This disambiguation page lists articles' in page:
            print "Disambiguation page, trying 'actor'"
            return self.test_wiki_page(wiki_name_str + '_(actor)')

        return wiki_name_str


    def get_stats_page(self, name_str):
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]

        page = None

        try:
            #print name_str
            infile = opener.open(name_str)

            page = infile.read()
        except:
            raise WikiError()

        return page

    def get_json_stats(self, date_str, star):
        s = self.json_url % (date_str, star.wiki_name )
        print s
        response = urllib2.urlopen(s)
        data = json.load(response)  

        days = data['daily_views']
        for key,val in days.items():
            print key
            star.wiki_page_views[key] = val


    def get_views_value_from_source(self,source):
        res = 0
        #print obj.text
        m = re.findall("has been viewed ([+-]?\d+)", source)
        if m:
            #print m[0]
            res = str(m[0])

        return res


    def open_page(self,date_str,name_str):

        #wiki_name = self.wikify_name(name_str)
        s = self.base_url % (date_str, name_str )

        source = self.get_stats_page(s)

        return source
        
    def get_views_with_date(self,date_str,name_str):
        source = self.open_page(date_str,name_str)
        if source <> None:
            return self.get_views_value_from_source(source)
        else:
            print 'no source'



class MovieStar():
   
    def __init__(self,name):
        self.bomojo_name = name
        self.wiki_name = ""
        self.wiki_page_views = defaultdict()

    def check_for_timeperiod(self,time_str,wiki_scraper):
        if time_str in page_views:
            return page_views[time_str]
        else:
            page_source = wiki_scraper.open_page(time_str,name_str)
            page_views[time_str] = wiki_scraper.get_views_value_from_source(source)

    def save_to_txt(self):
        filename = 'stars/' + self.bomojo_name + '.txt'
        with codecs.open(filename, 'w+', 'UTF-8') as f:
            for time_str, data in self.wiki_page_views.iteritems():
                f.write( "%s,%s\n" % (time_str,data) )
            f.close()

    def read_from_txt(self):
        with codecs.open('stars/' + self.name + '.txt', 'r', 'UTF-8') as f:
            for line in f:
                fields = line.split(",")
                self.wiki_page_views[fields[0]] = fields[1]
            
            f.close()


class MovieStars():

    list_of_stars = defaultdict(MovieStar)

    def read_actors_from_movies_csv(self):
        with open("movie_data.csv", "rb") as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                if row['Actors'] <> '':
                    movie_actors = row['Actors'].split(";")
                    for actor in movie_actors:
                        if actor not in self.list_of_stars:
                            print actor
                            self.list_of_stars[actor] = MovieStar(actor)
    
    def read_directors_from_movies_csv(self):
        with open("movie_data.csv", "rb") as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                if row['Director'] <> '':
                    director = row['Director']
                    self.list_of_stars[director] = MovieStar(director)

          
    def load_name_translation_table(self):
        with open("name_translation.txt", "rb") as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                if row['BOMojo Name'] in self.list_of_stars:
                    print row['BOMojo Name']
                    ms = self.list_of_stars[row['BOMojo Name']]
                    wiki_name = row['Wiki Name'].replace("*",",")
                    ms.wiki_name = row['Wiki Name']
            f.close()

    def save_name_translation_table(self):
         with open("name_translation3.txt", "w") as f:
            f.write("BOMojo Name,Wiki Name\n")
            for name,star in self.list_of_stars.iteritems():
                if not star.wiki_name == "":
                    wiki_name = star.wiki_name.replace(",","*")
                    f.write( "%s,%s\n" % (star.bomojo_name, wiki_name ))
            f.close()

    def test_all_wiki_pages(self,wikistats):
        for name,star in self.list_of_stars.iteritems():
            if star.wiki_name == "":
                name = wikistats.wikify_name(star.bomojo_name)
                star.wiki_name = wikistats.test_wiki_page(name)
            #else:
            #    star.wiki_name = wikistats.test_wiki_page(star.wiki_name)

            #save everytime because paranoia ;-)
            self.save_name_translation_table()




if __name__ == "__main__":        
    ws = WikiStats()

    ms = MovieStars()
    ms.read_actors_from_movies_csv()
   
    ms.load_name_translation_table()
    ms.test_all_wiki_pages(ws)
    
    for name,star in ms.list_of_stars.iteritems():
        print name
        for year in range(2010,2014):
            for month in range(1,13):
                time_str = "%04d%02d" % (year,month) 
                ws.get_json_stats(time_str,star)
        
        star.save_to_txt() 

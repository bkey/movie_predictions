# -*- coding: utf-8 -*-
import sys
import re
import urllib2
import scraper
from bs4 import BeautifulSoup
import dateutil.parser
import urlparse

class BOMojoScraper(scraper.Scraper):

    base_url = "http://www.boxofficemojo.com/"
    search_url = base_url + "search/?q=%s"

    def full_movie_dict_from_title(self,movie_name):
        return self.parse_full_mojo_page(self.get_full_page_url_from_title(movie_name))

    def get_full_page_url_from_title(self,movie_name):
        search_soup = self.search(movie_name)
        found_matches = search_soup.find(text=re.compile("Movie Matches"))
        if found_matches:
            matches_table = found_matches.parent.find_next_sibling("table")
            result_row = matches_table.find_all('tr')[1]
            full_page_url = urlparse.urljoin(self.base_url,result_row.find('a')['href'])

            return full_page_url

        # if we end up here without returning anything, we did not hit a match
        log_message = "[LOG: No match found for %s]" % movie_name
        print >> sys.stderr, log_message
        return -1


    def parse_full_mojo_page(self,full_page_url):
        soup = self.connect(full_page_url)

        release_date = self.to_date(
            self.get_movie_value(soup,'Release Date'))
        domestic_total_gross = self.money_to_int(
            self.get_movie_value(soup,'Domestic Total'))
        runtime = self.runtime_to_minutes(self.get_movie_value(soup,'Runtime'))
        director = self.get_movie_value(soup,'Director')
        rating = self.get_movie_value(soup,'MPAA Rating')
        writers = self.get_movie_value(soup, 'Writers')
        actors = self.get_actors_as_list(soup)
        distributor = self.get_movie_value(soup, 'Distributor:')
        genre = self.get_movie_value(soup, 'Genre:')
        budget = self.budget_to_int(self.get_movie_value(soup, 'Production Budget:'))
        opening_wknd = self.money_to_int(self.get_opening_weekend(soup))

        movie_dict = {
            'movie title':self.get_movie_title(soup),
            'release date':release_date,
            'domestic_total_gross':domestic_total_gross,
            'runtime':runtime,
            'director':director,
            'rating':rating,
            'writers':writers,
            'actors':actors,
            'distributor':distributor,
            'genre':genre,
            'budget':budget,
            'opening_wknd':opening_wknd
        }

        return movie_dict

    def get_actors_as_list(self,soup):
        result = []
        actor_links = soup.find_all('a', href=re.compile("Actor"))
        for link in actor_links:
            if not ":" in link.text:
                name = link.text.replace("*","")
                re.sub(r'\([^)]*\)', '', name)
                print name
                result.append(name)

        return ";".join(result)

    def get_opening_weekend(self,soup):
        obj = soup.find(text=re.compile("Opening"))
        if not obj: 
            return ""

        if obj.find_parent('td'):
            sibling_cell = obj.find_parent('td').findNextSibling()
            if sibling_cell:
                #print sibling_cell.text
                return sibling_cell.text
        else:
            return ""
            

    def get_movie_value(self,soup,value_name):
        '''
        takes a string attribute of a movie on the page and 
        returns the string in the next sibling object (the value for that attribute)
        '''
        obj = soup.find(text=re.compile(value_name))
        if not obj: 
            return ""
    
        # this works for most of the values
        next_sibling = obj.findNextSibling()
        if next_sibling:
            return next_sibling.text

        # this next part works for the director
        elif obj.find_parent('td'):
            sibling_cell = obj.find_parent('tr').findNextSibling()
            if sibling_cell:
                return sibling_cell.text.replace(",","")
        
        else:
            return ""


    def get_movie_title(self,soup):
        title_tag = soup.find('title')
        movie_title = title_tag.text.split('(')[0].strip()
        return movie_title.replace(",","")
    
    def to_date(self,datestring):
        return dateutil.parser.parse(datestring)

    def money_to_int(self,moneystring):
        try:
            moneystring = moneystring.strip()
            return int(moneystring.replace('$','').replace(',',''))
        except:
            return 0

    def budget_to_int(self,budgetstring):
        try:
            return int(float(budgetstring.replace('$','').replace(' million','')) * 1000000)
        except:
            return 0

    def runtime_to_minutes(self,runtimestring):
        rt = runtimestring.split(' ')
        try:
            return int(rt[0])*60 + int(rt[2])
        except:
            return 0

import scraper

class IMDBScraper(scraper.Scraper):
    stars_url = "http://www.imdb.com/search/name?gender=male%2Cfemale&count=100&sort=starmeter,asc&start={0}"
    titles_url = "http://www.imdb.com/search/title?at=0&count=100&sort=moviemeter,asc&title_type=feature&start={0}"

    stars_search_id = "name"
    titles_search_id = "title"

    def get_buzz_value(self,soup,names_list,search_id):
        for names in soup.find_all("td", class_=search_id):
            link = names.find('a')
            #print link.text
            names_list.append(link.text)

    def scrape_from_meter_list(self,url,search_id,num_pages):
        names_list = []
	for i in range(0,num_pages):
            val = (i * 100) + 1
	    s = url.format(val) 

            soup = self.connect(s)
            self.get_buzz_value(soup,names_list,search_id)

        return names_list
            

    def scrape_star_meter(self,num_pages):
        return self.scrape_from_meter_list(self.stars_url,self.stars_search_id,num_pages)
        
    def scrape_top_titles(self,num_pages):
        return self.scrape_from_meter_list(self.titles_url,self.titles_search_id,num_pages)

    


import requests
import urllib2
import math
import re
from bs4 import BeautifulSoup
from useragents import getUserAgent        
from proxies import getProxy
import logging
from simListParse import simListParse
from bgps import bgps
logging.basicConfig(level = logging.DEBUG, format='%(asctime)s -%(levelname)s - %(message)s')

logging.debug("this is a log message.")


class GoogleSearch:
    """
    Gets google search results and related search queries. Use getuseragent() to assign a random user agent string from a list,
    use bgps to load proxy.
    """
    #USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/ 58.0.3029.81 Safari/537.36"
    USER_AGENT=getUserAgent()
    PROXY_STRING=bgps()

    #PROXY_STRING=getProxy()<-these proxies are bad
    SEARCH_URL = "https://google.com/search"
    RESULT_SELECTOR = "h3.r a"
    #SIM_SELECTOR = "p._e4b a"<--this needs to be revisited
    SIM_SELECTOR = "div.card-section a"
    TOTAL_SELECTOR = "#resultStats"
    RESULTS_PER_PAGE = 10
    DEFAULT_HEADERS = [
            ('User-Agent', USER_AGENT),
            ("Accept-Language", "en-US,en;q=0.5"),
        ]
    
    def search(self, query, use_proxy = 1, num_results = 10):
        searchResults = []
        total = None
        sim_query_list = []
        pages = int(math.ceil(num_results / float(GoogleSearch.RESULTS_PER_PAGE)));
        for i in range(pages) :
            start = i * GoogleSearch.RESULTS_PER_PAGE
            proxy_handler=urllib2.ProxyHandler({'https' : GoogleSearch.PROXY_STRING})

            #Deal with proxy jazz
            if use_proxy == 1:
                opener = urllib2.build_opener(proxy_handler)
            else:
                opener = urllib2.build_opener()

            opener.addheaders = GoogleSearch.DEFAULT_HEADERS
            #################################################
            #Deal with getting 503'd
            response_is_200_Flag = False
            count = 0
            while (not response_is_200_Flag) and (count < 5):
                try:
                    response = opener.open(GoogleSearch.SEARCH_URL + "?q="+ urllib2.quote(query) + ("" if start == 0 else ("&start=" + str(start))))
                    response_is_200_Flag = True
                except:
                    count = count + 1
                    logging.debug("Blocked Query:"+query+" Attempts: "+count)
                    if count == 5:
                        logging.debug("Aborted on:"+query)
                    pass
            #################################################
            soup = BeautifulSoup(response.read(), "lxml")
            response.close()
            #################################################
            if total is None:
                totalText = soup.select(GoogleSearch.TOTAL_SELECTOR)[0].children.next().encode('utf-8')
                total = long(re.sub("[', ]", "", re.search("(([0-9]+[', ])*[0-9]+)", totalText).group(1)))
                sim_queries = soup.select(GoogleSearch.SIM_SELECTOR) #<-this is where we find the sims
                for item in sim_queries:
                    sim_query_list.append(simListParse(str(item)))
            #################################################
            results = self.parseResults(soup.select(GoogleSearch.RESULT_SELECTOR))
            if len(searchResults) + len(results) > num_results:
                del results[num_results - len(searchResults):]
            searchResults += results
        return SearchResponse(searchResults, total, sim_query_list);
        
    def parseResults(self, results):
        searchResults = [];
        for result in results:
            url = result["href"];
            title = result.text
            searchResults.append(SearchResult(title, url))
        return searchResults

class SearchResponse:
    def __init__(self, results, total, sims):
        self.results = results;
        self.total = total;
        self.sims = sims;
class SearchResult:
    def __init__(self, title, url):
        self.title = title
        self.url = url
        self.__text = None
        self.__markup = None
    
    def __str__(self):
        return  str(self.__dict__)
    def __unicode__(self):
        return unicode(self.__str__())
    def __repr__(self):
        return self.__str__()

if __name__ == "__main__":
    import sys
    search = GoogleSearch()
    i=1
    query = "python"
    count = 10
    response = search.search(query, count)
    print "Total results: ",str(response.total), "\n"
    for x in response.sims:
        print "Similar query: ",x
    print "\n"
    for result in response.results:
        print("RESULT #" +str (i) + ": "+ (result.url if result.url is not None else "[None]") + "\n\n")
        i+=1





























        

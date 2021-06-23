import sys
import requests
import csv

from multiprocessing import Process, Pool
from bs4 import BeautifulSoup


class Scraper():
    
    def __init__(self, urls_file, n, local_test=False):
        self.urls_file = urls_file
        self.n = n
        self.local_test = local_test


    def get_links(self, link, local_test = False):
        #discart url parameters
        raw_link = link.strip().split('?')[0].rstrip('/')
        found_links_list = []
        tuple_count_list = []

        try:
            if local_test:
                page_content = open(raw_link,'r').read()
            else:
                page_content = requests.get(raw_link).content
            
            soup = BeautifulSoup(page_content, 'html.parser')
            links_list = soup.find_all('a')
        except:
            print(f"Could Not get link: {raw_link}")
            links_list = []

        for link in links_list:
            href = link.get("href")
            #get only http and https links
            if href and (href.startswith('http') or href.startswith('https') or local_test):
                url_part = href.split('?')[0].rstrip('/')
                found_links_list.append(url_part)
                tuple_count_list.append((raw_link, url_part, 1))

        #return list of found links and a list with information to be lately processed
        return (found_links_list, tuple_count_list)


    #for each given url found all links from that considering a depth of n
    def found_links(self, url, n, output_file=None):   
        links_list = [url]
        result_tuple = set()
        
        while n > 0:
            pool = Pool()
            pool_result = pool.map(self.get_links, links_list)
            print("POOL RESULT: "+str(pool_result))
            
            del links_list[:]

            for result in pool_result:
                links_list+=result[0]
                result_tuple = result_tuple.union(set(result[1]))

            n -= 1
        
        #saves information to be lately processed
        if output_file:
            self.save_file(result_tuple, output_file)
            
        return result_tuple
        
    
    #start scraper process
    def scraper(self, base_output_file=None):
        process_list = []
        file_count = 0

        with open(self.urls_file,"r") as f:
            for url in f:
                print(url)
                p1 = Process(target=self.found_links, args=(url, self.n, f"{base_output_file}-{file_count}.csv"))
                p1.start()
                process_list.append(p1)
                file_count += 1

        for pi in process_list:
            pi.join()

    #save file
    def save_file(self, result, file):
        with open(file,'w+') as out:
            csv_out = csv.writer(out)
            csv_out.writerows(result)
               

if __name__ == '__main__':

    urls_base = sys.argv[1]
    n = int(sys.argv[2])
    base_output_file = sys.argv[3]

    s = Scraper(urls_base, n)
    s.scraper(base_output_file)

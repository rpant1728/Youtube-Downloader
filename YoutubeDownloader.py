import sys, re, os, selenium, time, argparse
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from urllib.request import urlopen, urlretrieve

class YoutubeDownloader(object):
    def __init__(self):
        self.driver = webdriver.Chrome()

    def download_video(self, directory, query):
        driver = self.driver
        download_link = "http://www.ssyoutube.com/watch?v=" + query.split("?v=")[1]
        driver.get(download_link)
        sleep(10)
        html = driver.page_source
        soup  = BeautifulSoup(html, "lxml")
        for a in soup.find_all('a'): 
            if "videoplayback" in a['href']:
                name = a['href'].split('=')[-1].replace("+", " ").replace("%28", "(").replace("%29", ")")
                urlretrieve(a['href'], directory + "/" + name + ".mp4")
                break
        driver.close()

    def parse_links(self, query):
        driver = self.driver
        driver.get(query)
        sleep(10)
        html = driver.page_source
        soup  = BeautifulSoup(html, "lxml")
        title = soup.select('yt-formatted-string.title > a:nth-child(1)')[0].text
        links = list()
        for a in soup.find_all('a'): 
            if "index=" in a['href']:
                links.append(a['href'].split('v=')[-1])

        return title, links

    def download_playlist(self, links, list_dir, number):
        driver = self.driver
        num = 0
        for link in links:  
            if(num == number):
                break
            num = num + 1     
            download_link = "http://www.ssyoutube.com/watch?v=" + link
            driver.get(download_link)
            time.sleep(15)
            html = driver.page_source
            soup  = BeautifulSoup(html, "lxml")
            for a in soup.find_all('a'): 
                if "videoplayback" in a['href']:
                    name = a['href'].split('=')[-1].replace("+", " ").replace("%28", "(").replace("%29", ")")
                    urlretrieve(a['href'], list_dir + "/" + name + ".mp4")
                    break
        driver.close()

    def create_base_directory(self, directory):
        direct = os.path.dirname(directory)
        if not os.path.exists(direct):
            os.makedirs(direct)
        else:
            direct = os.path.dirname(directory) 
        
        return direct

    def create_list_directory(self, directory, title):
        direct = os.path.dirname(os.path.join(directory, title))
        if not os.path.exists(direct):
            os.makedirs(direct)
        else:
            direct = os.path.dirname(directory, title)

        return direct
    
    def download(self, query, crawl_type, number, directory):
        direct = self.create_base_directory(directory)
        if(crawl_type == 'video'):
            self.download_video(direct, query)
        elif(crawl_type == 'playlist'):
            title, links = self.parse_links(query)
            list_dir = self.create_list_directory(direct, title)
            self.download_playlist(links, list_dir, number)

def main():
    parser = argparse.ArgumentParser(description='Youtube Downloader')
    parser.add_argument('-q', '--query', type=str, help='Link of video or playlist')
    parser.add_argument('-t', '--crawl_type', type=str, default='video', help="Options: 'video' | 'playlist'")
    parser.add_argument('-n', '--number', type=int, default=0, help='Number of videos to download from playlist: integer, -1 to download all')
    parser.add_argument('-d', '--directory', type=str, default='./Videos/', help='Directory to save results')
    # parser.add_argument('-l', '--headless', action='store_true', help='If set, script will be run headless')
    args = parser.parse_args()
    downloader = YoutubeDownloader()
    downloader.download(query=args.query,
                        crawl_type=args.crawl_type,
                        number=args.number,
                        directory=args.directory)

if __name__ == "__main__":
    main()

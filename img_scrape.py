import os
import sys
import urllib
from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup

#Based on solution here: https://stackoverflow.com/questions/18497840/beautifulsoup-how-to-open-images-and-download-them/18498480
def scrape(url, shoe_model):    
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    imgs = soup.findAll('img')

    os.chdir("shoe_images")
    os.mkdir(shoe_model)
    os.chdir("..")
    for img in imgs:
            imgUrl = img['src']
            if "https:" not in imgUrl:
                imgUrl = "https:" + imgUrl
            path = os.path.join(os.getcwd() + '\\' + "shoe_images\\" + shoe_model, os.path.basename(imgUrl))
            urlretrieve(imgUrl, path)
            print(os.path.basename(imgUrl))

if __name__ == '__main__':
    run = True
    
    if("-h" in sys.argv):
        run = False
        print("Run \"python img_scrape.py\" and answer prompt\nEnter \"q\" for either prompt to quit")
    
    while(run): 
        print("\nURL: ")
        url = input()
        if(url == "q"):
            break
        print("Shoe model / Folder name: " )
        folder = input()
        if(folder == "q"):
            break
        try:
            scrape(url, folder)
        except Exception as e:
            print(str(e))
            print("Error with scraping. Try again")

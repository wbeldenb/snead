import os
import traceback
import sys
import urllib
from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import json
import random

random.seed(100)

#Based on solution here: https://gist.github.com/stephenhouser/c5e2b921c3770ed47eb3b75efbc94799
def get_soup(url,header):
    return BeautifulSoup(urllib.request.urlopen(
        urllib.request.Request(url,headers=header)),
        'html.parser')

#Based on solution here: https://stackoverflow.com/questions/18497840/beautifulsoup-how-to-open-images-and-download-them/18498480
def scrape(url, train, shoe_model):   
    train_or_valid = None
    if train:
        train_or_valid = "train"
    else:
        train_or_valid = "validation"
    
    bing = False
    if "bing" in url:
        header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        soup = get_soup(url, header)
        imgs = soup.findAll("a", {"class":"iusc"})
        bing = True
    else:
        html = urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
        imgs = soup.findAll('img')
        print(imgs)
    
    os.chdir("data/")
    try:
        os.mkdir(shoe_model)
    except:
        print("Shoe model folder already exist")
    os.chdir("..")
    for img in imgs:
            if (bing):
                mad = json.loads(img["mad"])
                imgUrl = mad["turl"]
            else:
                try:
                    imgUrl = img["src"]
                except:
                    continue
                if "https:" not in imgUrl:
                    imgUrl = "https:" + imgUrl
                
            path = os.path.join(os.getcwd() + "\\" + "data\\" + shoe_model, str( int (random.random() * 1000)) + os.path.basename(imgUrl)) .replace("\\", "/").replace("?", "")
            
            if ".png" not in path or ".jpg" not in path:
                path = path + ".jpg"

            try:
                if(bing):
                    urlretrieve(imgUrl, path)
                else:
                    raw_img = urllib.request.urlopen(imgUrl).read()
                    f = open(path, 'wb')
                    f.write(raw_img)
                    f.close()
                print(os.path.basename(imgUrl))
            except:
                print("Could not get image: " + imgUrl)
                traceback.print_exc()

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
        
        print("Train or Test: ")
        train_string = input()
        train = True
        if (train_string.upper() != "TRAIN"):
            train = False
        elif (train_string == "q"):
            break

        print("Shoe model / Folder name: " )
        folder = input()
        if(folder == "q"):
            break
        try:
            scrape(url, train, folder.upper())
        except Exception as e:
            print(str(e))
            traceback.print_exc()
            print(url)
            print("Error with scraping. Try again")

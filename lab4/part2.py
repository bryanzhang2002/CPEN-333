#student name:
#student number:

import random    # used to randomly choose comic numbers 
import requests  # used to make HTTP get requests and to download comic images
import bs4       # used to parse the html file and locate the image file
import time      # used to estimate time duration to compare between the two methods 
import threading # used in the second portion of the program
      
def getComic(comicNumber: int) -> None:
    """
    This function downloads the image file associated with the specific 
      comicNumber on http://xkcd.com
    Use as is.
    """
    if not isinstance(comicNumber, int):             # a simple safeguard against non-integer values
        raise ValueError("Invalid comic number")
    
    url = f"http://xkcd.com/{comicNumber}/"
    
    try:
        comic = requests.get(url)     # GET request to get the webpage
        print(f"Comic #{comicNumber} status code: {comic.status_code} (200 means success)")
        # locate the image from the content 
        webpageContent = bs4.BeautifulSoup(comic.text,'html.parser')
        comicImageUrl = f"http:{webpageContent.select('#comic img')[0].get('src')}"
        # GET request to get the image file
        imageFile = requests.get(comicImageUrl) 
    except:
        print(f"Something is not right with {url}") 
    else:
        # save the image file (same folder as this python file)
        with open(f"comic{comicNumber}.{comicImageUrl[-3:]}", "wb") as outputfile: #assuming 3-char image extension only
            outputfile.write(imageFile.content)

comicCount = 5   # number of comics we are to download for each of the following program portions 

#############################
# 1st portion: we get the comics sequentially (no multithreading)
# Use this portion as is
list1 = random.sample(range(1, 100, 2), comicCount) # odd numbers only, not to overlap with the other part
start = time.time() # start time to get an estimate of the duration it takes to download the comics
for num in list1:
    getComic(num)
print()
print(f"Sequentially, it took {time.time() - start :.3f}s to download {comicCount} random comics")
print()

#############################
# 2nd portion: use multithreading - one thread for downloading each of the comics 
# You are to complete this portion
list2 = random.sample(range(2, 100, 2), comicCount) # even numbers only, not to overlap with the other part
start = time.time()

# Your code come below here
threads = []    # list for storing the threads
for i in range(comicCount):
    getComicthread = threading.Thread(target = getComic, args=(list2[i],))  # initializing thread
    threads.append(getComicthread)  # append to the list of threads
    getComicthread.start()  

for thread in threads:
    thread.join()   # join all threads before ending the program

# end of your code
print()
print(f"Using threading, it took {time.time() - start :.3f}s to download {comicCount} random comics")
print()
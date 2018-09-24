import urllib
import json
import numpy as np
import math
import pygame
import io
import sys
from threading import Lock, Thread

class FlickrImageLoader:
    def __init__(self,
                 searchQueries,
                 randomize,
                 maxImagesPerCategory):
        self._images = []
        self._lastImageChoices = []

        if searchQueries is None or len(searchQueries) == 0:
            return
        
        self._lock = Lock()
        
        for i in range(len(searchQueries)):
            self._images.append([])
            self._lastImageChoices.append(None)
                
        def makeFlickrApiUrl(options):
            query = []
            
            for key in options:
                query.append("=".join([ key, options[key] ]))
                
            query = "&".join(query)
            
            return "https://api.flickr.com/services/rest/?%s" % query
        
        def makeFlickrSearchUrl(query,
                                page):
            options = {
                "method": "flickr.photos.search",
                "api_key": "8cccb7028346a7af96f088188f142fdb",
                "text": urllib.quote(query),
                "sort": "relevance",
                "safe_search": "1",
                "content_type": "1",
                "page": str(page),
                "media": "photos",
                "format": "json",
                "nojsoncallback": "1",
                "privacy_filter": "1"
            }
            
            return makeFlickrApiUrl(options)
        
        def makeFlickrGetSizesUrl(photoId):
            options = {
                "method": "flickr.photos.getSizes",
                "api_key": "8cccb7028346a7af96f088188f142fdb",
                "photo_id": urllib.quote(str(photoId)),
                "format": "json",
                "nojsoncallback": "1"
            }
            
            return makeFlickrApiUrl(options)
        
        def getJson(url):
            reader = urllib.urlopen(url)
            
            return json.load(reader)

        def getFlickrImageIds(query):
            url = makeFlickrSearchUrl(query, 1)
            
            try:
                json = getJson(url)
                
                pages = int(json["photos"]["pages"])
                perPage = int(json["photos"]["perpage"])
            
                pages = np.arange(pages)
                ids = {}
                finished = False
                for page in pages:
                    url = makeFlickrSearchUrl(query, page)

                    try:
                        pageJson = getJson(url)
                        
                        for photo in pageJson["photos"]["photo"]:
                            ids[photo["id"]] = True
                            
                            if len(ids) == maxImagesPerCategory * 3:
                                finished = True
                                break
                            
                    except Exception:
                        pass
                            
                    if finished:
                        break

                ids = ids.keys()
                if randomize:
                    np.random.shuffle(ids)
                    
                return ids[0:maxImagesPerCategory]
            except Exception:
                return []

        def getFlickrImageUrl(id):
            url = makeFlickrGetSizesUrl(id)

            try:
                sizesJson = getJson(url)
                for size in sizesJson["sizes"]["size"]:
                    if size["label"] == "Large":
                        return size["source"]
            
            except Exception:
                pass
            
            return None
        
        def getFlickrImageUrls(query):
            url = makeFlickrSearchUrl(query, 1)

            try:
                json = getJson(url)
            
                pages = int(json["photos"]["pages"])
                perPage = int(json["photos"]["perpage"])
            except Exception:
                return []
            
            pages = np.arange(pages)
            if randomize:
                np.random.shuffle(pages)
                

            urls = {}
            finished = False
            for page in pages:
                url = makeFlickrSearchUrl(query, page)

                try:
                    pageJson = getJson(url)

                    for photo in pageJson["photos"]["photo"]:
                        id = photo["id"]
                        url = makeFlickrGetSizesUrl(id)

                        try:
                            sizesJson = getJson(url)
                            for size in sizesJson["sizes"]["size"]:
                                if size["label"] == "Large":
                                    urls[size["source"]] = True
                                    if randomize and len(urls) == int(maxImagesPerCategory * 1.5):
                                        finished = True
                                        break
                                    elif len(urls) == maxImagesPerCategory:
                                        finished = True
                                        break
                        except Exception:
                            pass
                        if finished:
                            break
                    if finished:
                        break
                except Exception:
                    pass
                
            urls = urls.keys()
                                
            if randomize:
                np.random.shuffle(urls)

            return urls[0:maxImagesPerCategory]
        
        def loadImageUrl(url):
            try:
                image = urllib.urlopen(url).read()
                image = io.BytesIO(image)
                return pygame.image.load(image)
            except Exception:
                return None
        
        def loader():
            urlsToLoad = []
            categoryId = 0
            for searchQuery in searchQueries:

                urlIds = getFlickrImageIds(searchQuery)

                count = 0
                for urlId in urlIds:
                    urlsToLoad.append([ count, categoryId, urlId ])
                    count = count + 1
                categoryId = categoryId + 1
            urlsToLoad.sort(key=lambda x: (x[0], x[1]))
            for urlToLoad in urlsToLoad:
                url = getFlickrImageUrl(urlToLoad[2])

                if not (url is None):
                    image = loadImageUrl(url)
                    if not (image is None):
                        self._lock.acquire()
                        self._images[urlToLoad[1]].append(image)
                        self._lock.release()

        loaderThread = Thread(target=loader,
                              name="Image loader thread",
                              args=[])
        loaderThread.daemon = True
        loaderThread.start()

    def getImage(self,
                 category,
                 width,
                 height):
        image = None
        self._lock.acquire()
        try:
            images = self._images[category]
            imageIds = range(len(images))
            np.random.shuffle(imageIds)
            imageId = None
            for imageId in imageIds:
                if len(imageIds) == 1 or not (imageId == self._lastImageChoices[category]):
                    break
            self._lastImageChoices[category] = imageId
            if not (imageId is None):
                image = images[imageId]
                if not (width == image.get_width()) or not (height == image.get_height()):
                    image = pygame.transform.smoothscale(image, (width, height))
                    images[imageId] = image
        except Exception:
            image = None
        self._lock.release()
        return image
            
loader = FlickrImageLoader([
    "christina aguilera",
    "britney spears"
], True, 200)

pygame.init()
screen = pygame.display.set_mode((800, 600))
height = screen.get_height()
width = screen.get_width()

count = 0
while True:
    if count % 30 == 0:
        screen.fill((0, 0, 0))
        imageA = loader.getImage(0, 400,600)
        imageB = loader.getImage(1, 400,600)
        if not (imageA is None):
            screen.blit(imageA, (0,0))
        if not (imageB is None):
            screen.blit(imageB, (400,0))
        pygame.display.flip()
    count = count + 1
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("exiting...")
                sys.exit(0)
                
        elif event.type == pygame.QUIT:
            print("exiting...")
            sys.exit(0)
    
    pygame.time.delay(100)

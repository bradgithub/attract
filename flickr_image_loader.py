import io
import sys
import math
import json
import time
import urllib
import pygame
import numpy as np
from threading import Lock, Thread

class FlickrImageLoader:
    def __init__(self,
                 searchQueries,
                 groupIds,
                 randomize,
                 maxImagesPerCategory,
                 infoCallback):
        if searchQueries is None or len(searchQueries) == 0:
            return
        
        images = []
        lastImageChoices = []
        lock = Lock()
        
        for i in range(len(searchQueries)):
            images.append([])
            lastImageChoices.append(None)
                
        def log(message):
            if not (infoCallback is None):
                infoCallback(message)
        
        def makeFlickrApiUrl(options):
            query = []
            
            for key in options:
                query.append("=".join([ key, options[key] ]))
                
            query = "&".join(query)
            
            return "https://api.flickr.com/services/rest/?%s" % query
        
        def makeFlickrSearchUrl(query,
                                groupId,
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
            
            if not (groupId is None):
                options["group_id"] = str(groupId)
            
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

        def getFlickrImageIds(query,
                              groupId):
            url = makeFlickrSearchUrl(query, groupId, 1)
            
            try:
                json = getJson(url)
                                
                pages = int(json["photos"]["pages"])
                pages = np.arange(pages)
                
                ids = {}
                finished = False
                for page in pages:
                    url = makeFlickrSearchUrl(query, groupId, page + 1)

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
                    
                return ids
            
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
        
        def loadImageUrl(url):
            try:
                image = urllib.urlopen(url).read()
                image = io.BytesIO(image)
                return pygame.image.load(image)
            except Exception:
                return None
        
        def loader():
            urlsToLoad = []
            classId = 0
            for searchQuery, groupId in zip(searchQueries, groupIds):
                log("Running " + str(searchQuery) + " search")

                urlIds = getFlickrImageIds(searchQuery, groupId)

                log("Retrieved " + str(len(urlIds)) + " possible image urls")
                
                count = 0
                for urlId in urlIds:
                    urlsToLoad.append([ count, classId, urlId ])
                    count = count + 1
                classId = classId + 1
                
            log("Retrieving images")
            
            urlsToLoad.sort(key=lambda x: (x[0], x[1]))
            for urlToLoad in urlsToLoad:
                if len(images[urlToLoad[1]]) < maxImagesPerCategory:
                    url = getFlickrImageUrl(urlToLoad[2])

                    if not (url is None):
                        image = loadImageUrl(url)
                        if not (image is None):
                            log("Retrieved class " + str(urlToLoad[1]) + " image url " + url)
                            with lock:
                                images[urlToLoad[1]].append(image)

        loaderThread = Thread(target=loader,
                              name="Image loader thread",
                              args=[])
        loaderThread.daemon = True
        loaderThread.start()

        def getImage(classId,
                     width,
                     height):
            image = None
            
            with lock:
                try:
                    _images = images[classId]
                    imageIds = range(len(_images))
                    np.random.shuffle(imageIds)
                    imageId = None
                    for imageId in imageIds:
                        if len(imageIds) == 1 or not (imageId == lastImageChoices[classId]):
                            break
                    lastImageChoices[classId] = imageId
                    if not (imageId is None):
                        image = _images[imageId]
                        if not (width == image.get_width()) or not (height == image.get_height()):
                            image = pygame.transform.smoothscale(image, (width, height))
                            _images[imageId] = image
                            
                except Exception:
                    image = None

            return image
        
        self.getImage = getImage
            
if __name__ == "__main__":
    def log(message):
        print(message)
                
    loader = FlickrImageLoader([
        "christina aguilera",
        "britney spears"
    ], [
        None,
        None
    ], True, 200, log)

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
        
        #pygame.time.delay(100)
        time.sleep(0.100)

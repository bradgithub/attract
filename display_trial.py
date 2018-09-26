import pygame

class DisplayTrial:
    def __init__(self,
                 screen):
        screenWidth = screen.get_width()
        screenHeight = screen.get_height()
        
        halfScreenWidth = int(screenWidth / 2.0);
        
        white = pygame.Color(255, 255, 255)
        red = pygame.Color(255, 0, 0)
        green = pygame.Color(0, 255, 0)
        yellow = pygame.Color(255, 255, 0)
        
        displayRadius = int(min(screenWidth, screenHeight) * 0.05)
        
        highlightImage = pygame.Surface((halfScreenWidth, screenHeight))
        highlightImage.fill((255, 255, 255))

        imageData = [ None ]
        gazePoint = [ None ]

        def setImage(imageA,
                     imageB=None):
            imageData[0] = None
            
            if not (imageA is None):
                if not (imageB is None):
                    imageData[0] = [ imageA, imageB ]
                    
                else:
                    imageData[0] = [ imageA ]
        
        def setGazePoint(xy):
            gazePoint[0] = xy
        
        def render():
            if not (imageData[0] is None):
                image = None
                
                if len(imageData[0]) is 2:
                    combinedImage = pygame.Surface((screenWidth, screenHeight))
                    combinedImage.fill((0, 0, 0))
                    
                    if not (gazePoint[0] is None):
                        x, y = gazePoint[0]
                        
                        if x <= 0.5:
                            combinedImage.blit(highlightImage, (0, 0))
                        
                        else:
                            combinedImage.blit(highlightImage, (halfScreenWidth, 0))
                            
                    combinedImage.blit(imageData[0][0],
                                        (int(screenWidth / 12.0),
                                        int(screenHeight / 12.0)))
                    
                    combinedImage.blit(imageData[0][1],
                                        (int(screenWidth * 7.0 / 12.0),
                                        int(screenHeight / 12.0)))
                        
                    image = combinedImage
                    
                else:
                    image = imageData[0][0]
                
                screen.blit(image, (0, 0))
                
                if not (gazePoint[0] is None):
                    x, y = gazePoint[0]
                    
                    x = int(x * screenWidth)
                    y = int(y * screenHeight)
                    
                    pygame.draw.circle(screen, green, (x, y), displayRadius, 4)
                    pygame.draw.circle(screen, white, (x, y), displayRadius, 2)
                
        self.setImage = setImage
        self.setGazePoint = setGazePoint
        self.render = render

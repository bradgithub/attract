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

        arousalPredictionImage = pygame.Surface((halfScreenWidth, screenHeight))

        imageData = [ None ]
        gazePoint = [ None ]
        arousalPrediction = [ None ]

        fontSize = 40
        fontColor = (255, 255, 255)
        font = pygame.font.Font("NotoSansMono-Bold.ttf", fontSize)

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
        
        def setArousalPrediction(arousalPrediction_):
            arousalPrediction[0] = arousalPrediction_
        
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
                            
                    if not (arousalPrediction[0] is None):
                        arousalPredictionImage.fill((0, 255, 0))
                        
                        score = str(int(abs(arousalPrediction[0] - 0.5) / 0.5 * 1000) / 10.0)
                        score = score[0:4] + "%"
                        renderedScore = font.render(score, 0, fontColor)
                        wordWidth, wordHeight = renderedScore.get_size()
                        arousalPredictionImage.blit(renderedScore, ( int((halfScreenWidth - wordWidth) / 2.0), int((screenHeight / 12.0 - wordHeight) / 2.0) ))
        
                        if arousalPrediction[0] > 0.5:
                            combinedImage.blit(arousalPredictionImage, (halfScreenWidth, 0))
                        
                        else:
                            combinedImage.blit(arousalPredictionImage, (0, 0))
                            
                    imageX = int(float(screenWidth * 4.0 / 12.0 - imageData[0][0].get_width()) / 2.0)
                    imageY = int(float(screenHeight * 10.0 / 12.0 - imageData[0][0].get_height()) / 2.0)
                            
                    combinedImage.blit(imageData[0][0],
                                        (imageX + int(screenWidth / 12.0),
                                        imageY + int(screenHeight / 12.0)))
                    
                    imageX = int(float(screenWidth * 4.0 / 12.0 - imageData[0][1].get_width()) / 2.0)
                    imageY = int(float(screenHeight * 10.0 / 12.0 - imageData[0][1].get_height()) / 2.0)
                    
                    combinedImage.blit(imageData[0][1],
                                        (imageX + int(screenWidth * 7.0 / 12.0),
                                        imageY + int(screenHeight / 12.0)))
                        
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
        self.setArousalPrediction = setArousalPrediction
        self.render = render

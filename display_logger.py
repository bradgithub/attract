import re
import pygame

class DisplayLogger:
    def __init__(self,
                 screen):
        screenWidth = screen.get_width()
        screenHeight = screen.get_height()
        
        minX = int(screenWidth * 0.05)
        maxX = int(screenWidth * 0.95)
        minY = int(screenHeight * 0.05)
        maxY = int(screenHeight * 0.95)
        
        fontSize = 20
        fontColor = pygame.Color("white")
        font = pygame.font.Font("NotoSansMono-Light.ttf", fontSize)

        spaceWidth = font.size(" ")[0]
        
        textLog = [ [] ]

        def splitText(text):
            lines = []
            
            for line in text.splitlines():
                words = []
                
                lines.append(words)
                
                for word in re.split("\s+", line):
                    words.append(word)
                    
            return lines
        
        def render(text):
            lines = splitText(text)
            
            for line in textLog[0]:
                lines.append(line)
                
            textLog[0] = []

            x = minX
            y = minY
            for line in lines:
                outputLine = None
                
                for word in line:
                    renderedWord = font.render(word, 0, fontColor)
                    
                    wordWidth, wordHeight = renderedWord.get_size()
                    
                    if x + wordWidth > maxX:
                        x = minX
                        y = y + wordHeight
                        
                    if y > maxY - wordHeight:
                        break
                    
                    if outputLine is None:
                        outputLine = []
                        textLog[0].append(outputLine)
                    
                    outputLine.append(word)
                    
                    screen.blit(renderedWord, (x, y))
                    
                    x = x + wordWidth + spaceWidth
                    
                x = minX
                y = y + wordHeight * 2

                if y > maxY - wordHeight:
                    break
                
        def clear():
            textLog[0] = []
            
        self.render = render
        self.clear = clear

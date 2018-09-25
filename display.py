import pygame
from threading import Lock

from display_logger import DisplayLogger
                
class Display:
    def __init__(self):
        pygame.init()

        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screenWidth = screen.get_width()
        self.screenHeight = screen.get_height()

        white = pygame.Color(255, 255, 255, 255)
        red = pygame.Color(255, 0, 0, 255)
        green = pygame.Color(0, 255, 0, 255)
        yellow = pygame.Color(255, 255, 0, 255)
        
        displayRadius = int(min(self.screenWidth, self.screenHeight) * 0.05)
        
        highlightImage = pygame.Surface((int(self.screenWidth / 2.0), self.screenHeight))
        highlightImage.fill((255, 255, 255))
        
        displayLogger = DisplayLogger(screen)
        
        inLoggingThread = True
        loggingLock = Lock()
        loggingQueue = [ [] ]
        
        def log(text):
            with loggingLock:
                loggingQueue[0].append(text)
        
        def mainloop():
            while True:
                if inLoggingThread:
                    oldLoggingQueue = [ [] ]
                    
                    with loggingLock:
                        oldLoggingQueue[0] = loggingQueue[0]
                        loggingQueue[0] = []
                        
                    output = []
                    for entry in reversed(oldLoggingQueue[0]):
                        output.append(str(entry))
                        
                    text = "\n".join(output)

                    screen.fill((40, 40, 40))
                    displayLogger.render(text)
                
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            print("exiting...")
                            sys.exit(0)
                            
                    elif event.type == pygame.QUIT:
                        print("exiting...")
                        sys.exit(0)
            
                pygame.time.delay(100)
                
        self.log = log
        self.mainloop = mainloop

if __name__ == "__main__":
    Display()

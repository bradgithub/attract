import pygame
from threading import Lock

from display_logger import DisplayLogger
from display_trial import DisplayTrial
                
class Display:
    def __init__(self):
        pygame.init()

        #screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        screen = pygame.display.set_mode((1000, 1000))
        self.screenWidth = screen.get_width()
        self.screenHeight = screen.get_height()
        
        displayLogger = DisplayLogger(screen)
        displayTrial = DisplayTrial(screen)
        
        displayLog = [ True ]
        loggingLock = Lock()
        loggingQueue = [ [] ]
        updateTrial = [ None ]
        stopLogging = [ None ]
        startLogging = [ None ]
        
        def log(text):
            with loggingLock:
                loggingQueue[0].append(text)
        
        def setUpdateTrial(updateTrial_):
            updateTrial[0] = updateTrial_
            
        def setStopLogging(stopLogging_):
            stopLogging[0] = stopLogging_
        
        def setStartLogging(startLogging_):
            startLogging[0] = startLogging_
        
        def mainloop():
            while True:
                if displayLog[0]:
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

                else:
                    screen.fill((0, 0, 0))
            
                    updateTrialSuccess = False
                    if not (updateTrial[0] is None):
                        updateTrialSuccess = updateTrial[0]()
                    
                    displayTrialSuccess = False
                    if updateTrialSuccess:
                        displayTrialSuccess = displayTrial.render()
                
                    pygame.display.flip()

                    if displayTrialSuccess:
                        if not (updateLogging[0] is None):
                            updateLogging[0]()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            print("exiting...")
                            sys.exit(0)
                            
                        elif event.key == pygame.K_SPACE:
                            displayLog[0] = not displayLog[0]

                    elif event.type == pygame.QUIT:
                        print("exiting...")
                        sys.exit(0)
            
                pygame.time.delay(100)
                
        self.log = log
        self.mainloop = mainloop
        self.setImage = displayTrial.setImage
        self.setGazePoint = displayTrial.setGazePoint
        self.setUpdateTrial = setUpdateTrial
        self.setUpdateLogging = setUpdateLogging

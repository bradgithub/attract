import re
import pygame

class Logger:
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
        #fontName = pygame.freetype.get_default_font()
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
        
        logger = Logger(screen)
        
        lines = [
            "President Donald Trump last week showed somewhat unexpected restraint when discussing the sexual assault allegations against Supreme Court nominee Brett Kavanaugh. His reserve has been deteriorating in recent days; he declared on Twitter on Friday that Kavanaugh's first accuser, Christine Blasey Ford, surely would have alerted the authorities if the incident was \"as bad as she says.\"",
            "Now that a second accuser, Deborah Ramirez, has come forward with sexual misconduct claims against Kavanaugh, the wheels are off the bus for the president.",
            "He said that Ramirez, who has said she was drinking during the alleged incident and that there are gaps in her memory, was \"totally inebriated and all messed up\" and dismissed her claims while speaking to reporters at the United Nations General Assembly on Tuesday after meeting with the president of Colombia.",
            "\"I think [Kavanaugh] is just a wonderful human being,\" Trump said. \"I think it is horrible what the Democrats have done. It is a con game; they are real con artists.\"",
            "Trump repeated the \"con\" claim multiple times and grew angrier as he spoke. \"Thirty-six years ago? Nobody ever knew about it? Nobody ever heard about it? And now a new charge comes up,\" Trump said. He said to \"take a look at the lawyers\" who \"are the same lawyers who have been fighting for years\" and worried that no one will want to go before \"this system\" to be a judge or politician in the current environment.",
            "\"I can tell you that false accusation and false accusations of all types are made against a lot of people,\" Trump, who himself has been accused of sexual misconduct by more than a dozen women, said. \"This is a high-quality person, and it would be a horrible insult to our country if this doesn't happen. And it'll be a horrible, horrible thing for future political people, judges, anything you want, it'll be a horrible thing. It cannot be allowed to happen.\"",
            "He then went back to attacking Democrats. \"The Democrats are playing a con game, C-O-N, a con game,\" he said. \"It's a shame.\"",
            "Trump doesn't believe Ramirez because she was drunk. So, allegedly, was Kavanaugh.",
            "Ford alleges that during the early 1980s when she and Kavanaugh were at a party in high school, he drunkenly pinned her to a bed, tried to take off her clothes, and covered her mouth when she screamed as another boy, his friend Mark Judge, looked on. Ramirez came forth on Sunday alleging that Kavanaugh exposed himself to her and thrust his genitals in her face while both were drunk at a party in college. Kavanaugh has vehemently denied both women's claims.",
            "Trump last week said Ford should be heard, but per his Tuesday comments, he doesn't appear to believe the same about Ramirez. He seized on the fact that she has said she was drinking during the alleged incident to attack her ? even though Kavanaugh was allegedly drunk during both incidents.",
            "\"The second accuser has nothing. The second accuser doesn't even know, she thinks maybe it could have been him, maybe not. She admits that she was drunk, she admits time lapses,\" Trump said when asked whether Ramirez should be invited to testify before the Senate Judiciary Committee on Thursday, as Ford and Kavanaugh have been.",
            "He continued, exasperated, \"This is a person, and this is a series of statements, that's going to take one of the most talented, one of the greatest intellects, from a judicial standpoint in our country, going to keep him off the United States Supreme Court?\"",
            "Trump isn't the only one in the White House who has been changing his tune on the allegations against Kavanaugh. Counselor to the president Kellyanne Conway last week also said that Ford should be heard, but in a call with White House surrogates on Monday, she reportedly defended Kavanaugh by saying he's better than Hollywood producer Harvey Weinstein and told CBS This Morning that the accusations are \"starting to feel like a left-wing conspiracy.\"",
            "President Donald Trump last week showed somewhat unexpected restraint when discussing the sexual assault allegations against Supreme Court nominee Brett Kavanaugh. His reserve has been deteriorating in recent days; he declared on Twitter on Friday that Kavanaugh's first accuser, Christine Blasey Ford, surely would have alerted the authorities if the incident was \"as bad as she says.\"",
            "Now that a second accuser, Deborah Ramirez, has come forward with sexual misconduct claims against Kavanaugh, the wheels are off the bus for the president.",
            "He said that Ramirez, who has said she was drinking during the alleged incident and that there are gaps in her memory, was \"totally inebriated and all messed up\" and dismissed her claims while speaking to reporters at the United Nations General Assembly on Tuesday after meeting with the president of Colombia.",
            "\"I think [Kavanaugh] is just a wonderful human being,\" Trump said. \"I think it is horrible what the Democrats have done. It is a con game; they are real con artists.\"",
            "Trump repeated the \"con\" claim multiple times and grew angrier as he spoke. \"Thirty-six years ago? Nobody ever knew about it? Nobody ever heard about it? And now a new charge comes up,\" Trump said. He said to \"take a look at the lawyers\" who \"are the same lawyers who have been fighting for years\" and worried that no one will want to go before \"this system\" to be a judge or politician in the current environment.",
            "\"I can tell you that false accusation and false accusations of all types are made against a lot of people,\" Trump, who himself has been accused of sexual misconduct by more than a dozen women, said. \"This is a high-quality person, and it would be a horrible insult to our country if this doesn't happen. And it'll be a horrible, horrible thing for future political people, judges, anything you want, it'll be a horrible thing. It cannot be allowed to happen.\"",
            "He then went back to attacking Democrats. \"The Democrats are playing a con game, C-O-N, a con game,\" he said. \"It's a shame.\"",
            "Trump doesn't believe Ramirez because she was drunk. So, allegedly, was Kavanaugh.",
            "Ford alleges that during the early 1980s when she and Kavanaugh were at a party in high school, he drunkenly pinned her to a bed, tried to take off her clothes, and covered her mouth when she screamed as another boy, his friend Mark Judge, looked on. Ramirez came forth on Sunday alleging that Kavanaugh exposed himself to her and thrust his genitals in her face while both were drunk at a party in college. Kavanaugh has vehemently denied both women's claims.",
            "Trump last week said Ford should be heard, but per his Tuesday comments, he doesn't appear to believe the same about Ramirez. He seized on the fact that she has said she was drinking during the alleged incident to attack her ? even though Kavanaugh was allegedly drunk during both incidents.",
            "\"The second accuser has nothing. The second accuser doesn't even know, she thinks maybe it could have been him, maybe not. She admits that she was drunk, she admits time lapses,\" Trump said when asked whether Ramirez should be invited to testify before the Senate Judiciary Committee on Thursday, as Ford and Kavanaugh have been.",
            "He continued, exasperated, \"This is a person, and this is a series of statements, that's going to take one of the most talented, one of the greatest intellects, from a judicial standpoint in our country, going to keep him off the United States Supreme Court?\"",
            "Trump isn't the only one in the White House who has been changing his tune on the allegations against Kavanaugh. Counselor to the president Kellyanne Conway last week also said that Ford should be heard, but in a call with White House surrogates on Monday, she reportedly defended Kavanaugh by saying he's better than Hollywood producer Harvey Weinstein and told CBS This Morning that the accusations are \"starting to feel like a left-wing conspiracy.\""
        ]
        
        i = 0
        n = 0
        while True:
            if i % 10 == 0 and n < len(lines):
                screen.fill((0, 0, 0))
                logger.render(lines[n])
                n = n + 1
            
            i = i + 1
            
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

if __name__ == "__main__":
    Display()

import random
import numpy as nPy
import pygame
import pickle
import time

# color definitions with rgb values
class Color:
    def __init__(self):
        self.white = (255, 255, 255)
        self.green = (156, 209, 73)
        self.red = (255, 0, 0)
        self.blue = (38, 66, 139)
        self.drkBlue = (50, 150, 255)

class Game:
    def __init__(self):
        # generation number showing and game scale
        self.scale = 1.5
        self.showGen = False
        self.gen = 0
        
        # game board size determined by scake
        self.gWidth = int(600 * self.scale)
        self.gHeight = int(400 * self.scale)

        self.sWidth = self.gWidth
        self.sHeight = self.gHeight
         
        self.pSize = int(10 * self.scale)
        self.fSize = int(10 * self.scale)
        self.pSpeed = 40
                 
        self.pCoords = []
        self.pLength = 1
        self.dir = "right"
        self.board = nPy.zeros((self.gHeight // self.pSize, self.gWidth // self.pSize))
        
        self.gameClose = False
     
        
        # starting location of snake
        self.x1 = self.gWidth / 2
        self.y1 = self.gHeight / 2
        
        self.r1, self.c1 = self.coordToStore(self.x1, self.y1)
        self.board[self.r1][self.c1] = 1
             
        self.cChange = 1
        self.rChange = 0
          
        self.rFood, self.cFood = self.foodGen()
        self.board[self.rFood][self.cFood] = 2
        self.survived = 0
        pygame.init()
        self.color = Color()
                  
        self.screen = pygame.display.set_mode((self.sWidth, self.sHeight)) 
        self.clock = pygame.time.Clock()
         
        self.font = pygame.font.SysFont("bahnschrift", int(18 * self.scale))
        self.prevDir = None
        self.step()
        
    def scoring(self, score):
        value = self.font.render(f"Score: {score}", True, self.color.white)
        self.screen.blit(value, [500 * self.scale, 10])
        
    def gens(self):
        if self.showGen:
            value = self.font.render(f"Generation: {self.gen}", True, self.color.white)
            self.screen.blit(value, [10, 10])
        
    def snakeGen(self):
        for i in range(len(self.pCoords) - 1, -1, -1):
            r, c = self.pCoords[i]
            x, y = self.storeToGame(r, c)
            if i == len(self.pCoords) - 1:
                # head color
                pygame.draw.rect(self.screen, self.color.blue, [x, y, self.pSize, self.pSize])
            else:
                pygame.draw.rect(self.screen, self.color.drkBlue, [x, y, self.pSize, self.pSize])
            
    def endScreen(self):
        mesg = self.font.render("Game Over", True, self.color.red)
        self.screen.blit(mesg, [2 * self.gWidth / 5, 2 * self.gHeight / 5 ])
        
    # checking for wall/body in a square
    def isUnsafe(self, r, c):
        if self.validIndex(r, c):
          if self.board[r][c] == 1:
              return 1
          return 0
        else:
          return 1

    # table with direction, food and danger data
    def getState(self):
        head_r, head_c = self.pCoords[-1]
        state = []
        state.append(int(self.dir == "left"))
        state.append(int(self.dir == "right"))
        state.append(int(self.dir == "up"))
        state.append(int(self.dir == "down"))
        state.append(int(self.rFood < head_r))
        state.append(int(self.rFood > head_r))
        state.append(int(self.cFood < head_c))
        state.append(int(self.cFood > head_c))
        state.append(self.isUnsafe(head_r + 1, head_c))
        state.append(self.isUnsafe(head_r - 1, head_c))
        state.append(self.isUnsafe(head_r, head_c + 1))
        state.append(self.isUnsafe(head_r, head_c - 1))
        return tuple(state)
    
    def getDist(self, r1, c1, r2, c2):
        return ((r2 - r1) ** 2 + (c2 - c1) ** 2) ** 0.5
                
    def validIndex(self, r, c):
        return 0 <= r < len(self.board) and 0 <= c < len(self.board[0])
      
    # converting coords to matrix/table form
    def storeToGame(self, r, c):
        x = c * self.pSize
        y = r * self.pSize
        return (x, y)
    def coordToStore(self, x, y):
        r = int(y // self.pSize)
        c = int(x // self.pSize)
        return (r, c)
    
    # randomly place food
    def foodGen(self):
        cFood = int(round(random.randrange(0, self.gWidth - self.fSize) / self.fSize))
        rFood = int(round(random.randrange(0, self.gHeight - self.fSize) / self.fSize))
        if self.board[rFood][cFood] != 0:
            rFood, cFood = self.foodGen()
        return rFood, cFood
    
    def gameOver(self):
        return self.gameClose
        
        
    def step(self, action="None"):
        if action == "None":
            action = random.choice(["left", "right", "up", "down"])
        else:
            action = ["left", "right", "up", "down"][action]

        reward = 0
        
        for event in pygame.event.get():
            pass
 
        # take action
        self.prevDir = self.dir
        if action == "left" and (self.dir != "right" or self.pLength == 1):
            self.cChange = -1
            self.rChange = 0
            self.dir = "left"
        elif action == "right" and (self.dir != "left" or self.pLength == 1):
            self.cChange = 1
            self.rChange = 0
            self.dir = "right"
        elif action == "up" and (self.dir != "down" or self.pLength == 1):
            self.rChange = -1
            self.cChange = 0
            self.dir = "up"
        elif action == "down" and (self.dir != "up" or self.pLength == 1):
            self.rChange = 1
            self.cChange = 0
            self.dir = "down"

 
        if self.c1 >= self.gWidth // self.pSize or self.c1 < 0 or self.r1 >= self.gHeight // self.pSize or self.r1 < 0:
            self.gameClose = True
        self.c1 += self.cChange
        self.r1 += self.rChange
        
        self.screen.fill(self.color.green)
        pygame.draw.rect(self.screen, (255, 255, 255), (0, 0, self.gWidth, self.gHeight), 1)

        
        xFood, yFood = self.storeToGame(self.rFood, self.cFood)
        pygame.draw.rect(self.screen, self.color.red, [xFood, yFood, self.fSize, self.fSize])
        
        self.pCoords.append((self.r1, self.c1))
        
        if self.validIndex(self.r1, self.c1):
            self.board[self.r1][self.c1] = 1
        
        if len(self.pCoords) > self.pLength:
            rd, cd = self.pCoords[0]
            del self.pCoords[0]
            if self.validIndex(rd, cd):
                self.board[rd][cd] = 0
 
        for r, c in self.pCoords[:-1]:
            if r == self.r1 and c == self.c1:
                self.gameClose = True
                
        self.snakeGen()
        self.scoring(self.pLength - 1)
        self.gens()
        pygame.display.update()
 
        # eating food and getting reward
        if self.c1 == self.cFood and self.r1 == self.rFood:
            self.rFood, self.cFood = self.foodGen()
            self.board[self.rFood][self.cFood] = 2
            self.pLength += 1
            reward = 1
        self.survived += 1

        # punishing death
        if self.gameClose:
            reward = -10
        self.survived += 1

        return self.getState(), reward, self.gameClose
    
    def runGame(self, generation):
        self.showGen = False
        self.gen = generation
        self.gens()
        pygame.display.update()

        # pass it to pickle file made in directory named generation
        filename = f"generation/{generation}.pickle"
        with open(filename, 'rb') as file:
            table = pickle.load(file)
        time.sleep(5)
        currentLength = 2
        stepsUnchanged = 0
        while not self.gameOver():
            if self.pLength != currentLength:
                stepsUnchanged = 0
                currentLength = self.pLength
            else:
                stepsUnchanged += 1
                

            state = self.getState()
            action = nPy.argmax(table[state])
            if stepsUnchanged == 1000:
                # stopping to prevent snake from learning to survive without food
                break
            self.step(action)
            self.clock.tick(self.pSpeed)
        if self.gameOver() == True:
            # snake dies
            self.screen.fill(self.color.green)
            pygame.draw.rect(self.screen, (255, 255, 255), (0, 0, self.gWidth, self.gHeight), 1)
            self.endScreen()
            self.gens()
            self.scoring(self.pLength - 1)
            pygame.display.update()
            time.sleep(5)
            pygame.quit()
        return self.pLength
    
class Agent():
    def __init__(self):
        # define starting Q learning parameters
        self.dRate = 0.95
        self.lRate = 0.01
        self.generations = 1.0
        self.genDiscount = 0.9992
        self.minGen = 0.001
        self.genCount = 25000
        self.table = nPy.zeros((2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4))
        self.environment = Game()
        self.score = []
        self.survived = []
        
    # switching from exploration and exploitation
    def getAction(self, state):
        # random action i.e. exploration
        if random.random() < self.generations:
            return random.choice([0, 1, 2, 3])
        
        # learned best action i.e. exploitation
        return nPy.argmax(self.table[state])
    
    def train(self):
        for i in range(1, self.genCount + 1):
            self.environment  = Game()
            hungrySteps = 0
            length = self.environment.pLength
            
            # to see updates on terminal
            if i % 25 == 0:
                print(f"Generation: {i}, score: {nPy.mean(self.score)}, survived: {nPy.mean(self.survived)}, generations: {self.generations}, lr: {self.lRate}")
                self.score = []
                self.survived = []
               
            # save latest model in multiples of 500
            if (i % 500 == 0):
                with open(f'generation/{i}.pickle', 'wb') as file:
                    pickle.dump(self.table, file)
                
            current_state = self.environment.getState()
            self.generations = max(self.generations * self.genDiscount, self.minGen)
            done = False
            while not done:
                # choose and take action
                action = self.getAction(current_state)
                new_state, reward, done = self.environment.step(action)
                
                # Q learning equation updating
                self.table[current_state][action] = (1 - self.lRate)\
                    * self.table[current_state][action] + self.lRate\
                    * (reward + self.dRate * max(self.table[new_state])) 
                current_state = new_state
                
                hungrySteps += 1
                if length != self.environment.pLength:
                    length = self.environment.pLength
                    hungrySteps = 0
                if hungrySteps == 1000:
                    # prevent looping or hungry survival
                    break
            
            # track length and score
            self.score.append(self.environment.pLength - 1)
            self.survived.append(self.environment.survived)



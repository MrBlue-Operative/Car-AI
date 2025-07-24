import pygame as py
from config import screen, BLACK, WIDTH, HEIGHT, YELLOW, scale, distribute, shift, inputs, RED
import math
import neuralNetwork as NN

class Car:
    def __init__(self, x, y, color, op=256):
        self.x = x
        self.y = y
        self.color = color
        self.score = 0
        self.speed = 0
        self.max_speed = 5
        self.acceleration = 0.2
        self.angle = 0 
        self.rotation_speed = 5
        self.width = 20
        self.height = 37
        self.running = False
        self.direction = 1

        self.car_image = py.image.load('car.png').convert_alpha()
        self.car_image = py.transform.scale(self.car_image, (self.width, self.height))
        self.car_image.set_alpha(op)

        self.leftside = 0
        self.rightside = 0

        self.rotated_rect = None 
        self.mask = None
        self.information = 0
        self.finalPlace = (500, 50)
        self.last_score_milestone = 0

        # --- AI ---

        self.brain = NN.NeuralNetwork4([5, 7, 5, 2])
        self.actions = []

        self.draw()



    def draw(self):
        rotated_surface = py.transform.rotate(self.car_image, -self.angle)
        self.rotated_rect = rotated_surface.get_rect(center=(self.x, self.y))
        
        # Draw the rotated car
        screen.blit(rotated_surface, self.rotated_rect.topleft)
        
        
        # Create mask for collision detection
        self.mask = py.mask.from_surface(rotated_surface)
        # uncomment this element in order to see the sensors
        self.information = self.sensor()
        self.information = self.refine(self.information)

        self.actions = self.brain.fit(self.information)


    def update(self):
        keys = py.key.get_pressed()
        if self.running:
            if keys[py.K_a] or self.actions[0]:
                self.angle -= self.rotation_speed * self.direction
            if keys[py.K_d] or self.actions[1]:
                self.angle += self.rotation_speed * self.direction
            
        if keys[py.K_w] or 1:
            self.running = True
            self.direction = 1  
            self.score += 0.1 * self.direction
        elif keys[py.K_s]:
            self.running = True
            self.direction = -1 
            self.score += 0.1 * self.direction 
        else:
            self.running = False

        if self.running:
            self.speed += self.acceleration
        else:
            self.speed -= self.acceleration

        if self.speed > self.max_speed:
            self.speed = self.max_speed
        elif self.speed < 0:
            self.speed = 0

        angle_radians = math.radians(self.angle)
        self.x += self.speed * math.sin(angle_radians) * self.direction
        self.y -= self.speed * math.cos(angle_radians) * self.direction
        
        # speed was suppoesed to go up
        current_milestone = int(self.score // 50)
        if current_milestone > self.last_score_milestone:
            self.max_speed += 1
            self.rotation_speed += 1
            self.last_score_milestone = current_milestone

        self.draw()

        return self.running



    def sensor(self, display=False):
        YELLOW = (0, 0, 0)
        length = 120
        angle_radians = math.radians(self.angle)
        information = []
        spread = 20

        north_x = self.x + length * math.sin(angle_radians)
        north_y = self.y - length * math.cos(angle_radians)
        
        east_x = self.x + length * math.cos(angle_radians - spread)
        east_y = self.y + length * math.sin(angle_radians - spread)
        
        west_x = self.x - length * math.cos(angle_radians + spread)
        west_y = self.y - length * math.sin(angle_radians + spread)

        res = distribute(self.x, self.y, north_x, north_y)
        dr = True
        for i in range(len(res) - 1):
            if dr:
                for road in roads:
                    if check(res[i][0], res[i][1], road):
                        dr = False
            else:
                information.append(res[i-1][0])
                information.append(res[i-1][1])
                if display:
                    py.draw.circle(screen, YELLOW, (res[i-1][0], res[i-1][1]), 4)
                break
        if dr:
            destx = north_x
            desty = north_y
            information.append(destx)
            information.append(desty)
            if display:
                py.draw.circle(screen, YELLOW, (destx, desty), 4)

        while len(information) != 2:
            information.append(0)

        
        
        res = distribute(self.x, self.y, east_x, east_y)
        dr = True
        for i in range(len(res) - 1):
            if dr:
                for road in roads:
                    if check(res[i][0], res[i][1], road):
                        dr = False
            else:
                information.append(res[i-1][0])
                information.append(res[i-1][1])
                if display:
                    py.draw.circle(screen, YELLOW, (res[i-1][0], res[i-1][1]), 4)
                break
        
        if dr:
            destx = east_x
            desty = east_y
            information.append(destx)
            information.append(desty)
            if display:
                py.draw.circle(screen, YELLOW, (destx, desty), 4)

        while len(information) != 4:
            information.append(0)
    

        res = distribute(self.x, self.y, west_x, west_y)
        dr = True
        for i in range(len(res) - 1):
            if dr:
                for road in roads:
                    if check(res[i][0], res[i][1], road):
                        dr = False
            else:
                information.append(res[i-1][0])
                information.append(res[i-1][1])
                if display:
                    py.draw.circle(screen, YELLOW, (res[i-1][0], res[i-1][1]), 4)
                break

        if dr:
            destx = west_x
            desty = west_y
            information.append(destx)
            information.append(desty)
            if display:
                py.draw.circle(screen, YELLOW, (destx, desty), 4)
        
        while len(information) != 6:
            information.append(0)

        spread = -10

        east_x = self.x + length * math.cos(angle_radians - spread)
        east_y = self.y + length * math.sin(angle_radians - spread)
        
        west_x = self.x - length * math.cos(angle_radians + spread)
        west_y = self.y - length * math.sin(angle_radians + spread)

        res = distribute(self.x, self.y, east_x, east_y)
        dr = True
        for i in range(len(res) - 1):
            if dr:
                for road in roads:
                    if check(res[i][0], res[i][1], road):
                        dr = False
            else:
                information.append(res[i-1][0])
                information.append(res[i-1][1])
                if display:
                    py.draw.circle(screen, YELLOW, (res[i-1][0], res[i-1][1]), 4)
                break
        
        if dr:
            destx = east_x
            desty = east_y
            information.append(destx)
            information.append(desty)
            if display:
                py.draw.circle(screen, YELLOW, (destx, desty), 4)

        while len(information) != 8:
            information.append(0)
    

        res = distribute(self.x, self.y, west_x, west_y)
        dr = True
        for i in range(len(res) - 1):
            if dr:
                for road in roads:
                    if check(res[i][0], res[i][1], road):
                        dr = False
            else:
                information.append(res[i-1][0])
                information.append(res[i-1][1])
                if display:
                    py.draw.circle(screen, YELLOW, (res[i-1][0], res[i-1][1]), 4)
                break

        if dr:
            destx = west_x
            desty = west_y
            information.append(destx)
            information.append(desty)
            if display:
                py.draw.circle(screen, YELLOW, (destx, desty), 4)
        
        while len(information) != 10:
            information.append(0)

        return information
    
    def refine(self, info):
        res = []
        for i in range(0, len(info)-1, 2):
            tempX = (info[i] - self.x) ** 2 
            tempY = (info[i+1] - self.y) ** 2
            res.append(1 - math.sqrt(tempX + tempY)/100)
        return res
    
    def get(self):
        t1 = (self.finalPlace[0] - self.x) ** 2
        t2 = (self.finalPlace[1] - self.y) ** 2
        return math.sqrt(t1 + t2) / 10

            

class Road:
    def __init__(self, x, y, width, height, angle):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = angle
        self.color = (120, 90, 0)

        # Create and cache the rotated surface and mask
        self.road_surface = py.Surface((self.width, self.height), py.SRCALPHA)
        py.draw.rect(self.road_surface, self.color, (0, 0, self.width, self.height))
        self.rotated_surface = py.transform.rotate(self.road_surface, -self.angle)
        self.rotated_rect = self.rotated_surface.get_rect(center=(self.x, self.y))
        self.mask = py.mask.from_surface(self.rotated_surface)

    def draw(self):
        # Just blit the pre-rotated surface
        screen.blit(self.rotated_surface, self.rotated_rect.topleft)
    
thickness = 10
# roads = [
#     Road(420, 350, thickness, 700, 0), Road(700, 350, thickness, 700, 0),
#     #Road(470, 280, thickness, 180, 15), Road(620, 280, thickness, 180, 60),
#     Road(510, 500, thickness, 200, 60), #Road(600, 330, thickness, 70, 0),
#     Road(650, 390, thickness, 115, 120), Road(650, 140, thickness, 115, 120),
#     Road(490, 300, thickness, 200, 50), Road(650, 320, thickness, 130, 50),

#     Road(560, 10, thickness, 280, 90), Road(560, 700, thickness, 280, 90),
#     Road(530, 630, thickness, 70, 0), Road(600, 630, thickness, 70, 0),
#     Road(510, 400, thickness, 200, 120)
# ]
roads = [Road(40, 300, thickness, 280, 0), Road(100, 110, thickness, 160, 50),
         Road(255 + 125, 60, thickness, 200 + shift, 90), Road(130, 300, thickness, 200, 0),
         Road(165, 170, thickness, 100, 50), Road(270 + 125, 140, thickness, 140 + shift, 90),
         Road(450 + shift, 35, thickness, 200, 76), Road(440 + shift, 120, thickness, 220, 80), 
         Road(580 + shift, 12, thickness, 80, 90), Road(660 + shift, 90, thickness, 180, 150),
         Road(585 + shift, 150, thickness, 120, 140), Road(620 + shift, 260, thickness, 150, 0),
         Road(705 + shift, 240, thickness, 150, 0), Road(595 + shift, 370, thickness, 100, 30),
         Road(590 + shift, 440, thickness, 80, 150), Road(610 + shift, 485, thickness, 30, 0), 
         Road(600 + shift, 500, thickness, 30, 50), Road(515, 510, thickness, 400 + shift, 90),
         Road(515, 580, thickness, 500 + shift, 90), Road(650 + shift, 573, thickness, 45, 70),
         Road(688 + shift, 360, thickness, 100, 20), Road(690 + shift, 440, thickness, 80, 150),
         Road(690 + shift, 518, thickness, 100, 25), Road(160, 450, thickness, 131, 150),
         Road(90, 510, thickness, 180, 145)]

def check(x, y, obj):
    if not obj.rotated_rect.collidepoint(x, y):
        return False
    
    mask_x = int(x - obj.rotated_rect.left)
    mask_y = int(y - obj.rotated_rect.top)
    
    if (0 <= mask_x < obj.mask.get_size()[0] and 
        0 <= mask_y < obj.mask.get_size()[1] and 
        obj.mask.get_at((mask_x, mask_y))):
        return True
    
    return False

class Car2:
    def __init__(self, x, y, color, op=256):
        self.x = x
        self.y = y
        self.color = color
        self.score = 0
        self.speed = 0
        self.max_speed = 5
        self.acceleration = 0.2
        self.angle = 0 
        self.rotation_speed = 5
        self.width = 20
        self.height = 37
        self.running = False
        self.direction = 1

        self.car_image = py.image.load('car2.png').convert_alpha()
        self.car_image = py.transform.scale(self.car_image, (self.width, self.height))
        self.car_image.set_alpha(op)

        self.leftside = 0
        self.rightside = 0

        self.rotated_rect = None 
        self.mask = None
        self.information = 0
        self.finalPlace = (500, 50)
        self.last_score_milestone = 0

        # --- AI ---

        self.brain = None
        self.actions = []

        self.draw()



    def draw(self):
        rotated_surface = py.transform.rotate(self.car_image, -self.angle)
        self.rotated_rect = rotated_surface.get_rect(center=(self.x, self.y))
        
        # Draw the rotated car
        screen.blit(rotated_surface, self.rotated_rect.topleft)
        
        
        # Create mask for collision detection
        self.mask = py.mask.from_surface(rotated_surface)

        self.actions = [0, 0]


    def update(self):
        keys = py.key.get_pressed()
        if self.running:
            if keys[py.K_a] or self.actions[0]:
                self.angle -= self.rotation_speed * self.direction
            if keys[py.K_d] or self.actions[1]:
                self.angle += self.rotation_speed * self.direction
            
        if keys[py.K_w]:
            self.running = True
            self.direction = 1  
            self.score += 0.1 * self.direction
        elif keys[py.K_s]:
            self.running = True
            self.direction = -1 
            self.score += 0.1 * self.direction 
        else:
            self.running = False

        if self.running:
            self.speed += self.acceleration
        else:
            self.speed -= self.acceleration

        if self.speed > self.max_speed:
            self.speed = self.max_speed
        elif self.speed < 0:
            self.speed = 0

        angle_radians = math.radians(self.angle)
        self.x += self.speed * math.sin(angle_radians) * self.direction
        self.y -= self.speed * math.cos(angle_radians) * self.direction
        
        # speed was suppoesed to go up
        current_milestone = int(self.score // 50)
        if current_milestone > self.last_score_milestone:
            self.max_speed += 1
            self.rotation_speed += 1
            self.last_score_milestone = current_milestone

        self.draw()

        return self.running


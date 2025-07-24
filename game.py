import pygame as py
import sys
from config import screen, WHITE, RED, FPS, check_collision, WIDTH, HEIGHT
import objects as obj

def Generation(agents, epoch):
    x = 80
    y = 400
    high_score = 0
    py.display.set_caption("Need For Speed: Temu Version")
    font = py.font.SysFont('Arial', 30)
    clock = py.time.Clock()

    best_Car = obj.Car(x, y, RED)
    player = obj.Car2(x, y, RED)
    best_Car.brain.load('brain.npz')

    carsCount = agents
    car = []
    for i in range(carsCount):
        car.append(obj.Car(x, y, RED))

    for c in car:
        c.brain.mutate(best_Car.brain)

    best_Car = None
    best_distance = 0


    running = True
    while running:
        clock.tick(FPS)
        screen.fill((100, 255, 100))
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
        for road in obj.roads:
            road.draw()
            for c in car:
                distance = c.score
                if distance >= best_distance:
                    best_distance = distance
                    best_Car = c 
                if check_collision(c, road):
                    car.remove(c)
            if check_collision(player, road):
                player.x = x
                player.y = y
                player.angle = 0


        player.update()
        # Uncomment here to visualize the brain of the car, its kinda messy so.. not my fault....
        #best_Car.brain.visualizer(730, 70)

        if len(car) == 0:
            running = False

        text_surface = font.render(f"Score: {int(best_Car.score)}", True, (0, 0, 0))
        highScore_surface = font.render(f"Agents: {int(len(car))}", True, (0, 0, 0))
        screen.blit(text_surface, (10, 10))
        screen.blit(highScore_surface, (170, 10))
        for c in car:
            state = c.update()
        

        if state:
            high_score = max(best_Car.score, high_score)    


        fps = clock.get_fps()
        fps_surface = font.render(f"FPS: {int(fps)}", True, (0, 0, 0))
        screen.blit(fps_surface, (10, 50))  
        # text = font.render(f"Epoch: {epoch}", True, (0, 0, 0))
        # screen.blit(text, (750, 20))

        py.display.flip()

    best_Car.brain.save('brain.npz')

epochs = 3
Agents = 35
Generation(Agents, 1)
for epoch in range(epochs-1):
    screen = py.display.set_mode((WIDTH, HEIGHT))
    Generation(Agents, epoch+2)



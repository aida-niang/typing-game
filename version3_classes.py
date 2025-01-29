#import the libraries :
import random
import pygame

#define the classes :
class screen :
    def __init__(self, backgroud_color, size, title) :
        self.size = size
        self.title = title
        self.background_color = backgroud_color

    
class Fruits :
    def __init__(self, fruit_image, fruit_x, fruit_y, speed_x, speed_y) :
        fruit_image = pygame.image.load('fruits/pasteque.png')
        self.size = fruit_image.get_size()
        self.fruit_x = fruit_x
        self.fruit_y = fruit_y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.gravity = 0.1



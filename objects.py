import pygame
from config import *

class Paddle:
    def __init__(self):
        self.reset()

    def reset(self):
        self.width = 64
        self.height = 16
        self.x = int((WIDTH / 2) - (self.width / 2))
        self.y = int(HEIGHT - (self.height * 2))
        self.speed = 480
        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)
        self.direction = 0

    def update(self, dt):
        self.direction = 0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left >= 0:
            self.x -= self.speed * dt
            self.direction = -60 * dt

        if keys[pygame.K_RIGHT] and self.rect.right <= WIDTH:
            self.x += self.speed * dt
            self.direction = 60 * dt
        
        self.rect.x = int(self.x)

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

class Ball:
    def __init__(self, x, y):
        self.reset(x, y)
    
    def reset(self, x, y):
        self.speed_x = 240
        self.speed_y = -240
        self.max_speed = 480
        self.radius = 8
        self.rect = pygame.Rect(x, y, self.radius * 2, self.radius * 2)
        self.prev_rect = self.rect.copy()
    
    def update(self, dt):
        self.prev_rect = self.rect.copy()
        
        self.rect.x += int(self.speed_x * dt)
        self.rect.y += int(self.speed_y * dt)

    def bounce(self, direction):
        if direction == 'x':
            self.speed_x *= -1
        elif direction == 'y':
            self.speed_y *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, CYAN, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)

class Brick:
    def __init__(self, x, y, health, width, height):
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.health = health
        self.colors = {4:BLUE, 3:GREEN, 2:YELLOW, 1:RED}
        self.is_alive = True
    
    def hit(self):
        self.health -= 1
        if self.health <= 0:
            self.is_alive = False

    def draw(self, screen):
        if not self.is_alive:
            return
        pygame.draw.rect(screen, self.colors[self.health], self.rect)

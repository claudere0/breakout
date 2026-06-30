import pygame
pygame.init()

WIDTH = 512
HEIGHT = 512
FPS = 60
ROWS = 8
COLS = 8

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
MAGENTA = (255,0,255)
CYAN = (0,255,255)
WHITE = (255,255,255)
BLACK = (0,0,0)

class Paddle:
    def __init__(self):
        self.reset()

    def reset(self):
        self.width = 64
        self.height = 16
        self.x = int((WIDTH / 2) - (self.width / 2))
        self.y = int(HEIGHT - (self.height * 2))
        self.speed = 8
        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)
        self.direction = 0

    def update(self):
        self.direction = 0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left >= 0:
            self.x -= self.speed
            self.direction = -1

        if keys[pygame.K_RIGHT] and self.rect.right <= WIDTH:
            self.x += self.speed
            self.direction = 1
        
        self.rect.x = int(self.x)

    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW, self.rect)

class Ball:
    def __init__(self, x, y):
        self.reset(x, y)
    
    def reset(self, x, y):
        self.speed_x = 4
        self.speed_y = -4
        self.max_speed = 8
        self.radius = 8
        self.x = x-self.radius
        self.y = y
        self.rect = pygame.Rect(x, y, self.radius * 2, self.radius * 2)
    
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

        self.rect.x = self.x
        self.rect.y = self.y

    def bounce(self, direction):
        if direction == 'x':
            self.speed_x *= -1
        elif direction == 'y':
            self.speed_y *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, CYAN, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("breakout")
        self.clock = pygame.time.Clock()
        self.screen_color = BLACK

        self.paddle = Paddle()
        self.ball = Ball(int(WIDTH//2-WIDTH//64), int(WIDTH-(WIDTH//64)*5))

        self.running = True

    def update(self):
        # if not self.live_ball:
        #     return

        # update objects(paddle, ball), handle_collisions(screen, paddle, bricks), check_game_state
        self.paddle.update()
        self.ball.update()



    def draw(self):
        self.screen.fill(self.screen_color)

        # draw ball, paddle, bricks, ui
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
                # elif event.key == pygame.K_r:
                #     self.restart()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
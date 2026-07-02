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
MAGENTA = (255,127,255)
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
        pygame.draw.rect(screen, WHITE, self.rect)

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
        pygame.draw.circle(screen, MAGENTA, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)

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

    def color(self):
        if self.health == 4:
            return BLUE
        elif self.health == 3:
            return GREEN
        elif self.health == 2:
            return YELLOW
        elif self.health == 1:
            return RED
        else:
            return

    def draw(self, screen):
        if not self.is_alive:
            return
        pygame.draw.rect(screen, self.colors[self.health], self.rect)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("breakout")
        self.clock = pygame.time.Clock()
        self.screen_color = BLACK

        self.paddle = Paddle()
        self.ball = Ball(int(WIDTH//2-WIDTH//64), int(WIDTH-(WIDTH//64)*6))
        self.craete_bricks()

        self.game_state = 0
        self.live_ball = False

        self.running = True

    def craete_bricks(self):
        self.bricks = []

        for row in range(ROWS):
            if row < 2:
                health = 4
            elif row < 4:
                health = 3
            elif row < 6:
                health = 2
            elif row < 8:
                health = 1

            for col in range(COLS):
                self.bricks.append(Brick(col * (WIDTH//COLS), row * (HEIGHT//16), health, WIDTH//COLS, HEIGHT//16))


    def restart(self):
        self.paddle.reset()
        self.ball.reset(int(WIDTH//2-WIDTH//64), int(WIDTH-(WIDTH//64)*6))
        self.create_bricks()

        self.game_state = 0
        self.live_ball = False

    def handle_collisions(self):
        # screen
        if self.ball.rect.right >= WIDTH:
            self.ball.rect.left = WIDTH
            self.ball.bounce('x')

        if self.ball.rect.left <= 0:
            self.ball.rect.left = 0
            self.ball.bounce('x')

        if self.ball.rect.top <= 0:
            self.ball.rect.top = 0
            self.ball.bounce('y')

        # paddle
        if self.ball.rect.colliderect(self.paddle.rect):
            self.ball.rect.bottom = self.paddle.rect.top
            self.ball.bounce('y')

            self.ball.speed_x += self.paddle.direction
            self.ball.speed_x = max(-self.ball.max_speed, min(self.ball.speed_x, self.ball.max_speed))

        # bricks
        for brick in self.bricks:
            if self.ball.rect.colliderect(brick.rect):
                brick.hit()
                if not brick.is_alive:
                    self.bricks.remove(brick)

                self.ball.bounce('x')
                self.ball.bounce('y')

                break

    def check_game_state(self):
        if self.ball.rect.bottom >= HEIGHT:
            self.game_state = -1
        
        if all(not brick.is_alive for brick in self.bricks):
            self.game_over = 1


    def update(self):
        # if not self.live_ball:
        #     return

        # update objects(paddle, ball), handle_collisions(screen, paddle, bricks), check_game_state
        self.paddle.update()
        self.ball.update()
        self.handle_collisions()

        if self.game_state != 0:
            self.live_ball = False

    def draw_text(self):
        pass

    def draw_ui(self):
        if self.game.state == 1:
            self.draw_text()

    def draw(self):
        self.screen.fill(self.screen_color)

        # draw ball, paddle, bricks, ui
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)

        for brick in self.bricks:
            brick.draw(self.screen)

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
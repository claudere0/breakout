import pygame
from config import *
from objects import *
from levels import *
pygame.init()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("breakout")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('monospace', 24)
        self.screen_color = BLACK

        self.paddle = Paddle()
        self.ball = Ball(int(WIDTH//2-WIDTH//64), int(WIDTH-(WIDTH//8))-16)
        self.level = 1
        self.build_level(1)
        self.create_bricks()

        self.state = MENU
        self.running = True

    def restart(self):
        self.state = MENU

    # alternative restart
    # def restart(self):
    #     self.start_level(self.level)

    def build_level(self, level):
        self.map = LEVELS[level-1]

    def create_bricks(self):
        self.bricks = []

        brick_w = WIDTH // COLS
        brick_h = HEIGHT // 16

        for row, line in enumerate(self.map):
            for col, health in enumerate(line):
                if health == 0:
                    continue

                x = col * brick_w
                y = row * brick_h

                self.bricks.append(Brick(x, y, health, brick_w, brick_h))

    def bricks_collision(self):
        for brick in self.bricks:

            if not self.ball.rect.colliderect(brick.rect):
                continue

            self.resolve_collision(brick.rect)

            brick.hit()

            if not brick.is_alive:
                self.bricks.remove(brick)

            break

    def resolve_collision(self, rect):
        if self.ball.prev_rect.bottom <= rect.top:
            self.ball.rect.bottom = rect.top
            self.ball.y = self.ball.rect.y
            self.ball.bounce("y")
            return "top"

        elif self.ball.prev_rect.top >= rect.bottom:
            self.ball.rect.top = rect.bottom
            self.ball.bounce("y")
            return "bottom"

        elif self.ball.prev_rect.right <= rect.left:
            self.ball.rect.right = rect.left
            self.ball.bounce("x")
            return "left"

        elif self.ball.prev_rect.left >= rect.right:
            self.ball.rect.left = rect.right
            self.ball.bounce("x")
            return "right"

        return None

    def paddle_collision(self):
        if self.ball.rect.colliderect(self.paddle.rect):
            side = self.resolve_collision(self.paddle.rect)

            if side == "top":
                self.ball.speed_x += self.paddle.direction
                self.ball.speed_x = max(-self.ball.max_speed, min(self.ball.speed_x, self.ball.max_speed))

    def wall_collision(self):
        if self.ball.rect.right >= WIDTH:
            self.ball.rect.right = WIDTH
            self.ball.bounce('x')

        if self.ball.rect.left <= 0:
            self.ball.rect.left = 0
            self.ball.bounce('x')

        if self.ball.rect.top <= 0:
            self.ball.rect.top = 0
            self.ball.bounce('y')

    def handle_collisions(self):
        self.wall_collision() # screen
        self.paddle_collision() # paddle
        self.bricks_collision() # bricks

    def check_game_state(self):
        if self.ball.rect.bottom >= HEIGHT:
            self.state = LOSE
        elif not self.bricks:
            self.state = WIN

    def update(self, dt):
        if self.state != PLAYING:
            return
        self.paddle.update(dt)
        self.ball.update(dt)
        self.handle_collisions()
        self.check_game_state()

    def draw_text(self, text, x, y):
        text_image = self.font.render(text, True, WHITE)
        self.screen.blit(text_image, (x, y))

    def draw_bricks(self):
        for brick in self.bricks:
            brick.draw(self.screen)

    def draw_objects(self):
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        self.draw_bricks()

    def draw(self):
        self.screen.fill(self.screen_color)
        if self.state == PLAYING:
            self.draw_objects()
        elif self.state == MENU:
            self.draw_text("CHOOSE LEVEL", WIDTH//4+52, HEIGHT // 16 + 160)
            self.draw_text("PRESS BUTTON FROM 1 TO 8", WIDTH//8 + 32, HEIGHT // 8 + 160)
            self.draw_text("TO SELECT LEVEL", WIDTH//4+24, HEIGHT // 4 + 128)
            self.draw_text("OR Q TO QUIT", WIDTH//4+52, HEIGHT // 4 + 160)
        elif self.state == WIN:
            self.draw_objects()
            self.draw_text("YOU WON!", WIDTH//4+64, HEIGHT // 2 + 64)
            self.draw_text("PRESS R TO RESTART", WIDTH//8 + 32, HEIGHT // 2 + 96)
            if self.level != 8:
                self.draw_text("PRESS N TO NEXT", WIDTH//8 + 64, HEIGHT // 2 + 128)
        elif self.state == LOSE:
            self.draw_objects()
            self.draw_text("YOU LOST!", WIDTH//4+70, HEIGHT // 2 + 64)
            self.draw_text("PRESS R TO RESTART", WIDTH//4, HEIGHT // 2 + 96)

        pygame.display.flip()

    def start_level(self, level):
        self.level = level
        self.build_level(level)
        self.create_bricks()
        self.paddle.reset()
        self.ball.reset(int(WIDTH//2-WIDTH//64), int(WIDTH-(WIDTH//8))-16)
        self.state = PLAYING

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
                elif event.key == pygame.K_r and self.state in (WIN, LOSE):
                    self.restart()
                if event.key == pygame.K_n and self.state == WIN and self.level != 8:
                    self.start_level(self.level+1)
                elif self.state == MENU:
                    if pygame.K_1 <= event.key <= pygame.K_8:
                        self.start_level(event.key - pygame.K_0)

    def run(self):
        while self.running:
            # self.clock.tick(FPS)
            dt = self.clock.tick(FPS)/1000
            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
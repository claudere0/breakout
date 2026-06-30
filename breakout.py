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

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("breakout")
        self.clock = pygame.time.Clock()

        self.running = True

    def update(self):
        # if not self.live_ball:
        #     return

        # update objects(paddle, ball), handle_collisions(screen, paddle, bricks), check_game_state

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.screen.fill(WHITE)
        # pass

    def draw(self):
        self.screen.fill(BLACK)

        # draw ball, paddle, bricks, ui

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
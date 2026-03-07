import pygame

class Game:
    def __init__(self, width=800, height=600, title="Fan Jumper"):
        self.width = width
        self.height = height
        self.title = title

        self.screen = None
        self.clock = None
        self.running = False

    def initialize(self):
        """Initialize pygame and create the window."""
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()
        self.running = True

    def draw(self):
        """
        Draw the frame.
        Override this in subclasses or extend it with your own logic.
        """
        self.screen.fill((0, 0, 0))  # Clear screen (black)

    def run(self):
        """Main game loop."""
        self.initialize()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.draw()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()

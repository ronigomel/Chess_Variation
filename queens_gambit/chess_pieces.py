import pygame


class Piece:
    def __init__(self, team, typee, img_file, placement):
        self.team = team
        self.type = typee
        self.alive = True
        self.is_killable = False
        self.img_file = img_file
        self.img = pygame.image.load(self.img_file)
        self.placement = placement

    def killed(self):
        self.alive = False

    def get_file(self):
        return self.img

    def killable(self):
        self.is_killable = True

    def risk_free(self):
        if self.is_killable:
            self.is_killable = False

    def get_team(self):
        return self.team

    def get_placement(self):
        return self.placement

    def print(self, x, y, screen):
        red = (255, 0, 0, 0)
        self.img = pygame.image.load(self.img_file).convert()
        self.img.set_colorkey(red)
        screen.blit(self.img, [x, y])
        pygame.display.flip()

    def set_placement(self, placement):
        self.placement = placement

    def delete(self, x, y, screen):
        screen.fill((0, 0, 0, 255))
        screen.blit(self.img, (x, y))
        pygame.display.flip()

    def get_type(self):
        return self.type

    def get_killable(self):
        return self.is_killable
import pygame

from pygame.sprite import Sprite

class Bullet(Sprite):
    """Eine Klasse zur Verwaltung der vom Schiff abgefeuerten Bullets."""
    def __init__(self, ai_game):
        """Ein Bullet-objekt an der aktuellen Position des Schiffes erstellen."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Bullet-Rect bei (0, 0) erstellen und die richtige Position festlegen
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Position des Bullets als Dezimalwert speichern
        self.y = float(self.rect.y)

    def update(self):
        """Bullet auf dem Bildschirm nach oben bewegen."""
        # Dezimalposition des Bullets aktualisieren
        self.y -= self.settings.bullet_speed
        # Position des Rechtecks aktualisieren
        self.rect.y = self.y

    def draw_bullet(self):
        """Das Bullet auf den Bildschirm zeichnen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
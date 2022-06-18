import sys, os
import pygame
from pygame.sprite import Sprite

def resource_path(relative_path):
    """Absoluter Pfad zur Ressource, funktioniert für PyInstaller."""
    try:
        # PyInstaller erstellt einen temporären Ordner und speichert den Pfad in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("images")
    return os.path.join(base_path, relative_path)


class Ship(Sprite):
    """Die Klasse Ship steuert das Schiff."""

    def __init__(self, ai_game):
        """Schiff initialisieren und Startposition festlegen."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Das Schiff-Image laden und sein Rect erhalten
        self.img_path = resource_path('ship.png')
        self.image = pygame.image.load(self.img_path)
        self.rect = self.image.get_rect()

        # Jedes neue Schiff in der unteren Mitte des Bildschirms beginnen
        self.rect.midbottom = self.screen_rect.midbottom

        # Dezimalwert für die horizontale Position des Schiffs speichern
        self.x = float(self.rect.x)

        # Bewegungs-flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Die Position des Schiffes anhand der Bewegungs-flags aktualisieren."""
        # Den X-Wert des Schiffes aktualisieren
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        
        # Rect-objekt von self.x aktualisieren
        self.rect.x = self.x
    
    def center_ship(self):
        """Das Schiff auf dem Bildschirm zentrieren."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def blitme(self):
        """Das Schiff an seiner aktuellen Position zeichnen."""
        self.screen.blit(self.image, self.rect)

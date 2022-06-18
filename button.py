import pygame.font

class Button:

    def __init__(self, ai_game, msg):
        """Button-Attributen initialisieren."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Festlegung der Abmessungen und Eigenschaften der Taste
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (0,0,0)
        self.font = pygame.font.SysFont(None, 48)

        # Erstellen des rect-objekt der Taste und zentrieren
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # msg auf der Button muss nur einmal vorbereitet werden
        self._prep_msg(msg)
        
    def _prep_msg(self, msg):
        """msg in ein gerendertes Bild verwandeln und den Text auf der Taste zentrieren."""
        self.msg_image = self.font.render(msg, True, self.text_color,
            self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        
    def draw_button(self):
        # Eine leere Taste zeichnen und dann eine Nachricht
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

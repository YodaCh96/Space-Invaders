class Settings:
    """Eine Klasse zum Speichern aller Einstellungen für Space Invaders."""

    def __init__(self):
        """Statischen Einstellungen des Spiels initialisieren."""
        # Bildschirmeinstellungen
        self.screen_width = 1200
        self.screen_height = 800

        # Schiffseinstellungen
        self.ship_limit = 3

        # Einstellungen für Bullets
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Alien Einstellungen
        self.fleet_drop_speed = 10
        
        # Wie schnell sich das Spiel beschleunigt
        self.speedup_scale = 1.2
        # Wie schnell die Punktwerte der Ausserirdischen steigen
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.offset = 11
        self.ship_speed = 0.7 * self.offset
        self.bullet_speed = 0.7 * self.offset
        self.alien_speed = 0.1 * self.offset

        # fleet_direction von 1 steht für rechts, -1 für links
        self.fleet_direction = 1

        # Punktestand
        self.alien_points = 50

    def increase_speed(self):
        """Geschwindigkeitseinstellungen und Alien-Punktewerte erhöhen."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

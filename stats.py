class GameStats:
    """Track-Statistiken für Space Invaders."""

    def __init__(self, ai_game):
        """Statistiken initialisieren."""
        self.settings = ai_game.settings
        self.reset_stats()

        # Space Invaders in einem inaktiven Zustand starten
        self.game_active = False

        # Der Highscore sollte nie zurückgesetzt werden
        self.high_score = 0

    def reset_stats(self):
        """Statistiken initialisieren, die sich während des Spiels ändern können."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

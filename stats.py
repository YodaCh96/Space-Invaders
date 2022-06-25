class GameStats:
    """Track-Statistiken fuer Space Invaders."""

    def __init__(self, ai_game):
        """Statistiken initialisieren."""
        self.settings = ai_game.settings
        self.reset_stats()

        # Space Invaders in einem inaktiven Zustand starten
        self.game_active = False

        # Der Highscore sollte nie zurueckgesetzt werden
        self.high_score = 0

    def reset_stats(self):
        """Statistiken initialisieren, die sich waehrend des Spiels aendern koennen."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

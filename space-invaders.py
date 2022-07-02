import sys, spidev, os, time
from time import sleep
from gpiozero import LightSensor, Buzzer
import pygame
from settings import Settings
from stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class SpaceInvaders:
    """Allgemeine Klasse zur Verwaltung von Spielelementen und Verhalten."""
    def __init__(self):
        """Das Spiel initialisieren und die Spiel-Ressourcen erstellen."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((
        self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Space Invaders")
        
        self.ldr = LightSensor(4)
        
        self.buzzer = Buzzer(21)
        
        # Definition von Channels
        self.swt_channel = 0
        self.vrx_channel = 1
        self.vry_channel = 2
        
        # Zeitverzoegerung, alle wie viel Sekunden ausgelesen wird
        self.delay = 0.5
         
        # SPI oeffnen
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
        self.spi.max_speed_hz=1000000

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Die Schaltflaeche Play
        self.play_button = Button(self, "Play")
    
    def run_game(self):
        """Die Hauptschleife fuer das Spiel wird hier gestartet."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()
    
    def _check_events(self):
        """Reagieren auf Tastendrucke und Mausereignisse."""
        
        self.swt_val = self.spi.xfer2([1,(8 + self.swt_channel) << 4, 0])
        self.swt_val = ((self.swt_val[1] & 3) << 8) + self.swt_val[2]
        self.vry_val = self.spi.xfer2([1,(8 + self.vry_channel) << 4, 0])
        self.vry_val = ((self.vry_val[1] & 3) << 8) + self.vry_val[2]
        
        # Taste vom Joystick wird gedrueckt
        print(self.swt_val)
        if self.swt_val == 0:
            self._fire_bullet()
        
        # Bewegung nach rechts
        if self.vry_val <= 1:
            self.ship.moving_right = True
        else:
            self.ship.moving_right = False
        
        # Bewegung nach links
        if self.vry_val >= 1015:
            self.ship.moving_left = True
        else:
            self.ship.moving_left = False
        
        # Auf Tastendrucke und Mausereignisse reagieren
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)
                #elif event.type == pygame.KEYDOWN:
                    #self._check_keydown_events(event)
                #elif event.type == pygame.KEYUP:
                    #self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        """Ein neues Spiel starten, wenn der Spieler auf Play klickt."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Zuruecksetzen der Spieleinstellungen
            self.settings.initialize_dynamic_settings()

            # Zuruecksetzen der Statistiken des Spiels
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Alle verbleibenden Aliens und Bullets entfernen
            self.aliens.empty()
            self.bullets.empty()

            # Eine neue Flotte erstellen und das Schiff zentrieren
            self._create_fleet()
            self.ship.center_ship()

            # Den Mauszeiger ausblenden
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Reagieren auf Tastendruecke."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
    
    def _check_keyup_events(self, event):
        """Reagieren auf Releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    
    def _ship_hit(self):
        """Reagieren darauf, dass das Schiff von einem Alien angegriffen wird."""
        # Dekrementieren von ships_left
        self.stats.ships_left -= 1
        # Scoreboard aktualisieren
        self.sb.prep_ships()

        if self.stats.ships_left > 0:
            # Alle verbleibenden Aliens und Bullets entfernen
            self.aliens.empty()
            self.bullets.empty()

            # Eine neue Flotte erstellen und das Schiff zentrieren
            self._create_fleet()
            self.ship.center_ship()

            sleep(self.delay)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
        
    def _fire_bullet(self):
        """Erstellen ein neues Bullet und fuegen es der Bullet-Gruppe hinzu."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.buzzer.on()
            sleep(0.03)
            self.buzzer.off()
    
    def _update_bullets(self):
        """Aktualisieren die Position der Bullets und loeschen die alten Bullets."""
        # Position der Bullets aktualisieren
        self.bullets.update()

        # Verschwundene Bullets loeschen
        for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()
    
    def _check_bullet_alien_collisions(self):
        """Reagieren auf Kollisionen zwischen Bullets und Aliens."""
        # Entferne alle Bullets und Aliens, die zusammengestossen sind
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points *len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        
        if not self.aliens:
            # Bestehende Bullets zerstoeren und neue Flotte erstellen
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Level erhoehen
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """Pruefen, ob die Flotte an einem Rand steht, und dann die Positionen aller Aliens in der Flotte aktualisieren."""
        self._check_fleet_edges()
        self.aliens.update()

        # Suche nach Kollisionen mit Alien-Schiffen
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # Suche nach Aliens, die auf den unteren Teil des Bildschirms treffen
        self._check_aliens_bottom()
    
    def _create_fleet(self):
        """Die Flotte der Aliens erstellen."""
        # Ein Alien erstellen und die Anzahl der Aliens in einer Reihe finden
        # Der Abstand zwischen den einzelnen Aliens entspricht der Breite eines Aliens
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Die Anzahl der Reihen von Aliens bestimmen, die auf den Bildschirm passen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) -
        ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Die komplette Flotte von Aliens erstellen
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
    
    def _check_fleet_edges(self):
        """Reagieren, wenn ein Alien eine Ecke erreicht hat."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Die gesamte Flotte fallen lassen und die Richtung der Flotte aendern."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_alien(self, alien_number, row_number):
        """Einen Alien erstellen und ihn in der Reihe platzieren."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number + 50
        self.aliens.add(alien)
    
    def _check_aliens_bottom(self):
        """Pruefen, ob Aliens den unteren Rand des Bildschirms erreicht haben."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _update_screen(self):
        """Die Bilder auf dem Bildschirm aktualisieren, und zum neuen Bildschirm wechseln."""
        if self.ldr.light_detected:
            self.screen.fill((255,255,255))
            self.sb.text_color = (0,0,0)
        else:
            self.screen.fill((0,0,0))
            self.sb.text_color = (255,0,0)
        self.sb.prep_score()
        self.sb.prep_high_score()
        self.sb.prep_level()
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()

        # Den Play-Button zeichnen, wenn das Spiel inaktiv ist.
        if not self.stats.game_active:
            self.play_button.draw_button()
            
        pygame.display.flip()

if __name__ == '__main__':
    game = SpaceInvaders()
    # Spiel starten
    game.run_game()

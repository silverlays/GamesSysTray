from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from game import Game
from icons import Icons


class GameAction(QAction):
  def __init__(self, parent: QWidget, game: Game):
    self.game = game
    super().__init__(self.game.icon, self.game.name, parent)
  
  def launchGame(self):
    try:
      self.game.launch()
    except OSError as e:
      if e.errno == 22: # Elevation required
        QMessageBox.critical(self.parent(), 'ERREUR', 'Impossible de démarrer le jeu.\n\nRedémarrer en mode administrateur pour éviter cette erreur.')  
    except Exception as e:
      QMessageBox.critical(self.parent(), 'ERREUR', f'Une erreur est survenue:\n\n{e.args[1]}')
  

class CustomSysTrayWidget(QSystemTrayIcon):
  actions = []


  def __init__(self, parent: QWidget):
    super().__init__(parent)
    self.setIcon(Icons.appIcon())
    self.activated.connect(self._systrayDoubleClicked)


  def reload(self, games: list[Game]):
    self.systray_menu = QMenu()
    self.actions = []

    for game in games:
      game: Game
      action = GameAction(self.parent(), game)
      action.triggered.connect(action.launchGame)
      self.actions.append(action)
      self.systray_menu.addActions(self.actions)
    self.systray_menu.addSeparator()
    self.systray_menu.addAction(Icons.appIcon(), 'Afficher l\'interface', self.showInterfaceEvent)
    self.systray_menu.addSeparator()
    self.systray_menu.addAction(Icons.quitIcon(), 'Quitter', self.quitEvent)
    
    self.systray_menu.setFont(QFont('Segoe UI', 12)) # FONT & SIZE WILL BE DEFINED IN SETTINGS LATER

    self.setContextMenu(self.systray_menu)
    self.setToolTip(f'{len(games)} game(s)')
  

  def _systrayDoubleClicked(self, reason: QSystemTrayIcon.ActivationReason):
    if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
      self.showInterfaceEvent()

  def showInterfaceEvent(): pass # OVERRIDED BY CALLER
  def quitEvent(): pass # OVERRIDED BY CALLER

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from games_controller import Game
from icons import Icons
from static import *


class GameAction(QAction):
  def __init__(self, parent: QSystemTrayIcon, index: int, game: Game):
    super().__init__(icon=game.icon, text=game.name, parent=parent)
    self.index = index
    self.game = game
    self.triggered.connect(lambda: GameAction.launchGame(self.index))

  @staticmethod
  def launchGame(index: int): pass # OVERRIDED BY APP


class SystrayCustomWidget(QSystemTrayIcon):
  actions = []
  show_mainwindow = Signal()
  quit = Signal()


  def __init__(self):
    super().__init__()
    self.setIcon(Icons.appIcon())
    self.activated.connect(self._activatedSlot)


  @Slot(QSystemTrayIcon.ActivationReason)
  def _activatedSlot(self, reason: QSystemTrayIcon.ActivationReason):
    if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
      self.show_mainwindow.emit()


  def refresh(self, games: list[Game]):
    self.systray_menu = QMenu()
    self.actions = []

    for game in games:
      game: Game
      index = len(self.actions)
      action = GameAction(self.parent(), index, game)
      self.actions.append(action)

    self.systray_menu.addActions(self.actions)

    self.systray_menu.addSeparator()
    self.systray_menu.addAction(Icons.appIcon(), 'Afficher l\'interface', self.show_mainwindow.emit)
    self.systray_menu.addSeparator()
    self.systray_menu.addAction(Icons.quitIcon(), 'Quitter', self.quit.emit)
    
    self.systray_menu.setFont(QFont('Segoe UI', 12)) # FONT & SIZE WILL BE DEFINED IN SETTINGS LATER

    self.setContextMenu(self.systray_menu)
    self.setToolTip(f'{APP_TITLE} v{APP_VERSION}\n{len(games)} game(s)')

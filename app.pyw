import sys
from PySide6.QtCore import *
from PySide6.QtWidgets import QApplication

from window_main import MainWindow
from systray import SystrayCustomWidget, GameAction

from icons import Icons
from games_controller import GamesController, Game
from static import *


app = QApplication(sys.argv)
app.setWindowIcon(Icons.appIcon())


class Main():
  def __init__(self):
    self.games_controller = GamesController(settings_path=SETTINGS_PATH)
    self.mainwindow = MainWindow()
    self.systray = SystrayCustomWidget()
    
    # Signals
    self.mainwindow.game_added.connect(self._addGameSlot)
    self.mainwindow.game_deleted.connect(self._deleteGameSlot)
    self.mainwindow.game_edited.connect(self._editGameSlot)
    self.mainwindow.launch_game.connect(self.games_controller.launchGame)
    self.systray.show_mainwindow.connect(self.mainwindow.show)
    self.systray.quit.connect(self.mainwindow.quit)

    # Events
    self.mainwindow.retreiveGame = self.games_controller.getGameFromIndex
    GameAction.launchGame = self.games_controller.launchGame

    self._refreshGames()
    self.systray.show()
    # self.mainwindow.show() # DEBUG

    sys.exit(app.exec())


  @Slot(str, str, str)
  def _addGameSlot(self, name: str, path: str, args: str):
    self.games_controller.addGame(name, path, args)
    self._refreshGames()


  @Slot(int)
  def _deleteGameSlot(self, index: int):
    self.games_controller.deleteGame(index)
    self._refreshGames()


  @Slot(int, Game)
  def _editGameSlot(self, index: int, game: Game):
    self.games_controller.editGame(index, game)
    self._refreshGames()


  def _refreshGames(self):
    self.mainwindow.refresh(self.games_controller.games)
    self.systray.refresh(self.games_controller.games)



if __name__ == '__main__':
  app.setStyle("Fusion")
  Main()

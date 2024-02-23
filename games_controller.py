import json
import os
import subprocess

from PySide6.QtCore import *
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFileIconProvider, QMessageBox


class Game(QObject):
  def __init__(self, name: str, path: str, args: str):
    super().__init__()
    self.name = name
    self.path = path
    self.args = args
    self.icon = self._generateIcon()


  def _generateIcon(self) -> QIcon:
    self.icon = QIcon(QFileIconProvider().icon(QFileInfo(self.path)))
    pixmap = self.icon.pixmap(48, 48)
    pixmap = pixmap.scaled(64, 64)
    return QIcon(pixmap)



class GamesController(QObject):
  games: list[Game] = []

  def __init__(self, settings_path: str):
    self.settings_path = settings_path
    self._loadData()


  def _loadData(self) -> None:
    try:
      with open(self.settings_path, 'r') as file: games_json = json.load(file)
      for game in games_json: self.games.append(Game(game['Name'], game['Path'], game['Args']))
    except (IOError, json.JSONDecodeError): 
      with open(self.settings_path, 'w') as file:
        json.dump([], file, indent=2)
        self.games = []


  def _saveData(self) -> None:
    self.games = sorted(self.games, key=lambda x: x.name)
    games_json = []
    for game in self.games:
      game_json = {
        "Name": game.name,
        "Path": game.path,
        "Args": game.args
      }
      games_json.append(game_json)
    with open(self.settings_path, 'w') as fp: json.dump(games_json, fp, indent=2)


  def addGame(self, name: str, path: str, args: str):
    self.games.append(Game(name, path, args))
    self._saveData()


  def deleteGame(self, index: int):
    game = self.games[index]
    self.games.remove(game)
    self._saveData()


  def editGame(self, index: int, game: Game):
    self.games[index] = game
    self._saveData()


  def getGameFromIndex(self, index: int) -> Game:
    return self.games[index]


  def launchGame(self, index: int) -> None:
    game = self.getGameFromIndex(index)
    
    if os.path.exists(game.path):
      gssPath = os.path.abspath(os.curdir)
      exePath = os.path.dirname(game.path)
      exeName = os.path.basename(game.path)
    try:
      os.chdir(exePath)
      os.system(f"{exeName} {game.args}")
      os.chdir(gssPath)
    except Exception as e:
      QMessageBox.critical(self, 'ERREUR', f'Une erreur est survenue:\n\n{e.args[1]}')

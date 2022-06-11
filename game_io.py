import json
import sys
from PyQt6.QtWidgets import QMessageBox
from game import Game


class GameIO():
  def __init__(self, settings_path):
    self.settings_path = settings_path


  def loadData(self) -> list[Game]|None:
    try:
      with open(self.settings_path, 'r') as file:
        games_json = json.load(file)
        games_json = sorted(games_json, key=lambda x: x['Name'])

        games = []
        for d in games_json: games.append(Game(d))
        
        return games
    except IOError: 
      with open(self.settings_path, 'w') as file:
        json.dump([], file, indent=2)
        return []
    except json.JSONDecodeError:
      QMessageBox.critical(None, 'ERROR', f'Une erreur est survenue lors du chargement de {self.settings_path}.\n\nSupprimez ou corrigez le fichier puis réessayez.')
      sys.exit()


  def saveData(self, games: list[Game]):
    games_json = []
    games = self.sort(games)

    with open(self.settings_path, 'w') as file:
      for game in games:
        games_json.append(game.jsonOutput())

      json.dump(games_json, file, indent=2)
  
  
  def sort(self, games: list[Game]) -> list[Game]:
    return sorted(games, key=lambda x: x.name)
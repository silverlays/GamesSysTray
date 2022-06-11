import os
import subprocess
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class Game():
  def __init__(self, game_dict: dict = None):
    try:
      self.name = game_dict['Name']
      self.path = game_dict['Path']
      self.arguments = str(game_dict['Args']).strip('"')
      self.icon = QIcon(QFileIconProvider().icon(QFileInfo(game_dict['Path'])))
    except: raise Exception('Cannot create game object.')


  def launch(self):
    if os.path.exists(self.path):
      path = os.path.dirname(self.path)
      exe = os.path.basename(self.path)
      os.chdir(path)
      subprocess.Popen(executable=exe, args=self.arguments)


  def jsonOutput(self):
    return self.convertToDict(self.name, self.path, self.arguments)


  @staticmethod
  def convertToDict(name: str, path: str, args: str):
    return {
      "Name": name,
      "Path": path,
      "Args": args
    }
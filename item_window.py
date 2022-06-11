import os
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from game import Game
from icons import Icons


class ItemWindow(QWidget):
  game: Game


  def __init__(self, parent: QWidget, game: Game = None) -> None:
    super().__init__(parent, Qt.WindowType.Dialog)
    self.setWindowIcon(Icons.appIcon())
    self.setWindowModality(Qt.WindowModality.WindowModal)
    self.setMinimumWidth(600)
    self.game = game

    if game:
      self.setWindowTitle(f'Modification du jeu - {game.name}')
    else:
      self.setWindowTitle('Ajout d\'un nouveau jeu')
    
    self._setupUi()


  def _setupUi(self):
    self.game_name_editbox = QLineEdit()
    if self.game: self.game_name_editbox.setText(self.game.name)

    self.game_path_editbox = QLineEdit()
    if self.game: self.game_path_editbox.setText(self.game.path)
    
    self.game_path_browse = QPushButton('...')
    self.game_path_browse.setFixedWidth(20)
    self.game_path_browse.clicked.connect(self._browseClicked)

    self.game_path_layout = QHBoxLayout()
    self.game_path_layout.addWidget(self.game_path_editbox)
    self.game_path_layout.addWidget(self.game_path_browse)

    self.game_arguments_editbox = QLineEdit()
    if self.game: self.game_arguments_editbox.setText(self.game.arguments)

    self.save_button = QPushButton(Icons.saveIcon(), 'Sauvegarder')
    font = self.save_button.font()
    font.setBold(True)
    self.save_button.setFont(font)
    self.save_button.clicked.connect(self._saveClicked)

    self.cancel_button = QPushButton(Icons.quitIcon(), 'Annuler')
    self.cancel_button.clicked.connect(lambda: self.close())

    self.buttons_layout = QHBoxLayout()
    self.buttons_layout.addWidget(self.save_button)
    self.buttons_layout.addWidget(self.cancel_button)

    layout = QFormLayout(self)
    layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
    layout.addRow('Nom du jeu:', self.game_name_editbox)
    layout.addRow('Chemin du jeu:', self.game_path_layout)
    layout.addRow('Argument(s) supplémentaire(s):', self.game_arguments_editbox)
    layout.addRow(self.buttons_layout)

    self.setLayout(layout)
  
  
  def _browseClicked(self):
    file = QFileDialog.getOpenFileName(self.parent(), directory=os.path.abspath(self.game_path_editbox.text()), filter='Exécutables (*.exe)')[0]
    self.game_path_editbox.setText(file.replace('/', '\\'))


  def _saveClicked(self):
    if self.game_name_editbox.text() != '' and self.game_path_editbox.text() != '':
      if os.path.exists(self.game_path_editbox.text()):
        if self.game:
          self.game.name = self.game_name_editbox.text()
          self.game.path = self.game_path_editbox.text()
          self.game.arguments = self.game_arguments_editbox.text()
        else:
          self.game = Game(Game.convertToDict(self.game_name_editbox.text(), self.game_path_editbox.text(), self.game_arguments_editbox.text()))
        self.close()
        self.saveCompletedEvent()
      else:
        QMessageBox.critical(self, 'ERREUR', 'Le fichier n\'existe pas! Veuillez corriger et réessayer')
    else:
      QMessageBox.critical(self, 'ERREUR', 'Un nom et un chemin valide doivent être remplis avant de poursuivre.')
  
  def saveCompletedEvent(self): pass # OVERRIDED BY CALLER

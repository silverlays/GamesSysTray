import os
import sys
import pylnk3

from PySide6.QtCore import *
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QAction, QCloseEvent, QBrush
from PySide6.QtWidgets import QMainWindow, QMenu, QListWidget, QListWidgetItem

from dialog_item_edit import ItemEditDialog
from games_controller import Game
from icons import Icons
from static import *


class ListWidgetItemCustom(QListWidgetItem):
  def __init__(self, game: Game):
    super().__init__()
    font = self.font()
    font.setBold(True)
    self.setFont(font)
    self.setIcon(game.icon)
    self.setText(game.name)


class MainWindow(QMainWindow):
  game_added = Signal(str, str, str) # Name, Path, Args
  game_edited = Signal(int, Game) # Index, Game
  game_deleted = Signal(int) # Index
  launch_game = Signal(int) # Index


  def __init__(self):
    super().__init__()
    self.setWindowTitle(f'{APP_TITLE} v{APP_VERSION}')
    self.setMinimumSize(APP_SIZE)

    self.list_widget = QListWidget()
    self.list_widget.setViewMode(self.list_widget.ViewMode.ListMode)
    self.list_widget.setMovement(self.list_widget.Movement.Static)
    self.list_widget.setIconSize(QSize(64, 64))
    self.list_widget.setSelectionMode(self.list_widget.SelectionMode.SingleSelection)
    self.list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
    self.list_widget.customContextMenuRequested.connect(self._contextMenuItem)
    self.list_widget.doubleClicked.connect(lambda: self.launch_game.emit(self.getCurrentIndex()))

    self.setCentralWidget(self.list_widget)

    # Events
    self.closeEvent = self._hide


  def _addGameClicked(self):
    self.item_window = ItemEditDialog(self)
    self.item_window.show()


  def _contextMenuItem(self, pos: QPoint):
    self.context_menu = QMenu()
    item = self.list_widget.itemAt(pos)
    action_launch_font = item.font()
    action_launch_font.setBold(True)
    action_launch = QAction(item.icon(), f'Lancer {item.text()}', self.context_menu)
    action_launch.setFont(action_launch_font)
    action_launch.triggered.connect(lambda: self.launch_game.emit(self.getCurrentIndex()))

    action_modify = QAction(Icons.modifyIcon(), 'Modifier l\'entrée', self.context_menu)
    action_modify.triggered.connect(self._editGameClicked)

    action_delete = QAction(Icons.removeIcon(), 'Supprimer l\'entrée', self.context_menu)
    action_delete.triggered.connect(self._deleteGameClicked)

    action_add = QAction(Icons.addIcon(), 'Ajouter manuellement un jeu', self.context_menu)
    action_add.triggered.connect(self._addGameClicked)

    action_cancel = QAction('Annuler', self.context_menu)
    
    self.context_menu.addAction(action_launch)
    self.context_menu.addSeparator()
    self.context_menu.addAction(action_modify)
    self.context_menu.addAction(action_delete)
    self.context_menu.addSeparator()
    self.context_menu.addAction(action_add)
    self.context_menu.addSeparator()
    self.context_menu.addAction(action_cancel)
    self.context_menu.popup(self.list_widget.viewport().mapToGlobal(pos))


  def _deleteGameClicked(self):
    self.game_deleted.emit(self.getCurrentIndex())


  def _editGameClicked(self):
    index = self.getCurrentIndex()
    game = self.retreiveGame(index)
    self.item_window = ItemEditDialog(self, game)
    self.item_window.save_button.clicked.connect(lambda: self.game_edited.emit(index, self.item_window.game))
    self.item_window.show()


  def _hide(self, event: QCloseEvent):
    event.ignore()
    self.hide()


  @Slot()
  def quit(self):
    self.hide()
    sys.exit()


  def dragEnterEvent(self, event: QDragEnterEvent) -> None:
    if event.mimeData().hasUrls() and event.mimeData().urls()[0].fileName().endswith('.lnk'):
      event.accept()
    else:
      event.ignore()


  def dropEvent(self, event: QDropEvent | None) -> None:
    mime_data = event.mimeData()
    if mime_data.hasUrls():
      link_path = mime_data.urls()[0].toLocalFile()
      if link_path.endswith(".lnk"):
        lnk_parsed = pylnk3.parse(link_path)
        game_name = os.path.basename(link_path).removesuffix(".lnk")
        self.game_added.emit(game_name, lnk_parsed.path, lnk_parsed.arguments or "")


  def getCurrentIndex(self) -> int:
    return self.list_widget.selectedIndexes()[0].row()


  def refresh(self, games: list[Game]):
    self.list_widget.clear()
    for game in games:
      item = ListWidgetItemCustom(game)
      self.list_widget.addItem(item)


  def retreiveGame(self, index: int): pass # OVERRIDED BY APP



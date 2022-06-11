import os
import sys
import pylnk3 # Used to import .lnk with arguments
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from game import Game
from icons import Icons
from custom_systray import CustomSysTrayWidget
from game_io import GameIO
from item_window import ItemWindow


__title__ = 'Games SysTray'
__version__ = '1.0'
SETTINGS_PATH = 'games.json'
STYLE_PATH = 'style.qss'
APP_SIZE = QSize(640, 480)

app = QApplication(sys.argv)
app.setWindowIcon(Icons.appIcon())


class main(QMainWindow):
  games = []


  def __init__(self):
    super().__init__(None)
    self.setWindowTitle(f'{__title__} v{__version__}')
    self.setFixedSize(APP_SIZE)
    self.closeEvent = self._hide
    
    self.game_io = GameIO(SETTINGS_PATH)
    self.systay_widget = CustomSysTrayWidget(self)
    self.games = self.game_io.loadData()

    self.systay_widget.showInterfaceEvent = self.showNormal
    self.systay_widget.quitEvent = self._quit
    self.systay_widget.reload(self.games)
    self.systay_widget.show()

    self._setupUI()
    sys.exit(app.exec())


  def _setupUI(self):
    self.widget_list = QListWidget(self)
    self.widget_list.setViewMode(self.widget_list.ViewMode.IconMode)
    self.widget_list.setMovement(self.widget_list.Movement.Static)
    self.widget_list.setWordWrap(True)
    self.widget_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    self.widget_list.setGridSize(QSize(115, 90))
    self.widget_list.setStyleSheet('padding: 20px; border: 0px')
    self.widget_list.setSelectionMode(self.widget_list.SelectionMode.SingleSelection)
    self.widget_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
    self.widget_list.customContextMenuRequested.connect(self._widgetListContextMenu)
    self.widget_list.doubleClicked.connect(self._launchGame)
    
    self._reloadData()
    
    self.setCentralWidget(self.widget_list)
  

  def _reloadData(self):
    self.games = self.game_io.loadData()
    self.systay_widget.reload(self.games)
    self.widget_list.clear()
    for game in self.games:
      game: Game
      widget_item = QListWidgetItem(game.icon, game.name, self.widget_list)
      self.widget_list.addItem(widget_item)


  def _widgetListContextMenu(self, pos: QPoint):
    self.context_menu = QMenu()
    if self.widget_list.itemAt(pos) == None:
      action_add = QAction(Icons.addIcon(), 'Ajouter un jeu', self.context_menu)
      action_add.triggered.connect(self._addGameClicked)

      action_import = QAction(Icons.importIcon(), 'Importer des liens', self.context_menu)
      action_import.triggered.connect(self._importLinkClicked)

      action_quit = QAction(Icons.quitIcon(), 'Quitter l\'application', self.context_menu)
      action_quit.triggered.connect(lambda: sys.exit())

      self.context_menu.addAction(action_add)
      self.context_menu.addSeparator()
      self.context_menu.addAction(action_import)
      self.context_menu.addSeparator()
      self.context_menu.addAction(action_quit)
    else:
      item = self.widget_list.itemAt(pos)
      action_launch_font = item.font()
      action_launch_font.setBold(True)
      action_launch = QAction(item.icon(), f'Lancer {item.text()}', self.context_menu)
      action_launch.setFont(action_launch_font)
      action_launch.triggered.connect(self._launchGame)

      action_modify = QAction(Icons.modifyIcon(), 'Modifier l\'entrée', self.context_menu)
      action_modify.triggered.connect(self._modifyGameClicked)

      action_delete = QAction(Icons.removeIcon(), 'Supprimer l\'entrée', self.context_menu)
      action_delete.triggered.connect(self._deleteGameClicked)

      action_cancel = QAction('Annuler', self.context_menu)
      
      self.context_menu.addAction(action_launch)
      self.context_menu.addSeparator()
      self.context_menu.addAction(action_modify)
      self.context_menu.addAction(action_delete)
      self.context_menu.addSeparator()
      self.context_menu.addAction(action_cancel)
    self.context_menu.popup(self.widget_list.viewport().mapToGlobal(pos))


  def _launchGame(self):
    game: Game = self.games[self.widget_list.currentIndex().row()]
    try:
      game.launch()
    except OSError as e:
      if e.errno == 22: # Elevation required
        QMessageBox.critical(self.parent(), 'ERREUR', 'Impossible de démarrer le jeu.\n\nRedémarrer en mode administrateur pour éviter cette erreur.')  
    except Exception as e:
      QMessageBox.critical(self, 'ERREUR', f'Une erreur est survenue:\n\n{e.args[1]}')


  def _addGameClicked(self):
    self.item_window = ItemWindow(self)
    self.item_window.saveCompletedEvent = self._addCompletedEvent
    self.item_window.show()


  def _importLinkClicked(self):
    for link in QFileDialog.getOpenFileNames(self, filter='Raccourcis (*.lnk)')[0]:
      file = pylnk3.parse(link)
      name = os.path.basename(link).removesuffix('.lnk')
      self.games.append(Game(Game.convertToDict(name, file.path, file.arguments or '')))
    self.game_io.saveData(self.games)
    self._reloadData()


  def _modifyGameClicked(self):
    game: Game = self.games[self.widget_list.currentIndex().row()]
    self.item_window = ItemWindow(self, game)
    self.item_window.saveCompletedEvent = self._modifyCompletedEvent
    self.item_window.show()


  def _deleteGameClicked(self):
    game: Game = self.games[self.widget_list.currentIndex().row()]
    self.games.remove(game)
    self.game_io.saveData(self.games)
    self._reloadData()


  def _addCompletedEvent(self):
    self.games.append(self.item_window.game)
    self.game_io.saveData(self.games)
    self._reloadData()


  def _modifyCompletedEvent(self):
    self.game_io.saveData(self.games)
    self._reloadData()

  
  def _hide(self, event: QCloseEvent):
    event.ignore()
    self.hide()


  def _quit(self):
    self.systay_widget.hide()
    sys.exit()



if __name__ == '__main__':
  if os.path.exists(STYLE_PATH): app.setStyleSheet(open(STYLE_PATH, 'r').read())
  main()

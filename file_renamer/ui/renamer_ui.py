import sys

from PySide2.QtWidgets import *
from PySide2.QtGui import *


class FileRenamerUi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ImRenamer")
        self.screen_resolution = QGuiApplication.primaryScreen().geometry()
        x = (self.screen_resolution.width() - self.width()) / 2
        y = (self.screen_resolution.height() - self.height()) / 2
        self.setGeometry(x, y, 500, 400)

        self.select_dir_line = None
        self.select_dir_but = None

        self.file_list_view = None

        self.old_text_line = None
        self.arrow_label = None
        self.new_text_line = None
        self.add_but = None

        self.add_old_text_line = None
        self.add_arrow_label = None
        self.add_new_text_line = None

        self.rename_but = None

        self.vbox2 = None

        self.line_count = 0
        self.add_line_edits = {}

        # 실행
        self.main_ui()

    def main_ui(self):
        self.select_dir_line = QLineEdit(self)
        self.select_dir_line.setMinimumWidth(500)
        self.select_dir_but = QPushButton("select")
        self.select_dir_but.setMaximumWidth(110)

        self.file_list_view = QListWidget(self)
        self.file_list_view.setMinimumHeight(250)

        self.old_text_line = QLineEdit(self)
        self.arrow_label = QLabel(">")
        self.new_text_line = QLineEdit(self)
        self.add_but = QPushButton("+")
        self.add_but.setMaximumWidth(110)

        self.rename_but = QPushButton("Rename")
        self.rename_but.setMinimumSize(500, 80)

        # Layout
        vbox = QVBoxLayout()
        self.vbox2 = QVBoxLayout()
        vbox3 = QVBoxLayout()

        hbox = QHBoxLayout()
        hbox2 = QHBoxLayout()

        self.setLayout(vbox)
        hbox.addWidget(self.select_dir_line)
        hbox.addWidget(self.select_dir_but)
        vbox.addLayout(hbox)
        vbox.addWidget(self.file_list_view)

        self.setLayout(self.vbox2)
        vbox.addLayout(self.vbox2)
        hbox2.addWidget(self.old_text_line)
        hbox2.addWidget(self.arrow_label)
        hbox2.addWidget(self.new_text_line)
        hbox2.addWidget(self.add_but)
        self.vbox2.addLayout(hbox2)

        self.setLayout(vbox3)
        self.vbox2.addLayout(vbox3)
        vbox3.addWidget(self.rename_but)

        # connect
        self.add_but.clicked.connect(self.add_clicked)

        # ui print
        self.select_dir_but.clicked.connect(self.selected_dir_clicked)
        self.rename_but.clicked.connect(self.rename_clicked)

    def add_clicked(self):
        print("add text line")
        self.add_old_text_line = QLineEdit(self)
        self.add_arrow_label = QLabel(">")
        self.add_new_text_line = QLineEdit(self)
        delete_but = QPushButton("-")
        delete_but.setMaximumWidth(110)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.add_old_text_line)
        hbox3.addWidget(self.add_arrow_label)
        hbox3.addWidget(self.add_new_text_line)
        hbox3.addWidget(delete_but)
        self.vbox2.insertLayout(self.vbox2.count() - 1, hbox3)
        delete_but.clicked.connect(lambda: self.delete_clicked(hbox3))
        self.line_count += 1
        self.add_line_edits[self.line_count] = (self.add_old_text_line, self.add_new_text_line, hbox3)
        return hbox3

    def delete_clicked(self, add_hbox):
        print("delete text line")
        if add_hbox is not None:
            for i in reversed(range(add_hbox.count())):
                widget_item = add_hbox.itemAt(i)
                if isinstance(widget_item, (QWidgetItem, QSpacerItem)):
                    widget_item.widget().deleteLater()
            self.vbox2.removeItem(add_hbox)
            self.adjustSize()
            self.update()

            delete_key = None
            for key, value in self.add_line_edits.items():
                if value[0] == add_hbox.itemAt(0).widget() and value[1] == add_hbox.itemAt(2).widget():
                    delete_key = key
                    break

            if delete_key is not None:
                del self.add_line_edits[delete_key]

    def selected_dir_clicked(self):
        print("selected directory")

    def rename_clicked(self):
        print("renamer")


def main():
    app = QApplication()
    ui = FileRenamerUi()
    ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
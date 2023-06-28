import sys

from PySide2.QtWidgets import *

from python.files_renamer import *

class FileReNamerController:
    def __init__(self):
        self.ui = FileRenamerUi()
        self.frn = FileReNamer()

        self.add_old_text_list = []
        self.add_new_text_list = []

        # event handler
        self.ui.select_dir_but.clicked.connect(self.selected_dir_clicked)

        self.ui.old_text_line.textChanged.connect(self.old_text_line)
        self.ui.new_text_line.textChanged.connect(self.new_text_line)

        self.ui.add_but.clicked.connect(self.add_line_edit)

        self.ui.rename_but.clicked.connect(self.rename_clicked)

    def selected_dir_clicked(self):
        self.ui.select_dir_line.clear()
        selected_directory = QFileDialog.getExistingDirectory(self.ui, "Select Directory", options=QFileDialog.ShowDirsOnly)
        if not selected_directory:
            return
        self.ui.select_dir_but = selected_directory
        self.ui.select_dir_line.setText(self.ui.select_dir_but)
        self.frn.input_path = self.ui.select_dir_but
        self.file_list_view()

    def file_list_view(self):
        self.ui.file_list_view.clear()
        file_list = self.frn.selected_files()
        for list_item in file_list:
            self.ui.file_list_view.addItem(list_item)

    def add_line_edit(self):
        if self.ui.add_old_text_line and self.ui.add_new_text_line is not None:
            self.ui.add_old_text_line.textChanged.connect(self.add_old_text_line)
            self.ui.add_new_text_line.textChanged.connect(self.add_new_text_line)

    def old_text_line(self, text):
        self.frn.old_text = []
        if text:
            self.frn.old_text.append(text)

    def add_old_text_line(self):
        self.add_old_text_list = []
        for i in range(1, self.ui.line_count + 1):
            if i in self.ui.add_line_edits.keys():
                line_edit = self.ui.add_line_edits[i][0]
                line_text = line_edit.text()
                if line_text:
                    self.add_old_text_list.append(line_text)

    def new_text_line(self, text):
        self.frn.new_text = []
        if text:
            self.frn.new_text.append(text)

    def add_new_text_line(self):
        self.add_new_text_list = []
        for i in range(1, self.ui.line_count + 1):
            if i in self.ui.add_line_edits.keys():
                line_edit = self.ui.add_line_edits[i][1]
                line_text = line_edit.text()
                if line_text:
                    self.add_new_text_list.append(line_text)

    def delete_all_line_edits(self):
        keys_to_delete = list(self.ui.add_line_edits.keys())
        for key in keys_to_delete:
            line_edit_tuple = self.ui.add_line_edits[key]
            line_edit_1, line_edit_2, hboxs = line_edit_tuple
            line_edit_1.clear()
            line_edit_2.clear()
            self.ui.delete_clicked(hboxs)
        self.ui.add_line_edits = {}

    def rename_clicked(self):
        self.frn.search_text()
        if self.ui.add_old_text_line and self.ui.add_new_text_line is not None:
            self.frn.old_text.extend(self.add_old_text_list)
            self.frn.new_text.extend(self.add_new_text_list)
            self.delete_all_line_edits()
        self.frn.edit_text()
        self.frn.rename_files()
        self.ui.old_text_line.clear()
        self.ui.new_text_line.clear()
        self.file_list_view()


def main():
    app = QApplication()
    controller = FileReNamerController()
    controller.ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

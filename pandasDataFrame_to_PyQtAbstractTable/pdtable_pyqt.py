# Some experiments in creating a PyQt table from a pandas DataFrame
#
# Features demonstrated:
#   * instantiate a QtAbstractTableModel from a pandas DataFrame
#   * allow editing od cells with changes being reflected in the DataFrame
#     object. This required some changes to the DataFrame indexing (certain
#     ways of indexing return a copy rather than a view into the DataFrame,
#     this was what prevented some stackoverflow solutions from working)
#   * finding out which rows are fully selected (or have at least one cell
#     selected) 
# 
# Background info:
# 
# https://stackoverflow.com/questions/31475965/fastest-way-to-populate-qtableview-from-pandas-data-frame/31557937
# https://stackoverflow.com/questions/41192293/make-qtableview-editable-when-model-is-pandas-dataframe
# https://www.youtube.com/watch?v=hJEQEECZSH0
# https://stackoverflow.com/questions/39914926/pyqt-load-sql-in-qabstracttablemodel-qtableview-using-pandas-dataframe-edi/39971773#39971773

# to show selection
# https://stackoverflow.com/questions/22577327/how-to-retrieve-the-selected-row-of-a-qtableview


# Checkboxes
# https://stackoverflow.com/questions/39511181/python-add-checkbox-to-every-row-in-qtablewidget
# https://stackoverflow.com/questions/12366521/pyqt-checkbox-in-qtablewidget

import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant
import ptvsd

df = pd.DataFrame({'a': ['Mary', 'Jim', 'John'],
                   'b': [100, 200, 300],
                   'c': ['a', 'b', 'c']})

class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None
    
    def setData_disabled(self, index, value, role):
        if not index.isValid():
            return False
        if role != Qt.EditRole:
            return False
        row = index.row()
        if row < 0 or row >= len(self._data.values):
            return False
        column = index.column()
        if column < 0 or column >= self._data.columns.size:
            return False
        self._data.values[row][column] = value
        self.dataChanged.emit(index, index)
        return True

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid():
            print(f"row {index.row()}, col {index.column()}")
            print("data set with keyboard : " , str(value))
            # in contrast to a couple if stackoverflow posts, the following
            # line did the trick. The nested indexing used in the stackoverflow posts
            # may not modify the original item but returns a copy of the cell
            # With the following modification I can now edit and the changes
            # are reflected in the data table
            self._data.iloc[index.row(),index.column()] = value
            print(self._data)
            print("data committed : " , self._data.values[index.row()][index.column()])
            self.dataChanged.emit(index, index)
            return True
        return QVariant()

    def flags(self, index):
        flags = super(self.__class__,self).flags(index)
        flags |= Qt.ItemIsEditable
        flags |= Qt.ItemIsSelectable
        flags |= Qt.ItemIsEnabled
        #flags |= Qt.ItemIsDragEnabled
        #flags |= Qt.ItemIsDropEnabled
        return flags

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ptvsd.debug_this_thread()
    window = QWidget()
    layout = QVBoxLayout()

    model = pandasModel(df)
    printbutton = QPushButton("print")
    view = QTableView()
   
    view.setModel(model)
    view.resize(800, 600)

    def show_data():
        # prints some information to the console on button 
        # press
        print("pandas Data Frame in model:")
        print(model._data)
        print("Selected rows:")
        indexes = view.selectionModel().selectedRows()
        for index in sorted(indexes):
            print('Row %d is completely selected' % index.row())
        rows = sorted(set(index.row() for index in
                      view.selectedIndexes()))
        for row in rows:
            print('at least one cell in row %d is selected' % row)
    
    printbutton.clicked.connect(show_data)

    layout.addWidget(view)
    layout.addWidget(printbutton)
    window.setLayout(layout)
    window.show()

    sys.exit(app.exec_())

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from generator_ui import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.start_home_position = """(Move to work position)
$H
G90 G20
G0 X0 Y0
G0 Z0 \n
"""
        self.end_home_position = """(Move back to work position)
G0 Z0.85
G0 X0 Y0
"""

        self.xoffset = ""
        self.yoffset = ""
        self.xyspeed = ""
        self.zspeed = ""
        self.xyextracut = ""
        self.cutdepth = ""
        self.inputlength = ""
        self.inputwidth = ""
        self.inputthickness = ""
        self.outputlength = ""
        self.outputwidth = ""

        self.data_x = []
        self.data_y = []
        self.no_rows = 2
        self.no_columns = 1

        self.pushButton_generate.clicked.connect(self.operator_save)
        self.show()

    def operator_save(self):
        self.xoffset = self.lineEdit_xoffset.text()
        self.yoffset = self.lineEdit_yoffset.text()
        self.xyspeed = self.lineEdit_xyspeed.text()
        self.zspeed = self.lineEdit_zspeed.text()
        self.xyextracut = self.lineEdit_xyextracut.text()
        self.cutdepth = self.lineEdit_cutdepth.text()

        self.inputlength = self.lineEdit_inputlength.text()
        self.inputwidth = self.lineEdit_inputwidth.text()
        self.inputthickness = self.lineEdit_thickness.text()

        self.outputlength = self.lineEdit_outputlength.text()
        self.outputwidth = self.lineEdit_outputwidth.text()
        # print(self.xoffset, self.yoffset, self.xyspeed, self.zspeed, self.xyextracut, self.cutdepth)
        # print(self.inputlength, self.inputwidth, self.inputthickness, self.outputlength, self.outputwidth)

        self.create_file()

    # Function to convert
    def listToString(self, s):
        # initialize an empty string
        str1 = ""
        # return string
        return (str1.join(s))

    # Function to generate along x axis movement Gcode
    def x_rows(self, no_rows):
        self.data_x.append("(start of the rows along x axis movement)\n")
        for x in range(self.no_rows):
            self.new_row_string = """G01 X{} Y{} F{}
G01 Z-{} F{}
G01 X{} F{}
G01 Z{} F{}\n\n""".format(self.xoffset, (self.outputlength * (x+1)), self.xyspeed,
                               self.cutdepth, self.zspeed,
                               self.outputwidth + self.xyextracut, self.xyspeed,
                               self.cutdepth, self.zspeed)
            self.data_x.append(self.new_row_string)

        return self.listToString(self.data_x)

    # Function to generate along y axis movement Gcode
    def y_columns(self, no_columns):
        self.data_y.append("(start of the column along y axis movement)\n")
        for y in range(self.no_columns):
            new_column_string = """G01 X{} Y{} F{}
G01 Z-{} F{}
G01 y{} F{}
G01 Z{} F{}\n\n""".format((self.outputwidth * (y+1)), self.yoffset, self.xyspeed,
                               self.cutdepth, self.zspeed,
                               self.outputlength + self.xyextracut, self.xyspeed,
                               self.cutdepth, self.zspeed)
            self.data_y.append(new_column_string)

        return self.listToString(self.data_y)

    def create_file(self):
        f = open("Gcode.nc", "w")
        f.write(self.start_home_position)             # start of the G code -- work position zero Gcode
        f.write(self.x_rows(self.no_rows))            # start of the rows (along x movement)
        f.write(self.y_columns(self.no_columns))          # start of the columns (along y movement)
        f.write(self.end_home_position)             # End of Gode -- return to home
        f.close()
        print("End of the code")

if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("Gcode Generator")

    window = MainWindow()
    app.exec_()

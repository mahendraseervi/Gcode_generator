no_rows = 2
no_colums = 1
x_row_offset = 0.2
y_column_offset = 0.2
data_x = []
data_y = []

x_load_distance = 24
y_load_distance = 48
x_distance = 12
y_distance = 15
z_distance = 0.5
speed = 800
z_speed = 100
extra_cut = 1

start_home_position = """(Move to work position)
$H
G90 G20
G0 X0 Y0
G0 Z0 \n
"""
end_home_position = """(Move back to work position)
G0 Z0.85
G0 X0 Y0
"""

# Function to convert
def listToString(s):
    # initialize an empty string
    str1 = ""
    # return string
    return (str1.join(s))

# Function to generate along x axis movement Gcode
def x_rows(rows):
    data_x.append("(start of the rows along x axis movement)\n")
    for x in range(rows):
        new_row_string = """G01 X{} Y{} F{}
G01 Z-{} F{}
G01 X{} F{}
G01 Z{} F{}\n\n""".format(x_row_offset, (y_distance * (x+1)), speed,
                           z_distance, z_speed,
                           x_load_distance + extra_cut, speed,
                           z_distance, z_speed)
        data_x.append(new_row_string)

    return listToString(data_x)


# Function to generate along y axis movement Gcode
def y_columns(columns):
    data_y.append("(start of the column along y axis movement)\n")
    for y in range(columns):
        new_column_string = """G01 X{} Y{} F{}
G01 Z-{} F{}
G01 y{} F{}
G01 Z{} F{}\n\n""".format((x_distance * (y+1)), y_column_offset, speed,
                           z_distance, z_speed,
                           y_load_distance + extra_cut, speed,
                           z_distance, z_speed)
        data_y.append(new_column_string)

    return listToString(data_y)


f = open("Gcode.nc", "w")
f.write(start_home_position)           # start of the G code -- work position zero Gcode
f.write(x_rows(no_rows))               # start of the rows (along x movement)
f.write(y_columns(no_colums))          # start of the columns (along y movement)
f.write(end_home_position)             # End of Gode -- return to home
f.close()

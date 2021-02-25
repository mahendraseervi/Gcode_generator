(Move to work position)
$H
G90 G20
G0 X0 Y0
G0 Z0 

(start of the rows along x axis movement)
G01 X0.2 Y F600
G01 Z-0.8 F100
G01 X0.7 F600
G01 Z0.8 F100

G01 X0.2 Y F600
G01 Z-0.8 F100
G01 X0.7 F600
G01 Z0.8 F100

(start of the column along y axis movement)
G01 X Y0.2 F600
G01 Z-0.8 F100
G01 y0.7 F600
G01 Z0.8 F100

(Move back to work position)
G0 Z0.85
G0 X0 Y0

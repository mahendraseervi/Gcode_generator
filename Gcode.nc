(Move to work position)
$H
G90 G20
G0 X0 Y0
G0 Z0 

(start of the rows along x axis movement)
G01 X0.2 Y15 F800
G01 Z-0.5 F100
G01 X25 F800
G01 Z0.5 F100

G01 X0.2 Y30 F800
G01 Z-0.5 F100
G01 X25 F800
G01 Z0.5 F100

(start of the column along y axis movement)
G01 X12 Y0.2 F800
G01 Z-0.5 F100
G01 y49 F800
G01 Z0.5 F100

(Move back to work position)
G0 Z0.85
G0 X0 Y0

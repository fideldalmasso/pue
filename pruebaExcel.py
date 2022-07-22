import openpyxl
import PySimpleGUI as sg
wb = openpyxl.load_workbook('archivo2.xlsx')
sheet = wb['Sheet1']

# obtener todos los rangos
for i in wb.defined_names.definedName:

	dests = i.destinations # returns a generator of (worksheet title, cell range) tuples

	cells = []
	
	for title, coord in dests:
		rango = wb[title][coord]

	print('Nombre='+i.name+' Coordenada=' + coord)
	if hasattr(rango, '__iter__'):		 # es un rango de celdas
		for row in rango:
			for cell in row:
				print('\tContenido=' + str(cell.value))
	else:							 	 # es una celda
		print('\tContenido=' + str(rango.value))
		rango.value='HolaCambiado'


wb.save('archivo2Modificado.xlsx')

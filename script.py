import openpyxl
import PySimpleGUI as sg
import re

class Componente:
	def __init__(self, tipo1):
		self.tipo = tipo1
		self.nombre = ""
		self.dict= {}
		self.valores = [[]]
		self.valor = "vacio"
		self.resultado=""
		# self.coordenada = coor1
	
	def modificar(self,nuevoValor):
		self.valor = nuevoValor
		match self.tipo:
			case 'NUM':
				self.resultado.value = float(nuevoValor)
			case 'STRING':
				self.resultado.value = nuevoValor
			case 'SLIDE':
				self.resultado.value = float(nuevoValor)
			case 'SWITCH':
				self.resultado.value = nuevoValor=='True'

def funcion(nombre,resultado):

	obj = None
	separador="[\.\_]"
	pattern = re.compile(rf"""(?x)
	(?P<Tipo>PUE{separador}[A-Z]+){separador}
	(
		((?P<MinValue>\d+){separador}(?P<MaxValue>\d+){separador}(?P<Resolution>[\d\.]+){separador}) |
	)
	(?P<Nombre>[a-zA-z0-9_]+)
	""",re.VERBOSE)

	s=nombre
	m = pattern.fullmatch(s)

	if(m!=None):
		m=m.groupdict()
		if hasattr(resultado, '__iter__'):  # es un rango de celdas

			if m.get('Tipo')=='PUE.TABLE' or  m.get('Tipo')=='PUE_TABLE':
				obj = Componente("TABLE")
				obj.nombre = str(m.get('Nombre'))
				h=len(resultado)
				w=len(resultado[0])
				obj.valores = [[0 for x in range(w)] for y in range(h)] 
				# for row in resultado:
				# 	for cell in row:
				# 		obj.valores[int(counter/ancho)][counter%ancho]=cell.value
				# 		counter+=1
				for i in range(h):
					for j in range(w):
						obj.valores[i][j]=str(resultado[i][j].value)
				return [obj]
						
			else:
				counter=0
				lista = []
				for row in resultado:
					for cell in row:
						match m.get('Tipo'):
							case "PUE.NUM" | "PUE_NUM":
								obj = Componente("NUM")
							case 'PUE.STRING' | "PUE_STRING":
								obj = Componente("STRING")
							case 'PUE.SLIDE.' | 'PUE_SLIDE':
								print("Warning: Range SLIDE not supported!")
							case 'PUE.SWITCH' | "PUE_SWITCH":
								obj = Componente("SWITCH")
							case _:
								print('Error! No se matchea con ningun caso!')
						obj.nombre = m.get('Nombre')+"{"+str(counter)+"}"
						obj.resultado = cell
						obj.valor=cell.value
						lista.append(obj)
						counter+=1

				return lista
		else:  # es una celda
			
			match m.get('Tipo'):
				case "PUE.NUM" | "PUE_NUM":
					obj = Componente("NUM")
				case 'PUE.STRING' | "PUE_STRING":
					obj = Componente("STRING")
				case 'PUE.SLIDE' | 'PUE_SLIDE':
					obj = Componente("SLIDE")
					obj.dict['MinValue']=m.get('MinValue')
					obj.dict['MaxValue']=m.get('MaxValue')
					obj.dict['Resolution']=float(m.get('Resolution'))
				case 'PUE.SWITCH' | "PUE_SWITCH":
					obj = Componente("SWITCH")
					# obj.dict['TrueValue']=m.get('MinValue')
					# obj.dict['FalseValue']=m.get('MaxValue')
				case _:
					print('Error! No se matchea con ningun caso!')
			obj.valor = resultado.value
			obj.nombre = m.get('Nombre')
			obj.resultado= resultado
			return [obj]



def make_window(componentes):
	
	NAME_SIZE = 35
	def name(name):
		dots = NAME_SIZE-len(name)-2
		return sg.Text(name + ' ' + '•'*dots, size=(NAME_SIZE,1), justification='r',pad=(0,0), font='Courier 10')
	
	layout=[[sg.Input(FILENAME,key='browse',readonly=True,enable_events=True,s=35,font='Courier 10'), sg.FileBrowse( target='browse')]]

# 				[[sg.Input(key='_FILEBROWSE_', enable_events=True, visible=False)],
#             [sg.FileBrowse(target='_FILEBROWSE_')],
#             [sg.OK()],]

	for i in componentes.keys():
		componente = componentes[i]
		match componente.tipo:
			case 'NUM':
				c = [name(componente.nombre),sg.InputText(s=15,key=componente.nombre)]
				# c.Update(componente.valor)
			case 'STRING':
				c = [name(componente.nombre),sg.InputText(s=15,key=componente.nombre)]
				# c.Update(componente.valor)
			case 'SLIDE':
				c = [name(componente.nombre), sg.Slider((componente.dict['MinValue'],componente.dict['MaxValue']), orientation='h', s=(10,15),resolution=componente.dict['Resolution'],key=componente.nombre)]
				# c.Update(componente.valor)
			case 'SWITCH':
				c = [name(componente.nombre), sg.Checkbox('',default=componente.valor=='True',key=componente.nombre)],
			case 'TABLE':
				layout.append([name(componente.nombre)])
				c = [sg.Table(componente.valores[1:],headings=componente.valores[0],key=componente.nombre, expand_x=True,num_rows=len(componente.valores[0]), expand_y=True,alternating_row_color=sg.theme_button_color()[1])]
				# c = [name(componente.nombre), sg.Button('caca')]
		layout.append(c)




	layout.append([name('Guardar cambios'),sg.Button('Guardar',key='Go')])
	window = sg.Window('SISTEMA PUE', layout, finalize=True, scaling=2.5)
	return window


def cargarArchivo(FILENAME):
	wb = openpyxl.load_workbook(FILENAME)
	componentes={}
	keylist=[]
	# obtener todos los rangos
	for i in wb.defined_names.definedName:
		dests = i.destinations # returns a generator of (worksheet title, cell range) tuples
		for title, coord in dests:
			resultado = wb[title][coord]
			oneOrMoreComponents = funcion(i.name,resultado)
			if(oneOrMoreComponents!=None):
				for c in oneOrMoreComponents:
					componentes[c.nombre]=c
					keylist.append(c.nombre)

	window= make_window(componentes)
	for i in keylist:
		if(componentes[i].tipo!='TABLE'):
			window[i].Update(componentes[i].valor) # poner los valores iniciales
	return wb,componentes,keylist,window


FILENAME = 'archivo.xlsx'
wb, componentes, keylist, window = cargarArchivo(FILENAME)
while True:
	event, values = window.read()
	# sg.popup(event, values)  # show the results of the read in a popup Window
	if event == sg.WIN_CLOSED or event == 'Exit':
		break
	if event == "browse":
		
		newFileName=str(values['browse'])
		if(newFileName[-5:]==".xlsx"):
			window.close()
			FILENAME=str(values['browse'])
			wb, componentes, keylist, window = cargarArchivo(FILENAME)
		else:
			sg.popup('No es un archivo excel!')
			
	elif event == "Go":
		for i in keylist:
			# if(values[i]!=None):
			if(componentes[i].tipo!='TABLE'):
				print("["+i+"="+str(values[i])+"]",end='')
				componentes[i].modificar(str(values[i]))
		print()
		nuevoArchivo = FILENAME.split('.')[0]+'Modificado.xlsx'
		print("Guardando cambios en " + nuevoArchivo+" ...")
		wb.save(nuevoArchivo)
window.close()
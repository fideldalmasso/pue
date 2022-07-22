from asyncio import run_coroutine_threadsafe
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

	pattern = re.compile(r"""(?x)
	(?P<Tipo>PUE\.[A-Z]+\.)
	(
		# ((?P<TrueValue>[a-zA-Z]+)\.(?P<FalseValue>[a-zA-Z]+)\.) | 
		((?P<MinValue>\d+)\.(?P<MaxValue>\d+)\.(?P<Resolution>[\d\.]+)\.) |
	)
	(?P<Nombre>[a-zA-z0-9]+)
	""",re.VERBOSE)

	s=nombre
	m = pattern.fullmatch(s)

	if(m!=None):
		m=m.groupdict()
		if hasattr(resultado, '__iter__'):  # es un rango de celdas
			pass
			lista = []
			
			counter=0
			for row in resultado:
				for cell in row:
					match m.get('Tipo'):
						case 'PUE.NUM.':
							obj = Componente("NUM")
						case 'PUE.STRING.':
							obj = Componente("STRING")
						case 'PUE.SLIDE.':
							print("Warning: Range SLIDE not supported!")
						case 'PUE.SWITCH.':
							obj = Componente("SWITCH")
					obj.nombre = m.get('Nombre')+"{"+str(counter)+"}"
					obj.resultado = cell
					obj.valor=cell.value
					lista.append(obj)
					counter+=1

			return lista
		else:  # es una celda
			
			match m.get('Tipo'):
				case 'PUE.NUM.':
					obj = Componente("NUM")
				case 'PUE.STRING.':
					obj = Componente("STRING")
				case 'PUE.SLIDE.':
					obj = Componente("SLIDE")
					obj.dict['MinValue']=m.get('MinValue')
					obj.dict['MaxValue']=m.get('MaxValue')
					obj.dict['Resolution']=float(m.get('Resolution'))
				case 'PUE.SWITCH.':
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
	
	NAME_SIZE = 23
	def name(name):
		dots = NAME_SIZE-len(name)-2
		return sg.Text(name + ' ' + '•'*dots, size=(NAME_SIZE,1), justification='r',pad=(0,0), font='Courier 10')
	
	layout=[[sg.Input(FILENAME,key='browse',readonly=True,enable_events=True,s=33), sg.FileBrowse( target='browse')]]

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

		layout.append(c)

	layout.append([name('Guardar cambios'),sg.Button('Guardar',key='Go')])
	window = sg.Window('SISTEMA PUE', layout, finalize=True, keep_on_top=True)
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
		window.close()
		FILENAME=str(values['browse'])
		wb, componentes, keylist, window = cargarArchivo(FILENAME)
	elif event == "Go":
		for i in keylist:
			print("["+i+"="+str(values[i])+"]",end='')
			componentes[i].modificar(str(values[i]))
		print()
		nuevoArchivo = FILENAME.split('.')[0]+'Modificado.xlsx'
		print("Guardando cambios en " + nuevoArchivo+" ...")
		wb.save(nuevoArchivo)
window.close()


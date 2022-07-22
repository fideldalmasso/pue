import PySimpleGUI as sg

def make_window(theme=None):
	
	keylist = ["Input1", "Input22"]
	NAME_SIZE = 23
	def name(name):
		dots = NAME_SIZE-len(name)-2
		return sg.Text(name + ' ' + '•'*dots, size=(NAME_SIZE,1), justification='r',pad=(0,0), font='Courier 10')

	layout=[
		[name('Input'), sg.InputText(s=15,key=keylist[0])],
		[name('Checkbox'), sg.Checkbox('Analizar',key=keylist[1])],
		[name('Go'),sg.Button('Go',key='Go')]
	]

	window = sg.Window('The PySimpleGUI Element List', layout, finalize=True, keep_on_top=True)
	window['Input1'].bind("<Return>", "_Enter")

	return window, keylist

window ,keylist= make_window()

while True:
	event, values = window.read()
	# sg.popup(event, values)  # show the results of the read in a popup Window
	if event == sg.WIN_CLOSED or event == 'Exit':
		break
	elif event == "Go":
		for i in keylist:
			print("["+i+"="+str(values[i])+"]",end='')
		print()
		# print("Input1="+window['Input1'].get())
		# print("Input2="+str(window['Input2'].get()))
window.close()

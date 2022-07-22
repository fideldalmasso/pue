import re

pattern = re.compile(r"""(?x)
	(?P<Tipo>PUE\.[A-Z]+\.)
	(
		((?P<TrueValue>[a-zA-Z]+)\.(?P<FalseValue>[a-zA-Z]+)\.) | 
		((?P<MinValue>\d+)\.(?P<MaxValue>\d+)\.) |

	)
	(?P<Nombre>[a-zA-z]+)
""",re.VERBOSE)

for s in [ "PUE.NUM.Fidel", "PUE.SLIDE.1.100.Jose", "PUE.SWITCH.Activado.Desactivado.Jose"]: #,
	m = pattern.fullmatch(s)
	if(m!=None):
		m=m.groupdict()
		print("\n" + s + "-> " + "Nombre= " + m.get('Nombre')+" Tipo=" + m.get('Tipo') + " ",end='')   
		match m.get('Tipo'):
			case 'PUE.NUM.':
				pass
			case 'PUE.STRING.':
				pass
			case 'PUE.TABLE.':
				pass
			case 'PUE.SLIDE.':
				print("m="+str(m.get('MinValue'))+" M="+str(m.get('MaxValue')), end='')
			case 'PUE.SWITCH.':
				print("T="+m.get('TrueValue')+" F="+m.get('FalseValue'), end='')
			case _:
				print('Error! No se matchea con ningun caso!')
			
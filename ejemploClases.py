
class Componente:
	def __init__(self, tipo1,nombre1):
		self.tipo = tipo1
		self.nombre = nombre1
		self.dict= {}


obj = Componente("COMBO","Fidel")
obj.dict['minValue']=1
print(obj.tipo)
print(obj.dict)
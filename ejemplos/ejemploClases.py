
class Componente:
	def __init__(self, tipo1,nombre1,coor1):
		self.tipo = tipo1
		self.nombre = nombre1
		self.dict= {}
		self.valores = [[]]
		self.valor = "vacio"
		self.coordenada = coor1


obj = Componente("COMBO","Fidel","111")
obj.dict['minValue']=1
print(obj.tipo)
print(obj.dict)
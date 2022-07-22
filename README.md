# PUE: Herramienta GUI para editar archivos Excel
![](captura.png)
El script de Python permite editar visualmente celdas de archivos Excel. Para ello, es necesario *taggear* las celdas y/o rangos correspondientes mediante *Named Ranges*.

# Tags disponibles
## Primitivos
```
PUE.NUM.Nombre
PUE.STRING.Nombre
```

## Tablas
```
PUE.TABLE.Nombre (no disponible)
```

## Especiales
```
PUE.SWITCH.Nombre
PUE.SLIDER.MinValue.MaxValue.Nombre
PUE.COMBO.{valores}.Nombre (no disponible)
```
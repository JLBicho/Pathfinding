'''
	Generacion de los nodos de la matriz de distancias entre nodos
'''

from SSSP_Djikstra import sssp_djisktra_func, sssp_djikstra_a2b

Nnodos = int(input('¿Cuantos nodos hay? '))

nodos = []
for i in range(0,Nnodos):
	x = i + 97
	nodos.append(str(chr(x)))

S = []
Q = nodos.copy()
distNodos = [float("inf")] * len(nodos) 

filas = Nnodos
columnas = Nnodos

# Matriz de distancias
matrizDist = [None] * filas
for i in range(filas):
    matrizDist[i] = [None] * columnas


print('======')
print('Ahora se introducen las distancias entre nodos.')
print('Puede haber diferentes distancias a->b que b->a.')
print('Si no se puede ir de a->b marcar -1')
print('======')

for i in range(filas):
	for j in range(columnas):
		if i != j:
			matrizDist[j][i] = int(input('Distancia ' + nodos[i] + ' --> ' + nodos[j] + ': '))
		else:
			matrizDist[j][i] = 0
	

print('======')
src = input('Nodo inicial: ')
while(src not in nodos):
	src = input('El nodo no existe. Nodo inicial: ')

dst = input('Nodo destino: ')
while (dst not in nodos):
	dst = input('El nodo no existe. Nodo destino: ')

print('======')
dist_a2b, camino = sssp_djikstra_a2b(source=src, destination=dst, nodes=nodos, distances=matrizDist)
print('Distancia entre ' + src + ' y ' + dst + ' = ' + str(dist_a2b))
print('Camino recorrido ' + str(camino))
print('======')
print('Nodos: ' + str(nodos))
dists = sssp_djisktra_func(starting_node=src, nodes=nodos, distances=matrizDist)
print('Distancia desde "' + str(src) + '" a cada nodo: ')
for i in range(len(dists)):
	print(str(nodos[i])+' '+ str(dists[i]))
print('======')

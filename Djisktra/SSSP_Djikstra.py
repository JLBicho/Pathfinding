'''
	Autor: Jose Luis Millan Valbuena
	
	Funciones para encontrar distancias minimas mediante
	el algoritmo de Djikstra.
	Se usan matrices de distancias.

'''

'''
nodos = ['A', 'B', 'C']
A --> B; B --> C; C --> B
	dAB			 dBC 			dCB

En la matriz de distancias, debe haber un 0 en la diagonal y -1 en los nodos no conectados.
Las distancias van desde COLUMNA(origen) -> FILA(destino)

matriz = [[0   -1   -1];
					[dAB  0  dCB];
					[0   dBC   0]]
'''
def sssp_djisktra_func(starting_node, nodes = [], distances = []):
	if nodes == []:
		print("Empty nodes")

	if distances == []:
		print("Empty distances")

	if len(distances[0]) != len(nodes) or len(distances) != len(nodes):
		print("Matrix dimensions are wrong")

	S = []
	Q = nodes.copy()
	distNodes = [float("inf")] * len(nodes) 

	col = nodes.index(starting_node)
	
	distNodes[col] = 0 

	while len(Q) != 0:	
		row = 0
		for row in range(len(nodes)):
			if distances[row][col] is not -1:
				if(distNodes[row] > distNodes[col] + distances[row][col]):
					distNodes[row] = distNodes[col] + distances[row][col]

		visited = []
		for j in range(len(S)):
			visited.append(nodes.index(S[j]))

		distMin = float("inf")
		for i in range(len(distNodes)):
			if i not in visited and distNodes[i] < distMin:
				distMin = distNodes[i]

		for index, value in enumerate(distNodes):
			if value == distMin and index not in visited:
				rowIndex = index

		rowIndex = distNodes.index(distMin)
		if nodes[rowIndex] in Q:
			S.append(Q.pop(Q.index(nodes[rowIndex])))
		else:
			S.append(Q.pop(0))
		
		col = nodes.index(S[-1])
	
	return distNodes

'''
	La siguiente funcion permite conocer la distancia entre dos puntos
'''
def sssp_djikstra_a2b(source, destination, nodes = [], distances = []):
	
	distNodes = sssp_djisktra_func(starting_node=source, nodes=nodes, distances=distances)
	dist_a2b = distNodes[nodes.index(destination)]
	
	path = []
	path.append(source)
	while destination not in path:
		distMin = float("inf")
		for i in range(len(distNodes)):
			if distNodes[i] < distMin and nodes[i] not in path:
				distMin = distNodes[i]
				actual_node = nodes[i]
		
		path.append(actual_node)
		distNodes = sssp_djisktra_func(starting_node=actual_node, nodes=nodes, distances=distances) 

	return dist_a2b, path # , distPath


import random
import math
from time import *
import gc

def main():
	#Test ob Adjazenzliste aus Adjazenzmatrix ordnungsgemaess erstellt wird 

	mat = 0#[[1,0,1,1,0,1],[1,0,1,0,0,0],[0,1,1,1,1,0],[1,0,0,0,0,1],[1,0,1,1,0,0],[0,0,1,0,1,1]]
#
 	g = graph(mat, "G")
	g.read("../Graphen/data_mis_0000.mis")
#	#g.printmat()
	#g.printlist()

#Zeitmessung
	#erster Parameter: wie oft wird gemessen, 
	#zweiter Parameter: In wie grossen abstaenden wird gemessen
	#timeTest(80,100)

def timeTest(runs, stepsize):
	#im Array times werden die zeiten in sekunden gespeichert
	#fuer jede Runde wird die Zeit von InitRandomly gemessen, welche je nach runde groesser
	#werdende graphen als liste initialisiert
	times = []
	for i in range(1,runs+1):
		a = i * stepsize
		g2 = graph(0, "G" + str(a))
		t1 = clock()
		g2.initRandomly(a)
		times.append(clock() - t1)

		#wird naturlich nicht mitgemessen
		g2.printlist()
		del g2
		gc.collect()
		try: 
			print(str(g2.name) + " existiert noch")
			return 0
		except:
			print "Objekt geloescht"

		#diese Scheife dient zum ausgeben der Messwerte
	for i in range(0,runs):
		print ("Durchlauf " + str(i+1) + " dauerte "+str(times[i]) + " Sekunden (" + str(stepsize*(i+1)) + " Vertices erstellt)")

class vertex:
	#Jeder Vertex hat einige Nachbarn (somit eine Edge pro Nachbar)
	#einen Index bzw Name und, falls es nochmal wichtig wird, ein Gewicht
	def __init__(self,i):

		self.neighbours = []
		self.index = 0
		self.weight = 0
		self.name = ""

		self.index = i

	def setName(self,n):
		self.name = n

	def setNeighbour(self,v):
		self.neighbours.append(v)
		self.weight += 1

	def printNeighbours(self):
		prntstr = ""
		for i in self.neighbours:
			prntstr += str(i.index) + "  "
		return prntstr

class graph:
	#Graphen haben Einen Namen, Vertices, und ueber deren nachbarn, Edges.
	#durch angabe einer adjazenzmatrix kann ein graph generiert werden, ohne diese
	#bleibt er leer
	def __init__(self, mat, name):

		self.name = name
		self.adjmat = []
		self.vertices = []

		self.nameIndexPair = {}#Hashmap fuer die vertices

		if mat != 0:
			if len(mat) == len(mat[0]):
				self.adjmat = mat
				self.initListFromMat()
			else:
				print("Adjazenzmatrizen mussen quadratisch sein.")

	def read(self, filepath):

		vertices = 0
		edges    = 0

		if filepath.endswith(".mis"):
			misFile = open(filepath, "r").readlines()
			lineOne = misFile[0].split()
			
			if lineOne[0] == "p" and lineOne[1] == "edges":
				vertices = int(lineOne[2])
				edges    = int(lineOne[3])
				print("Reading " + filepath)


				#
				#edges = 1000
				#

				self.initializeVertices(misFile, edges)
				self.initializeEdges(misFile, edges)
				self.printlist()
			else:
				return (".mis : invalid format")

		else:
			return ("unknown format")

	def initializeVertices(self, file, edges):
		listV = []

		startTime = clock()
		for i in range (1,edges + 1):
			vertexLHS = file[i].split()[1]
			if i % 10000 == 0:
				print("We are at line "+str(i) +" of " + str(edges))
				if i % 100000 == 0:
					print("(Took " + str(clock() - startTime) + " seconds until now.)")
			if vertexLHS not in listV:
				listV.append(vertexLHS)
		print("Es werden " + str(len(listV)) + " Vertices erstellt...")
		index = 0
		for v in listV:
			newVertex = vertex(index)
			newVertex.setName(v)

			self.nameIndexPair.update( {v:index} )

			self.vertices.append(newVertex)
			index += 1

	def initializeEdges(self, file, edges):
		
		for i in range (1,edges + 1):
			nameLHS = file[i].split()[1]
			nameRHS = file[i].split()[2]#kann im monent sein, dass name rhs noch nicht existiert
			
			indexLHS = self.nameIndexPair[nameLHS]

			if nameRHS in self.nameIndexPair: 
				indexRHS = self.nameIndexPair[nameRHS]
				self.vertices[indexLHS].setNeighbour(self.vertices[indexRHS])
		
#gehe durch liste: jeder name(links) gibt einen index zurueck.
#der vertex mit diesem index bekommt rechts (wieder name zu index) als neighbour -> quadratische laufzeit 
#brauche hashmap von name zu index :/
	def initListFromMat(self):
		#Funktion um aus adjMat adjList zu machen
		for i in range(0,len(self.adjmat)):
			newVertex = vertex(i)
			self.vertices.append(newVertex)
		
		for row in range(0,len(self.adjmat)):
			for column in range(0,len(self.adjmat)):
				if self.adjmat[row][column] == 1:
					self.vertices[row].setNeighbour(self.vertices[column])
	def initRandomly(self,size):
		#initialisiert einen beliebig grossen graphen mit IVI^(1,5) vielen Kanten zufaellig

		#vertices erstellen
		for i in range(0, size):
			newVertex = vertex(i)
			self.vertices.append(newVertex)

		#jedem dieser Vertices einige Vertices als Nachbarn zuweisen
		for v in self.vertices:
			probabilityEachStep = int( math.sqrt(size))
			while random.randint(0,probabilityEachStep) != 0:
				neighbourIndex = random.randint(0,size-1)
				#while self.vertices[neighbourIndex] in v.neighbours:
				#	neighbourIndex = random.randint(0,size-1)
				v.setNeighbour(self.vertices[neighbourIndex])
		# Wenn pro Vertex jeder sqrt(IVI) -te Vertex ein Nachbar ist, gilt etwa IEI = IVI^(1,5)

	def printmat(self):
		print("Adjazenzmatrix von "+ self.name + ":")
		for i in self.adjmat:
			print i
	def printlist(self):
		print("Adjazenzliste von "+ self.name + ":")
		for i in self.vertices:
			print(" Index   Name ")
			print(str(self.nameIndexPair[i.name]) +" " + i.name +  ": " + i.printNeighbours())
		
main()
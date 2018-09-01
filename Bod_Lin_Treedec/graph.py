import random
import math
from time import *
import gc
from treedec import *

def main():
	mat = 0	# obligatorisch zu testzwecken. 
			#geeigneter zum erstellen von graphen ist das mis file.	
#[[1,0,1,1,0,1],[1,0,1,0,0,0],[0,1,1,1,1,0],[1,0,0,0,0,1],[1,0,1,1,0,0],[0,0,1,0,1,1]]

	#Graph einlesen und erstellen. Zeit messen.
 	g = graph(mat, "G")
	t = clock()
	g.read("../data_mis_0001.mis")#../Graphen/data_mis_0000.mis")
	print("Gesamt: " + str(clock()-t) + " Sekunden")

	#erstellen eines Baumzerlegung - Objekts
	T = TreeDec("TW(G)")

	#Tests fuer k = 1 ... 5
	for i in range(1,6):
		T.decompose(g,i)

class vertex:
	#Jeder Vertex hat einige Nachbarn (somit eine Edge pro Nachbar)
	#einen Index bzw Name und, falls es nochmal wichtig wird, ein Gewicht
	def __init__(self,i):

		self.neighbours = []
		self.index = 0
		self.degree = 0
		self.name = ""

		self.index = i

	def setName(self,n):
		self.name = n

	def setNeighbour(self,v):
		self.neighbours.append(v)
		self.degree += 1

	def printNeighbours(self):
		prntstr = ""
		for i in self.neighbours:
			prntstr += str(i.name) + "  "
		return prntstr

class graph:
	#Graphen haben Einen Namen, Vertices, und ueber deren nachbarn, Edges.
	#durch angabe einer adjazenzmatrix kann ein graph generiert werden, ohne diese
	#bleibt er leer
	def __init__(self, mat, name):

		self.name = name
		self.adjmat = []
		self.vertices = []

		self.totalVertices = 0
		self.totalEdges    = 0

		self.nameIndexPair = {}#Hashmap fuer die vertices

		if mat != 0:
			if len(mat) == len(mat[0]):
				self.adjmat = mat
				self.initListFromMat()
			else:
				print("Adjazenzmatrizen mussen quadratisch sein.")

	def read(self, filepath):
		#einlesen und initialisieren
		#aus der Struktur im mis file wird intern eine Art zeigerstruktur
		vertices = 0
		edges    = 0

		if filepath.endswith(".mis"):
			misFile = open(filepath, "r").readlines()
			lineOne = misFile[0].split()
			
			if lineOne[0] == "p" and lineOne[1] == "edges":
				self.totalVertices = int(lineOne[2])
				self.totalEdges    = int(lineOne[3])
				print("Reading " + filepath)

				self.initializeVertices(misFile)
				self.initializeEdges(misFile)
				#####
				for v in self.vertices:
					print(v.name + " " + str(v.degree))
				#####
			else:
				return (".mis : invalid format")

		else:
			return ("unknown format")

	def initializeVertices(self, file):
		listV = []
		for i in range (0, self.totalVertices):
			listV.append(None)
		startTime = clock()
		for i in range (1,self.totalEdges + 1):
			vertexLHS = file[i].split()[1]
			vertexRHS = file[i].split()[2]
			if i % 100000 == 0:
				print("We are at line "+str(i) +" of " + str(self.totalEdges))
				if i % 1000000 == 0:
					print("(Took " + str(clock() - startTime) + " seconds until now.)")
			if listV[int(vertexLHS)] == None:
				listV[int(vertexLHS)] = vertexLHS
			if listV[int(vertexRHS)] == None:
				listV[int(vertexRHS)] = vertexRHS
		print("Es werden " + str(len(listV)) + " Vertices erstellt...")
		index = 0
		for v in listV:
			if v != None:

				newVertex = vertex(index)
				newVertex.setName(v)

				self.nameIndexPair.update( {v:index} )

				self.vertices.append(newVertex)
				index += 1
		print("Done.")
	def initializeEdges(self, file):
		
		for i in range (1,self.totalEdges + 1):
			nameLHS = file[i].split()[1]
			nameRHS = file[i].split()[2]#kann im monent sein, dass name rhs noch nicht existiert
			
			indexLHS = self.nameIndexPair[nameLHS]
			if i % 100000 == 0:
				print("Read "+str(i) +" Edges of " + str(self.totalEdges))
		
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
		#####ZU TESTZWECKEN#####
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
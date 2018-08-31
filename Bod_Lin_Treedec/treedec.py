import math

class TreeDec:

	def __init__(self, name):

		self.name = name
		
		self.bags = [] 			#I
		self.edges= [[],[]]

		self.vertices = []

		self.nameIndexPair = {}#Hashmap fuer die vertices

	def printDec(self):
		for i in self.bags:
			for vertices in i:
				pass

	def decompose(self, G, k):
		V = G.totalVertices
		E = G.totalEdges

		self.calculateInitialalues(k)

		#if E >= k * V - k * ( k+1 ) / 2:
			#self.devideVertexSets(k)
		#else:
			#print("Treewidth of " + self.name + " is bigger than " + str(k))
	def calculateInitialalues(self,k):
		c1 = 0.0
		c2 = -1.0
		d  = 0

		c1 = 2.0 / float(4*k**4 + 16*k**3 + 28*k**2 + 16*k)

		while c2 <= 0.0:
			c1 = c1 / 2.0
			c2 = (1.0 / float(4*k**2 + 12*k + 16)) - float(c1 * k**2*(k+1)) / 2.0

			print(str(c2))
		d = math.ceil((2*k) / c1)

		print("k = " + str(k) + ", c1 = " + str(c1) + ", c2 = " + str(c2)+ ", d = " + str(d))
	def devideVertexSets(self,k):
		d = (k + 2) ** 2 
		l = 1
		cg = 0.0
		cd = 0.0
		c1 = 0.0
		c2 = 0.0
		#while (c2 > 1.0 or c2 <= 0.0) and l != 0 and d <(k + 2) ** 2 + (2*k * self.totalVertices) / l:
		#	print ("__________")
		#	print("d = " + str(d))
		#	l = 0
#
#		#	for v in self.vertices:
#		#		if v.degree >= d:
#		#			l += 1
#		#	
#		#	print("l = " + str(l))
#		#	cg = float(l) / float(self.totalVertices)
#		#	print("cg = " + str(cg))
#		#	cd = float(2*k) / float(d)
#		#	print("cd = " + str(cd))
#		#	c1 = cg
#		#	if cd > cg:
#		#		c1 = cd
#		#	print("c1 = " + str(c1))
#		#	c2 = 1 / (4 * k**2 + 12*k + 16)   -   (c1 * k*k*(k+1)) / 2
#		#	print("c2 = " + str(c2))
		#	d += 1
		print(" ")
		print("k = "+ str(k))
		k = float(k)
		cc1 = float(  1 / ((2*k**2+6*k+8)* k**2 * (k+1) )  )
		cc2 = float(1 / (4 * k**2 + 12*k + 16)   -   (cc1 * k*k*(k+1)) / 2)
		s1 = float((2*k)/cc1 )
		s2 = float((k**2 +4*k+4) )

		print("cc1 = " + str(cc1*10**10) + ", cc2 = " + str(cc2*10**10))
		print("Schranke fuer l = " +   str(float(cc1*self.totalVertices)))
		print("S1 = " +   str(s1))
		print("S2 = " +   str(s2))

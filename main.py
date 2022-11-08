# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#BENEDEK ROBERT 931

#https://github.com/cs-ubbcluj-ro/Formal-Languages-and-Compiler-Design


#I made hash table - symbol table with 2 separate tables, one for variables and one for values, i used
#informations from this sites and i treated the case when the developer was in a rush and forgot to place
#spaces near "=" (ex: b=10 ) and the one with multiple declarations : integer a = 1, b = 2, ...
#The program is able to identify String, Integer, boolean values.


#https://www.w3schools.com/python/ref_string_split.asp

#https://www.vipinajayakumar.com/parsing-text-with-python/

#https://stephenagrice.medium.com/how-to-implement-a-hash-table-in-python-1eb6c55019fd

import re

INITIAL_CAPACITY = 1000


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class LinkedList: #linked list with value a tupple (poz reserved,poz sym) and key the inserted
	def __init__(self):
		self.head = None

	#could insert at the beggining
	def insert(self,key,value): #value is a tuple/pair
		if key == None:
			raise Exception("The key should not be None")
		if(self.head == None) :
			self.head = Node(key,value)

		else:
			node = self.head
			while node.next is not None:
				node = node.next
			# Add a new node at the end of the list with provided key/value
			node.next =  Node(key, value)

	def find(self,key):
		node = self.head
		while node is not None and node.key != key:
			node = node.next
		# Add a new node at the end of the list with provided key/value
		return node	#None if not found

class HashTable:
	def __init__(self):
		self.capacity = INITIAL_CAPACITY
		self.size = 0
		self.buckets = [None] * self.capacity

	def hash(self, key):
		hashsum = 0
		# For each character in the key

		for idx, c in enumerate(key):
			# Add (index + length of key) ^ (current char code)

			hashsum += (idx + len(key)) # ** ord(c)
			# Perform modulus to keep hashsum in range [0, self.capacity - 1]

			hashsum = hashsum % self.capacity
		return hashsum

	def insert(self, key):
		# 1. Increment size

		self.size += 1
		# 2. Compute index of key

		index = self.hash(key)
		# Go to the node corresponding to the hash

		node = self.buckets[index]
		# 3. If bucket is empty:

		if node is None:
			# Create node, add it, return

			self.buckets[index] = Node(key, self.size)
			return
		# 4. Collision! Iterate to the end of the linked list at provided index

		prev = node
		while node is not None:
			prev = node
			node = node.next
		# Add a new node at the end of the list with provided key/value

		prev.next = Node(key, self.size)

	def find(self, key):
		# 1. Compute hash

		index = self.hash(key)
		# 2. Go to first node in list at bucket

		node = self.buckets[index]
		# 3. Traverse the linked list at this node

		while node is not None and node.key != key:
			node = node.next
		# 4. Now, node is the requested key/value pair or None

		if node is None:
			# Not found

			return None
		else:
			# Found - return the data value

			return node.value

	def remove(self, key):
		# 1. Compute hash

		index = self.hash(key)
		node = self.buckets[index]
		prev = None
		# 2. Iterate to the requested node

		while node is not None and node.key != key:
			prev = node
			node = node.next
		# Now, node is either the requested node or none

		if node is None:
			# 3. Key not found

			return None
		else:
			# 4. The key was found.

			self.size -= 1
			result = node.value
			# Delete this element in linked list

			if prev is None:
				node = None
			else:
				prev.next = prev.next.next
			# Return the deleted variable

			return result

class Compiler :
	def __init__(self):
		self.problem = ""
		self.symbols = HashTable()
		self.values = HashTable()
		self.types = ["string", "integer","boolean"]
		self.reservedKeyword = ["integer", "while", "if",  "elif", "else", "string", "input", "input_integer", "input_string",
								"print", "boolean"]
		self.reservedKeywordTable = HashTable()
		self.PIF = LinkedList()

	def isIdentifier(self,elem):
		return bool(re.search("^[a-zA-Z_][a-zA-Z_0-9]*$", elem))

	def isConstant(self,elem):
		if elem == "true" or elem == "false":
			return True
		return bool(re.search("^[0-9]*$", elem)  or
					 re.search("^\"[a-zA-Z]*\"$",elem))


	def readProblem(self,file):
		f = open(file, "r")
		text = ""
		for line in f:
			text+=line
		#all_of_it = f.read()
		f.close()
		return text

	def getReservedKeywords(self,file):
		f = open(file, "r")
		for line in f:
			line = line.strip()
			self.reservedKeywordTable.insert(line)


	def scanner(self,text):
		self.problem = text
		text = re.split(';|{|}', text) # get rows

		lineNumber = 0
		for line in text: #Take each line

			line = line.strip().split(' ')
			i = 1
			#print (line)
			if(line[0] in self.types):
									#if we have a declaration
				while i < len(line):	 #the hole line
					line[i] = line[i].strip()

					if not (line[i] in self.reservedKeyword):
						if self.isIdentifier(line[i]):
							word = line[i]
							self.symbols.insert(word)
							#print(word)
							if (i + 1 < len(line) and line[i + 1].strip() == '='):

								if( i + 2 < len(line) and line[i+2] and self.isConstant(line[i+2])):
									self.values.insert(line[i + 2])
								else:
									print("lexical error" + lineNumber.__str__())
									return
								i += 2  # skip the next = and the the value assigned to word

						elif line[i].__contains__('=') :   #treat case b=10
							words = line[i].split('=')
							if len(words) == 2 and self.isIdentifier(words[0]):
								self.symbols.insert(words[0])
								if self.isConstant(words[1]):
									self.values.insert(words[1])
					i += 1
			elif not (line[0] in self.reservedKeyword) and self.isIdentifier(line[0]) : #if we have an identifier but is not declared
				if self.symbols.find(line[0]) is None:
					print("lexical error" + lineNumber.__str__())
					return
				elif ( len(line) == 3 and line[1].strip() == '=' and self.isConstant(line[2])):
					self.values.insert(line[2])

			lineNumber += 1
			#if line[i] not in self.reservedKeyword and  self.isIdentifier(line[i]) and i + 2 < len()

	def getPIF(self):
		text = self.problem
		text = text.replace(";"," ;")
		text = text.replace("("," ( ")
		text = text.replace(")"," ) ")
		text = text.replace("{"," { ")
		text = text.replace("}"," } ")
		#text = text.replace("\n"," ")
		#print(self.reservedKeywordTable.buckets)
		#print(text)

		text = text.split("\n")
		#text = text.split(" ")
		#print(text)
		lineNumber = 0
		for line in text:
			line = line.split(" ")

			#print(line)
			for elem in line:
				if(elem != ""):
					elem = elem.strip()
					#print(elem)
					rw = self.reservedKeywordTable.find(elem)
					#print(rw)
					if rw is None:

							if self.isIdentifier(elem):  #CONST = 1; IDENT = 2
								indexIndent =  self.symbols.find(elem)
								#print(indexIndent)
								if indexIndent != None:
									self.PIF.insert(elem,(2,indexIndent))
								else:
									print("Alexical error " + lineNumber.__str__())
									return
							elif self.isConstant(elem):
								indexConst = self.values.find(elem)
								#print(indexConst)
								if(indexConst != None):
									self.PIF.insert(elem,(1,indexConst))
								else:
									print("Blexical error " + lineNumber.__str__())
									return
							else:
								print("Clexical error " + lineNumber.__str__() + " token : " + elem)
								return ;
					else:
						self.PIF.insert(elem,(rw,-1))

			lineNumber += 1


	#Print the symtables
	def afisSym(self):
		for node in self.symbols.buckets:
			while node != None :
				print (node.key + "  Index  - > " + str(node.value))
				node = node.next

	def afisRW(self):
		for node in self.reservedKeywordTable.buckets:
			while node != None:
				print(node.key + "  Index  - > " + str(node.value))
				node = node.next
	def afisVal(self):
		for node in self.values.buckets:
			while node != None :
				print (node.key + "  Index  - > " + str(node.value))
				node = node.next

	def afisPIF(self):
			node = self.PIF.head
			while node != None :
				#print(node.key)
				print (node.key + "  Tuple  - > (" + str(node.value[0]) + " , " + str(node.value[1] )+ ")")
				node = node.next

	def printAll(self):
		print("\nIdentifiers")
		self.afisSym()
		print("\nConstants")
		self.afisVal()
		print("\nPIF")
		self.afisPIF()

	def afisReservedKeywordsTable(self):
		for node in self.reservedKeywordTable.buckets:
			while node != None :
				print (node.key + "  Index  - > " + str(node.value))
				node = node.next



if __name__ == '__main__':

	problem1 =  "\n" \
			"a = 11 ;\n"\
			"integer i = 2;\n"\
			"boolean prime = true;\n" \
 		 	"while (i < a/2 A prime == true) {\n" \
				" if (a mod i == 0) {\n"\
					"prime = false;\n" \
				" }\n"\
			"i = i + 1;\n"\
			"}\n"\
			"if(prime == true) {\n" \
				"print(“The number is prime”);\n"\
			"}\n"\
			"elif (prime == false) {\n"\
					"print(“Thenumberisnotprime”);\n"\
			"}\n"
	p1error = ""
	stringMy =  "integer a = 5;" \
				"integer x , y , z; " \
			"integer b=10 ;" \
			"integer c = 131 ;" \
			"x = 2001 ;" \
		   "string something = \"somestring\" ;" \
		   "integer ok = 1 , kg = 86;"

	ST = Compiler()
	ST.getReservedKeywords("token.txt")

	#problem2Text = ST.readProblem(r"C:\Users\Beni\Desktop\sem5\lftc\Programe\problem1.txt")
	problem2Text = ST.readProblem("problem2.txt")
	#problem2Text = ST.readProblem("p1error.txt")
	#problem2Text = ST.readProblem("problem3.txt")
	#ST.scanner(problem1Text)
	ST.scanner(problem2Text)
	#ST.scanner(problem3Text)
	#ST.scanner(problem1)

	ST.getPIF()

	print("PRINT ALL \n ")
	ST.printAll()


#TODO figure it out what are the constants "strings" and true, false and solve maximum = b ( chech if is const else dont do anything
#TODO if we habe maximum = a i dont have to do anything right ?
#todo MY STRIngs cant have spaces between "some string"
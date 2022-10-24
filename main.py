# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#BENEDEK ROBERT 931



INITIAL_CAPACITY = 1000


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

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

			hashsum += (idx + len(key)) ** ord(c)
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

class SymbolTable :
	def __init__(self):
		self.symbols = HashTable()
		self.values = HashTable()
		self.types = ["string", "integer","boolean"]
		self.reservedKeyword = ["integer", "while", "if",  "elif", "else", "string", "input", "input_integer", "input_string",
								"print", "boolean"]

	def scanner(self,text):

		text = text.split(";") # get rows


		for line in text: #Take each line
			line = line.strip().split(' ')
			i = 1
			if(line[0] in self.types):   #if we have a declaration
				while i < len(line):	 #the hole line
					line[i] = line[i].strip()

					if line[i] != '' and  line[i] != '=' and line[i] != ',' and not (line[i] in self.reservedKeyword): # no tokens
						if not line[i].__contains__('=') : # avoid b=10
							word = line[i]
							self.symbols.insert(word)

							if( i+1 < len(line) and line[i+1].strip() == '='):
								self.values.insert(line[i+2])
								i+=2   #skip the next = and the the value assigned to word
						else:  #treat case b=10
							words = line[i].split('=')

							if len(words) == 2 :
								self.symbols.insert(words[0])
								self.values.insert(words[1])
					i += 1
	#Print the symtables 
	def afisSym(self):
		for node in self.symbols.buckets:
			while node != None :
				print (node.key + "  Value  - > " + str(node.value))
				node = node.next
	def afisVal(self):
		for node in self.values.buckets:
			while node != None :
				print (node.key + "  Value  - > " + str(node.value))
				node = node.next

if __name__ == '__main__':

	problem1 =  "integer a;\n" \
			"a = input();\n"\
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
					"print(“The number is not prime”);\n"\
			"}\n"

	stringMy =  "integer a = 5; " \
			"integer b=10 ;" \
			"integer c = 131 ;" \
		   "string something = \"somestring\" ;" \
		   "integer ok = 1 , kg = 86;"

	ST = SymbolTable()
	#ST.scanner(stringMy)
	ST.scanner(problem1)

	print("afis")
	ST.afisSym()
	print("\nafis Values")
	ST.afisVal()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

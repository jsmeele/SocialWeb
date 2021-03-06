import csv
class featureExtraction:
	def __init__(self):
		self.feature = {}
		self.attr = []
		self.root = ''
		self.nrc_processed = self.root + 'nrc.csv'
		self.nrc = self.root + 'NRC_emotion_lexicon_list.txt'
		self.words = set()
        
	def getFeature(self):
		category = set()
		temp = []
		with open(self.nrc, 'r') as f:
			for row in f:
#				print(row)
				self.words.add(row.split()[0])
				category.add(row.split()[1])
				temp.append(row.split())
		category = list(category)
#		print(category)
#		print(self.words)
		for item in self.words:
			feature = [0]*10
			for elem in temp:
#				print(elem)
				if elem[0] == item:
#					print(elem[0])
					if elem[1] in category:
#						print(elem[1])
						feature[category.index(elem[1])] = int(elem[2])
#			print(feature)
			self.feature[item] = feature
			self.attr = category
		with open(self.nrc_processed, 'w', newline='') as f:
			writer = csv.writer(f)
			for k, v in self.feature.items():
				writer.writerow([k] + v)
                
x = featureExtraction()
x.getFeature()
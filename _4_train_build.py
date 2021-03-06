import re
import string
import pandas as pd
import nltk
#self.lemmatizer.lemmatize(
class trainBuild:
	def __init__(self):
		self.root = ''
		self.nrc_processed = self.root + 'nrc.csv'
		self.mypersonality = self.root + 'mypersonality.csv'
		self.stop = list(set(nltk.corpus.stopwords.words('english')))
		self.nrc  =[]
		self.nrc_scores = {}
		self.data = pd.DataFrame()
		self.lemmatizer = nltk.stem.WordNetLemmatizer()
		self.noWord = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	def getValues(self):
		nrc = pd.read_csv(self.nrc_processed, header = None, index_col = False)
		for index, row in nrc.iterrows():
			self.nrc_scores[row[0]] = row[1:].values.tolist()
			self.nrc.append(row[0])
		self.data = pd.read_csv(self.mypersonality, encoding = 'ISO-8859-1')

	def getStatusProcessed(self):
		status = []

		for index, row in self.data.iterrows():
#			print(index)
			text = row['STATUS']
			attr = []
            
			text = re.sub(r'(?:@\S*|#\S*|http(?=.*://)\S*)', '', text.rsplit('\n')[0].lower())
			text = text.replace('rt', '').rsplit('\n')[0]
			for word in text.translate(str.maketrans('','',string.punctuation)).split():
				word = self.lemmatizer.lemmatize(word)
				if(word in self.nrc and word not in self.stop and word in self.nrc):
					attr.append(self.nrc_scores[word])
				else:
					attr.append(self.noWord)
			
			status.append([sum(x) for x in zip(*attr)])
#			print(status)
#            tot = 0
#			for tw in [sum(x) for x in zip(*attr)]:
#                tweet.append(tw)
#                tot = tot + tw
#    
#            if(tot > 0):
#                tweet.append(True)
#            else:
#                tweet.append(False) 
		#status = filter(None, status)
		## keep only english status, and clean the .csv file
		label_delete = [i for i, v in enumerate(status) if not v]
#		print(label_delete)
		self.data.drop(label_delete, inplace = True)
		self.data.to_csv('mp_extended.csv', index = False, header = False)
		mat = [] ## store processed numerical vectors
		for index, row in self.data.iterrows():
#			print(row[2:12].replace('n',0).replace('y',1))
			mat.append(status[index] + row[2:12].replace('n',0).replace('y',1).values.tolist())
#			print(status[index] + row[2:12].values.tolist())
#		print(pd.DataFrame(mat))
		pd.DataFrame(mat).to_csv('mp_trainset.csv', index = False, header = False)
x = trainBuild()
x.getValues()
x.getStatusProcessed()
print('DONE')
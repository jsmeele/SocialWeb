import os
import pickle
import pandas as pd
import numpy as np
#from trainProcess import trainProcess



class modelRun:
	def __init__(self):
		self.path = os.path.dirname(os.path.realpath(__file__))
		self.label_model = {} ## to store classfication model
		self.modelYes = {} ## to store regression "yes" model
		self.modelNo = {} ## to store regression "no" model
		self.name = [] ## trait names
	## get the list of all docs 
	## output: list that contains testing filenames
	def getDocs(self):
		docs = []
		for r, d ,f in os.walk(self.path):
			for files in f:
				if files.endswith("_clean.csv"):
					docs.append(files)
		return docs
	## get trained model
	## output: update dict to store trained model
	def getModel(self):
#		m = trainProcess()
#		self.name = m.name
		self.name = ["ext", "neu", "agr", "con", "opn"]
#		self.label_model = m.trainModelLabel()
#		m.saveModel()
		self.label_model = pickle.load(open('model.pickle', 'rb'))
		self.modelYes = pickle.load(open('modelYes.pickle', 'rb'))
		self.modelNo = pickle.load(open('modelNo.pickle', 'rb'))
        
	## apply trained model on validation dataset
	## user: user's processed data to scan, gathered from getDocs
	def getTrained(self, user):
#		print('-----------------')
#		s = self.path + user
#		print(s)
		dt = pd.read_csv(user, header=None) #.iloc[:,-10])
#		print(dt.head())
		dt2 = dt.iloc[:,-10:]
#		print('-----------------')
#		print(dt2.head())
##		print(dt.iloc[0,-10:])
#		print('*************')
		pred = []
		for item in self.name:
			pre = pickle.loads(self.label_model[item]).predict(dt2).tolist()
			pred.append(pre)
		pred = np.matrix(np.array(pred))
		mat = pd.concat([dt2, pd.DataFrame(pred.transpose())], axis = 1)
		mat.columns = ['anticipation', 'joy', 'negative', 'sadness', 
			'disgust', 'positive', 'anger', 'surprise', 'fear', 'trust',
			'ext', 'neu', 'agr', 'con', 'opn']
		pd.DataFrame(mat).to_csv(user[:-4] + "_processed.csv", header = True, index = False)
		return mat
	## apply regression model on classified dataset
	## mat: dataframe from getTrained()
	## trait: trait to be regressed
	## statis: predicted label, 1 for yes, N for 0
	def getRegressed(self, mat, trait, status):
		sample = mat[mat[trait] == status]## could be empty
		if(sample.empty):
			return [0]
		else:
			sample = sample.iloc[:, 0:10]
			if(status == 1):
				pre = pickle.loads(self.modelYes[trait]).predict(sample).tolist()
				return pre
			else:
				pre = pickle.loads(self.modelNo[trait]).predict(sample).tolist()
				return pre
	## get "final" score for each trait for each user
	## a driver function for this class
	def getRated(self):
		self.getModel()
		docs = self.getDocs()
		for files in docs:
			print("processing classification validation user file: ", files)
			mat = self.getTrained(files)
			print("processing regression validation user file: ", files)
			s = {}
			for each in self.name:
				pre1 = self.getRegressed(mat, each, 1)
				pre2 = self.getRegressed(mat, each, 0)
				score = (np.mean(pre1)*len(pre1) + np.mean(pre2)*len(pre2))/(len(pre1) + len(pre2))
				s[each] = score
			for k, v in s.items():
				print(k, v)
x = modelRun()
#print(x.getDocs())
x.getRated()
import pandas as pd
import os

def make_train_dict(inputPath):
	df = pd.read_csv(inputPath)
	packedData = df['Body']
	print(len(packedData))

def load_data(inputDir):
	# Find training data
	trainingPath = os.path.join(inputDir, "train.csv")
	validPath = os.path.join(inputDir, "valid.csv")
	testPath = os.path.join(inputDir, "test.csv")

	make_train_dict(trainingPath)

load_data("./train_data/")
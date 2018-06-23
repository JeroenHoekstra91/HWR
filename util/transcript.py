import numpy as np
import types

def generate_transcripts(ngrams_model, sorted_window_groups, character_map, confidence_map):
	transcripts = {}
	end = np.zeros((1, len(sorted_window_groups)))
	for i in range(len(sorted_window_groups)):
		end[0,i] = len(sorted_window_groups[i])

	for counter in _count(end):
		word = ""
		number_of_windows = []
		cnn_confidence_sum = 0

		for i in range(len(sorted_window_groups)):
			group = sorted_window_groups[i][int(counter[0,i])]
			character = character_map[group[0][0]][group[0][1]]
			word += character + " "
			number_of_windows.append(len(group))

			for coor in group:
				cnn_confidence_sum += confidence_map[coor[0], coor[1]]

		word = word.strip()
		word = " ".join(word.split(" ")[::-1])
		number_of_windows = number_of_windows[::-1]
		
		if word in transcripts.keys():
			transcripts[word]["cnn_confidence_sum"] += cnn_confidence_sum
			for i in range(len(number_of_windows)):
				transcripts[word]["number_of_windows"][i] += number_of_windows[i]
		else:
			klass = word.split(' ')[-1]
			feature = '_'.join(word.split(' ')[0:-1])
			ngrams_likelihood = ngrams_model.classify(klass, feature)

			transcripts[word] = {}
			transcripts[word]["ngrams_likelihood"] = ngrams_likelihood
			transcripts[word]["cnn_confidence_sum"] = cnn_confidence_sum
			transcripts[word]["number_of_windows"] = number_of_windows

	transcripts = [dict({"word": key}, **value) for (key, value) in transcripts.items()]
	transcripts.sort(key=lambda x: x["cnn_confidence_sum"], reverse=True)
	return transcripts

def to_hebrew(word):
	hebrew = ""
	for character in word.split(" "):
		hebrew += hebrew_map[character]
	return hebrew

def filter_transcripts(transcripts, ngrams_likelihood_threshold=0.0):
	return [x for x in transcripts if x["ngrams_likelihood"] > ngrams_likelihood_threshold]

def where(element, collection):
	sub_collection = list(collection)
	index = [0]
	indices = []
	
	while True:
		while index[-1] == len(sub_collection):
			if len(index) == 1: return indices
			
			# Backtrack by one
			index = index[:-1]
			index[-1] += 1
			sub_collection = list(collection)
			
			for i in range(len(index) - 1):
				sub_collection = sub_collection[index[i]]

		if type(element) == types.LambdaType:
			if not type(sub_collection[index[-1]]) in [list, np.ndarray]:
				try:
					if element(sub_collection[index[-1]]):
						indices.append(list(index))
				except: pass
		elif sub_collection[index[-1]] == element:
			indices.append(list(index))	

		if type(sub_collection[index[-1]]) in [list, np.ndarray]:
			# Step into list element
			sub_collection = sub_collection[index[-1]]
			index.append(0)
		else:
			index[-1] += 1


#### HELPER FUNCTIONS ####

def _count(end):
	if len(end[0]) == 0: return
	counter = np.zeros_like(end)
	while True:
		yield counter
		counter[0,0] += 1
		for i in range(len(counter[0])):
			if counter[0,i] != 0 and counter[0,i] % end[0,i] == 0:
				counter[0,i] = 0
				try:
					while end[0, i+1] == 0:
						i += 1
					counter[0,i+1] += 1
				except IndexError: return
import numpy as np

def generate_transcripts(ngrams_model, filtered_window_groups, character_map, confidence_map):
	transcript = {}
	end = np.zeros((1, len(filtered_window_groups)))
	for j in range(len(filtered_window_groups)):
		end[0,j] = len(filtered_window_groups[j])

	for counter in _count(end):
		word = ""
		number_of_windows = 0
		cnn_confidence_sum = 0

		for j in range(len(filtered_window_groups)):
			group = filtered_window_groups[j][int(counter[0,j])]
			character = character_map[group[0][0]][group[0][1]]
			word += character + " "
			number_of_windows += len(group)

			for coor in group:
				cnn_confidence_sum += confidence_map[coor[0], coor[1]]

		word = word.strip()
		
		transcript_element = {
			"cnn_confidence_sum": cnn_confidence_sum,
			"number_of_windows": number_of_windows
			}

		if word in transcript.keys():
			for key in transcript_element.keys():
				transcript[word][key] += transcript_element[key]
		else:
			ngrams_likelihood = ngrams_model.classify(word.split(" ")[0], "_".join(word.split(" ")[1:]))
			transcript[word] = transcript_element
			transcript[word]["ngrams_likelihood"] = ngrams_likelihood

	transcript = [dict({"word": key}, **value) for (key, value) in transcript.items()]
	transcript.sort(key=lambda x: x["cnn_confidence_sum"], reverse=True)
	return transcript

### HELPER FUNCTIONS ###

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
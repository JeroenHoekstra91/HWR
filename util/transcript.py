import numpy as np
import types
from util.sliding_window import *
from util.character_map import to_hebrew


def generate_transcripts(ngrams_model, window_groups, character_map, confidence_map,
    ngrams_depth=2, ngrams_weights=[.4,.6]):
    transcripts = []
    sort_window_groups(window_groups, character_map, confidence_map)
    
    return traverse_characters(ngrams_model,
        list(window_groups[::-1]),
        character_map,
        confidence_map,
        ngrams_weights=ngrams_weights)

def traverse_characters(ngrams_model, window_groups, character_map, confidence_map, 
    ngrams_weights=[.4,.6], word=[], character_index=0):
    transcripts = []
    sequence_end = 0
    for group_index in range(len(window_groups[character_index])):
        word.append(get_label(window_groups[character_index][group_index][0], character_map))

        # exit on likelihood == 0 for all possible characters at position character_index
        if len(word) >= 2:
            ngrams_likelihood = ngrams_model.classify(word[-1], "_".join(word[-2:-1]))
            if ngrams_likelihood == 0:
                word = word[:-1]
                sequence_end += 1
                if sequence_end == len(window_groups[character_index]):
                    return -1
                continue

        # exit on word end
        if len(word) == len(window_groups):
            return [" ".join(word)]

        # traverse deeper
        transcript = traverse_characters(ngrams_model,
            window_groups,
            character_map,
            confidence_map,
            ngrams_weights=ngrams_weights,
            word=list(word), 
            character_index=character_index + 1)

        if transcript == -1:
            if group_index == len(window_groups[character_index])-1 and len(transcripts) == 0:
                # prune possible characters
                print "pruning"
                window_groups[character_index].pop(group_index)
        else:
            transcripts += transcript
        word = word[:-1]
    return transcripts




def generate_transcripts_depricated(ngrams_model, window_groups, character_map, confidence_map,
    ngrams_depth=2, ngrams_weights=[.4,.6]):
    
    transcripts = {}
    end = np.zeros((1, len(window_groups)))
    for i in range(len(window_groups)):
        end[0, i] = len(window_groups[i])

    for counter in _count(end):
        word = ""
        number_of_windows = []
        cnn_confidence_sum = 0

        for i in range(len(window_groups)):
            if(len(window_groups[i]) == 0):
                continue

            group = window_groups[i][int(counter[0, i])]
            character = get_label(group[0], character_map)
            word += character + " "
            number_of_windows.append(len(group))

            for coor in group:
                cnn_confidence_sum += get_confidence(coor, character_map, confidence_map)

        word = word.strip()
        word = " ".join(word.split(" ")[::-1])
        number_of_windows = number_of_windows[::-1]

        if word in transcripts.keys():
            transcripts[word]["cnn_confidence_sum"] += cnn_confidence_sum
            for i in range(len(number_of_windows)):
                transcripts[word]["number_of_windows"][i] += number_of_windows[i]
        else:
            ngrams_likelihood = calculate_ngrams_likelihood(ngrams_model, word, 
                ngrams_depth=ngrams_depth, ngrams_weights=ngrams_weights)

            transcripts[word] = {}
            transcripts[word]["ngrams_likelihood"] = ngrams_likelihood
            transcripts[word]["cnn_confidence_sum"] = cnn_confidence_sum
            transcripts[word]["number_of_windows"] = number_of_windows

    transcripts = [dict({"word": key}, **value) for (key, value) in transcripts.items()]
    transcripts.sort(key=lambda x: x["cnn_confidence_sum"], reverse=True)
    return transcripts


def calculate_ngrams_likelihood(model, word, ngrams_depth=2, ngrams_weights=[.4,.6]):
    if np.sum(ngrams_weights) != 1: raise ValueError('Sum of ngrams weights needs to be 1')
    word_length = len(word.split(' '))
    ngrams_likelihood = 1.0/27.0 * ngrams_weights[0] * word_length

    for i in range(2, ngrams_depth + 1):
        for j in range(word_length - i + 1):
            combination = word.split(' ')[j:j + i]
            klass = combination[-1]
            features = "_".join(combination[:-1])
            ngrams_likelihood += ngrams_weights[i - 1] * model.classify(klass, features)
            
    return ngrams_likelihood


def write_to_file(filename, word):
    file = open(filename, "a")
    file.write(to_hebrew(word) + "\n")
    file.close()

def sort_by_relevance(transcripts, cnn_confidence_weight=1, ngrams_likelihood_weight=1):
    transcripts.sort(key=lambda x:
        x["cnn_confidence_sum"] * cnn_confidence_weight +
        x["ngrams_likelihood"] * ngrams_likelihood_weight,
        reverse=True)


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
                except:
                    pass
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
        counter[0, 0] += 1
        for i in range(len(counter[0])):
            if counter[0, i] != 0 and counter[0, i] % end[0, i] == 0:
                counter[0, i] = 0
                try:
                    while end[0, i + 1] == 0:
                        i += 1
                    counter[0, i + 1] += 1
                except IndexError:
                    return

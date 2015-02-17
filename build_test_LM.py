#!/usr/bin/python
import re
import nltk
import sys
import getopt
import codecs
import math

NORMALIZE_LOWERCASE = True # for toggling between n-gram normalization to lowercases

def build_LM(input_file_name):
    """
    build language models for each label
    each line in in_file contains a label and an URL separated by a tab(\t)
    """
    print ('building language models...')
    
    # index 0: Malaysian, index 1: indonesian, index 2: Tamil
    LM = [
        [0, {}], # Malaysian:   [total counts, 4-gram hashmap]
        [0, {}], # Indonesian:  [total counts, 4-gram hashmap]
        [0, {}]  # Tamil:       [total counts, 4-gram hashmap]
    ]
    combined_set = set()    # a set of all the 4-grams from all models combined
    in_file = codecs.open(input_file_name, encoding='utf-8')
    for line in in_file:
        """ determine language in line """
        language = ''
        index = 0
        for char in line:
            index += 1
            if char == " ":
                break
            language += char
        """ preprocess line """   
        line = line[index:]         # remove the language word from line e.g. "malaysian "
        if NORMALIZE_LOWERCASE:     # if True, convert string to lower case
            line = line.lower()
        line = "SSS" + line + "EEE" # prepend and append start and end tokens. Respectively: 'S' and 'E'
        
        """ populate LM with all 4-grams in line """
        if (language == "malaysian"):
            populate_lang_model(line, LM[0], combined_set)
        elif (language == "indonesian"):
            populate_lang_model(line, LM[1], combined_set)
        elif (language == "tamil"):
            populate_lang_model(line, LM[2], combined_set)
    in_file.close()

    """ update each language model with the other 4-grams in combined_set """
    # update total counts
    for i in range(3):
        LM[i][0] += len(combined_set) - len(LM[i][1])

    # add new four_grams from combined set
    for four_gram in combined_set:
        for i in range(3):
            if not four_gram in LM[i][1]:
                LM[i][1][four_gram] = 1     # add to model

    return LM

def populate_lang_model(line, lang_model, combined_set):
    # for each 4-gram in given line
    for i in range(len(line) - 3):
        four_gram = line[i: i + 4]   # get four_gram as a substring

        # add to combined set
        if not four_gram in combined_set:
            combined_set.add(four_gram)

        # add to language model
        if not four_gram in lang_model[1]:
            lang_model[1][four_gram] = 2    # start at 2 because of add 1 smoothing
            lang_model[0] += 2              # update total count
        else:
            lang_model[1][four_gram] += 1
            lang_model[0] += 1              # update total count
    
def test_LM(input_file_name, output_file_name, LM):
    """
    test the language models on new URLs
    each line of in_file contains an URL
    you should print the most probable label for each URL into out_file
    """
    print ("testing language models...")
    in_file = codecs.open(input_file_name, encoding='utf-8')
    out_file = codecs.open(output_file_name, 'w', encoding='utf-8')
    
    # for each line in test file
    for line in in_file:
        prob_list = []      # list of probabilities
        # determine most probable language
        prob_list.append((get_probability(line, LM[0]), "malaysian"))
        prob_list.append((get_probability(line, LM[1]), "indonesian"))
        prob_list.append((get_probability(line, LM[2]), "tamil"))
        prob_list.sort(key = lambda x: x[0])

        """
        Determining 'other' languages
        Idea: if language belongs to 'other', then we can also say that it is equally likely to come from any of the three langauges
        Thus the approach is look at a "tight bound" scenario where all three language models produces smiliar probability
        To do this, I evaluate the probability ratio of the most probable language to that of the least probable language
        """
        is_other = (prob_list[2][0] / prob_list[0][0]) < 5   # experimentally determined value (see README.txt)
        
        # write to out_file
        out_file.write((prob_list[2][1] if not is_other else "other") + " " + line)
    in_file.close()
    out_file.close()

# returns the probability of a line for a given language model
def get_probability(line, lang_model):
    if NORMALIZE_LOWERCASE:     # if True, convert string to lower case
        line = line.lower()
    line = 'SSS' + line + 'EEE'
    prob_list = []              # list of probabilities of all 4-grams
    
    # iterates through each 4-gram in line
    for i in range(len(line) - 3):
        four_gram = line[i: i+4]
        # only conisders 4-grams in language model
        if (four_gram in lang_model[1]):
            prob = float(lang_model[1][four_gram])/lang_model[0]    # raw probability evaluated
            prob = -1/math.log10(prob)  # normalize value (log to supress values, -1 to eliminate negatives and inverse to restore relative profiles)
            prob_list.append(prob)
            # print (prob) # check

    # evaluate and return total cumulative probability
    total_prob = 0
    if prob_list:   # if list is not empty
        total_prob = prob_list[0]
        for i in range(1, len(prob_list)):
            total_prob *= prob_list[i]
    return total_prob


def usage():
    print ("usage: " + sys.argv[0] + " -b input-file-for-building-LM -t input-file-for-testing-LM -o output-file")

input_file_b = input_file_t = output_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'b:t:o:')
except (getopt.GetoptError, err):
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-b':
        input_file_b = a
    elif o == '-t':
        input_file_t = a
    elif o == '-o':
        output_file = a
    else:
        assert False, "unhandled option"
if input_file_b == None or input_file_t == None or output_file == None:
    usage()
    sys.exit(2)

LM = build_LM(input_file_b)
test_LM(input_file_t, output_file, LM)
import os
import sys
import argparse
import numpy as np

# training list but with the " : " removed 
#trainingList = []

def create_trainingList(training_list):
    list_train = training_list.split('\n')
    trainingList = []
    wordsList = []
    tagsList = []
    for currLine in list_train:
        line = currLine.split(' : ') 
        if len(line) == 2:
            # passing into the global trainingList variable
            trainingList.append(line)
            tagsList.append(line[1])
            if line[0] not in ['.', '!', '?', ':', ';', '"', ","]:
                wordsList.append(line[0])
    

    return trainingList, wordsList, tagsList

# Determine number of states by finding unique text-tag pairs
def find_pairs(training_list):
    pairs = {}

    for currLine in training_list:
        line = currLine.split(' : ') 

        # passing into the global trainingList variable
        trainingList.append(line)

        if line[1] not in pairs.keys():
            pairs[line[1]] = [line[0]]
        else:
            pairs[line[1]].append(line[0])
        

    return pairs

def create_tags(training_list):
    l_tag = []
    d_tag = {}
    i = 0
    for _, tag in training_list:
        if tag not in l_tag:        # ensures uniquness
            l_tag.append(tag)
            d_tag[tag] = i
            i += 1
    
    return l_tag, d_tag

def create_text(training_list):
    l_text = []
    d_text = {}
    i = 0
    for text_init, _ in training_list:
        if text_init not in ['.', '!', '?', ':', ';', '"', ","]:
            text = text_init.lower()        
            if text not in l_text:      # ensures uniqueness
                l_text.append(text)
                d_text[text] = i
                i += 1
    
    return l_text, d_text

# Calculate the initial probability table by determing how likely a tag is to appear at the beginning of the sentence
def init_table(trainingList, l_tag, d_tag):
    sentTot = 0
    # find total number of sentence 
    for text, _ in trainingList:
        if text in ['!', '?', '.']:
            sentTot += 1

    newSent = True
    initTable = {}
    for text, tag in trainingList:
        if newSent:
            if tag not in initTable.keys():
                initTable[tag] = 1
            else:
                initTable[tag] += 1
            newSent = False
        elif text in ['.', '!', '?', '.']: 
            newSent = True
    
    init_vector = [0] * len(l_tag)
    '''# create the probability value inside initTable
    for val in initTable.values():
        val = val/sentTot'''
    
    for tag in l_tag:
        if tag in initTable.keys():
            init_vector[d_tag[tag]] = initTable[tag]/sentTot

    '''print(init_vector, len(init_vector))
    print(sum(init_vector))'''


    #print(d_tag['NP0'], l_tag[d_tag['NP0']])

    return init_vector      #, initTable

# Calculating the transition probabilty table by using the freq of first and next tag occuring (i.e. NN1 -> PRP)
def trans_table(trainingList, l_tag, d_tag):
    
    # create the two dimensional matrix
    trans_m1 = [0] * len(l_tag)
    trans_m = []
    for i in range(len(l_tag)):
        trans_m.append(trans_m1)

    i = 0
    
    while i < len(trainingList):
        pun=True
        # i keeps iterating until we reach word
        while pun:
            if trainingList[i][0] in ['.', '!', '?', ':', ';', '"', ","]:
                i+=1
            else:
                pun=False
        # word reached
        text1 = trainingList[i][0]
        tag1 = trainingList[i][1]

        j=i
        pun=True
        while pun:
            if trainingList[j] in [',',':',';','"']:
                j+=1
            else:
                pun=False     
              
        text2 = trainingList[j + 1][0]
        tag2 = trainingList[j+ 1][1]

        if text2 not in ['.','!','?']:
            trans_m[d_tag[tag1]][d_tag[tag2]] += 1
            i=j+1
        else:
            i=j+2
    
    for i in range(len(trans_m)):
        sum_i = sum(trans_m[i])
        for j in range(len(trans_m[i])):
            trans_m[i][j] = trans_m[i][j]/sum_i


    '''# j is lhs and i is rhs P(a|b) : prob of b transition to a
    for i in range(len(trans_m)):
        print(sum(trans_m[i]))'''

    return trans_m
    
# Calculate number of times a tag appears with every word in the training example (i.e. Smith : NN1)
def obs_table(trainingList, l_text, d_text, d_tag):

    # create the two dimensional matrix
    obs_m1 = [0] * len(l_text)
    obs_m = []
    for _ in range(len(l_tag)):
        obs_m.append(obs_m1)

    for pair in trainingList:
        if pair[0] not in ['.', '!', '?', ':', ';', '"', ","]:
            pair_lower = pair[0].lower()
            obs_m[d_tag[pair[1]]][d_text[pair_lower]] += 1

    for i in range(len(obs_m)):
        sum_i = sum(obs_m[i])
        for j in range(len(obs_m[i])):
            obs_m[i][j] = obs_m[i][j]/sum_i
    

    '''for i in range(len(obs_m)):
        print(sum(obs_m[i]))'''
    
    #print(d_text['detective'], l_text[d_text['detective']])

    return obs_m


def viterbi(inp, init_v, d_text, trans_m, obs_m):
    obs_m = np.array(obs_m)

    prob = np.zeros((len(inp), len(init_v)))
    prev = np.zeros((len(inp), len(init_v)))
    
    prob[0] = init_v*obs_m[:, d_text[inp[0].lower()]]      # take all the rows and get the index of words corresponding to first word observed, gets the prob of the first word over the tags, and the dimensions of the two things we're multiplying matches as a result 
    
    '''prob = matrix(length(E),length(S))
    prev = matrix(length(E),length(S))'''




if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--trainingfiles",
        action="append",
        nargs="+",
        required=True,
        help="The training files."
    )
    parser.add_argument(
        "--testfile",
        type=str,
        required=True,
        help="One test file."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file."
    )
    args = parser.parse_args()

    training_list = args.trainingfiles[0]
    print("training files are {}".format(training_list))

    print("test file is {}".format(args.testfile))

    print("output file is {}".format(args.outputfile))


    print("Starting the tagging process.")


    print((training_list))
    s=''
    for filename in training_list:
        f=open(filename)
        s=s+f.read()+'\n'
        f.close()
    #rint(s)
    trainingList, wordsList, tagsList = create_trainingList(s)
    print(len(trainingList), len(trainingList[0]))
    #print(wordsList)
    l_tag, d_tag = create_tags(trainingList)
    l_text, d_text = create_text(trainingList)
    print(len(l_text), len(l_text[0]))
    init_vector = init_table(trainingList, l_tag, d_tag)
    trans_m = trans_table(trainingList, l_tag, d_tag)
    obs_m = obs_table(trainingList,l_text, d_text, d_tag)
    #print(len(init_vector) )#, len(initTable))
    viterbi(wordsList, init_vector, d_text, trans_m, obs_m)

    # sanity check of the tables: PASSED
    '''p_np0 = obs_m[0]    # first row corresponding to np0 tag which gives us a distrubtion to all the words
    print(np.shape(p_np0))      # prob distr over vocab size for tag NP0
    sorted_indx_p_np0 = np.argsort(p_np0)       # return sorted version with the indices sorting it
    print(sorted_indx_p_np0[-100:])
    for i in (sorted_indx_p_np0[-100:]):      # indices are from lowest to highest
        print(p_np0[i])     # given NP0, what is the probability of this word
        #print(i)
        print(l_text[i])     # get the corresponding tags

    #print(d_text )'''

    

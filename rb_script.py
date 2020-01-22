import pandas as pd
import numpy as np
import csv
import re
from negex import *
from support_functions import *
from argparse import ArgumentParser

## Import tokenization methods
from nltk import word_tokenize, pos_tag
from nltk.tokenize import TweetTokenizer
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

# Import the negex trigger rules
#rfile - natural language negation rules
#ifile2 - structured negation rules
rfile = open(r'NegexRules/natural_rules.txt')
irules = sortRules(rfile.readlines())
ifile2 = open(r'NegexRules/structured_rules.txt')
irules2 = sortRules(ifile2.readlines())


def return_RB_approach(data_frame, note_c, SI_phrases, suicide_assessments):
    
    #Function Definition: This function executes the rule-based approach
    #Steps:
    # 1) It preprocesses the text by removing and replacing specific phrases within the text (punctuation, years, dates, suicide assessments)
    # 2) It tokenizes the note into an array of words.
    # 3) We identify the indexes in which the suicidal ideation terms exist and nearest "sentence breaks", which include periods, question marks, and colons.
    # 4) Based on the type of sentence break, a phrase is selected around the "suicidal ideation" term. This phrase is then fed into one of the two NegEx algorithms based on the structure of the phrase.
    # 5) The phrase is classified as either positive or negative and added to the respective set. The entire document is also flagged as 1 for positive or negative SI.
    
    
    positive_SI = [0 for i in range(len(data_frame))]
    negative_SI = [0 for i in range(len(data_frame))]
    pos_mention = [set() for i in range(len(data_frame))]
    neg_mention = [set() for i in range(len(data_frame))]
    
    for i in range(len(data_frame)):
        
        #preprocess this note
        this_note = data_frame[note_c].iloc[i].encode('ascii','ignore').decode().lower()
        this_note = preprocess_note(this_note, suicide_assessments)
    
        #tokenize this note
        note = tknzr.tokenize(this_note)
        
        #identify the locations of SI phrases
        indices = [r for r, x in enumerate(note) if x in SI_phrases]
        values = [x for r, x in enumerate(note) if x in SI_phrases]
        

        #Identify sentence breaks
        sentence_breaks = [m for m, x in enumerate(note) if x == '.' or x== '?' or x == ':' ]
        sentence_breaks.insert(0,0)
        sentence_breaks.append(len(note) - 1)
        
        #for each mention of SI
        for idx, places in enumerate(indices):
            
            #find the previous sentence break and next sentence break after the SI term
            for j, val in enumerate(sentence_breaks):
                if places > val:
                    next
                else:
                    prev = sentence_breaks[j - 1]
                    nex = sentence_breaks[j]
                    break
        
            #if the next sentence break is a period
            if note[nex] == '.':
                sub_array = note[prev:places + 2]
                substring = substring_period(sub_array, values, idx)
                
                #check to make sure string is not empty
                if len(substring) > 0:
                    neg_flag = natural_tagger(substring, SI_phrases, irules)
                    
                    if neg_flag == True:
                        negative_SI[i] = 1
                        neg_mention[i].add(substring)
                    else:
                        positive_SI[i] = 1
                        pos_mention[i].add(substring)
            
            #if the next sentence is a colon or question mark
            else:
    
                question = (note[nex] == '?')
                note_end = (nex == len(note) - 1)
                sub_array = note[prev:nex + 3]
                substring = ' '.join(sub_array)
                
                #check to make sure the string is not empty
                if len(sub_array) > 0:
                    #if end of the note
                    if note_end == True:
                        distance = -1
                    else:
                        distance = SI_distance(sub_array, question, values, idx)
                    
                    #Use the structured tagger form
                    if distance > 0 and distance < 5:
                        neg_flag = structured_tagger(substring, SI_phrases, irules2)
                    else:
                        neg_flag = natural_tagger(substring, SI_phrases, irules)
                    
                    if neg_flag == True:
                        negative_SI[i] = 1
                        neg_mention[i].add(substring)
                    else:
                        positive_SI[i] = 1
                        pos_mention[i].add(substring)
                            

    data_frame['pos'] = pd.Series(positive_SI, index = data_frame.index)
    data_frame['neg'] = pd.Series(negative_SI, index = data_frame.index)
    data_frame['pos_men'] = pd.Series(pos_mention, index = data_frame.index)
    data_frame['neg_men'] = pd.Series(neg_mention, index = data_frame.index)

    return data_frame

def create_predictions(data_frame):
    
    #Function Definition: This function generates the predictions based on the outputs of the mentions
    #In this case, all notes that have a positive current suicidal ideation mention will be classified as positive for current suicidal ideation.
    
    pred_SI = [0.0 for i in range(len(data_frame))]
    
    for i in range(len(data_frame)):
        
        if data_frame['pos'].iloc[i] == 1 :
            pred_SI[i] = 1.0

    data_frame['pred_SI'] = pd.Series(pred_SI, index = data_frame.index)

    
    return data_frame


## MAIN - starting the script

#Read in the arguments from the script
parser = ArgumentParser()
parser.add_argument("-d", dest = "data_path", required = True, help = "data path to read in")
parser.add_argument("-nc", dest = "note_text_column", required = True, help = "name of note text column")
parser.add_argument("-s", dest = "save_path", required = True, help = "data path to save to")
parser.add_argument("-a", dest = "accuracy_flag", required = False, help = "print accuracy")
parser.add_argument("-tc", dest = "truth_column", required = False, help = "name of true column")
args = parser.parse_args()
data_p = args.data_path
note_c = args.note_text_column
save_p = args.save_path
accuracy_f = int(args.accuracy_flag)
truth_c = args.truth_column

#Declare suicidal ideation phrases
#Declare suicide assessments to exclude
tknzr = TweetTokenizer()

with open('SI_Files/SI_phrases.txt') as f:
    content = f.readlines()
SI_phrases = [x.strip() for x in content]

with open('SI_Files/SI_assessments.txt') as f:
    content = f.readlines()
suicide_assessments = [x.strip() for x in content]

#Read in the data
df = pd.read_excel(data_p)

#Identify positive and negative mentions of current SI
df = return_RB_approach(df,note_c, SI_phrases, suicide_assessments)
# return the current SI predictions
df = create_predictions(df)

#print the accuracy score of the predictions - if test
if accuracy_f == 1:
    print (accuracy_score(df[truth_c], df['pred_SI']))
    print (classification_report(df[truth_c], df['pred_SI']))

#save the predictions to an excel file
df.to_excel(save_p, index = False)











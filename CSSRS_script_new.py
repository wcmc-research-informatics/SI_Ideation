import pandas as pd
import numpy as np
import re
import string
from negex import *
from support_functions import *
from argparse import ArgumentParser

from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

def run_taggers(substr, suicidal_ideation, phrase_list, plan_phrases, intent_phrases, these_rules,\
            hist_rules, plan_rules):

    neg = False
    pos = False
    plan = False
    intent = False
    neg_hist = False
    pos_hist = False

    tagger = negTagger(sentence = substr, phrases = phrase_list ,rules = these_rules, negP = False)
    hist_tagger = negTagger(sentence = substr, phrases = phrase_list ,rules = hist_rules, negP = False)
    
    if tagger.getNegationFlag() == 'negated':
        neg = True

    else:
        if '[PHRASE]' in  tagger.getNegTaggedSentence():
            pos = True
        if suicidal_ideation == True:
            tagger2 = negTagger(sentence = substr, phrases = plan_phrases,rules = plan_rules, negP = False)
            if '[PHRASE]' in  tagger2.getNegTaggedSentence() and tagger2.getNegationFlag() == 'affirmed':
                plan = True
                
            tagger3 = negTagger(sentence = substr, phrases = intent_phrases,rules = plan_rules, negP = False)
            if '[PHRASE]' in  tagger3.getNegTaggedSentence() and tagger3.getNegationFlag() == 'affirmed':
                intent = True
        
    if hist_tagger.getNegationFlag() == 'negated':
        neg_hist = True
    else:
        if '[PHRASE]' in hist_tagger.getNegTaggedSentence():
            pos_hist = True

    
    return pos,pos_hist, neg,neg_hist, plan, intent

def run_portion(this_text,sentence_breaks, phrase_list, phrase_list2, suicidal_ideation, intent_phrases, plan_phrases ):
    neg_mention = set()
    neg_hist_mention = set()
    pos_mention = set()
    pos_hist_mention = set()
    plan_mention = set()
    intent_mention = set()


    indices = set()
    for s in phrase_list2:
        if this_text.find(s) !=-1:
            all_idx = find_all_indexes(this_text, s)
            for j in all_idx:
                indices.add(j)
    indices = sorted(list(indices))

    for idx, places in enumerate(indices):
        next_break = list(filter(lambda x: x > indices[idx], sentence_breaks))[0]
        break_index = np.where(np.array(sentence_breaks) == next_break)[0][0]

        if this_text[next_break] == ':' or this_text[next_break] == '?':
        
            list_of_words = this_text[next_break:].split()
            max_length = min(len(list_of_words)-1,3)
        
            space = this_text.find(list_of_words[max_length], next_break) + len(list_of_words[max_length])
        
            
            substr = this_text[sentence_breaks[break_index - 1]: space]
            if suicidal_ideation == True:

                pos,pos_hist, neg,neg_hist, plan, intent = run_taggers(substr, suicidal_ideation, phrase_list, plan_phrases, intent_phrases,irules3 , irules8, irules4)
            
        
            else:
                pos,pos_hist, neg,neg_hist, plan, intent = run_taggers(substr, suicidal_ideation, phrase_list, plan_phrases, intent_phrases,irules6 , irules10, irules4)

            if pos == True:
                pos_mention.add(substr)
            if pos_hist == True:
                pos_hist_mention.add(substr)
            if neg == True:
                neg_mention.add(substr)
            if neg_hist == True:
                neg_hist_mention.add(substr)
            if plan == True:
                plan_mention.add(substr)
            if intent == True:
                intent_mention.add(substr)

    
        else:
        
            substr = this_text[sentence_breaks[break_index - 1]: next_break + 1]
        
            if suicidal_ideation == True:
                pos,pos_hist, neg,neg_hist, plan, intent = run_taggers(substr, suicidal_ideation, phrase_list, plan_phrases, intent_phrases,irules , irules7, irules4)

            else:
                pos,pos_hist, neg,neg_hist, plan, intent = run_taggers(substr, suicidal_ideation, phrase_list, plan_phrases, intent_phrases,irules5 , irules7, irules4)
        
            if pos == True:
                pos_mention.add(substr)
            if pos_hist == True:
                pos_hist_mention.add(substr)
            if neg == True:
                neg_mention.add(substr)
            if neg_hist == True:
                neg_hist_mention.add(substr)
            if plan == True:
                plan_mention.add(substr)
            if intent == True:
                intent_mention.add(substr)
                    
    if suicidal_ideation == True:
        return neg_mention, neg_hist_mention, pos_mention, pos_hist_mention, intent_mention, plan_mention
    else:
        return neg_mention,neg_hist_mention, pos_mention, pos_hist_mention


def run_algorithm(dataframe,note_c, breaks, SI_phrases, SI_phrases2, SB_phrases, SB_phrases2, SA_phrases, SA_phrases2, intent_phrases, plan_phrases):

    pos_SImention = [set() for i in range(len(dataframe))]
    neg_SImention = [set() for i in range(len(dataframe))]
    plan_SImention = [set() for i in range(len(dataframe))]
    intent_SImention = [set() for i in range(len(dataframe))]

    pos_histSImention = [set() for i in range(len(dataframe))]
    neg_histSImention = [set() for i in range(len(dataframe))]

    pos_SBmention = [set() for i in range(len(dataframe))]
    neg_SBmention = [set() for i in range(len(dataframe))]

    pos_histSBmention = [set() for i in range(len(dataframe))]
    neg_histSBmention = [set() for i in range(len(dataframe))]
    
    pos_SAmention = [set() for i in range(len(dataframe))]
    neg_SAmention = [set() for i in range(len(dataframe))]

    pos_histSAmention = [set() for i in range(len(dataframe))]
    neg_histSAmention = [set() for i in range(len(dataframe))]


    predSI_intent = [0 for i in range(len(dataframe))]
    predSI_plan = [0 for i in range(len(dataframe))]
    predSI = [0 for i in range(len(dataframe))]
    predSB = [0 for i in range(len(dataframe))]
    predSA = [0 for i in range(len(dataframe))]

    predhistSI = [0 for i in range(len(dataframe))]
    predhistSB = [0 for i in range(len(dataframe))]
    predhistSA = [0 for i in range(len(dataframe))]

    not_relevant = [0 for i in range(len(dataframe))]

    for i in range(len(dataframe)):
        this_text = dataframe[note_c].iloc[i].lower()

    #translator = str.maketrans(our_punct, ' '*len(our_punct))
    #this_text = this_text.translate(translator)
    
        this_text = preprocess_note2(this_text)

        sentence_breaks = set()
        for b in breaks:
            if this_text.find(b) != -1:
                all_b = find_all_indexes(this_text, b)
                for j in all_b:
                    sentence_breaks.add(j)
    
        sentence_breaks = sorted(list(sentence_breaks))
        sentence_breaks.insert(0,0)
        sentence_breaks.append(len(this_text) - 1)
    
    
        neg_SImention[i],neg_histSImention[i], pos_SImention[i],pos_histSImention[i],intent_SImention[i], plan_SImention[i] = run_portion(this_text, sentence_breaks, SI_phrases,SI_phrases2, True, intent_phrases, plan_phrases)
    
        neg_SBmention[i],neg_histSBmention[i], pos_SBmention[i], pos_histSBmention[i] = run_portion(this_text, sentence_breaks, SB_phrases, SB_phrases2, False, intent_phrases, plan_phrases)

        
        neg_SAmention[i],neg_histSAmention[i], pos_SAmention[i], pos_histSAmention[i] = run_portion(this_text, sentence_breaks, SA_phrases, SA_phrases2, False, intent_phrases, plan_phrases)
        
        
        if len(pos_SImention[i]) > 0:
            predSI[i] = 1
        
        if len(pos_histSImention[i]) > 0:
            predhistSI[i] = 1
        
        if len(pos_SBmention[i]) > 0: #or len(pos_SAmention[i]) > 0:
            predSB[i] = 1
    
        if len(pos_histSBmention[i]) > 0: #or len(pos_SAmention[i]) > 0:
            predhistSB[i] = 1
            
        if len(pos_SAmention[i]) > 0:
            predSA[i] = 1
        
        if len(pos_SAmention[i]) > 0:
            predhistSA[i] = 1
        
        if len(intent_SImention[i]) > 0:
            predSI_intent[i] = 1
        if len(plan_SImention[i]) > 0:
            predSI_plan[i] = 1

        if len(neg_SImention[i]) == 0 and len(pos_SImention[i]) == 0 and len(neg_SBmention[i]) == 0 and len(pos_SBmention[i]) == 0:
            not_relevant[i] = 1
        
    dataframe['predSI'] = pd.Series(predSI, index = dataframe.index)
    dataframe['predhistSI'] = pd.Series(predhistSI, index = dataframe.index)

    dataframe['pos_SI_men'] = pd.Series(pos_SImention , index = dataframe.index)
    dataframe['neg_SI_men']= pd.Series(neg_SImention , index = dataframe.index)

    dataframe['pos_SI_hist_men'] = pd.Series(pos_histSImention , index = dataframe.index)
    dataframe['neg_SI_hist_men']= pd.Series(neg_histSImention , index = dataframe.index)

    dataframe['plan_SImention'] = pd.Series(plan_SImention, index = dataframe.index)
    dataframe['predSI_plan'] = pd.Series(predSI_plan, index = dataframe.index)
    dataframe['intent_SImention'] = pd.Series(intent_SImention, index = dataframe.index)
    dataframe['predSI_intent'] = pd.Series(predSI_intent, index = dataframe.index)

    dataframe['pos_SB_men'] = pd.Series(pos_SBmention , index = dataframe.index)
    dataframe['neg_SB_men']= pd.Series(neg_SBmention , index = dataframe.index)
    
    dataframe['pos_SA_men'] = pd.Series(pos_SAmention , index = dataframe.index)
    dataframe['neg_SA_men']= pd.Series(neg_SAmention , index = dataframe.index)

    dataframe['pos_SB_hist_men'] = pd.Series(pos_histSBmention, index = dataframe.index)
    dataframe['neg_SB_hist_men']= pd.Series(neg_histSBmention, index = dataframe.index)
    
    dataframe['pos_SA_hist_men'] = pd.Series(pos_histSAmention, index = dataframe.index)
    dataframe['neg_SA_hist_men']= pd.Series(neg_histSAmention, index = dataframe.index)

    dataframe['predSB'] = pd.Series(predSB, index = dataframe.index)
    dataframe['predhistSB'] = pd.Series(predhistSB, index = dataframe.index)
    
    dataframe['predSA'] = pd.Series(predSA, index = dataframe.index)
    dataframe['predhistSA'] = pd.Series(predhistSA, index = dataframe.index)

    dataframe['not_relevant'] = pd.Series(not_relevant, index = dataframe.index)


    return dataframe

with open('SI_Files/full_si_phrases.txt') as f:
    content = f.readlines()
SI_phrases = [x.strip() for x in content]

with open('SI_Files/full_si_phrases2.txt') as f:
    content = f.readlines()
SI_phrases2 = [x.strip() for x in content]

with open('SI_Files/full_sa_phrases_new.txt') as f:
    content = f.readlines()
SA_phrases = [x.strip() for x in content]

with open('SI_Files/full_sa_phrases_new2.txt') as f:
    content = f.readlines()
SA_phrases2 = [x.strip() for x in content]

with open('SI_Files/full_sb_phrases_new.txt') as f:
    content = f.readlines()
SB_phrases = [x.strip() for x in content]

with open('SI_Files/full_sb_phrases_new.txt') as f:
    content = f.readlines()
SB_phrases2 = [x.strip() for x in content]


with open('SI_Files/plan_phrases_new.txt') as f:
    content = f.readlines()
plan_phrases = [x.strip() for x in content]

with open('SI_Files/intent_phrases_new.txt') as f:
    content = f.readlines()
intent_phrases = [x.strip() for x in content]

breaks = ['.', '?', ':']

rfile = open(r'NegexRules2/SI_natural.txt')
irules = sortRules(rfile.readlines())
ifile3 = open(r'NegexRules2/SI_post_rules.txt')
irules3 = sortRules(ifile3.readlines())
ifile4 = open(r'NegexRules2/SI_intent.txt')
irules4 = sortRules(ifile4.readlines())

rfile5 = open(r'NegexRules2/SB_natural.txt')
irules5 = sortRules(rfile5.readlines())
ifile6 = open(r'NegexRules2/SB_post_rules.txt')
irules6 = sortRules(ifile6.readlines())

rfile7 = open(r'NegexRules2/SI_natural_hist.txt')
irules7 = sortRules(rfile7.readlines())
ifile8 = open(r'NegexRules2/SI_post_hist_rules.txt')
irules8 = sortRules(ifile8.readlines())

rfile9 = open(r'NegexRules2/SB_natural_hist.txt')
irules9 = sortRules(rfile9.readlines())
ifile10 = open(r'NegexRules2/SB_post_hist_rules.txt')
irules10 = sortRules(ifile10.readlines())

parser = ArgumentParser()
parser.add_argument("-d", dest = "data_path", required = True, help = "data path to read in")
parser.add_argument("-nc", dest = "note_text_column", required = True, help = "name of note text column")
parser.add_argument("-s", dest = "save_path", required = True, help = "data path to save to")

args = parser.parse_args()
data_p = args.data_path
note_c = args.note_text_column
save_p = args.save_path

 
df = pd.read_excel(data_p)
 
df = run_algorithm(df, note_c, breaks, SI_phrases, SI_phrases2, SB_phrases, SB_phrases2,SA_phrases, SA_phrases2, intent_phrases, plan_phrases)

df.to_excel(save_p, index = False)


print (df['predSI'].value_counts())
print (df['predhistSI'].value_counts())

print (df['predSB'].value_counts())
print (df['predhistSB'].value_counts())

import pandas as pd
import numpy as np
from negex import *

def remove_this(x):
    #Function Defintion: This function removes unncessary punctuation from the string
    x = x.strip()
    if x == ',' or x == ')' or x== '(' or x == ';' or x == '/' or x == '[' or x == ']':
        return False
    return True


def preprocess_note(this_note, suicide_asssments):
    #Function Definition: This function preprocesses the note to get rid of specific punctuations, the year, dates, and suicide assessments
    
    this_note = this_note.replace('-', ' ')
    this_note = this_note.replace('/', ' ')
    
    this_note = re.sub('[1-3][0-9]{3}', 'xYEARx', this_note)
    this_note = re.sub('((0?[13578]|10|12)(-|\/)(([1-9])|(0[1-9])|([12])([0-9]?)|(3[01]?))(-|\/)((19)([2-9])(\d{1})|(20)([01])(\d{1})|([8901])(\d{1}))|(0?[2469]|11)(-|\/)(([1-9])|(0[1-9])|([12])([0-9]?)|(3[0]?))(-|\/)((19)([2-9])(\d{1})|(20)([01])(\d{1})|([8901])(\d{1})))$', 'xDATEx', this_note)
    this_note = re.sub('(0?[1-9]|[12][0-9]|3[01])/[12][0-9]|3[01]', 'xDATEx', this_note)
    
    for s in suicide_asssments:
        this_note = this_note.replace(s, '')

    return this_note

def substring_period(sub_array, values, idx):
    # Function Defintion: This function returns the substring inputted into the negex algorithm when the phrase sends with a period.
    #Steps:
    #1) Remove extraneous characters
    #2) Checks to make sure the string is greater than 0
    #3) Check to see whether the substring is long in length.
    #4) If so, we find the index of the SI term and select a short substring surrounding that term
    #5) Returns the substring
    
    sub_array = [sa for sa in sub_array if remove_this(sa)]
    
    if len(sub_array) > 0:
    
        suicidal_term_index = sub_array.index(values[idx])
    
    # if we have a very long sentence
        if len(sub_array) > 20:
            dist = suicidal_term_index - 10
            if dist < 0:
                max_dist = suicidal_term_index - 0
            else:
                max_dist = 10
            sub_array = sub_array[suicidal_term_index -max_dist: suicidal_term_index + 2]
            suicidal_term_index = sub_array.index(values[idx])

        substring = ' '.join(sub_array)

        return substring
    else:
        return ''

def SI_distance(sub_array, question, values, idx):
    #Function Definition: This function returns the distance between the suicidal ideation term and the sentence break to determine if the substring is natural or structured.
    #Steps:
    #1a) If the sentence break is a question mark, find the index of the question mark
    #1b) If the sentence break is a colon, find the index of the colon
    #2) Find the index of the suicidal ideation term
    #3) Return the distance between the break index and the suicidal ideation term
    
    if question == True:
        break_index = sub_array.index('?',1)
    else:
        break_index = sub_array.index(':',1)

    suicidal_term_index = sub_array.index(values[idx])
    distance = break_index - suicidal_term_index

    return distance


def natural_tagger(substring, SI_phrases, irules):
    #Function Definition: This function returns the negation flag for substrings written in natural language form.
    tagger = negTagger(sentence = substring, phrases = SI_phrases ,rules = irules, negP = False)
    if tagger.getNegationFlag() == "affirmed":
        return False
    else:
        return True

def structured_tagger(substring, SI_phrases, irules2):
    #Function Definition: This function returns the negation flag for substrings written in structured language form.
    tagger = negTagger(sentence = substring, phrases = SI_phrases ,rules = irules2, negP = False)
    if tagger.getNegationFlag() == "affirmed":
        return False
    else:
        return True


def find_all_indexes(input_str, search_str):
    l1 = []
    length = len(input_str)
    index = 0
    while index < length:
        i = input_str.find(search_str, index)
        if i == -1:
            return l1
        l1.append(i)
        index = i + 1
    return l1

def preprocess_note2(this_text):

    our_punct = '!"#$%&\'()*+,-/;<=>@[\\]^_`{|}~·'
    translator = str.maketrans(our_punct, ' '*len(our_punct))
    this_text = this_text.translate(translator)

    this_text = re.sub('[1-3][0-9]{3}', 'xYEARx', this_text)

    this_text = re.sub('((0?[13578]|10|12)(-|\/)(([1-9])|(0[1-9])|([12])([0-9]?)|(3[01]?))(-|\/)((19)([2-9])(\d{1})|(20)([01])(\d{1})|([8901])(\d{1}))|(0?[2469]|11)(-|\/)(([1-9])|(0[1-9])|([12])([0-9]?)|(3[0]?))(-|\/)((19)([2-9])(\d{1})|(20)([01])(\d{1})|([8901])(\d{1})))$', 'xDATEx', this_text)
    this_text = re.sub('(0?[1-9]|[12][0-9]|3[01])/[12][0-9]|3[01]', 'xDATEx', this_text)

    return this_text

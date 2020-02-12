import pyConTextNLP.pyConText as pyConText
import pyConTextNLP.itemData as itemData
import networkx as nx
from textblob import TextBlob
import pyConTextNLP.display.html as html
from IPython.display import display, HTML
from collections import Counter
import itertools
import pandas as pd

from argparse import ArgumentParser

import spacy
nlp = spacy.load('en_core_web_sm')

from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report


def getNegationValue(g, te):

    if g.isModifiedByCategory(te, "DEFINITE_NEGATED_EXISTENCE"):
        return 'Negated', te
    return 'Positive', te

def getExperiencerValue(g, te):
    if g.isModifiedByCategory(te, "experiencer"):
        return 'Other', te
    return 'Patient', te

def analyze_sentence(sentence, modifiers, targets, tagExperiencer=False):
  context = pyConText.ConTextDocument()
  markup = pyConText.ConTextMarkup()
  markup.setRawText(sentence)
  markup.markItems(modifiers, mode="modifier")
  markup.markItems(targets, mode="target")


  markup.pruneMarks()
  markup.dropMarks('Exclusion')
  markup.applyModifiers()

  markup.dropInactiveModifiers()
  markup.updateScopes()

  context.addMarkup(markup)
  g = context.getDocumentGraph()

  ma = g.getMarkedTargets()
 
  tst = []
  details = []
  found = {}
  for te in ma:
      #print ma
      tmp1, tmp2 = getNegationValue(g, te)
      if tagExperiencer:
          e1, e2 = getExperiencerValue(g, te)
          if e1 != 'Other':
              st.append(tmp1)
              details.append(tmp2)
              found[tmp2]=Counter(tmp1)
      else:
          tst.append(tmp1)
          details.append(tmp2)
          found[tmp2]=Counter(tmp1)

  return tst, details
  
  
def return_context_trigger(pred):
  
  tmp1 = []
  tmp2 = []
  for p in pred:
      if len(p[0]) > 0:
          tmp1.append(p[0][0])
      for tr in p[1]:
          trigger = str(tr)
          #print "Trigger: "+trigger
          trigger = trigger.split('phrase')[1]
          trigger = trigger[2:]
          trigger = trigger[0:-2]
          #print "Trigger2: "+trigger
          tmp2.append(trigger.strip())
  return tmp1, tmp2
  
  
  ## function to map list of pycontext predictions into one document label
def mapPyConTextLabelsToAnnotations(row):
  if 'Positive' in row:
      return 'document_level_suicidal'
  elif 'Negated' in row:
      return 'document_level_nonsuicidal'
  else:
      return 'non_relevant_document'

def mapPyConTextLabelsToAnnotationsMajority(row):
  c = Counter(row)
  nop = c['Positive']
  non = c['Negated']
  if nop==0 and non==0:
      return 'non_relevant_document'
  elif nop>=non:
      return 'document_level_suicidal'
  else:
      return 'document_level_nonsuicidal'


def generate_predictions(data_frame, modifiers, targets, note_c, majority):

    pycontext_label = [0 for i in range(len(data_frame))]
    for i in range(len(data_frame)):
        note = data_frame[note_c].iloc[i]
        doc = nlp(note)
        sents = [sent.string.strip() for sent in doc.sents]
        pred = [analyze_sentence(s, modifiers, targets, tagExperiencer=False) for s in sents]
        triggers, contexts = return_context_trigger(pred)
        if majority == 0:
            if mapPyConTextLabelsToAnnotations(triggers) == 'document_level_suicidal':
                pycontext_label[i] = 1
        else:
            if mapPyConTextLabelsToAnnotationsMajority(triggers) == 'document_level_suicidal':
                    pycontext_label[i] = 1
    
    data_frame['pycontext_label'] = pd.Series(pycontext_label, index = data_frame.index)
    return data_frame
            

#Read in the arguments from the script
parser = ArgumentParser()
parser.add_argument("-d", dest = "data_path", required = True, help = "data path to read in")
parser.add_argument("-nc", dest = "note_text_column", required = True, help = "name of note text column")
parser.add_argument("-m", dest = "majority", required = False, help = "majority rule")
parser.add_argument("-s", dest = "save_path", required = True, help = "data path to save to")
parser.add_argument("-a", dest = "accuracy_flag", required = False, help = "print accuracy")
parser.add_argument("-tc", dest = "truth_column", required = False, help = "name of true column")


args = parser.parse_args()
data_p = args.data_path
note_c = args.note_text_column
save_p = args.save_path
accuracy_f = int(args.accuracy_flag)
truth_c = args.truth_column
majority = int(args.majority)

#Read in the data
df = pd.read_excel(data_p)

#Read in the modifiers and the targets
modifiers = itemData.get_items('https://raw.githubusercontent.com/wcmc-research-informatics/SI_Ideation/master/pycontext/amia_2017.yml')
targets = itemData.get_items('https://raw.githubusercontent.com/wcmc-research-informatics/SI_Ideation/master/pycontext/targets.yml')


df = generate_predictions(df, modifiers, targets, note_c, majority)

#print the accuracy score of the predictions - if test
if accuracy_f == 1:
    print (accuracy_score(df[truth_c], df['pycontext_label']))
    print (classification_report(df[truth_c], df['pycontext_label']))
    
#save the predictions to an excel file
df.to_excel(save_p, index = False)







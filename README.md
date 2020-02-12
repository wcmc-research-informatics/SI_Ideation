# Suicidal (SI) Ideation Detection
This repository maintains the code for detection of suicidal ideation (SI) in clinical notes. 

**Setting up the virtual environment:**

1. Clone/download repository to your local machine 
2. cd (change directory) to location of cloned repository (ex. ```cd Users/.../SI_IDEATION_REPO``` )
3. Run the command ```python3 -m venv SI_env```
3. Run the command ```source SI_env/bin/activate``` in terminal 
4. Run the command ```pip install -r rq.txt``` in terminal. This will install the necessary packages to run the scripts
5. Run the command ```deactivate``` in terminal. 

**Running the WCM script:** 
1. Enter the virtual environment with the following command: ```source SI_env/bin/activate```
2. Run the command: ```python rb_script.py``` with the following arguments:
  - Name of excel file to read in: ```-d "datapath.xlsx" ```
  - Name of note text column: ```-nc "note_text"```
  - Name of excel file to save to: ```-s "savepath.xlsx" ```
  - Optional: print accuracy and classification report (yes): ```-a 1 ```
  - Optional: truth column: ```-tc "SI Label"```
  
  Example Command: ```python rb_script.py -d "datapath.xlsx" -nc "note_text" -s "save_path.xlsx" -a 1 -tc "SI Label"```

**Important Information about the WCM Script:**
- Additional suicidal ideation keywords can be added to the SI_phrases.txt file in the SI_Files folder
- Suicidal ideation asssessments to be ignored can be added to the SI_assessments.txt file in the SI_Files folder
- Additional negation triggers for natural sentence forms can be added to the natural_rules.txt file in the NegexRules folder 
- Additional negation triggers for structured sentence forms can be added to the structured_rules.txt file in the NegexRules folder

**Running the KCL Script:**
1. Enter the virtual environment with the following command: ```source SI_env/bin/activate```
2. Install a couple of new libraries in the virtual environment with the following command: ```pip install -r rq.txt```
3. Install the spacy "english" library with the following command: ```pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.0/en_core_web_sm-2.2.0.tar.gz```
4. The updated version of python requires one change to the PyConTextNLP package. Within the ConTextMarkup.py file, we need to comment out line 489. You should be able to find this file within SI_Env/python3.7/pyConTextNLP/... Without this comment, you will get the following error: AttributeError: 'dict_keyiterator' object has no attribute 'sort'
5. Run the command : ```python pycontext_script.py``` with the following arguments:
  - Name of excel file to read in: ```-d "datapath.xlsx" ```
  - Name of note text column: ```-nc "note_text"```
  - Name of excel file to save to: ```-s "savepath.xlsx" ```
  - Use the majority rule for classification (yes): ```-m 1 ```
  - Optional: print accuracy and classification report (yes): ```-a 1 ```
  - Optional: truth column: ```-tc "SI Label"```

Example Command: ```python pycontext_script.py -d "datapath.xlsx" -nc "note_text" -s "save_path.xlsx" -m 0 -a 1 -tc "SI Label"```

**Important Information about the KCL Script:**
- This script currently uses the targets from the target.csv file in the lexicons folder of [this github page](https://github.com/KCL-Health-NLP/camhs_pycontext_adaptation)
- This script currently uses the modifiers from the AMIA2017.csv file in the lexicons folder of [this github page](https://github.com/KCL-Health-NLP/camhs_pycontext_adaptation)

**Citations:**

Negex code was downloaded from the following repository with credit to Peter Kang: https://github.com/mongoose54/negex/tree/master/negex.python. The code was downloaded and altered for the purposes of our classification problem. 

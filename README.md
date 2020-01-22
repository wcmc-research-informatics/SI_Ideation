# SI_Ideation
This repository maintains the code for detection of suicidal ideation (SI) in clinical notes. 

**Setting up the virtual environment:**

1. Clone/download repository to your local machine 
2. cd (change directory) to location of cloned repository (ex. ```cd Users/.../SI_IDEATION_REPO``` )
3. Run the command ```source SI_env/bin/activate``` in terminal 
4. Run the command ```pip install -r rq.txt``` in terminal. This will install the necessary packages to run the scripts
5. Run the command ```deactivate``` in terminal. 


**Running the script:** 
1. Enter the virtual environment with the following command: ```source SI_env/bin/activate```
2. Run the command: ```python rb_script.py``` with the following arguments:
  - Nath of excel file to read in: ```-d "datapath.xlsx" ```
  - Name of note text column: ```-nc "note_text"```
  - Name of excel file to save to: ```-s "savepath.xlsx" ```
  - Optional: print accuracy and classification report (yes): ```-a 1 ```
  - Optional: truth column: ```-tc "SI Label"```
  
  Example Command: ```python rb_script.py -d "datapath.xlsx" -nc "note_text" -s "save_path.xlsx" -a 1 -tc "SI Label"```




**Citations:**

Negex code was downloaded from the following repository with credit to Peter Kang: https://github.com/mongoose54/negex/tree/master/negex.python. The code was downloaded and altered for the purposes of our classification problem. 

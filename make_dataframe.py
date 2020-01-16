# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 11:16:21 2020

@author: jacqu


Gather DUDE molecules in a dataframe with SMILES for docking
"""

import pandas as pd 
import numpy as np

import os 


TARGET = 'esr1'
dud_repo = 'C:/Users/jacqu/Documents/mol2_resource/dud/all'
os.chdir(dud_repo)


for target_folder in os.listdir(dud_repo):
    if(target_folder==TARGET):
        smiles, active, decoy = [], [], []
        
        with open(f'{target_folder}/actives_final.ism', 'r') as f : 
            actives = f.readlines()
            for l in actives :
                s=l.split(' ')[0]
                if('9' in s or 'p' in s or ' ' in s or '.' in s or len(s)>150):
                    next
                else:
                    smiles.append(s)
                    active.append(1)
                    decoy.append(0)
            
    
        with open(f'{target_folder}/decoys_final.ism', 'r') as f : 
            dec = f.readlines()
            for l in dec :
                s=l.split(' ')[0]
                if('9' in s or 'p' in s or ' ' in s or '.' in s or len(s)>150):
                    next
                else:
                    smiles.append(s)
                    active.append(0)
                    decoy.append(1)
   
         
df = pd.DataFrame.from_dict({'can':smiles, 'active':active, 'decoy':decoy})

df['other']=0

df.to_csv('C:/Users/jacqu/Documents/GitHub/vina_docking/esr1_dude.csv')
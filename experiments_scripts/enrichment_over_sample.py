# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 09:37:28 2020

@author: jacqu

Compare results for different exhaustivenesses, on 100 actives and 100 decoys
"""

import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv('../data/aa2ar_dude_scored.csv')

actives = df[df['active']==1]
decoys = df[df['decoy']==1]
na, nd, ntot = actives.shape[0], decoys.shape[0] , df.shape[0]

# Enrichment and separate distributions 
plt.figure()
sns.distplot(actives['score'], label = 'actives', bins=20)
sns.distplot(decoys['score'], label = 'decoys', bins=20)
plt.xlabel('Energy (kcal/mol)')
plt.xlim(-12,-4)
plt.legend()
plt.title(f'Distributions for sample with {na} actives and {nd} decoys')

# Difference in means : 
delta = np.mean(actives['score']) - np.mean(decoys['score'])
print('mean(a)-mean(d) = ',delta)


# Enrichment factor
df=df.sort_values('score')
percent = 5
pct = int(percent*df.shape[0]/100)
top_df = df.iloc[:pct]

# ef = pct actives in top k% divided by pct actives in the whole dataset 
ef = (top_df[top_df['active']==1].shape[0]/pct) / (na/ntot)
print(f'enrichment at {percent}% over {df.shape[0]} molecules : {ef} // exhaustiveness = 4')

# Time versus smiles length 
plt.figure()
lens = np.array([len(s) for s in df['can']])
sns.lineplot(x=lens, y=df['time'])
plt.ylabel('Time per molecule (s),')
plt.xlabel('length of SMILES string (number of chars)')
plt.title('Docking time vs molecule size // 24 cores, exhaustiveness = 4')
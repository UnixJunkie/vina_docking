# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 21:19:35 2020

@author: jacqu

File to run vina docking: 
    
    Directory with individual mol2 files 
    Path to receptor PDB file 
    exhaustiveness 
    Suffix for scores file output 

"""

import sys
import subprocess
import os 
import argparse
from time import time
import numpy as np
  
def cline():
    # Parses arguments and calls main function with these args
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-d", "--mols_dir", default='data/decoys_split', help="directory with mol2 files")
    parser.add_argument("-r", "--receptor_file", default='data/receptor.pdb', help="path to receptor pdb")
    parser.add_argument("-e", "--ex", default=8, help="exhaustiveness parameter for vina")
    parser.add_argument("-o", "--output_suffix", default='', help="Suffix for output scores files")
    args = parser.parse_args()
    
    main(args)
    
def main(args):
    # Runs the docking process with the args provided
    
    # target to pdbqt 
    subprocess.run(['python3','pdb_select.py',f'{args.receptor_file}','! hydro', f'{args.receptor_file}'])
    subprocess.run(['/home/mcb/users/jboitr/mgltools_x86_64Linux2_1.5.6/bin/pythonsh', 'prepare_receptor4.py',
                    f'-r /home/mcb/users/jboitr/vina_docking/{args.receptor_file}','-o tmp/receptor.pdbqt', '-A hydrogens'])
    
    # Iterate on molecules
    scores, times = [], []
    mols_list = os.listdir(args.mols_dir)
    mols_list=mols_list[:100] # Number of molecules to dock
    for file in mols_list:
        # ligand to pdbqt 
        subprocess.run(['/home/mcb/users/jboitr/mgltools_x86_64Linux2_1.5.6/bin/pythonsh', 'prepare_ligand4.py',
                        f'-l /home/mcb/users/jboitr/vina_docking/{args.mols_dir}/{file}', '-o tmp/ligand.pdbqt', '-A hydrogens'])
        
        # RUN DOCKING 
        start=time()
        subprocess.run(['/home/mcb/users/jboitr/local/autodock_vina_1_1_2_linux_x86/bin/vina',
                        '--config', '/home/mcb/users/jboitr/vina_docking/data/conf.txt','--exhaustiveness', f'{args.ex}'])
        end = time()
        print("Docking time :", end-start)
        times.append(end-start)
        
        #reading output tmp/ligand_out.pdbqt
        with open('tmp/ligand_out.pdbqt','r') as f :
            lines = f.readlines()
            sline = lines[1]
            values = sline.split('      ')
            scores.append(float(values[1]))
    
    if(args.output_suffix!=''):
        np.save(f'exp/out_scores_e{args.ex}_{args.output_suffix}',scores)
        np.save(f'exp/out_times_e{args.ex}_{args.output_suffix}',times)
    else:
        np.save(f'exp/out_scores_e{args.ex}',scores)
        np.save(f'exp/out_times_e{args.ex}',times)
    
if(__name__=='__main__'):
    cline()
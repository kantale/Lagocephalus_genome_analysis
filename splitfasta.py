
# coding: utf-8

#!/usr/bin/env python3 
# Created by: Teo Danis
# Descript: This script splits a fasta sequence into several similarly-sized pieces and creates fasta files with linear sequenses
#  
# Usage: python3 splitfasta.py --fasta <genome fasta file> --pieces <number of pieces> --out <output directory>
# Example: python3 splitfasta.py --fasta myseqs.fasta  --pieces 5 --out my_out_dir
#----------------------------------------------------------------------------------------
#===========================================================================================================


import argparse
import numpy as np
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
         prog='splitfasta.py',
         usage='''python3 splitfasta.py --fasta <genome fasta file>  --pieces <number of pieces> --out <output directory>''',
         description='''This program splits a fasta sequence into several similarly-sized pieces.''',
         epilog='''It requires numpy''')
    parser.add_argument('-f', '--fasta', type=str, help='The name of the fasta file', required=True)
    parser.add_argument('-p', '--pieces', type=int, help='number of pieces', required=True)
    parser.add_argument('-o', '--out', type=str, help='path of output files', required=False)
    args = parser.parse_args()
    out = args.out
    file1=args.fasta
    pieces=args.pieces
    

def linear_plus_split_fasta():
    
    with open(file1, "r+") as f:

        cur_name = ""
        cur_seq = ''
        mega_list = []
        first_seq = True  # special variable to handle the first sequence
        
        for line in f:
            line = line.strip()

            if line.startswith(">"): # and "chromosome" in line: # we reached a new fasta sequence


                    if first_seq:          # if first sequence, record name and continue
                        cur_name = line
                        first_seq = False  # mark that we are done with the first sequence

                    else:                 # we are past the first sequence

                        yield cur_name, cur_seq

                        cur_name= line  # record the name of the new sequence
                        cur_seq= "" # reset cur_len
            else:
                cur_seq += line

        yield cur_name, cur_seq
        
mega_list=list(linear_plus_split_fasta())
        
 
def write():       
        for i in range(0, pieces):
            
            if out==None:

                new_file = "file" + str(i+1) + ".fa"

            else:
                if out[-1] == '/':
                    new_file = out + "file" + str(i+1) + ".fa"
                else:
                    new_file = out + "/file" + str(i+1) + ".fa"
            
            
            new_file = "file" + str(i+1) + ".fa"

            l = list(map(lambda x : x[0] + '\n' + x[1] + '\n' , mega_list[i::pieces]))
    
            with open(new_file, "wt") as p:
                for chunk in l:
                    p.write(chunk)

           
            
write()
   


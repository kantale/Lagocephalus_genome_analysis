#!/usr/bin/env python
# coding: utf-8

# In[ ]:



#!/usr/bin/env python3 
# Created by: Teo Danis
# Descript: This script parses busco full tsv info file and reports summary statistics from busco tsv file and genome fasta file
# 		and creates summary statistics file which includes imformation for both categories of genes which are hitted or not from Buscos.
# Usage: python3 busco_stats.py --fasta <genome fasta file> --input <the busco tsv file> --out <output directory>
# Example: python3 busco_stats.py --fasta myseqs.fasta  --input my_busco_tsv --out my_out_dir
#----------------------------------------------------------------------------------------
#===========================================================================================================

import re
from collections import defaultdict
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
         prog=' busco_stats.py ',
         usage='''python3 busco_stats.py --fasta <genome fasta file> --input <the busco tsv file> --out <output directory>''',
         description='''This script parses busco full tsv info file and reports summary statistics from busco tsv file and genome fasta file.''')
    
    parser.add_argument('-f', '--fasta', type=str, help='The name of the fasta file', required=True)
    parser.add_argument('-i', '--input', type=str, help='the busco tsv file', required=True)
    parser.add_argument('-o', '--out', type=str, help='path of output files', required=False)
    args = parser.parse_args()
    out = args.out
    file1=args.fasta
    file2=args.input
   
    



def count_lengths_Lagocephalus():
    with open('pilon_afteRaconMed.fa', "r+") as f2:
        
        dic = {}
        
        for line in f2:
            line = line.strip()
            if line.startswith(">"):

                header = line[1:]
                
                dic[header] = 0
 
            else:
                dic[header] += len(line)
                
                
        total_genome_size = sum(dic.values())

        sorted_reversed = dict(sorted(dic.items(), key=lambda item: item[1], reverse =True))
        #total = sum(sorted_reversed.values())

        return sorted_reversed, total_genome_size


dict_contig_len, total_bases = count_lengths_Lagocephalus()

def parsing_busco_tsv():
    
    with open('full_table.tsv', "r+") as tab_file, open('busco_summary_statistics.tsv', 'wt') as busco:
        
        missing_list = []

  
        con_regions = defaultdict(list)
        buscos = []
        for line in tab_file:
            
            line = line.strip()
            
            
            if line.startswith("#"):
            
                buscos.append(re.findall(r'number of species:(.*),', line))

                continue
                    
            if "Missing" in line:
                missing_list.append(line)
                
            else: 
                contig_name = line.split()[2]

                start = line.split()[3]
                end = line.split()[4]
                con_regions[contig_name].append((int(start), int(end)))
     
        contigs_lengths_busco_genes = {k: dict([("genes", len(v)), ("length", length)]) for k,v in con_regions.items() for con, length in dict_contig_len.items() if k in con}

        sorted_by_genes = sorted(contigs_lengths_busco_genes.items(), key=lambda item: item[1]["genes"], reverse = True)
        sorted_by_length = sorted(contigs_lengths_busco_genes.items(), key=lambda item: item[1]["length"], reverse = True)
        
        not_included = {contig:int(length) for contig, length in dict_contig_len.items() if contig not in con_regions.keys()}
        sorted_not_included =dict(sorted(not_included.items(),key=lambda item: item[1], reverse = True ))
        
        gs = 0
        counter = 0
        
        busco.write('#contigs'+'\t'+'length (Mbases)'+'\t'+'hitted_genes'+'\n')

        for ks, vs in contigs_lengths_busco_genes.items():

            busco.write(ks +"\t"+"with total length"+ "\t" +str(vs['length']/10**6)+ " " + "Mb" + "\t" + "genes" + "\t" + str(vs['genes'])+ '\n')
            counter += 1
            gs += int(vs['genes'])
            
        busco.write('\n'+"Total genes" + str(buscos) + '\n')
        busco.write("Hitted genes" + " " + str(gs) + '\n')
        for buscos in buscos:
            if buscos: ## I mean if the list is not empty because re.findall returns null if pattern does not match somewhere
                busco.write("Not found" + " " + str(int(''.join(buscos))-gs) + '\n')
        busco.write(f'Total contigs {len(list(dict_contig_len.keys()))}' + '\n')
        busco.write("Number of Contigs with almost one Busco hit" + ' ' + f'{counter}')
        busco.write(2*'\n')
        
        busco.write(2*"\n"+"The longest contig is" + "\t" + str(list(sorted_by_length)[0][0]) +"\t"+ "with length" + "\t" +                     str(list(sorted_by_length)[0][1]['length']/10**6)+ " " + "Mb"+ "\t"+ "which hitted" + "\t" + str(list(sorted_by_length)[0][1]['genes'])+" " + "genes"+ "\n" )
        busco.write(2*"\n"+"The contig" + "\t" + str(list(sorted_by_genes)[0][0])+"\t"+ "with length" + "\t" +                     str(list(sorted_by_genes)[0][1]['length']/10**6)+ " " + "Mb"+ "\t" + "\t"+ "which hitted" + "\t" + str(list(sorted_by_genes)[0][1]['genes'])+" " + "genes"+ "\n" )
        busco.write(2*"\n"+80*'#'+ '\n')
        busco.write("\n"+"Next Lagocephalus contigs are not match in BUSCOS of actinopterygii_orthodb10" + "\n")
        busco.write("\n"+80*'#'+ 2*'\n')
        
        for contigs, lens in sorted_not_included.items():

            busco.write(contigs +"\t"+"with total length"+ "\t" +str(lens/10**6)+ " " + "Mb" + '\n')
        
        print("Busco tsv file parsing completed successfully.")
parsing_busco_tsv()


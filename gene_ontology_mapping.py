#!/usr/bin/env python
# coding: utf-8

# In[ ]:
# created by Tdanis

######################
###   GO mapping   ###
######################

import urllib.parse
import urllib.request
import io
from bioservices import UniProt
import pandas as pd
import progressbar



df = pd.read_table('mega_blast.txt', header=None)   #### imput blast file

default_outfmt6_cols = 'qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore'.strip().split(' ')
df.columns = default_outfmt6_cols ## assign columns

df_new = df.loc[df['qseqid'] != df['qseqid'].shift()] ### keep the best hit for every prot

service = UniProt()


ls = list(df_new['sseqid'])  ### list the final ids

e = "id,organism,pathway,go(biological process), go(molecular function), go(cellular component)" ###retrieve the info that you want

bar = progressbar.ProgressBar(maxval=len(ls),widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

result = ''

bar.start()

for i, query in enumerate(ls):
    
    
    bar.update(i+1)
    if i % 1000 == 0: print(i)
    result += service.search(query, frmt="tab", columns=e)
    
bar.finish()

new_df2 = pd.read_table(io.StringIO(result)) ### load results into a dataframe


final_df = new_df2[new_df2.Entry != 'Entry'] #### remove duplicate header bars

with open('GO.txt', 'wt') as txt_f:
    txt_f.write(final_df.to_csv(sep='\t', index = False, header=True)) ### export to csv format

# final_df


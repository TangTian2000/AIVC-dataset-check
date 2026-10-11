#!/usr/bin/env python3
"""Export a scientific design figure; does not display expression or cell counts."""
from pathlib import Path
import os
os.environ.setdefault('MPLCONFIGDIR', '/tmp/aivc-matplotlib-cache')
os.environ.setdefault('XDG_CACHE_HOME', '/tmp/aivc-font-cache')
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
R=Path(__file__).resolve().parents[1]
d=pd.read_csv(R/'metadata/scplex_Supplementary_Table_3.txt',sep='\t')
meta=d[['plate_oligo','cell_type','replicate','time_point']].drop_duplicates()
meta['plate_number']=meta.plate_oligo.str.replace('plate','',regex=False).astype(int)
meta=meta.sort_values(['cell_type','time_point','replicate','plate_number'])
plate_order=meta.plate_oligo.tolist()
treat_order=['S0000']+sorted(set(d.treatment)-{'S0000'})
a=d.groupby(['plate_oligo','treatment']).size().unstack(fill_value=0).reindex(index=plate_order,columns=treat_order,fill_value=0)
fig,ax=plt.subplots(figsize=(16,13),layout='constrained')
im=ax.imshow(a.to_numpy(),aspect='auto',interpolation='none',vmin=0,vmax=int(a.to_numpy().max()),cmap='Blues')
labels=[f'{r.cell_type} / {r.time_point}h / {r.replicate} / P{r.plate_number}' for r in meta.itertuples()]
ax.set_yticks(np.arange(len(labels)),labels,fontsize=7)
xt=[0]+list(range(6,len(treat_order),10));ax.set_xticks(xt,[treat_order[i] for i in xt],rotation=90,fontsize=8)
ax.set_xlabel('Treatment catalogue ID (S0000 = vehicle); selected labels shown')
ax.set_ylabel('Culture-plate hash labels grouped by cell background, time and replicate')
ax.set_title('sciPlex3 author sample design: plate and treatment overlap\nCounts are designed samples, not cells; independent culture replication remains unverified',fontsize=12)
for i in range(1,len(meta)):
 prev=meta.iloc[i-1];cur=meta.iloc[i]
 if any(prev[k]!=cur[k] for k in ['cell_type','time_point','replicate']):ax.axhline(i-.5,color='gray',linewidth=.5)
c=fig.colorbar(im,ax=ax,shrink=.4,pad=.015);c.set_label('Number of design samples per plate / treatment');c.set_ticks(range(int(a.to_numpy().max())+1))
(R/'figures').mkdir(exist_ok=True)
fig.savefig(R/'figures/sciplex3_sample_design.png',dpi=180)
fig.savefig(R/'figures/sciplex3_sample_design.pdf')
print('Exported PNG/PDF sample-design heatmap; no expression/cell-count inference')

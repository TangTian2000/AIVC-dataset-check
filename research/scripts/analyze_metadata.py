#!/usr/bin/env python3
"""Audit real downloaded metadata, with explicit units and batch semantics.
Default: sciPlex3 sample-design tables, sciPlex2 sample sheet, MIX-seq experiment declarations.
Optional: --cell-csv FILE --schema JSON --output DIR (requires a reviewed schema).
Sample/experiment declarations are NEVER counted as cells. Expression is never read.
"""
import argparse, json, re
from pathlib import Path
import pandas as pd
R=Path(__file__).resolve().parents[1]

def write(df, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path,index=False)

def grouped(df, columns, unit):
    return df.groupby(columns,dropna=False,observed=True).size().reset_index(name=unit)

def audit_frame(df, out, batch, perturbation, strata, controls, unit, provenance, min_n=1, control_match_strata=None):
    required=[batch,perturbation]+strata
    if df[required].isna().any().any():
        raise ValueError('Missing batch/condition/context values; resolve explicitly before counting')
    df=df.copy()
    for c in required: df[c]=df[c].astype(str)
    controls=set(map(str,controls))
    df['_is_control']=df[perturbation].isin(controls)
    if not df['_is_control'].any(): raise ValueError('No exact control label found')
    out.mkdir(parents=True,exist_ok=True)
    write(grouped(df,[batch,perturbation],unit),out/f'batch_x_perturbation_{unit}.csv')
    write(grouped(df[df._is_control],[batch],unit),out/f'controls_by_batch_{unit}.csv')
    # Strata = biological background, dose, time and stimulus. Control dose is matched separately.
    strict=[perturbation]+strata
    totals=grouped(df,strict+[batch],unit)
    eligible=totals[totals[unit]>=min_n]
    coverage=eligible.groupby(strict,dropna=False,observed=True)[batch].nunique().reset_index(name='n_groups_with_min_n')
    write(coverage,out/f'condition_coverage_{unit}.csv')
    write(df.groupby(perturbation,observed=True)[batch].nunique().reset_index(name='n_groups'),out/f'perturbation_coverage_{unit}.csv')
    for col in strata:
        write(grouped(df,[batch,col],unit),out/f'batch_x_{col}_{unit}.csv')
    # For each condition, list training coverage after leaving out each group.
    control_strata=control_match_strata if control_match_strata is not None else [c for c in strata if c not in ['dose','dose_uM','dose_nM']]
    if not set(control_strata).issubset(strata): raise ValueError('Control matching columns must be among the declared strata')
    ct=grouped(df[df._is_control],[batch]+control_strata,unit)
    ck=ct.set_index([batch]+control_strata)[unit].to_dict()
    active=totals[~totals[perturbation].isin(controls)]
    strict_counts={}
    for _,row in active.iterrows():
        key=tuple(row[c] for c in strict)
        strict_counts.setdefault(key,{})[row[batch]]=int(row[unit])
    splits=[]
    for _,row in active.iterrows():
        key=tuple(row[c] for c in strict);held=row[batch]
        other={k:n for k,n in strict_counts[key].items() if k!=held and n>=min_n}
        ctrlkey=(held,)+tuple(row[c] for c in control_strata)
        # Pandas single-column set_index uses scalar keys.
        if not control_strata:ctrlkey=held
        heldctrl=int(ck.get(ctrlkey,0))
        training_controls=sum(int(ck.get((k,)+tuple(row[c] for c in control_strata) if control_strata else k,0)) for k in other)
        paired_training_groups=sum(int(ck.get((k,)+tuple(row[c] for c in control_strata) if control_strata else k,0))>=min_n for k in other)
        d={c:row[c] for c in strict};d.update(heldout_group=held,heldout_n=int(row[unit]),training_n_same_condition=sum(other.values()),training_groups_same_condition=len(other),heldout_matched_control_n=heldctrl,training_matched_control_n=training_controls,paired_training_groups=paired_training_groups)
        d['design_or_metadata_eligible']=bool(row[unit]>=min_n and other and heldctrl>=min_n and paired_training_groups>0)
        splits.append(d)
    split=pd.DataFrame(splits)
    write(split,out/f'leave_one_group_out_{unit}.csv')
    summary=dict(unit=unit,rows=len(df),batch_or_group_key=batch,groups=int(df[batch].nunique()),perturbation_labels=int(df[perturbation].nunique()),control_rows=int(df._is_control.sum()),strict_strata=strata,min_n=min_n,strict_conditions=len(coverage),strict_conditions_cross_groups=int((coverage.n_groups_with_min_n>=2).sum()),eligible_heldout_condition_groups=int(split.design_or_metadata_eligible.sum()),evaluated_heldout_condition_groups=len(split),provenance=provenance)
    (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
    return summary

def sciplex_design():
    p=R/'metadata/scplex_Supplementary_Table_3.txt';d=pd.read_csv(p,sep='\t',keep_default_na=False)
    assert not d.duplicated(['well_oligo','plate_oligo']).any(), 'Duplicate hash sample keys'
    original=pd.read_csv(R/'metadata/scplex_sciChem3_screen2_hashMeta_data.tsv',sep='\t',header=None,names=['well_oligo','plate_oligo','cell_type','replicate','time_point','drug_dose'],keep_default_na=False)
    assert len(original)==len(d)
    joined=d.merge(original,on=['well_oligo','plate_oligo'],validate='one_to_one',suffixes=('_table','_hash'))
    for c in ['cell_type','replicate','time_point','drug_dose']:
        assert joined[c+'_table'].astype(str).equals(joined[c+'_hash'].astype(str)),c+' mapping mismatch'
    # Dose values are retained as source values; unit requires paper confirmation.
    vehicle=d.vehicle.astype(str).str.lower().eq('true')
    assert set(d.loc[vehicle,'treatment'])=={'S0000'}
    assert vehicle.equals(d.treatment.eq('S0000'))
    ids=(R/'metadata/scplex_valid_cells.tsv').read_text().splitlines()
    assert len(ids)==len(set(ids)), 'Duplicate valid-cell IDs'
    out=R/'tables/sciplex3_design'
    write(grouped(d,['cell_type','replicate','time_point'],'n_design_samples'),out/'context_replicate_time.csv')
    write(d.groupby('plate_oligo').agg(n_design_samples=('treatment','size'),n_cell_backgrounds=('cell_type','nunique'),n_replicate_labels=('replicate','nunique'),n_timepoints=('time_point','nunique')).reset_index(),out/'plate_nesting.csv')
    summaries={}
    for key in ['plate_oligo','replicate']:
        summaries[key]=audit_frame(d,out/key,key,'treatment',['cell_type','dose','time_point'],['S0000'],'n_design_samples','Author Supplementary_Table_3 + hashMeta mapping; NOT cells. plate_oligo maps to culture_plate in Notebook1. Primary paper supports biological replicates and replicate culture plates; exact cell/library/run mapping pending.')
    result=dict(sample_rows=len(d),unique_cell_ids_without_annotations=len(ids),cell_ids_file_bytes=(R/'metadata/scplex_valid_cells.tsv').stat().st_size,cell_metadata_mapping_available=False,drug_labels_excluding_control=int(d.loc[d.treatment!='S0000','treatment'].nunique()),all_plates=int(d.plate_oligo.nunique()),timepoints=sorted(map(int,d.time_point.unique())),details=summaries)
    (out/'summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print('sciPlex3',json.dumps(result,ensure_ascii=False))
    s=pd.read_csv(R/'metadata/scplex_hashSampleSheet.txt',sep='\t',header=None,names=['encoded_sample','hash_oligo','sheet_column3','empty'],keep_default_na=False)
    pieces=s.encoded_sample.str.extract(r'^(?P<drug_label>[^_]+)_(?P<dose_source_value>[^_]+)_(?P<well_label>.+)$')
    assert not pieces.isna().any().any()
    s=pd.concat([s,pieces],axis=1)
    # The third column is deliberately NOT called replicate without decoding documentation.
    write(s,R/'metadata/derived/sciplex2_sample_sheet_parsed.csv')
    write(grouped(s,['drug_label','dose_source_value'],'n_design_samples'),R/'tables/sciplex2_design/drug_dose_samples.csv')
    (R/'tables/sciplex2_design/summary.json').write_text(json.dumps(dict(rows=len(s),drug_labels=sorted(s.drug_label.unique()),column3_unique=sorted(s.sheet_column3.unique().tolist()),note='Headerless source. Column3 semantics unverified; sample counts, not cells.'),ensure_ascii=False,indent=2))

def mixseq_design():
    text=(R/'sources/mixseq_expt_meta_data.R').read_text()
    decl,compare=text.split('sc_DE_meta <- list(',1)
    starts=list(re.finditer(r'^\s{2,4}([A-Za-z0-9_]+)\s*=\s*list\(',decl,re.M))
    result=[]
    for i,m in enumerate(starts):
        block=decl[m.end():starts[i+1].start() if i+1<len(starts) else len(decl)]
        batch=re.search(r"expt_batch\s*=\s*'([^']+)'",block)
        if batch is None: raise ValueError('Unmapped declaration '+m.group(1))
        name=m.group(1);time=re.search(r'_(\d+)hr_',name);treat=name.split('_')[0]
        if name=='tramet_tc_expt5':treat='Trametinib';time=None
        result.append(dict(declared_dataset=name,expt_batch=batch.group(1),treatment_source_label=treat,time_hr=time.group(1) if time else 'unknown_or_multi',is_vehicle_or_untreated=treat in ['DMSO','Untreated']))
    df=pd.DataFrame(result);write(df,R/'metadata/derived/mixseq_experiment_declarations.csv')
    out=R/'tables/mixseq_design'
    write(grouped(df,['expt_batch','treatment_source_label','time_hr'],'n_declared_datasets'),out/'experiment_treatment_time.csv')
    write(grouped(df[df.is_vehicle_or_untreated],['expt_batch','time_hr'],'n_declared_datasets'),out/'declared_controls.csv')
    write(df.groupby(['treatment_source_label','time_hr']).expt_batch.nunique().reset_index(name='n_expt_batches'),out/'treatment_time_coverage.csv')
    # Parse only top-level DE comparisons (indented four spaces). Do not execute R or access Taiga.
    starts=list(re.finditer(r'^    ([A-Za-z0-9_]+)\s*=\s*list\(',compare,re.M))
    comps=[]
    for i,m in enumerate(starts):
        b=compare[m.end():starts[i+1].start() if i+1<len(starts) else len(compare)]
        batch=re.search(r"expt_batch\s*=\s*'([^']+)'",b)
        drug=re.search(r"drug_name\s*=\s*'([^']+)'",b)
        refs=re.findall(r"(control(?:_\d)?|treat(?:_\d)?)\s*=\s*'([^']+)'",b)
        for role,dataset in refs:comps.append(dict(comparison=m.group(1),expt_batch=batch.group(1) if batch else 'unknown',drug=drug.group(1) if drug else 'genetic_or_unknown',role=role,declared_dataset=dataset))
    cmp=pd.DataFrame(comps);assert len(cmp)>0
    write(cmp,out/'comparison_control_links.csv')
    summary=dict(declared_datasets=len(df),expt_batches=sorted(df.expt_batch.unique()),treatment_labels=sorted(df.treatment_source_label.unique()),comparisons=len(starts),note='Author-coded experimental declarations only. expt_batch includes changed pools/protocols; independence and per-cell context coverage not established.')
    (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print('MIXseq',summary)

def audit_cells(args):
    schema=json.loads(Path(args.schema).read_text())
    if not schema.get('batch_semantics_evidence'):raise ValueError('Supply evidence of batch meaning; a column name is insufficient')
    df=pd.read_csv(args.cell_csv,sep=schema.get('separator',','),dtype=str,keep_default_na=False)
    keys=schema['cell_id_columns'];required=keys+[schema['batch'],schema['perturbation']]+schema['strata']
    if any(c not in df for c in required): raise ValueError('Missing schema columns')
    if df.duplicated(keys).any():raise ValueError('Cell IDs are not unique in declared namespace')
    if (df[required]=='').any().any():raise ValueError('Missing IDs, batch or stratum values')
    if 'control_match_columns' not in schema: raise ValueError('Declare matching context/time/donor columns for controls explicitly')
    source=dict(schema=schema,cell_csv=str(args.cell_csv),independent_batch_confirmed=schema.get('independent_batch_confirmed',False))
    audit_frame(df,Path(args.output),schema['batch'],schema['perturbation'],schema['strata'],schema['controls'],'n_cells',source,args.min_cells,schema['control_match_columns'])
    print('Real cell metadata audit completed; see summary.json for semantic limits.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cell-csv');p.add_argument('--schema');p.add_argument('--output');p.add_argument('--min-cells',type=int,default=30);a=p.parse_args()
    if a.cell_csv:
        if not a.schema or not a.output:p.error('--schema and --output required')
        audit_cells(a)
    else:sciplex_design();mixseq_design()

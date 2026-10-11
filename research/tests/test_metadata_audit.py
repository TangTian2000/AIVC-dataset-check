"""Synthetic semantic checks are not evidence about any real dataset."""
import importlib.util, tempfile, unittest
from pathlib import Path
import pandas as pd
P=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('analysis',P/'scripts/analyze_metadata.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class AuditChecks(unittest.TestCase):
    def run_frame(self, rows):
        columns=['batch','condition','cell_type','dose','time_point']
        frame=pd.DataFrame(rows,columns=columns)
        with tempfile.TemporaryDirectory() as directory:
            m.audit_frame(frame,Path(directory),'batch','condition',['cell_type','dose','time_point'],['control'],'n_cells','SYNTHETIC_TEST_ONLY',1,['cell_type','time_point'])
            return pd.read_csv(Path(directory)/'leave_one_group_out_n_cells.csv')
    def test_paired_controls_and_conditions(self):
        d=self.run_frame([['b1','drug','A',1,24],['b2','drug','A',1,24],['b1','control','A',0,24],['b2','control','A',0,24]])
        self.assertTrue(d.design_or_metadata_eligible.all())
        self.assertEqual(d.training_n_same_condition.tolist(),[1,1])
    def test_dose_confounding_is_not_seen_condition(self):
        d=self.run_frame([['b1','drug','A',1,24],['b2','drug','A',2,24],['b1','control','A',0,24],['b2','control','A',0,24]])
        self.assertFalse(d.design_or_metadata_eligible.any())
        self.assertEqual(d.training_n_same_condition.sum(),0)
    def test_wrong_background_controls_block_both_sides(self):
        d=self.run_frame([['b1','drug','A',1,24],['b2','drug','A',1,24],['b1','control','B',0,24],['b2','control','A',0,24]])
        self.assertFalse(d.design_or_metadata_eligible.any())
    def test_time_confounding_is_not_seen_condition(self):
        d=self.run_frame([['b1','drug','A',1,24],['b2','drug','A',1,72],['b1','control','A',0,24],['b2','control','A',0,72]])
        self.assertFalse(d.design_or_metadata_eligible.any())
    def test_missing_control_is_rejected(self):
        with self.assertRaises(ValueError):
            self.run_frame([['b1','drug','A',1,24]])
    def test_author_sample_tables_closed_form(self):
        d=pd.read_csv(P/'metadata/scplex_Supplementary_Table_3.txt',sep='\t')
        self.assertEqual(len(d),52*96)
        self.assertEqual((d.treatment=='S0000').sum(),52*2)
        n=188*4*3+47*4
        self.assertEqual((d.treatment!='S0000').sum(),2*n)
        self.assertEqual(d.loc[d.treatment!='S0000'].drop_duplicates(['treatment','cell_type','dose','time_point']).shape[0],n)
        self.assertEqual(d.groupby('plate_oligo').treatment.apply(lambda x:(x=='S0000').sum()).unique().tolist(),[2])
if __name__=='__main__':unittest.main()

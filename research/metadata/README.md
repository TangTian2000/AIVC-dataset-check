# 已下载元数据及统计边界

|文件|内容与单位|来源和大小|能回答/不能回答|
|---|---|---|---|
|scplex_Supplementary_Table_3.txt|4,992行处理样本；17字段|作者GitHub；966,644 bytes|样本层drug/dose/time/background/rep设计；不是细胞数|
|scplex_sciChem3_screen2_hashMeta_data.tsv|无表头6字段；4,992 hash样本|作者GitHub；195,743 bytes|与Supplementary Table 3逐键对应；不能分配valid cell IDs|
|scplex_valid_cells.tsv|649,340个唯一细胞ID；没有hash/处理列|作者GitHub；18,484,236 bytes|只证明该公开ID清单的规模；不能按条码后缀推断生物处理或独立技术batch|
|scplex_hashSampleSheet.txt|sciPlex2无表头192行sample sheet|作者GitHub；5,183 bytes|解析drug/dose/well；第3列语义未核实，不称replicate|
|derived/sciplex2_sample_sheet_parsed.csv|上表的保守解析|本轮脚本生成|保留原编码；不是cell obs|
|derived/mixseq_experiment_declarations.csv|30个作者声明实验数据集|从作者expt_meta_data.R解析|可定位条件/时间/作者expt_batch；不是细胞数|

来源URL、commit与SHA-256在 `../resources.json`。小元数据请求被拒绝的记录在 `../access_log.jsonl`；不能据拒绝判断文件不存在。

本轮未获得任何完整、带处理与batch的细胞级obs，因此没有生成真实batch×perturbation细胞数量表。设计输出在 `../tables/sciplex3_design` 与 `../tables/mixseq_design`，明确单位为`n_design_samples` / `n_declared_datasets`。未计算状态在 `../audits/availability.csv`，不是假零。

取得真实CSV/TSV细胞元数据后，先复制并填写schema_template.json：为batch提供原论文/作者实验表证据；ID命名空间需要唯一；strata保留供体/细胞背景、剂量、时间及必要刺激。control_match_columns明确对照应匹配的背景；对照dose=0时不应要求同药物dose。NTC、untreated、vehicle、positive control和未分配guide不能混为一类。

```bash
python research/scripts/analyze_metadata.py \
  --cell-csv /path/to/real_cell_metadata.csv \
  --schema /path/to/reviewed_schema.json \
  --output research/tables/DATASET_cell_audit \
  --min-cells 30
```

这个入口输出所需batch×扰动细胞数、每batch对照、跨batch扰动和严格条件覆盖、batch与各stratum交叉统计、逐留出组覆盖/对照匹配检查。30是可调整门槛，不是独立重复或功效保证。`independent_batch_confirmed=false`时，即使coverage通过，也不能称独立批次任务成立。本轮该入口仅用明确标为synthetic的语义测试验证；没有真实cell audit运行结果。

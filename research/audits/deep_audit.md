# 深入审计报告

日期：2026-10-11（UTC）（含新增原文核查）。先保存第一阶段总表，再深入核查；随后因State/Arc新证据补充Parse、Nadig、VCC。最终总表32个版本/子资源条目、28个候选家族。不是28个均已证明“常用”，也不是32个独立来源；缺少原研究身份核验的条目保留未知。第一阶段快照见 `tables/dataset_inventory_stage1.*`。

本轮统一深入核查10个候选：sciPlex3、Replogle K562、Replogle RPE1、MIX-seq、OP3、Frangieh、sci-Plex G×E、Kang、Norman、Parse。Jiang24、Tahoe、Nadig、VCC完成有来源的扩展筛选，未冒充完成细胞级深审计。

**结论：sciPlex3设计层面最有希望；MIX-seq与OP3值得优先补齐元数据。当前没有一个候选已完成全部细胞级覆盖和独立技术批次证明，不能宣称主研究测试任务已可用。** 未检验任何表达矩阵的真实批次效应强度。

证据标签：**[文]** 原作者代码/说明明确记录；原论文全文若未访问会注明。**[算]** 本轮从下载的真实元数据/设计表计算，明确单位。**[二]** 模型/benchmark/整合资源记录，不能替代原实验说明。**[推]** 有条件推测。**[未知]** 未能核实。字段名或条形码后缀不构成独立技术批次证据。

## 统一判断标准

必须先给实验单元建立层级：独立培养/处理重复 → 处理板/孔 → 样本pool/hash → 建库/GEM group → 测序run/lane。关系未证实就保持未知；重复给同一library测序、同一pool拆多个GEM、同一板多孔都不能自动视为独立培养重复。

纯技术批次外推的条件单元为 `扰动（可含guide身份）×剂量×时间×细胞背景×必要刺激背景`；原代数据还要保留供体。先在背景内判断跨batch覆盖，再单独研究跨供体/细胞系外推。每一留出条件都需至少一个训练批次包含相同条件及其匹配对照，测试批次也需有匹配对照。细胞≥30只是后续脚本的可调工程门槛，不是足够实验重复或统计功效的保证。

两个技术层级要分别测试，不能混为一个结果：同一培养pool跨library/GEM评估较浅的建库泛化；跨独立培养/处理重复评估较深的实验泛化。若library完全嵌套在treatment，缺少跨library共同条件，无法识别该层级的批次校正效果。

## 1. sciPlex3（Srivatsan2020家族）

[文] 原作者Notebook1由 `top_oligo_P` 生成 `culture_plate`；`well_oligo + plate_oligo` 经hash表关联细胞背景、replicate、time、drug-dose。RT、ligation、PCR plate/well另有代码字段，分别是组合索引步骤，不能当培养批次互换。它使用sci-RNA-seq，不套用10x GEM group定义。见 E08 [sci-Plex原作者：hash、culture/RT/ligation/PCR映射](https://raw.githubusercontent.com/cole-trapnell-lab/sci-plex/079639c50811dd43a206a779ab2f0199a147c98f/large_screen/Notebook1_preprocess_data.R#L41)、E09 [sci-Plex原作者Supplementary Table 3（样本表）](https://raw.githubusercontent.com/cole-trapnell-lab/sci-plex/079639c50811dd43a206a779ab2f0199a147c98f/large_screen/bin/Supplementary_Table_3.txt#L1)。

[算] 作者Supplementary Table 3有 **4,992个唯一hash样本键、52个plate_oligo、rep1/rep2两个标签、188种药+S0000 vehicle**。两个作者样本表的6个共同字段逐键完全相符，重复键为0。每个plate有96个设计样本、2个vehicle样本；每plate只对应一个cell_type、一个replicate和一个time_point，三个因素均嵌套在plate。

[算] 24h：A549/K562/MCF7各188药×4剂量×2rep。72h：仅A549，47药×4剂量×2rep。编码dose为10/100/1000/10000，vehicle归零；原文第2页已目视核实为10/100 nM、1/10 µM。处理样本 **4,888**，vehicle样本 **104**。严格条件标签含对照共2,448，均覆盖两rep及两plate标签；在设计表单位下，4,888个“留出组×非对照条件”均具有另一组同条件与背景/时间匹配对照。

这不意味着每种药覆盖所有plate。不同plate承载不同药物子集，plate与面板部分混杂；只有重叠条件子集适合测试。72h不是三细胞系共享的独立技术batch，它是仅A549的不同生物条件。要保留time和cell_type，不能直接整合成同批次分布。

[算] `valid_cells.tsv`有 **649,340个唯一细胞ID**（18,484,236 bytes）。该文件只有ID，没有细胞到hash/replicate/培养板/处理的映射。这一枚举不是重新验证h5ad矩阵行数，也不能把649,340均分到4,992个样本。完整cell obs仍未取得。因此 **真实batch×perturbation细胞数、每batch对照细胞数、QC后跨batch覆盖、每条件可训练细胞数未计算**。

[文] 原文第2页明确重复培养板和孔位随机化，第4页Fig.3A明确biological replicate，已支持生物学重复设计。见 E32 [sciPlex原文 PDF pp2,4,6](https://raw.githubusercontent.com/cole-trapnell-lab/cole-trapnell-lab.github.io/a7ead73c4da7190d05b4928ace5b67d457329114/pdfs/papers/srivatsan_mcfaline_ramani_sci-plex_Science_2019.pdf)。[推] 固定背景、剂量和时间留出重复很有希望；仍需逐细胞对应及培养日期/lot、索引板、建库、测序关系，不能把52个板当52次独立实验。

[未知] culture_plate与独立培养日期/lot、建库/测序run的映射；每rep/plate过滤后的细胞数；真实批次强度。下一步下载GSM4150378完整cell metadata或请作者导出`colData(cds)`，保留hash与所有索引步骤。无需先下载大表达矩阵。

已生成 [设计统计目录](../tables/sciplex3_design/summary.json)：`batch_x_perturbation_n_design_samples.csv`、`controls_by_batch_n_design_samples.csv`、`condition_coverage_n_design_samples.csv`、按背景/剂量/时间交叉表、`leave_one_group_out_n_design_samples.csv`。文件名明确为样本数。

同家族sciPlex2的headerless hashSampleSheet有192行。本轮按无表头读取并解析drug/dose/well；第3列语义未确认，没有称其为replicate。pertpy文档称4药×7剂量×triplicate、24h；样本表含其他标记，须核实样本设计，不能直接推断全部192行都是正式药物处理。sciPlex4是另一HDACi rescue实验，不等于CPA新组合药物GSE206741。

## 2. Replogle K562：GWPS与essential须分开

[文/二] 原作者原文件名在整合脚本中分别为`K562_gwps_raw_singlecell_01.h5ad`、`K562_essential_raw_singlecell_01.h5ad`。同研究但面板/时间不同，不能当相同扰动跨batch独立重复。`gene`用于扰动、`sgID_AB`改名guide_id、`gem_group`改名batch，non-targeting是对照。见 E12 [Replogle整合脚本：gem_group重命名batch](https://raw.githubusercontent.com/sanderlab/scPerturb/b69f72a070a92bcbaf41e7f9897b11598109ab48/dataset_processing/scripts/ReplogleWeissman2022.py#L49)。

[二] gem_group→batch只是整合约定，不能证明独立培养/处理，不能自动当测序批次。GEM/library/culture/run是否一对一或嵌套均未知。原细胞背景是K562，要与RPE1和后续Jurkat/HepG2区别。

[二] 旧目录GWPS有9,867、essential有2,058扰动标签（含对照），不是已读原obs基因数、guide数或本轮细胞数。GWPS文档day8；essential docstring开头day7而内文day6/day7混用，原文/作者表须解决这一时间冲突。`scPerturb`旧目录的提交年不应当出版年。见 E06 [pertpy数据文档与loader（整合方）](https://raw.githubusercontent.com/scverse/pertpy/a4c30738468f8cb6bed677efb9331a9e35a168bd/src/pertpy/data/_datasets.py#L29)、E07 [scPerturb旧版目录（140922，非原论文）](https://raw.githubusercontent.com/sanderlab/scPerturb/b69f72a070a92bcbaf41e7f9897b11598109ab48/metadata/scperturb_dataset_info_140922.csv#L1)。

[二] GEARS README仅明确v0.1.1支持K562 essential/RPE1 loader；“支持下载”不证明原GEARS论文评测采用。State README称Replogle-Nadig，其`replogle_nogwps_v2`合并目录还含Jurkat/HepG2，不能把该训练目录的结果归到2022 GWPS。见 E01 [GEARS作者README / Core API](https://raw.githubusercontent.com/snap-stanford/GEARS/f374e43e197b295016d80395d7a54ddb81cc6769/README.md#L35)、E24 [State原作者论文与训练教程](https://raw.githubusercontent.com/arcinstitute/state/9bbfe78a434a55205e4de834e1ea99f85f7a3add/README.md#L14)、E31 [State Replogle合并目录/训练配置](https://raw.githubusercontent.com/arcinstitute/state/9bbfe78a434a55205e4de834e1ea99f85f7a3add/state_preprint_toml_files/replogle_tomls/k562.toml#L2)。

[二] 下游notebook按min_counts和equal_subsampling筛选、保存counts再normalize/log1p，这会改变条件与批次覆盖。不能用标准化均衡子集替代原始批次结构和QC指标。见 E29 [Replogle下游过滤notebook / Cell5](https://raw.githubusercontent.com/sanderlab/scPerturb/b69f72a070a92bcbaf41e7f9897b11598109ab48/revision/notebooks/replogle_handling.ipynb)。

[未知] 独立培养重复、plate/GEM/library/测序关系；同一gene/guide跨GEM覆盖；每GEM non-targeting数；技术批次留出能否保留相同时间、面板和对照。原门户受代理拒绝。当前推荐 **信息不足，优先核实**；不默认不适合，也不默认满足目标。

## 3. Replogle RPE1

[二] 同2022家族的hTERT-RPE1 essential screen，整合脚本读`rpe1_raw_singlecell_01.h5ad`；基于CRISPRi，non-targeting对照。旧目录2,394标签含对照，不是本轮obs枚举。文档day7。

[二] 字段与K562一样存在gem_group→batch。K562/RPE1是生物背景与不同筛选，不能把两细胞系作为要消除的技术批次。应先在RPE1内部证明跨独立技术批次条件覆盖，再另设跨背景外推。

[未知] 所有培养/板/library/run的映射、跨GEM重复和匹配对照数量。尚不能判定“已见扰动、未见独立批次”可构建。原始h5ad可能包含obs，但没有验证独立小元数据下载；门户拒绝导致尺寸也未知。见 E12 [Replogle整合脚本：gem_group重命名batch](https://raw.githubusercontent.com/sanderlab/scPerturb/b69f72a070a92bcbaf41e7f9897b11598109ab48/dataset_processing/scripts/ReplogleWeissman2022.py#L49)、E06 [pertpy数据文档与loader（整合方）](https://raw.githubusercontent.com/scverse/pertpy/a4c30738468f8cb6bed677efb9331a9e35a168bd/src/pertpy/data/_datasets.py#L29)。

## 4. MIX-seq（McFarland2020）

[文] 原作者`expt_meta_data.R`明确`sc_expts`与`sc_DE_meta`，定义数据版本、`expt_batch`及treat/control对应。脚本用Taiga名称/版本管理，作者README说明Figshare公开副本与本地路径。这是实验级元数据，不是细胞数。见 E14 [MIX-seq原作者实验与对照映射](https://raw.githubusercontent.com/broadinstitute/mix_seq_ms/edcf2266fc8fd586a4d9ee2db027d142f8a27ba6/src/expt_meta_data.R#L2)。

[算] 本轮解析该文件 **30个声明数据集、5个实验标签：expt1/2/3/5/10、20个DE comparison**。只有这些在当前文件被核实，不声称覆盖全研究所有实验。固定24h时，Trametinib在expt1/expt3重复；两个实验均有6h/24h DMSO。expt10是另一药物面板，expt2是GPX4 guide等遗传处理，expt5是time course。这些不构成通用全药物×全实验笛卡尔积。

[文] 部分6h/24h比较同时借用两个时间的DMSO，`comparison_control_links.csv`保存作者实际选择；这不等于所有对照严格时间匹配。若研究时间保真，应改在元数据审计阶段筛选可匹配对照的条件，不能默默沿用混合时间的参照。

[推] Trametinib 24h跨expt1/expt3可做候选实验留出，但须筛选两实验共同细胞系/相同剂量，核实pool、培养条件及独立运行。expt_batch包含不同细胞系pool/协议，不能全部视为纯技术可消除因素。SNP分类细胞系是生物背景，必须保留。

[未知] 单细胞标签、各实验共同细胞系数量、剂量、QC后counts、独立培养/建库/测序映射。Figshare API访问失败；本轮未把Taiga内部链接当公开文件。只有 [实验级设计输出](../tables/mixseq_design/summary.json)，没有细胞级跨表。条件性优先候选。

## 5. Open Problems / NeurIPS 2023 PBMC（OP3）

[文] 作者README：144 compounds、24h、3 healthy donors；另有每供体baseline Multiome。这些donor是生物背景，baseline Multiome不是相同技术重复。scRNA schema明确`dose_uM,timepoint_hr,well,row,col,plate_name,hashtag_id,donor_id,sm_name,cell_type`，`layers[counts]`与原cell ID。见 E15 [Open Problems原作者README / design及cell schema](https://raw.githubusercontent.com/openproblems-bio/task_perturbation_prediction/626f94521fd236e6b79cc60696159172dd07d2bd/README.md#L101)。

[二] PerturBench curation明确GSE279945；DMSO为negative control，belinostat/dabrafenib是positive controls。它引用原文剂量：belinostat0.1µM、DMSO14.1µM、其他1µM；本轮没有原文/obs独立复核。标成control并不意味着都是未扰动细胞。见 E25 [PerturBench OP3 curation / Cells7,20,27](https://raw.githubusercontent.com/altoslabs/perturbench/c84038bc1ea409aa54f3832cfa6f34f5059adf0c/notebooks/neurips2025/data_curation/curate_op3.ipynb)。

[文] competition训练/测试常用DE结果；`de_train.uns[single_cell_obs]`官方描述为**训练集**细胞metadata，不能覆盖整个实验的private test/所有plate。PerturBench另用scRNA矩阵。比赛的细胞背景/药物split不是technical-batch split。

[推] 可先在每donor×cell_type×dose×24h内测试plate/library留出；需要每plate有DMSO、留出板药物在其他板仍存在。若plate完全由donor/药物面板决定，donor间“跨batch”会混入生物或干预变化。

[未知] plate→donor/well/pool/library/run嵌套、细胞数和跨板药物覆盖。处理h5ad HEAD被代理拒绝，尺寸未知。需官方导出全obs（包括control状态与split）或从完整metadata分片获得；不能只读训练DE文件声称全实验审计完成。条件性优先候选。

## 6. Frangieh Perturb-CITE-seq

[文] 原作者README公开SCP1064 UMI矩阵，raw reads指DUOS-000124；不能把受控raw sequencing与公开count matrix混称“raw全部公开”。原作者QC门槛<200 genes、>18% mitochondrial、genes<200 cells属于原流程记录，未在本轮复算。见 E13 [Frangieh原作者README / counts与raw数据访问](https://raw.githubusercontent.com/klarman-cell-observatory/Perturb-CITE-seq/c90d46f268ffb7b30e9b35fc23ddd0967feca42b/README.md#L9)。

[二] 研究包含遗传扰动与Control/Co-culture/IFNγ背景。benchmark将`perturbation_2`映射为`treatment`，并把`cell_type`统一成melanocyte；这可能省略患者模型的生物差异，需原obs的patient/model字段。benchmark设置`perturbation_type='CRISPRi'`，而原资源目录写CRISPR-Cas9。**机制注释不一致，不能未经原文核验按benchmark标签决定KO/i。** 见 E26 [PerturBench Frangieh curation / Cells4,6,8](https://raw.githubusercontent.com/altoslabs/perturbench/c84038bc1ea409aa54f3832cfa6f34f5059adf0c/notebooks/neurips2025/data_curation/curate_Frangieh21.ipynb)、E07 [scPerturb旧版目录（140922，非原论文）](https://raw.githubusercontent.com/sanderlab/scPerturb/b69f72a070a92bcbaf41e7f9897b11598109ab48/metadata/scperturb_dataset_info_140922.csv#L1)。

[二] >218k cells/~750 perturbations为研究概述，旧整合目录RNA有249标签，可能分别是guide层与合并target层。没有原文件不自行强行统一为“750基因”，也不认定两个数字矛盾必是错误。

[推] 可研究免疫背景内遗传预测，或明示遗传×免疫背景生物泛化。患者模型、IFNγ、共培养不是应该消除的技术batch。若技术库与treatment完全混杂，校正效果不能被识别为纯技术改善。

[未知] 相同guide×免疫背景是否跨独立培养/library，NTC逐背景/逐batch数，背景/患者/技术层级嵌套。SCP/Zenodo受阻，未下载全obs。当前作为机制与G×E补充候选，技术批次主任务信息不足。

## 7. sci-Plex G×E（McFaline-Figueroa2024；benchmark别名McFaline23）

[二] 原文件GSM7056148 GxE1与GSM7056149 GxE2，benchmark从RDS转h5ad并合并GxE1/A172/T98G/U87MG。这是同研究不同实验与细胞背景，不能冒充多个独立数据源，也不能直接作为技术重复。原文已核实正式题名、GSE225775及作者sci-Plex-GxE仓库；2024-01-25发表，2024-02-14卷期，不能从DOI中的2023推断发表年。见 E33 [G×E原文 PDF pp7,15,20,22–23](https://raw.githubusercontent.com/cole-trapnell-lab/cole-trapnell-lab.github.io/a7ead73c4da7190d05b4928ace5b67d457329114/pdfs/papers/mcfaline-sci-plex-gxe.pdf)。见 E19 [PerturBench G×E原文件下载/转换](https://raw.githubusercontent.com/altoslabs/perturbench/c84038bc1ea409aa54f3832cfa6f34f5059adf0c/notebooks/neurips2025/data_curation/curate_McFalineFigueroa23_step1.R#L38)、E06 [pertpy数据文档与loader（整合方）](https://raw.githubusercontent.com/scverse/pertpy/a4c30738468f8cb6bed677efb9331a9e35a168bd/src/pertpy/data/_datasets.py#L29)。

[二] 元数据含`gene_id,treatment,dose,cell_type`；组合gene_id逗号转+，NTC/random/NA被benchmark转control。NA是否原始对照或未分配guide，必须原文件/设计核实，不根据转换规则把缺失当阴性对照。

[二] scPerturb notebook读独立hashTable：`orig_ident,cell_barcode,plate_id,all_ones,counts`，以最高hash counts推best_plate_id。它是**一细胞多hash记录的长表**，不是每行一个细胞；未先去重/判定doublet不能计细胞。highest hash本身也没有说明plate的物理批次类型。部分notebook代码还标注sample_sheet“useless?”并有未定义prefix，不能当完整可复现的已验证设计映射。

[推] 遗传×药物条件非常适合检查校正是否删除生物反应；但纯技术batch外推必须在同cell_type/gene/chemical/dose/time内定义。

[文] kinome screen原文明确两次独立转导、1,052,205细胞；使用4个RT板和4个连接板，部分实验复用hash但不混池，分配不同RT孔。[未知] GxE1/2与这些实验的精确对应、逐细胞转导/plate/pool/library/run映射、背景内NTC数量。GEO受阻，未下载hash长表；若该长表很大，优先请求作者导出去歧义后的cell-level plate标签及RNA-QC ID，不下载整个RDS来猜批次。当前补充候选。

### 新增原文核查：Gasperini2019

[文] STAR Methods明确规模实验32个10x lane在RT后分成两批各16 lane继续建库，提供了实际技术批次定义；差异表达方法明确将`prep_batch`纳入Monocle2回归模型，但不能据此声称预测泛化改善。原文两个at-scale实验共254,974细胞、5,920候选enhancers；2019-01-03发表、01-10卷期。见 E34 [Gasperini原文 STAR Methods / Single cell transcriptome capture](https://raw.githubusercontent.com/cole-trapnell-lab/cole-trapnell-lab.github.io/a7ead73c4da7190d05b4928ace5b67d457329114/pdfs/papers/gasperini-crispri.pdf)。[未知] 逐细胞lane→两批对应、同guide组合及对照的跨批次数量。因此升级为优先核实建库批次的候选；这不是独立培养重复，也尚不能宣布留批次测试可执行。

## 8. Kang2018 IFN-β PBMC

[文/二] IFN-β/未刺激6h PBMC子集。原研究含自然遗传变异demultiplexing与其他样本，不把常见scGen处理子集或所有GEO细胞合为一个统计范围。CPA Kang教程、CellOT lupuspatients与scPerturBench kangCrossCell/Patient证明采用。见 E02 [CPA作者README / tutorials](https://raw.githubusercontent.com/theislab/cpa/fbd7c0250edc23eff003a10c99655579c53afd63/README.md#L31)、E03 [CellOT作者README / experiments](https://raw.githubusercontent.com/bunnech/cellot/522d2b953da8ad244fcf36f64521487fdf763788/README.md#L11)、E05 [scPerturBench作者README / scenarios & citation](https://raw.githubusercontent.com/bm2-lab/scPerturBench/698f8ff5ed19530bff171e4205be9b42a46a769d/README.md#L8)。

[二] 基因型demultiplexed donor不是technical batch。CellOT任务示例的ctrl/stim、sample_id，以及benchmark留出患者描述，证明的是生物背景泛化设置，不证明独立技术batch。

[未知] 该IFN子集每donor供体内重复的独立培养/板/library/GEM/run；stim/ctrl是否跨同样技术库重复。若处理与library完全混杂，多个donor也不能解决识别问题。目前适合**跨供体/细胞类型补充任务**；纯技术batch主任务信息不足。

## 9. Norman2019组合CRISPRa

[文/二] 单/双基因CRISPRa；GEARS、CPA、PerturBench训练/留出单基因或组合测试都有明确代码证据。原作者原文件GSE133344 raw/filtered `cell_identities.csv.gz`在整合notebook被读取，这是可单独下载细胞metadata的实际线索。见 E01 [GEARS作者README / Core API](https://raw.githubusercontent.com/snap-stanford/GEARS/f374e43e197b295016d80395d7a54ddb81cc6769/README.md#L35)、E02 [CPA作者README / tutorials](https://raw.githubusercontent.com/theislab/cpa/fbd7c0250edc23eff003a10c99655579c53afd63/README.md#L31)、E27 [scPerturb原文件读取 / Norman Cells34,38](https://raw.githubusercontent.com/sanderlab/scPerturb/b69f72a070a92bcbaf41e7f9897b11598109ab48/dataset_processing/notebooks/data_access_and_preprocessing_JS.ipynb)。

[二] 旧目录filtered 237扰动标签含对照；不是原全screen组合数，也不是GEARS过滤后的训练条件数。遗传剂量编码1不是药物浓度。模型simulation/split标签是训练分割，不是experimental batch。

[未知] cell identities具体列，独立培养/处理板、建库、GEM、测序映射。同一单/双基因是否跨独立batch、每batch NT数量无法计算。GEO小metadata请求被代理拒绝；应直接取raw/filtered cell_identities并与实验样本表连接。当前组合模型参照值得保留，**不能因经典benchmark而默认技术batch适合**。

## 10. Parse cytokine PBMC（State使用版本）

[文] State原作者`parse_tomls`明确`[training] parse='train'`，fewshot val/test列出IFN、IL、growth factors等刺激。`donor.toml`有Donor1/4/9/12；`celltype.toml`有B-cell亚型。这直接证明ST预测训练/测试采用，而不是只做普通预训练。见 E18 [State作者Parse供体条件配置](https://raw.githubusercontent.com/arcinstitute/state/9bbfe78a434a55205e4de834e1ea99f85f7a3add/state_preprint_toml_files/parse_tomls/donor.toml#L7)、E24 [State原作者论文与训练教程](https://raw.githubusercontent.com/arcinstitute/state/9bbfe78a434a55205e4de834e1ea99f85f7a3add/README.md#L14)。

[未知] 正式资源card/accession、原paper、确切release、全资源供体/刺激数、counts与独立metadata下载。本轮不能把Donor12标签自动推断为已验证12供体，也不以俗称10M作为QC后细胞数。

[推] 多刺激与供体适合生物泛化；若有供体内多plate/library可转为技术batch任务。供体必须保留为背景。当前没有证明同cytokine/dose/time/donor跨独立技术重复，或每plate matched untreated。

[未知] culture/plate/library/run嵌套及留出可行性；列为信息不足的重点扩展候选。

## 新资源的进一步筛选结果

Tahoe-100M的官方文档明确 **100,648,790 cells、1,344 samples**，counts=h5ad、metadata=Parquet，`sample`定义为区分replicated treatment的unique treatment ID，`sublibrary`关联建库和测序；还包含`plate,drugname_drugconc,cell_line,pass_filter`。State明确提供Tahoe-trained ST，训练/评测配置也存在。单独Parquet是避免下大表达矩阵的理想路径。但plate/library与独立培养、相同dose/line跨plate和control覆盖仍未知。见 E17 [Arc官方Tahoe说明 / stats & obs schema](https://raw.githubusercontent.com/arcinstitute/arc-virtual-cell-atlas/4f7bb170c61d2fafce70f67db6e52c7d9af1be4b/tahoe-100M/README.md#L29)、E30 [State Tahoe训练与fewshot评测配置](https://raw.githubusercontent.com/arcinstitute/state/9bbfe78a434a55205e4de834e1ea99f85f7a3add/state_preprint_toml_files/tahoe_tomls/generalization.toml#L8)。

官方当前README说明2026-03-31旧GCS路径退役，迁移至Google Marketplace/Requester Pays，要求已订阅项目以获得规定免费额度。**本轮没有订阅、提供计费项目或执行下载**；不得默认旧bucket仍公开可读。优先核实官方小元数据镜像/Parquet大小及获取条件。见 E22 [Arc官方数据迁移/Requester Pays说明](https://raw.githubusercontent.com/arcinstitute/arc-virtual-cell-atlas/4f7bb170c61d2fafce70f67db6e52c7d9af1be4b/README.md#L9)。这属于真实获取限制，不把未打开文件说成不存在。

VCC2025官方描述H1 hESC、约300k cells/300 target genes，h5ad counts、Parquet/CSV metadata，train/validation/test按2025目录组织。`pert_counts_Training.csv`是计数摘要，不等同含全部library字段的cell obs；需要正式独立重复表。见 E16 [Arc官方Virtual Cell Challenge说明](https://raw.githubusercontent.com/arcinstitute/arc-virtual-cell-atlas/4f7bb170c61d2fafce70f67db6e52c7d9af1be4b/virtual-cell-challenge/README.md#L10)。State作者训练教程证明采用。

Nadig GSE264667的Jurkat/HepG2来自另一个原研究，State将其与Replogle2022合用。其gem_group→batch转换也不证明独立培养。它是跨细胞背景遗传补充，不能用于把跨原研究差异全部称纯技术batch。见 E21 [Nadig GSE264667整合notebook / Cells1,4,9,11](https://raw.githubusercontent.com/sanderlab/scPerturb/b69f72a070a92bcbaf41e7f9897b11598109ab48/dataset_processing/notebooks/NadigOConner2024.ipynb)、E24 [State原作者论文与训练教程](https://raw.githubusercontent.com/arcinstitute/state/9bbfe78a434a55205e4de834e1ea99f85f7a3add/README.md#L14)。

Jiang24已确认5个IFNB/IFNG/INS/TGFB/TNFA RDS和benchmark训练使用；`treatment`由文件名生成，NT为各刺激背景的遗传对照，而非未刺激对照。Seurat adata.raw.X被转换成X，不保证就是UMI counts。原paper、供体/技术重复、未刺激基线均未知。见 E20 [PerturBench Jiang24五种刺激RDS下载/转换](https://raw.githubusercontent.com/altoslabs/perturbench/c84038bc1ea409aa54f3832cfa6f34f5059adf0c/notebooks/neurips2025/data_curation/curate_Jiang24_step1.R#L23)。

## 元数据可回答的与表达矩阵才能回答的

已回答：sciPlex3设计样本条件覆盖、plate嵌套、对照设计、ID列表规模；MIX-seq作者声明的跨实验重叠和对照选择。没有回答：QC后细胞覆盖、guide效力、实际批次效应强度、校正保真、模型泛化收益。

元数据混杂决定哪些比较可识别，但无法给出真实batch effect强度。下一轮若获counts，先在matched controls内比较深度、基因检测数、mt比例、pseudobulk相关和batch方差；再在相同扰动内检查response-to-control、DE符号/效应量、重复一致性。细胞类型组成变化、真实时间响应、供体效应不能因跨batch分布不同就判为技术噪声。

检验“训练前指标能指导处理策略”需要外层留batch、内层选策略：所有归一化/HVG/拟合校正和策略选择在训练折完成，未见batch扰动表达留作最后评测。若使用未见batch的control适配，要单独标为允许test-control的协议；不与完全归纳的协议混在一起。跨数据集或跨独立实验验证指标→策略关系，不能在同一测试结果上择优再报告泛化。未来可比较不校正、仅规范化和技术因素校正，同时检查扰动与背景保真；本轮未执行这些表达/训练实验。

## 证据目录

- E01 [GEARS作者README / Core API](https://raw.githubusercontent.com/snap-stanford/GEARS/f374e43e197b295016d80395d7a54ddb81cc6769/README.md#L35)
- E02 [CPA作者README / tutorials](https://raw.githubusercontent.com/theislab/cpa/fbd7c0250edc23eff003a10c99655579c53afd63/README.md#L31)
- E03 [CellOT作者README / experiments](https://raw.githubusercontent.com/bunnech/cellot/522d2b953da8ad244fcf36f64521487fdf763788/README.md#L11)
- E04 [PerturBench作者README / Dataset Access](https://raw.githubusercontent.com/altoslabs/perturbench/c84038bc1ea409aa54f3832cfa6f34f5059adf0c/README.md#L28)
- E05 [scPerturBench作者README / scenarios & citation](https://raw.githubusercontent.com/bm2-lab/scPerturBench/698f8ff5ed19530bff171e4205be9b42a46a769d/README.md#L8)
- E06 [pertpy数据文档与loader（整合方）](https://raw.githubusercontent.com/scverse/pertpy/a4c30738468f8cb6bed677efb9331a9e35a168bd/src/pertpy/data/_datasets.py#L29)
- E07 [scPerturb旧版目录（140922，非原论文）](https://raw.githubusercontent.com/sanderlab/scPerturb/b69f72a070a92bcbaf41e7f9897b11598109ab48/metadata/scperturb_dataset_info_140922.csv#L1)
- E08 [sci-Plex原作者：hash、culture/RT/ligation/PCR映射](https://raw.githubusercontent.com/cole-trapnell-lab/sci-plex/079639c50811dd43a206a779ab2f0199a147c98f/large_screen/Notebook1_preprocess_data.R#L41)
- E09 [sci-Plex原作者Supplementary Table 3（样本表）](https://raw.githubusercontent.com/cole-trapnell-lab/sci-plex/079639c50811dd43a206a779ab2f0199a147c98f/large_screen/bin/Supplementary_Table_3.txt#L1)
- E10 [sci-Plex原作者hash设计表](https://raw.githubusercontent.com/cole-trapnell-lab/sci-plex/079639c50811dd43a206a779ab2f0199a147c98f/large_screen/bin/sciChem3_screen2_hashMeta_data.tsv)
- E11 [sci-Plex原作者valid cell ID列表（没有扰动注释）](https://raw.githubusercontent.com/cole-trapnell-lab/sci-plex/079639c50811dd43a206a779ab2f0199a147c98f/large_screen/bin/valid_cells.tsv)
- E12 [Replogle整合脚本：gem_group重命名batch](https://raw.githubusercontent.com/sanderlab/scPerturb/b69f72a070a92bcbaf41e7f9897b11598109ab48/dataset_processing/scripts/ReplogleWeissman2022.py#L49)
- E13 [Frangieh原作者README / counts与raw数据访问](https://raw.githubusercontent.com/klarman-cell-observatory/Perturb-CITE-seq/c90d46f268ffb7b30e9b35fc23ddd0967feca42b/README.md#L9)
- E14 [MIX-seq原作者实验与对照映射](https://raw.githubusercontent.com/broadinstitute/mix_seq_ms/edcf2266fc8fd586a4d9ee2db027d142f8a27ba6/src/expt_meta_data.R#L2)
- E15 [Open Problems原作者README / design及cell schema](https://raw.githubusercontent.com/openproblems-bio/task_perturbation_prediction/626f94521fd236e6b79cc60696159172dd07d2bd/README.md#L101)
- E16 [Arc官方Virtual Cell Challenge说明](https://raw.githubusercontent.com/arcinstitute/arc-virtual-cell-atlas/4f7bb170c61d2fafce70f67db6e52c7d9af1be4b/virtual-cell-challenge/README.md#L10)
- E17 [Arc官方Tahoe说明 / stats & obs schema](https://raw.githubusercontent.com/arcinstitute/arc-virtual-cell-atlas/4f7bb170c61d2fafce70f67db6e52c7d9af1be4b/tahoe-100M/README.md#L29)
- E18 [State作者Parse供体条件配置](https://raw.githubusercontent.com/arcinstitute/state/9bbfe78a434a55205e4de834e1ea99f85f7a3add/state_preprint_toml_files/parse_tomls/donor.toml#L7)
- E19 [PerturBench G×E原文件下载/转换](https://raw.githubusercontent.com/altoslabs/perturbench/c84038bc1ea409aa54f3832cfa6f34f5059adf0c/notebooks/neurips2025/data_curation/curate_McFalineFigueroa23_step1.R#L38)
- E20 [PerturBench Jiang24五种刺激RDS下载/转换](https://raw.githubusercontent.com/altoslabs/perturbench/c84038bc1ea409aa54f3832cfa6f34f5059adf0c/notebooks/neurips2025/data_curation/curate_Jiang24_step1.R#L23)
- E21 [Nadig GSE264667整合notebook / Cells1,4,9,11](https://raw.githubusercontent.com/sanderlab/scPerturb/b69f72a070a92bcbaf41e7f9897b11598109ab48/dataset_processing/notebooks/NadigOConner2024.ipynb)
- E22 [Arc官方数据迁移/Requester Pays说明](https://raw.githubusercontent.com/arcinstitute/arc-virtual-cell-atlas/4f7bb170c61d2fafce70f67db6e52c7d9af1be4b/README.md#L9)
- E23 [CINEMA-OT原作者论文/教程说明](https://raw.githubusercontent.com/vandijklab/CINEMA-OT/949bc3f587285a5c7ed92c6d3fd345b42a9f791c/Readme.md#L14)
- E24 [State原作者论文与训练教程](https://raw.githubusercontent.com/arcinstitute/state/9bbfe78a434a55205e4de834e1ea99f85f7a3add/README.md#L14)
- E25 [PerturBench OP3 curation / Cells7,20,27](https://raw.githubusercontent.com/altoslabs/perturbench/c84038bc1ea409aa54f3832cfa6f34f5059adf0c/notebooks/neurips2025/data_curation/curate_op3.ipynb)
- E26 [PerturBench Frangieh curation / Cells4,6,8](https://raw.githubusercontent.com/altoslabs/perturbench/c84038bc1ea409aa54f3832cfa6f34f5059adf0c/notebooks/neurips2025/data_curation/curate_Frangieh21.ipynb)
- E27 [scPerturb原文件读取 / Norman Cells34,38](https://raw.githubusercontent.com/sanderlab/scPerturb/b69f72a070a92bcbaf41e7f9897b11598109ab48/dataset_processing/notebooks/data_access_and_preprocessing_JS.ipynb)
- E28 [sci-Plex原作者重复性分析代码](https://raw.githubusercontent.com/cole-trapnell-lab/sci-plex/079639c50811dd43a206a779ab2f0199a147c98f/large_screen/Notebook17_Replicability_DEG_test.R#L1)
- E29 [Replogle下游过滤notebook / Cell5](https://raw.githubusercontent.com/sanderlab/scPerturb/b69f72a070a92bcbaf41e7f9897b11598109ab48/revision/notebooks/replogle_handling.ipynb)
- E30 [State Tahoe训练与fewshot评测配置](https://raw.githubusercontent.com/arcinstitute/state/9bbfe78a434a55205e4de834e1ea99f85f7a3add/state_preprint_toml_files/tahoe_tomls/generalization.toml#L8)
- E32 [sciPlex原文 PDF pp2,4,6](https://raw.githubusercontent.com/cole-trapnell-lab/cole-trapnell-lab.github.io/a7ead73c4da7190d05b4928ace5b67d457329114/pdfs/papers/srivatsan_mcfaline_ramani_sci-plex_Science_2019.pdf)
- E33 [G×E原文 PDF pp7,15,20,22–23](https://raw.githubusercontent.com/cole-trapnell-lab/cole-trapnell-lab.github.io/a7ead73c4da7190d05b4928ace5b67d457329114/pdfs/papers/mcfaline-sci-plex-gxe.pdf)
- E34 [Gasperini原文 STAR Methods / Single cell transcriptome capture](https://raw.githubusercontent.com/cole-trapnell-lab/cole-trapnell-lab.github.io/a7ead73c4da7190d05b4928ace5b67d457329114/pdfs/papers/gasperini-crispri.pdf)
- E31 [State Replogle合并目录/训练配置](https://raw.githubusercontent.com/arcinstitute/state/9bbfe78a434a55205e4de834e1ea99f85f7a3add/state_preprint_toml_files/replogle_tomls/k562.toml#L2)

每个下载对象的精确commit、URL、byte数与SHA-256见 `resources.json` 和 `download_log.jsonl`。本轮计算见 `tables/*_design/summary.json`；网络拒绝与尺寸未知见 `access_log.jsonl`。没有找到batch记录，不等于没有batch effect。

公开benchmark结果还明确出现Replogle_K562essential/RPE1essential、TianActivation/Inhibition、Papalexi、Frangieh、Adamson、Norman等标签，采用证据见 `tables/observed_benchmark_usage.csv`。这比loader支持更强，但仍不能从结果表推断每方法训练/微调协议或模糊exp标签的原研究身份。对应下载文件为冻结来源，未读取其分数来替代本研究的模型验证。

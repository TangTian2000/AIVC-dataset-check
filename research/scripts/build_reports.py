#!/usr/bin/env python3
"""Build the evidence-linked audit reports from frozen sources and metadata summaries."""
from pathlib import Path
import json,csv
R=Path(__file__).resolve().parents[1]
resources=json.loads((R/'resources.json').read_text());byid={x['id']:x for x in resources}
def ref(i,label,locator=''):
    u=byid[i]['url'];p=R/byid[i]['path']
    if locator and p.exists() and p.suffix!='.ipynb':
        for n,line in enumerate(p.read_text(errors='replace').splitlines(),1):
            if locator in line:u+=f'#L{n}';break
    return f'[{label}]({u})'
refs={
'E01':('gears_README_md','GEARS作者README / Core API','norman, adamson, dixit'),
'E02':('cpa_README_md','CPA作者README / tutorials','Predicting combinatorial'),
'E03':('cellot_README_md','CellOT作者README / experiments','holdout lupus'),
'E04':('perturbench_README_md','PerturBench作者README / Dataset Access','Dataset Access'),
'E05':('scperturbench_README_md','scPerturBench作者README / scenarios & citation','Cellular context'),
'E06':('pertpy__datasets_py','pertpy数据文档与loader（整合方）','def papalexi_2021'),
'E07':('scperturb_scperturb_dataset_info_140922_csv','scPerturb旧版目录（140922，非原论文）','Index'),
'E08':('scplex_Notebook1_preprocess_data_R','sci-Plex原作者：hash、culture/RT/ligation/PCR映射','culture_plate = top_oligo_P'),
'E09':('scplex_Supplementary_Table_3_txt','sci-Plex原作者Supplementary Table 3（样本表）','well_oligo'),
'E10':('scplex_sciChem3_screen2_hashMeta_data_tsv','sci-Plex原作者hash设计表',''),
'E11':('scplex_valid_cells_tsv','sci-Plex原作者valid cell ID列表（没有扰动注释）',''),
'E12':('scperturb_ReplogleWeissman2022_py','Replogle整合脚本：gem_group重命名batch','gem_group'),
'E13':('frangieh_README_md','Frangieh原作者README / counts与raw数据访问','Count matrices'),
'E14':('mixseq_expt_meta_data_R','MIX-seq原作者实验与对照映射','sc_expts'),
'E15':('op3_primary_readme','Open Problems原作者README / design及cell schema','144 compounds'),
'E16':('arc_atlas_virtual-cell-challenge','Arc官方Virtual Cell Challenge说明','Metadata'),
'E17':('arc_atlas_tahoe-100M','Arc官方Tahoe说明 / stats & obs schema','obs (cell)'),
'E18':('state_parse_tomls_donor_toml','State作者Parse供体条件配置','[training]'),
'E19':('perturbench_curate_McFalineFigueroa23_step1_R','PerturBench G×E原文件下载/转换','GSM7056148'),
'E20':('perturbench_curate_Jiang24_step1_R','PerturBench Jiang24五种刺激RDS下载/转换','10520190'),
'E21':('scperturb_NadigOConner2024_ipynb','Nadig GSE264667整合notebook / Cells1,4,9,11',''),
'E22':('arc_atlas_root','Arc官方数据迁移/Requester Pays说明','March 31, 2026'),
'E23':('cinemaot_primary_readme','CINEMA-OT原作者论文/教程说明','Causal identification'),
'E24':('state_primary_readme','State原作者论文与训练教程','Replogle-Nadig'),
'E25':('perturbench_curate_op3_ipynb','PerturBench OP3 curation / Cells7,20,27',''),
'E26':('perturbench_curate_Frangieh21_ipynb','PerturBench Frangieh curation / Cells4,6,8',''),
'E27':('scperturb_data_access_and_preprocessing_JS_ipynb','scPerturb原文件读取 / Norman Cells34,38',''),
'E28':('scplex_Notebook17_Replicability_DEG_test_R','sci-Plex原作者重复性分析代码','rep'),
'E29':('scperturb_replogle_handling_ipynb','Replogle下游过滤notebook / Cell5',''),
'E30':('state_tahoe_tomls_generalization_toml','State Tahoe训练与fewshot评测配置','[training]'),
'E32':('sciplex_primary','sciPlex原文 PDF pp2,4,6',''),
'E33':('gxe_primary','G×E原文 PDF pp7,15,20,22–23',''),
'E34':('gasperini_primary','Gasperini原文 STAR Methods / Single cell transcriptome capture',''),
'E31':('state_replogle_tomls_k562_toml','State Replogle合并目录/训练配置','replogle_nogwps_v2'),
}
def e(k):return k+' '+ref(*refs[k])
bib='\n'.join('- '+e(k) for k in refs)
summary=json.loads((R/'tables/sciplex3_design/summary.json').read_text())
report=f'''# 深入审计报告

日期：2026-10-11（UTC）（含新增原文核查）。先保存第一阶段总表，再深入核查；随后因State/Arc新证据补充Parse、Nadig、VCC。最终总表32个版本/子资源条目、28个候选家族。不是28个均已证明“常用”，也不是32个独立来源；缺少原研究身份核验的条目保留未知。第一阶段快照见 `tables/dataset_inventory_stage1.*`。

本轮统一深入核查10个候选：sciPlex3、Replogle K562、Replogle RPE1、MIX-seq、OP3、Frangieh、sci-Plex G×E、Kang、Norman、Parse。Jiang24、Tahoe、Nadig、VCC完成有来源的扩展筛选，未冒充完成细胞级深审计。

**结论：sciPlex3设计层面最有希望；MIX-seq与OP3值得优先补齐元数据。当前没有一个候选已完成全部细胞级覆盖和独立技术批次证明，不能宣称主研究测试任务已可用。** 未检验任何表达矩阵的真实批次效应强度。

证据标签：**[文]** 原作者代码/说明明确记录；原论文全文若未访问会注明。**[算]** 本轮从下载的真实元数据/设计表计算，明确单位。**[二]** 模型/benchmark/整合资源记录，不能替代原实验说明。**[推]** 有条件推测。**[未知]** 未能核实。字段名或条形码后缀不构成独立技术批次证据。

## 统一判断标准

必须先给实验单元建立层级：独立培养/处理重复 → 处理板/孔 → 样本pool/hash → 建库/GEM group → 测序run/lane。关系未证实就保持未知；重复给同一library测序、同一pool拆多个GEM、同一板多孔都不能自动视为独立培养重复。

纯技术批次外推的条件单元为 `扰动（可含guide身份）×剂量×时间×细胞背景×必要刺激背景`；原代数据还要保留供体。先在背景内判断跨batch覆盖，再单独研究跨供体/细胞系外推。每一留出条件都需至少一个训练批次包含相同条件及其匹配对照，测试批次也需有匹配对照。细胞≥30只是后续脚本的可调工程门槛，不是足够实验重复或统计功效的保证。

两个技术层级要分别测试，不能混为一个结果：同一培养pool跨library/GEM评估较浅的建库泛化；跨独立培养/处理重复评估较深的实验泛化。若library完全嵌套在treatment，缺少跨library共同条件，无法识别该层级的批次校正效果。

## 1. sciPlex3（Srivatsan2020家族）

[文] 原作者Notebook1由 `top_oligo_P` 生成 `culture_plate`；`well_oligo + plate_oligo` 经hash表关联细胞背景、replicate、time、drug-dose。RT、ligation、PCR plate/well另有代码字段，分别是组合索引步骤，不能当培养批次互换。它使用sci-RNA-seq，不套用10x GEM group定义。见 {e('E08')}、{e('E09')}。

[算] 作者Supplementary Table 3有 **4,992个唯一hash样本键、52个plate_oligo、rep1/rep2两个标签、188种药+S0000 vehicle**。两个作者样本表的6个共同字段逐键完全相符，重复键为0。每个plate有96个设计样本、2个vehicle样本；每plate只对应一个cell_type、一个replicate和一个time_point，三个因素均嵌套在plate。

[算] 24h：A549/K562/MCF7各188药×4剂量×2rep。72h：仅A549，47药×4剂量×2rep。编码dose为10/100/1000/10000，vehicle归零；原文第2页已目视核实为10/100 nM、1/10 µM。处理样本 **4,888**，vehicle样本 **104**。严格条件标签含对照共2,448，均覆盖两rep及两plate标签；在设计表单位下，4,888个“留出组×非对照条件”均具有另一组同条件与背景/时间匹配对照。

这不意味着每种药覆盖所有plate。不同plate承载不同药物子集，plate与面板部分混杂；只有重叠条件子集适合测试。72h不是三细胞系共享的独立技术batch，它是仅A549的不同生物条件。要保留time和cell_type，不能直接整合成同批次分布。

[算] `valid_cells.tsv`有 **649,340个唯一细胞ID**（18,484,236 bytes）。该文件只有ID，没有细胞到hash/replicate/培养板/处理的映射。这一枚举不是重新验证h5ad矩阵行数，也不能把649,340均分到4,992个样本。完整cell obs仍未取得。因此 **真实batch×perturbation细胞数、每batch对照细胞数、QC后跨batch覆盖、每条件可训练细胞数未计算**。

[文] 原文第2页明确重复培养板和孔位随机化，第4页Fig.3A明确biological replicate，已支持生物学重复设计。见 {e('E32')}。[推] 固定背景、剂量和时间留出重复很有希望；仍需逐细胞对应及培养日期/lot、索引板、建库、测序关系，不能把52个板当52次独立实验。

[未知] culture_plate与独立培养日期/lot、建库/测序run的映射；每rep/plate过滤后的细胞数；真实批次强度。下一步下载GSM4150378完整cell metadata或请作者导出`colData(cds)`，保留hash与所有索引步骤。无需先下载大表达矩阵。

已生成 [设计统计目录](../tables/sciplex3_design/summary.json)：`batch_x_perturbation_n_design_samples.csv`、`controls_by_batch_n_design_samples.csv`、`condition_coverage_n_design_samples.csv`、按背景/剂量/时间交叉表、`leave_one_group_out_n_design_samples.csv`。文件名明确为样本数。

同家族sciPlex2的headerless hashSampleSheet有192行。本轮按无表头读取并解析drug/dose/well；第3列语义未确认，没有称其为replicate。pertpy文档称4药×7剂量×triplicate、24h；样本表含其他标记，须核实样本设计，不能直接推断全部192行都是正式药物处理。sciPlex4是另一HDACi rescue实验，不等于CPA新组合药物GSE206741。

## 2. Replogle K562：GWPS与essential须分开

[文/二] 原作者原文件名在整合脚本中分别为`K562_gwps_raw_singlecell_01.h5ad`、`K562_essential_raw_singlecell_01.h5ad`。同研究但面板/时间不同，不能当相同扰动跨batch独立重复。`gene`用于扰动、`sgID_AB`改名guide_id、`gem_group`改名batch，non-targeting是对照。见 {e('E12')}。

[二] gem_group→batch只是整合约定，不能证明独立培养/处理，不能自动当测序批次。GEM/library/culture/run是否一对一或嵌套均未知。原细胞背景是K562，要与RPE1和后续Jurkat/HepG2区别。

[二] 旧目录GWPS有9,867、essential有2,058扰动标签（含对照），不是已读原obs基因数、guide数或本轮细胞数。GWPS文档day8；essential docstring开头day7而内文day6/day7混用，原文/作者表须解决这一时间冲突。`scPerturb`旧目录的提交年不应当出版年。见 {e('E06')}、{e('E07')}。

[二] GEARS README仅明确v0.1.1支持K562 essential/RPE1 loader；“支持下载”不证明原GEARS论文评测采用。State README称Replogle-Nadig，其`replogle_nogwps_v2`合并目录还含Jurkat/HepG2，不能把该训练目录的结果归到2022 GWPS。见 {e('E01')}、{e('E24')}、{e('E31')}。

[二] 下游notebook按min_counts和equal_subsampling筛选、保存counts再normalize/log1p，这会改变条件与批次覆盖。不能用标准化均衡子集替代原始批次结构和QC指标。见 {e('E29')}。

[未知] 独立培养重复、plate/GEM/library/测序关系；同一gene/guide跨GEM覆盖；每GEM non-targeting数；技术批次留出能否保留相同时间、面板和对照。原门户受代理拒绝。当前推荐 **信息不足，优先核实**；不默认不适合，也不默认满足目标。

## 3. Replogle RPE1

[二] 同2022家族的hTERT-RPE1 essential screen，整合脚本读`rpe1_raw_singlecell_01.h5ad`；基于CRISPRi，non-targeting对照。旧目录2,394标签含对照，不是本轮obs枚举。文档day7。

[二] 字段与K562一样存在gem_group→batch。K562/RPE1是生物背景与不同筛选，不能把两细胞系作为要消除的技术批次。应先在RPE1内部证明跨独立技术批次条件覆盖，再另设跨背景外推。

[未知] 所有培养/板/library/run的映射、跨GEM重复和匹配对照数量。尚不能判定“已见扰动、未见独立批次”可构建。原始h5ad可能包含obs，但没有验证独立小元数据下载；门户拒绝导致尺寸也未知。见 {e('E12')}、{e('E06')}。

## 4. MIX-seq（McFarland2020）

[文] 原作者`expt_meta_data.R`明确`sc_expts`与`sc_DE_meta`，定义数据版本、`expt_batch`及treat/control对应。脚本用Taiga名称/版本管理，作者README说明Figshare公开副本与本地路径。这是实验级元数据，不是细胞数。见 {e('E14')}。

[算] 本轮解析该文件 **30个声明数据集、5个实验标签：expt1/2/3/5/10、20个DE comparison**。只有这些在当前文件被核实，不声称覆盖全研究所有实验。固定24h时，Trametinib在expt1/expt3重复；两个实验均有6h/24h DMSO。expt10是另一药物面板，expt2是GPX4 guide等遗传处理，expt5是time course。这些不构成通用全药物×全实验笛卡尔积。

[文] 部分6h/24h比较同时借用两个时间的DMSO，`comparison_control_links.csv`保存作者实际选择；这不等于所有对照严格时间匹配。若研究时间保真，应改在元数据审计阶段筛选可匹配对照的条件，不能默默沿用混合时间的参照。

[推] Trametinib 24h跨expt1/expt3可做候选实验留出，但须筛选两实验共同细胞系/相同剂量，核实pool、培养条件及独立运行。expt_batch包含不同细胞系pool/协议，不能全部视为纯技术可消除因素。SNP分类细胞系是生物背景，必须保留。

[未知] 单细胞标签、各实验共同细胞系数量、剂量、QC后counts、独立培养/建库/测序映射。Figshare API访问失败；本轮未把Taiga内部链接当公开文件。只有 [实验级设计输出](../tables/mixseq_design/summary.json)，没有细胞级跨表。条件性优先候选。

## 5. Open Problems / NeurIPS 2023 PBMC（OP3）

[文] 作者README：144 compounds、24h、3 healthy donors；另有每供体baseline Multiome。这些donor是生物背景，baseline Multiome不是相同技术重复。scRNA schema明确`dose_uM,timepoint_hr,well,row,col,plate_name,hashtag_id,donor_id,sm_name,cell_type`，`layers[counts]`与原cell ID。见 {e('E15')}。

[二] PerturBench curation明确GSE279945；DMSO为negative control，belinostat/dabrafenib是positive controls。它引用原文剂量：belinostat0.1µM、DMSO14.1µM、其他1µM；本轮没有原文/obs独立复核。标成control并不意味着都是未扰动细胞。见 {e('E25')}。

[文] competition训练/测试常用DE结果；`de_train.uns[single_cell_obs]`官方描述为**训练集**细胞metadata，不能覆盖整个实验的private test/所有plate。PerturBench另用scRNA矩阵。比赛的细胞背景/药物split不是technical-batch split。

[推] 可先在每donor×cell_type×dose×24h内测试plate/library留出；需要每plate有DMSO、留出板药物在其他板仍存在。若plate完全由donor/药物面板决定，donor间“跨batch”会混入生物或干预变化。

[未知] plate→donor/well/pool/library/run嵌套、细胞数和跨板药物覆盖。处理h5ad HEAD被代理拒绝，尺寸未知。需官方导出全obs（包括control状态与split）或从完整metadata分片获得；不能只读训练DE文件声称全实验审计完成。条件性优先候选。

## 6. Frangieh Perturb-CITE-seq

[文] 原作者README公开SCP1064 UMI矩阵，raw reads指DUOS-000124；不能把受控raw sequencing与公开count matrix混称“raw全部公开”。原作者QC门槛<200 genes、>18% mitochondrial、genes<200 cells属于原流程记录，未在本轮复算。见 {e('E13')}。

[二] 研究包含遗传扰动与Control/Co-culture/IFNγ背景。benchmark将`perturbation_2`映射为`treatment`，并把`cell_type`统一成melanocyte；这可能省略患者模型的生物差异，需原obs的patient/model字段。benchmark设置`perturbation_type='CRISPRi'`，而原资源目录写CRISPR-Cas9。**机制注释不一致，不能未经原文核验按benchmark标签决定KO/i。** 见 {e('E26')}、{e('E07')}。

[二] >218k cells/~750 perturbations为研究概述，旧整合目录RNA有249标签，可能分别是guide层与合并target层。没有原文件不自行强行统一为“750基因”，也不认定两个数字矛盾必是错误。

[推] 可研究免疫背景内遗传预测，或明示遗传×免疫背景生物泛化。患者模型、IFNγ、共培养不是应该消除的技术batch。若技术库与treatment完全混杂，校正效果不能被识别为纯技术改善。

[未知] 相同guide×免疫背景是否跨独立培养/library，NTC逐背景/逐batch数，背景/患者/技术层级嵌套。SCP/Zenodo受阻，未下载全obs。当前作为机制与G×E补充候选，技术批次主任务信息不足。

## 7. sci-Plex G×E（McFaline-Figueroa2024；benchmark别名McFaline23）

[二] 原文件GSM7056148 GxE1与GSM7056149 GxE2，benchmark从RDS转h5ad并合并GxE1/A172/T98G/U87MG。这是同研究不同实验与细胞背景，不能冒充多个独立数据源，也不能直接作为技术重复。原文已核实正式题名、GSE225775及作者sci-Plex-GxE仓库；2024-01-25发表，2024-02-14卷期，不能从DOI中的2023推断发表年。见 {e('E33')}。见 {e('E19')}、{e('E06')}。

[二] 元数据含`gene_id,treatment,dose,cell_type`；组合gene_id逗号转+，NTC/random/NA被benchmark转control。NA是否原始对照或未分配guide，必须原文件/设计核实，不根据转换规则把缺失当阴性对照。

[二] scPerturb notebook读独立hashTable：`orig_ident,cell_barcode,plate_id,all_ones,counts`，以最高hash counts推best_plate_id。它是**一细胞多hash记录的长表**，不是每行一个细胞；未先去重/判定doublet不能计细胞。highest hash本身也没有说明plate的物理批次类型。部分notebook代码还标注sample_sheet“useless?”并有未定义prefix，不能当完整可复现的已验证设计映射。

[推] 遗传×药物条件非常适合检查校正是否删除生物反应；但纯技术batch外推必须在同cell_type/gene/chemical/dose/time内定义。

[文] kinome screen原文明确两次独立转导、1,052,205细胞；使用4个RT板和4个连接板，部分实验复用hash但不混池，分配不同RT孔。[未知] GxE1/2与这些实验的精确对应、逐细胞转导/plate/pool/library/run映射、背景内NTC数量。GEO受阻，未下载hash长表；若该长表很大，优先请求作者导出去歧义后的cell-level plate标签及RNA-QC ID，不下载整个RDS来猜批次。当前补充候选。

### 新增原文核查：Gasperini2019

[文] STAR Methods明确规模实验32个10x lane在RT后分成两批各16 lane继续建库，提供了实际技术批次定义；差异表达方法明确将`prep_batch`纳入Monocle2回归模型，但不能据此声称预测泛化改善。原文两个at-scale实验共254,974细胞、5,920候选enhancers；2019-01-03发表、01-10卷期。见 {e('E34')}。[未知] 逐细胞lane→两批对应、同guide组合及对照的跨批次数量。因此升级为优先核实建库批次的候选；这不是独立培养重复，也尚不能宣布留批次测试可执行。

## 8. Kang2018 IFN-β PBMC

[文/二] IFN-β/未刺激6h PBMC子集。原研究含自然遗传变异demultiplexing与其他样本，不把常见scGen处理子集或所有GEO细胞合为一个统计范围。CPA Kang教程、CellOT lupuspatients与scPerturBench kangCrossCell/Patient证明采用。见 {e('E02')}、{e('E03')}、{e('E05')}。

[二] 基因型demultiplexed donor不是technical batch。CellOT任务示例的ctrl/stim、sample_id，以及benchmark留出患者描述，证明的是生物背景泛化设置，不证明独立技术batch。

[未知] 该IFN子集每donor供体内重复的独立培养/板/library/GEM/run；stim/ctrl是否跨同样技术库重复。若处理与library完全混杂，多个donor也不能解决识别问题。目前适合**跨供体/细胞类型补充任务**；纯技术batch主任务信息不足。

## 9. Norman2019组合CRISPRa

[文/二] 单/双基因CRISPRa；GEARS、CPA、PerturBench训练/留出单基因或组合测试都有明确代码证据。原作者原文件GSE133344 raw/filtered `cell_identities.csv.gz`在整合notebook被读取，这是可单独下载细胞metadata的实际线索。见 {e('E01')}、{e('E02')}、{e('E27')}。

[二] 旧目录filtered 237扰动标签含对照；不是原全screen组合数，也不是GEARS过滤后的训练条件数。遗传剂量编码1不是药物浓度。模型simulation/split标签是训练分割，不是experimental batch。

[未知] cell identities具体列，独立培养/处理板、建库、GEM、测序映射。同一单/双基因是否跨独立batch、每batch NT数量无法计算。GEO小metadata请求被代理拒绝；应直接取raw/filtered cell_identities并与实验样本表连接。当前组合模型参照值得保留，**不能因经典benchmark而默认技术batch适合**。

## 10. Parse cytokine PBMC（State使用版本）

[文] State原作者`parse_tomls`明确`[training] parse='train'`，fewshot val/test列出IFN、IL、growth factors等刺激。`donor.toml`有Donor1/4/9/12；`celltype.toml`有B-cell亚型。这直接证明ST预测训练/测试采用，而不是只做普通预训练。见 {e('E18')}、{e('E24')}。

[未知] 正式资源card/accession、原paper、确切release、全资源供体/刺激数、counts与独立metadata下载。本轮不能把Donor12标签自动推断为已验证12供体，也不以俗称10M作为QC后细胞数。

[推] 多刺激与供体适合生物泛化；若有供体内多plate/library可转为技术batch任务。供体必须保留为背景。当前没有证明同cytokine/dose/time/donor跨独立技术重复，或每plate matched untreated。

[未知] culture/plate/library/run嵌套及留出可行性；列为信息不足的重点扩展候选。

## 新资源的进一步筛选结果

Tahoe-100M的官方文档明确 **100,648,790 cells、1,344 samples**，counts=h5ad、metadata=Parquet，`sample`定义为区分replicated treatment的unique treatment ID，`sublibrary`关联建库和测序；还包含`plate,drugname_drugconc,cell_line,pass_filter`。State明确提供Tahoe-trained ST，训练/评测配置也存在。单独Parquet是避免下大表达矩阵的理想路径。但plate/library与独立培养、相同dose/line跨plate和control覆盖仍未知。见 {e('E17')}、{e('E30')}。

官方当前README说明2026-03-31旧GCS路径退役，迁移至Google Marketplace/Requester Pays，要求已订阅项目以获得规定免费额度。**本轮没有订阅、提供计费项目或执行下载**；不得默认旧bucket仍公开可读。优先核实官方小元数据镜像/Parquet大小及获取条件。见 {e('E22')}。这属于真实获取限制，不把未打开文件说成不存在。

VCC2025官方描述H1 hESC、约300k cells/300 target genes，h5ad counts、Parquet/CSV metadata，train/validation/test按2025目录组织。`pert_counts_Training.csv`是计数摘要，不等同含全部library字段的cell obs；需要正式独立重复表。见 {e('E16')}。State作者训练教程证明采用。

Nadig GSE264667的Jurkat/HepG2来自另一个原研究，State将其与Replogle2022合用。其gem_group→batch转换也不证明独立培养。它是跨细胞背景遗传补充，不能用于把跨原研究差异全部称纯技术batch。见 {e('E21')}、{e('E24')}。

Jiang24已确认5个IFNB/IFNG/INS/TGFB/TNFA RDS和benchmark训练使用；`treatment`由文件名生成，NT为各刺激背景的遗传对照，而非未刺激对照。Seurat adata.raw.X被转换成X，不保证就是UMI counts。原paper、供体/技术重复、未刺激基线均未知。见 {e('E20')}。

## 元数据可回答的与表达矩阵才能回答的

已回答：sciPlex3设计样本条件覆盖、plate嵌套、对照设计、ID列表规模；MIX-seq作者声明的跨实验重叠和对照选择。没有回答：QC后细胞覆盖、guide效力、实际批次效应强度、校正保真、模型泛化收益。

元数据混杂决定哪些比较可识别，但无法给出真实batch effect强度。下一轮若获counts，先在matched controls内比较深度、基因检测数、mt比例、pseudobulk相关和batch方差；再在相同扰动内检查response-to-control、DE符号/效应量、重复一致性。细胞类型组成变化、真实时间响应、供体效应不能因跨batch分布不同就判为技术噪声。

检验“训练前指标能指导处理策略”需要外层留batch、内层选策略：所有归一化/HVG/拟合校正和策略选择在训练折完成，未见batch扰动表达留作最后评测。若使用未见batch的control适配，要单独标为允许test-control的协议；不与完全归纳的协议混在一起。跨数据集或跨独立实验验证指标→策略关系，不能在同一测试结果上择优再报告泛化。未来可比较不校正、仅规范化和技术因素校正，同时检查扰动与背景保真；本轮未执行这些表达/训练实验。

## 证据目录

{bib}

每个下载对象的精确commit、URL、byte数与SHA-256见 `resources.json` 和 `download_log.jsonl`。本轮计算见 `tables/*_design/summary.json`；网络拒绝与尺寸未知见 `access_log.jsonl`。没有找到batch记录，不等于没有batch effect。
'''
(R/'audits/deep_audit.md').write_text(report)
# Machine-readable availability is deliberately not a fake zero-cell table.
availability=[]
for id in ['sciplex3','replogle2022_k562_gwps','replogle2022_rpe1','mcfarland2020','op3_2023','frangieh2021','mcfaline2023','kang2018','norman2019','parse_cytokines']:
 availability.append(dict(dataset_id=id,cell_metadata_status='not_obtained',batch_x_perturbation_cell_counts='not_computed',controls_by_batch_cell_counts='not_computed',strict_cell_condition_coverage='not_computed',batch_context_dose_time_cell_crosstabs='not_computed',design_statistics='computed; sample-level only' if id=='sciplex3' else 'computed; experiment declarations only' if id=='mcfarland2020' else 'source/schema audit only',independent_technical_batch_proven='primary paper supports biological replicates / independent transductions; cell mapping pending' if id in {'sciplex3','mcfaline2023'} else 'not established',cell_level_batch_mapping_validated='no',expression_batch_strength='not_evaluated'))
with (R/'audits/availability.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,list(availability[0]));w.writeheader();w.writerows(availability)
index=[]
for key,(ident,label,loc) in refs.items():
 x=byid[ident];index.append(dict(evidence_id=key,label=label,resource_id=ident,url=x['url'],local_path=x['path'],section_or_locator=loc))
with (R/'sources/evidence_index.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,list(index[0]));w.writeheader();w.writerows(index)
print('Built audit report, availability matrix, evidence index')

inventory=json.loads((R/'tables/dataset_inventory.json').read_text())
priority={'sciplex3','mcfarland2020','op3_2023'}
supplement={'norman2019','lotfollahi2023_combo','kang2018','hagai2018','frangieh2021','papalexi2021','tian2019','tian2021','shifrut2018','zhao2021','mcfaline2023','dong2023','nadig2024','vcc2025','sciplex2'}
not_primary={'aissa2021'}
recommend=[]
for row in inventory:
 i=row['dataset_id'];tier='优先采用' if i in priority else '可作补充' if i in supplement else '暂不适合' if i in not_primary else '信息不足'
 target='供体内/同背景的技术批次试点（条件性）' if i in priority else '遗传组合参照' if i=='norman2019' else '跨供体/细胞类型/物种生物泛化；不当纯技术batch' if i in {'kang2018','hagai2018','shifrut2018','zhao2021','nadig2024'} else '遗传×刺激/药物及生物保真补充' if i in {'frangieh2021','mcfaline2023','lotfollahi2023_combo','dong2023'} else '当前PC9多时间子集暂不直接作为纯技术batch主任务' if i in not_primary else '扩展筛选/元数据核实后再定'
 gate='完整cell-to-hash/QC映射 + 原文重复与培养/建库/run对应' if i=='sciplex3' else 'expt1/3共同细胞系、Trametinib24h同剂量及独立运行' if i=='mcfarland2020' else '供体内plate/library重复 + 每板DMSO + 跨板共同药物' if i=='op3_2023' else '核实独立培养/处理/建库映射、跨batch相同条件及匹配阴性对照'
 if i=='aissa2021':gate='优先核实是否有同时间未处理对照；其他multirep子研究不能自动继承当前子集'
 recommend.append(dict(dataset_id=i,family_id=row['family_id'],tier=tier,task_fit=target,reason=row['screening_reason'],adoption_gate=gate,technical_batch_task_ready='未证实',source_urls=row['source_urls']))
with (R/'tables/recommendations.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,list(recommend[0]));w.writeheader();w.writerows(recommend)
text='''# 推荐清单

这些分级针对“批次效应、校正对扰动预测泛化的影响、训练前质量指标指导策略”的研究目的，不按细胞数或知名度排序。

**“优先采用”是条件性试点/核实优先级，不表示已具备可执行的独立技术批次测试任务。当前所有候选的完整细胞覆盖与独立培养映射均未证实。** 证据限制详见 [审计报告](audits/deep_audit.md) 与 [可用性矩阵](audits/availability.csv)。完整逐数据集清单见 [recommendations.csv](tables/recommendations.csv)。

## 优先采用（通过采用门槛后）

|候选|研究适用性|已获证据|采用门槛|
|---|---|---|---|
|sciPlex3|可固定背景/剂量/时间、比较重复及板层级，并研究生物效应保真|188药、两rep、52板、每板2 vehicle设计样本；严格条件跨两组|完整cell-to-hash映射与QC细胞数；将rep标签与原文生物学重复及下游建库/run对应；不要把不同时间当batch|
|MIX-seq|同药跨实验有真实作者对照映射，可检验有限条件的外部实验泛化|Trametinib24h在expt1/expt3，两个实验均有DMSO设计|共同细胞系、同剂量、培养/pool/库映射；实验差异若含生物背景，另设背景泛化任务|
|OP3 PBMC|官方schema有plate、well、donor、dose、time，可同时检验技术与生物因素|144 compounds/24h/3 donors；DMSO与positive controls分开|完整obs；供体内跨plate共同药物与DMSO；plate/library不能被donor完全代替|

这三个是不同研究/不同实验流程，可作为“质量指标→策略选择”的跨资源验证候选。主分析应先在每个背景内部进行。只有两个独立重复的设计，对多层嵌套选策略支持有限；需要跨多个条件/资源验证，而不是把细胞bootstrap当新增实验重复。

## 可作补充

Norman2019适合作遗传组合预测参照；GSE206741 CPA组合药物、sci-Plex G×E与Frangieh适合作组合/刺激保真任务。Kang、Hagai、Zhao、Shifrut、Nadig适合作跨供体/细胞系/物种泛化，但这些背景不能作为应消除的技术batch。Papalexi适合扰动效力/未响应细胞的质量问题；Tian2019/2021覆盖神经元遗传模式；Dong/CINEMA-OT提供组合IFN机制分析；VCC提供新挑战任务；sciPlex2可在同家族作小剂量设计补充，不能算新独立资源。

补充类别不证明技术batch可用；逐项门槛和未知字段保留在CSV。单细胞RNA作为核心，protein/ATAC可作额外读出，不能替代RNA响应训练数据。

## 暂不适合（当前选定子集/用法）

当前Aissa/pertpy PC9多时间子集暂不直接作纯技术batch主数据：时间响应、样本/建库可能混杂，未核实每时间点匹配未处理对照。原研究其他multirep/组合药子研究有价值，需另审计，不能把一个子集结论推广到全研究。

同时明确排除以下用法：把Replogle K562与RPE1作为要消除的技术batch；把Kang/OP3 donor作为纯技术batch；把Hagai species或sciPlex24/72h作为技术batch；把同一原细胞群不同guide/条码或多个cell当独立实验重复。这是对使用方案的否定，不是认定数据本身无价值。

## 信息不足

Replogle2022 K562 GWPS/essential、RPE1仍保留为重点遗传候选，但gem_group重命名不能解决独立批次定义。Tahoe有独立Parquet和重复sample定义、被State实际采用，值得获取小metadata后升级；当前版本/访问与层级关系未解决。Parse刺激覆盖丰富、State训练证据明确，但正式card/技术重复未核实。Jiang24的遗传×五刺激有benchmark使用证据，原论文、counts及技术层级仍缺。Gasperini原文已找到32 lane在RT后分两批的建库设计，优先取得lane→批次及细胞映射；仍属信息不足是因为实际共同条件/对照数未核实。Adamson、Dixit、Xie、sciPlex4需要验证面板、MOI、时间、背景与batch重叠；不能因未找到记录认定没有批次效应。

## 采用前的研究决策

第一道门槛是可识别性：同条件跨独立技术组、训练/测试均有匹配对照；完全混杂不能靠更大的细胞数弥补。第二道门槛才是表达质量：在matched controls中测批次强度，同时检查同扰动重复一致性与生物信号保真。最后在外层留batch评测策略，而非用测试结果倒选最佳校正。

本轮不建议马上选“校正最强”的方法，不训练模型；先解决候选的实验层级与细胞覆盖。
'''
(R/'recommendations.md').write_text(text)
(R/'non_core_resources.md').write_text(f'''# 核心之外的资源

以下不计入候选扰动数据家族数。目录中的名称不能自动作为独立研究来源。

|资源/数据类型|与本研究的关系|分类与证据|
|---|---|---|
|CELLxGENE/Human Cell Atlas/Tabula Sapiens普通图谱|可作为预训练背景、细胞注释参考；通常缺少明确干预-对照配对|普通图谱另列；需要逐study确认干预，不能与扰动训练数据混称|
|scGPT whole-human等预训练语料|作者README称33 million normal human cells；是representation pretraining|{ref('scgpt_primary_readme','scGPT Model Zoo','33 million')}；具体Norman等预测任务fine-tuning不能与这个正常细胞语料混为一谈|
|Arc scBaseCount|通用公共scRNA再处理汇编，可能同时包含观察与干预研究|{ref('arc_atlas_scBaseCount','Arc官方scBaseCount说明')}；逐原study筛选，不能整包作为一个独立扰动实验；评估预训练泄漏时按原study/样本追溯|
|Arc Virtual Cell Atlas|scBaseCount/Tahoe/VCC汇编入口|{e('E22')}；包含观察和扰动数据；Tahoe/VCC已在核心候选单列，不能重复计来源|
|Haber普通regions/atlas子集|没有明确感染条件的区域图谱不属于干预训练|pertpy `haber_2017_regions`与感染候选区别；只有干预/对照子集可以进入核心|
|Datlinger2021四细胞系scifi混样演示|有技术preindexing重复，但示例纯混样不是扰动响应预测|{e('E06')} `datlinger_2021`；全论文也有CRISPR筛选，需准确定位那个子实验，不能据纯图谱示例算干预数据|
|Weinreb LARRY / Schiebinger developmental trajectory|CellOT包含state-fate；time、lineage和培养条件不能自动当perturbation/technical batch|{e('E03')} 与 `configs/tasks/statefate.yaml`；若使用明确cytokine intervention子集，另核查matched control；本轮不把整体trajectory当核心干预资源|
|Schraivogel TAP-seq targeted panels|有干预，但只测目标转录本，RNA质量指标/全转录组预测受限|{e('E06')}；作为针对性补充，不能与全转录组矩阵直接比较HVG/全基因响应|
|CellOT 4i / Frangieh protein-only|蛋白成像/ADT读出不等于scRNA|{e('E03')}；RNA部分已另列，纯蛋白数据不计核心|
|LINCS/CMap L1000、bulk RNA-seq|药物签名、外部先验、药物选择来源|OP3 compounds来源LINCS不意味着OP3是bulk；L1000本身不计单细胞RNA核心|
|scPerturb/pertpy/GEARS/PerturBench处理副本|是再处理、子集、统一元数据，不是新实验|按family_id追溯原数据；不同QC/HVG/均衡抽样版本的细胞/条件数不能相加|

模型角色仅按读过的作者代码/配置描述。SE/scGPT等embedding预训练、ST预测训练、fine-tuning、heldout评估需分开；“loader支持”不是“原论文采用”。
''')
(R/'open_questions.md').write_text('''# 未解决问题与下一步核实途径

这些是尚未完成的工作，不是“没有批次效应”的结论。联网失败后没有把未知补成确定事实；完整记录见 `access_log.jsonl`。

|优先级/对象|需要的文件或说明|核实问题|无需大矩阵的首选路径|
|---|---|---|---|
|P1 sciPlex3|GSM4150378 `colData(cds)`/cell metadata，含cell/hash/culture_plate/replicate/RT/ligation/PCR及QC|原文已支持生物学重复；rep1/2如何映射培养日期/lot？index plates是否嵌套或跨培养plate？测序run如何映射？|GEO单独cellMetadata文件；作者导出obs；若只提供RDS，先HEAD记录大小，再请求小导出|
|P1 MIX-seq|Figshare10298696 file listing、每实验cell_info/metadata及sample设计|expt1/3共有细胞系、Trametinib24h剂量与培养pool是否相同？每库对照？|API文件列表后只下载cell metadata；Taiga内部凭据不是公开获取前提|
|P1 OP3|GSE279945完整scRNA obs、plate/well/pool/library/run设计表|供体内同药是否跨plate重复？每plate DMSO？positive controls是否和药物一起保留？|全obs导出，不以de_train.uns[single_cell_obs]训练子集替代整个实验|
|P1 Replogle K562/RPE1|各原raw_singlecell文件obs、gem_group→culture/sample/library/run映射|同gene和同guide跨GEM覆盖；GEM独立培养还是同pool拆库？essential day6/7到底是什么？|GWPS官方metadata或作者obs导出；分开GWPS/essential/RPE1|
|P2 Norman|GSE133344 raw/filtered cell_identities.csv.gz及experiment/sample表|哪些列记录独立技术batch？组合是否跨重复？control如何定义？|直接小metadata；若缺batch字段，向原作者核实sample linkage而非条码后缀推断|
|P2 Frangieh|SCP1064 RNA metadata及病人模型/plate/library表|KO/i机制注释；750guide与249标签关系；各背景NT与技术重复覆盖|SCP独立metadata；必要时作者导出RNA obs，raw sequencing DUOS授权另谈|
|P2 sci-Plex G×E|hashTable、hash_sample_sheet、QC cell obs、实验原文|plate_id物理含义；GxE1/2/细胞背景嵌套；NA是否未分配而非control？|hash长表先查大小；请求去歧义cell-to-sample映射，不能每hash行当一细胞|
|P2 Parse|准确原resource card、release及plate/library/sample obs|全资源供体/刺激数、dose/time、供体内技术重复、匹配对照|官方数据目录/作者小obs；State配置只证明采用，不证明原设计|
|P2 Tahoe|当前Parquet元数据文件清单与大小、plate/sample/sublibrary映射|sample重复是独立培养吗？同line/drug/dose跨plate？pass_filter子集控制覆盖？|官方Parquet或经确认镜像；当前Marketplace有订阅/计费前提，本轮未执行相关操作|
|P2 VCC/Nadig/Jiang|准确论文/正式card、release、完整obs与实验层级|原数据身份和发表状态；baseline/NT/control含义；batch与biology分离|VCC Parquet/CSV、Nadig作者obs、Jiang作者metadata导出；计数摘要不是细胞metadata|
|P3其余遗传/药物候选|GEO原研究设计/批次表/补充材料|guide/目标数、原研究与processed数口径、独立重复|先用目录定位原论文再按相同审计标准下载小表|

文献补全：Nature/Cell/Science/PMC/EuropePMC/DOI解析目前多数受代理限制。优先打开每行paper_url的Methods、Data availability、Supplementary sample tables；正式出版状态以原期刊为准，不用仓库名年份或旧目录Year/Date of Submission代替。

网络下一步：可在环境网络设置允许所需官方域名，详见 `required_domains.txt`。这不是宣称配置已更新；本轮未修改网络草稿或发布环境。恢复访问后先运行 `python research/scripts/probe_access.py`，每次重试记录状态；只取小metadata。论文/下载链接不一致，保留差异并向作者核实，不能静默换版本。

大型文件：本轮对OP3 h5ad、Frangieh h5ad、G×E RDS、Jiang RDS只发HEAD，代理拒绝，因此文件大小**未知**。不能把未知写成0或估算GB。理由是metadata可能嵌在容器内；替代途径是独立obs/Parquet/作者导出，或服务器支持range时仅读取obs（先验证协议和元数据大小）。本轮没有尝试全量容器读取。唯一被大小上限拒绝的55,119,282-byte对象是benchmark汇总结果CSV，不是表达矩阵，已从默认下载禁用。

尚需表达矩阵才能验证：实际批次强度、测序深度/genes/mt分布、匹配对照的表达差异、同扰动重复一致性、校正是否丢失真实扰动响应。尚需模型实验才能验证：训练前指标是否预测某校正策略的训练/泛化收益。这两项均未在本轮运行。
''')
print('Built recommendations, non-core list, unresolved questions')
# Record observed use in public result tables. These tables are NOT cell metadata.
import pandas as pd
usage=[]
for ident,scenario in [('scperturbench_cellular_ood_performance_top100','cellular-context OOD evaluation'),('scperturbench_all_dataset_chemical','chemical perturbation evaluation'),('scperturbench_genetic_single_performance_top100','genetic single perturbation evaluation'),('scperturbench_genetic_combo_performance_top100','genetic combination evaluation')]:
 source=byid[ident];d=pd.read_csv(R/source['path'])
 for label,group in d.groupby('DataSet'):
  usage.append(dict(benchmark='scPerturBench',dataset_label=label,scenario=scenario,methods_in_result_records=';'.join(sorted(group['method'].astype(str).unique())),role='benchmark evaluation; per-method training/fine-tuning details not inferred from result records',source_url=source['url']))
pd.DataFrame(usage).to_csv(R/'tables/observed_benchmark_usage.csv',index=False)
unmapped=['Replogle_exp6','Replogle_exp7','Replogle_exp8','Schmidt','Wessels','Afriat','Parekh','TCDD']
pd.DataFrame([dict(dataset_label=label,original_source_status='not_resolved',counted_as_independent_family=False,next_step='Read benchmark data-cards/preprocessing and resolve original accession before inclusion; do not infer batch or family from this label') for label in unmapped]).to_csv(R/'tables/unmapped_benchmark_labels.csv',index=False)
with (R/'open_questions.md').open('a') as f:
 f.write('\n额外发现但未归源的benchmark标签见 `tables/unmapped_benchmark_labels.csv`：Replogle_exp6/7/8、Schmidt、Wessels、Afriat、Parekh、TCDD。公开结果证明采用，但原研究身份/具体版本尚未核实，未为凑数计作新的独立来源，也未把exp后缀当技术batch。\n')
with (R/'audits/deep_audit.md').open('a') as f:
 f.write('\n公开benchmark结果还明确出现Replogle_K562essential/RPE1essential、TianActivation/Inhibition、Papalexi、Frangieh、Adamson、Norman等标签，采用证据见 `tables/observed_benchmark_usage.csv`。这比loader支持更强，但仍不能从结果表推断每方法训练/微调协议或模糊exp标签的原研究身份。对应下载文件为冻结来源，未读取其分数来替代本研究的模型验证。\n')
print('Built observed benchmark adoption and unresolved-label tables')

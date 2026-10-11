# 数据年份、规模、文件大小与模型训练用途

更新日期：2026-10-11（UTC）。覆盖32个条目；同源子集分别列出。完整字段见 [CSV](dataset_year_size_models.csv) / [JSON](dataset_year_size_models.json)。

“年份”分为论文在线发表、卷期年份、数据首次公开和后续版本日期；未核实的数据发布日期不使用论文年替代。旧scPerturb目录Year列有混合提交时间问题，没有直接采用。多数非原文年份来自文献引用，证据级别和链接在CSV。

“规模”是细胞数/特征数及对应版本；notebook输出是作者保存的历史记录，不是本轮读矩阵计算，也不是模型训练折细胞数。特征数是文件列数，不自动等于去重后的基因数。原研究、benchmark筛选子集和train split不能混用。

表达文件大小目前只有sciPlex3旧下载日志提供精确值：2,456,030,368 bytes，约2.456 GB/2.287 GiB。本轮没有下载该表达矩阵，不能保证当前版本大小相同。其他未知不填0，不按细胞数估算。PDF大小与表达数据大小分开。

下表只把有作者教程、专用训练配置或明确脚本的模型写进训练/微调栏；完整 [模型关联与角色证据](dataset_model_training_evidence.csv) 记录来源和定位。其余仅有benchmark结果的模型仍见 [已有评测采用](observed_benchmark_usage.csv)，不能直接称为训练。

|数据集|论文年份/日期（非数据首次公开日）|规模与版本|训练/微调用途|
|---|---|---|---|
|Adamson UPR Perturb-seq|2016|pertpy 文档：UPR screen 约65,000；epistasis 约15,000；不是 GEARS 实际训练数|GEARS：训练与留出扰动测试；scGPT：微调与测试|
|Dixit Perturb-seq|2016|pertpy 文档约200,000，六个 screen 总体；GEARS 子集数量未知|GEARS：训练与留出扰动测试|
|CROP-seq Jurkat TCR|2017|pertpy 文档5,905高质量且唯一gRNA细胞|未取得数据集专用训练/微调证据；已有benchmark记录或整合收录另见采用列|
|Norman CRISPRa genetic interaction screen|2019|CPA教程：111122细胞×5044特征（全部split对象）|GEARS：训练与留出扰动测试；CPA：训练与测试；scGPT：可配置微调；另有benchmark评测记录；CPA（PerturBench实现）：benchmark训练与测试配置；Linear Additive：benchmark训练与测试配置；Latent Additive：benchmark训练与测试配置；biolord（PerturBench实现）：benchmark训练与测试配置|
|Replogle genome-scale Perturb-seq — K562 genome-wide|2022|存档同名adata输出819400和1989578细胞（均8248特征）；变更过程不明，未选定唯一规模|未取得数据集专用训练/微调证据；已有benchmark记录或整合收录另见采用列|
|Replogle genome-scale Perturb-seq — K562 essential|2022|本轮未读取该子集obs；不以整篇 >250万细胞替代子集数|未取得数据集专用训练/微调证据；已有benchmark记录或整合收录另见采用列|
|Replogle genome-scale Perturb-seq — RPE1 essential|2022|本轮未读取该子集obs；不以整篇 >250万细胞替代子集数|未取得数据集专用训练/微调证据；已有benchmark记录或整合收录另见采用列|
|sci-Plex — small screen|2019-12-05在线；2020-01-03卷期|未知；本轮未核实|未取得数据集专用训练/微调证据；已有benchmark记录或整合收录另见采用列|
|sci-Plex — large screen|2019-12-05在线；2020-01-03卷期|原论文/QC后649340细胞；PerturBench下载对象799317×110984，处理后183856×9198；版本差异未闭合|chemCPA：从头训练；或LINCS预训练后微调；留药物测试；CellOT：任务内训练与测试；CPA（PerturBench实现）：benchmark训练与测试配置；Linear Additive：benchmark训练与测试配置；Latent Additive：benchmark训练与测试配置；biolord（PerturBench实现）：benchmark训练与测试配置|
|sci-Plex — HDACi rescue|2019-12-05在线；2020-01-03卷期|未知；本轮未核实|未取得数据集专用训练/微调证据；已有benchmark记录或整合收录另见采用列|
|CPA combination-drug sci-Plex (combosciplex)|2023|CPA教程：63378细胞×5000特征|CPA：训练与测试|
|Kang demuxlet IFN-β PBMC|2018|CPA教程：13576细胞×5000特征（不是GEO全研究）|CPA：训练与测试；CellOT：任务内训练与测试；trVAE：benchmark训练与测试|
|Hagai cross-species innate immune stimulation|2018|未知；本轮未核实|CellOT：任务内训练与测试|
|MIX-seq|2020|本轮未读取cell metadata，不以各实验相加给精确细胞数|未取得数据集专用训练/微调证据；已有benchmark记录或整合收录另见采用列|
|Perturb-CITE-seq melanoma immune evasion|2021|PerturBench输入存档输出218331细胞×23712特征；不等于最终训练折|CPA（PerturBench实现）：benchmark训练与测试配置；Linear Additive：benchmark训练与测试配置；Latent Additive：benchmark训练与测试配置；biolord（PerturBench实现）：benchmark训练与测试配置|
|ECCITE-seq / Mixscape THP-1|2021|未知；本轮未核实|GEARS：benchmark重新训练与测试；AttentionPert：benchmark训练与测试；scGPT：benchmark加载预训练权重后微调与测试|
|iPSC/neuronal CRISPRi CROP-seq|2019|每背景约20k测序；唯一guide QC后约8,400 neurons/15,000 iPSC（pertpy文档）|未取得数据集专用训练/微调证据；已有benchmark记录或整合收录另见采用列|
|Neuronal genome-wide CRISPRi/a follow-up CROP-seq|2021|文档98k CRISPRi/50k CRISPRa是loaded/input级数字；不作为QC最终细胞数|未取得数据集专用训练/微调证据；已有benchmark记录或整合收录另见采用列|
|Gasperini enhancer CRISPRi screen|2019-01-03在线；2019-01-10卷期|原论文两项at-scale实验合计254974细胞、5920候选enhancer；不同面板/MOI|未取得数据集专用训练/微调证据；已有benchmark记录或整合收录另见采用列|
|SLICE / primary T-cell CROP-seq|2018|未知；本轮未核实|未取得数据集专用训练/微调证据；已有benchmark记录或整合收录另见采用列|
|Mosaic-seq enhancer perturbations|2017|文档51,448 sgRNA-induced transcriptomes|未取得数据集专用训练/微调证据；已有benchmark记录或整合收录另见采用列|
|GBM acute-slice drug perturbation|2021|未知；本轮未核实|CellOT：任务内训练与测试|
|PC9 drug-tolerance time course|2021|pertpy Aissa2021子集：848 treated+756 control；不是全研究|未取得数据集专用训练/微调证据；已有benchmark记录或整合收录另见采用列|
|Open Problems / NeurIPS 2023 PBMC chemical perturbation|原研究论文发表日期未核实|整理notebook存档298087细胞×21265特征；输出与代码单元位置不一致，须原文件复核|CPA（PerturBench实现）：benchmark训练与测试配置；Linear Additive：benchmark训练与测试配置；Latent Additive：benchmark训练与测试配置；biolord（PerturBench实现）：benchmark训练与测试配置|
|sci-Plex G×E (McFaline-Figueroa 2024; benchmark alias McFaline23)|2024-01-25在线；2024-02-14卷期|原论文kinome screen：1052205细胞、14121 G×E组合、两次独立转导；PerturBench处理后存档输出111445×5666|CPA（PerturBench实现）：benchmark训练与测试配置；Linear Additive：benchmark训练与测试配置；Latent Additive：benchmark训练与测试配置|
|PerturBench Jiang24 cytokine × CRISPRi collection|未核实；Jiang2025书目存在，但与该下载版本的关联仍需核实|PerturBench合并输出1628476细胞×15476特征；不是最终训练折|CPA（PerturBench实现）：benchmark训练与测试配置；Linear Additive：benchmark训练与测试配置；Latent Additive：benchmark训练与测试配置|
|Tahoe-100M single-cell perturbation atlas|2025预印本；最终期刊日期未核实|官方README100,648,790 cells、1,344 samples；未本轮读取QC/obs；samples不是独立重复数|State Transition：预测模型训练与留出测试|
|CINEMA-OT PBMC interferon combinations|2022预印本；2023 Nature Methods|pertpy full dong_2023 9,209；example 1,000是子集，不可相加|未取得数据集专用训练/微调证据；已有benchmark记录或整合收录另见采用列|
|Haber intestinal infection intervention subset|2017|未知；本轮未核实|未取得数据集专用训练/微调证据；已有benchmark记录或整合收录另见采用列|
|Parse PBMC cytokine screen used by State (parse_final_concat)|原论文未核实；2025 State预印本已有使用证据|本轮不将俗称10M作为实测QC数|State Transition：预测模型训练与留出测试|
|Nadig multi-context Perturb-seq (Jurkat/HepG2)|2024是整合资源标签；原刊年份未核实|未读取obs，不给该子集精确数|State Transition：预测模型训练与留出测试|
|Arc Virtual Cell Challenge 2025 H1 hESC perturbation data|原研究论文发表日期未核实|官方README约300,000；train/val/test全挑战范围，非单一split实测数|State Transition：预测模型训练与留出测试|

补充说明：OP3竞赛数据是2023版本，VCC是2025版本；其余首次数据库公开日仍需官方记录。State的Parse/Tahoe/Replogle-Nadig用途是扰动预测模型State Transition训练，不能自动称为State Embedding预训练。Replogle-Nadig合并目录到2022各子集的对应未闭合，因此没有把State逐项写进GWPS/essential/RPE1的已确认训练栏。

chemCPA作者说明的LINCS预训练属于非单细胞的L1000资源，仍在核心扰动单细胞清单之外；sciPlex3用于后续微调或从头训练。scGPT加载已有模型权重后训练的条目明确标微调；作者教程当前默认Adamson，Norman分支支持不冒充该教程实际运行结果。

新增原文及批次结论见 [PDF阅读记录](../papers/reading_notes.md)。G×E原文2024年发表，不能沿用McFaline23别名当发表年；sciPlex在线2019、卷期2020，两者均保留。CINEMA-OT正式期刊引用已补为2023，但不是证明该数据用于预测模型训练。

可复现：`python research/scripts/build_year_size_usage.py`；读取本地冻结来源，不下载表达矩阵或训练模型。[各版本存档规模](version_size_observations.csv) 与 [表达文件大小证据](expression_file_sizes.csv) 保留所有差异。Replogle相邻存档输出互相不一致；OP3输出在注释单元下；这些数字需要实际文件复核，不能据此完成细胞级批次审计。

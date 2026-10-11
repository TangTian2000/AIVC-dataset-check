# 未解决问题与下一步核实途径

这些是尚未完成的工作，不是“没有批次效应”的结论。联网失败后没有把未知补成确定事实；完整记录见 `access_log.jsonl`。

|优先级/对象|需要的文件或说明|核实问题|无需大矩阵的首选路径|
|---|---|---|---|
|P1 sciPlex3|GSM4150378 `colData(cds)`/cell metadata，含cell/hash/culture_plate/replicate/RT/ligation/PCR及QC|rep1/2是否独立培养？index plates是否嵌套或跨培养plate？测序run如何映射？|GEO单独cellMetadata文件；作者导出obs；若只提供RDS，先HEAD记录大小，再请求小导出|
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

额外发现但未归源的benchmark标签见 `tables/unmapped_benchmark_labels.csv`：Replogle_exp6/7/8、Schmidt、Wessels、Afriat、Parekh、TCDD。公开结果证明采用，但原研究身份/具体版本尚未核实，未为凑数计作新的独立来源，也未把exp后缀当技术batch。

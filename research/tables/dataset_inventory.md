# 候选数据集总表（第一阶段）

审计日期：2026-10-11。32 个版本/子资源条目，28 个候选研究/资源家族；同一家族不计独立来源，正式原研究尚未核实者标为未知。覆盖遗传、药物、组合药物和免疫刺激。此前项目只有README，未发现已有调研可复用；Replogle K562/RPE1与sciPlex3均保留。

完整逐字段表见 [dataset_inventory.csv](dataset_inventory.csv) / [JSON](dataset_inventory.json)。未知不是不存在；公开链接不是本轮亲自读过数据文件。counts指UMI矩阵，raw reads另述；模型支持loader不等于原模型论文实际采用。

本表先保存，再进行统一深入审计。第一阶段筛选理由不是最终推荐；第二阶段结论见审计报告和推荐清单。论文全文/GEO/Zenodo受到代理限制时，结论限定为作者代码或整合代码证据。所有精确细胞数注明文档/版本/统计范围，未用细胞数推断独立实验重复。

|ID / 来源家族|背景与干预|采用证据与用途|进一步核查|
|---|---|---|---|
|adamson2016 / adamson2016|K562；CRISPRi|GEARS README 明列 adamson 为 paper dataset；原论文及使用版本需分开；scPerturBench公开genetic single结果DataSet=Adamson；GEARS 数据内训练/留出扰动测试；不是普通预训练；遗传单扰动泛化benchmark评测；各方法训练/微调细节须原脚本核验|否；扩展背景与扰动种类；先核实独立重复和对照|
|dixit2016 / dixit2016|K562；CRISPR-cas9|GEARS README：dixit 为 paper dataset；数据内训练/留出扰动测试|否；扩展背景与扰动种类；先核实独立重复和对照|
|datlinger2017 / datlinger2017|Jurkat cells (immune cancer)；CRISPR-cas9, TCR stim|scPerturb/pertpy 收录与 E-distance 分析；不能据此称预测模型常用；整合资源分析；训练/微调/预测测试未证实；预训练未证实|否；扩展背景与扰动种类；先核实独立重复和对照|
|norman2019 / norman2019|K562；单基因与双基因 CRISPRa|GEARS README + CPA Norman教程 + PerturBench Norman19 accessor；scPerturBench公开genetic combo结果DataSet=Norman；模型训练/单基因和组合留出测试；无预训练角色证据|是；组合预测的关键参照；先验证跨独立批次覆盖，不因常用而默认适合|
|replogle2022_k562_gwps / replogle2022|K562；CRISPRi|GEARS README v0.1.1明确支持K562 essential/RPE1；仅数据loader支持，不证明在原GEARS论文用于评估。GWPS loader未在README明确列出；可供下游训练；原GEARS发表实验中该子集角色未知；不是普通图谱预训练|是；大遗传筛选；需要证实guide跨GEM覆盖及GEM与培养重复关系|
|replogle2022_k562_essential / replogle2022|K562；CRISPRi|GEARS README v0.1.1明确支持K562 essential/RPE1；仅数据loader支持，不证明在原GEARS论文用于评估。GWPS loader未在README明确列出；scPerturBench公开genetic single结果DataSet=Replogle_K562essential；可供下游训练；原GEARS发表实验中该子集角色未知；不是普通图谱预训练；遗传单扰动泛化benchmark评测；各方法训练/微调细节须原脚本核验|随K562审计；大遗传筛选；需要证实guide跨GEM覆盖及GEM与培养重复关系|
|replogle2022_rpe1 / replogle2022|hTERT-RPE1；CRISPRi|GEARS README v0.1.1明确支持K562 essential/RPE1；仅数据loader支持，不证明在原GEARS论文用于评估。GWPS loader未在README明确列出；scPerturBench公开genetic single结果DataSet=Replogle_RPE1essential；可供下游训练；原GEARS发表实验中该子集角色未知；不是普通图谱预训练；遗传单扰动泛化benchmark评测；各方法训练/微调细节须原脚本核验|是；大遗传筛选；需要证实guide跨GEM覆盖及GEM与培养重复关系|
|sciplex2 / srivatsan2020|A549；drugs|sciPlex3：CPA/chemCPA、CellOT、PerturBench、scPerturBench；sciPlex2/4：目前仅整合资源采用，未证实预测常用；sciPlex3：数据内训练/留出药物、剂量或背景测试；sciPlex2/4预测用途未核实|随sciPlex家族审计；sciPlex3优先核查：同药跨replicate/plate，但plate与背景可能嵌套|
|sciplex3 / srivatsan2020|A549/K562/MCF7；drugs|sciPlex3：CPA/chemCPA、CellOT、PerturBench、scPerturBench；sciPlex2/4：目前仅整合资源采用，未证实预测常用；sciPlex3：数据内训练/留出药物、剂量或背景测试；sciPlex2/4预测用途未核实|是；sciPlex3优先核查：同药跨replicate/plate，但plate与背景可能嵌套|
|sciplex4 / srivatsan2020|A549/MCF7；drugs|sciPlex3：CPA/chemCPA、CellOT、PerturBench、scPerturBench；sciPlex2/4：目前仅整合资源采用，未证实预测常用；sciPlex3：数据内训练/留出药物、剂量或背景测试；sciPlex2/4预测用途未核实|随sciPlex家族审计；sciPlex3优先核查：同药跨replicate/plate，但plate与背景可能嵌套|
|lotfollahi2023_combo / lotfollahi2023|见 cell_type；具体细胞系须核实原元数据，不能直接继承sciPlex3；单药及组合药物|CPA combosciplex教程明确训练/组合预测；同名sciPlex4不能自动归为此新实验；CPA 训练/组合药物测试；不是预训练|否；组合药物适用；需要重复/对照设计核实，作为补充候选|
|kang2018 / kang2018|人PBMC/SLE患者；按IFN-β子集而非整研究；IFN-β刺激|CPA Kang教程；CellOT lupuspatients任务；scPerturBench kangCrossCell/kangCrossPatient结果；数据内训练/留出细胞类型或患者测试；这些是生物泛化|是；适合生物背景泛化补充；不能把donor当纯技术batch|
|hagai2018 / hagai2018|原代皮肤成纤维细胞/骨髓来源吞噬细胞，依子集；dsRNA、IFNB免疫刺激|CellOT configs/tasks/crossspecies.yaml；跨物种任务；具体原数据对应需要原文核对；训练/留出物种测试；不是技术批次泛化|否；扩展背景与扰动种类；先核实独立重复和对照|
|mcfarland2020 / mcfarland2020|200 different cell lines；drugs, CRISPR-cas9|scPerturBench cellular OOD结果含McFarland；原作者代码含predictive_model_compare；跨细胞背景训练/测试；原作者药敏关联分析另列|是；公开的跨实验matched-control逻辑，对批次外推有价值；覆盖不完整|
|frangieh2021 / frangieh2021|co-culture of melanoma and TILs；CRISPR-Cas9 + IFNγ/免疫共培养背景；KO机制待原文核验；RNA+surface proteins|PerturBench Frangieh21 curation/accessor明确采用；scPerturBench公开genetic single结果DataSet=Frangieh；模型训练/免疫背景与遗传扰动留出测试；不是基础模型预训练；遗传单扰动泛化benchmark评测；各方法训练/微调细节须原脚本核验|是；适合遗传×免疫刺激泛化；先确认技术批次不与背景完全混杂|
|papalexi2021 / papalexi2021|THP-1；CRISPR-cas9|scPerturBench README把Papalexi列作预置benchmark数据；需进一步定位确切split；scPerturBench公开genetic single结果DataSet=Papalexi；预测benchmark采用已证实；训练/测试边界本轮未读取；Mixscape原任务是扰动识别；遗传单扰动泛化benchmark评测；各方法训练/微调细节须原脚本核验|否；KO效力与质量指标研究的补充，不先认定适合batch外推|
|tian2019 / tian2019|iPSC derived neurons；CRISPRi|scPerturb/pertpy 收录与 E-distance 分析；不能据此称预测模型常用；整合资源分析；训练/微调/预测测试未证实；预训练未证实|否；跨分化背景补充；未找到技术批次复现证据|
|tian2021 / tian2021|human iPSC-derived neurons；CRISPRa|scPerturb/pertpy 收录与 E-distance 分析；不能据此称预测模型常用；scPerturBench公开genetic single结果DataSet=TianActivation/TianInhibition（模式一致，具体原文件版本待核验）；整合资源分析；训练/微调/预测测试未证实；预训练未证实；遗传单扰动泛化benchmark评测；各方法训练/微调细节须原脚本核验|否；同背景i/a比较；需解决文档口径冲突后再采用|
|gasperini2019 / gasperini2019|K562；CRISPRi|scPerturb/pertpy 收录与 E-distance 分析；不能据此称预测模型常用；整合资源分析；训练/微调/预测测试未证实；预训练未证实|原文补充核查；细胞级未完成；优先核实明确的RT后建库批次；需同guide组合和对照跨批次数量|
|shifrut2018 / shifrut2018|Primary Human T Cells；CRISPR-cas9, TCR stim|scPerturb/pertpy 收录与 E-distance 分析；不能据此称预测模型常用；整合资源分析；训练/微调/预测测试未证实；预训练未证实|否；原代T细胞补充；纯技术batch研究须另找供体内重复|
|xie2017 / xie2017|K562；CRISPR-cas9|scPerturb/pertpy 收录与 E-distance 分析；不能据此称预测模型常用；整合资源分析；训练/微调/预测测试未证实；预训练未证实|否；enhancer扰动补充；预测常用及技术重复证据不足|
|zhao2021 / zhao2021|glioblastoma, patient tissue；drugs|CellOT gbm task配置；原始对应由代码ZhaoSims2021映射支持；模型训练/跨patient测试；生物泛化|否；可作临床背景泛化补充；技术重复需原实验对应|
|aissa2021 / aissa2021|PC9（当前候选子集）；全研究含其他细胞/组织/xenograft；drugs|scPerturb/pertpy 收录与 E-distance 分析；不能据此称预测模型常用；整合资源分析；训练/微调/预测测试未证实；预训练未证实|否；疾病耐受时间任务补充；若没有时间匹配对照，暂不用于主批次实验|
|op3_2023 / op3_2023|3 healthy human donor PBMC，多细胞类型；小分子药物|NeurIPS competition；PerturBench OP3 accessor；scPerturBench KaggleCrossCell/Patient；competition用DE/pseudobulk标签训练/测试；PerturBench用scRNA矩阵训练/测试，两任务不同|是；plate、剂量、时间、donor有清晰字段，优先验证供体内技术batch是否有重复|
|mcfaline2023 / mcfaline2023|A172/T98G/U87MG等；各实验具体覆盖需元数据；CRISPRi × chemical；含sgRNA doublets组合映射|PerturBench McFaline23明确训练/数据规模实验；scPerturb提供GxE整合；遗传×药物训练/留出组合与背景测试|是；特别适合G×E与生物保真风险研究；纯技术batch仍须独立重复验证|
|jiang24 / jiang24|元数据cell_type；原模型/供体背景待核实；CRISPRi × IFNB/IFNG/INS/TGFB/TNFA条件|PerturBench Jiang24 accessor与step1/2 curation；模型训练/遗传×刺激/细胞背景留出测试；无预训练证据|是；刺激种类丰富；元数据设计未完整，先列信息不足|
|tahoe100m / tahoe100m|癌细胞系；具体版本背景数待官方card核实；药物扰动|State README明确Tahoe-100M-trained ST推理；tahoe_tomls/generalization.toml声明training和fewshot val/test；State Transition训练/药物×剂量留出测试；SE预训练角色未从配置证明|否；已证实新模型采用；metadata分离有利于审计，访问与技术层级仍待解决|
|dong2023 / dong2023|PBMC；IFNβ/IFNγ/IFNβ+IFNγ|原方法CINEMA-OT的因果响应分解/匹配分析；不是本轮已证实的预测训练benchmark；方法响应分析；预测训练/测试采用未知|否；小规模组合细胞因子资源，适合补充机制检查；独立批次不足证据|
|haber2017_infection / haber2017|小肠上皮；只将感染/未感染干预子集列作候选；感染刺激；不把regions图谱当扰动训练|scPerturBench cellular OOD结果DataSet=Haber；具体感染子集需复现代码核对；模型训练/细胞背景泛化测试；普通regions atlas另列|否；可补充体内免疫刺激；不适合作为已证实技术batch主数据|
|parse_cytokines / parse_cytokines|人PBMC；State配置存在多个donor和B细胞亚群；细胞因子刺激|State原作者state_preprint_toml_files/parse_tomls明确training=parse及fewshot val/test；State Transition模型训练/留出刺激测试；donor/celltype是生物背景；SE预训练用途未知|是（新增证据）；明确被新一代模型采用且刺激丰富；供体内技术重复是采用门槛|
|nadig2024 / nadig2024|Jurkat/HepG2；与Replogle2022 K562/RPE1亲缘但不是同原研究；遗传CRISPR；确切i/KO模式需原研究，不能从通用CRISPR字段推断|State README称Replogle-Nadig；replogle_nogwps_v2配置含Jurkat/HepG2/K562/RPE1；State合并遗传屏幕训练/背景及扰动留出测试；合并目录不能自动解释原数据来源|否；新模型常用多背景遗传补充；不能与Replogle2022合成纯技术batch|
|vcc2025 / vcc2025|H1 human embryonic stem cells；遗传目标扰动；官方README未说明KO/i，须原实验设计|State README有VCC训练教程；官方明确train/validation/held-out test；challenge训练/验证/留出扰动评测；技术batch留出不是既有challenge任务|否；代表性新benchmark值得补充；需要plate/library/replicate映射|

普通图谱、基础模型语料、bulk和其他模态见 [另列资源](../non_core_resources.md)，不计入上述家族数。

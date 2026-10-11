# 推荐清单

这些分级针对“批次效应、校正对扰动预测泛化的影响、训练前质量指标指导策略”的研究目的，不按细胞数或知名度排序。

**“优先采用”是条件性试点/核实优先级，不表示已具备可执行的独立技术批次测试任务。当前所有候选的完整细胞覆盖与独立培养映射均未证实。** 证据限制详见 [审计报告](audits/deep_audit.md) 与 [可用性矩阵](audits/availability.csv)。完整逐数据集清单见 [recommendations.csv](tables/recommendations.csv)。

## 优先采用（通过采用门槛后）

|候选|研究适用性|已获证据|采用门槛|
|---|---|---|---|
|sciPlex3|可固定背景/剂量/时间、比较重复及板层级，并研究生物效应保真|188药、两rep、52板、每板2 vehicle设计样本；严格条件跨两组|完整cell-to-hash映射与QC细胞数；证明rep标签代表独立培养/处理；不要把不同时间当batch|
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

Replogle2022 K562 GWPS/essential、RPE1仍保留为重点遗传候选，但gem_group重命名不能解决独立批次定义。Tahoe有独立Parquet和重复sample定义、被State实际采用，值得获取小metadata后升级；当前版本/访问与层级关系未解决。Parse刺激覆盖丰富、State训练证据明确，但正式card/技术重复未核实。Jiang24的遗传×五刺激有benchmark使用证据，原论文、counts及技术层级仍缺。Adamson、Dixit、Gasperini、Xie、sciPlex4需要验证面板、MOI、时间、背景与batch重叠；不能因未找到记录认定没有批次效应。

## 采用前的研究决策

第一道门槛是可识别性：同条件跨独立技术组、训练/测试均有匹配对照；完全混杂不能靠更大的细胞数弥补。第二道门槛才是表达质量：在matched controls中测批次强度，同时检查同扰动重复一致性与生物信号保真。最后在外层留batch评测策略，而非用测试结果倒选最佳校正。

本轮不建议马上选“校正最强”的方法，不训练模型；先解决候选的实验层级与细胞覆盖。

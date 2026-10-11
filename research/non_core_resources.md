# 核心之外的资源

以下不计入候选扰动数据家族数。目录中的名称不能自动作为独立研究来源。

|资源/数据类型|与本研究的关系|分类与证据|
|---|---|---|
|CELLxGENE/Human Cell Atlas/Tabula Sapiens普通图谱|可作为预训练背景、细胞注释参考；通常缺少明确干预-对照配对|普通图谱另列；需要逐study确认干预，不能与扰动训练数据混称|
|scGPT whole-human等预训练语料|作者README称33 million normal human cells；是representation pretraining|[scGPT Model Zoo](https://raw.githubusercontent.com/bowang-lab/scGPT/cebd6fae655b9c585a4807daa3ac31bb764f06b4/README.md#L20)；具体Norman等预测任务fine-tuning不能与这个正常细胞语料混为一谈|
|Arc scBaseCount|通用公共scRNA再处理汇编，可能同时包含观察与干预研究|[Arc官方scBaseCount说明](https://raw.githubusercontent.com/arcinstitute/arc-virtual-cell-atlas/4f7bb170c61d2fafce70f67db6e52c7d9af1be4b/scBaseCount/README.md)；逐原study筛选，不能整包作为一个独立扰动实验；评估预训练泄漏时按原study/样本追溯|
|Arc Virtual Cell Atlas|scBaseCount/Tahoe/VCC汇编入口|E22 [Arc官方数据迁移/Requester Pays说明](https://raw.githubusercontent.com/arcinstitute/arc-virtual-cell-atlas/4f7bb170c61d2fafce70f67db6e52c7d9af1be4b/README.md#L9)；包含观察和扰动数据；Tahoe/VCC已在核心候选单列，不能重复计来源|
|Haber普通regions/atlas子集|没有明确感染条件的区域图谱不属于干预训练|pertpy `haber_2017_regions`与感染候选区别；只有干预/对照子集可以进入核心|
|Datlinger2021四细胞系scifi混样演示|有技术preindexing重复，但示例纯混样不是扰动响应预测|E06 [pertpy数据文档与loader（整合方）](https://raw.githubusercontent.com/scverse/pertpy/a4c30738468f8cb6bed677efb9331a9e35a168bd/src/pertpy/data/_datasets.py#L29) `datlinger_2021`；全论文也有CRISPR筛选，需准确定位那个子实验，不能据纯图谱示例算干预数据|
|Weinreb LARRY / Schiebinger developmental trajectory|CellOT包含state-fate；time、lineage和培养条件不能自动当perturbation/technical batch|E03 [CellOT作者README / experiments](https://raw.githubusercontent.com/bunnech/cellot/522d2b953da8ad244fcf36f64521487fdf763788/README.md#L11) 与 `configs/tasks/statefate.yaml`；若使用明确cytokine intervention子集，另核查matched control；本轮不把整体trajectory当核心干预资源|
|Schraivogel TAP-seq targeted panels|有干预，但只测目标转录本，RNA质量指标/全转录组预测受限|E06 [pertpy数据文档与loader（整合方）](https://raw.githubusercontent.com/scverse/pertpy/a4c30738468f8cb6bed677efb9331a9e35a168bd/src/pertpy/data/_datasets.py#L29)；作为针对性补充，不能与全转录组矩阵直接比较HVG/全基因响应|
|CellOT 4i / Frangieh protein-only|蛋白成像/ADT读出不等于scRNA|E03 [CellOT作者README / experiments](https://raw.githubusercontent.com/bunnech/cellot/522d2b953da8ad244fcf36f64521487fdf763788/README.md#L11)；RNA部分已另列，纯蛋白数据不计核心|
|LINCS/CMap L1000、bulk RNA-seq|药物签名、外部先验、药物选择来源|OP3 compounds来源LINCS不意味着OP3是bulk；L1000本身不计单细胞RNA核心|
|scPerturb/pertpy/GEARS/PerturBench处理副本|是再处理、子集、统一元数据，不是新实验|按family_id追溯原数据；不同QC/HVG/均衡抽样版本的细胞/条件数不能相加|

模型角色仅按读过的作者代码/配置描述。SE/scGPT等embedding预训练、ST预测训练、fine-tuning、heldout评估需分开；“loader支持”不是“原论文采用”。

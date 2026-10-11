# 原论文PDF读取记录与结论修订

日期：2026-10-11（UTC）。已从作者实验室网站的GitHub公开存档下载并读取三篇原文。官网、PMC、bioRxiv、OpenReview的本轮GET仍遭代理隧道403；作者公开副本提供了可访问替代路径。来源完整commit、SHA-256和字节数见 [resources.json](../resources.json)。本轮阅读的是下面三篇，不能扩展为其他论文也已读。

|原论文|作者公开PDF|文件大小|确证的发表日期|论文规模|
|---|---|---|---|---|
|Srivatsan等，Massively multiplex chemical transcriptomics at single cell resolution|[作者副本](https://raw.githubusercontent.com/cole-trapnell-lab/cole-trapnell-lab.github.io/a7ead73c4da7190d05b4928ace5b67d457329114/pdfs/papers/srivatsan_mcfaline_ramani_sci-plex_Science_2019.pdf)|1,534,850 bytes|2019-12-05在线；2020-01-03 Science卷期|大型药物实验QC后649,340细胞；188药，4,992独立处理样本|
|McFaline-Figueroa等，Multiplex single-cell chemical genomics reveals the kinase dependence of the response to targeted therapy|[作者副本](https://raw.githubusercontent.com/cole-trapnell-lab/cole-trapnell-lab.github.io/a7ead73c4da7190d05b4928ace5b67d457329114/pdfs/papers/mcfaline-sci-plex-gxe.pdf)|8,619,150 bytes|2024-01-25 Published；2024-02-14 Cell Genomics卷期|kinome screen 1,052,205细胞；522 kinases、3,165 sgRNAs；14,121基因×环境组合，两次独立转导形成28,242条件|
|Gasperini等，A genome-wide framework for mapping gene regulation via cellular genetic screens|[作者副本](https://raw.githubusercontent.com/cole-trapnell-lab/cole-trapnell-lab.github.io/a7ead73c4da7190d05b4928ace5b67d457329114/pdfs/papers/gasperini-crispri.pdf)|8,243,231 bytes|2019-01-03 Published；2019-01-10 Cell卷期|两个at-scale实验合计254,974细胞、5,920候选enhancers|

上述MB级文件大小是**论文PDF大小**，不是表达矩阵大小。原文报告细胞数也不自动等于模型筛选后训练数据规模。

## sciPlex：原文明确支持生物学重复

- PDF第2页正文明确在重复培养板进行duplicate处理，并将药物及剂量在孔位置随机化；同页说明获得649,340个单细胞转录组。
- PDF第4页Fig.3A图注写明“in biological replicate”，对应三细胞系、188药、四剂量、24h；还说明药物与剂量位置在重复之间变化。
- PDF第2页剂量已目视核对：10 nM、100 nM、1 µM、10 µM。文本抽取将µ误呈现为m，不能据纯文本写成1/10 mM。
- PDF第6页明确在线发表日；页脚提供2020卷期日，不能只选一个年份抹掉差异。

**修订旧结论**：不再把“作者是否声明生物学重复/重复培养板”列为完全未知。论文证据与已下载样本表相互支持；但仍未取得完整细胞到样本的对应表。培养日期/试剂批号、索引板/建库/测序的细节及实际细胞覆盖尚未完整核实。不能把52个板解释成52次独立培养运行。

## sci-Plex G×E：独立转导与技术流程有明确描述

- PDF第7页（印刷正文第6页）kinome screen段落明确“across two independent transductions”；三种GBM细胞系、四药×两剂量或vehicle、72h。此独立性指转导层级，不自动证明每下游建库/测序run独立。
- PDF第22页（STAR Methods e4）说明部分实验跨重复/细胞系复用hash。复用同一hash的样本没有混在一起，而是放在不同RT孔；因此hash身份需要结合RT信息，不能只凭hash去重或给批次。
- 同页至下一页说明除kinome screen用4个RT板和4个连接板外，其他实验各用1个RT板和1个连接板。这些板是组合索引步骤，不等于培养重复数。
- PDF第23页（e5）说明PCR板标记及NextSeq 550、NextSeq 2000、NovaSeq平台；未给出每个细胞与各次测序run的完整对应，不能由平台名直接建立批次表。
- PDF第20页（e2）Data and code availability明确GSE225775、作者代码 `https://github.com/cole-trapnell-lab/sci-Plex-GxE`，代码归档v1.0.0 DOI `10.5281/zenodo.10293222`。代码版本号不是数据首次公开日期。
- PDF第15页明确Published: January 25, 2024；封面和页脚是February 14, 2024。作者网站写Cell Genomics (2023)，DOI也含2023，但不能覆盖PDF明确的2024发表日期。

**修订旧结论**：补上正式题名、2024发表年、GSE225775、作者代码和两次独立转导证据。仍需原细胞表建立“转导重复→培养处理→hash/RT→连接/PCR→测序”对应，核实同基因×药物×背景的实际数量。GxE1/GxE2文件名不能直接替代这两次转导重复。

## Gasperini：明确的建库处理批次值得升级核查

- 原文STAR Methods “Single cell transcriptome capture”（文本可检索该标题）说明规模实验使用32个10x lane，RT后分为两批，每批16个lane，完成其余制备步骤。
- 这给出了真正的技术批次定义：**RT之后的建库处理分批**。它不等于两次独立培养，也不能与不同MOI/面板的实验混为一谈。
- 原文差异表达方法还将`prep_batch`纳入Monocle2公式：`gRNA_group + guide_count + percent.mito + prep_batch`；作者报告回归这些因素略提高检测灵敏度。这证明该建库分批被实际纳入分析，但不是本轮测得的批次效应强度，也不是扰动预测泛化收益。
- 原文Data and software availability给出GSE120861；仍需逐细胞lane与这两批的映射，以及同guide组合/对照在两批中的实际数量。

**修订旧结论**：从只有一般批次线索升级为“已找到明确建库分批设计，优先取得lane→处理批次映射”。本轮没有证明该映射已公开，也未完成细胞级审计，因此仍不能直接宣布留批次任务可执行。

## 可复现与边界

`python research/scripts/fetch_resources.py` 可按冻结清单重新取得PDF，遵守25MiB单文件上限；`python research/scripts/extract_papers.py` 使用Poppler的`pdftotext -layout`重建文本。本环境已安装；新环境需要系统包`poppler-utils`。主要证据按PDF页码定位，抽取文本用于搜索，图表和特殊单位必要时查看PDF。

此次没有下载大型表达矩阵或训练模型；也没有取得Science独立补充PDF，G×E/Gasperini下载副本含STAR Methods，不能据此称全部补充数据表均已获取。此前“没有找到独立批次证明”的文字是旧状态，以本次原文修订为准。

PDF和全文文本是本地阅读缓存（`research/papers/`），不随成果提交到GitHub；GitHub保存原作者下载地址、哈希、阅读笔记和复现脚本。

# 下一步需要你处理的事项

> 2026-10-11（UTC）补充：已下载读取三篇原文，sciPlex生物学重复、G×E两次独立转导、Gasperini RT后两批建库已有直接证据；下文早期“未知”不再适用于这些已确认设计。最新逐项修订见[原文阅读记录](papers/reading_notes.md)、[审计报告](audits/deep_audit.md)；新增[32项年份、规模与模型用途表](tables/dataset_year_size_models.md)。完整细胞级映射及批次细胞数仍未取得。

日期：2026-10-11。当前瓶颈是资料访问与实验设计证据，不是计算资源。暂时不需要GPU，也不需要下载大表达矩阵。

## 1. 查看GitHub成果分支

成果已推送到 [research/perturbation-dataset-audit-20261011](https://github.com/TangTian2000/AIVC-dataset-check/tree/research/perturbation-dataset-audit-20261011)，查看 [成果入口](https://github.com/TangTian2000/AIVC-dataset-check/blob/research/perturbation-dataset-audit-20261011/research/README.md) 即可。默认main尚未合并，所以仓库默认首页仍会显示旧内容。你可以先审阅报告；如希望默认分支也显示成果，再通过 [分支比较](https://github.com/TangTian2000/AIVC-dataset-check/compare/main...research/perturbation-dataset-audit-20261011) 创建并合并PR。

本轮Git推送成功，无需为查看成果重新授权。GitHub CLI单独报告凭据无效，但没有阻碍分支发布；如之后需要用CLI管理PR，再处理该连接问题。不要把访问令牌贴到聊天或提交到仓库。

## 2. 允许访问官方文献与数据域名

此前16个代表性官方资料HEAD请求都遭代理403。请在云环境网络设置中允许 [required_domains.txt](required_domains.txt) 列出的文献和数据域名。优先恢复 `www.ncbi.nlm.nih.gov`、`ftp.ncbi.nlm.nih.gov`、`api.figshare.com`、`figshare.com`、`singlecell.broadinstitute.org`、`gwps.wi.mit.edu`、`doi.org` 和 `zenodo.org`。

修改后重新运行 `python research/scripts/probe_access.py` 验证实际访问；允许列表不代表文件一定存在或可以读取。恢复访问后即可继续取得小元数据、补全文献来源和计算真实细胞覆盖。

## 3. 若公开记录不足，向作者申请小元数据与设计说明

优先申请sciPlex3、MIX-seq、OP3，保留Replogle K562/RPE1为遗传候选。每个数据集的具体文件与问题见 [open_questions.md](open_questions.md)。可使用下面的请求内容，按数据集删去不适用字段：

> 我们研究技术批次校正对单细胞扰动预测训练与泛化的影响，希望取得无需表达矩阵的完整细胞元数据，以及实验单元的对应表。所需字段包括原细胞ID、扰动/guide与阴性对照标记、剂量、时间、细胞系/供体/细胞类型、培养或处理重复、板/孔、pool/hash、建库/GEM及测序run。请说明各层级的嵌套关系，以及重复是否为独立培养/处理。我们尤其需要确认相同扰动在相同生物背景、剂量和时间下是否跨独立技术批次重复，且每批次有匹配对照。CSV/TSV/Parquet或AnnData obs导出即可；本阶段不需要表达矩阵。

没有batch字段时，应请求样本对应表与实验说明，不能仅靠条码后缀补出批次。此模板仅供你使用，本轮没有发送任何对外消息。

## 4. 根据补齐后的证据决定主数据

先检验独立技术批次的定义、同条件跨批次重复、训练/测试两侧匹配对照与QC后细胞覆盖。通过门槛的资源才进入主研究；若只能证明同一pool拆库，测试任务只能声称建库层级泛化。若完全混杂，则改为明确的生物背景泛化补充任务或更换资源。

完成这些后再决定表达下载与模型实验：先在匹配对照中测实际批次强度，检查扰动重复一致性与生物信号保真，再用外层留批次评测质量指标是否指导校正策略。策略选择不能使用最终留出批次的结果。

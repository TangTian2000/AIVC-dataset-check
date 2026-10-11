# 单细胞扰动数据与批次研究调研

日期：2026-10-11。成果是有证据分级的筛选与设计审计；完整细胞级审计仍被资料访问与元数据缺失阻断。未下载大型表达矩阵，未训练模型，未更新或发布环境配置。

- [数据集总表](tables/dataset_inventory.md)：32个版本/子资源条目，28个候选研究/资源家族；完整字段见 [CSV](tables/dataset_inventory.csv) 或 [JSON](tables/dataset_inventory.json)。同源子集不当独立来源，预测采用与仅整合资源收录分开。
- [深入审计报告](audits/deep_audit.md)：统一核查10个候选；包含层级、混杂、对照、跨批次可行性与证据链接。
- [已取得信息、具体发现与缺口对照表](audit_progress_summary.md)：覆盖全部32条，并解释“完整设计”和“跨批次覆盖”。
- [分级推荐](recommendations.md)：优先采用、可作补充、暂不适合、信息不足；优先类均为条件性建议，未证明可直接开展技术batch留出。
- [真实计算与未完成状态](audits/availability.csv)：设计表已计算；细胞数量跨表未计算。
- [下载的元数据和用法](metadata/README.md)、[设计热图PNG](figures/sciplex3_sample_design.png) / [PDF](figures/sciplex3_sample_design.pdf)：图与统计都是设计样本，不是细胞/表达批次效应。
- [未解决问题与核实途径](open_questions.md)、[核心之外资源](non_core_resources.md)。
- [证据索引](sources/evidence_index.csv)、[冻结来源索引](sources/source_index.csv)、[下载记录](download_log.jsonl)、[网络记录](access_log.jsonl)。
- [benchmark实际采用记录](tables/observed_benchmark_usage.csv)、[尚未对应原研究的标签](tables/unmapped_benchmark_labels.csv)、[交付验证](verification.md)。

当前项目起初只有标题README，没有找到此前调研文件。Replogle K562、RPE1与sciPlex3均保留，未否定任何未见到的既有结论。第一阶段先保存29条/25家族；找到State与Arc明确新证据后再增补Parse、Nadig、VCC，最终略超过约15–25的初步目标。新条目因实际模型采用或官方challenge设计纳入，不因规模凑数。`dataset_inventory_stage1.*`保存早期范围快照；引用以最终表和证据索引为准。

“正式名称/原论文/发表状态”未核实的字段写未知，未用仓库年份猜出版；公开URL不代表已读取数据；metadata字段名不等于批次物理含义。所有文档明确区分原作者说明、整合代码、设计表计算、有条件推测和未知。

## 关键结果

sciPlex3有4,992处理样本、188种药、52培养板hash标签与两个replicate标签，每板2个vehicle样本；24h三背景，72h仅A54947药。严格背景/剂量/时间条件有跨rep设计，但完整cell-to-hash及独立培养证明尚缺。MIX-seq作者声明Trametinib24h跨expt1/3，并指定DMSO参照；OP3官方schema有plate/donor/dose/time，值得核实供体内技术重复。

本轮79个经审阅来源/metadata对象中，78个已存盘并冻结SHA-256；一个55MB benchmark结果CSV因上限而禁用（不是表达矩阵）。官方外部资料的16个代表性HEAD访问检查均遭代理403，文件大小保持未知。GitHub作者源码可读，因此仍完成了上述独立工作。

## 复现

当前Python3.12环境已有依赖；版本在 requirements.txt。使用新的本地环境时，按该文件安装，保持TLS和默认代理配置，不需要模型/GPU依赖。

```bash
cd /workspace/AIVC-dataset-check
# 只在需要重新取来源时运行；默认仅已审阅且<=25MiB的对象：
python research/scripts/fetch_resources.py
# 对本地冻结输入离线重新生成表/报告/图并运行语义检查：
bash research/scripts/run_all.sh
```

不运行benchmark模型代码。下载脚本不会自动访问大型表达容器；每个正文有25MiB硬上限，预期hash不符时失败并保留原文件。后续网络核查用 `python research/scripts/probe_access.py`（HEAD-only；失败返回非零，完整记录）。

真实cell metadata入口见metadata说明，当前schema模板故意不包含batch证据，不能直接用于宣称某列是独立批次。6个测试验证严格条件、背景匹配、剂量/时间混杂和设计数闭式核对；synthetic测试不属于数据集实测结果。

未完成的核心项是10个候选的完整obs、实验层级与QC后细胞覆盖，以及部分原论文/正式出版信息。访问恢复后从小metadata继续；需大RDS/h5ad才能取obs时先查大小并请求独立导出，本轮不下载这些表达容器。

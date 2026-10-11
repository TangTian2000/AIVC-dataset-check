#!/usr/bin/env python3
"""Build version-specific year, size and model-use evidence from frozen sources.

Notebook outputs are quoted historical observations, never a local matrix audit.
"""
import csv
import json
import re
from pathlib import Path

R = Path(__file__).resolve().parents[1]
inventory = json.loads((R / 'tables/dataset_inventory.json').read_text())
sources = {x['id']: x for x in json.loads((R / 'resources.json').read_text())}
by_path = {x['path']: x for x in sources.values()}


def url(key):
    return sources[key]['url']


def write_csv(name, rows):
    with (R / 'tables' / name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def output_text(cell):
    strings = []
    for out in cell.get('outputs', []):
        for value in [out.get('text', ''), out.get('data', {}).get('text/plain', '')]:
            strings.append(''.join(value) if isinstance(value, list) else value)
    return '\n'.join(strings)


# Explicitly reviewed output locations; zero-based notebook cell indices.
specs = [
    ('norman2019', 'cpa_Norman.ipynb', 8, 'CPA教程载入对象；不是训练折单独细胞数', ''),
    ('kang2018', 'cpa_Kang.ipynb', 9, 'CPA教程载入对象；不是GEO全研究或训练折单独细胞数', ''),
    ('lotfollahi2023_combo', 'cpa_combosciplex.ipynb', 8, 'CPA组合药物教程载入对象；所有split合计', ''),
    ('frangieh2021', 'perturbench_curate_Frangieh21.ipynb', 2, 'PerturBench整理输入对象', ''),
    ('jiang24', 'perturbench_curate_Jiang24_step2.ipynb', 8, 'PerturBench五刺激文件合并后的保存输出', '不是最终训练集大小'),
    ('mcfaline2023', 'perturbench_curate_McFalineFigueroa23_step2.ipynb', 21, 'PerturBench合并/早期整理对象', ''),
    ('mcfaline2023', 'perturbench_curate_McFalineFigueroa23_step2.ipynb', 29, '每perturbation×cell_type×treatment至少20细胞后', ''),
    ('mcfaline2023', 'perturbench_curate_McFalineFigueroa23_step2.ipynb', 41, '去除temozolomide/thioguanine后', ''),
    ('mcfaline2023', 'perturbench_curate_McFalineFigueroa23_step2.ipynb', 42, 'preprocess打印的处理后对象', '不能与原论文kinome screen总规模直接等同'),
    ('sciplex3', 'perturbench_curate_Srivatsan20.ipynb', 4, 'scPerturb h5ad被PerturBench载入时', '与原论文649340不同；文件版本/QC差异未完全追溯'),
    ('sciplex3', 'perturbench_curate_Srivatsan20.ipynb', 35, '三细胞系、最高剂量/对照选择并preprocess后的对象', '不是原论文全数据或单独训练折'),
    ('op3_2023', 'perturbench_curate_op3.ipynb', 1, 'OP3整理notebook保存的对象输出', '输出保存在注释单元下；随后读文件单元没有同样输出，须原文件复核'),
    ('replogle2022_k562_gwps', 'scperturb_replogle_handling.ipynb', 3, 'GWPS处理notebook保存的adata输出A', '相邻adata输出为1989578；缺少两者之间变更代码，不认定最终版本'),
    ('replogle2022_k562_gwps', 'scperturb_replogle_handling.ipynb', 4, 'GWPS处理notebook保存的adata输出B', '相邻adata输出为819400；不可推断版本关系或选一个作唯一规模'),
]
observations = []
for dataset, name, index, scope, caveat in specs:
    path = 'sources/' + name
    nb = json.loads((R / path).read_text())
    text = output_text(nb['cells'][index])
    match = re.search(r'n_obs [×x] n_vars = (\d+) [×x] (\d+)', text)
    if not match:
        raise ValueError(f'Expected archived shape absent: {name} cell {index}')
    observations.append(dict(dataset_id=dataset, version_scope=scope,
                             n_cells=int(match[1]), n_features=int(match[2]),
                             evidence='作者/benchmark存档notebook输出；本轮没有下载或复算表达矩阵',
                             source_url=by_path[path]['url'], locator=f'Notebook Cell {index} (zero-based)',
                             caveat=caveat or '存档输出可过时；需要精确匹配实际下载版本'))
write_csv('version_size_observations.csv', observations)

uses = []


def use(dataset, model, role, scope, keys, locator, level):
    uses.append(dict(dataset_id=dataset, model=model, role=role, version_scope=scope,
                     evidence_level=level, source_urls=' ; '.join(url(k) for k in keys), locator=locator))


for ds in ['adamson2016', 'dixit2016', 'norman2019']:
    use(ds, 'GEARS', '训练与留出扰动测试', 'GEARS论文/示例使用版本；细胞数不能继承原研究总数',
        ['gears_README_md'], 'Datasets used in paper / Core API', '模型作者明确采用')
for ds, nb in [('norman2019', 'cpa_Norman_ipynb'), ('kang2018', 'cpa_Kang_ipynb'),
               ('lotfollahi2023_combo', 'cpa_combosciplex_ipynb')]:
    use(ds, 'CPA', '训练与测试', '当前作者教程对应版本；不自动等同原论文全部实验',
        [nb], 'setup_anndata / model.train / prediction', '作者可执行教程及存档输出')
use('adamson2016', 'scGPT', '微调与测试', '作者Tutorial_Perturbation默认data_name=adamson；加载scGPT_human',
    ['year_scgpt_perturbation'], 'Cells 3, 5, 6, 8, 10', '作者微调教程')
use('norman2019', 'scGPT', '可配置微调；另有benchmark评测记录', '教程有norman配置分支，当前默认执行Adamson',
    ['year_scgpt_perturbation', 'scperturbench_genetic_combo_performance_top100'], 'Cell 3 / result DataSet=Norman', '支持路径与评测证据；不冒充当前教程已运行Norman')
use('sciplex3', 'chemCPA', '从头训练；或LINCS预训练后微调；留药物测试', '不同约900/2000基因版本',
    ['year_chemcpa_experiments', 'year_chemcpa_preprocessing'], 'experiments README sections 2–3', '模型作者明确实验方案')
for ds, task in [('sciplex3', 'cellot_sciplex3_yaml'), ('kang2018', 'cellot_lupuspatients_yaml'),
                 ('hagai2018', 'cellot_crossspecies_yaml'), ('zhao2021', 'cellot_gbm_yaml')]:
    use(ds, 'CellOT', '任务内训练与测试', '作者对应任务配置；Hagai具体原子集对应仍待核',
        [task, 'cellot_README_md'], 'configs/tasks / README experiments', '作者任务配置')
use('kang2018', 'trVAE', 'benchmark训练与测试', 'scPerturBench kangCrossCell、hvg5000子集',
    ['year_scpb_trvae'], 'DataSet=kangCrossCell / trvae.train', 'benchmark明确训练脚本')
for model, key, role in [('GEARS', 'year_scpb_myGears', 'benchmark重新训练与测试'),
                         ('AttentionPert', 'year_scpb_myAttentionPert', 'benchmark训练与测试'),
                         ('scGPT', 'year_scpb_myscGPT1', 'benchmark加载预训练权重后微调与测试')]:
    use('papalexi2021', model, role, 'scPerturBench脚本当前主循环Papalexi', [key],
        'main Papalexi loop / train; scGPT torch.load + optimizer training', 'benchmark明确训练入口')
pb_map = {'norman19': 'norman2019', 'sciplex3': 'sciplex3', 'op3': 'op3_2023',
          'frangieh21': 'frangieh2021', 'jiang24': 'jiang24', 'mcfaline23': 'mcfaline2023'}
names = {'cpa': 'CPA（PerturBench实现）', 'linear': 'Linear Additive', 'latent': 'Latent Additive', 'biolord': 'biolord（PerturBench实现）'}
for short, ds in pb_map.items():
    for model, name in names.items():
        key = f'year_pb_{short}_{model}'
        if key not in sources:
            continue
        cfg = (R / sources[key]['path']).read_text()
        if 'override /data:' not in cfg or 'override /model:' not in cfg:
            raise ValueError('Missing reviewed model/data binding: ' + key)
        use(ds, name, 'benchmark训练与测试配置', 'NeurIPS2025处理版本；G×E此处是full配置',
            [key, 'year_pb_train_defaults', 'perturbench_README_md'],
            'defaults /data and /model; train.yaml train=True,test=True', '数据集专用复现实验配置；本轮未运行')
for ds, keys, scope in [
    ('parse_cytokines', ['state_parse_tomls_split_1_toml'], 'parse_final_concat对应版本'),
    ('tahoe100m', ['state_tahoe_tomls_generalization'], 'Tahoe药物/剂量划分版本'),
    ('nadig2024', ['state_replogle_tomls_hepg2_toml'], '与Replogle合并的replogle_nogwps_v2目录；HepG2/Jurkat'),
    ('vcc2025', ['state_primary_readme'], 'VCC2025训练教程')]:
    # Resource aliases differ across discovery passes; resolve by the exact cached path if needed.
    resolved = []
    for key in keys:
        if key in sources:
            resolved.append(key)
        else:
            expected = {'state_parse_tomls_split_1_toml': 'sources/state_parse_tomls_split_1.toml',
                        'state_tahoe_tomls_generalization': 'sources/state_tahoe_tomls_generalization.toml',
                        'state_replogle_tomls_hepg2_toml': 'sources/state_replogle_tomls_hepg2.toml'}[key]
            resolved.append(by_path[expected]['id'])
    use(ds, 'State Transition', '预测模型训练与留出测试', scope,
        resolved + ['state_primary_readme'], '[training] / fewshot val,test / VCC training tutorial', '模型作者训练配置/教程')
write_csv('dataset_model_training_evidence.csv', uses)

# Paper year and first public data release are intentionally separate.
years = {
    'adamson2016': '2016', 'dixit2016': '2016', 'datlinger2017': '2017', 'norman2019': '2019',
    'replogle2022': '2022', 'srivatsan2020': '2019-12-05在线；2020-01-03卷期',
    'lotfollahi2023': '2023', 'kang2018': '2018', 'hagai2018': '2018', 'mcfarland2020': '2020',
    'frangieh2021': '2021', 'papalexi2021': '2021', 'tian2019': '2019', 'tian2021': '2021',
    'gasperini2019': '2019-01-03在线；2019-01-10卷期', 'shifrut2018': '2018',
    'xie2017': '2017', 'zhao2021': '2021', 'aissa2021': '2021',
    'op3_2023': '原研究论文发表日期未核实',
    'mcfaline2023': '2024-01-25在线；2024-02-14卷期',
    'jiang24': '未核实；Jiang2025书目存在，但与该下载版本的关联仍需核实',
    'tahoe100m': '2025预印本；最终期刊日期未核实',
    'dong2023': '2022预印本；2023 Nature Methods', 'haber2017': '2017',
    'parse_cytokines': '原论文未核实；2025 State预印本已有使用证据',
    'nadig2024': '2024是整合资源标签；原刊年份未核实', 'vcc2025': '原研究论文发表日期未核实',
}
paper_keys = {'srivatsan2020': 'sciplex_primary', 'mcfaline2023': 'gxe_primary',
              'gasperini2019': 'gasperini_primary'}
selected_scales = {
    'norman2019': 'CPA教程：111122细胞×5044特征（全部split对象）',
    'kang2018': 'CPA教程：13576细胞×5000特征（不是GEO全研究）',
    'lotfollahi2023_combo': 'CPA教程：63378细胞×5000特征',
    'sciplex3': '原论文/QC后649340细胞；PerturBench下载对象799317×110984，处理后183856×9198；版本差异未闭合',
    'mcfaline2023': '原论文kinome screen：1052205细胞、14121 G×E组合、两次独立转导；PerturBench处理后存档输出111445×5666',
    'frangieh2021': 'PerturBench输入存档输出218331细胞×23712特征；不等于最终训练折',
    'jiang24': 'PerturBench合并输出1628476细胞×15476特征；不是最终训练折',
    'op3_2023': '整理notebook存档298087细胞×21265特征；输出与代码单元位置不一致，须原文件复核',
    'replogle2022_k562_gwps': '存档同名adata输出819400和1989578细胞（均8248特征）；变更过程不明，未选定唯一规模',
    'gasperini2019': '原论文两项at-scale实验合计254974细胞、5920候选enhancer；不同面板/MOI',
}
log_nb = json.loads((R / 'sources/perturbench_curate_Srivatsan20.ipynb').read_text())
download_log = output_text(log_nb['cells'][3])
file_bytes = int(re.search(r'Length: (\d+)', download_log)[1])
files = [dict(dataset_id='sciplex3', object_name='SrivatsanTrapnell2020_sciplex3.h5ad',
              file_bytes=file_bytes, decimal_GB=round(file_bytes / 10**9, 6), GiB=round(file_bytes / 1024**3, 6),
              evidence='PerturBench作者notebook保存的2024-06-12 wget响应长度；本轮未下载此表达文件',
              source_url=by_path['sources/perturbench_curate_Srivatsan20.ipynb']['url'],
              locator='Cell 3; Length header', current_release_revalidated='no')]
write_csv('expression_file_sizes.csv', files)

rows = []
for old in inventory:
    ds, family = old['dataset_id'], old['family_id']
    model_rows = [u for u in uses if u['dataset_id'] == ds]
    basis = '整合文档/文献引用年；原刊具体日期未核验；未采用旧目录Year列'
    year_source = old['source_urls']
    if family in paper_keys:
        basis = '本轮已下载并读取原论文PDF，在线日与卷期日分列'
        year_source = url(paper_keys[family])
    elif family in ['replogle2022', 'papalexi2021', 'dong2023']:
        basis = 'pertpy references.bib正式期刊引用；二级书目证据'
        year_source = url('year_pertpy_references')
    elif family in ['adamson2016', 'dixit2016', 'datlinger2017', 'norman2019', 'frangieh2021']:
        basis = 'G×E原论文参考文献5/6/8/9/10等明确年份；属于被引文献证据'
        year_source = url('gxe_primary')
    release = '原始数据库首次公开日期、后续release日期尚未核实；论文年份不代替发布日期'
    if family == 'op3_2023': release = '2023竞赛数据发布；GSE279945具体首次公开/更新日期未核实'
    if family == 'vcc2025': release = '官方2025 challenge版本；精确首次公开日未核实'
    train = '；'.join(f"{u['model']}：{u['role']}" for u in model_rows) or '未取得数据集专用训练/微调证据；已有benchmark记录或整合收录另见采用列'
    rows.append(dict(dataset_id=ds, family_id=family, dataset_name=old['formal_name'],
                     paper_year_or_date=years[family], year_evidence=basis, year_source=year_source,
                     data_first_release=release,
                     original_study_scale=old['cell_count_and_scope'],
                     version_specific_scale=selected_scales.get(ds, old['cell_count_and_scope']),
                     perturbations_and_scope=old['perturbation_count_and_scope'],
                     expression_file_size=f'{file_bytes} bytes / {file_bytes / 10**9:.3f} GB / {file_bytes / 1024**3:.3f} GiB；2024下载日志对应h5ad，不是本轮当前版本HEAD' if ds == 'sciplex3' else '尚未核实；不由细胞数估算，也不使用PDF/代码/容器大小替代',
                     training_and_finetuning_models=train,
                     other_adoption_evidence=old['model_benchmark_evidence'],
                     roles_note='原作者训练、benchmark重训、微调、仅评测、仅支持下载分别记录；不据结果表认定训练角色',
                     unresolved='数据首次公开/版本日期、当前表达文件字节数和各模型实际训练折细胞数未完全核验'))
assert len(rows) == 32 and len({r['dataset_id'] for r in rows}) == 32
write_csv('dataset_year_size_models.csv', rows)
(R / 'tables/dataset_year_size_models.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n')

intro = '''# 数据年份、规模、文件大小与模型训练用途

更新日期：2026-10-11（UTC）。覆盖32个条目；同源子集分别列出。完整字段见 [CSV](dataset_year_size_models.csv) / [JSON](dataset_year_size_models.json)。

“年份”分为论文在线发表、卷期年份、数据首次公开和后续版本日期；未核实的数据发布日期不使用论文年替代。旧scPerturb目录Year列有混合提交时间问题，没有直接采用。多数非原文年份来自文献引用，证据级别和链接在CSV。

“规模”是细胞数/特征数及对应版本；notebook输出是作者保存的历史记录，不是本轮读矩阵计算，也不是模型训练折细胞数。特征数是文件列数，不自动等于去重后的基因数。原研究、benchmark筛选子集和train split不能混用。

表达文件大小目前只有sciPlex3旧下载日志提供精确值：2,456,030,368 bytes，约2.456 GB/2.287 GiB。本轮没有下载该表达矩阵，不能保证当前版本大小相同。其他未知不填0，不按细胞数估算。PDF大小与表达数据大小分开。

下表只把有作者教程、专用训练配置或明确脚本的模型写进训练/微调栏；完整 [模型关联与角色证据](dataset_model_training_evidence.csv) 记录来源和定位。其余仅有benchmark结果的模型仍见 [已有评测采用](observed_benchmark_usage.csv)，不能直接称为训练。

|数据集|论文年份/日期（非数据首次公开日）|规模与版本|训练/微调用途|
|---|---|---|---|
'''
def md(s): return str(s).replace('|', '/').replace('\n', ' ')
table = '\n'.join('|'+ '|'.join(md(r[k]) for k in ['dataset_name','paper_year_or_date','version_specific_scale','training_and_finetuning_models'])+'|' for r in rows)
tail = '''

补充说明：OP3竞赛数据是2023版本，VCC是2025版本；其余首次数据库公开日仍需官方记录。State的Parse/Tahoe/Replogle-Nadig用途是扰动预测模型State Transition训练，不能自动称为State Embedding预训练。Replogle-Nadig合并目录到2022各子集的对应未闭合，因此没有把State逐项写进GWPS/essential/RPE1的已确认训练栏。

chemCPA作者说明的LINCS预训练属于非单细胞的L1000资源，仍在核心扰动单细胞清单之外；sciPlex3用于后续微调或从头训练。scGPT加载已有模型权重后训练的条目明确标微调；作者教程当前默认Adamson，Norman分支支持不冒充该教程实际运行结果。

新增原文及批次结论见 [PDF阅读记录](../papers/reading_notes.md)。G×E原文2024年发表，不能沿用McFaline23别名当发表年；sciPlex在线2019、卷期2020，两者均保留。CINEMA-OT正式期刊引用已补为2023，但不是证明该数据用于预测模型训练。

可复现：`python research/scripts/build_year_size_usage.py`；读取本地冻结来源，不下载表达矩阵或训练模型。[各版本存档规模](version_size_observations.csv) 与 [表达文件大小证据](expression_file_sizes.csv) 保留所有差异。Replogle相邻存档输出互相不一致；OP3输出在注释单元下；这些数字需要实际文件复核，不能据此完成细胞级批次审计。
'''
(R / 'tables/dataset_year_size_models.md').write_text(intro + table + tail)
print(f'Built {len(rows)} dataset profiles, {len(uses)} model-role links, {len(observations)} archived size observations')

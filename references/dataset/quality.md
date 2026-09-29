# Markdown版验收范围

2026-09-29。验收命令为技能根目录下的 `python3 scripts/verify_skill.py .` 与 `python3 scripts/verify_dataset.py .`。

- 新增5,593条JSON与源Parquet全部11字段逐行对照；Markdown正文按原字符逐条对照JSON，所有记录及正文哈希可追溯。
- 原183份来源的Markdown正文与原PDF提取TXT逐条比较；PDF和原提取文本仍保留原有校验链。
- 印花税、扣除凭证、房产税检索返回相应Markdown路径；索引与章节的本地引用检查存在性。
- book-to-skill按文本模式处理资料并提炼实务章节；生成技能安全扫描仅覆盖入口、章节、术语、模式和速查，不覆盖原始语料。
- 原始正文中的空白按源数据保留；代码和手写文档单独做语法及Git空白检查。

没有逐条在线核验现行法规效力或后续修订。没有恢复源数据中缺失的附件或表格单元格。实务算例是教学假设，不是实际申报或记账。新数据Markdown直接来自Parquet，不依赖已生成的本地PDF。

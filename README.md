# finance-advisor

面向 Agent 的自包含中文财务顾问技能：内置税务交易识别、企业会计准则、准则解释、效力核验、酒店业实务和可审计回答流程。2026-09-29新增5,593条财税记录及完整Markdown正文、原始JSON字段，补充印花税申报、扣除凭证和物业税费实操。

## 安装

将本仓库目录作为一个 skill 安装，使 `SKILL.md` 位于 skill 根目录。仓库已经内置全部政策Markdown正文及原183份PDF核对件，不需要另行准备本地资料：

```bash
git clone https://github.com/fujinghui110110-cyber/finance-advisor-skill.git
```

也可以把本目录复制到 Agent 的 skills 目录，或使用 Agent Skills 兼容安装器：

```bash
npx skills add https://github.com/fujinghui110110-cyber/finance-advisor-skill --skill finance-advisor
```

## Markdown优先

全部5,776份来源均可通过Markdown读取；标题、元数据、完整正文和引用路径在仓库内。新数据直接从Parquet无损转制，不经过PDF回抽，避免分页和字体干扰。PDF适合版面核对、打印，并不提高原生文本的检索准确性。源数据未提供的表格结构或附件，Markdown同样不能恢复。

## 使用边界

- 本技能提供判断框架、2026-09-28原资料快照和2026-09-29导入数据；`references/text/`、`references/pdf/`为原资料，新增内容在`references/dataset/`。
- 语料按 SHA-256 从 359 份 PDF 合并为 183 份唯一文件，重复映射见 `references/duplicates.md`。
- 快照不是实时法规库。涉及申报、报表定稿、付款、合同或重大判断时，必须回看现行官方原文并核对具体事实、地域和施行日。
- 不把会计司实施问答、地方口径或原目录状态提示当作可以替代正式法源的结论。

## 目录

- `SKILL.md`：入口和路由规则
- `chapters/`：11个主题章节，含酒店业、合同印花税及扣除凭证实务
- `references/`：原183份Markdown正文、PDF核对件、哈希清单和重复映射
- `scripts/build_corpus.py`：从本地 PDF 目录重新生成内置语料
- `scripts/verify_skill.py`：离线验证语料覆盖、哈希和本地路径隔离
- `references/dataset/`：5,593条完整Markdown正文和原字段JSON；新增转制PDF仅本地保留，不进入Git历史；成文日期截至2026-02-13，不能视为最新有效法规全集。完整性说明见[导入说明](references/dataset/README.md)。
- `scripts/search_dataset.py`：只用Python标准库离线检索；`scripts/verify_dataset.py`校验新增全量文件。
- `scripts/import_parquet.py`：可复现转换入口；仅从Parquet重新构建需要pyarrow，使用与校验技能只需Python标准库，无需PDF工具或中文字体。
- `patterns.md`、`cheatsheet.md`、`glossary.md`：回答模板、现场速查和术语表

## 许可边界

技能代码、索引和编排结构使用 MIT License，详见 [LICENSE](LICENSE)。内置政策文件及其文本提取的再分发仍应遵守相应来源文件的公开、转载和使用要求。

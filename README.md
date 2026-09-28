# finance-advisor

面向 Agent 的自包含中文财务顾问技能：内置税务交易识别、企业会计准则、准则解释、效力核验、酒店业实务和可审计回答流程。

## 安装

将本仓库目录作为一个 skill 安装，使 `SKILL.md` 位于 skill 根目录。仓库已经内置政策文本和 PDF，不需要另行准备本地资料：

```bash
git clone https://github.com/fujinghui110110-cyber/finance-advisor-skill.git
```

也可以把本目录复制到 Agent 的 skills 目录，或使用 Agent Skills 兼容安装器：

```bash
npx skills add https://github.com/fujinghui110110-cyber/finance-advisor-skill --skill finance-advisor
```

## 使用边界

- 本技能同时提供判断框架和 2026-09-28 资料快照；`references/text/` 是逐份完整提取文本，`references/pdf/` 是逐份 PDF 副本。
- 语料按 SHA-256 从 359 份 PDF 合并为 183 份唯一文件，重复映射见 `references/duplicates.md`。
- 快照不是实时法规库。涉及申报、报表定稿、付款、合同或重大判断时，必须回看现行官方原文并核对具体事实、地域和施行日。
- 不把会计司实施问答、地方口径或原目录状态提示当作可以替代正式法源的结论。

## 目录

- `SKILL.md`：入口和路由规则
- `chapters/`：9 个主题章节，含酒店业实务
- `references/`：183 份完整政策文本、PDF、哈希清单和重复映射
- `scripts/build_corpus.py`：从本地 PDF 目录重新生成内置语料
- `scripts/verify_skill.py`：离线验证语料覆盖、哈希和本地路径隔离
- `patterns.md`、`cheatsheet.md`、`glossary.md`：回答模板、现场速查和术语表

## 许可边界

技能代码、索引和编排结构使用 MIT License，详见 [LICENSE](LICENSE)。内置政策文件及其文本提取的再分发仍应遵守相应来源文件的公开、转载和使用要求。

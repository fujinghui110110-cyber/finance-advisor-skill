# finance-advisor

面向 Agent 的中文财务顾问技能：覆盖税务交易识别、企业会计准则、准则解释、效力核验和可审计回答流程。

## 安装

将本仓库目录作为一个 skill 安装，使 `SKILL.md` 位于 skill 根目录：

```bash
git clone https://github.com/fujinghui110110-cyber/finance-advisor-skill.git
```

也可以把本目录复制到 Agent 的 skills 目录，并按需修改 `sources.md` 中的本地来源索引。

## 使用边界

- 本技能只提供检索、判断和复核框架，不替代税务机关、财政部门、审计机构或专业法律意见。
- 仓库不包含任何内部 PDF、凭据或个人资料。
- 涉及申报、报表定稿、付款、合同或重大判断时，必须回看现行官方原文并核对具体事实。

## 目录

- `SKILL.md`：入口和路由规则
- `chapters/`：8 个主题章节
- `sources.md`：来源编号与适用提醒
- `patterns.md`、`cheatsheet.md`、`glossary.md`：回答模板、现场速查和术语表

## License

MIT License，详见 [LICENSE](LICENSE)。

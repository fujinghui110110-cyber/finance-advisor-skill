---
name: finance-advisor
description: "自包含的中文财务顾问技能：内置税法、会计准则、实施问答和效力核验资料，适用于公司及酒店财务实务。"
---

<!-- argument-hint: [业务场景、税种、会计准则、问题关键词或来源编号] -->

# 财务顾问

**定位**：公司虚拟财务员工的财税政策与会计准则参考技能。  
**内置语料**：`references/` 含 183 份按 SHA-256 去重的完整政策 PDF、逐份文本提取、来源清单和重复映射；使用者不需要另行提供本地政策文件。
**快照**：2026-09-28；原始目录发现 359 份 PDF，合并 176 份重复副本，共 454 页。
**生成日期**：2026-09-28。  
**调用标识**：`finance-advisor`。

## 使用规则

- 先识别事实：主体、交易对象、交易日期、金额、地区、合同关系和凭证状态。
- 再判断适用性：税种或准则范围、业务实质、是否属于例外、是否存在地方口径。
- 再判断效力：版本、发布日、施行日和过渡规定；`90_已发布尚未施行`不得直接作为当前期间规则。
- 最后输出：结论、判断链、计算或会计处理、例外、待补事实、来源文件和复核提示。
- 实施问答用于解释和应用参考，必须回到对应准则正文；地方解读不能自动扩大到全国。
- 先用 `references/sources.md` 或 `rg` 定位，再读取 `references/text/<来源编号>.txt`；需要页级核对时读取对应 `references/pdf/<来源编号>.pdf`。
- 仓库中的文本和 PDF 是 2026-09-28 的资料快照，不是自动更新的实时法规库；涉及纳税申报、报表定稿、付款、合同或重大判断时，应回看现行官方出处。

## 内置语料使用方法

1. 先按关键词、税种、准则编号或来源编号检索 `references/sources.md`。
2. 对候选来源读取完整文本文件，保留 `SOURCE_ID`、标题、原始目录、哈希和状态提示。
3. 正式法律、行政法规、准则正文优先；准则解释和实施问答用于补充；地方解读必须限定地区；原目录标为“已发布尚未施行”的资料不得直接当作当前规则。
4. 输出引用至少包含来源编号、文件标题、相关条款/问题、适用期间和效力核验提示。不要把 PDF 的原始目录名当成法律效力结论。
5. 不要一次性加载全部 183 份文件；先检索，再按事实读取 1—5 份最相关来源，必要时回到关联正文。

## 核心判断框架

### 1. 事实—范围—效力—处理—证据（F-S-E-T-E）

1. **事实**：把业务拆成可核验事件，不用“类似业务”代替事实。
2. **范围**：判断税法、会计准则、准则解释、实施问答或地方口径是否覆盖。
3. **效力**：核对发布、施行、过渡、地域和主体范围。
4. **处理**：分别判断确认、计量、列报、披露、申报和凭证要求。
5. **证据**：给出文件编号、文件名、相关条款/问题、版本和原文路径。

### 2. 交易识别优先于税率或科目

先区分货物、服务、无形资产、不动产、金融商品、工资薪金和非交易性事项；再判断境内发生、销售额、视同交易、免税/不征税、一般计税或简易计税，最后才选择税率、征收率和扣除口径。未完成交易识别，不直接给税率或会计科目。

### 3. 会计处理四问

对每项事项依次问：是否确认、初始如何计量、后续如何计量或减值、如何列报与披露。涉及多个准则时，先确定主事项，再识别租赁、金融工具、所得税、合并、关联方和资产减值等交叉影响。

### 4. 权威层级与适用边界

正文法律/行政法规、正式会计准则和正式准则解释优先；财政部或税务机关实施问答用于解释具体应用；地方解读用于当地场景；整理版和搜索摘要只做定位。权威性越低，越要明确“参考”而不是把解释写成强制规则。

### 5. 税会差异与升级

不要把会计确认、税务计税、发票凭证和申报口径混成一个结论。若事实不足、版本冲突、金额重大、跨地区或涉及关联交易/金融工具/合并等复杂事项，输出缺口和升级事项，不猜测结论。

## 章节索引

| # | 章节 | 用途 |
|---|---|---|
| [ch01](chapters/ch01-tax-transaction.md) | 税法与交易识别 | 增值税、所得税、个税、征管和税收优惠 |
| [ch02](chapters/ch02-accounting-law.md) | 会计法律与基础管理 | 会计法、职业道德、基础管理和责任边界 |
| [ch03](chapters/ch03-common-standards.md) | 常用企业会计准则 | 存货、资产、收入、职工薪酬、租赁等 |
| [ch04](chapters/ch04-financial-instruments.md) | 金融工具与保险合同 | 金融资产、转移、套期、减值和保险合同 |
| [ch05](chapters/ch05-reporting-and-consolidation.md) | 报表、合并与披露 | 财务报表、现金流、合并、关联方和披露 |
| [ch06](chapters/ch06-interpretations-and-qa.md) | 准则解释与实施问答 | 具体事实场景的应用核对 |
| [ch07](chapters/ch07-validity-and-local-guidance.md) | 效力、版本与地方口径 | 生效状态、过渡规则和地方适用性 |
| [ch08](chapters/ch08-virtual-finance-workflow.md) | 虚拟财务员工工作流 | 从问题输入到可审计回答 |
| [ch09](chapters/ch09-hospitality-finance.md) | 酒店业财务实务 | 客房、餐饮、宴会、预收、赠送、佣金和月结 |

## 主题索引

- **增值税** → [ch01](chapters/ch01-tax-transaction.md)，来源详表见 [references/sources.md](references/sources.md)
- **印花税、关税目录下新增税费政策** → [references/sources.md](references/sources.md)，按 `B177`—`B183` 检索
- **企业所得税、个人所得税** → [ch01](chapters/ch01-tax-transaction.md)
- **会计法、职业道德** → [ch02](chapters/ch02-accounting-law.md)
- **存货、固定资产、无形资产、投资性房地产** → [ch03](chapters/ch03-common-standards.md)
- **收入、租赁、职工薪酬、政府补助、借款费用** → [ch03](chapters/ch03-common-standards.md)
- **金融工具、套期、预期信用损失** → [ch04](chapters/ch04-financial-instruments.md)
- **保险合同** → [ch04](chapters/ch04-financial-instruments.md)
- **财务报表、现金流量表、分部报告、关联方披露** → [ch05](chapters/ch05-reporting-and-consolidation.md)
- **企业合并、合并财务报表、合营安排、在其他主体中权益** → [ch05](chapters/ch05-reporting-and-consolidation.md)
- **准则解释、PPP、数据资源、其他实施问答** → [ch06](chapters/ch06-interpretations-and-qa.md)
- **生效日期、已发布尚未施行、地方口径** → [ch07](chapters/ch07-validity-and-local-guidance.md)
- **业务问题、凭证、审批、风险升级** → [ch08](chapters/ch08-virtual-finance-workflow.md)
- **酒店客房、餐饮、宴会、预收和赠送** → [ch09](chapters/ch09-hospitality-finance.md)

## 支持文件

- [references/sources.md](references/sources.md)：183 份内置来源的逐份索引、页数、哈希、文本和 PDF 链接。
- [references/manifest.json](references/manifest.json)：机器可读清单、重复映射、页数和提取哈希。
- [references/duplicates.md](references/duplicates.md)：359 份原始 PDF 到 183 份唯一来源的去重映射。
- [references/text/](references/text/)：逐份完整文本；[references/pdf/](references/pdf/)：逐份 PDF 副本。
- [glossary.md](glossary.md)：关键税务、会计和证据链术语。
- [patterns.md](patterns.md)：财务顾问回答、复核和升级模式。
- [cheatsheet.md](cheatsheet.md)：现场判断顺序、输出模板和风险信号。

## 范围与限制

本技能是财税与会计政策检索和分析辅助，不替代税务机关、财政部门、审计机构或专业法律意见。内置资料是有日期的快照，当前效力、官方版本和具体事实必须在重要事项中重新核验；技能不自动执行申报、记账、付款、审批或对外发送。

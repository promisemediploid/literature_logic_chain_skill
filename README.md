# Literature Logic Chain

**把一篇算法论文还原成一条完整的因果逻辑链，并生成一份可直接阅读、可交互的独立网页。**

这是一个 Codex Skill，默认使用者是**计算机基础薄弱的读者**：文科生、管理/社科背景学生，以及刚开始读算法论文的人。

它不把论文压成摘要、关键词或流程图，而是按照人类真正理解事物的顺序，从「作者到底在解决什么问题」一路讲到「论文真正证明了什么、没有证明什么」。

> An interactive Codex skill that turns a technical paper into a full causal chain ordered by human cognition, plus a single-file, content-first HTML reading page. Documentation is in Chinese because the skill's target readers are Chinese-speaking beginners.

---

## 它解决什么问题

大多数人读论文失败，不是因为不够聪明，而是因为阅读顺序错了。

常见的失败模式：

* 读完 abstract 和 conclusion，记住了几个术语，但说不出作者为什么非这么做不可；
* 把「解决 content/style entanglement」「学习 residual style」这类短语当成理解；
* 看到 ablation 表格的分数高低，却不知道它到底反驳了哪一种设计；
* 读完之后说不清哪些结论真的被证明了，哪些只是合理猜测。

这个 skill 强制改变输出方式：**内容优先于结构与功能，理解优先于压缩，认知顺序优先于论文原始章节顺序。**

## 效果预览

`demo/2606.10099_logic_chain.html` 是一篇示例论文的完整阅读结果。单文件、无外部依赖、可直接分享：把它 clone 下来用浏览器直接打开即可（GitHub 页面不会渲染 HTML 文件，需要下载或点 `Raw`）。

* 页面顶部是 **「先用一段完整的话把整篇论文讲懂」**；
* 前置知识只占很小一块，按「必须知道 / 建议知道 / 知道名字即可」列词条，不做课程；
* 逻辑链的每一节都是完整解释，并回答四个问题：为什么必须走到这一步、这一步在做什么、不这样做会怎样、论文给了什么证据；
* 支持搜索、阶段筛选、点击定位、上下游高亮、术语高亮相关节点；
* 默认状态下正文已经直接展示，不需要点开节点才能读到解释。

对应的结构化数据在 `demo/2606.10099_logic_chain.json`，可以作为自己写输入文件时的参照。

## 快速开始

### 1. 安装为 Codex Skill

全局安装（所有项目可用）：

```bash
git clone https://github.com/<your-name>/literature-logic-chain.git ~/.codex/skills/literature-logic-chain
```

只在某个项目里使用（项目级 skill）：

```bash
cp -r literature-logic-chain <your-repo>/.agents/skills/literature-logic-chain
```

安装完成后重启 Codex 会话，让它重新扫描 skill 目录。

### 2. 在对话里调用

```text
$literature-logic-chain

请从头到尾阅读这篇论文。
我的计算机基础比较薄弱，请不要用摘要式、术语堆砌式的方式解释。
一定要按照人类认知顺序，从「作者为什么研究这个问题」开始，一步一步解释：
为什么现有方法不够、作者发现了什么、如何把这个想法变成数据和模型、
每个模型具体负责什么、为什么必须这样设计、不这样做为什么不行、
实验分别在验证哪一个说法、ablation 说明了什么，
最后说明论文证明了什么和没有证明什么。

开头请先用一整段完整的话把全篇逻辑讲懂，不要为了「一句话」而压缩成口号。
前置知识只列词条即可。
最后生成一个蓝色系、可直接阅读、可交互的独立 HTML。
```

论文可以直接贴文本、贴文件路径，或者只给标题让你先检索。

### 3. 只使用 HTML 生成器

如果你已经有结构化数据，只想生成网页：

```bash
python scripts/generate_logic_html.py demo/2606.10099_logic_chain.json -o output.html
```

脚本只依赖 Python 标准库（3.8+），生成的是**单文件自包含 HTML**：样式和脚本都内联，没有 CDN、没有网络请求，可以离线打开或直接发给别人。

## 仓库结构

```text
literature-logic-chain/
├── SKILL.md                      # Skill 本体：全部写作规范与输出要求
├── README.md
├── agents/
│   └── openai.yaml               # Skill 的界面元数据（显示名、配色、默认提示词）
├── references/
│   ├── example-principles.md     # 从范例中提炼的设计要点
│   └── output-schema.md          # 结构化数据格式说明
├── scripts/
│   └── generate_logic_html.py    # 由 JSON 生成单文件交互网页
└── demo/
    ├── 2606.10099_logic_chain.html
    └── 2606.10099_logic_chain.json
```

## 输出结构

默认按下面的顺序输出，每一步都是完整解释而不是标签：

1. **先用一段完整的话把整篇论文讲懂**（约 250–500 字，覆盖问题 → 现有方法不足 → 关键观察 → 数据与模型设计 → 最终任务 → 实验验证）
2. **阅读前置知识**（只列词条，分三档，不做教学）
3. **从头到尾的完整逻辑链**（按认知顺序，而不是论文章节顺序）
4. **为什么这样设计？不这样做为什么不行？**
5. **模型/组件各自负责什么？**
6. **数据为什么要这样处理？**
7. **实验到底在验证前面的哪一句话？**
8. **Ablation：把关键设计拿掉会发生什么？**
9. **论文真正证明了什么？没有证明什么？**
10. **研究空白**（优先来自论文 explicit limitation，推断必须标明是推断）

## 设计原则

这些原则是 SKILL.md 里被反复强调的硬约束：

* **完整自然语言优先。** 「Why: 防止信息泄漏 / Function: 学习 style」这种写法被明确禁止作为主要解释，必须展开成读者能懂的因果叙述。
* **不为了精炼牺牲理解。** 「解决 content/style entanglement」只能是术语标签，正文必须说清混在一起的是什么、为什么混在一起会出问题、模型做了什么让它们分开。
* **术语先翻译再使用。** 第一次出现 embedding、encoder、frozen、loss、prototype、AUROC 时，先补足读懂这篇论文所需的最低理解。
* **公式先讲人话。** 先说这个公式在让什么东西变大或变小，再讲符号。
* **逻辑链写成能顺着读下去的故事。** 节点标题是问题或因果判断，不是名词；每个节点都要回答「为什么必须这样、这一步承担什么作用、不这样做会出现什么捷径或信息丢失、论文用什么结果支持」。
* **实验是对前面说法的逐项盘问。** 不按表格念分数，而要说明这个实验检验了哪一句话、能证明到什么程度、还有什么不能由它推出。
* **Ablation 用反事实解释。** 写清「拿掉这个设计后，模型获得了什么机会、原本的分工如何被削弱」，而不是只写「Frozen > Unfrozen」。
* **结论有边界。** 严格区分论文明确说的、由结构直接推出的、实验支持的、以及我们自己的推断；一个语言上的结果不等于所有语言成立。
* **网页首先是阅读稿。** 默认状态正文直接可读，交互只服务于定位与对照，不允许为了「交互感」把核心解释藏起来。

## 数据格式

网页由一份 JSON 驱动。顶层字段：

```json
{
  "title": "论文标题",
  "subtitle": "按人类认知顺序理解整篇论文",
  "opening_explanation": "一段完整的全篇逻辑解释",
  "prerequisites": {
    "required": ["必须知道的词条"],
    "recommended": ["建议知道的词条"],
    "nice_to_know": ["知道名字即可的词条"]
  },
  "nodes": [],
  "edges": [],
  "experiments": [],
  "limitations": []
}
```

每个逻辑节点：

```json
{
  "id": "unique-id",
  "stage": "problem|gap|hypothesis|data|model|training|downstream|evidence|limitation",
  "title": "用一个完整问题或判断告诉读者这一阶段在讲什么",
  "explanation": "2–5 句完整中文解释",
  "why": "为什么必须走到这一步",
  "function": "这一步为整个方法贡献什么",
  "if_omitted": "删掉或改掉这一步会出现什么问题",
  "evidence": ["对应的实验、图表或论文依据"],
  "source": ["论文页码/章节/图表"],
  "depends_on": ["previous-node-id"]
}
```

生成脚本会校验：顶层字段是否齐全、每个节点是否包含必需字段、`stage` 是否合法、`id` 是否重复、`edges` 是否指向存在的节点。生成前先跑一遍就能拿到明确的报错。细节见 `references/output-schema.md`。

## 常见问题

**为什么输出这么长？**

因为目标读者读不懂短版本。SKILL.md 里有一条明确规则：遇到多 encoder、多 loss、多阶段的复杂论文，宁愿展开解释，也不要压缩成一张表或一句话。

**可以直接用它做文献综述吗？**

它的定位是「把单篇论文讲懂」。综述需要的是横向比较，输出结构不同，可以把它当作写综述前的精读步骤。

**生成的 HTML 能改样式吗？**

样式全部内联在 `scripts/generate_logic_html.py` 的模板里，改配色或排版直接改 CSS 变量即可，生成的页面依然是单文件。

**必须联网吗？**

不需要。生成脚本只用 Python 标准库，生成的网页不含任何外部资源。

## 致谢

写作规范来自一份人工精读范例的逆向拆解：先找出「读懂了」和「以为自己读懂了」之间的差别，再把这些差别固化成可复用的检查项。

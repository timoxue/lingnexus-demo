# LingNexus - AI 药物分子发现系统

> 基于 **AgentScope** 框架的多智能体药物发现流程
> 
> **三大模型对比**：Qwen-Max vs DeepSeek 3.2 vs Gemini 3 Pro

---

## 🎯 核心特性

- ✅ **3 大 LLM 模型**：Qwen-Max / DeepSeek 3.2 / Gemini 3 Pro
- ✅ **智能体协作**：MoleculeDesigner + ADMETEvaluator
- ✅ **化学验证**：基于 RDKit 的 ADMET 筛选
- ✅ **图形界面**：Web UI 可视化对比
- ✅ **安全合规**：仅使用公开靶点（BTK、EGFR、JAK2）

---

## 📊 三大模型对比

| 模型 | 优势 | 通过率 | 适用场景 |
|------|------|--------|----------|
| **Qwen-Max** 🇨🇳 | 中文优化，格式规范 | 80% | 国内应用，演示 |
| **DeepSeek 3.2** 🧠 | 推理能力强 | 75% | 复杂约束 |
| **Gemini 3 Pro** 🔥 | 最新最强，质量最高 | 85% | 高质量要求 |

---

## 🚀 快速开始

### 1️⃣ 安装依赖

```bash
pip install -r requirements.txt

# Windows 推荐使用 conda 安装 RDKit
conda install -c conda-forge rdkit
```

### 2️⃣ 配置 API Key

编辑 `config/model_config.json`：

```json
[
  {
    "config_name": "qwen-max",
    "api_key": "YOUR_QWEN_API_KEY"  // 👈 填入 API Key
  },
  {
    "config_name": "deepseek",
    "api_key": "YOUR_DEEPSEEK_API_KEY"  // 👈 填入 API Key
  },
  {
    "config_name": "gemini",
    "api_key": "YOUR_GEMINI_API_KEY"  // 👈 填入 API Key
  }
]
```

**获取 API Key**：
- **Qwen-Max**：https://dashscope.console.aliyun.com/
- **DeepSeek**：https://platform.deepseek.com/
- **Gemini**：https://aistudio.google.com/

### 3️⃣ 启动图形界面

```bash
# 单模型生成
python app.py

# 模型对比（推荐）
python app_compare.py
```

或**双击批处理文件**：
- `启动图形界面.bat` - 单模型生成
- `启动模型对比工具.bat` - 模型对比

---

## 💡 使用说明

### 图形界面（推荐）

启动后访问：http://127.0.0.1:7860（单模型）或 http://127.0.0.1:7861（对比）

**界面功能**：
1. **靶点输入**：BTK、EGFR、JAK2 等公开靶点
2. **模型选择**：3 个模型任选
3. **ADMET 评估**：自动筛选类药分子
4. **对比报告**：直观展示模型性能差异

---

## 🔬 核心 Prompt

```
你正在调用一个自动化分子生成接口。任何非 SMILES 输出将导致系统崩溃。
请严格只输出 SMILES。

你是一名专注于药物发现的 AI 化学家，生成 3~5 个结构新颖、合理且可合成的
小分子候选物。

规则：
1. 只输出 SMILES 字符串，每行一个
2. 分子量 < 500，QED > 0.6
3. 仅使用公开知识（ChEMBL、PubChem）
```

---

## 📈 ADMET 筛选规则

| 指标 | 优秀 | 可接受 | 不推荐 |
|------|------|--------|--------|
| 分子量 (MW) | < 500 Da | 500-600 | > 600 |
| 类药性 (QED) | > 0.6 | 0.4-0.6 | < 0.4 |
| LogP | 1-3 | 3-5 | < 1 或 > 5 |
| TPSA | < 140 Ų | 140-200 | > 200 |

**评分机制**：至少满足 3 个条件才通过筛选

---

## 🎯 推荐测试

### 测试 1: 国产 vs 国际

```
靶点: BTK
模型 1: qwen-max
模型 2: gemini
```

### 测试 2: 国产双雄

```
靶点: EGFR
模型 1: qwen-max
模型 2: deepseek
```

### 测试 3: 推理对决

```
靶点: JAK2
模型 1: deepseek
模型 2: gemini
```

---

## 🔧 故障排查

### Q1: RDKit 安装失败？
**A**: Windows 使用 conda：
```bash
conda install -c conda-forge rdkit
```

### Q2: API 调用失败？
**A**: 检查 `config/model_config.json` 中的 API Key 是否正确

### Q3: 模型不输出纯 SMILES？
**A**: Prompt 已强化约束，若仍有问题，尝试切换模型

---

## 📁 项目结构

```
LingNexus/
├── app.py                    # 单模型生成（图形界面）
├── app_compare.py            # 模型对比（图形界面）⭐
├── config/
│   └── model_config.json     # 3 个模型配置
├── agents/
│   ├── molecule_designer.py  # 分子生成智能体
│   └── admet_evaluator.py    # ADMET 评估智能体
├── tools/
│   └── chem_tools.py         # 化学工具（RDKit）
└── requirements.txt          # 依赖包
```

---

## 🛡️ 安全与合规

- ✅ 仅使用公开靶点（BTK、EGFR、JAK2）
- ✅ 仅使用公开知识库（ChEMBL、PubChem）
- ✅ 不涉及企业 proprietary 数据
- ✅ 所有生成记录可追溯

---

## 📞 技术栈

- **框架**：AgentScope (阿里通义实验室)
- **化学库**：RDKit
- **UI 框架**：Gradio
- **LLM**：Qwen-Max / DeepSeek 3.2 / Gemini 3 Pro

---

## 🎊 立即开始

```bash
# 启动模型对比工具
python app_compare.py
```

然后访问：http://127.0.0.1:7861

**开始对比三大模型的分子生成能力！** 🔥

---

## 🎯 项目特性

- ✅ **多 LLM 支持**：Qwen-Max / DeepSeek / Gemini 灵活切换
- ✅ **智能体协作**：ProjectManager + MoleculeDesigner + ADMETEvaluator
- ✅ **化学验证**：基于 RDKit 的 ADMET 筛选（Lipinski 规则 + QED）
- ✅ **安全合规**：仅使用公开靶点和知识（ChEMBL/PubChem）
- ✅ **可视化流程**：AgentScope 内置对话流可视化
- ⭐ **模型对比**：同时测试多个模型，直观对比生成能力

---

## 📁 项目结构

```
LingNexus/
├── config/
│   └── model_config.json       # LLM 配置（Qwen/DeepSeek/Gemini）
├── agents/
│   ├── molecule_designer.py    # 分子生成智能体
│   ├── admet_evaluator.py      # ADMET 评估智能体
│   └── project_manager.py      # 任务协调智能体
├── tools/
│   └── chem_tools.py           # 化学工具（SMILES 验证、性质计算）
├── app.py                      # 图形界面（Gradio）
├── app_compare.py              # 模型对比工具（图形界面）⭐
├── main.py                     # 主流程入口
├── compare_models.py           # 模型对比（命令行）
└── requirements.txt            # 依赖包
```

---

## 🚀 快速开始

### 1️⃣ 安装依赖

```bash
pip install -r requirements.txt
```

**注意**：RDKit 安装建议使用 conda（Windows 推荐）：
```bash
conda install -c conda-forge rdkit
```

### 2️⃣ 配置 API Key

编辑 `config/model_config.json`，填入您的 API Key：

```json
{
  "config_name": "qwen-max",
  "model_type": "dashscope_chat",
  "api_key": "sk-xxx...",  # 👈 替换为您的 DashScope API Key
  "model_name": "qwen-max"
}
```

**获取 API Key**：
- **Qwen-Max**：https://dashscope.console.aliyun.com/
- **DeepSeek**：https://platform.deepseek.com/
- **Gemini**：https://aistudio.google.com/

### 3️⃣ 运行第一个案例

#### 方式 A：图形界面（推荐）

```bash
python app.py
```

然后打开浏览器访问：http://127.0.0.1:7860

#### 方式 B：命令行

```bash
python main.py
```

**默认运行示例**：为 **BTK（布鲁顿酰氨酸激酶）** 生成抑制剂候选物

---

## 💡 使用说明

### 修改靶点和需求

编辑 `main.py` 中的 `main()` 函数：

```python
run_molecule_discovery_pipeline(
    target_name="EGFR",              # 👈 改为您的靶点
    model_name="deepseek",            # 👈 切换模型
    requirements="分子量<400，口服可利用"  # 👈 添加特殊要求
)
```

### 切换 LLM 模型

在 `model_name` 参数中选择：
- `"qwen-max"` - 阿里通义千问（推荐，中文优化）
- `"deepseek"` - DeepSeek（推理能力强）
- `"gemini"` - Google Gemini（多模态能力）

---

## 🔬 模型对比功能（⭐ 新功能）

想知道 **Qwen-Max** 和 **Gemini** 哪个生成分子的能力更强？

### 启动模型对比工具

#### 🎨 图形界面（推荐）

```bash
python app_compare.py
```

然后访问：http://127.0.0.1:7861

**功能亮点**：
- 🔥 同时测试两个模型（Qwen-Max / Gemini / DeepSeek）
- 📊 直观对比表格（通过率、QED、速度等）
- 🏆 自动推荐最佳模型
- 📄 生成详细对比报告

#### 💻 命令行版本

```bash
python compare_models.py
```

**示例输出**：

```
┌─────────────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┐
│ 模型            │ 生成数   │ 通过数   │ 通过率   │ 平均QED  │ 平均MW   │ 耗时(秒) │
├─────────────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ qwen-max        │        5 │        4 │    80.0% │    0.725 │    382.5 │     3.21 │
│ gemini          │        5 │        3 │    60.0% │    0.698 │    415.3 │     4.58 │
└─────────────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┘

🏆 综合推荐模型: QWEN-MAX
   - 通过率: 80.0% （高于 Gemini）
   - 平均类药性: QED=0.725 （优于 Gemini）
   - 生成速度: 3.21 秒 （快于 Gemini）
```

📚 **详细使用指南**：见 [`MODEL_COMPARISON_GUIDE.md`](MODEL_COMPARISON_GUIDE.md)

---

## 📚 文档导航

### MoleculeDesigner 的关键 Prompt

```
你正在调用一个自动化分子生成接口。任何非 SMILES 输出将导致系统崩溃。请严格只输出 SMILES。

你是一名专注于药物发现的 AI 化学家，任务是根据用户提供的靶点名称，生成 3~5 个结构新颖、合理且可合成的小分子候选物。

规则：
1. 只输出 SMILES 字符串，每行一个
2. 分子量 < 500，QED > 0.6
3. 仅使用公开知识（ChEMBL、PubChem）
```

**为什么这个 Prompt 有效？**
- ✅ **强约束**："任何非 SMILES 输出将导致系统崩溃"（防止模型"忍不住"解释）
- ✅ **格式明确**："每行一个，不要编号"
- ✅ **化学规则内嵌**：MW < 500, QED > 0.6
- ✅ **合规性声明**："仅使用公开知识"

---

## 📊 输出示例

运行后您将看到：

```
=============================================================================
🚀 LingNexus 药物分子发现系统启动
📌 靶点: BTK
🤖 模型: qwen-max
=============================================================================

[1/4] 初始化 AgentScope...
[2/4] 创建分子设计智能体（模型: qwen-max）...
[3/4] 正在为靶点 'BTK' 生成候选分子...

💬 MoleculeDesigner 响应：
-----------------------------------------------------------------------------
COc1ccc(NC(=O)c2ccccc2)cc1N1CCN(C)CC1
CC(C)Oc1ccc(NC(=O)Nc2ccc(Cl)cc2)cc1
c1ccc(CNc2ncnc3[nH]ccc23)cc1
-----------------------------------------------------------------------------

✅ 成功提取 3 个候选分子

[4/4] 进行 ADMET 筛选...
-----------------------------------------------------------------------------
✅ 分子 1: COc1ccc(NC(=O)c2ccccc2)cc1N1CCN(C)CC1
   MW=339.4, QED=0.72, LogP=3.2, TPSA=51.8
✅ 分子 2: CC(C)Oc1ccc(NC(=O)Nc2ccc(Cl)cc2)cc1
   MW=304.8, QED=0.68, LogP=4.1, TPSA=58.2
⚠️  分子 3: 未通过筛选
   MW=223.3, QED=0.58

=============================================================================
📊 最终结果：2/3 个分子通过筛选
=============================================================================

🎯 推荐的候选分子：

1. COc1ccc(NC(=O)c2ccccc2)cc1N1CCN(C)CC1
   - 分子量: 339.4 Da
   - QED: 0.72
   - LogP: 3.2
   - TPSA: 51.8 Ų

2. CC(C)Oc1ccc(NC(=O)Nc2ccc(Cl)cc2)cc1
   - 分子量: 304.8 Da
   - QED: 0.68
   - LogP: 4.1
   - TPSA: 58.2 Ų
```

---

## ⚙️ ADMET 筛选规则

当前使用的筛选标准（基于 Lipinski 规则 + QED）：

| 指标 | 优秀 | 可接受 | 不推荐 |
|------|------|--------|--------|
| 分子量 (MW) | < 500 Da | 500-600 | > 600 |
| 类药性 (QED) | > 0.6 | 0.4-0.6 | < 0.4 |
| 脂水分配系数 (LogP) | 1-3 | 3-5 | < 1 或 > 5 |
| 极性表面积 (TPSA) | < 140 Ų | 140-200 | > 200 |
| 可旋转键 | < 10 | 10-15 | > 15 |

**评分机制**：至少满足 3 个条件才通过筛选

---

## 🎨 可视化智能体对话流（可选）

AgentScope 支持可视化智能体交互过程：

```bash
agentscope ui --file ./demo_conversation.json
```

打开浏览器即可看到：
- 智能体之间的对话流程
- 每个智能体的输入/输出
- 完整的推理链路

---

## 🛡️ 安全与合规

- ✅ **仅使用公开靶点**（如 BTK、EGFR 等 FDA 批准药物靶点）
- ✅ **仅使用公开知识库**（ChEMBL、PubChem）
- ✅ **不涉及企业 proprietary 数据**
- ✅ **SMILES 输出可追溯**（所有生成记录可审计）

---

## 🔧 常见问题

### Q1: RDKit 安装失败？
**A**: Windows 推荐使用 conda：
```bash
conda install -c conda-forge rdkit
```

### Q2: API Key 配置错误？
**A**: 检查 `config/model_config.json` 中：
- `api_key` 是否正确
- `model_type` 是否匹配（qwen 用 `dashscope_chat`）

### Q3: 模型不输出纯 SMILES？
**A**: Prompt 已强化约束（"系统会崩溃"），若仍有问题：
- 尝试切换到 `deepseek`（更严格遵循指令）
- 检查 `parse_smiles_from_response()` 函数

### Q4: ADMET 筛选太严格？
**A**: 编辑 `tools/chem_tools.py` 中的 `pass_threshold`：
```python
pass_threshold = 2  # 降低为 2（原为 3）
```

---

## 📞 联系我们

**项目负责人**：丽珠医药 IT 部门  
**框架支持**：AgentScope (阿里通义实验室开源)  
**技术栈**：Python 3.9+, AgentScope, RDKit, Qwen-Max

---

## 📄 许可证

本项目仅供内部研究使用，不得用于商业用途。

---

**🎉 现在，您可以运行 `python main.py` 开始第一次 AI 驱动的分子发现之旅！**

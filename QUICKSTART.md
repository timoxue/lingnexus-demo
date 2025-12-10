# 🚀 LingNexus 快速开始

## 🎯 三步开始

### 第 1 步：安装依赖

```powershell
pip install -r requirements.txt

# Windows 推荐使用 conda 安装 RDKit
conda install -c conda-forge rdkit
```

---

### 第 2 步：配置 API Key

编辑 `config/model_config.json`，填入三个模型的 API Key：

```json
[
  {
    "config_name": "qwen-max",
    "api_key": "YOUR_QWEN_API_KEY"  // 👈 这里
  },
  {
    "config_name": "deepseek",
    "api_key": "YOUR_DEEPSEEK_API_KEY"  // 👈 这里
  },
  {
    "config_name": "gemini",
    "api_key": "YOUR_GEMINI_API_KEY"  // 👈 这里
  }
]
```

**获取 API Key**：
- Qwen-Max：https://dashscope.console.aliyun.com/
- DeepSeek：https://platform.deepseek.com/
- Gemini：https://aistudio.google.com/

---

### 第 3 步：启动图形界面

#### 方式 A：双击批处理文件（推荐）

- `启动图形界面.bat` - 单模型生成
- `启动模型对比工具.bat` - 模型对比 ⭐

#### 方式 B：命令行

```powershell
# 单模型生成
python app.py

# 模型对比（推荐）
python app_compare.py
```

**访问地址**：
- 单模型：http://127.0.0.1:7860
- 模型对比：http://127.0.0.1:7861

---

## 📊 三大模型

| 模型 | 说明 | 特点 |
|------|------|------|
| **qwen-max** 🇨🇳 | 阿里通义千问 | 中文优化，格式规范 |
| **deepseek** 🧠 | DeepSeek 3.2 | 推理能力强 |
| **gemini** 🔥 | Gemini 3 Pro Preview | 最新最强，质量最高 |

---

## 🎯 推荐测试

### 测试 1：国产 vs 国际

```
靶点: BTK
模型 1: qwen-max
模型 2: gemini
```

### 测试 2：国产双雄

```
靶点: EGFR
模型 1: qwen-max
模型 2: deepseek
```

### 测试 3：推理对决

```
靶点: JAK2
模型 1: deepseek
模型 2: gemini
```

---

## 🛠️ 常见问题

### Q1: RDKit 安装失败？
```powershell
conda install -c conda-forge rdkit
```

### Q2: API 调用失败？
检查 `config/model_config.json` 中的 API Key

### Q3: 如何切换模型？
在图形界面的下拉框中选择

---

## ✨ 立即开始

```powershell
python app_compare.py
```

**开始对比三大模型的分子生成能力！** 🔥

## 第一步：安装依赖

### 方法 1：使用 pip（推荐）
```powershell
pip install -r requirements.txt
```

### 方法 2：使用 conda（适合安装 RDKit）
```powershell
conda create -n lingnexus python=3.9
conda activate lingnexus
conda install -c conda-forge rdkit
pip install agentscope dashscope gradio openai
```

---

## 第二步：配置 API Key

### 选项 A：直接编辑配置文件
打开 `config/model_config.json`，找到您要使用的模型：

```json
{
  "config_name": "qwen-max",
  "model_type": "dashscope_chat",
  "api_key": "sk-xxx...",  # 👈 替换为您的真实 API Key
  "model_name": "qwen-max"
}
```

### 选项 B：使用环境变量
```powershell
# 复制示例文件
copy .env.example .env

# 编辑 .env 文件，填入 API Key
notepad .env
```

### API Key 获取地址：
- **Qwen-Max**：https://dashscope.console.aliyun.com/
- **DeepSeek**：https://platform.deepseek.com/
- **Gemini**：https://aistudio.google.com/

---

## 第三步：运行项目

### 🎨 方式 1：图形界面（推荐，适合演示）

```powershell
python app.py
```

然后在浏览器打开：http://127.0.0.1:7860

**界面功能**：
- ✅ 输入靶点名称（如 BTK）
- ✅ 选择 LLM 模型（Qwen-Max / DeepSeek / Gemini）
- ✅ 设置特殊要求（可选）
- ✅ 一键生成 + 自动评估
- ✅ 可视化 ADMET 结果

---

### 💻 方式 2：命令行版本（适合批量处理）

```powershell
python main.py
```

**修改靶点**：编辑 `main.py` 中的 `main()` 函数：

```python
run_molecule_discovery_pipeline(
    target_name="EGFR",              # 👈 改为您的靶点
    model_name="deepseek",            # 👈 切换模型
    requirements="分子量<400"         # 👈 添加要求
)
```

---

## 第四步：验证结果

成功运行后，您将看到：

```
=============================================================================
🚀 LingNexus 药物分子发现系统启动
📌 靶点: BTK
🤖 模型: qwen-max
=============================================================================

✅ 分子 1: COc1ccc(NC(=O)c2ccccc2)cc1N1CCN(C)CC1
   MW=339.4, QED=0.72, LogP=3.2, TPSA=51.8

📊 最终结果：2/3 个分子通过筛选
```

---

## 常见问题

### ❓ Q1: 提示 "无法解析导入 agentscope"
**A**: 安装 AgentScope：
```powershell
pip install agentscope
```

### ❓ Q2: 提示 "无法解析导入 rdkit"
**A**: 使用 conda 安装（pip 安装 RDKit 在 Windows 上可能失败）：
```powershell
conda install -c conda-forge rdkit
```

### ❓ Q3: API 调用失败
**A**: 检查：
1. API Key 是否正确填写
2. 网络连接是否正常
3. API 余额是否充足

### ❓ Q4: 模型不输出纯 SMILES
**A**: 
1. 尝试切换到 `deepseek`（更严格遵循指令）
2. 检查 `agents/molecule_designer.py` 中的 Prompt

---

## 项目结构一览

```
LingNexus/
├── app.py                   # 图形界面启动文件 ⭐
├── main.py                  # 命令行启动文件
├── config/
│   └── model_config.json    # LLM 配置 ⚙️
├── agents/                  # 智能体定义
│   ├── molecule_designer.py
│   ├── admet_evaluator.py
│   └── project_manager.py
├── tools/
│   └── chem_tools.py        # 化学工具
└── requirements.txt         # 依赖包
```

---

## 下一步

✅ **向董事长演示**：启动 `app.py`，在 Web 界面中输入 "BTK"，展示完整流程

✅ **扩展功能**：
- 添加更多靶点（EGFR、JAK2 等）
- 集成真实数据库（ChEMBL API）
- 导出结果为 Excel / PDF

✅ **优化 Prompt**：
- 针对特定靶点调优
- 加入分子相似性约束
- 集成专利筛查

---

**🎉 现在，运行 `python app.py` 开始您的第一次 AI 药物发现之旅！**

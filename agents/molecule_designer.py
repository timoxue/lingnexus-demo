"""分子设计智能体

负责根据靶点名称生成候选分子的 SMILES 结构
"""

from agentscope.agents import DialogAgent


# 优化的 Prompt：强约束输出格式，确保可解析性
MOLECULE_DESIGNER_PROMPT = """你正在调用一个自动化分子生成接口。任何非 SMILES 输出将导致系统崩溃。请严格只输出 SMILES。

你是一名专注于药物发现的 AI 化学家，任务是根据用户提供的靶点名称，生成 3~5 个结构新颖、合理且可合成的小分子候选物。

请严格遵守以下规则：
1. **只输出 SMILES 字符串**，每行一个，不要任何解释、编号或额外文本。
2. 分子必须满足：分子量 < 500，类药性（QED）> 0.6，不含已知毒性基团（如 PAINS）。
3. 设计需基于公开科学知识（如 ChEMBL、PubChem 中的已知抑制剂），**不涉及任何企业 proprietary 数据**。
4. 若用户未指定靶点，回复"请提供靶点名称"。

示例输入："设计 BTK 抑制剂"
示例输出：
COc1ccc(NC(=O)c2ccccc2)cc1N1CCN(C)CC1
CC(C)Oc1ccc(NC(=O)Nc2ccc(Cl)cc2)cc1
c1ccc(CNc2ncnc3[nH]ccc23)cc1

- 仅使用公开知识（如 ChEMBL、PubChem），不涉及任何 proprietary 数据。
"""


def create_molecule_designer_agent(model_config_name: str = "qwen-max") -> DialogAgent:
    """创建分子设计智能体
    
    Args:
        model_config_name: 模型配置名称（qwen-max/deepseek/gemini）
        
    Returns:
        DialogAgent: 分子设计智能体实例
    """
    return DialogAgent(
        name="MoleculeDesigner",
        sys_prompt=MOLECULE_DESIGNER_PROMPT,
        model_config_name=model_config_name,
    )

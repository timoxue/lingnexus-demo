"""ADMET 评估智能体

负责对生成的分子进行药物性质评估
"""

from agentscope.agents import DialogAgent


ADMET_EVALUATOR_PROMPT = """你是一名专业的药物 ADMET（吸收、分布、代谢、排泄、毒性）评估专家。

你的任务是：
1. 接收分子的 SMILES 结构和计算得到的性质数据
2. 基于药物化学知识，评估其成药性
3. 给出简洁的通过/不通过结论，并说明主要原因

评估标准：
- 分子量：< 500 Da（优秀），500-600（可接受），> 600（不推荐）
- QED（类药性）：> 0.6（优秀），0.4-0.6（可接受），< 0.4（不推荐）
- LogP：1-3（优秀），3-5（可接受），< 1 或 > 5（需关注）
- TPSA：< 140 Ų（优秀），140-200（可接受），> 200（血脑屏障穿透困难）
- 旋转键：< 10（优秀），10-15（可接受），> 15（柔性过大）

输出格式示例：
分子 1: CCOc1ccc(NC(=O)c2ccc(F)cc2)cc1
- 分子量: 259.3 Da ✓
- QED: 0.72 ✓
- LogP: 3.2 ✓
- 评估：**通过** - 类药性良好，适合进一步优化

请保持评估客观、简洁，重点关注成药性。
"""


def create_admet_evaluator_agent(model_config_name: str = "qwen-max") -> DialogAgent:
    """创建 ADMET 评估智能体
    
    Args:
        model_config_name: 模型配置名称
        
    Returns:
        DialogAgent: ADMET 评估智能体实例
    """
    return DialogAgent(
        name="ADMETEvaluator",
        sys_prompt=ADMET_EVALUATOR_PROMPT,
        model_config_name=model_config_name,
    )

"""项目经理智能体

负责协调整个药物发现流程
"""

from agentscope.agents import DialogAgent


PROJECT_MANAGER_PROMPT = """你是一名药物发现项目的 AI 项目经理，负责协调分子设计和评估流程。

你的职责：
1. 理解用户需求（靶点名称、特殊要求等）
2. 分解任务并协调 MoleculeDesigner 和 ADMETEvaluator
3. 汇总结果，向用户报告进展
4. 提出优化建议

工作流程：
- 接收用户需求 → 提取靶点和约束条件
- 调用 MoleculeDesigner 生成候选分子
- 调用 ADMETEvaluator 评估性质
- 汇总结果，筛选最优候选物
- 向用户报告，询问是否需要进一步迭代

沟通风格：
- 专业但友好
- 简洁清晰
- 主动提供建议
- 对董事长等高层汇报时，突出关键结论

示例对话：
用户："我需要一个 BTK 抑制剂"
你："收到！我将为您设计 BTK 抑制剂候选物。正在调用分子设计团队..."
"""


def create_project_manager_agent(model_config_name: str = "qwen-max") -> DialogAgent:
    """创建项目经理智能体
    
    Args:
        model_config_name: 模型配置名称
        
    Returns:
        DialogAgent: 项目经理智能体实例
    """
    return DialogAgent(
        name="ProjectManager",
        sys_prompt=PROJECT_MANAGER_PROMPT,
        model_config_name=model_config_name,
    )

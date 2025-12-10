"""LingNexus 图形界面版本

基于 Gradio 的 Web UI，提供可视化的药物分子发现交互界面
"""

try:
    import gradio as gr
except ImportError:
    print("错误：未安装 Gradio。请运行：pip install gradio")
    exit(1)

import agentscope
from agentscope.message import Msg
from agents.molecule_designer import create_molecule_designer_agent
from agents.admet_evaluator import create_admet_evaluator_agent
from tools.chem_tools import admet_filter, calculate_molecular_properties
import re
from typing import Tuple, List


# 初始化标志
_initialized = False


def initialize_agentscope():
    """初始化 AgentScope（只执行一次）"""
    global _initialized
    if not _initialized:
        agentscope.init(
            model_configs="./config/model_config.json",
            project="LingNexus",
            save_code=False,
            save_api_invoke=False,
        )
        _initialized = True


def parse_smiles_from_response(response_text: str) -> List[str]:
    """从智能体响应中提取 SMILES"""
    lines = response_text.strip().split('\n')
    smiles_list = []
    
    for line in lines:
        line = line.strip()
        if not line or '请提供' in line or len(line) < 5:
            continue
        line = re.sub(r'^[\d\-\.\)]+\s*', '', line)
        
        if line and not line.startswith(('#', '//')):
            smiles_list.append(line)
    
    return smiles_list


def generate_molecules(
    target_name: str,
    model_name: str,
    requirements: str,
    progress=gr.Progress()
) -> Tuple[str, str, str]:
    """生成分子并评估（图形界面回调函数）
    
    Returns:
        Tuple[str, str, str]: (状态信息, 生成的SMILES, 评估结果)
    """
    
    if not target_name.strip():
        return "❌ 错误：请输入靶点名称", "", ""
    
    try:
        # 1. 初始化
        progress(0.1, desc="初始化 AgentScope...")
        initialize_agentscope()
        
        # 2. 创建智能体
        progress(0.2, desc="创建分子设计智能体...")
        designer = create_molecule_designer_agent(model_config_name=model_name)
        evaluator = create_admet_evaluator_agent(model_config_name=model_name)
        
        # 3. 生成分子
        progress(0.4, desc=f"正在为 {target_name} 生成候选分子...")
        user_request = f"设计 {target_name} 抑制剂"
        if requirements:
            user_request += f"，{requirements}"
        
        user_msg = Msg(name="User", content=user_request, role="user")
        designer_response = designer(user_msg)
        
        raw_response = designer_response.content
        
        # 4. 解析 SMILES
        progress(0.6, desc="解析 SMILES 结构...")
        smiles_list = parse_smiles_from_response(raw_response)
        
        if not smiles_list:
            return (
                "❌ 错误：未能从模型响应中提取有效的 SMILES",
                raw_response,
                "无法进行评估"
            )
        
        # 5. ADMET 筛选
        progress(0.8, desc="进行 ADMET 筛选...")
        passed_molecules = admet_filter(smiles_list, verbose=False)
        
        # 6. 格式化输出
        progress(1.0, desc="完成！")
        
        # 状态信息
        status = f"""
✅ 成功完成分子生成与评估

📌 靶点：{target_name}
🤖 模型：{model_name}
📊 生成：{len(smiles_list)} 个候选分子
✅ 通过：{len(passed_molecules)} 个分子通过 ADMET 筛选
        """
        
        # SMILES 列表
        smiles_output = "### 生成的 SMILES 结构\n\n"
        for idx, smi in enumerate(smiles_list, 1):
            smiles_output += f"{idx}. `{smi}`\n"
        
        # 评估结果
        if passed_molecules:
            eval_output = "### ✅ 通过 ADMET 筛选的候选分子\n\n"
            
            for idx, mol_data in enumerate(passed_molecules, 1):
                props = mol_data['properties']
                eval_output += f"""
**分子 {idx}**: `{mol_data['smiles']}`

| 指标 | 数值 | 状态 |
|------|------|------|
| 分子量 (MW) | {props['molecular_weight']:.1f} Da | {'✅' if props['molecular_weight'] < 500 else '⚠️'} |
| 类药性 (QED) | {props['qed']:.3f} | {'✅' if props['qed'] > 0.6 else '⚠️'} |
| LogP | {props['logp']:.2f} | {'✅' if 1 <= props['logp'] <= 5 else '⚠️'} |
| TPSA | {props['tpsa']:.1f} Ų | {'✅' if props['tpsa'] < 140 else '⚠️'} |
| 可旋转键 | {props['rotatable_bonds']} | {'✅' if props['rotatable_bonds'] < 10 else '⚠️'} |

---
"""
            
            # 请 AI 专家点评
            eval_prompt = f"请评估以下 {len(passed_molecules)} 个 {target_name} 抑制剂候选物：\n\n"
            for idx, mol_data in enumerate(passed_molecules, 1):
                props = mol_data['properties']
                eval_prompt += f"分子 {idx}: {mol_data['smiles']}\n"
                eval_prompt += f"- 分子量: {props['molecular_weight']:.1f} Da\n"
                eval_prompt += f"- QED: {props['qed']:.2f}\n"
                eval_prompt += f"- LogP: {props['logp']:.2f}\n\n"
            
            eval_msg = Msg(name="System", content=eval_prompt, role="user")
            eval_response = evaluator(eval_msg)
            
            eval_output += f"\n### 🔬 ADMET 专家评估\n\n{eval_response.content}"
            
        else:
            eval_output = "### ⚠️ 无分子通过筛选\n\n所有候选分子均未通过 ADMET 筛选。建议：\n- 放宽筛选条件\n- 调整生成要求\n- 重新生成"
        
        return status, smiles_output, eval_output
        
    except Exception as e:
        return f"❌ 错误：{str(e)}", "", ""


def create_demo():
    """创建 Gradio 界面"""
    
    with gr.Blocks(
        title="LingNexus - AI 药物分子发现系统",
        theme=gr.themes.Soft()
    ) as demo:
        
        gr.Markdown("""
# 🧬 LingNexus - AI 驱动的药物分子发现系统

> 基于 AgentScope 框架 + 多智能体协作
> 
> **流程**：靶点输入 → AI 生成分子 → ADMET 自动评估 → 推荐候选物
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 📝 输入参数")
                
                target_input = gr.Textbox(
                    label="靶点名称",
                    placeholder="例如：BTK, EGFR, JAK2",
                    value="BTK",
                    info="请输入公开靶点名称"
                )
                
                model_choice = gr.Dropdown(
                    label="LLM 模型",
                    choices=["qwen-max", "deepseek", "gemini"],
                    value="qwen-max",
                    info="选择生成模型 (🔥 gemini = Gemini 3 Pro Preview)"
                )
                
                requirements_input = gr.Textbox(
                    label="特殊要求（可选）",
                    placeholder="例如：分子量<400，高选择性，口服可利用",
                    lines=2
                )
                
                generate_btn = gr.Button(
                    "🚀 生成候选分子",
                    variant="primary",
                    size="lg"
                )
                
                status_output = gr.Textbox(
                    label="状态",
                    lines=8,
                    interactive=False
                )
        
            with gr.Column(scale=2):
                gr.Markdown("### 📊 生成结果")
                
                with gr.Tab("SMILES 结构"):
                    smiles_output = gr.Markdown()
                
                with gr.Tab("ADMET 评估"):
                    eval_output = gr.Markdown()
        
        # 绑定事件
        generate_btn.click(
            fn=generate_molecules,
            inputs=[target_input, model_choice, requirements_input],
            outputs=[status_output, smiles_output, eval_output]
        )
        
        # 示例
        gr.Markdown("""
---
### 💡 使用建议

1. **安全靶点示例**：BTK、EGFR、JAK2
2. **三大模型**：
   - `qwen-max`：🇨🇳 阿里通义千问（中文优化）
   - `deepseek`：🧠 DeepSeek 3.2（推理能力强）
   - `gemini`：🔥 Gemini 3 Pro Preview（最新最强）
3. **ADMET 筛选**：分子量<500、QED>0.6、LogP 1-5

**⚠️ 注意**：首次运行需配置 API Key（见 `config/model_config.json`）
        """)
    
    return demo


if __name__ == "__main__":
    demo = create_demo()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True
    )
    print("\n✨ LingNexus 图形界面已启动！")
    print("🌐 访问地址：http://127.0.0.1:7860")

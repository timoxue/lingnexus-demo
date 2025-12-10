"""LingNexus 模型对比图形界面

同时使用多个模型（Qwen-Max, Gemini, DeepSeek）生成分子并对比性能
"""

try:
    import gradio as gr
except ImportError:
    print("错误：未安装 Gradio。请运行：pip install gradio")
    exit(1)

import agentscope
from agentscope.message import Msg
from agents.molecule_designer import create_molecule_designer_agent
from tools.chem_tools import admet_filter, calculate_molecular_properties
import re
import time
from typing import List, Tuple, Dict


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


def compare_models_ui(
    target_name: str,
    model1: str,
    model2: str,
    requirements: str,
    progress=gr.Progress()
) -> Tuple[str, str, str]:
    """图形界面：对比两个模型的分子生成能力
    
    Returns:
        Tuple[str, str, str]: (对比报告, 模型1结果, 模型2结果)
    """
    
    if not target_name.strip():
        return "❌ 错误：请输入靶点名称", "", ""
    
    try:
        # 初始化
        progress(0.05, desc="初始化 AgentScope...")
        initialize_agentscope()
        
        # 准备请求
        user_request = f"设计 {target_name} 抑制剂"
        if requirements:
            user_request += f"，{requirements}"
        
        models = [model1, model2]
        results = {}
        
        # 测试每个模型
        for idx, model_name in enumerate(models):
            progress_val = 0.1 + (idx * 0.4)
            progress(progress_val, desc=f"正在测试 {model_name.upper()}...")
            
            try:
                # 创建智能体
                designer = create_molecule_designer_agent(model_config_name=model_name)
                
                # 生成分子
                start_time = time.time()
                user_msg = Msg(name="User", content=user_request, role="user")
                designer_response = designer(user_msg)
                end_time = time.time()
                
                generation_time = end_time - start_time
                
                # 解析 SMILES
                smiles_list = parse_smiles_from_response(designer_response.content)
                
                if not smiles_list:
                    results[model_name] = {
                        "success": False,
                        "error": "无法提取 SMILES",
                        "raw_response": designer_response.content
                    }
                    continue
                
                # ADMET 评估
                passed_molecules = admet_filter(smiles_list, verbose=False)
                
                # 计算统计
                pass_rate = len(passed_molecules) / len(smiles_list) * 100 if smiles_list else 0
                
                if passed_molecules:
                    avg_mw = sum(m['properties']['molecular_weight'] for m in passed_molecules) / len(passed_molecules)
                    avg_qed = sum(m['properties']['qed'] for m in passed_molecules) / len(passed_molecules)
                    avg_logp = sum(m['properties']['logp'] for m in passed_molecules) / len(passed_molecules)
                else:
                    avg_mw = avg_qed = avg_logp = 0
                
                results[model_name] = {
                    "success": True,
                    "generated_count": len(smiles_list),
                    "passed_count": len(passed_molecules),
                    "pass_rate": pass_rate,
                    "generation_time": generation_time,
                    "smiles_list": smiles_list,
                    "passed_molecules": passed_molecules,
                    "avg_mw": avg_mw,
                    "avg_qed": avg_qed,
                    "avg_logp": avg_logp,
                    "raw_response": designer_response.content
                }
                
            except Exception as e:
                results[model_name] = {
                    "success": False,
                    "error": str(e)
                }
        
        progress(0.95, desc="生成对比报告...")
        
        # 生成对比报告
        report = generate_comparison_report(target_name, models, results)
        
        # 生成详细结果
        model1_detail = generate_model_detail(model1, results.get(model1, {}))
        model2_detail = generate_model_detail(model2, results.get(model2, {}))
        
        progress(1.0, desc="完成！")
        
        return report, model1_detail, model2_detail
        
    except Exception as e:
        return f"❌ 错误：{str(e)}", "", ""


def generate_comparison_report(target_name: str, models: List[str], results: Dict) -> str:
    """生成 Markdown 格式的对比报告"""
    
    report = f"""# 🔬 模型对比报告

**靶点**: {target_name}  
**对比模型**: {models[0].upper()} vs {models[1].upper()}

---

## 📊 性能对比表

| 指标 | {models[0].upper()} | {models[1].upper()} | 优势 |
|------|---------|---------|------|
"""
    
    # 提取结果
    r1 = results.get(models[0], {})
    r2 = results.get(models[1], {})
    
    if r1.get("success") and r2.get("success"):
        # 生成数量
        winner = "🏆" if r1['generated_count'] >= r2['generated_count'] else ""
        winner2 = "🏆" if r2['generated_count'] > r1['generated_count'] else ""
        report += f"| 生成分子数 | {r1['generated_count']} {winner} | {r2['generated_count']} {winner2} | {'平局' if winner == winner2 else (models[0].upper() if winner else models[1].upper())} |\n"
        
        # 通过数量
        winner = "🏆" if r1['passed_count'] >= r2['passed_count'] else ""
        winner2 = "🏆" if r2['passed_count'] > r1['passed_count'] else ""
        report += f"| 通过筛选数 | {r1['passed_count']} {winner} | {r2['passed_count']} {winner2} | {'平局' if winner == winner2 else (models[0].upper() if winner else models[1].upper())} |\n"
        
        # 通过率
        winner = "🏆" if r1['pass_rate'] >= r2['pass_rate'] else ""
        winner2 = "🏆" if r2['pass_rate'] > r1['pass_rate'] else ""
        report += f"| 通过率 | {r1['pass_rate']:.1f}% {winner} | {r2['pass_rate']:.1f}% {winner2} | {'平局' if abs(r1['pass_rate'] - r2['pass_rate']) < 1 else (models[0].upper() if winner else models[1].upper())} |\n"
        
        # 平均 QED
        if r1['passed_count'] > 0 and r2['passed_count'] > 0:
            winner = "🏆" if r1['avg_qed'] >= r2['avg_qed'] else ""
            winner2 = "🏆" if r2['avg_qed'] > r1['avg_qed'] else ""
            report += f"| 平均类药性(QED) | {r1['avg_qed']:.3f} {winner} | {r2['avg_qed']:.3f} {winner2} | {models[0].upper() if winner else models[1].upper()} |\n"
        
        # 平均分子量
        if r1['passed_count'] > 0 and r2['passed_count'] > 0:
            winner = "✓" if abs(r1['avg_mw'] - 400) <= abs(r2['avg_mw'] - 400) else ""
            winner2 = "✓" if abs(r2['avg_mw'] - 400) < abs(r1['avg_mw'] - 400) else ""
            report += f"| 平均分子量(MW) | {r1['avg_mw']:.1f} {winner} | {r2['avg_mw']:.1f} {winner2} | {models[0].upper() if winner else models[1].upper()} |\n"
        
        # 生成速度
        winner = "🏆" if r1['generation_time'] <= r2['generation_time'] else ""
        winner2 = "🏆" if r2['generation_time'] < r1['generation_time'] else ""
        report += f"| 生成速度(秒) | {r1['generation_time']:.2f} {winner} | {r2['generation_time']:.2f} {winner2} | {models[0].upper() if winner else models[1].upper()} |\n"
        
        report += "\n---\n\n"
        
        # 输出格式质量
        report += "## 📝 输出格式质量\n\n"
        
        for model_name in models:
            r = results[model_name]
            raw_text = r['raw_response']
            
            has_explanation = any(keyword in raw_text for keyword in 
                                 ['分子', '抑制剂', '设计', '具有', '该', '这', '可以', 'The', 'This'])
            has_numbering = bool(re.search(r'^\d+[\.\)、]', raw_text, re.MULTILINE))
            
            report += f"**{model_name.upper()}**: "
            if not has_explanation and not has_numbering:
                report += "✅ 优秀（纯 SMILES，无解释）\n\n"
            elif not has_explanation:
                report += "⚠️ 良好（有编号，但无解释）\n\n"
            else:
                report += "⚠️ 一般（包含解释性文字）\n\n"
        
        report += "---\n\n"
        
        # 综合评分
        report += "## 🏆 综合评分\n\n"
        
        scores = {}
        for model in models:
            r = results[model]
            # 综合评分：通过率(40%) + QED(30%) + 速度(30%)
            score = (r['pass_rate'] / 100) * 40
            if r['passed_count'] > 0:
                score += (r['avg_qed'] / 1.0) * 30
            # 速度分数（越快越好）
            max_time = max(r1['generation_time'], r2['generation_time'])
            if max_time > 0:
                score += (1 - r['generation_time'] / max_time) * 30
            scores[model] = score
        
        for model in models:
            report += f"- **{model.upper()}**: {scores[model]:.1f} 分\n"
        
        best_model = max(scores, key=lambda k: scores[k])
        report += f"\n**🎯 推荐**: {best_model.upper()}\n\n"
        
        # 使用建议
        report += "---\n\n## 💡 使用建议\n\n"
        
        if r1['pass_rate'] > r2['pass_rate'] + 10:
            report += f"- **{models[0].upper()}** 通过率明显更高，适合需要大量高质量候选物的场景\n"
        elif r2['pass_rate'] > r1['pass_rate'] + 10:
            report += f"- **{models[1].upper()}** 通过率明显更高，适合需要大量高质量候选物的场景\n"
        
        if r1['generation_time'] < r2['generation_time'] * 0.7:
            report += f"- **{models[0].upper()}** 速度快，适合快速原型设计和批量生成\n"
        elif r2['generation_time'] < r1['generation_time'] * 0.7:
            report += f"- **{models[1].upper()}** 速度快，适合快速原型设计和批量生成\n"
        
        if r1['passed_count'] > 0 and r2['passed_count'] > 0:
            if r1['avg_qed'] > r2['avg_qed'] + 0.05:
                report += f"- **{models[0].upper()}** 平均类药性更好，适合质量优先的筛选\n"
            elif r2['avg_qed'] > r1['avg_qed'] + 0.05:
                report += f"- **{models[1].upper()}** 平均类药性更好，适合质量优先的筛选\n"
    
    else:
        # 有模型失败
        for model in models:
            r = results.get(model, {})
            if not r.get("success"):
                report += f"\n❌ **{model.upper()}** 运行失败: {r.get('error', '未知错误')}\n"
    
    return report


def generate_model_detail(model_name: str, result: Dict) -> str:
    """生成单个模型的详细结果"""
    
    if not result.get("success"):
        return f"""# ❌ {model_name.upper()} - 运行失败

**错误**: {result.get('error', '未知错误')}

---

## 原始响应

```
{result.get('raw_response', '无响应')}
```
"""
    
    detail = f"""# 🤖 {model_name.upper()} - 详细结果

## 📊 统计信息

- **生成分子数**: {result['generated_count']}
- **通过筛选数**: {result['passed_count']}
- **通过率**: {result['pass_rate']:.1f}%
- **生成耗时**: {result['generation_time']:.2f} 秒

---

## 🧪 生成的 SMILES

"""
    
    for idx, smi in enumerate(result['smiles_list'], 1):
        detail += f"{idx}. `{smi}`\n"
    
    detail += "\n---\n\n## ✅ 通过 ADMET 筛选的分子\n\n"
    
    if result['passed_molecules']:
        for idx, mol_data in enumerate(result['passed_molecules'], 1):
            props = mol_data['properties']
            detail += f"""
### 分子 {idx}

**SMILES**: `{mol_data['smiles']}`

| 指标 | 数值 | 状态 |
|------|------|------|
| 分子量 (MW) | {props['molecular_weight']:.1f} Da | {'✅' if props['molecular_weight'] < 500 else '⚠️'} |
| 类药性 (QED) | {props['qed']:.3f} | {'✅' if props['qed'] > 0.6 else '⚠️'} |
| LogP | {props['logp']:.2f} | {'✅' if 1 <= props['logp'] <= 5 else '⚠️'} |
| TPSA | {props['tpsa']:.1f} Ų | {'✅' if props['tpsa'] < 140 else '⚠️'} |
| 可旋转键 | {props['rotatable_bonds']} | {'✅' if props['rotatable_bonds'] < 10 else '⚠️'} |

---
"""
        
        # 平均性质
        detail += f"""
## 📈 平均性质

- **平均分子量**: {result['avg_mw']:.1f} Da
- **平均类药性**: {result['avg_qed']:.3f}
- **平均 LogP**: {result['avg_logp']:.2f}
"""
    else:
        detail += "\n⚠️ 没有分子通过 ADMET 筛选\n"
    
    return detail


def create_demo():
    """创建模型对比图形界面"""
    
    with gr.Blocks(
        title="LingNexus - 模型对比工具",
        theme=gr.themes.Soft()
    ) as demo:
        
        gr.Markdown("""
# 🔬 LingNexus - AI 模型对比工具

> 同时测试多个 LLM 模型的分子生成能力，直观对比性能差异
> 
> **支持模型**: Qwen-Max / Gemini / DeepSeek
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 📝 对比设置")
                
                target_input = gr.Textbox(
                    label="靶点名称",
                    placeholder="例如：BTK, EGFR, JAK2",
                    value="BTK",
                    info="请输入公开靶点名称"
                )
                
                with gr.Row():
                    model1_choice = gr.Dropdown(
                        label="模型 1",
                        choices=["qwen-max", "deepseek", "gemini"],
                        value="qwen-max",
                        info="第一个测试模型"
                    )
                    
                    model2_choice = gr.Dropdown(
                        label="模型 2",
                        choices=["qwen-max", "deepseek", "gemini"],
                        value="gemini",
                        info="第二个测试模型 (🔥 gemini = Gemini 3 Pro)"
                    )
                
                requirements_input = gr.Textbox(
                    label="特殊要求（可选）",
                    placeholder="例如：分子量<400，高选择性",
                    lines=2
                )
                
                compare_btn = gr.Button(
                    "🔬 开始对比",
                    variant="primary",
                    size="lg"
                )
                
                gr.Markdown("""
---
### 💡 使用提示

1. **选择两个不同的模型**进行对比
2. **三大模型**：
   - 🇨🇳 `qwen-max` = 阿里通义千问（中文优化）
   - 🧠 `deepseek` = DeepSeek 3.2（推理能力强）
   - 🔥 `gemini` = Gemini 3 Pro Preview（最新最强）
3. **推荐对比组合**：
   - Qwen-Max vs Gemini（国产 vs 国际）
   - Qwen-Max vs DeepSeek（国产双雄）
   - DeepSeek vs Gemini（推理对决）·
4. **对比维度**：通过率、QED、速度、输出格式
                """)
        
            with gr.Column(scale=2):
                gr.Markdown("### 📊 对比结果")
                
                with gr.Tab("📊 对比报告"):
                    report_output = gr.Markdown()
                
                with gr.Tab("🤖 模型 1 详情"):
                    model1_detail = gr.Markdown()
                
                with gr.Tab("🤖 模型 2 详情"):
                    model2_detail = gr.Markdown()
        
        # 绑定事件
        compare_btn.click(
            fn=compare_models_ui,
            inputs=[target_input, model1_choice, model2_choice, requirements_input],
            outputs=[report_output, model1_detail, model2_detail]
        )
        
        # 示例
        gr.Markdown("""
---
### 🧪 推荐测试案例

| 靶点 | 说明 | 推荐对比 |
|------|------|---------|
| BTK | 布鲁顿酪氨酸激酶（Ibrutinib 靶点） | Qwen-Max vs Gemini |
| EGFR | 表皮生长因子受体（Gefitinib 靶点） | Qwen-Max vs DeepSeek |
| JAK2 | Janus 激酶 2（Ruxolitinib 靶点） | DeepSeek vs Gemini |

**⚠️ 注意**: 首次运行需确保已配置所有模型的 API Key（见 `config/model_config.json`）
        """)
    
    return demo


if __name__ == "__main__":
    demo = create_demo()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7861,  # 使用不同端口避免冲突
        share=False,
        show_error=True
    )
    print("\n✨ LingNexus 模型对比工具已启动！")
    print("🌐 访问地址：http://127.0.0.1:7861")

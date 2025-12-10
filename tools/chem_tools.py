"""化学分子处理工具集

提供 SMILES 验证、性质计算、ADMET 评估等功能
"""

from typing import List, Dict, Optional


def validate_smiles(smiles: str) -> bool:
    """验证 SMILES 字符串是否有效
    
    Args:
        smiles: SMILES 字符串
        
    Returns:
        bool: 是否有效
    """
    try:
        from rdkit import Chem
        mol = Chem.MolFromSmiles(smiles)
        return mol is not None
    except ImportError:
        # 如果未安装 RDKit，返回基础验证
        return len(smiles) > 0 and not smiles.isspace()


def calculate_molecular_properties(smiles: str) -> Optional[Dict[str, float]]:
    """计算分子性质
    
    Args:
        smiles: SMILES 字符串
        
    Returns:
        Dict: 包含分子量、LogP、QED、TPSA 等性质，若无效则返回 None
    """
    try:
        from rdkit import Chem
        from rdkit.Chem import Descriptors, QED
        
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        
        properties = {
            "molecular_weight": Descriptors.MolWt(mol),
            "logp": Descriptors.MolLogP(mol),
            "qed": QED.qed(mol),
            "tpsa": Descriptors.TPSA(mol),
            "rotatable_bonds": Descriptors.NumRotatableBonds(mol),
            "h_bond_donors": Descriptors.NumHDonors(mol),
            "h_bond_acceptors": Descriptors.NumHAcceptors(mol),
            "aromatic_rings": Descriptors.NumAromaticRings(mol)
        }
        
        return properties
        
    except ImportError:
        print("警告：未安装 RDKit，无法计算分子性质。请运行：pip install rdkit")
        return None


def admet_filter(smiles_list: List[str], verbose: bool = True) -> List[Dict[str, any]]:
    """轻量级 ADMET 过滤（基于 Lipinski 规则和 QED）
    
    Args:
        smiles_list: SMILES 字符串列表
        verbose: 是否打印详细信息
        
    Returns:
        List[Dict]: 通过筛选的分子及其性质
    """
    passed = []
    
    for idx, smiles in enumerate(smiles_list, 1):
        props = calculate_molecular_properties(smiles)
        
        if props is None:
            if verbose:
                print(f"❌ 分子 {idx}: 无效的 SMILES - {smiles}")
            continue
        
        # ADMET 筛选规则
        mw_ok = props["molecular_weight"] < 500
        qed_ok = props["qed"] > 0.6
        logp_ok = 1 <= props["logp"] <= 5
        tpsa_ok = props["tpsa"] < 140
        rotatable_ok = props["rotatable_bonds"] < 10
        
        # 整体评分
        score = sum([mw_ok, qed_ok, logp_ok, tpsa_ok, rotatable_ok])
        pass_threshold = 3  # 至少满足 3 个条件
        
        if score >= pass_threshold:
            result = {
                "smiles": smiles,
                "properties": props,
                "score": score,
                "passed": True
            }
            passed.append(result)
            
            if verbose:
                print(f"✅ 分子 {idx}: {smiles}")
                print(f"   MW={props['molecular_weight']:.1f}, QED={props['qed']:.2f}, "
                      f"LogP={props['logp']:.2f}, TPSA={props['tpsa']:.1f}")
        else:
            if verbose:
                print(f"⚠️  分子 {idx}: 未通过筛选 - {smiles}")
                print(f"   MW={props['molecular_weight']:.1f}, QED={props['qed']:.2f}")
    
    return passed


def check_pains_alerts(smiles: str) -> bool:
    """检查是否包含 PAINS（Pan-Assay Interference Compounds）结构
    
    Args:
        smiles: SMILES 字符串
        
    Returns:
        bool: True 表示安全（无 PAINS），False 表示有问题
    """
    try:
        from rdkit import Chem
        from rdkit.Chem.FilterCatalog import FilterCatalog, FilterCatalogParams
        
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return False
        
        params = FilterCatalogParams()
        params.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS)
        catalog = FilterCatalog(params)
        
        entry = catalog.GetFirstMatch(mol)
        return entry is None  # None 表示无匹配（安全）
        
    except ImportError:
        # 未安装 RDKit 时跳过检查
        return True


if __name__ == "__main__":
    # 测试示例
    test_smiles = [
        "COc1ccc(NC(=O)c2ccccc2)cc1N1CCN(C)CC1",  # 好的类药分子
        "CC(C)Oc1ccc(NC(=O)Nc2ccc(Cl)cc2)cc1",   # 好的类药分子
        "CCCCCCCCCCCCCCCCCC",  # 分子量太大，不类药
    ]
    
    print("=== ADMET 筛选测试 ===")
    results = admet_filter(test_smiles)
    print(f"\n通过筛选: {len(results)}/{len(test_smiles)}")

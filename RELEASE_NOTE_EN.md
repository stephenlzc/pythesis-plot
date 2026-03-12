# 🎉 PyThesisPlot v1.0.0 Release Notes

## Overview

**PyThesisPlot** is a professional scientific plotting tool designed for academic publications. It provides a complete workflow from data upload to publication-ready figures, following top journal standards (Nature/Science/Lancet).

---

## ✨ Key Features

### 🎯 Intelligent Workflow
- **5-Stage Process**: Data Upload → Analysis → Recommendations → Confirmation → Generation
- **Smart Analysis**: Automatic data type detection, statistical summaries, and relationship analysis
- **AI Recommendations**: Intelligent chart type suggestions based on data characteristics
- **User Confirmation**: Required confirmation before generation to ensure accuracy

### 🎨 Publication-Ready Output
- **300 DPI High Resolution**: Suitable for journal submission
- **Academic Style Compliance**: Nature/Science/Lancet journal standards
- **Statistical Annotations**: Automatic significance markers (* / ** / ***)
- **Colorblind-Friendly Palettes**: Okabe-Ito, Paul Tol, and Nature/Science color schemes

### 🔬 Multi-Domain Support
| Domain | Application Examples |
|:------:|:---------------------|
| 🧬 **Biology & Medicine** | qPCR, Western Blot, Cell assays, Histology |
| 🧠 **Psychology & Social Sciences** | Survey data, RCT studies, Questionnaires |
| 📈 **Economics & Business** | Time series, Market analysis, Financial data |
| 🧪 **Chemistry & Materials** | Spectroscopy, Chromatography, Measurements |

---

## 📦 What's Included

### Core Scripts
| Script | Description |
|:-------|:------------|
| `workflow.py` | Main workflow orchestrator - Complete pipeline from data to figures |
| `data_analyzer.py` | Data analysis engine - Automatic insights and recommendations |
| `plot_generator.py` | Chart generation engine - Publication-ready visualization |

### Style Themes
- **academic.mplstyle** - General academic style
- **nature.mplstyle** - Nature journal style
- **presentation.mplstyle** - Presentation-optimized style

### Documentation
- **README.md** - English documentation
- **README.zh-CN.md** - Chinese documentation
- **workflow_guide.md** - Detailed workflow instructions
- **chart_types.md** - Chart type selection guide
- **style_guide.md** - Visual style standards
- **examples.md** - Code examples and tutorials

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/stephenlzc/pythesis-plot.git

# Navigate to project directory
cd pythesis-plot

# Install dependencies
pip install pandas matplotlib seaborn openpyxl numpy scipy
```

### Basic Usage

```bash
# Complete workflow (Recommended)
python scripts/workflow.py --input your_data.csv

# Analysis only
python scripts/data_analyzer.py --input your_data.csv

# Generate from config
python scripts/plot_generator.py --config plot_config.json
```

---

## 💡 Example Use Cases

### Example 1: PCOS Study (Biomedical)
**Data**: Mouse PCOS model with BRAC1 gene expression (108 samples, 3 groups)

**Generated Figures**:
- Body weight comparison with significance markers
- Ovary weight analysis
- BRAC1 relative expression (log scale, 55× downregulation)
- qPCR Ct value distributions
- Comprehensive 2×2 dashboard

**Key Finding**: BRAC1 expression significantly downregulated in PCOS model (p<0.001)

### Example 2: Mental Health RCT (Psychology)
**Data**: Adolescent mental health intervention (1200 participants, 4 groups)

**Generated Figures**:
- CONSORT-style study overview
- SDQ pre/post comparison
- Responder analysis (0.3% → 61.3%)
- Dose-response relationship
- 6-panel comprehensive dashboard

**Key Finding**: Combined CBT+Mindfulness intervention achieved 61.3% response rate

---

## 📊 Supported Chart Types

| Chart Type | Best For | Output Format |
|:----------:|:---------|:-------------:|
| 📈 Line Plot | Time series, Trends | PNG (300 DPI) |
| 📊 Bar Chart | Group comparisons | PNG (300 DPI) |
| 🎯 Box Plot | Distribution, Outliers | PNG (300 DPI) |
| ⚡ Scatter + Regression | Correlations | PNG (300 DPI) |
| 🔥 Heatmap | Correlation matrices | PNG (300 DPI) |
| 📋 Dashboard | Multi-panel figures | PNG (300 DPI) |

---

## 🏗️ Project Structure

```
pythesis-plot/
├── 📄 README.md                    # English documentation
├── 📄 README.zh-CN.md              # Chinese documentation
├── 📄 SKILL.md                     # Skill definition
├── 📁 scripts/
│   ├── 🔄 workflow.py              # Main workflow
│   ├── 🔍 data_analyzer.py         # Data analysis
│   └── 🎨 plot_generator.py        # Chart generation
├── 📁 references/                  # Documentation
├── 📁 assets/themes/               # Style themes
└── 📁 output/                      # Generated outputs
```

---

## 📋 Output Organization

All outputs are organized in timestamped directories:

```
output/
└── 20250312-143052-your-data/
    ├── 20250312-143052-your-data.csv    # Original data
    ├── analysis_report.md               # Analysis report
    ├── plot_config.json                 # Chart configuration
    ├── 20250312-143052_plot.py          # Reproducible Python code
    └── *.png                            # 300 DPI figures
```

---

## 🔧 Dependencies

```toml
[dependencies]
python = ">=3.8"
pandas = ">=1.3.0"
matplotlib = ">=3.5.0"
seaborn = ">=0.11.0"
openpyxl = ">=3.0.0"
numpy = ">=1.20.0"
scipy = ">=1.7.0"
```

---

## 🌐 Languages

- **English**: [README.md](README.md)
- **中文**: [README.zh-CN.md](README.zh-CN.md)

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- 🎨 Color palettes inspired by [Nature](https://www.nature.com/) and [Science](https://www.science.org/) style guides
- 📊 Statistical visualization best practices from [Seaborn](https://seaborn.pydata.org/)
- 🎓 Academic plotting standards from [Matplotlib](https://matplotlib.org/)

---

## 📮 Feedback & Contributions

- 💡 **Feature Requests**: Open an [Issue](https://github.com/stephenlzc/pythesis-plot/issues)
- 🐛 **Bug Reports**: Open an [Issue](https://github.com/stephenlzc/pythesis-plot/issues)
- 🤝 **Contributions**: Submit a [Pull Request](https://github.com/stephenlzc/pythesis-plot/pulls)

---

**Made with ❤️ for Researchers Worldwide**

[⬆ Back to Top](#-pythesisplot-v100-release-notes)

---

# 🎉 PyThesisPlot v1.0.0 发行说明

## 概述

**PyThesisPlot** 是一款专为学术发表设计的专业科研作图工具。它提供从数据上传到顶刊级图表的完整工作流，符合 Nature/Science/Lancet 等顶级期刊标准。

---

## ✨ 核心功能

### 🎯 智能工作流
- **5阶段流程**: 数据上传 → 分析 → 推荐 → 确认 → 生成
- **智能分析**: 自动数据类型检测、统计摘要、关系分析
- **AI 推荐**: 基于数据特征智能推荐图表类型
- **用户确认**: 生成前必须经用户确认，确保准确性

### 🎨 顶刊品质输出
- **300 DPI 高分辨率**: 适合期刊投稿
- **学术风格合规**: Nature/Science/Lancet 期刊标准
- **统计显著性标注**: 自动添加 * / ** / *** 标记
- **色盲友好配色**: Okabe-Ito、Paul Tol、Nature/Science 配色方案

### 🔬 多领域支持
| 领域 | 应用示例 |
|:------:|:---------------------|
| 🧬 **生物医学** | qPCR、Western Blot、细胞实验、组织学 |
| 🧠 **心理与社会科学** | 问卷调查、RCT研究、量表数据 |
| 📈 **经济与商科** | 时间序列、市场分析、金融数据 |
| 🧪 **化学与材料** | 光谱分析、色谱、测量数据 |

---

## 📦 包含内容

### 核心脚本
| 脚本 | 说明 |
|:-------|:------------|
| `workflow.py` | 主工作流编排器 - 从数据到图表的完整流水线 |
| `data_analyzer.py` | 数据分析引擎 - 自动洞察与推荐 |
| `plot_generator.py` | 图表生成引擎 - 顶刊级可视化 |

### 样式主题
- **academic.mplstyle** - 通用学术风格
- **nature.mplstyle** - Nature 期刊风格
- **presentation.mplstyle** - 演示优化风格

### 文档
- **README.md** - 英文文档
- **README.zh-CN.md** - 中文文档
- **workflow_guide.md** - 详细工作流说明
- **chart_types.md** - 图表类型选择指南
- **style_guide.md** - 视觉样式标准
- **examples.md** - 代码示例与教程

---

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/stephenlzc/pythesis-plot.git

# 进入项目目录
cd pythesis-plot

# 安装依赖
pip install pandas matplotlib seaborn openpyxl numpy scipy
```

### 基本用法

```bash
# 完整工作流（推荐）
python scripts/workflow.py --input your_data.csv

# 仅数据分析
python scripts/data_analyzer.py --input your_data.csv

# 根据配置生成
python scripts/plot_generator.py --config plot_config.json
```

---

## 💡 应用示例

### 示例 1：PCOS 研究（生物医学）
**数据**: 小鼠PCOS模型，BRAC1基因表达（108样本，3组）

**生成图表**:
- 体重对比（含显著性标记）
- 卵巢重量分析
- BRAC1相对表达量（对数刻度，下调55倍）
- qPCR Ct值分布
- 2×2 综合仪表盘

**核心发现**: PCOS模型组BRAC1表达显著下调 (p<0.001)

### 示例 2：心理健康 RCT（心理学）
**数据**: 青少年心理健康干预（1200参与者，4组）

**生成图表**:
- CONSORT风格研究概况
- SDQ干预前后对比
- 响应者分析（0.3% → 61.3%）
- 剂量-效应关系
- 6图综合仪表盘

**核心发现**: CBT+正念联合干预响应率达61.3%

---

## 📊 支持的图表类型

| 图表类型 | 适用场景 | 输出格式 |
|:----------:|:---------|:-------------:|
| 📈 折线图 | 时间序列、趋势 | PNG (300 DPI) |
| 📊 柱状图 | 分组对比 | PNG (300 DPI) |
| 🎯 箱线图 | 分布、异常值 | PNG (300 DPI) |
| ⚡ 散点+回归 | 相关性 | PNG (300 DPI) |
| 🔥 热力图 | 相关性矩阵 | PNG (300 DPI) |
| 📋 仪表盘 | 多子图组合 | PNG (300 DPI) |

---

## 🏗️ 项目结构

```
pythesis-plot/
├── 📄 README.md                    # 英文文档
├── 📄 README.zh-CN.md              # 中文文档
├── 📄 SKILL.md                     # Skill定义
├── 📁 scripts/
│   ├── 🔄 workflow.py              # 主工作流
│   ├── 🔍 data_analyzer.py         # 数据分析
│   └── 🎨 plot_generator.py        # 图表生成
├── 📁 references/                  # 文档
├── 📁 assets/themes/               # 样式主题
└── 📁 output/                      # 输出目录
```

---

## 📋 输出组织

所有输出按时间戳目录组织：

```
output/
└── 20250312-143052-your-data/
    ├── 20250312-143052-your-data.csv    # 原始数据
    ├── analysis_report.md               # 分析报告
    ├── plot_config.json                 # 图表配置
    ├── 20250312-143052_plot.py          # 可复现Python代码
    └── *.png                            # 300 DPI 图表
```

---

## 🔧 依赖要求

```toml
[dependencies]
python = ">=3.8"
pandas = ">=1.3.0"
matplotlib = ">=3.5.0"
seaborn = ">=0.11.0"
openpyxl = ">=3.0.0"
numpy = ">=1.20.0"
scipy = ">=1.7.0"
```

---

## 🌐 多语言支持

- **English**: [README.md](README.md)
- **中文**: [README.zh-CN.md](README.zh-CN.md)

---

## 📄 开源协议

本项目采用 MIT 协议。

---

## 🙏 致谢

- 🎨 配色方案参考 [Nature](https://www.nature.com/) 和 [Science](https://www.science.org/) 风格指南
- 📊 统计可视化最佳实践来自 [Seaborn](https://seaborn.pydata.org/)
- 🎓 学术作图标准参考 [Matplotlib](https://matplotlib.org/)

---

## 📮 反馈与贡献

- 💡 **功能建议**: 提交 [Issue](https://github.com/stephenlzc/pythesis-plot/issues)
- 🐛 **Bug 报告**: 提交 [Issue](https://github.com/stephenlzc/pythesis-plot/issues)
- 🤝 **代码贡献**: 提交 [Pull Request](https://github.com/stephenlzc/pythesis-plot/pulls)

---

**用 ❤️ 为全球科研工作者打造**

[⬆ 返回顶部](#-pythesisplot-v100-发行说明)

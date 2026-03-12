#!/usr/bin/env python3
"""
PyThesisPlot 生成脚本
数据: Mouse_PCOS_BRAC1_RawData_108.xlsx
生成时间: 2026-03-12 19:30:07
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# 设置科研样式
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9

# 中文字体设置
try:
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Heiti TC', 'Arial Unicode MS', 'Arial', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
except:
    pass

# 配色方案
PALETTE = ['#4472C4', '#ED7D31', '#A5A5A5', '#FFC000', '#5B9BD5']

# 读取数据
data_file = "20260312-193007-Mouse_PCOS_BRAC1_RawData_108.xlsx"
df = pd.read_excel(data_file, sheet_name="RawData")

# 设置顺序
df['Group'] = pd.Categorical(df['Group'], categories=['Control', 'PCOS_Model', 'PCOS_Treatment'], ordered=True)

timestamp = "20260312-193007"


def add_significance(ax, x1, x2, y, pvalue, h=0.02):
    """添加显著性标记"""
    if pvalue < 0.001:
        sig = "***"
    elif pvalue < 0.01:
        sig = "**"
    elif pvalue < 0.05:
        sig = "*"
    else:
        sig = "ns"
    
    y_max = ax.get_ylim()[1]
    h_factor = h * (ax.get_ylim()[1] - ax.get_ylim()[0])
    
    ax.plot([x1, x1, x2, x2], [y, y+h_factor, y+h_factor, y], 'k-', linewidth=1)
    ax.text((x1+x2)/2, y+h_factor, sig, ha='center', va='bottom', fontsize=10, fontweight='bold')


# ========== Figure 1: 体重对比 ==========
fig1, ax1 = plt.subplots(figsize=(8, 6))

groups = ['Control', 'PCOS_Model', 'PCOS_Treatment']
body_data = [df[df['Group']==g]['Body_Weight_g'].values for g in groups]
body_means = [np.mean(d) for d in body_data]
body_stds = [np.std(d, ddof=1) for d in body_data]

bars = ax1.bar(groups, body_means, yerr=body_stds, capsize=5, 
               color=PALETTE[:3], edgecolor='black', linewidth=1.2,
               error_kw={'elinewidth': 1.5, 'capthick': 1.5})

# 添加散点
for i, (g, data) in enumerate(zip(groups, body_data)):
    jitter = np.random.normal(i, 0.08, size=len(data))
    ax1.scatter(jitter, data, color='black', s=20, alpha=0.5, zorder=3)

ax1.set_ylabel('Body Weight (g)', fontsize=12, fontweight='bold')
ax1.set_title('Body Weight Comparison\n(Control vs PCOS Model vs Treatment)', fontsize=13, fontweight='bold')
ax1.set_ylim(20, 32)

# 统计检验
_, p1 = stats.ttest_ind(body_data[0], body_data[1])
_, p2 = stats.ttest_ind(body_data[1], body_data[2])
_, p3 = stats.ttest_ind(body_data[0], body_data[2])

# 添加显著性标记
add_significance(ax1, 0, 1, 31, p1)
add_significance(ax1, 1, 2, 30, p2)
add_significance(ax1, 0, 2, 29, p3)

# 添加数值标签
for i, (m, s) in enumerate(zip(body_means, body_stds)):
    ax1.text(i, m+s+0.3, f'{m:.2f}±{s:.2f}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
fig1.savefig(f'{timestamp}_fig1_body_weight.png', bbox_inches='tight')
plt.close()
print("✅ Figure 1: 体重对比 - 已生成")


# ========== Figure 2: 卵巢重量对比 ==========
fig2, ax2 = plt.subplots(figsize=(8, 6))

ovary_data = [df[df['Group']==g]['Ovary_Weight_mg'].values for g in groups]
ovary_means = [np.mean(d) for d in ovary_data]
ovary_stds = [np.std(d, ddof=1) for d in ovary_data]

bars = ax2.bar(groups, ovary_means, yerr=ovary_stds, capsize=5,
               color=PALETTE[:3], edgecolor='black', linewidth=1.2,
               error_kw={'elinewidth': 1.5, 'capthick': 1.5})

for i, (g, data) in enumerate(zip(groups, ovary_data)):
    jitter = np.random.normal(i, 0.08, size=len(data))
    ax2.scatter(jitter, data, color='black', s=20, alpha=0.5, zorder=3)

ax2.set_ylabel('Ovary Weight (mg)', fontsize=12, fontweight='bold')
ax2.set_title('Ovary Weight Comparison\n(Control vs PCOS Model vs Treatment)', fontsize=13, fontweight='bold')
ax2.set_ylim(10, 22)

# 统计检验
_, p1 = stats.ttest_ind(ovary_data[0], ovary_data[1])
_, p2 = stats.ttest_ind(ovary_data[1], ovary_data[2])
_, p3 = stats.ttest_ind(ovary_data[0], ovary_data[2])

add_significance(ax2, 0, 1, 21, p1)
add_significance(ax2, 1, 2, 20, p2)
add_significance(ax2, 0, 2, 19, p3)

for i, (m, s) in enumerate(zip(ovary_means, ovary_stds)):
    ax2.text(i, m+s+0.2, f'{m:.2f}±{s:.2f}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
fig2.savefig(f'{timestamp}_fig2_ovary_weight.png', bbox_inches='tight')
plt.close()
print("✅ Figure 2: 卵巢重量对比 - 已生成")


# ========== Figure 3: BRAC1相对表达量 (对数刻度) ==========
fig3, ax3 = plt.subplots(figsize=(8, 6))

expr_data = [df[df['Group']==g]['Relative_Expression'].values for g in groups]
expr_means = [np.mean(d) for d in expr_data]
expr_stds = [np.std(d, ddof=1) for d in expr_data]

bars = ax3.bar(groups, expr_means, yerr=expr_stds, capsize=5,
               color=PALETTE[:3], edgecolor='black', linewidth=1.2,
               error_kw={'elinewidth': 1.5, 'capthick': 1.5})

for i, (g, data) in enumerate(zip(groups, expr_data)):
    jitter = np.random.normal(i, 0.08, size=len(data))
    ax3.scatter(jitter, data, color='black', s=20, alpha=0.5, zorder=3)

ax3.set_ylabel('Relative Expression', fontsize=12, fontweight='bold')
ax3.set_title('BRAC1 Relative Expression\n(Control vs PCOS Model vs Treatment)', fontsize=13, fontweight='bold')
ax3.set_yscale('log')
ax3.set_ylim(0.001, 5)

# 统计检验
_, p1 = stats.ttest_ind(expr_data[0], expr_data[1])
_, p2 = stats.ttest_ind(expr_data[1], expr_data[2])
_, p3 = stats.ttest_ind(expr_data[0], expr_data[2])

add_significance(ax3, 0, 1, 3, p1)
add_significance(ax3, 1, 2, 2, p2)
add_significance(ax3, 0, 2, 1.5, p3)

# 添加折叠变化标注
fold_change_model = expr_means[0] / expr_means[1]
fold_change_treatment = expr_means[2] / expr_means[1]
ax3.text(0.02, 0.98, f'Fold Change (Model/Baseline): {fold_change_model:.1f}×↓\nFold Change (Treatment/Model): {fold_change_treatment:.1f}×↑',
         transform=ax3.transAxes, fontsize=9, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
fig3.savefig(f'{timestamp}_fig3_brac1_expression.png', bbox_inches='tight')
plt.close()
print("✅ Figure 3: BRAC1相对表达量 - 已生成")


# ========== Figure 4: qPCR Ct值分布 ==========
fig4, ax4 = plt.subplots(figsize=(10, 6))

# 准备数据
brac1_data = [df[df['Group']==g]['BRAC1_Ct'].values for g in groups]
gapdh_data = [df[df['Group']==g]['GAPDH_Ct'].values for g in groups]

positions = [1, 2, 3, 5, 6, 7]
all_data = [brac1_data[0], brac1_data[1], brac1_data[2],
            gapdh_data[0], gapdh_data[1], gapdh_data[2]]

bp = ax4.boxplot(all_data, positions=positions, widths=0.6, patch_artist=True,
                 showmeans=True, meanline=True,
                 boxprops=dict(facecolor='lightblue', alpha=0.7),
                 medianprops=dict(color='red', linewidth=2),
                 meanprops=dict(color='green', linestyle='--'))

# 设置颜色
colors = PALETTE[:3] + ['lightgray']*3
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)

# 添加散点
for i, (pos, data) in enumerate(zip(positions, all_data)):
    jitter = np.random.normal(pos, 0.05, size=len(data))
    ax4.scatter(jitter, data, color='black', s=15, alpha=0.4, zorder=3)

ax4.set_xticks([2, 6])
ax4.set_xticklabels(['BRAC1_Ct', 'GAPDH_Ct'], fontsize=11, fontweight='bold')
ax4.set_ylabel('Ct Value', fontsize=12, fontweight='bold')
ax4.set_title('qPCR Ct Values Distribution\n(Control vs PCOS Model vs Treatment)', fontsize=13, fontweight='bold')
ax4.set_ylim(14, 26)

# 添加分组标签
for i, g in enumerate(groups):
    ax4.text(i+1, 14.5, g, ha='center', fontsize=9, rotation=15)
    ax4.text(i+5, 14.5, g, ha='center', fontsize=9, rotation=15)

plt.tight_layout()
fig4.savefig(f'{timestamp}_fig4_ct_values.png', bbox_inches='tight')
plt.close()
print("✅ Figure 4: qPCR Ct值分布 - 已生成")


# ========== Figure 5: 综合仪表盘 (2x2) ==========
fig5 = plt.figure(figsize=(14, 12))

# (a) 体重对比
ax5a = fig5.add_subplot(2, 2, 1)
bars_a = ax5a.bar(groups, body_means, yerr=body_stds, capsize=4,
                  color=PALETTE[:3], edgecolor='black', linewidth=1,
                  error_kw={'elinewidth': 1.2, 'capthick': 1.2})
for i, data in enumerate(body_data):
    jitter = np.random.normal(i, 0.06, size=len(data))
    ax5a.scatter(jitter, data, color='black', s=15, alpha=0.4, zorder=3)
ax5a.set_ylabel('Body Weight (g)', fontsize=10, fontweight='bold')
ax5a.set_title('(a) Body Weight', fontsize=11, fontweight='bold')
ax5a.set_ylim(20, 32)
add_significance(ax5a, 0, 1, 31, p1, h=0.015)
add_significance(ax5a, 1, 2, 30, p2, h=0.015)

# (b) 卵巢重量对比
ax5b = fig5.add_subplot(2, 2, 2)
bars_b = ax5b.bar(groups, ovary_means, yerr=ovary_stds, capsize=4,
                  color=PALETTE[:3], edgecolor='black', linewidth=1,
                  error_kw={'elinewidth': 1.2, 'capthick': 1.2})
for i, data in enumerate(ovary_data):
    jitter = np.random.normal(i, 0.06, size=len(data))
    ax5b.scatter(jitter, data, color='black', s=15, alpha=0.4, zorder=3)
ax5b.set_ylabel('Ovary Weight (mg)', fontsize=10, fontweight='bold')
ax5b.set_title('(b) Ovary Weight', fontsize=11, fontweight='bold')
ax5b.set_ylim(10, 22)
add_significance(ax5b, 0, 1, 21, p1, h=0.015)
add_significance(ax5b, 1, 2, 20, p2, h=0.015)

# (c) BRAC1表达量 (对数)
ax5c = fig5.add_subplot(2, 2, 3)
bars_c = ax5c.bar(groups, expr_means, yerr=expr_stds, capsize=4,
                  color=PALETTE[:3], edgecolor='black', linewidth=1,
                  error_kw={'elinewidth': 1.2, 'capthick': 1.2})
for i, data in enumerate(expr_data):
    jitter = np.random.normal(i, 0.06, size=len(data))
    ax5c.scatter(jitter, data, color='black', s=15, alpha=0.4, zorder=3)
ax5c.set_ylabel('Relative Expression (log)', fontsize=10, fontweight='bold')
ax5c.set_title('(c) BRAC1 Expression', fontsize=11, fontweight='bold')
ax5c.set_yscale('log')
ax5c.set_ylim(0.001, 5)
add_significance(ax5c, 0, 1, 3, p1, h=0.015)
add_significance(ax5c, 1, 2, 2, p2, h=0.015)

# (d) BRAC1 Ct值箱线图
ax5d = fig5.add_subplot(2, 2, 4)
bp_d = ax5d.boxplot(brac1_data, labels=groups, patch_artist=True,
                    showmeans=True, meanline=True,
                    boxprops=dict(facecolor='lightblue', alpha=0.7),
                    medianprops=dict(color='red', linewidth=1.5))
for patch, color in zip(bp_d['boxes'], PALETTE[:3]):
    patch.set_facecolor(color)
for i, data in enumerate(brac1_data):
    jitter = np.random.normal(i+1, 0.06, size=len(data))
    ax5d.scatter(jitter, data, color='black', s=15, alpha=0.4, zorder=3)
ax5d.set_ylabel('BRAC1 Ct Value', fontsize=10, fontweight='bold')
ax5d.set_title('(d) BRAC1 qPCR Ct', fontsize=11, fontweight='bold')
ax5d.set_ylim(16, 26)

plt.tight_layout()
fig5.savefig(f'{timestamp}_fig5_dashboard.png', bbox_inches='tight')
plt.close()
print("✅ Figure 5: 综合仪表盘 - 已生成")


print("\n" + "="*60)
print("✅ 全部图表生成完成！（仅PNG格式）")
print("="*60)
print("\n生成文件列表:")
print(f"  • {timestamp}_fig1_body_weight.png")
print(f"  • {timestamp}_fig2_ovary_weight.png")
print(f"  • {timestamp}_fig3_brac1_expression.png")
print(f"  • {timestamp}_fig4_ct_values.png")
print(f"  • {timestamp}_fig5_dashboard.png")

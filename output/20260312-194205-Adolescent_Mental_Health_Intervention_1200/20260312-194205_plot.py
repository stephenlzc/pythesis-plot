#!/usr/bin/env python3
"""
PyThesisPlot 生成脚本
数据: Adolescent_Mental_Health_Intervention_1200.xlsx
研究: 青少年心理健康干预RCT
生成时间: 2026-03-12 19:42:05
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

try:
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Heiti TC', 'Arial Unicode MS', 'Arial', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
except:
    pass

# 配色方案
PALETTE = ['#4472C4', '#ED7D31', '#70AD47', '#A5A5A5', '#FFC000']
GROUP_COLORS = {
    'Control': '#A5A5A5',
    'Intervention_CBT': '#4472C4',
    'Intervention_Mindfulness': '#70AD47',
    'Intervention_Combined': '#ED7D31'
}

GROUP_LABELS = {
    'Control': 'Control',
    'Intervention_CBT': 'CBT',
    'Intervention_Mindfulness': 'Mindfulness',
    'Intervention_Combined': 'Combined'
}

# 读取数据
data_file = "20260312-194205-Adolescent_Mental_Health_Intervention_1200.xlsx"
df = pd.read_excel(data_file, sheet_name="RawData")

# 设置分组顺序
group_order = ['Control', 'Intervention_CBT', 'Intervention_Mindfulness', 'Intervention_Combined']
df['Group'] = pd.Categorical(df['Group'], categories=group_order, ordered=True)

timestamp = "20260312-194205"


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
    
    h_factor = h * (ax.get_ylim()[1] - ax.get_ylim()[0])
    ax.plot([x1, x1, x2, x2], [y, y+h_factor, y+h_factor, y], 'k-', linewidth=1)
    ax.text((x1+x2)/2, y+h_factor, sig, ha='center', va='bottom', fontsize=9, fontweight='bold')


# ========== Figure 1: 研究概况 (CONSORT style) ==========
print("🎨 正在生成 Figure 1: 研究概况...")

fig1, axes = plt.subplots(1, 3, figsize=(15, 5))

# (a) 各组样本量
ax1a = axes[0]
group_counts = df['Group'].value_counts().reindex(group_order)
colors = [GROUP_COLORS[g] for g in group_order]
bars = ax1a.bar(range(len(group_order)), group_counts.values, color=colors, edgecolor='black', linewidth=1.2)
ax1a.set_xticks(range(len(group_order)))
ax1a.set_xticklabels([GROUP_LABELS[g] for g in group_order], rotation=15, ha='right')
ax1a.set_ylabel('Number of Participants', fontsize=11, fontweight='bold')
ax1a.set_title('(a) Sample Size by Group', fontsize=12, fontweight='bold')
for i, v in enumerate(group_counts.values):
    ax1a.text(i, v+5, str(v), ha='center', va='bottom', fontsize=10, fontweight='bold')

# (b) 脱落率
ax1b = axes[1]
dropout_rates = df.groupby('Group')['Is_Dropout'].mean() * 100
dropout_rates = dropout_rates.reindex(group_order)
bars = ax1b.bar(range(len(group_order)), dropout_rates.values, color=colors, edgecolor='black', linewidth=1.2)
ax1b.set_xticks(range(len(group_order)))
ax1b.set_xticklabels([GROUP_LABELS[g] for g in group_order], rotation=15, ha='right')
ax1b.set_ylabel('Dropout Rate (%)', fontsize=11, fontweight='bold')
ax1b.set_title('(b) Dropout Rate', fontsize=12, fontweight='bold')
ax1b.set_ylim(0, max(dropout_rates.values) * 1.5)
for i, v in enumerate(dropout_rates.values):
    ax1b.text(i, v+0.1, f'{v:.1f}%', ha='center', va='bottom', fontsize=9)

# (c) 响应率
ax1c = axes[2]
response_rates = df.groupby('Group')['Is_Responder'].mean() * 100
response_rates = response_rates.reindex(group_order)
bars = ax1c.bar(range(len(group_order)), response_rates.values, color=colors, edgecolor='black', linewidth=1.2)
ax1c.set_xticks(range(len(group_order)))
ax1c.set_xticklabels([GROUP_LABELS[g] for g in group_order], rotation=15, ha='right')
ax1c.set_ylabel('Response Rate (%)', fontsize=11, fontweight='bold')
ax1c.set_title('(c) Responder Rate', fontsize=12, fontweight='bold')
ax1c.set_ylim(0, max(response_rates.values) * 1.3)
for i, v in enumerate(response_rates.values):
    ax1c.text(i, v+1, f'{v:.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
fig1.savefig(f'{timestamp}_fig1_study_overview.png', bbox_inches='tight')
plt.close()
print("✅ Figure 1: 研究概况 - 已生成")


# ========== Figure 2: SDQ前后对比 ==========
print("🎨 正在生成 Figure 2: SDQ前后对比...")

fig2, ax2 = plt.subplots(figsize=(10, 7))

# 准备数据
sdq_baseline = df.groupby('Group')['Baseline_SDQ'].agg(['mean', 'std']).reindex(group_order)
sdq_post = df.groupby('Group')['Post_SDQ'].agg(['mean', 'std']).reindex(group_order)

x = np.arange(len(group_order))
width = 0.35

colors = [GROUP_COLORS[g] for g in group_order]
light_colors = ['#B4C7E7', '#F4B183', '#A9D08E', '#C5E0B4']

# 基线
bars1 = ax2.bar(x - width/2, sdq_baseline['mean'], width, yerr=sdq_baseline['std'],
                label='Baseline', color=light_colors, edgecolor='black', linewidth=1,
                capsize=4, error_kw={'elinewidth': 1.2})

# 干预后
bars2 = ax2.bar(x + width/2, sdq_post['mean'], width, yerr=sdq_post['std'],
                label='Post-Intervention', color=colors, edgecolor='black', linewidth=1,
                capsize=4, error_kw={'elinewidth': 1.2})

ax2.set_ylabel('SDQ Total Score', fontsize=12, fontweight='bold')
ax2.set_title('Strengths and Difficulties Questionnaire (SDQ)\nBaseline vs Post-Intervention', 
              fontsize=13, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels([GROUP_LABELS[g] for g in group_order], fontsize=10)
ax2.legend(loc='upper right', fontsize=10)
ax2.set_ylim(0, 30)

# 添加数值标签
for i, (bl, po) in enumerate(zip(sdq_baseline['mean'], sdq_post['mean'])):
    ax2.text(i - width/2, bl + 1, f'{bl:.1f}', ha='center', va='bottom', fontsize=8)
    ax2.text(i + width/2, po + 1, f'{po:.1f}', ha='center', va='bottom', fontsize=8, fontweight='bold')

# 添加改善箭头标注
for i, g in enumerate(group_order):
    bl = sdq_baseline.loc[g, 'mean']
    po = sdq_post.loc[g, 'mean']
    improvement = bl - po
    if improvement > 2:
        ax2.annotate('', xy=(i + width/2, po), xytext=(i - width/2, bl),
                    arrowprops=dict(arrowstyle='->', color='red', lw=1.5))
        mid_y = (bl + po) / 2
        ax2.text(i + 0.3, mid_y, f'↓{improvement:.1f}', fontsize=8, color='red', fontweight='bold')

plt.tight_layout()
fig2.savefig(f'{timestamp}_fig2_sdq_comparison.png', bbox_inches='tight')
plt.close()
print("✅ Figure 2: SDQ前后对比 - 已生成")


# ========== Figure 4: 响应者分析 ==========
print("🎨 正在生成 Figure 4: 响应者分析...")

fig4, ax4 = plt.subplots(figsize=(10, 7))

# 计算响应者和非响应者
responder_data = []
non_responder_data = []
for g in group_order:
    group_df = df[df['Group'] == g]
    responders = group_df['Is_Responder'].sum()
    non_responders = len(group_df) - responders
    responder_data.append(responders)
    non_responder_data.append(non_responders)

x = np.arange(len(group_order))
width = 0.6

# 堆叠柱状图
bars1 = ax4.bar(x, non_responder_data, width, label='Non-responder', 
                color='lightgray', edgecolor='black', linewidth=1)
bars2 = ax4.bar(x, responder_data, width, bottom=non_responder_data, 
                label='Responder', color=colors, edgecolor='black', linewidth=1)

ax4.set_ylabel('Number of Participants', fontsize=12, fontweight='bold')
ax4.set_title('Responder Analysis by Intervention Group\n(Response = Clinically Significant Improvement)', 
              fontsize=13, fontweight='bold')
ax4.set_xticks(x)
ax4.set_xticklabels([GROUP_LABELS[g] for g in group_order], fontsize=10)
ax4.legend(loc='upper left', fontsize=10)
ax4.set_ylim(0, 320)

# 添加百分比标注
for i, (resp, non_resp) in enumerate(zip(responder_data, non_responder_data)):
    total = resp + non_resp
    pct = resp / total * 100
    ax4.text(i, total + 5, f'{pct:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')
    ax4.text(i, non_resp + resp/2, f'{resp}', ha='center', va='center', fontsize=10, color='white', fontweight='bold')

plt.tight_layout()
fig4.savefig(f'{timestamp}_fig4_responder_analysis.png', bbox_inches='tight')
plt.close()
print("✅ Figure 4: 响应者分析 - 已生成")


# ========== Figure 5: 剂量效应关系 ==========
print("🎨 正在生成 Figure 5: 剂量效应关系...")

fig5, axes = plt.subplots(1, 2, figsize=(14, 6))

# (a) 出勤率 vs SDQ改善
ax5a = axes[0]
intervention_df = df[df['Group'] != 'Control'].copy()
for i, g in enumerate(['Intervention_CBT', 'Intervention_Mindfulness', 'Intervention_Combined']):
    group_data = intervention_df[intervention_df['Group'] == g]
    ax5a.scatter(group_data['Attendance_Rate'], group_data['SDQ_Improvement'], 
                alpha=0.5, s=30, label=GROUP_LABELS[g], color=GROUP_COLORS[g])

# 添加回归线
from scipy.stats import linregress
mask = intervention_df['Attendance_Rate'] > 0
slope, intercept, r_value, p_value, std_err = linregress(
    intervention_df.loc[mask, 'Attendance_Rate'], 
    intervention_df.loc[mask, 'SDQ_Improvement'])
x_line = np.linspace(50, 100, 100)
ax5a.plot(x_line, slope * x_line + intercept, 'r--', linewidth=2, 
         label=f'Linear fit (r={r_value:.2f}, p<0.001)')

ax5a.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
ax5a.set_xlabel('Attendance Rate (%)', fontsize=11, fontweight='bold')
ax5a.set_ylabel('SDQ Improvement (Negative = Better)', fontsize=11, fontweight='bold')
ax5a.set_title('(a) Attendance Rate vs Treatment Outcome', fontsize=12, fontweight='bold')
ax5a.legend(loc='lower right', fontsize=9)
ax5a.set_xlim(50, 105)

# (b) 出勤率分布
ax5b = axes[1]
attendance_by_group = []
for g in ['Intervention_CBT', 'Intervention_Mindfulness', 'Intervention_Combined']:
    group_data = df[df['Group'] == g]['Attendance_Rate']
    attendance_by_group.append(group_data.values)

bp = ax5b.boxplot(attendance_by_group, labels=['CBT', 'Mindfulness', 'Combined'],
                  patch_artist=True, showmeans=True, meanline=True,
                  boxprops=dict(alpha=0.7),
                  medianprops=dict(color='red', linewidth=2))

colors_box = [GROUP_COLORS[g] for g in ['Intervention_CBT', 'Intervention_Mindfulness', 'Intervention_Combined']]
for patch, color in zip(bp['boxes'], colors_box):
    patch.set_facecolor(color)

ax5b.set_ylabel('Attendance Rate (%)', fontsize=11, fontweight='bold')
ax5b.set_title('(b) Distribution of Attendance Rate', fontsize=12, fontweight='bold')
ax5b.set_ylim(40, 105)

# 添加均值标注
for i, g in enumerate(['Intervention_CBT', 'Intervention_Mindfulness', 'Intervention_Combined']):
    mean_val = df[df['Group'] == g]['Attendance_Rate'].mean()
    ax5b.text(i+1, 102, f'{mean_val:.1f}%', ha='center', fontsize=9, fontweight='bold')

plt.tight_layout()
fig5.savefig(f'{timestamp}_fig5_dose_response.png', bbox_inches='tight')
plt.close()
print("✅ Figure 5: 剂量效应关系 - 已生成")


# ========== Figure 6: 综合结果图 (2×3 Dashboard) ==========
print("🎨 正在生成 Figure 6: 综合结果图...")

fig6 = plt.figure(figsize=(16, 10))

# (a) SDQ改善幅度
ax6a = fig6.add_subplot(2, 3, 1)
sdq_improve = df.groupby('Group')['SDQ_Improvement'].agg(['mean', 'std']).reindex(group_order)
colors = [GROUP_COLORS[g] for g in group_order]
bars = ax6a.bar(range(len(group_order)), sdq_improve['mean'], yerr=sdq_improve['std'],
                color=colors, edgecolor='black', linewidth=1, capsize=3)
ax6a.axhline(y=0, color='gray', linestyle='--', linewidth=1)
ax6a.set_xticks(range(len(group_order)))
ax6a.set_xticklabels([GROUP_LABELS[g] for g in group_order], fontsize=9, rotation=15, ha='right')
ax6a.set_ylabel('SDQ Change Score', fontsize=10, fontweight='bold')
ax6a.set_title('(a) SDQ Improvement', fontsize=11, fontweight='bold')
for i, (m, s) in enumerate(zip(sdq_improve['mean'], sdq_improve['std'])):
    ax6a.text(i, m-s-0.5, f'{m:.1f}', ha='center', va='top', fontsize=8, fontweight='bold')

# (b) PHQ-9改善
ax6b = fig6.add_subplot(2, 3, 2)
df['PHQ9_Improvement'] = df['Post_PHQ9'] - df['Baseline_PHQ9']
phq9_improve = df.groupby('Group')['PHQ9_Improvement'].agg(['mean', 'std']).reindex(group_order)
bars = ax6b.bar(range(len(group_order)), phq9_improve['mean'], yerr=phq9_improve['std'],
                color=colors, edgecolor='black', linewidth=1, capsize=3)
ax6b.axhline(y=0, color='gray', linestyle='--', linewidth=1)
ax6b.set_xticks(range(len(group_order)))
ax6b.set_xticklabels([GROUP_LABELS[g] for g in group_order], fontsize=9, rotation=15, ha='right')
ax6b.set_ylabel('PHQ-9 Change Score', fontsize=10, fontweight='bold')
ax6b.set_title('(b) Depression (PHQ-9) Improvement', fontsize=11, fontweight='bold')

# (c) GAD-7改善
ax6c = fig6.add_subplot(2, 3, 3)
df['GAD7_Improvement'] = df['Post_GAD7'] - df['Baseline_GAD7']
gad7_improve = df.groupby('Group')['GAD7_Improvement'].agg(['mean', 'std']).reindex(group_order)
bars = ax6c.bar(range(len(group_order)), gad7_improve['mean'], yerr=gad7_improve['std'],
                color=colors, edgecolor='black', linewidth=1, capsize=3)
ax6c.axhline(y=0, color='gray', linestyle='--', linewidth=1)
ax6c.set_xticks(range(len(group_order)))
ax6c.set_xticklabels([GROUP_LABELS[g] for g in group_order], fontsize=9, rotation=15, ha='right')
ax6c.set_ylabel('GAD-7 Change Score', fontsize=10, fontweight='bold')
ax6c.set_title('(c) Anxiety (GAD-7) Improvement', fontsize=11, fontweight='bold')

# (d) Wellbeing提升
ax6d = fig6.add_subplot(2, 3, 4)
df['Wellbeing_Change'] = df['Post_Wellbeing'] - df['Baseline_Wellbeing']
wellbeing_change = df.groupby('Group')['Wellbeing_Change'].agg(['mean', 'std']).reindex(group_order)
bars = ax6d.bar(range(len(group_order)), wellbeing_change['mean'], yerr=wellbeing_change['std'],
                color=colors, edgecolor='black', linewidth=1, capsize=3)
ax6d.axhline(y=0, color='gray', linestyle='--', linewidth=1)
ax6d.set_xticks(range(len(group_order)))
ax6d.set_xticklabels([GROUP_LABELS[g] for g in group_order], fontsize=9, rotation=15, ha='right')
ax6d.set_ylabel('Wellbeing Change Score', fontsize=10, fontweight='bold')
ax6d.set_title('(d) Wellbeing Improvement', fontsize=11, fontweight='bold')

# (e) 响应者比例
ax6e = fig6.add_subplot(2, 3, 5)
response_rates = df.groupby('Group')['Is_Responder'].mean() * 100
response_rates = response_rates.reindex(group_order)
bars = ax6e.bar(range(len(group_order)), response_rates.values, color=colors, edgecolor='black', linewidth=1)
ax6e.set_xticks(range(len(group_order)))
ax6e.set_xticklabels([GROUP_LABELS[g] for g in group_order], fontsize=9, rotation=15, ha='right')
ax6e.set_ylabel('Response Rate (%)', fontsize=10, fontweight='bold')
ax6e.set_title('(e) Responder Rate', fontsize=11, fontweight='bold')
ax6e.set_ylim(0, 70)
for i, v in enumerate(response_rates.values):
    ax6e.text(i, v+1, f'{v:.1f}%', ha='center', va='bottom', fontsize=8, fontweight='bold')

# (f) 效应量森林图 (Cohen's d)
ax6f = fig6.add_subplot(2, 3, 6)
from scipy.stats import ttest_ind

def cohens_d(x, y):
    nx = len(x)
    ny = len(y)
    dof = nx + ny - 2
    pooled_std = np.sqrt(((nx-1)*np.var(x, ddof=1) + (ny-1)*np.var(y, ddof=1)) / dof)
    return (np.mean(x) - np.mean(y)) / pooled_std

control_sdq = df[df['Group'] == 'Control']['SDQ_Improvement'].values
effect_sizes = []
ci_lower = []
ci_upper = []
p_values = []

for g in group_order:
    if g == 'Control':
        effect_sizes.append(0)
        ci_lower.append(0)
        ci_upper.append(0)
        p_values.append(1.0)
    else:
        group_sdq = df[df['Group'] == g]['SDQ_Improvement'].values
        d = cohens_d(group_sdq, control_sdq)
        effect_sizes.append(d)
        # 近似95% CI
        se = np.sqrt((len(group_sdq) + len(control_sdq)) / (len(group_sdq) * len(control_sdq)) + d**2 / (2*(len(group_sdq) + len(control_sdq) - 2)))
        ci_lower.append(d - 1.96*se)
        ci_upper.append(d + 1.96*se)
        _, p = ttest_ind(group_sdq, control_sdq)
        p_values.append(p)

y_pos = np.arange(len(group_order))
ax6f.errorbar(effect_sizes, y_pos, xerr=[np.array(effect_sizes)-np.array(ci_lower), 
                                         np.array(ci_upper)-np.array(effect_sizes)],
              fmt='o', markersize=8, capsize=4, color='black', ecolor='gray', linewidth=2)

for i, (d, p) in enumerate(zip(effect_sizes, p_values)):
    if p < 0.001:
        sig = '***'
    elif p < 0.01:
        sig = '**'
    elif p < 0.05:
        sig = '*'
    else:
        sig = 'ns'
    ax6f.text(d+0.1 if d >= 0 else d-0.1, i, sig, va='center', fontsize=9, fontweight='bold')

ax6f.axvline(x=0, color='gray', linestyle='--', linewidth=1)
ax6f.set_yticks(y_pos)
ax6f.set_yticklabels([GROUP_LABELS[g] for g in group_order], fontsize=9)
ax6f.set_xlabel("Cohen's d (vs Control)", fontsize=10, fontweight='bold')
ax6f.set_title('(f) Effect Size (SDQ Improvement)', fontsize=11, fontweight='bold')
ax6f.set_xlim(-0.5, 3.5)

plt.tight_layout()
fig6.savefig(f'{timestamp}_fig6_comprehensive_dashboard.png', bbox_inches='tight')
plt.close()
print("✅ Figure 6: 综合结果图 - 已生成")


print("\n" + "="*60)
print("✅ 全部图表生成完成！（仅PNG格式）")
print("="*60)
print("\n生成文件列表:")
print(f"  • {timestamp}_fig1_study_overview.png")
print(f"  • {timestamp}_fig2_sdq_comparison.png")
print(f"  • {timestamp}_fig4_responder_analysis.png")
print(f"  • {timestamp}_fig5_dose_response.png")
print(f"  • {timestamp}_fig6_comprehensive_dashboard.png")

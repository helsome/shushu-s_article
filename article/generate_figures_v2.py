# -*- coding: utf-8 -*-
"""
论文图表生成脚本 v2
生成4张更新后的图表，包含最新数据
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# macOS中文字体设置
for font in ['Heiti SC', 'PingFang SC', 'STSong', 'Arial Unicode MS', 'SimHei']:
    try:
        matplotlib.font_manager.findfont(font, fallback_to_default=False)
        plt.rcParams['font.sans-serif'] = [font]
        break
    except Exception:
        continue
plt.rcParams['axes.unicode_minus'] = False

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(OUT_DIR, 'figures'), exist_ok=True)


def create_pricing_timeline():
    """图1：OpenAI定价策略演变时间线（2022-2024）"""
    fig, ax = plt.subplots(figsize=(14, 5))

    events = [
        ('2022.11', 'ChatGPT发布\n完全免费'),
        ('2023.02', 'Plus推出\n$20/月'),
        ('2023.03', 'GPT-4发布\nPlus专属'),
        ('2023.08', 'Enterprise版\n定制化定价'),
        ('2023.11', 'GPT-4 Turbo\nAPI降价'),
        ('2024.01', 'Team版推出\n$25-30/人/月'),
        ('2024.05', 'GPT-4o发布\n免费用户可用'),
        ('2024.12', 'Pro版推出\n$200/月'),
    ]

    y_base = 0.5
    colors = ['#e74c3c', '#2ecc71', '#3498db', '#9b59b6',
              '#f39c12', '#1abc9c', '#e67e22', '#8e44ad']

    # Draw timeline
    ax.plot(range(len(events)), [y_base]*len(events), '-', color='#34495e', linewidth=2.5, zorder=1)

    for i, (date, event) in enumerate(events):
        # Alternate above/below
        if i % 2 == 0:
            y_text = y_base + 0.22
            y_date = y_base - 0.10
            va_text = 'bottom'
        else:
            y_text = y_base - 0.22
            y_date = y_base + 0.10
            va_text = 'top'

        ax.plot(i, y_base, 'o', markersize=12, color=colors[i], zorder=3,
                markeredgecolor='white', markeredgewidth=2)

        ax.annotate(event, (i, y_text), ha='center', va=va_text, fontsize=8.5,
                    bbox=dict(boxstyle='round,pad=0.4', facecolor=colors[i], alpha=0.15,
                              edgecolor=colors[i], linewidth=1))

        ax.annotate(date, (i, y_date), ha='center', fontsize=8, fontweight='bold', color='#2c3e50')

        # Connector line
        ax.plot([i, i], [y_base, y_text], '-', color=colors[i], linewidth=1, alpha=0.5, zorder=2)

    ax.set_xlim(-0.8, len(events)-0.2)
    ax.set_ylim(-0.05, 1.05)
    ax.axis('off')
    ax.set_title('图1  OpenAI定价策略演变时间线（2022-2024）', fontsize=13, fontweight='bold', pad=15)

    plt.tight_layout()
    for p in [os.path.join(OUT_DIR, 'fig1_pricing_timeline.png'),
              os.path.join(OUT_DIR, 'figures', 'fig1_pricing_timeline.png')]:
        plt.savefig(p, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print("图1 已生成")


def create_competitor_comparison():
    """图2：主要AI产品月订阅定价对比"""
    fig, ax = plt.subplots(figsize=(11, 6))

    products = ['OpenAI\nChatGPT', 'Anthropic\nClaude', 'Google\nGemini',
                'DeepSeek', 'Microsoft\nCopilot']

    # Standard tier prices
    standard = [20, 20, 19.99, 0, 20]
    # Premium tier prices
    premium = [200, 100, 249.99, 0, 30]

    x = np.arange(len(products))
    width = 0.35

    colors_std = ['#10a37f', '#d4a574', '#4285f4', '#ff6b6b', '#00a4ef']
    colors_prm = ['#0d8c6c', '#b8915f', '#3367d6', '#e05555', '#0090d9']

    bars1 = ax.bar(x - width/2, standard, width, label='标准订阅', color=colors_std,
                   edgecolor='white', linewidth=1.5)
    bars2 = ax.bar(x + width/2, premium, width, label='高级/企业订阅', color=colors_prm,
                   edgecolor='white', linewidth=1.5, alpha=0.7)

    # Value labels
    for bar, val in zip(bars1, standard):
        if val > 0:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3,
                    f'${val}', ha='center', va='bottom', fontsize=9, fontweight='bold')
        else:
            ax.text(bar.get_x() + bar.get_width()/2, 3,
                    '免费', ha='center', va='bottom', fontsize=9, fontweight='bold', color='#e74c3c')

    for bar, val in zip(bars2, premium):
        if val > 0:
            label = f'${int(val)}' if val == int(val) else f'${val}'
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3,
                    label, ha='center', va='bottom', fontsize=9, fontweight='bold')
        else:
            ax.text(bar.get_x() + bar.get_width()/2, 3,
                    'N/A', ha='center', va='bottom', fontsize=8, color='gray')

    # Standard tier labels
    tier_labels = ['Plus', 'Pro', 'Advanced', '免费聊天', 'Pro']
    premium_labels = ['Pro', 'Max', 'Ultra', '—', 'Business']
    for i, (sl, pl) in enumerate(zip(tier_labels, premium_labels)):
        ax.text(x[i] - width/2, -18, sl, ha='center', fontsize=7.5, color='#555')
        ax.text(x[i] + width/2, -18, pl, ha='center', fontsize=7.5, color='#555')

    ax.set_ylabel('月订阅价格（美元）', fontsize=11)
    ax.set_title('图2  主要AI产品月订阅定价对比', fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(products, fontsize=10)
    ax.set_ylim(0, 290)
    ax.legend(loc='upper left', fontsize=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.annotate('注：DeepSeek仅提供API按量计费，无订阅制产品；Google Ultra于2025年推出',
                xy=(0.5, -0.15), xycoords='axes fraction', ha='center', fontsize=8,
                style='italic', color='#666')

    plt.tight_layout()
    for p in [os.path.join(OUT_DIR, 'fig2_competitor_pricing.png'),
              os.path.join(OUT_DIR, 'figures', 'fig2_competitor_pricing.png')]:
        plt.savefig(p, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print("图2 已生成")


def create_cost_structure():
    """图3：生成式AI企业成本结构估算"""
    fig, ax = plt.subplots(figsize=(8, 7))

    labels = ['GPU算力/推理成本\n50%', '研发人员\n25%', '数据中心运营\n12%',
              '销售与管理\n8%', '其他\n5%']
    sizes = [50, 25, 12, 8, 5]
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#95a5a6']
    explode = (0.06, 0, 0, 0, 0)

    wedges, texts, autotexts = ax.pie(
        sizes, explode=explode, labels=None, colors=colors,
        autopct='', startangle=140, pctdistance=0.75,
        wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2))

    # Custom legend
    legend_labels = ['GPU算力/推理成本 (50%)', '研发人员 (25%)',
                     '数据中心运营 (12%)', '销售与管理 (8%)', '其他 (5%)']
    ax.legend(wedges, legend_labels, loc='center left', bbox_to_anchor=(0.85, 0.5),
              fontsize=9.5, frameon=False)

    # Center text
    ax.text(0, 0, '成本\n结构', ha='center', va='center', fontsize=14,
            fontweight='bold', color='#2c3e50')

    ax.set_title('图3  生成式AI企业成本结构估算', fontsize=13, fontweight='bold', y=1.02)

    plt.figtext(0.5, 0.02,
                '数据来源：基于a16z "Who Owns the Generative AI Platform" (2023) 及行业公开数据估算',
                ha='center', fontsize=8, style='italic', color='#888')

    plt.tight_layout()
    for p in [os.path.join(OUT_DIR, 'fig3_cost_structure.png'),
              os.path.join(OUT_DIR, 'figures', 'fig3_cost_structure.png')]:
        plt.savefig(p, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print("图3 已生成")


def create_price_discrimination_diagram():
    """图4：OpenAI多层级定价的价格歧视效果示意"""
    fig, ax = plt.subplots(figsize=(10, 7))

    # Demand curve
    q = np.linspace(0.05, 12, 200)
    p = 55 * np.exp(-0.18 * q)  # Exponential demand for better shape

    ax.plot(q, p, color='#2c3e50', linewidth=2.5, label='需求曲线 D', zorder=3)

    # Marginal cost
    mc = 8
    ax.axhline(y=mc, color='#e74c3c', linestyle='--', linewidth=1.5,
               label=f'边际成本 MC≈${mc}', alpha=0.8)

    # Price tiers (from high to low)
    tiers = [
        ('Enterprise\n(定制化)', 45, '#8e44ad', 0.15),
        ('Pro\n($200/月)', 35, '#9b59b6', 0.2),
        ('Plus\n($20/月)', 20, '#3498db', 0.25),
        ('Go\n($8/月)', 10, '#2ecc71', 0.15),
        ('Free\n(边际成本)', mc, '#95a5a6', 0.1),
    ]

    prev_p = 55
    for label, price, color, alpha in tiers:
        # Find q at this price on demand curve
        q_at_p = -np.log(price / 55) / 0.18 if price > 0 else 12

        # Shaded region (consumer surplus extracted at this tier)
        mask = (p >= price) & (p <= prev_p)
        if np.any(mask):
            ax.fill_between(q[mask], price, p[mask], alpha=alpha, color=color, zorder=2)

        # Price line
        ax.plot([0, q_at_p], [price, price], '--', color=color, alpha=0.6, linewidth=1)
        ax.plot([q_at_p, q_at_p], [0, price], '--', color=color, alpha=0.4, linewidth=0.8)
        ax.scatter([q_at_p], [price], s=60, color=color, zorder=4, edgecolors='white', linewidth=1.5)

        # Label
        if price >= 20:
            ax.annotate(label, (q_at_p + 0.3, price + 1), fontsize=9, color=color, fontweight='bold')
        else:
            ax.annotate(label, (q_at_p + 0.3, price - 1), fontsize=9, color=color, fontweight='bold')

        prev_p = price

    ax.set_xlabel('用户数量 Q', fontsize=11)
    ax.set_ylabel('价格/价值 P（美元/月）', fontsize=11)
    ax.set_title('图4  OpenAI多层级定价的价格歧视效果示意', fontsize=13, fontweight='bold')
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 58)
    ax.legend(loc='upper right', fontsize=10, framealpha=0.9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.annotate('注：纵轴价格为示意性标注，反映各层级的相对价值定位',
                xy=(0.5, -0.08), xycoords='axes fraction', ha='center',
                fontsize=8, style='italic', color='#888')

    plt.tight_layout()
    for p in [os.path.join(OUT_DIR, 'fig4_price_discrimination.png'),
              os.path.join(OUT_DIR, 'figures', 'fig4_price_discrimination.png')]:
        plt.savefig(p, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print("图4 已生成")


if __name__ == '__main__':
    print("开始生成论文图表 v2...")
    print("-" * 40)
    create_pricing_timeline()
    create_competitor_comparison()
    create_cost_structure()
    create_price_discrimination_diagram()
    print("-" * 40)
    print("所有图表生成完成！")

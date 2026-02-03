# -*- coding: utf-8 -*-
"""
论文图表生成脚本
生成：定价演变图、产品分层表、竞品对比图、成本结构图
注意：当前使用模拟数据，待替换为真实数据
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# ============================================
# 图1：OpenAI定价策略演变时间线
# ============================================
def create_pricing_timeline():
    fig, ax = plt.subplots(figsize=(12, 6))

    # 时间节点和事件 【待补充：确认具体日期】
    events = [
        ('2022.11', 'ChatGPT发布\n完全免费', 0),
        ('2023.02', 'Plus推出\n$20/月', 20),
        ('2023.03', 'GPT-4发布\nPlus专属', 20),
        ('2023.11', 'GPT-4 Turbo\nAPI降价', 20),
        ('2024.01', 'Team版推出\n$25-30/人/月', 30),
        ('2024.04', 'Enterprise\n定制化定价', 50),
    ]

    # 绘制时间线
    y_base = 0.5
    for i, (date, event, price) in enumerate(events):
        x = i
        ax.plot(x, y_base, 'o', markersize=15, color='#1a73e8')
        ax.annotate(date, (x, y_base - 0.15), ha='center', fontsize=10, fontweight='bold')
        ax.annotate(event, (x, y_base + 0.15), ha='center', fontsize=9,
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.7))

    # 连接线
    ax.plot(range(len(events)), [y_base]*len(events), '-', color='#1a73e8', linewidth=2)

    ax.set_xlim(-0.5, len(events)-0.5)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('图1 OpenAI定价策略演变时间线（2022-2024）', fontsize=14, fontweight='bold', pad=20)

    plt.tight_layout()
    plt.savefig('figures/fig1_pricing_timeline.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("图1 已生成: figures/fig1_pricing_timeline.png")


# ============================================
# 图2：竞品定价对比柱状图
# ============================================
def create_competitor_comparison():
    fig, ax = plt.subplots(figsize=(10, 6))

    # 竞品数据 【待补充：确认最新定价】
    products = ['OpenAI\nChatGPT Plus', 'Anthropic\nClaude Pro', 'Google\nGemini Advanced',
                'DeepSeek\nAPI(等效)', 'Microsoft\nCopilot Pro']
    prices = [20, 20, 19.99, 2, 20]  # DeepSeek按等效使用量估算
    colors = ['#10a37f', '#d4a574', '#4285f4', '#ff6b6b', '#00a4ef']

    bars = ax.bar(products, prices, color=colors, edgecolor='black', linewidth=1.2)

    # 添加数值标签
    for bar, price in zip(bars, prices):
        height = bar.get_height()
        ax.annotate(f'${price}',
                   xy=(bar.get_x() + bar.get_width()/2, height),
                   xytext=(0, 3), textcoords="offset points",
                   ha='center', va='bottom', fontsize=11, fontweight='bold')

    ax.set_ylabel('月订阅价格（美元）', fontsize=12)
    ax.set_title('图2 主要AI产品月订阅定价对比', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 30)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # 添加注释
    ax.annotate('注：DeepSeek为API按量计费，此处按等效使用量估算月成本',
               xy=(0.5, -0.12), xycoords='axes fraction', ha='center', fontsize=9, style='italic')

    plt.tight_layout()
    plt.savefig('figures/fig2_competitor_pricing.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("图2 已生成: figures/fig2_competitor_pricing.png")


# ============================================
# 图3：OpenAI成本结构估算（饼图）
# ============================================
def create_cost_structure():
    fig, ax = plt.subplots(figsize=(8, 8))

    # 成本结构 【待补充：需要研报数据支撑】
    labels = ['GPU算力/推理成本', '研发人员', '数据中心运营', '销售与管理', '其他']
    sizes = [50, 25, 12, 8, 5]  # 模拟数据，推理成本约50%
    colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#ffeaa7']
    explode = (0.05, 0, 0, 0, 0)

    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                                       autopct='%1.1f%%', startangle=90,
                                       textprops={'fontsize': 11})

    ax.set_title('图3 生成式AI企业成本结构估算', fontsize=14, fontweight='bold')

    # 添加注释
    plt.figtext(0.5, 0.02, '数据来源：【待补充：a16z/BCG研报】', ha='center', fontsize=9, style='italic')

    plt.tight_layout()
    plt.savefig('figures/fig3_cost_structure.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("图3 已生成: figures/fig3_cost_structure.png")


# ============================================
# 图4：价格歧视效果示意图（经济学模型图）
# ============================================
def create_price_discrimination_diagram():
    fig, ax = plt.subplots(figsize=(10, 7))

    # 需求曲线
    q = np.linspace(0.1, 10, 100)
    p = 50 - 4*q  # 线性需求曲线 P = 50 - 4Q

    ax.plot(q, p, 'b-', linewidth=2, label='需求曲线 D')

    # 边际成本线（假设固定）
    mc = 10
    ax.axhline(y=mc, color='r', linestyle='--', linewidth=1.5, label=f'边际成本 MC=${mc}')

    # 三个价格层级
    prices = [20, 27.5, 40]  # Free(边际), Plus, Enterprise
    labels = ['Free层\n(边际成本)', 'Plus层\n($20/月)', 'Enterprise层\n(定制化)']
    colors = ['#95a5a6', '#3498db', '#9b59b6']

    for i, (price, label, color) in enumerate(zip(prices, labels, colors)):
        q_at_p = (50 - price) / 4
        ax.plot([0, q_at_p], [price, price], '--', color=color, alpha=0.7)
        ax.plot([q_at_p, q_at_p], [0, price], '--', color=color, alpha=0.7)
        ax.scatter([q_at_p], [price], s=100, color=color, zorder=5)
        ax.annotate(label, (q_at_p + 0.3, price), fontsize=10, color=color)

    # 填充消费者剩余区域
    q_plus = (50 - 20) / 4
    ax.fill_between(q[:int(q_plus*10)], 20, p[:int(q_plus*10)], alpha=0.3, color='green',
                   label='消费者剩余')

    ax.set_xlabel('用户数量 Q', fontsize=12)
    ax.set_ylabel('价格 P（美元/月）', fontsize=12)
    ax.set_title('图4 OpenAI多层级定价的价格歧视效果示意', fontsize=14, fontweight='bold')
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 55)
    ax.legend(loc='upper right')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig('figures/fig4_price_discrimination.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("图4 已生成: figures/fig4_price_discrimination.png")


# ============================================
# 主函数
# ============================================
if __name__ == '__main__':
    print("开始生成论文图表...")
    print("-" * 40)

    create_pricing_timeline()
    create_competitor_comparison()
    create_cost_structure()
    create_price_discrimination_diagram()

    print("-" * 40)
    print("所有图表生成完成！")
    print("\n【注意】当前图表使用模拟数据，需要替换为真实数据后重新运行。")

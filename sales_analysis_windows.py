"""
January Monthly Sales Analysis Dashboard
Data Analyst: Sales Performance Report
Windows Compatible Version
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Rectangle
import warnings
import os
warnings.filterwarnings('ignore')

# Set style for better visualizations
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Set random seed for reproducibility
np.random.seed(42)

# Create output directory if it doesn't exist
OUTPUT_DIR = os.path.join(os.getcwd(), 'output')
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    print(f"✓ Created output directory: {OUTPUT_DIR}")

# Sales Data Configuration
ACTUAL_SALES = 350  # MT (Metric Tons)
TARGET_SALES = 590  # MT (Metric Tons)

# Product Configuration
PRODUCTS = {
    '10W-30 (4T Motor Oil)': {'price_per_mt': 1500, 'min_share': 0.15, 'max_share': 0.25},
    '20W-50 (SuperGT)': {'price_per_mt': 1800, 'min_share': 0.20, 'max_share': 0.30},
    '15W-40 (TitanTruck Plus)': {'price_per_mt': 1600, 'min_share': 0.18, 'max_share': 0.28},
    'Grease (FN-3)': {'price_per_mt': 2000, 'min_share': 0.10, 'max_share': 0.18},
    'Industrial (Renolin B)': {'price_per_mt': 2200, 'min_share': 0.12, 'max_share': 0.20}
}

# Area Configuration
AREAS = ['Dhaka', 'Rajshahi', 'Khulna', 'Shylet', 'Bogura']

# Salesman Configuration
SALESMEN = ['John Smith', 'Sarah Johnson', 'Michael Brown', 'Emily Davis', 
            'David Wilson', 'Jessica Martinez', 'Robert Taylor', 'Lisa Anderson']

def generate_sales_data():
    """Generate realistic sales data"""
    
    # Generate Product-wise sales
    product_shares = {}
    remaining = 1.0
    
    for i, (product, config) in enumerate(PRODUCTS.items()):
        if i == len(PRODUCTS) - 1:
            share = remaining
        else:
            share = np.random.uniform(config['min_share'], config['max_share'])
            remaining -= share
        product_shares[product] = share
    
    # Normalize to ensure sum = 1
    total = sum(product_shares.values())
    product_shares = {k: v/total for k, v in product_shares.items()}
    
    product_sales = {k: round(v * ACTUAL_SALES, 2) for k, v in product_shares.items()}
    
    # Generate Area-wise sales
    area_sales = {}
    remaining = ACTUAL_SALES
    for i, area in enumerate(AREAS):
        if i == len(AREAS) - 1:
            area_sales[area] = round(remaining, 2)
        else:
            sale = np.random.uniform(0.15, 0.25) * ACTUAL_SALES
            area_sales[area] = round(sale, 2)
            remaining -= sale
    
    # Normalize area sales
    total_area = sum(area_sales.values())
    area_sales = {k: round(v * ACTUAL_SALES / total_area, 2) for k, v in area_sales.items()}
    
    # Generate Salesman-wise sales with product breakdown
    salesman_data = []
    total_salesman_sales = 0
    
    for i, salesman in enumerate(SALESMEN):
        if i == len(SALESMEN) - 1:
            total_sales = ACTUAL_SALES - total_salesman_sales
        else:
            total_sales = np.random.uniform(30, 60)
            total_salesman_sales += total_sales
        
        area = np.random.choice(AREAS)
        
        # Distribute sales across products for this salesman
        for product in PRODUCTS.keys():
            product_sale = np.random.uniform(0.1, 0.3) * total_sales
            salesman_data.append({
                'Salesman': salesman,
                'Product': product,
                'Area': area,
                'Sales_MT': round(product_sale, 2),
                'Revenue': round(product_sale * PRODUCTS[product]['price_per_mt'], 2)
            })
    
    salesman_df = pd.DataFrame(salesman_data)
    
    # Normalize salesman sales to match actual total
    current_total = salesman_df['Sales_MT'].sum()
    salesman_df['Sales_MT'] = (salesman_df['Sales_MT'] / current_total * ACTUAL_SALES).round(2)
    salesman_df['Revenue'] = salesman_df.apply(
        lambda x: round(x['Sales_MT'] * PRODUCTS[x['Product']]['price_per_mt'], 2), axis=1
    )
    
    return product_sales, area_sales, salesman_df

def create_overview_dashboard(product_sales, area_sales):
    """Create overview dashboard with key metrics"""
    
    fig = plt.figure(figsize=(16, 10))
    fig.suptitle('January 2024 - Monthly Sales Analysis Dashboard', 
                 fontsize=20, fontweight='bold', y=0.98)
    
    # Create grid
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # 1. Sales vs Target Gauge
    ax1 = fig.add_subplot(gs[0, 0])
    achievement = (ACTUAL_SALES / TARGET_SALES) * 100
    
    colors = ['#ff4444' if achievement < 60 else '#ffaa00' if achievement < 80 else '#44ff44']
    ax1.barh(['Achievement'], [achievement], color=colors[0], height=0.4)
    ax1.barh(['Target'], [100], color='lightgray', height=0.4, alpha=0.3)
    ax1.set_xlim(0, 120)
    ax1.set_xlabel('Percentage (%)', fontweight='bold')
    ax1.set_title('Sales Achievement vs Target', fontweight='bold', pad=10)
    ax1.text(achievement + 2, 0, f'{achievement:.1f}%', va='center', fontweight='bold', fontsize=11)
    ax1.axvline(100, color='green', linestyle='--', linewidth=2, alpha=0.7)
    
    # 2. Key Metrics Card
    ax2 = fig.add_subplot(gs[0, 1:])
    ax2.axis('off')
    
    metrics_text = f"""
    📊 KEY PERFORMANCE INDICATORS
    
    Actual Sales:        {ACTUAL_SALES} MT
    Target Sales:        {TARGET_SALES} MT
    Variance:            {ACTUAL_SALES - TARGET_SALES} MT ({achievement - 100:.1f}%)
    
    Total Revenue:       ${sum(product_sales[p] * PRODUCTS[p]['price_per_mt'] for p in product_sales):,.2f}
    Active Areas:        {len(area_sales)}
    Active Products:     {len(product_sales)}
    """
    
    ax2.text(0.05, 0.5, metrics_text, transform=ax2.transAxes, 
             fontsize=11, verticalalignment='center', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    # 3. Product-wise Sales (Horizontal Bar)
    ax3 = fig.add_subplot(gs[1, :])
    products = list(product_sales.keys())
    sales = list(product_sales.values())
    
    colors_prod = sns.color_palette("Set2", len(products))
    bars = ax3.barh(products, sales, color=colors_prod, edgecolor='black', linewidth=1.2)
    
    ax3.set_xlabel('Sales (MT)', fontweight='bold', fontsize=11)
    ax3.set_title('Product-wise Sales Distribution', fontweight='bold', fontsize=13, pad=15)
    ax3.grid(axis='x', alpha=0.3)
    
    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, sales)):
        percentage = (val / ACTUAL_SALES) * 100
        ax3.text(val + 3, bar.get_y() + bar.get_height()/2, 
                f'{val:.1f} MT ({percentage:.1f}%)', 
                va='center', fontweight='bold', fontsize=9)
    
    # 4. Area-wise Sales (Pie Chart)
    ax4 = fig.add_subplot(gs[2, :2])
    areas = list(area_sales.keys())
    area_values = list(area_sales.values())
    
    colors_area = sns.color_palette("Set3", len(areas))
    wedges, texts, autotexts = ax4.pie(area_values, labels=areas, autopct='%1.1f%%',
                                         colors=colors_area, startangle=90,
                                         textprops={'fontweight': 'bold', 'fontsize': 9})
    
    ax4.set_title('Area-wise Sales Distribution', fontweight='bold', fontsize=13, pad=15)
    
    # Add legend with MT values
    legend_labels = [f'{area}: {val:.1f} MT' for area, val in zip(areas, area_values)]
    ax4.legend(legend_labels, loc='upper left', bbox_to_anchor=(1, 1), fontsize=9)
    
    # 5. Top 3 Products
    ax5 = fig.add_subplot(gs[2, 2])
    ax5.axis('off')
    
    sorted_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:3]
    
    top3_text = "🏆 TOP 3 PRODUCTS\n\n"
    medals = ['🥇', '🥈', '🥉']
    for i, (prod, sale) in enumerate(sorted_products):
        revenue = sale * PRODUCTS[prod]['price_per_mt']
        top3_text += f"{medals[i]} {prod}\n   {sale:.1f} MT | ${revenue:,.0f}\n\n"
    
    ax5.text(0.1, 0.5, top3_text, transform=ax5.transAxes, 
             fontsize=10, verticalalignment='center',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.4))
    
    output_path = os.path.join(OUTPUT_DIR, 'sales_overview_dashboard.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Overview Dashboard created: {output_path}")
    plt.show()  # Display the plot interactively
    plt.close()

def create_product_analysis(product_sales):
    """Detailed product analysis with seaborn"""
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Product-wise Detailed Analysis', fontsize=18, fontweight='bold', y=0.98)
    
    # Prepare data
    products = list(product_sales.keys())
    sales = list(product_sales.values())
    revenue = [sales[i] * PRODUCTS[products[i]]['price_per_mt'] for i in range(len(products))]
    
    df_products = pd.DataFrame({
        'Product': products,
        'Sales_MT': sales,
        'Revenue': revenue
    })
    
    # 1. Sales Bar Chart with Seaborn
    sns.barplot(data=df_products, x='Sales_MT', y='Product', ax=axes[0, 0], 
                palette='viridis', edgecolor='black', linewidth=1.5)
    axes[0, 0].set_title('Sales Volume by Product', fontweight='bold', fontsize=12)
    axes[0, 0].set_xlabel('Sales (MT)', fontweight='bold')
    axes[0, 0].set_ylabel('Product', fontweight='bold')
    
    for i, (idx, row) in enumerate(df_products.iterrows()):
        axes[0, 0].text(row['Sales_MT'] + 1, i, f"{row['Sales_MT']:.1f}", 
                       va='center', fontweight='bold')
    
    # 2. Revenue Analysis
    sns.barplot(data=df_products, x='Revenue', y='Product', ax=axes[0, 1], 
                palette='rocket', edgecolor='black', linewidth=1.5)
    axes[0, 1].set_title('Revenue by Product', fontweight='bold', fontsize=12)
    axes[0, 1].set_xlabel('Revenue ($)', fontweight='bold')
    axes[0, 1].set_ylabel('')
    axes[0, 1].ticklabel_format(style='plain', axis='x')
    
    for i, (idx, row) in enumerate(df_products.iterrows()):
        axes[0, 1].text(row['Revenue'] + 5000, i, f"${row['Revenue']:,.0f}", 
                       va='center', fontweight='bold', fontsize=9)
    
    # 3. Market Share (Donut Chart)
    colors = sns.color_palette("pastel", len(products))
    wedges, texts, autotexts = axes[1, 0].pie(sales, labels=products, autopct='%1.1f%%',
                                                colors=colors, startangle=45,
                                                pctdistance=0.85,
                                                textprops={'fontsize': 9, 'fontweight': 'bold'})
    
    # Create donut
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    axes[1, 0].add_artist(centre_circle)
    axes[1, 0].set_title('Market Share Distribution', fontweight='bold', fontsize=12, pad=15)
    
    # 4. Comparative Analysis Table
    axes[1, 1].axis('off')
    
    table_data = []
    for prod, sale in product_sales.items():
        rev = sale * PRODUCTS[prod]['price_per_mt']
        share = (sale / ACTUAL_SALES) * 100
        table_data.append([prod, f"{sale:.1f}", f"${rev:,.0f}", f"{share:.1f}%"])
    
    table = axes[1, 1].table(cellText=table_data,
                            colLabels=['Product', 'Sales (MT)', 'Revenue', 'Share'],
                            cellLoc='left',
                            loc='center',
                            colWidths=[0.4, 0.2, 0.2, 0.2])
    
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2)
    
    # Style header
    for i in range(4):
        table[(0, i)].set_facecolor('#4CAF50')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # Alternate row colors
    for i in range(1, len(table_data) + 1):
        for j in range(4):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#f0f0f0')
    
    axes[1, 1].set_title('Product Performance Summary', fontweight='bold', fontsize=12, pad=20)
    
    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, 'product_analysis.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Product Analysis created: {output_path}")
    plt.show()  # Display the plot interactively
    plt.close()

def create_salesman_analysis(salesman_df):
    """Salesman performance analysis"""
    
    fig, axes = plt.subplots(2, 2, figsize=(18, 12))
    fig.suptitle('Salesman Performance Analysis', fontsize=18, fontweight='bold', y=0.98)
    
    # Aggregate salesman data
    salesman_summary = salesman_df.groupby('Salesman').agg({
        'Sales_MT': 'sum',
        'Revenue': 'sum'
    }).reset_index().sort_values('Sales_MT', ascending=False)
    
    # 1. Top Performers (Bar Chart)
    sns.barplot(data=salesman_summary, x='Sales_MT', y='Salesman', 
                ax=axes[0, 0], palette='coolwarm', edgecolor='black', linewidth=1.2)
    axes[0, 0].set_title('Salesman-wise Total Sales', fontweight='bold', fontsize=13)
    axes[0, 0].set_xlabel('Total Sales (MT)', fontweight='bold')
    axes[0, 0].set_ylabel('Salesman', fontweight='bold')
    
    for i, (idx, row) in enumerate(salesman_summary.iterrows()):
        axes[0, 0].text(row['Sales_MT'] + 1, i, f"{row['Sales_MT']:.1f} MT", 
                       va='center', fontweight='bold', fontsize=9)
    
    # 2. Revenue Performance
    sns.barplot(data=salesman_summary, x='Revenue', y='Salesman', 
                ax=axes[0, 1], palette='viridis', edgecolor='black', linewidth=1.2)
    axes[0, 1].set_title('Revenue Generated by Salesman', fontweight='bold', fontsize=13)
    axes[0, 1].set_xlabel('Revenue ($)', fontweight='bold')
    axes[0, 1].set_ylabel('')
    axes[0, 1].ticklabel_format(style='plain', axis='x')
    
    # 3. Salesman-Product Heatmap
    pivot_data = salesman_df.pivot_table(values='Sales_MT', 
                                         index='Salesman', 
                                         columns='Product', 
                                         aggfunc='sum', 
                                         fill_value=0)
    
    sns.heatmap(pivot_data, annot=True, fmt='.1f', cmap='YlOrRd', 
                ax=axes[1, 0], cbar_kws={'label': 'Sales (MT)'},
                linewidths=0.5, linecolor='gray')
    axes[1, 0].set_title('Salesman × Product Sales Matrix', fontweight='bold', fontsize=13)
    axes[1, 0].set_xlabel('Product', fontweight='bold')
    axes[1, 0].set_ylabel('Salesman', fontweight='bold')
    plt.setp(axes[1, 0].get_xticklabels(), rotation=45, ha='right', fontsize=8)
    plt.setp(axes[1, 0].get_yticklabels(), fontsize=9)
    
    # 4. Performance Distribution
    axes[1, 1].axis('off')
    
    # Top 3 Salesmen
    top3_salesmen = salesman_summary.head(3)
    
    performance_text = "⭐ TOP 3 SALESMEN\n\n"
    medals = ['🥇', '🥈', '🥉']
    
    for i, (idx, row) in enumerate(top3_salesmen.iterrows()):
        performance_text += f"{medals[i]} {row['Salesman']}\n"
        performance_text += f"   Sales: {row['Sales_MT']:.1f} MT\n"
        performance_text += f"   Revenue: ${row['Revenue']:,.0f}\n\n"
    
    # Performance stats
    avg_sales = salesman_summary['Sales_MT'].mean()
    performance_text += f"\n📈 STATISTICS\n\n"
    performance_text += f"Average Sales: {avg_sales:.1f} MT\n"
    performance_text += f"Highest: {salesman_summary['Sales_MT'].max():.1f} MT\n"
    performance_text += f"Lowest: {salesman_summary['Sales_MT'].min():.1f} MT\n"
    
    axes[1, 1].text(0.1, 0.5, performance_text, transform=axes[1, 1].transAxes, 
                   fontsize=11, verticalalignment='center', fontfamily='monospace',
                   bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))
    
    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, 'salesman_analysis.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Salesman Analysis created: {output_path}")
    plt.show()  # Display the plot interactively
    plt.close()

def create_area_analysis(area_sales, salesman_df):
    """Area-wise detailed analysis"""
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Geographic Area Analysis', fontsize=18, fontweight='bold', y=0.98)
    
    # Prepare data
    areas = list(area_sales.keys())
    sales = list(area_sales.values())
    
    df_areas = pd.DataFrame({
        'Area': areas,
        'Sales_MT': sales
    })
    
    # 1. Area Sales Bar Chart
    sns.barplot(data=df_areas, x='Area', y='Sales_MT', ax=axes[0, 0],
                palette='Set2', edgecolor='black', linewidth=1.5)
    axes[0, 0].set_title('Sales by Geographic Area', fontweight='bold', fontsize=13)
    axes[0, 0].set_xlabel('Area', fontweight='bold')
    axes[0, 0].set_ylabel('Sales (MT)', fontweight='bold')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    for i, (idx, row) in enumerate(df_areas.iterrows()):
        axes[0, 0].text(i, row['Sales_MT'] + 2, f"{row['Sales_MT']:.1f}", 
                       ha='center', fontweight='bold')
    
    # 2. Area Performance Comparison
    df_areas_sorted = df_areas.sort_values('Sales_MT', ascending=True)
    colors = ['#ff4444' if x < df_areas['Sales_MT'].mean() else '#44ff44' 
              for x in df_areas_sorted['Sales_MT']]
    
    axes[0, 1].barh(df_areas_sorted['Area'], df_areas_sorted['Sales_MT'], 
                    color=colors, edgecolor='black', linewidth=1.5)
    axes[0, 1].axvline(df_areas['Sales_MT'].mean(), color='blue', 
                       linestyle='--', linewidth=2, label='Average')
    axes[0, 1].set_title('Area Performance vs Average', fontweight='bold', fontsize=13)
    axes[0, 1].set_xlabel('Sales (MT)', fontweight='bold')
    axes[0, 1].legend()
    
    # 3. Area-Product Mix
    area_product = salesman_df.groupby(['Area', 'Product'])['Sales_MT'].sum().reset_index()
    pivot_area_product = area_product.pivot(index='Area', columns='Product', 
                                             values='Sales_MT').fillna(0)
    
    pivot_area_product.plot(kind='bar', stacked=True, ax=axes[1, 0], 
                            colormap='tab10', edgecolor='black', linewidth=0.8)
    axes[1, 0].set_title('Product Mix by Area', fontweight='bold', fontsize=13)
    axes[1, 0].set_xlabel('Area', fontweight='bold')
    axes[1, 0].set_ylabel('Sales (MT)', fontweight='bold')
    axes[1, 0].legend(title='Product', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # 4. Area Statistics Table
    axes[1, 1].axis('off')
    
    table_data = []
    for area, sale in zip(areas, sales):
        share = (sale / ACTUAL_SALES) * 100
        vs_avg = sale - df_areas['Sales_MT'].mean()
        status = "▲" if vs_avg > 0 else "▼"
        table_data.append([area, f"{sale:.1f}", f"{share:.1f}%", f"{status} {abs(vs_avg):.1f}"])
    
    table = axes[1, 1].table(cellText=table_data,
                            colLabels=['Area', 'Sales (MT)', 'Share', 'vs Avg'],
                            cellLoc='center',
                            loc='center',
                            colWidths=[0.3, 0.25, 0.2, 0.25])
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2.5)
    
    for i in range(4):
        table[(0, i)].set_facecolor('#2196F3')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    for i in range(1, len(table_data) + 1):
        for j in range(4):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#e3f2fd')
    
    axes[1, 1].set_title('Area Performance Summary', fontweight='bold', fontsize=12, pad=20)
    
    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, 'area_analysis.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Area Analysis created: {output_path}")
    plt.show()  # Display the plot interactively
    plt.close()

def create_comprehensive_report(product_sales, area_sales, salesman_df):
    """Create a comprehensive single-page report"""
    
    fig = plt.figure(figsize=(20, 14))
    fig.suptitle('JANUARY 2024 - COMPREHENSIVE SALES REPORT', 
                 fontsize=22, fontweight='bold', y=0.97)
    
    gs = fig.add_gridspec(4, 4, hspace=0.35, wspace=0.35)
    
    # Executive Summary
    ax_summary = fig.add_subplot(gs[0, :])
    ax_summary.axis('off')
    
    achievement = (ACTUAL_SALES / TARGET_SALES) * 100
    total_revenue = sum(product_sales[p] * PRODUCTS[p]['price_per_mt'] for p in product_sales)
    
    summary_text = f"""
    ═══════════════════════════════════════════════════════════════════════════════════════════════════════
    EXECUTIVE SUMMARY  |  Achievement: {achievement:.1f}% of Target  |  Status: {'⚠️ Below Target' if achievement < 100 else '✓ Target Met'}
    ═══════════════════════════════════════════════════════════════════════════════════════════════════════
    
    Actual Sales: {ACTUAL_SALES} MT  |  Target: {TARGET_SALES} MT  |  Variance: {ACTUAL_SALES - TARGET_SALES} MT  |  Revenue: ${total_revenue:,.2f}
    """
    
    ax_summary.text(0.5, 0.5, summary_text, transform=ax_summary.transAxes,
                   fontsize=11, ha='center', va='center', fontfamily='monospace',
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
    
    # Product Analysis (2 charts)
    ax1 = fig.add_subplot(gs[1, :2])
    products = list(product_sales.keys())
    sales = list(product_sales.values())
    
    bars = ax1.bar(range(len(products)), sales, color=sns.color_palette("Set2", len(products)),
                   edgecolor='black', linewidth=1.5)
    ax1.set_xticks(range(len(products)))
    ax1.set_xticklabels([p.split('(')[0].strip() for p in products], rotation=45, ha='right')
    ax1.set_ylabel('Sales (MT)', fontweight='bold')
    ax1.set_title('Product Sales Performance', fontweight='bold', fontsize=12)
    ax1.grid(axis='y', alpha=0.3)
    
    for i, (bar, val) in enumerate(zip(bars, sales)):
        ax1.text(bar.get_x() + bar.get_width()/2, val + 2, f'{val:.1f}', 
                ha='center', fontweight='bold', fontsize=9)
    
    # Area Distribution
    ax2 = fig.add_subplot(gs[1, 2:])
    areas = list(area_sales.keys())
    area_vals = list(area_sales.values())
    
    wedges, texts, autotexts = ax2.pie(area_vals, labels=areas, autopct='%1.1f%%',
                                        colors=sns.color_palette("pastel", len(areas)),
                                        startangle=90, textprops={'fontsize': 9})
    ax2.set_title('Geographic Distribution', fontweight='bold', fontsize=12)
    
    # Salesman Performance
    ax3 = fig.add_subplot(gs[2, :])
    salesman_summary = salesman_df.groupby('Salesman')['Sales_MT'].sum().sort_values(ascending=False)
    
    colors_perf = ['#2ecc71' if x > salesman_summary.mean() else '#e74c3c' 
                   for x in salesman_summary.values]
    
    bars = ax3.barh(salesman_summary.index, salesman_summary.values, 
                    color=colors_perf, edgecolor='black', linewidth=1.2)
    ax3.axvline(salesman_summary.mean(), color='blue', linestyle='--', 
                linewidth=2, label=f'Average: {salesman_summary.mean():.1f} MT')
    ax3.set_xlabel('Sales (MT)', fontweight='bold')
    ax3.set_title('Salesman Performance Ranking', fontweight='bold', fontsize=12)
    ax3.legend(loc='lower right')
    ax3.grid(axis='x', alpha=0.3)
    
    for i, (salesman, val) in enumerate(salesman_summary.items()):
        ax3.text(val + 1, i, f'{val:.1f}', va='center', fontweight='bold', fontsize=9)
    
    # Top Products
    ax4 = fig.add_subplot(gs[3, :2])
    ax4.axis('off')
    
    sorted_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)
    
    top_text = "🏆 TOP PERFORMING PRODUCTS\n\n"
    for i, (prod, sale) in enumerate(sorted_products[:3], 1):
        revenue = sale * PRODUCTS[prod]['price_per_mt']
        share = (sale / ACTUAL_SALES) * 100
        top_text += f"{i}. {prod}\n"
        top_text += f"   Sales: {sale:.1f} MT ({share:.1f}%) | Revenue: ${revenue:,.0f}\n\n"
    
    ax4.text(0.05, 0.5, top_text, transform=ax4.transAxes,
            fontsize=10, verticalalignment='center',
            bbox=dict(boxstyle='round', facecolor='#d4edda', alpha=0.6))
    
    # Key Insights
    ax5 = fig.add_subplot(gs[3, 2:])
    ax5.axis('off')
    
    best_area = max(area_sales.items(), key=lambda x: x[1])
    best_salesman = salesman_summary.index[0]
    
    insights_text = f"""
    📊 KEY INSIGHTS
    
    • Best Performing Area: {best_area[0]}
      ({best_area[1]:.1f} MT)
    
    • Top Salesman: {best_salesman}
      ({salesman_summary.iloc[0]:.1f} MT)
    
    • Achievement Gap: {TARGET_SALES - ACTUAL_SALES} MT
      ({100 - achievement:.1f}% below target)
    
    • Avg. Sales per Area: {ACTUAL_SALES/len(areas):.1f} MT
    """
    
    ax5.text(0.05, 0.5, insights_text, transform=ax5.transAxes,
            fontsize=10, verticalalignment='center',
            bbox=dict(boxstyle='round', facecolor='#fff3cd', alpha=0.6))
    
    output_path = os.path.join(OUTPUT_DIR, 'comprehensive_sales_report.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Comprehensive Report created: {output_path}")
    plt.show()  # Display the plot interactively
    plt.close()

def export_data_to_csv(product_sales, area_sales, salesman_df):
    """Export all data to CSV files"""
    
    # Product data
    df_products = pd.DataFrame({
        'Product': list(product_sales.keys()),
        'Sales_MT': list(product_sales.values()),
        'Revenue': [product_sales[p] * PRODUCTS[p]['price_per_mt'] for p in product_sales.keys()],
        'Market_Share_%': [(v/ACTUAL_SALES)*100 for v in product_sales.values()]
    })
    output_path = os.path.join(OUTPUT_DIR, 'product_sales.csv')
    df_products.to_csv(output_path, index=False)
    
    # Area data
    df_areas = pd.DataFrame({
        'Area': list(area_sales.keys()),
        'Sales_MT': list(area_sales.values()),
        'Market_Share_%': [(v/ACTUAL_SALES)*100 for v in area_sales.values()]
    })
    output_path = os.path.join(OUTPUT_DIR, 'area_sales.csv')
    df_areas.to_csv(output_path, index=False)
    
    # Salesman data
    output_path = os.path.join(OUTPUT_DIR, 'salesman_sales.csv')
    salesman_df.to_csv(output_path, index=False)
    
    # Summary data
    summary_data = pd.DataFrame({
        'Metric': ['Actual Sales (MT)', 'Target Sales (MT)', 'Achievement %', 
                   'Variance (MT)', 'Total Revenue ($)', 'Number of Products', 
                   'Number of Areas', 'Number of Salesmen'],
        'Value': [ACTUAL_SALES, TARGET_SALES, 
                 f"{(ACTUAL_SALES/TARGET_SALES)*100:.2f}",
                 ACTUAL_SALES - TARGET_SALES,
                 f"{sum(product_sales[p] * PRODUCTS[p]['price_per_mt'] for p in product_sales):.2f}",
                 len(PRODUCTS), len(AREAS), len(SALESMEN)]
    })
    output_path = os.path.join(OUTPUT_DIR, 'sales_summary.csv')
    summary_data.to_csv(output_path, index=False)
    
    print("\n✓ CSV files exported to output folder:")
    print("  - product_sales.csv")
    print("  - area_sales.csv")
    print("  - salesman_sales.csv")
    print("  - sales_summary.csv")

def main():
    """Main execution function"""
    
    print("="*70)
    print("JANUARY SALES ANALYSIS - DATA GENERATION & VISUALIZATION")
    print("="*70)
    print()
    
    # Generate data
    print("📊 Generating sales data...")
    product_sales, area_sales, salesman_df = generate_sales_data()
    print("✓ Data generation complete\n")
    
    # Create visualizations
    print("🎨 Creating visualizations...")
    print("-" * 70)
    
    create_overview_dashboard(product_sales, area_sales)
    create_product_analysis(product_sales)
    create_salesman_analysis(salesman_df)
    create_area_analysis(area_sales, salesman_df)
    create_comprehensive_report(product_sales, area_sales, salesman_df)
    
    print("-" * 70)
    print()
    
    # Export data
    print("💾 Exporting data to CSV...")
    export_data_to_csv(product_sales, area_sales, salesman_df)
    print()
    
    # Summary
    achievement = (ACTUAL_SALES / TARGET_SALES) * 100
    total_revenue = sum(product_sales[p] * PRODUCTS[p]['price_per_mt'] for p in product_sales)
    
    print("="*70)
    print("ANALYSIS COMPLETE!")
    print("="*70)
    print(f"\n📈 Key Metrics:")
    print(f"   Actual Sales: {ACTUAL_SALES} MT")
    print(f"   Target Sales: {TARGET_SALES} MT")
    print(f"   Achievement: {achievement:.1f}%")
    print(f"   Total Revenue: ${total_revenue:,.2f}")
    print(f"\n📁 Output Location: {OUTPUT_DIR}")
    print(f"   • 5 PNG visualization files")
    print(f"   • 4 CSV data files")
    print(f"\n✅ All reports ready for review!")
    print("="*70)

if __name__ == "__main__":
    main()

"""
Data Visualization with Matplotlib and Seaborn

This module demonstrates comprehensive data visualization techniques
using Python's most popular plotting libraries.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from typing import List, Optional, Any
import warnings
warnings.filterwarnings('ignore')

# Set up the plotting style
plt.style.use('default')
sns.set_palette("husl")


def basic_matplotlib_plots():
    """Demonstrate basic matplotlib plotting functions."""
    print("=== Basic Matplotlib Plots ===")

    # Create sample data
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    y3 = np.sin(x) * np.cos(x)

    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle('Basic Matplotlib Plots', fontsize=16)

    # Line plot
    axes[0, 0].plot(x, y1, 'b-', linewidth=2, label='sin(x)')
    axes[0, 0].plot(x, y2, 'r--', linewidth=2, label='cos(x)')
    axes[0, 0].set_title('Line Plot')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # Scatter plot
    x_scatter = np.random.randn(100)
    y_scatter = np.random.randn(100)
    colors = np.random.rand(100)
    sizes = 100 * np.random.rand(100)

    scatter = axes[0, 1].scatter(x_scatter, y_scatter, c=colors, s=sizes, alpha=0.6, cmap='viridis')
    axes[0, 1].set_title('Scatter Plot')
    plt.colorbar(scatter, ax=axes[0, 1])

    # Bar plot
    categories = ['A', 'B', 'C', 'D', 'E']
    values = [23, 45, 56, 78, 32]

    bars = axes[1, 0].bar(categories, values, color=['red', 'green', 'blue', 'orange', 'purple'])
    axes[1, 0].set_title('Bar Plot')
    axes[1, 0].set_ylabel('Values')

    # Add value labels on bars
    for bar, value in zip(bars, values):
        axes[1, 0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                       str(value), ha='center', va='bottom')

    # Histogram
    data = np.random.normal(0, 1, 1000)
    axes[1, 1].hist(data, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
    axes[1, 1].set_title('Histogram')
    axes[1, 1].set_xlabel('Value')
    axes[1, 1].set_ylabel('Frequency')

    plt.tight_layout()
    plt.savefig('matplotlib_basic_plots.png', dpi=150, bbox_inches='tight')
    plt.show()

    print("Basic plots saved as 'matplotlib_basic_plots.png'")


def advanced_matplotlib_plots():
    """Demonstrate advanced matplotlib features."""
    print("\n=== Advanced Matplotlib Plots ===")

    # Create sample data
    np.random.seed(42)
    x = np.linspace(0, 4*np.pi, 100)

    # Create complex figure
    fig = plt.figure(figsize=(15, 10))

    # 3D plot
    ax1 = fig.add_subplot(221, projection='3d')
    X, Y = np.meshgrid(np.linspace(-5, 5, 50), np.linspace(-5, 5, 50))
    Z = np.sin(np.sqrt(X**2 + Y**2))

    surf = ax1.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
    ax1.set_title('3D Surface Plot')
    plt.colorbar(surf, ax=ax1, shrink=0.5)

    # Pie chart
    ax2 = fig.add_subplot(222)
    sizes = [30, 25, 20, 15, 10]
    labels = ['Category A', 'Category B', 'Category C', 'Category D', 'Category E']
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#ff99cc']

    wedges, texts, autotexts = ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                       startangle=90, wedgeprops=dict(width=0.7))
    ax2.set_title('Donut Chart')
    plt.setp(autotexts, size=8, weight="bold")

    # Box plot
    ax3 = fig.add_subplot(223)
    data = [np.random.normal(0, 1, 100),
            np.random.normal(1, 1.5, 100),
            np.random.normal(-1, 2, 100)]

    bp = ax3.boxplot(data, labels=['Group 1', 'Group 2', 'Group 3'], patch_artist=True)
    ax3.set_title('Box Plot')
    ax3.set_ylabel('Values')

    # Color the boxes
    colors = ['lightblue', 'lightgreen', 'lightcoral']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)

    # Violin plot
    ax4 = fig.add_subplot(224)
    data_dict = {'Group 1': np.random.normal(0, 1, 100),
                 'Group 2': np.random.normal(1, 1.5, 100),
                 'Group 3': np.random.normal(-1, 2, 100)}

    parts = ax4.violinplot([data_dict[key] for key in data_dict.keys()],
                          showmeans=True, showmedians=True)
    ax4.set_xticks([1, 2, 3])
    ax4.set_xticklabels(data_dict.keys())
    ax4.set_title('Violin Plot')
    ax4.set_ylabel('Values')

    plt.tight_layout()
    plt.savefig('matplotlib_advanced_plots.png', dpi=150, bbox_inches='tight')
    plt.show()

    print("Advanced plots saved as 'matplotlib_advanced_plots.png'")


def seaborn_visualizations():
    """Demonstrate seaborn plotting capabilities."""
    print("\n=== Seaborn Visualizations ===")

    # Create sample datasets
    np.random.seed(42)

    # Time series data
    dates = pd.date_range('2023-01-01', periods=100, freq='D')
    ts_data = pd.DataFrame({
        'date': dates,
        'value': np.sin(np.arange(100) * 0.1) + np.random.normal(0, 0.1, 100),
        'category': np.random.choice(['A', 'B', 'C'], 100)
    })

    # Categorical data
    categories = ['A', 'B', 'C', 'D']
    cat_data = pd.DataFrame({
        'category': np.random.choice(categories, 200),
        'value': np.random.randn(200),
        'size': np.random.randint(1, 5, 200)
    })

    # Correlation data
    corr_data = pd.DataFrame(np.random.randn(100, 4),
                           columns=['var1', 'var2', 'var3', 'var4'])
    corr_data['category'] = np.random.choice(['X', 'Y'], 100)

    # Create figure with subplots
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Seaborn Visualizations', fontsize=16)

    # Line plot with confidence interval
    sns.lineplot(data=ts_data, x='date', y='value', ax=axes[0, 0])
    axes[0, 0].set_title('Time Series with Confidence Interval')
    axes[0, 0].tick_params(axis='x', rotation=45)

    # Scatter plot with hue
    sns.scatterplot(data=cat_data, x='category', y='value', hue='category',
                   size='size', ax=axes[0, 1])
    axes[0, 1].set_title('Scatter Plot with Categories')

    # Box plot
    sns.boxplot(data=cat_data, x='category', y='value', ax=axes[0, 2])
    axes[0, 2].set_title('Box Plot by Category')

    # Violin plot with swarm
    sns.violinplot(data=cat_data, x='category', y='value', ax=axes[1, 0], inner=None)
    sns.swarmplot(data=cat_data, x='category', y='value', ax=axes[1, 0],
                 color='white', edgecolor='gray', size=3)
    axes[1, 0].set_title('Violin Plot with Swarm')

    # Heatmap
    corr_matrix = corr_data.drop('category', axis=1).corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=axes[1, 1])
    axes[1, 1].set_title('Correlation Heatmap')

    # Pair plot (separate figure for this one)
    plt.figure(figsize=(10, 8))
    pair_plot = sns.pairplot(corr_data, hue='category', diag_kind='kde')
    pair_plot.fig.suptitle('Pair Plot with Categories', y=1.02)
    plt.savefig('seaborn_pairplot.png', dpi=150, bbox_inches='tight')

    plt.tight_layout()
    plt.savefig('seaborn_plots.png', dpi=150, bbox_inches='tight')
    plt.show()

    print("Seaborn plots saved as 'seaborn_plots.png' and 'seaborn_pairplot.png'")


def statistical_visualizations():
    """Demonstrate statistical data visualizations."""
    print("\n=== Statistical Visualizations ===")

    # Create sample statistical data
    np.random.seed(42)

    # Regression data
    x = np.linspace(0, 10, 50)
    y = 2*x + 1 + np.random.normal(0, 1, 50)
    reg_data = pd.DataFrame({'x': x, 'y': y})

    # Distribution comparison
    dist_data = pd.DataFrame({
        'value': np.concatenate([
            np.random.normal(0, 1, 200),
            np.random.normal(2, 1.5, 200),
            np.random.exponential(1, 200)
        ]),
        'distribution': ['Normal(0,1)']*200 + ['Normal(2,1.5)']*200 + ['Exponential(1)']*200
    })

    # Categorical comparison
    cat_stats = pd.DataFrame({
        'method': np.random.choice(['Method A', 'Method B', 'Method C'], 300),
        'score': np.random.randn(300),
        'group': np.random.choice(['Control', 'Treatment'], 300)
    })

    # Create figure
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Statistical Visualizations', fontsize=16)

    # Regression plot
    sns.regplot(data=reg_data, x='x', y='y', ax=axes[0, 0], scatter_kws={'alpha':0.6})
    axes[0, 0].set_title('Linear Regression with Confidence Interval')

    # Distribution comparison
    sns.histplot(data=dist_data, x='value', hue='distribution', ax=axes[0, 1],
                alpha=0.7, kde=True)
    axes[0, 1].set_title('Distribution Comparison')

    # Box plot comparison
    sns.boxplot(data=cat_stats, x='method', y='score', hue='group', ax=axes[0, 2])
    axes[0, 2].set_title('Method Comparison by Group')

    # Violin plot with statistics
    sns.violinplot(data=cat_stats, x='method', y='score', ax=axes[1, 0])
    sns.pointplot(data=cat_stats, x='method', y='score', ax=axes[1, 0],
                 color='red', markers='D', scale=0.7)
    axes[1, 0].set_title('Violin Plot with Mean Points')

    # Residual plot
    from sklearn.linear_model import LinearRegression
    X = reg_data[['x']]
    y_true = reg_data['y']
    model = LinearRegression().fit(X, y_true)
    y_pred = model.predict(X)
    residuals = y_true - y_pred

    axes[1, 1].scatter(y_pred, residuals, alpha=0.6)
    axes[1, 1].axhline(y=0, color='red', linestyle='--')
    axes[1, 1].set_xlabel('Predicted Values')
    axes[1, 1].set_ylabel('Residuals')
    axes[1, 1].set_title('Residual Plot')

    # Q-Q plot
    from scipy import stats
    stats.probplot(dist_data[dist_data['distribution'] == 'Normal(0,1)']['value'],
                  dist="norm", plot=axes[1, 2])
    axes[1, 2].set_title('Q-Q Plot (Normality Check)')

    plt.tight_layout()
    plt.savefig('statistical_visualizations.png', dpi=150, bbox_inches='tight')
    plt.show()

    print("Statistical visualizations saved as 'statistical_visualizations.png'")


def interactive_plots():
    """Demonstrate interactive plotting capabilities."""
    print("\n=== Interactive Plots (Static Version) ===")

    # Note: For truly interactive plots, you would need to run this in a Jupyter notebook
    # or use a web-based interface. Here we create enhanced static plots.

    np.random.seed(42)

    # Create interactive-style data
    x = np.linspace(0, 4*np.pi, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)

    # Create figure with multiple layers
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot multiple lines
    line1, = ax.plot(x, y1, 'b-', linewidth=2, label='sin(x)', picker=True)
    line2, = ax.plot(x, y2, 'r-', linewidth=2, label='cos(x)', picker=True)

    # Add annotations
    ax.annotate('Maximum', xy=(np.pi/2, 1), xytext=(np.pi/2 + 0.5, 0.8),
               arrowprops=dict(facecolor='black', shrink=0.05))
    ax.annotate('Minimum', xy=(3*np.pi/2, -1), xytext=(3*np.pi/2 - 1, -0.8),
               arrowprops=dict(facecolor='black', shrink=0.05))

    # Add grid and styling
    ax.grid(True, alpha=0.3)
    ax.set_title('Interactive-style Plot (Static Version)', fontsize=14)
    ax.set_xlabel('x values')
    ax.set_ylabel('y values')
    ax.legend()

    # Add text box with statistics
    stats_text = f"""
    Statistics:
    sin(x) range: [{y1.min():.2f}, {y1.max():.2f}]
    cos(x) range: [{y2.min():.2f}, {y2.max():.2f}]
    Period: 2π
    """

    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
           verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.tight_layout()
    plt.savefig('interactive_plot.png', dpi=150, bbox_inches='tight')
    plt.show()

    print("Interactive-style plot saved as 'interactive_plot.png'")
    print("Note: For truly interactive plots, use Jupyter notebook with %matplotlib widget")


def custom_styling():
    """Demonstrate custom styling and theming."""
    print("\n=== Custom Styling and Theming ===")

    # Create sample data
    x = np.linspace(0, 10, 50)
    y = np.sin(x) * np.exp(-x/10)

    # Test different styles
    styles = ['default', 'classic', 'ggplot', 'seaborn', 'fivethirtyeight']

    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.flatten()

    for i, style in enumerate(styles):
        with plt.style.context(style):
            axes[i].plot(x, y, 'o-', markersize=4, linewidth=2, color='darkblue')
            axes[i].set_title(f'Style: {style}')
            axes[i].grid(True, alpha=0.3)

    # Custom style example
    plt.style.use('default')

    # Create custom style
    custom_style = {
        'figure.figsize': (10, 6),
        'axes.labelsize': 12,
        'axes.titlesize': 14,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'axes.grid': True,
        'grid.alpha': 0.3,
        'axes.facecolor': '#f8f9fa',
        'figure.facecolor': 'white'
    }

    plt.rcParams.update(custom_style)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, y, 'o-', markersize=6, linewidth=3, color='#2E86AB',
           markerfacecolor='#A23B72', markeredgecolor='white', markeredgewidth=2)
    ax.fill_between(x, y, alpha=0.3, color='#F18F01')
    ax.set_title('Custom Styled Plot', fontsize=16, fontweight='bold')
    ax.set_xlabel('X Values', fontsize=12)
    ax.set_ylabel('Y Values', fontsize=12)

    plt.tight_layout()
    plt.savefig('custom_styling.png', dpi=150, bbox_inches='tight')
    plt.show()

    print("Custom styling examples saved as 'custom_styling.png'")


def main():
    """Run all data visualization examples."""
    print("Python Data Visualization Examples")
    print("=" * 50)
    print()

    try:
        basic_matplotlib_plots()
        advanced_matplotlib_plots()
        seaborn_visualizations()
        statistical_visualizations()
        interactive_plots()
        custom_styling()

        print("\n" + "=" * 50)
        print("All visualizations completed successfully!")
        print("Generated files:")
        print("- matplotlib_basic_plots.png")
        print("- matplotlib_advanced_plots.png")
        print("- seaborn_plots.png")
        print("- seaborn_pairplot.png")
        print("- statistical_visualizations.png")
        print("- interactive_plot.png")
        print("- custom_styling.png")

    except ImportError as e:
        print(f"Import error: {e}")
        print("Please install required packages:")
        print("pip install matplotlib seaborn pandas numpy scikit-learn")
    except Exception as e:
        print(f"Error running visualizations: {e}")


if __name__ == "__main__":
    main()
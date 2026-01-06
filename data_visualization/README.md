# Data Visualization Examples

This directory contains comprehensive examples of data visualization in Python using matplotlib and seaborn.

## Files

- `matplotlib_seaborn.py` - Complete data visualization tutorial covering matplotlib and seaborn

## Prerequisites

```bash
pip install matplotlib>=3.5.0
pip install seaborn>=0.11.0
pip install pandas>=1.5.0
pip install numpy>=1.21.0
pip install scikit-learn>=1.0.0  # For statistical examples
```

## Topics Covered

### matplotlib_seaborn.py

#### Basic Matplotlib Plots
- Line plots with multiple series
- Scatter plots with color mapping
- Bar charts with value labels
- Histograms with customization

#### Advanced Matplotlib Features
- 3D surface plots
- Pie/donut charts
- Box plots and violin plots
- Subplot arrangements

#### Seaborn Visualizations
- Time series plots with confidence intervals
- Categorical scatter plots
- Statistical distribution plots
- Correlation heatmaps
- Pair plots with categorical coloring

#### Statistical Visualizations
- Linear regression plots
- Distribution comparisons
- Method comparison charts
- Residual analysis
- Q-Q plots for normality testing

#### Interactive-style Plots
- Enhanced static plots with annotations
- Statistical overlays
- Custom styling for interactive feel

#### Custom Styling and Theming
- Built-in matplotlib styles
- Custom style dictionaries
- Color schemes and themes
- Professional plot styling

## Running the Examples

```bash
python data_visualization/matplotlib_seaborn.py
```

This will generate several PNG files demonstrating different visualization techniques:
- `matplotlib_basic_plots.png` - Basic plotting functions
- `matplotlib_advanced_plots.png` - Advanced chart types
- `seaborn_plots.png` - Seaborn statistical plots
- `seaborn_pairplot.png` - Pairwise relationships
- `statistical_visualizations.png` - Statistical analysis plots
- `interactive_plot.png` - Enhanced interactive-style plots
- `custom_styling.png` - Custom styled visualizations

## Key Concepts

- **Figure and Axes**: Understanding matplotlib's object hierarchy
- **Styling**: Colors, markers, line styles, and themes
- **Statistical Plotting**: Seaborn's high-level statistical interfaces
- **Customization**: Fine-tuning plots for publication quality
- **Best Practices**: Clear labeling, appropriate color schemes, and effective data presentation

## Notes

- All examples include proper error handling and fallbacks
- Plots are saved as high-resolution PNG files
- Examples work in both interactive and non-interactive environments
- Code includes comprehensive comments explaining each visualization technique
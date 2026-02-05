# 🎯 Quick Start Guide - Interactive Plotting

## What's New? 🆕

The script now displays plots **interactively** in addition to saving them as PNG files!

## How It Works

When you run the script, each visualization will:
1. ✅ **Save** as a PNG file in the `output` folder
2. 🖼️ **Display** in an interactive window (you can zoom, pan, etc.)
3. ⏸️ **Wait** for you to close the window before showing the next plot

## Running the Script

### Method 1: Command Line
```bash
python sales_analysis_windows.py
```

### Method 2: VS Code
1. Open `sales_analysis_windows.py`
2. Press `F5` or click the Run button
3. Watch as each plot appears one by one!

## Interactive Features

When a plot window opens, you'll see a toolbar with these buttons:

| Button | Function |
|--------|----------|
| 🏠 Home | Reset to original view |
| ⬅️ Back | Go to previous view |
| ➡️ Forward | Go to next view |
| ↔️ Pan | Click and drag to move around |
| 🔍 Zoom | Click and drag to zoom into an area |
| 🔧 Configure | Adjust subplot spacing |
| 💾 Save | Save the current view |

## Workflow

1. **Run the script** - It will generate data and create visualizations
2. **First plot appears** - Sales Overview Dashboard
   - Examine the plot
   - Use zoom/pan if needed
   - Close the window when done (click X or press Q)
3. **Second plot appears** - Product Analysis
   - Review the analysis
   - Close when done
4. **Continue** - Process repeats for all 5 plots:
   - Sales Overview Dashboard
   - Product Analysis
   - Salesman Analysis
   - Area Analysis
   - Comprehensive Report
5. **CSV files created** - After all plots are closed, CSV files are generated
6. **Done!** - All files saved in the `output` folder

## Tips & Tricks

### Tip 1: Save Custom Views
- Zoom in on interesting data
- Click the 💾 save button
- Choose a filename to save that specific view

### Tip 2: Quick Close
- Press `Q` to quickly close the current plot window
- Or click the X button in the corner

### Tip 3: Skip Interactive Mode
If you want to run without interactive windows (just save files):

**Option A:** Comment out `plt.show()` lines:
```python
# plt.show()  # Commented out
```

**Option B:** Use Matplotlib's non-interactive backend:
Add this at the top of the script:
```python
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
```

### Tip 4: Keep Windows Open
To view all plots at once without closing, change to:
```python
plt.show(block=False)  # Don't wait for window close
```
Then add at the end of main():
```python
plt.show()  # Keep all windows open
```

## Keyboard Shortcuts (in Plot Window)

| Key | Action |
|-----|--------|
| `Q` | Close the current plot |
| `F` | Toggle fullscreen |
| `G` | Toggle grid |
| `L` | Toggle axis log scale |
| `K` | Toggle x-axis log scale |
| `S` | Save figure dialog |
| `Home` | Reset view |
| `P` | Pan mode |
| `O` | Zoom mode |

## Display Settings

### Adjust Figure Size
In each function, modify:
```python
fig = plt.figure(figsize=(16, 10))  # Width, Height in inches
```

### Adjust DPI (Resolution)
```python
plt.savefig(output_path, dpi=300)  # Higher = better quality, larger file
# Options: 72 (screen), 150 (good), 300 (print quality), 600 (publication)
```

### Adjust Window Position
Add after `fig = plt.figure()`:
```python
manager = plt.get_current_fig_manager()
manager.window.wm_geometry("+100+100")  # Position at x=100, y=100
```

## Troubleshooting

### Issue: Plots appear behind VS Code window
**Solution:** 
```python
# Add after creating figure
fig.canvas.manager.window.attributes('-topmost', True)
```

### Issue: Plots are too small/large
**Solution:** Adjust figsize:
```python
fig = plt.figure(figsize=(20, 12))  # Make larger
```

### Issue: Want to auto-close plots after X seconds
**Solution:** Add timer:
```python
plt.show(block=False)
plt.pause(5)  # Display for 5 seconds
plt.close()
```

### Issue: Memory warning with multiple plots
**Solution:** Script already uses `plt.close()` after each plot, which frees memory.

## Advanced: Batch Processing

If processing multiple months of data:

```python
# At the top of the script
import matplotlib
matplotlib.use('Agg')  # Skip interactive display

# Run multiple times
for month in ['January', 'February', 'March']:
    MONTH = month
    main()
```

## Output Files

After running, you'll have:

### PNG Files (High Resolution - 300 DPI)
- `sales_overview_dashboard.png` - Main dashboard
- `product_analysis.png` - Product details
- `salesman_analysis.png` - Sales team performance
- `area_analysis.png` - Geographic analysis
- `comprehensive_sales_report.png` - Complete report

### CSV Files (Data)
- `product_sales.csv` - Product metrics
- `area_sales.csv` - Area metrics
- `salesman_sales.csv` - Detailed salesman data
- `sales_summary.csv` - Executive summary

## Best Practices

1. ✅ **Review each plot** before closing to catch any issues
2. ✅ **Save custom views** if you zoom into important details
3. ✅ **Keep the terminal/console open** to see progress messages
4. ✅ **Check the output folder** to confirm all files were created
5. ✅ **Use version control** if making custom modifications

## Example Session

```
D:\salesman> python sales_analysis_windows.py

======================================================================
JANUARY SALES ANALYSIS - DATA GENERATION & VISUALIZATION
======================================================================

📊 Generating sales data...
✓ Data generation complete

🎨 Creating visualizations...
----------------------------------------------------------------------
✓ Overview Dashboard created: D:\salesman\output\sales_overview_dashboard.png
[Interactive window opens - review and close]

✓ Product Analysis created: D:\salesman\output\product_analysis.png
[Interactive window opens - review and close]

✓ Salesman Analysis created: D:\salesman\output\salesman_analysis.png
[Interactive window opens - review and close]

✓ Area Analysis created: D:\salesman\output\area_analysis.png
[Interactive window opens - review and close]

✓ Comprehensive Report created: D:\salesman\output\comprehensive_sales_report.png
[Interactive window opens - review and close]
----------------------------------------------------------------------

💾 Exporting data to CSV...
✓ CSV files exported to output folder
======================================================================
ANALYSIS COMPLETE!
======================================================================
```

## Enjoy Your Interactive Sales Analysis! 📊📈

Now you can explore your data visually before it's saved! 🎉

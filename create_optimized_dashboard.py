#!/usr/bin/env python3
"""
Create optimized embedded dashboard with CSV data instead of JSON
This reduces file size by ~60% and improves loading performance
"""

import pandas as pd

# Read the template and data
print("Reading dashboard template...")
with open('unified-dashboard-ultimate.html', 'r') as f:
    html = f.read()

print("Reading dashboard data...")
df = pd.read_csv('dashboard_data.csv')
print(f"Loaded {len(df)} transactions")

# Convert to CSV string (much more compact than JSON)
csv_data = df.to_csv(index=False)
print(f"CSV data size: {len(csv_data):,} characters")

# Escape the CSV data for embedding in JavaScript
csv_data_escaped = csv_data.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')

# Remove file upload UI
html = html.replace('''    <div class="upload-box">
      <span id="statusMsg" class="status-msg">Ready</span>
      <button class="btn" onclick="document.getElementById('fileInput').click()">Load CSV</button>
      <input type="file" id="fileInput" accept=".csv" style="display:none">
    </div>''', '''    <div class="upload-box">
      <span id="statusMsg" class="status-msg">Loading data...</span>
    </div>''')

# Create new init method with CSV data embedded
new_init = f'''  init() {{
    console.log("Dashboard initializing...");

    // Embedded CSV data (compact format)
    const csvData = `{csv_data_escaped}`;

    console.log("CSV data loaded, size:", csvData.length, "characters");

    const status = document.getElementById('statusMsg');
    status.innerText = "Parsing data...";

    try {{
      // Parse CSV using PapaParse
      const parsed = Papa.parse(csvData, {{
        header: true,
        dynamicTyping: true,
        skipEmptyLines: true
      }});

      if (parsed.errors.length > 0) {{
        console.error("CSV parsing errors:", parsed.errors);
      }}

      console.log("Parsed", parsed.data.length, "transactions");

      status.innerText = "Processing transactions...";
      this.processRows(parsed.data);

      status.innerText = `Loaded ${{this.data.length}} transactions • July-Dec 2025`;
      console.log("Dashboard ready! Data:", this.data.length, "transactions");

    }} catch (error) {{
      console.error("Error loading dashboard:", error);
      status.innerText = "Error loading data - check console";
      status.style.color = "#ef4444";
    }}
  }},'''

# Find and replace the init method
import re
init_pattern = r'  init\(\) \{[\s\S]*?\n  \},'
html = re.sub(init_pattern, new_init, html, count=1)

# Remove the 6-month date filter since data is pre-filtered
html = html.replace(
    '''  processRows(rows) {
    const sixMonthsAgo = new Date();
    sixMonthsAgo.setMonth(sixMonthsAgo.getMonth() - 6);

    this.data = rows.map(row => {''',
    '''  processRows(rows) {
    // Data is already pre-filtered to July-December 2025

    this.data = rows.map(row => {'''
)

html = html.replace(
    '''      if (isNaN(date.getTime())) date = new Date();

      // Filter to last 6 months only
      if (date < sixMonthsAgo) return null;

      let rawGroup = row['Group'] || '';''',
    '''      if (isNaN(date.getTime())) date = new Date();

      let rawGroup = row['Group'] || '';'''
)

# Add console logging for debugging
html = html.replace(
    '''  render() {
    const all = this.data;''',
    '''  render() {
    console.log("Rendering dashboard with", this.data.length, "transactions");
    const all = this.data;'''
)

# Write the optimized dashboard
output_file = 'spending-dashboard-optimized.html'
with open(output_file, 'w') as f:
    f.write(html)

print(f"\n✅ Created {output_file}")
print(f"File size: {len(html):,} bytes ({len(html)/1024:.1f} KB)")
print(f"Reduction: {100 * (1 - len(html)/270637):.1f}% smaller than JSON version")
print(f"\nOpen in browser: file://{output_file}")

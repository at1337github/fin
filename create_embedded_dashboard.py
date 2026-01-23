#!/usr/bin/env python3
"""
Create dashboard with embedded data - no file upload needed
"""

import pandas as pd
import json

# Read CSV data
df = pd.read_csv('dashboard_data.csv')

# Convert to list of dicts for JavaScript
data_array = df.to_dict('records')

# Convert to JavaScript array string
js_data = json.dumps(data_array, indent=2)

# Read the template HTML
with open('unified-dashboard-ultimate.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find and replace the init() method to load data directly instead of file upload
# Remove file upload UI and replace with auto-load

# First, let's remove the upload box HTML
html = html.replace('''<div class="upload-box">
      <input type="file" id="fileInput" accept=".csv" style="display:none" />
      <button class="btn" onclick="document.getElementById('fileInput').click()">Choose CSV File</button>
      <span class="status-msg" id="statusMsg">No file loaded</span>
    </div>''',
    '<span class="status-msg" id="statusMsg">Loading data...</span>')

# Now replace the init() and parseData() methods with direct data loading
old_init = '''  init() {
    document.getElementById('fileInput').addEventListener('change', (e) => {
      const file = e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = (event) => this.parseData(event.target.result);
      reader.readAsText(file);
    });
  },

  parseData(csvText) {
    const status = document.getElementById('statusMsg');
    status.innerText = "Processing...";

    const lines = csvText.split(/\\r\\n|\\n/);
    let startIndex = 0;
    for (let i = 0; i < Math.min(lines.length, 20); i++) {
      if (lines[i].toLowerCase().includes('date') &&
         (lines[i].toLowerCase().includes('amount') || lines[i].toLowerCase().includes('description'))) {
        startIndex = i;
        break;
      }
    }
    const cleanCSV = lines.slice(startIndex).join('\\n');

    Papa.parse(cleanCSV, {
      header: true,
      skipEmptyLines: true,
      complete: (res) => {
        if (res.data.length === 0) {
          status.innerText = "Error: No data";
          return;
        }
        this.processRows(res.data);
        status.innerText = `Loaded ${this.data.length} transactions`;
      }
    });
  },'''

# New version that loads embedded data directly
new_init = f'''  init() {{
    // Embedded data - no file upload needed
    const embeddedData = {js_data};

    const status = document.getElementById('statusMsg');
    status.innerText = "Loading...";

    this.processRows(embeddedData);
    status.innerText = `Loaded ${{this.data.length}} transactions • July-Dec 2025`;
  }},'''

html = html.replace(old_init, new_init)

# Write the new HTML
output_file = 'spending-dashboard.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("="*60)
print("✅ DASHBOARD CREATED WITH EMBEDDED DATA")
print("="*60)
print(f"\\nFile: {output_file}")
print(f"Transactions: {len(df)}")
print(f"Total Amount: ${abs(df['Amount'].sum()):,.2f}")
print(f"\\n✓ No file upload needed")
print(f"✓ Data embedded directly")
print(f"✓ Works offline")
print(f"✓ Mobile Safari compatible")
print(f"\\nJust open: {output_file}")
print("="*60)

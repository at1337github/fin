# Archive Directory

This directory contains historical versions of files that have been superseded by newer versions. Files are automatically archived when updated versions are created.

## Directory Structure

### `old_scripts/`
Previous versions of Python scripts that have been updated or replaced:
- `create_complete_audit.py` - Initial full audit creation
- `create_corrected_audit.py` - Corrected audit with CLEO AI/Insurance fixes
- `create_final_audit.py` - Final audit before July-Dec filtering
- `create_dashboard.py` - First dashboard attempt
- `create_dashboard_fixed.py` - Dashboard fix attempt
- `enhanced_categorization.py` - Initial categorization improvements

**Current scripts:** See root directory for latest versions

### `old_docs/`
Previous documentation that has been consolidated or superseded:
- `ANALYSIS_REPORT.txt` - Initial analysis findings
- `COMPLETE_AUDIT_SUMMARY.md` - Full year audit summary
- `CORRECTED_AUDIT_SUMMARY.md` - Post-correction summary
- `FINAL_SUMMARY.md` - Final audit summary
- `FINDINGS.md` - Initial findings document
- `DASHBOARD_README.md` - Old dashboard documentation
- `HOW_TO_VIEW_DASHBOARD.md` - Old viewing instructions

**Current docs:**
- `README.md` - Main project documentation
- `SPENDING_DASHBOARD_GUIDE.md` - Current dashboard guide
- `DASHBOARD_INSTRUCTIONS.md` - Dashboard instructions
- `AUDIT_CLEANING_LOGIC.md` - Audit methodology

### `old_data/`
Previous versions of audit and data files:
- `Complete_Audit_PayPal_CashApp.csv` - Full year audit (all transactions)
- `Complete_Audit_Enhanced.csv` - Enhanced categorization version
- `Corrected_Audit_Post_June_2025.csv` - Post-June with corrections
- `Final_Audit_PayPal_CashApp.csv` - Final version before date filtering
- `business_paypal-6.CSV` - Empty file (replaced by Download-6.CSV)

**Current data:**
- `July_December_2025_Audit.csv` - Current audit (July-Dec 2025)
- `dashboard_data.csv` - Formatted dashboard data
- `PayPal_True_Spend_Audit.csv` - Original PayPal audit
- Source files: `personal-6.CSV`, `Download-6.CSV`, `cash_app_report_*.csv`

### `old_dashboards/`
Previous dashboard versions:
- `Dashboard.html` - First dashboard attempt (iframe-based, 40KB)

**Current dashboards:**
- `spending-dashboard.html` - Self-contained with embedded data (265KB)
- `unified-dashboard-ultimate.html` - Template for dashboard generation

### `output_logs/`
Execution logs from various scripts:
- `analysis_output.txt` - PayPal analysis results
- `complete_audit_output.txt` - Full audit creation log
- `corrected_audit_output.txt` - Correction audit log
- `enhanced_categorization_output.txt` - Categorization improvement log
- `final_audit_output.txt` - Final audit log
- `july_dec_audit_output.txt` - July-Dec filtering log

## Retention Policy

Files are archived rather than deleted to maintain project history and allow for:
- Audit trails of data transformations
- Comparison with previous versions
- Recovery if needed
- Documentation of project evolution

## Automatic Archiving

Use the `archive_old_versions.sh` script in the root directory to automatically archive old files when creating new versions. The script:
1. Detects files with version indicators or timestamps
2. Moves older versions to appropriate archive subdirectories
3. Updates git with changes
4. Maintains clean working directory

---

*Last updated: 2026-01-23*

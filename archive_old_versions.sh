#!/bin/bash

# Automatic File Archiving Script
# Moves old file versions to organized archive directories
# Usage: ./archive_old_versions.sh [--dry-run]

set -e

ARCHIVE_DIR="archive"
DRY_RUN=false

# Parse arguments
if [[ "$1" == "--dry-run" ]]; then
    DRY_RUN=true
    echo "🔍 DRY RUN MODE - No files will be moved"
    echo
fi

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Ensure archive directories exist
mkdir -p "$ARCHIVE_DIR/old_scripts"
mkdir -p "$ARCHIVE_DIR/old_docs"
mkdir -p "$ARCHIVE_DIR/old_data"
mkdir -p "$ARCHIVE_DIR/old_dashboards"
mkdir -p "$ARCHIVE_DIR/output_logs"

echo -e "${BLUE}📦 Automatic File Archiving${NC}"
echo "=================================="
echo

# Function to archive a file
archive_file() {
    local file=$1
    local dest_dir=$2
    local reason=$3

    if [[ ! -f "$file" ]]; then
        return
    fi

    echo -e "${YELLOW}📄 Found:${NC} $file"
    echo -e "   ${GREEN}→${NC} $dest_dir/"
    echo -e "   Reason: $reason"

    if [[ "$DRY_RUN" == false ]]; then
        mv "$file" "$dest_dir/"
        git add "$file" "$dest_dir/" 2>/dev/null || true
    fi

    echo
}

# Archive old Python scripts
echo -e "${BLUE}=== Checking for Old Scripts ===${NC}"
archive_file "create_complete_audit_old.py" "$ARCHIVE_DIR/old_scripts" "Superseded by newer version"
archive_file "create_audit_v1.py" "$ARCHIVE_DIR/old_scripts" "Old version"
archive_file "create_audit_v2.py" "$ARCHIVE_DIR/old_scripts" "Old version"
archive_file "dashboard_v1.py" "$ARCHIVE_DIR/old_scripts" "Old dashboard version"
archive_file "test_*.py" "$ARCHIVE_DIR/old_scripts" "Test/development scripts"

# Archive old documentation
echo -e "${BLUE}=== Checking for Old Documentation ===${NC}"
archive_file "*_OLD.md" "$ARCHIVE_DIR/old_docs" "Marked as old"
archive_file "*_BACKUP.md" "$ARCHIVE_DIR/old_docs" "Backup file"
archive_file "README_old.md" "$ARCHIVE_DIR/old_docs" "Old README version"
archive_file "NOTES.txt" "$ARCHIVE_DIR/old_docs" "Development notes"

# Archive old data files
echo -e "${BLUE}=== Checking for Old Data ===${NC}"
archive_file "*_backup.csv" "$ARCHIVE_DIR/old_data" "Backup file"
archive_file "*_old.csv" "$ARCHIVE_DIR/old_data" "Marked as old"
archive_file "*_temp.csv" "$ARCHIVE_DIR/old_data" "Temporary file"
archive_file "Complete_Audit_*.csv" "$ARCHIVE_DIR/old_data" "Old complete audit (if exists)"

# Archive old dashboards
echo -e "${BLUE}=== Checking for Old Dashboards ===${NC}"
archive_file "dashboard_v*.html" "$ARCHIVE_DIR/old_dashboards" "Old dashboard version"
archive_file "*_dashboard_old.html" "$ARCHIVE_DIR/old_dashboards" "Old dashboard"

# Archive output logs (anything matching *_output.txt or *.log)
echo -e "${BLUE}=== Checking for Output Logs ===${NC}"
for file in *_output.txt; do
    if [[ -f "$file" ]]; then
        archive_file "$file" "$ARCHIVE_DIR/output_logs" "Script output log"
    fi
done

for file in *.log; do
    if [[ -f "$file" && "$file" != ".log" ]]; then
        archive_file "$file" "$ARCHIVE_DIR/output_logs" "Log file"
    fi
done

# Summary
echo -e "${GREEN}✅ Archive scan complete${NC}"
echo

if [[ "$DRY_RUN" == true ]]; then
    echo -e "${YELLOW}To actually move files, run: ./archive_old_versions.sh${NC}"
else
    echo -e "${GREEN}Files have been archived.${NC}"
    echo -e "Run ${BLUE}git status${NC} to see changes"
    echo -e "Run ${BLUE}git commit -m 'Archive old versions'${NC} to commit"
fi

echo
echo "📁 Archive structure:"
echo "  archive/"
echo "  ├── old_scripts/    - Previous Python scripts"
echo "  ├── old_docs/       - Superseded documentation"
echo "  ├── old_data/       - Historical data files"
echo "  ├── old_dashboards/ - Old dashboard versions"
echo "  └── output_logs/    - Execution logs"

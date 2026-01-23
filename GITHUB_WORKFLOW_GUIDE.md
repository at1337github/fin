# GitHub Workflow Guide

Complete guide for managing branches, syncing with GitHub Desktop, and using automatic archiving.

---

## 📋 Table of Contents

1. [Making claude/enhance-docs-review-u03EV the Default Branch](#making-the-branch-default)
2. [Syncing with GitHub Desktop](#syncing-with-github-desktop)
3. [Automatic Archiving](#automatic-archiving)
4. [Branch Cleanup](#branch-cleanup)
5. [Daily Workflow](#daily-workflow)

---

## 🌿 Making the Branch Default

### Current Status
- **Active Branch:** `claude/enhance-docs-review-u03EV` (fully organized, clean, with embedded dashboard)
- **Main Branch:** `main` (behind by 3 commits)
- **Old Branch:** `at1337github-patch-sample_dash` (can be deleted)

### Option 1: Make claude/enhance-docs-review-u03EV the Default (Recommended)

**On GitHub.com:**

1. Go to your repository: `https://github.com/at1337github/fin`

2. Click **Settings** (top right, need admin access)

3. In the left sidebar, click **Branches**

4. Under "Default branch", click the ⇄ switch icon

5. Select `claude/enhance-docs-review-u03EV` from the dropdown

6. Click **Update**

7. Confirm the change

**Result:** Your organized branch becomes the default. New clones and PRs will use this branch.

### Option 2: Merge to Main via Pull Request

**On GitHub.com:**

1. Go to **Pull Requests** tab

2. Click **New Pull Request**

3. Set:
   - Base: `main`
   - Compare: `claude/enhance-docs-review-u03EV`

4. Click **Create Pull Request**

5. Title: "Final: Clean organized repository with embedded dashboard"

6. Click **Merge Pull Request** → **Confirm merge**

7. Optional: Delete `claude/enhance-docs-review-u03EV` after merge (or keep it)

**Result:** Main branch gets all the organized changes.

### Option 3: Force Main to Match claude/enhance-docs-review-u03EV (Advanced)

**Warning:** This rewrites main branch history. Only do if you're the sole contributor.

```bash
# Backup main first
git branch main-backup main

# Force main to match claude/enhance-docs-review-u03EV
git checkout main
git reset --hard claude/enhance-docs-review-u03EV

# Force push (requires force permission)
# Note: This may be blocked by branch protection
git push origin main --force
```

**My Recommendation:** Use **Option 1** (make it the default branch). This is safest and doesn't require force pushing.

---

## 💻 Syncing with GitHub Desktop

### Initial Setup

1. **Open GitHub Desktop**

2. **Add Repository:**
   - File → Add Local Repository
   - Choose: `/path/to/fin`
   - Or: Clone from GitHub (at1337github/fin)

3. **Select Branch:**
   - Click current branch dropdown (top)
   - Select `claude/enhance-docs-review-u03EV`
   - Or select `main` if you made it the default

### Daily Workflow - Keeping Local Files Updated

#### **Fetch Latest Changes** (Check what's new)

1. Click **Fetch origin** button (top right)
   - Downloads info about new commits
   - Doesn't change your files yet

2. If there are new commits, you'll see "Pull X commits from origin"

#### **Pull Changes** (Update your local files)

1. Click **Pull origin** button
   - Downloads and applies new commits
   - Updates your local files to match GitHub

2. Your local files are now in sync!

#### **Push Changes** (Upload your local commits)

1. Make changes to files

2. GitHub Desktop shows changed files in left panel

3. Write commit message (bottom left):
   - Summary: Short description
   - Description: Optional details

4. Click **Commit to [branch]**

5. Click **Push origin** (top right)

### Automatic Sync Schedule

**Best Practices:**

- **Start of work:** Fetch + Pull (get latest changes)
- **After making changes:** Commit + Push (upload your work)
- **End of day:** Fetch + Pull (check for updates)
- **Before important work:** Always fetch first

**GitHub Desktop Preferences:**

- **Enable automatic fetch:**
  - Preferences → Git
  - Check "Periodically fetch from remote"
  - Set interval (e.g., every 5 minutes)

### Handling Conflicts

If you see "Resolve conflicts before continuing":

1. GitHub Desktop will open conflicted files

2. Look for conflict markers:
   ```
   <<<<<<< HEAD
   Your changes
   =======
   Their changes
   >>>>>>> branch-name
   ```

3. Edit file to keep desired changes

4. Remove conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)

5. Save file

6. In GitHub Desktop, mark as resolved

7. Complete merge/commit

---

## 🗄️ Automatic Archiving

### How It Works

The repository now has `archive_old_versions.sh` script that automatically moves old files to organized archive directories.

### Archive Structure

```
archive/
├── old_scripts/     - Previous Python script versions
├── old_docs/        - Superseded documentation
├── old_data/        - Historical data files
├── old_dashboards/  - Old dashboard versions
└── output_logs/     - Script execution logs
```

### Manual Archiving

**Dry run (preview what will be archived):**
```bash
./archive_old_versions.sh --dry-run
```

**Actually archive files:**
```bash
./archive_old_versions.sh
```

**Commit archived files:**
```bash
git commit -m "Archive old file versions"
git push origin [your-branch]
```

### What Gets Archived

The script looks for:

- **Old scripts:** `*_old.py`, `*_v1.py`, `*_backup.py`, `test_*.py`
- **Old docs:** `*_OLD.md`, `*_BACKUP.md`, `README_old.md`, `NOTES.txt`
- **Old data:** `*_backup.csv`, `*_old.csv`, `*_temp.csv`
- **Old dashboards:** `dashboard_v*.html`, `*_old.html`
- **Logs:** `*_output.txt`, `*.log`

### Automatic Archiving (Optional)

**Enable automatic archiving before every commit:**

```bash
# 1. Copy the example hook
cp .git/hooks/pre-commit-archive-example .git/hooks/pre-commit

# 2. Make it executable
chmod +x .git/hooks/pre-commit

# 3. Edit to enable archiving
nano .git/hooks/pre-commit

# 4. Uncomment the archiving line:
./archive_old_versions.sh
```

Now, every time you commit, old files are automatically archived!

**Disable automatic archiving:**
```bash
rm .git/hooks/pre-commit
```

### Manual File Archiving Rules

When creating new versions of files, follow this naming pattern to trigger automatic archiving:

**Scripts:**
- Old: `create_audit.py` → Rename to `create_audit_old.py`
- New: `create_audit_v2.py` or `create_audit.py` (same name)

**Data:**
- Old: `Audit.csv` → Rename to `Audit_backup.csv` or `Audit_old.csv`
- New: `Audit.csv` (same name) or `Audit_2025.csv` (new name)

**Documentation:**
- Old: `README.md` → Rename to `README_OLD.md`
- New: `README.md` (same name, updated content)

Then run `./archive_old_versions.sh` to move old versions to archive.

---

## 🧹 Branch Cleanup

### Current Branches

```bash
# List all branches
git branch -a
```

Output:
- `main` - Main branch
- `claude/enhance-docs-review-u03EV` - Clean organized branch ✅
- `at1337github-patch-sample_dash` - Old sample dashboard branch ❌

### Delete Local Branch

```bash
git branch -d at1337github-patch-sample_dash
```

### Delete Remote Branch

**On GitHub.com:**

1. Go to repository

2. Click **Branches** (near top, shows branch count)

3. Find `at1337github-patch-sample_dash`

4. Click trash can icon 🗑️

5. Confirm deletion

**Or via command line:**
```bash
git push origin --delete at1337github-patch-sample_dash
```

### Recommended Branch Structure

After cleanup, you should have:

1. **main** (or make `claude/enhance-docs-review-u03EV` the default)
2. **claude/enhance-docs-review-u03EV** (keep for reference, or delete after merging)

---

## 📆 Daily Workflow

### Morning Routine

```bash
# 1. Start GitHub Desktop
# 2. Fetch latest changes
#    Click "Fetch origin"

# 3. Pull if there are updates
#    Click "Pull origin"

# 4. Check current branch
#    Should be: claude/enhance-docs-review-u03EV or main

# 5. Ready to work!
```

### After Making Changes

```bash
# In GitHub Desktop:
# 1. Review changed files (left panel)
# 2. Write commit message
# 3. Click "Commit to [branch]"
# 4. Click "Push origin"

# Changes are now on GitHub!
```

### Before Ending Day

```bash
# 1. Commit any uncommitted changes
# 2. Push to GitHub
# 3. Fetch to see if anyone else made changes
# 4. Pull if needed
```

### Weekly Maintenance

```bash
# Run archiving script
./archive_old_versions.sh

# Review archived files
ls -lah archive/old_*

# Commit archive changes
git add archive/
git commit -m "Archive old file versions"
git push origin [your-branch]
```

---

## 🔧 Troubleshooting

### "Your branch is behind origin/[branch]"

**Solution:**
```bash
# In GitHub Desktop: Click "Pull origin"
# Or command line:
git pull origin [branch-name]
```

### "Conflict: merge conflict in [file]"

**Solution:**
1. Open file in editor
2. Find conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
3. Keep desired changes, remove markers
4. Save file
5. In GitHub Desktop: Mark as resolved
6. Commit merge

### "Can't push - branch protection"

**Solution:**
- Create a pull request instead of direct push
- Or ask repository admin to adjust protection rules

### "Untracked files" warning

**Solution:**
```bash
# See untracked files
git status

# Add specific files
git add [filename]

# Or add all
git add .

# Commit
git commit -m "Add files"
```

### Archive script not running

**Solution:**
```bash
# Make it executable
chmod +x archive_old_versions.sh

# Run it
./archive_old_versions.sh
```

---

## 📚 Quick Reference

### GitHub Desktop Actions

| Action | Button | When to Use |
|--------|--------|-------------|
| **Fetch** | Fetch origin | Check for updates (doesn't change files) |
| **Pull** | Pull origin | Download and apply updates |
| **Push** | Push origin | Upload your commits to GitHub |
| **Commit** | Commit to [branch] | Save changes with message |

### Command Line Equivalents

| GitHub Desktop | Command Line |
|----------------|--------------|
| Fetch origin | `git fetch origin` |
| Pull origin | `git pull origin [branch]` |
| Push origin | `git push origin [branch]` |
| Switch branch | `git checkout [branch]` |
| View changes | `git status` or `git diff` |

### File Organization

| Location | Purpose | Auto-Archive |
|----------|---------|--------------|
| `/` (root) | Current/active files only | No |
| `/archive/old_scripts/` | Previous Python scripts | Yes |
| `/archive/old_docs/` | Old documentation | Yes |
| `/archive/old_data/` | Historical data files | Yes |
| `/archive/old_dashboards/` | Old HTML dashboards | Yes |
| `/archive/output_logs/` | Script execution logs | Yes |

---

## ✅ Recommended Next Steps

1. ✅ **Make branch default** (Option 1 above)
2. ✅ **Set up GitHub Desktop** with auto-fetch
3. ✅ **Test archiving script:** `./archive_old_versions.sh --dry-run`
4. ✅ **Delete old branch:** `at1337github-patch-sample_dash`
5. ✅ **Establish routine:** Fetch → Work → Commit → Push

---

## 📞 Need Help?

**Git Issues:**
- Check GitHub Desktop: Help → Show Logs
- Command line: `git status` for current state

**Archive Issues:**
- Dry run first: `./archive_old_versions.sh --dry-run`
- Check archive/README.md for structure

**Sync Issues:**
- Always fetch before pulling
- Always commit before switching branches
- Use `git status` to see current state

---

*Last updated: 2026-01-23*
*Branch: claude/enhance-docs-review-u03EV*

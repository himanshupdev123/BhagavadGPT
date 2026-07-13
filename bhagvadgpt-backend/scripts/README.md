# BhagavadGPT Backend - Utility Scripts

## Overview

This directory contains utility scripts for data migration, tag enhancement, and database management.

## Scripts

### OKF Migration & Enhancement

**`migrate_to_okf.py`**
- Migrates verses from ChromaDB to OKF (Open Knowledge Format)
- Creates markdown files in `bhagvadgpt_okf/` directory
- Extracts and populates YAML frontmatter (tags, related, metadata)
- **Status**: Completed - 700 verses migrated

**How to run:**
```bash
cd BhagavadGPT/bhagvadgpt-backend
python scripts/migrate_to_okf.py
```

**`enhance_okf_tags.py`**
- Enhances existing tags with user-query-aligned language
- Adds semantic variations (e.g., "anxiety" → "worried", "stressed")
- Finds and links related verses based on tag overlap
- **Status**: Completed - 676 verses enhanced

**How to run:**
```bash
python scripts/enhance_okf_tags.py
```

**`refine_tags_v2.py`**
- Version 2 of tag refinement script
- More advanced tag processing and categorization
- **Status**: Available for future refinement

**How to run:**
```bash
python scripts/refine_tags_v2.py
```

### Legacy Scripts

**`build_db.py`**
- Original ChromaDB database builder
- **Status**: Deprecated (OKF is now used instead)
- **Note**: Keep for reference only

## Usage Guidelines

### When to Use Each Script

**migrate_to_okf.py**: 
- Run once when migrating from ChromaDB to OKF
- Re-run if you need to reset OKF structure
- Backs up existing data before migration

**enhance_okf_tags.py**:
- Run after manual tagging updates
- Run to apply bulk tag enhancements
- Analyzes user queries to improve tag relevance

**refine_tags_v2.py**:
- Use for advanced tag refinement
- Experimental features and processing

## Important Notes

### Before Running Scripts

1. **Backup your data**: Scripts in `backups/` folder contain backup copies
2. **Check dependencies**: Ensure all required packages are installed
3. **Review configuration**: Check script parameters before running

### Script Safety

- All scripts that modify data create backups automatically
- Check the `backups/` directory for previous versions
- Scripts are idempotent (safe to run multiple times)

### Migration Status

Current system state:
- ✅ Migrated to OKF format (700 verses)
- ✅ Tags enhanced (676 verses with tags)
- ✅ Related field populated (297 verses with connections)
- ✅ ChromaDB deprecated

## Dependencies

All scripts require:
```bash
pip install -r requirements.txt
```

Key dependencies:
- `pyyaml` - YAML parsing
- `pathlib` - File operations
- `json` - Data processing

## Output

Scripts create/modify:
- `bhagvadgpt_okf/` - OKF markdown files
- `backups/` - Backup copies
- Console logs with progress and statistics

## Troubleshooting

**Issue**: "ModuleNotFoundError"
**Solution**: Install dependencies with `pip install -r requirements.txt`

**Issue**: "File not found"
**Solution**: Ensure you're running from the backend root directory

**Issue**: "Permission denied"
**Solution**: Check file permissions and close any files open in editors

## Documentation

For more details, see:
- `../docs/KNOWLEDGE_GRAPH_IMPLEMENTATION.md` - OKF implementation
- `../docs/OKF_RELATED_FIELD.md` - Related field feature
- `../docs/TOKEN_LIMIT_FIX.md` - Token management

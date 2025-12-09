# .skill File Format Specification

**Version**: 2.0
**Created**: 2025-11-01
**Purpose**: Define distributable skill package format

---

## Overview

**.skill files** are distributable packages containing complete Nexus-v3 skills. They use standard ZIP format with a `.skill` extension for easy sharing and installation.

---

## File Format

**Format**: ZIP archive
**Extension**: `.skill`
**Compression**: DEFLATE
**Naming**: `{skill-name}.skill` (must match folder name)

---

## Internal Structure

```
skill-name.skill (ZIP archive)
└── skill-name/
    ├── SKILL.md (required)
    ├── scripts/ (optional)
    │   └── *.py
    ├── references/ (optional)
    │   └── *.md
    └── assets/ (optional)
        └── *.*
```

**Required**:
- `SKILL.md` - Main skill file with V2.0 YAML format

**Optional**:
- `scripts/` - Executable code (Python scripts, shell scripts, etc.)
- `references/` - Documentation loaded on demand
- `assets/` - Templates or output files

---

## Creating .skill Files

### Using package-skill.py

```bash
python 00-system/scripts/package-skill.py 00-system/skills/skill-name
python 00-system/scripts/package-skill.py 00-system/skills/skill-name --output dist/
```

**Process**:
1. Validates skill (must pass V2.0 validation)
2. Creates ZIP archive
3. Adds SKILL.md
4. Adds scripts/, references/, assets/ (if they exist)
5. Names file `{skill-name}.skill`

---

## Installing .skill Files

### Manual Installation

```bash
# 1. Extract to Skills folder
unzip skill-name.skill -d 00-system/skills/

# 2. Validate
python 00-system/scripts/validate-skill.py 00-system/skills/skill-name

# 3. Test
# Say one of the trigger phrases from the skill description
```

### Installation Checklist

- [ ] Extract .skill file to `00-system/skills/`
- [ ] Run `validate-skill.py` on extracted skill
- [ ] Verify SKILL.md uses V2.0 format (name + description only)
- [ ] Test skill with trigger phrase
- [ ] Update `framework-map.md` if needed (add triggers to navigation)

---

## Validation

**.skill files must contain**:
- ✅ Valid V2.0 YAML format (name + description only)
- ✅ SKILL.md < 500 lines
- ✅ All referenced files present (scripts, references, assets)
- ✅ No forbidden YAML fields (skill_name, type, frequency, tags)

**Validation happens**:
- Before packaging (automatic)
- After installation (manual)

---

## Distribution

### Sharing Skills

1. **Package the skill**:
   ```bash
   python package-skill.py 00-system/skills/my-skill --output dist/
   ```

2. **Share the .skill file**:
   - Email attachment
   - File sharing service
   - GitHub releases
   - Internal repository

3. **Provide installation instructions**:
   - See "Installing .skill Files" section above
   - Include trigger phrases from description

### Best Practices

✅ **DO**:
- Validate before packaging
- Test installation in clean environment
- Document dependencies (if any)
- Include comprehensive description with triggers
- Keep skills under 500 lines (use references/)

❌ **DON'T**:
- Package invalid skills
- Include sensitive data
- Package without testing
- Forget to document trigger phrases

---

## Examples

### Package create-skill

```bash
cd Nexus-v3-template
python 00-system/scripts/package-skill.py 00-system/skills/create-skill --output dist/

# Output: dist/create-skill.skill (6.5 KB)
```

### Install create-skill

```bash
# Recipient extracts
unzip create-skill.skill -d 00-system/skills/

# Validate
python 00-system/scripts/validate-skill.py 00-system/skills/create-skill

# Test
# Say "create skill" or "new skill"
```

---

## Technical Specification

### ZIP Compression

- **Method**: DEFLATE
- **Compression Level**: Default (balance speed/size)
- **Archive Type**: Standard ZIP (compatible with all tools)

### File Paths

- **Root folder**: Must match skill name
- **SKILL.md**: Always at `{skill-name}/SKILL.md`
- **Resources**: Relative to skill root

### Compatibility

- **OS**: Windows, macOS, Linux (standard ZIP)
- **Python**: 3.7+ (for packaging/installation scripts)
- **Tools**: Any ZIP utility can extract

---

## FAQ

### Q: Can I package skills with dependencies?

**A**: Yes, but document them clearly in SKILL.md. The .skill file only packages the skill itself, not external dependencies.

---

### Q: What if my skill needs Python packages?

**A**: Document required packages in SKILL.md `## Notes` section. Users must install separately.

---

### Q: Can I update a packaged skill?

**A**: Yes, package the updated version with the same name. Users overwrite the old installation.

---

### Q: How do I verify .skill file integrity?

**A**: Extract and run `validate-skill.py`. It checks YAML format, size limits, and structure.

---

### Q: Can .skill files be nested?

**A**: No. One .skill file = one skill. Don't package multiple skills together.

---

## References

- **Packaging Script**: [package-skill.py](../scripts/package-skill.py)
- **Validation Script**: [validate-skill.py](../scripts/validate-skill.py)
- **YAML Quick Reference**: [yaml-quick-reference.md](yaml-quick-reference.md)
- **create-skill skill**: Use the create-skill skill for guided skill creation with best practices

---

**Version**: 2.0
**Last Updated**: 2025-11-01
**Status**: Official Specification

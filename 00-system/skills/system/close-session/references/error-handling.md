# close-session Error Handling

Common error scenarios and solutions for the close-session workflow.

---

## No Active Build

**Scenario**: 02-builds/build-map.md shows no current focus

**Action**:
- Skip build state reading (Step 2)
- Skip task completion review (Step 2.5)
- Continue with map updates (Step 3)
- Create general session report
- Display summary without build info

---

## tasks.md Missing

**Scenario**: Build folder exists but planning/tasks.md is missing

**Action**:
- Report in summary: "⚠️ Build {name} missing tasks.md"
- Suggest: "Run validate-system to check structure"
- Skip progress calculation for that build
- Continue with other builds

---

## Memory/ Files Corrupted

**Scenario**: 02-builds/build-map.md or other memory files unreadable

**Action**:
- Attempt to create from template
- Scan Builds/ and Skills/ to rebuild
- Report in summary: "⚠️ Rebuilt memory from scan"
- Suggest: "Run validate-system to verify integrity"

---

## Map Generation Fails

**Scenario**: Error during Builds/ or Skills/ scan

**Action**:
- Keep old maps (don't overwrite)
- Report error in summary
- Suggest: "Try again or run validate-system"
- Continue with session report and cleanup

---

## Max Session Reports (>30)

**Scenario**: Too many session reports accumulate

**Action**:
- Keep 30 most recent
- Delete oldest reports
- Note in summary: "Archived old session reports"

---

## Temp File User Doesn't Respond

**Scenario**: User doesn't answer about temp file

**Action**:
- Default to "skip" (leave in place)
- Note: "Left {filename} in place (no response)"
- Continue with next file

---

## Goals File Missing

**Scenario**: 01-memory/goals.md missing or empty

**Action**:
- Note in summary: "⚠️ System not initialized"
- Suggest: "Run 00-setup-memory build to initialize"
- Continue with map updates and session closure

---

## Timestamp Command Fails

**Scenario**: powershell command fails to get timestamp

**Action**:
- Fall back to Python: `python -c "import datetime; print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))"`
- If that fails: Use "YYYY-MM-DD HH:MM:SS" format manually
- Report in summary: "⚠️ Timestamp generation issue"

---

**END OF ERROR HANDLING**

"""
### Scenario 2: Hospital Nurse Rostering (24-Hour Cycle)

**Context:** You are assigning nurses to three 8-hour shifts (Shift 1, Shift 2, Shift 3) for a single day.

**The Rules:**

1. **Coverage:** Every shift must have at least 4 nurses on duty.
2. **Seniority:** Every shift must have **at least one** "Senior" level nurse present.
3. **Fatigue:** No nurse can work more than one shift in a single day (No double shifts allowed).
4. **Union Rule:** If Nurse A is assigned to Shift 3 (Night), they cannot work Shift 1 (Morning) the very next day. *(Note: This implies a multi-day model, but for a single day, just assume "If Shift 3 today, then forbidden from something else").*

"""

import pulp

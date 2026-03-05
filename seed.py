"""
Run once to pre-load the ingredient database with common pregnancy safety data.
Usage: python seed.py
"""
from database import init_db, add_ingredient

SEED_DATA = [
    # Safe
    ("ginger", "Safe", "Natural remedy for nausea, safe in food amounts"),
    ("folic acid", "Safe", "Essential for fetal neural tube development"),
    ("iron", "Safe", "Important mineral; take as directed"),
    ("vitamin c", "Safe", "Supports immune system; safe in normal doses"),
    ("vitamin d", "Safe", "Supports bone development"),
    ("calcium", "Safe", "Essential for fetal bone growth"),
    ("omega-3", "Safe", "Supports brain development; choose low-mercury sources"),
    ("pasteurized milk", "Safe", "Safe dairy product"),
    ("cooked chicken", "Safe", "Fully cooked poultry is safe"),
    ("cooked salmon", "Safe", "Low-mercury fish, good omega-3 source"),

    # Caution
    ("caffeine", "Caution", "Limit to under 200mg/day"),
    ("tuna", "Caution", "Limit to 2 servings/week due to mercury"),
    ("unpasteurized cheese", "Caution", "Risk of listeria; avoid soft cheeses"),
    ("deli meat", "Caution", "Risk of listeria unless heated until steaming"),
    ("vitamin a", "Caution", "High doses (retinol) can cause birth defects"),
    ("herbal tea", "Caution", "Many herbs are unstudied in pregnancy; check each"),
    ("licorice root", "Caution", "High amounts linked to premature birth"),

    # Unsafe
    ("alcohol", "Unsafe", "No safe amount during pregnancy"),
    ("raw eggs", "Unsafe", "Risk of salmonella"),
    ("raw fish", "Unsafe", "Risk of bacteria and parasites"),
    ("shark", "Unsafe", "Very high mercury content"),
    ("swordfish", "Unsafe", "Very high mercury content"),
    ("raw sprouts", "Unsafe", "Risk of E. coli and salmonella"),
    ("unpasteurized juice", "Unsafe", "Risk of harmful bacteria"),
]


if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Seeding ingredients...")
    for name, status, notes in SEED_DATA:
        add_ingredient(name, status, notes)
        print(f"  + {name} ({status})")
    print(f"Done. {len(SEED_DATA)} ingredients loaded.")

# Checks the research files against docs/RESEARCH-PROTOCOL.md.
# Usage (from the project folder):  python3 tools/check_research.py
# Prints errors (must fix) and warnings (must be explained in notes/problems), then a summary of what is missing.
import json, os, sys, glob, datetime

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'research')

HOTELS = {  # key: (check_in, check_out, nights)
 'A0': ('2027-02-27', '2027-02-28', 1), 'A1': ('2027-02-28', '2027-03-01', 1), 'A2': ('2027-03-01', '2027-03-02', 1),
 'A3': ('2027-03-02', '2027-03-03', 1), 'A4': ('2027-03-03', '2027-03-04', 1), 'A5': ('2027-03-04', '2027-03-05', 1),
 'A6': ('2027-03-05', '2027-03-06', 1),
 'B0': ('2027-02-27', '2027-02-28', 1), 'B1': ('2027-02-28', '2027-03-01', 1), 'B2': ('2027-03-01', '2027-03-02', 1),
 'B3': ('2027-03-02', '2027-03-03', 1), 'B4': ('2027-03-03', '2027-03-04', 1), 'B5': ('2027-03-04', '2027-03-05', 1),
 'B6': ('2027-03-05', '2027-03-06', 1),
 'C1': ('2027-02-28', '2027-03-01', 1), 'C2': ('2027-03-01', '2027-03-03', 2), 'C3': ('2027-03-03', '2027-03-05', 2),
 'C4': ('2027-03-05', '2027-03-06', 1),
}
CARS = {  # key: (pickup datetime, return datetime)
 'CA': ('2027-02-28T10:00', '2027-03-06T15:00'),
 'CB': ('2027-02-28T10:00', '2027-03-06T15:00'),
 'CC': ('2027-03-03T09:00', '2027-03-06T15:00'),
}
COMPANIES = ['Toyota Rent a Car', 'Times Car Rental', 'Nippon Rent-A-Car']
TIERS = ['lower', 'middle', 'higher']

errors, warnings = [], []
def err(f, m): errors.append('%s: %s' % (f, m))
def warn(f, m): warnings.append('%s: %s' % (f, m))

def load(path):
    try:
        return json.load(open(path, encoding='utf-8'))
    except Exception as e:
        err(os.path.basename(path), 'not valid JSON (%s)' % e)
        return None

def stamp_ok(f, d):
    try:
        datetime.datetime.fromisoformat(d.get('read_at', ''))
    except Exception:
        err(f, 'read_at missing or not an ISO date-time')

def num(v): return isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0

# ---------- hotels ----------
seen_h = set()
for path in sorted(glob.glob(os.path.join(base, 'hotels', '*.json'))):
    f = 'hotels/' + os.path.basename(path)
    d = load(path)
    if d is None: continue
    key = str(d.get('key', ''))
    root = key[:2]
    if root not in HOTELS:
        err(f, 'key %r is not in the protocol table' % key); continue
    if os.path.basename(path) != key + '.json':
        err(f, 'file name should be %s.json' % key)
    seen_h.add(key)
    ci, co, n = HOTELS[root]
    if d.get('check_in') != ci or d.get('check_out') != co:
        err(f, 'dates are %s to %s; the protocol says %s to %s' % (d.get('check_in'), d.get('check_out'), ci, co))
    if d.get('nights') != n: err(f, 'nights should be %d' % n)
    if d.get('adults') != 2 or d.get('rooms') != 1: err(f, 'must be 2 adults, 1 room')
    if 'hotels.com' not in str(d.get('site', '')).lower(): err(f, 'site must be hotels.com')
    stamp_ok(f, d)
    pc = d.get('page_confirms') or {}
    for k in ('destination', 'dates', 'travelers'):
        if not str(pc.get(k, '')).strip() or 'as shown' in str(pc.get(k, '')):
            err(f, 'page_confirms.%s is empty: read it back from the page' % k)
    if not d.get('filters_used'): warn(f, 'filters_used is empty')
    if not isinstance(d.get('qualifying_count'), int): warn(f, 'qualifying_count missing')
    if len(key) > 2 and not d.get('fallback_of'): err(f, 'fallback file must set fallback_of')
    picks = d.get('picks') or []
    if len(picks) != 3 and not str(d.get('problems', '')).strip():
        err(f, '%d picks and no explanation in problems' % len(picks))
    tiers = [p.get('tier') for p in picks]
    if len(set(tiers)) != len(tiers) or any(t not in TIERS for t in tiers): err(f, 'tiers must be distinct and one of lower/middle/higher')
    if len(set(p.get('name') for p in picks)) != len(picks): err(f, 'the same hotel appears twice')
    for p in picks:
        who = '%s (%s)' % (p.get('name', '?'), p.get('tier', '?'))
        if not str(p.get('name', '')).strip() or 'exact hotel name' in str(p.get('name')): err(f, 'pick without a real name')
        if not str(p.get('url', '')).startswith('https://'): err(f, who + ': url missing')
        if not p.get('currency'): err(f, who + ': currency missing')
        if p.get('price_source') != 'detail':
            (warn if str(p.get('notes', '')).strip() else err)(f, who + ': price not read from the detail view')
        ppn, tot = p.get('price_per_night'), p.get('total_with_taxes')
        if not num(ppn): err(f, who + ': price_per_night missing')
        if tot is None:
            if not str(p.get('notes', '')).strip(): err(f, who + ': total_with_taxes is null with no note')
            else: warn(f, who + ': total_with_taxes not shown by the site')
        elif not num(tot): err(f, who + ': total_with_taxes is not a number')
        elif num(ppn) and tot < ppn * n * 0.95:
            warn(f, who + ': total (%s) is less than nightly price times nights (%s x %d); check which is which' % (tot, ppn, n))
        if p.get('stars') not in (3, 4, 3.5, 4.5) and not str(p.get('notes', '')).strip(): warn(f, who + ': stars outside 3 to 4 with no note')
        gr = p.get('guest_rating')
        if not num(gr): err(f, who + ': guest_rating missing')
        elif gr < 8.0 and not str(p.get('notes', '')).strip(): warn(f, who + ': guest rating under 8.0 with no note')
        if not isinstance(p.get('review_count'), int): warn(f, who + ': review_count missing')
        for k in ('room_type', 'free_cancellation', 'parking'):
            if not str(p.get(k, '')).strip() or ' / ' in str(p.get(k, '')): err(f, who + ': %s not filled in' % k)

# ---------- cars ----------
seen_c = set()
for path in sorted(glob.glob(os.path.join(base, 'cars', '*.json'))):
    f = 'cars/' + os.path.basename(path)
    d = load(path)
    if d is None: continue
    key = d.get('key')
    if key not in CARS: err(f, 'key %r is not CA, CB or CC' % key); continue
    seen_c.add((key, d.get('company')))
    pu, rt = CARS[key]
    if (d.get('pickup') or {}).get('datetime') != pu or (d.get('return') or {}).get('datetime') != rt:
        err(f, 'pickup/return times do not match the protocol (%s to %s)' % (pu, rt))
    stamp_ok(f, d)
    if d.get('company') not in COMPANIES: warn(f, 'company %r is not one of the three named' % d.get('company'))
    pc = d.get('page_confirms') or {}
    if not d.get('problems'):
        for k in ('pickup', 'return'):
            if not str(pc.get(k, '')).strip() or 'as shown' in str(pc.get(k, '')): err(f, 'page_confirms.%s is empty' % k)
        if not num(d.get('total_shown')): err(f, 'total_shown missing and no problems stated')
        if not str(d.get('total_includes', '')).strip(): err(f, 'total_includes not filled in')
        if d.get('price_source') != 'detail': err(f, 'price not read from the detail view')
        if d.get('is_kei') is not True: warn(f, 'not a kei car; problems should say why')
        if key in ('CA', 'CC') and d.get('one_way_fee') is None and not str(d.get('notes', '')).strip(): err(f, 'one_way_fee is null with no note')
        if key == 'CA' and (not str(d.get('winter_tires', '')).strip() or ' / ' in str(d.get('winter_tires'))): err(f, 'winter_tires not filled in')

# ---------- tolls, flights (light checks) ----------
tolls = {os.path.basename(p)[0] for p in glob.glob(os.path.join(base, 'tolls', '*.json')) if load(p) is not None}
flights = {os.path.basename(p)[:2] for p in glob.glob(os.path.join(base, 'flights', '*.json')) if load(p) is not None}

print('ERRORS (%d)' % len(errors)); [print('  ' + e) for e in errors]
print('WARNINGS (%d)' % len(warnings)); [print('  ' + w) for w in warnings]
missing_h = [k for k in HOTELS if k not in seen_h]
missing_c = ['%s/%s' % (k, c) for k in CARS for c in COMPANIES if (k, c) not in seen_c]
print('SUMMARY')
print('  hotels done %d of %d; missing: %s' % (len(HOTELS) - len(missing_h), len(HOTELS), ', '.join(missing_h) or 'none'))
print('  fallback files: %s' % (', '.join(sorted(k for k in seen_h if len(k) > 2)) or 'none'))
print('  cars done %d of %d; missing: %s' % (9 - len(missing_c), 9, ', '.join(missing_c) or 'none'))
print('  tolls done for routes: %s (need A, B, C)' % (', '.join(sorted(tolls)) or 'none'))
print('  flights done: %s (need FA, FB; blocked until Bobby gives the return date)' % (', '.join(sorted(flights)) or 'none'))
sys.exit(1 if errors else 0)

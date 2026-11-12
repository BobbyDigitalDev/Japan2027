# Builds routes.js for the dashboard from the routing file and the day plans written below.
# Usage: python3 tools/build_routes.py <path to routes-osrm.json> <output routes.js>
# The routing file comes from the OSRM demo server (see docs/DASHBOARD.md in the private project folder).
# Day plans are drafts written by the assistant; place ids refer to places.js.
import json, sys

osrm = json.load(open(sys.argv[1], encoding='utf-8'))
NAMES = {
    'hnd': 'Haneda Airport', 'kamakura': 'Kamakura', 'hakone': 'Hakone (Lake Ashi)', 'narai': 'Narai-juku',
    'kisof': 'Kiso-Fukushima', 'tsumago': 'Tsumago', 'magome': 'Magome', 'takayama': 'Takayama',
    'shirakawa': 'Shirakawa-go', 'kanazawa': 'Kanazawa', 'shirahige': 'Shirahige Shrine (Lake Biwa)',
    'kyoto': 'Kyoto', 'fushimi': 'Fushimi Inari', 'hotel': 'Osaka (hotel)', 'osaka': 'Osaka (Umeda)',
    'himeji': 'Himeji', 'onomichi': 'Onomichi', 'tadanoumi': 'Tadanoumi port', 'hiroshima': 'Hiroshima',
    'miyajimaguchi': 'Miyajimaguchi ferry', 'kurashiki': 'Kurashiki', 'maiko': 'Maiko (bridge view)',
    'kobe': 'Kobe', 'nara': 'Nara', 'kinosaki': 'Kinosaki Onsen',
}
WINTER = 'https://wwwtb.mlit.go.jp/chubu/gifu/r7/rentacar_English.pdf'

PLANS = {
 'A': {
  'name': 'Route A', 'title': 'Tokyo to Osaka through the Alps', 'area': 'corridor',
  'tagline': 'Hakone, the Kiso Valley post towns, Takayama, Shirakawa-go, Kanazawa and Lake Biwa. Fits a Haneda arrival.',
  'arrive': 'Sat Feb 27: land at Haneda. Rest night in Tokyo. No driving.',
  'start': 'hnd',
  'days': [
   {'night': 'Hakone', 'short': 'Hakone', 'stops': [64, 63, 62], 'note': 'Pick up the car in the morning. Two short drives on the first day while adjusting to the time change. Yokohama is on the way if you want a third stop.'},
   {'night': 'Narai-juku', 'short': 'Narai', 'stops': [48, 49], 'note': 'The longest single drive of this route. Aim to arrive with daylight left to walk the post town.'},
   {'night': 'Magome', 'short': 'Magome', 'stops': [52, 51, 50, 47], 'note': 'Three short hops down the Kiso Valley, with time to walk part of the trail between Tsumago and Magome.'},
   {'night': 'Takayama', 'short': 'Takayama', 'stops': [61], 'note': 'Afternoon and evening in the old town.'},
   {'night': 'Kanazawa', 'short': 'Kanazawa', 'stops': [60, 54, 55, 56, 57, 58, 59], 'note': 'Shirakawa-go in the morning, Kanazawa by mid-afternoon.'},
   {'night': 'Kyoto', 'short': 'Kyoto', 'stops': [19, 20, 13, 17, 18], 'note': 'A morning in Kanazawa before the drive south. The Lake Biwa shrine is on the way.'},
   {'night': 'Osaka (hotel check-in)', 'short': 'Osaka', 'stops': [14], 'note': 'Fushimi Inari early, then return the car in Osaka and check in.'},
  ],
  'caveats': [
   'Snow: the Gifu transport office says winter tires are a legal requirement in the Hida region (Takayama, Shirakawa-go) in winter (<a href="%s" target="_blank" rel="noopener">source</a>). Confirm winter tires with the rental company. Mountain legs can be slower, or closed, after snowfall.' % WINTER,
   'This is a one-way rental (pick up in Tokyo, return in Osaka). The drop-off fee has not been researched.',
   'Kanazawa gets about half a day. Giving it a full day means dropping a Kiso Valley night.',
  ],
 },
 'B': {
  'name': 'Route B', 'title': 'Loop west out of Osaka', 'area': 'loop',
  'tagline': 'Himeji, Onomichi, Rabbit Island, Hiroshima, a night on Miyajima, Kurashiki and Kobe. Fits an Osaka arrival.',
  'arrive': 'Sat Feb 27: land at Kansai or Itami. Rest night in Osaka. No driving.',
  'start': 'osaka',
  'days': [
   {'night': 'Himeji', 'short': 'Himeji', 'stops': [25, 26], 'note': 'Pick up the car in the morning. One short drive on the first day; the castle in the afternoon.'},
   {'night': 'Onomichi', 'short': 'Onomichi', 'stops': [31, 32], 'note': 'Afternoon in Onomichi, where the Shimanami Kaido begins.'},
   {'night': 'Hiroshima', 'short': 'Hiroshima', 'stops': [33, 34, 35, 36, 37, 38, 39], 'note': 'Ferry to Rabbit Island from Tadanoumi port (check the timetable; ferries are about hourly according to map reviews), then on to Hiroshima.'},
   {'night': 'Miyajima', 'short': 'Miyajima', 'stops': [40, 41, 42, 43, 44], 'note': 'Morning in Hiroshima, a short drive to Miyajimaguchi, then the ferry. The car stays on the mainland. The videos recommend staying the night on the island.', 'night_at': [34.2959896, 132.3198285]},
   {'night': 'Kurashiki', 'short': 'Kurashiki', 'stops': [30], 'note': 'Morning on Miyajima, then the drive east. Canal quarter in the late afternoon. Kojima Jeans Street is a separate area 14 km south.'},
   {'night': 'Kobe', 'short': 'Kobe', 'stops': [28, 24], 'note': 'Stop at Maiko for the view of the Akashi-Kaikyo Bridge. Kobe beef for dinner.'},
   {'night': 'Osaka (hotel check-in)', 'short': 'Osaka', 'stops': [1], 'note': 'A short drive. Return the car and check in.'},
  ],
  'caveats': [
   'Pick-up and return are both in Osaka, so a one-way fee should not apply. Not yet confirmed with a rental company.',
   'Parking at Miyajimaguchi overnight has not been researched.',
   'This route has the most detail from the videos.',
  ],
 },
 'C': {
  'name': 'Route C', 'title': 'Shorter Kansai loop', 'area': 'loop',
  'tagline': 'Nara, two nights in Kyoto, Lake Biwa, two nights in Kinosaki Onsen, Himeji and Kobe. The least driving.',
  'arrive': 'Sat Feb 27: land at Kansai or Itami. Rest night in Osaka. No driving.',
  'start': 'osaka',
  'days': [
   {'night': 'Nara', 'short': 'Nara', 'stops': [21, 22, 23], 'note': 'Pick up the car in the morning. One short drive on the first day.'},
   {'night': 'Kyoto', 'short': 'Kyoto', 'stops': [14, 17, 18, 13], 'note': 'A short drive, then the east side of Kyoto.'},
   {'night': 'Kyoto', 'short': 'Kyoto', 'stops': [15, 11, 16, 12], 'note': 'The car stays parked. Arashiyama and the north-west of the city.', 'at': 'Kyoto'},
   {'night': 'Kinosaki Onsen', 'short': 'Kinosaki', 'stops': [19, 20, 29], 'note': 'The longest drive of this route. The Lake Biwa shrine is on the way.'},
   {'night': 'Kinosaki Onsen', 'short': 'Kinosaki', 'stops': [29], 'note': 'A rest day in the onsen town.', 'at': 'Kinosaki Onsen'},
   {'night': 'Himeji', 'short': 'Himeji', 'stops': [25, 26], 'note': 'Castle in the afternoon.'},
   {'night': 'Osaka (hotel check-in)', 'short': 'Osaka', 'stops': [28, 24], 'note': 'Bridge view at Maiko, lunch in Kobe, then return the car and check in.'},
  ],
  'caveats': [
   'Kyoto and Nara are usually easier by train than by car (general knowledge, not yet checked for parking). A variant is to do Feb 28 to Mar 2 by train and rent the car only for Mar 3 to 6.',
   'Outside the cities this route leans on fewer researched places: Kinosaki has one entry.',
   'Pick-up and return are both in Osaka, so a one-way fee should not apply. Not yet confirmed with a rental company.',
  ],
 },
}

out = []
for rid in 'ABC':
    plan, days = PLANS[rid], osrm['routes'][rid]
    assert len(days) == 7 and len(plan['days']) == 7
    pts = osrm['points']
    r = {k: plan[k] for k in ('name', 'title', 'area', 'tagline', 'arrive', 'caveats')}
    r['id'] = rid
    s = pts[plan['start']]
    r['start'] = {'name': NAMES[plan['start']], 'lat': s[1], 'lon': s[0]}
    r['days'] = []
    tot_min = tot_km = longest = 0
    for i, (pd, od) in enumerate(zip(plan['days'], days)):
        d = {'night': pd['night'], 'short': pd['short'], 'stops': pd['stops'], 'note': pd['note'], 'legs': [], 'line': [], 'min': 0, 'km': 0}
        if od:
            assert 'error' not in od
            via = od['via']
            for j, leg in enumerate(od['legs']):
                d['legs'].append({'from': NAMES[via[j]], 'to': NAMES[via[j + 1]], 'min': leg['min'], 'km': leg['km']})
            d['min'] = sum(l['min'] for l in od['legs'])
            d['km'] = round(sum(l['km'] for l in od['legs']), 1)
            d['line'] = od['line']
            end = pts[via[-1]]
            d['at'] = pd.get('night_at') or [end[1], end[0]]
        else:
            d['stay'] = pd['at']
        tot_min += d['min']; tot_km += d['km']; longest = max(longest, d['min'])
        r['days'].append(d)
    r['totalMin'], r['totalKm'], r['longestMin'] = tot_min, round(tot_km), longest
    r['noDriveDays'] = sum(1 for d in r['days'] if not d['legs'])
    out.append(r)
    print(rid, 'total', tot_min, 'min', round(tot_km), 'km', 'longest day', longest, 'no-drive days', r['noDriveDays'], [d['min'] for d in r['days']])

meta = {'source': 'OSRM routing on OpenStreetMap data', 'fetched': osrm['fetched'][:10],
        'checks': 'Two legs were compared with Google Maps on Nov 12, 2026: Hakone to Narai-juku 3 h 13 min (OSRM 3 h 16 min) and Himeji to Onomichi 2 h 15 min (OSRM 2 h 36 min).'}
js = ('// Generated by tools/build_routes.py. Drive times and lines: OSRM demo server on OpenStreetMap data, no traffic.\n'
      '// Draft options only. Nothing is booked.\n'
      'window.ROUTES = ' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';\n'
      'window.ROUTES_META = ' + json.dumps(meta, ensure_ascii=False) + ';\n')
open(sys.argv[2], 'w', encoding='utf-8').write(js)
print('bytes', len(js))

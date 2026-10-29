"""Namaste Bead Store (namastebeadstore.com): stone bead bracelets by stone and intention, stacking sets and value. All copy is written for this site only."""
import re, collections
from copybase import E, stone_color, intent_color, kinds_phrase, kind_one, plist, tradition, hood_list, HOODS as HOOD_DATA

AISLES = {
 'mini':    ('Mini Stackers, 2 to 4 mm', 'Mini 2-4mm', 'mini-bead-bracelets', 'Fine strands that disappear into a stack.', '#7fe0c4'),
 'six':     ('6 mm Everyday', '6 mm', '6mm-bead-bracelets', 'Petite beads for everyday and office stacks.', '#3fbf9b'),
 'eight':   ('8 mm Classics', '8 mm', '8mm-bead-bracelets', 'The classic stone bead bracelet, in the widest choice of stones.', '#1d7a5f'),
 'bold':    ('10 to 12 mm Bold', 'Bold 10-12mm', 'bold-bead-bracelets', 'Chunky beads that anchor a stack.', '#14324a'),
 'mixed':   ('Chips, Mixed & Charm Bracelets', 'Chips & Charms', 'chip-charm-bracelets', 'Chip-stone, multi-stone, chakra and charm bracelets.', '#c2410c'),
}
def assign(x):
    if x['base'] not in ('beaded', 'bracelet'): return None
    if x['base'] == 'bracelet' and not re.search(r'\bbead|chip|stone', x['title'], re.I): return None
    m = x['mm']
    if m is None or re.search(r'chip|charm|chakra|karma', x['title'], re.I) or len(x['stones']) > 2: return 'mixed'
    return 'mini' if m <= 4.5 else 'six' if m < 7 else 'eight' if m <= 9 else 'bold'
LABELS = {'stone': 'Stone', 'metal': 'Strung on'}
PRICE_BANDS = [('0-10', 'Under $10'), ('0-15', 'Under $15'), ('0-20', 'Under $20'), ('20-99999', '$20 and up')]
BRAND_BANDS = [('Under $12', 0, 12), ('$12 to $18', 12, 18), ('$18 and up', 18, 1e9)]
STONE_MIN = 3; INTENT_MIN = 3; NAV_INTENTS = True

VISIT_EYEBROW = 'Try a stack on in store'
def STORE_DESC(S): return f'Stone bead bracelet store by Union Square in Manhattan: about {S.ABOUT_N:,} natural stone bracelets by stone, intention and bead size, most under $20.'
REVIEW_TITLE = 'Built your stack with us?'
REVIEW_TEXT = 'Leave a quick Google review so others near Union Square can find the bracelet wall.'
LOGO_SVG = '<svg viewBox="0 0 40 40"><g fill="none" stroke-width="3.4"><ellipse cx="20" cy="12" rx="12" ry="4.2" stroke="#3fbf9b"/><ellipse cx="20" cy="20" rx="12" ry="4.2" stroke="currentColor"/><ellipse cx="20" cy="28" rx="12" ry="4.2" stroke="#7fe0c4"/></g></svg>'
WORDMARK = 'Namaste <b>Bead Store</b>'
BAR_TEXT = 'Stone bead bracelets at 2 West 14th Street'
SEARCH_PLACEHOLDER = 'Search a stone: amethyst, tiger eye, lava'
QUIZ = {
 'slug': 'build-your-stack', 'nav': 'Build a stack', 'cta': 'Build my stack',
 'title': 'Build Your Bracelet Stack', 'desc': 'Choose an intention, a bead size and a budget and get a stack of stone bead bracelets in stock at 2 West 14th Street.',
 'h1': 'Build your stack', 'lead': 'Pick an intention and a size, and we line up bracelets that are in stock right now. Runs only in your browser. Intentions follow crystal tradition, not science.', 'submit': 'Show my stack',
 'questions': [
  {'q': 'Your intention', 'options': [{'label': 'Protection', 'filter': {'intent': ['protection']}}, {'label': 'Love', 'filter': {'intent': ['love']}}, {'label': 'Calm', 'filter': {'intent': ['calm']}},
    {'label': 'Abundance', 'filter': {'intent': ['abundance']}}, {'label': 'Grounding', 'filter': {'intent': ['grounding']}}, {'label': 'Confidence', 'filter': {'intent': ['confidence']}}]},
  {'q': 'Bead size', 'options': [{'label': 'Fine (2-6 mm)', 'filter': {'mmax': 6.9}}, {'label': 'Classic 8 mm', 'filter': {'mmin': 7, 'mmax': 9}}, {'label': 'Bold (10 mm+)', 'filter': {'mmin': 9.1}}, {'label': 'Mix it up', 'filter': {}}]},
  {'q': 'Per bracelet', 'options': [{'label': 'Under $12', 'filter': {'maxp': 12}}, {'label': 'Under $18', 'filter': {'maxp': 18}}, {'label': 'Any', 'filter': {}}]},
 ]}
STACKS = [  # name, intention key, the stones to pull one bracelet each from (in order)
 ('protection', 'The Protection Stack', 'protection', ['black-tourmaline', 'obsidian', 'hematite']),
 ('love', 'The Love Stack', 'love', ['rose-quartz', 'rhodonite', 'garnet']),
 ('calm', 'The Calm Stack', 'calm', ['amethyst', 'howlite', 'lepidolite', 'sodalite', 'aquamarine']),
 ('abundance', 'The Abundance Stack', 'abundance', ['citrine', 'tiger-eye', 'aventurine', 'pyrite', 'jade']),
 ('grounding', 'The Grounding Stack', 'grounding', ['hematite', 'smoky-quartz', 'jasper', 'onyx', 'lava']),
 ('intuition', 'The Intuition Stack', 'intuition', ['labradorite', 'moonstone', 'lapis', 'amethyst']),
]
def stack_items(S, stones):
    out, used = [], set()
    for st in stones:
        pool = S.by_rank([x for x in S.leaders if x['family'] == st and not x['noimg'] and x['aisle'] in ('six', 'eight', 'bold') and id(x['group']) not in used])
        if pool: out.append(pool[0]); used.add(id(pool[0]['group']))
        if len(out) == 3: break
    return out
def stack_html(S, key, name, intent, stones, link=True):
    xs = stack_items(S, stones)
    if len(xs) < 2: return ''
    vids = ','.join(f"{next(v for v in x['variants'] if v['available'])['id']}:1" for x in xs)
    total = sum(x['price'] for x in xs)
    atc = [{'v': str(next(v for v in x['variants'] if v['available'])['id']), 'h': x['handle'], 't': x['title'], 'p': f"{float(next(v for v in x['variants'] if v['available'])['price']):.2f}",
            'i': x['images'][0] + ('&' if '?' in x['images'][0] else '?') + 'width=400', 'c': x['aisle'], 'k': x['base']} for x in xs]
    names = plist([S.STONE_NAME[x['family']] for x in xs])
    return (f'<div class="stack"><div><h3>{E(name)}</h3><p>{E(names)}: {len(xs)} stone bead bracelets that tradition links with {E(S.INTENT_NAME[intent].lower())}.</p>'
            f'<p class="total">Today: {S.money(total)} for all {len(xs)}</p><p><button type="button" class="btn buy" data-atc-items="{E(__import__('json').dumps(atc))}">Add the stack to cart</button></p>'
            f'<p class="small">Adds all {len(xs)} bracelets to your cart; remove any before you check out. Prices are confirmed live.{" Choose Pickup to collect on 14th Street." if S.PICKUP_ON else ""}</p>'
            + (f'<p><a href="/stacks/{key}/">About this stack &rarr;</a></p>' if link else '') + f'</div>{S.grid(xs)}</div>')
def FOOTER_EXPLORE(S):
    return [('Stacking sets', '/stacks/'), ('Build a stack', '/build-your-stack/'), ('Bracelets by stone', '/stones/'), ('Bracelets by intention', '/intentions/'),
            ('How to stack bracelets', '/guide/how-to-stack-bead-bracelets/'), ('Best value under $15', '/bead-bracelets-under-15/'), ('Bead bracelets in NYC', '/bead-bracelets-nyc/')]
FOOT_BLURB = 'Stone bead bracelets sorted by stone, intention and size, with ready-made stacks, on 14th Street by Union Square.'
HERO_BASES = ('beaded',)
def HERO(S):
    return {'eyebrow': 'Stone bead bracelets &middot; 2 West 14th Street &middot; Union Square',
            'h1': 'Pick a stone. <em>Stack your intention.</em>',
            'lede': f'{S.N:,} natural stone bead bracelets in {len([k for k in S.stone_any])} stones, sorted by bead size and by the intentions crystal tradition gives them. Most under $20, from {S.money(S.MIN_PRICE)}.' + (f' Reserve and pick up; {S.READY.lower()}.' if S.PICKUP_ON else ''),
            'shop_cta': 'Shop bracelets'}
def _stacks(S):
    body = ''.join(stack_html(S, *s) for s in STACKS[:3])
    return f'<section class="wrap"><div class="sechead"><h2>Ready-made stacks</h2><a href="/stacks/">All stacks &rarr;</a></div>{body}<p class="small">Stacks pair stones by crystal tradition. That is lore, not a claim about effects.</p></section>' if body else ''
def _stones(S):
    keys = [k for k in S.STONE_KEYS if k not in S.NON_STONE][:15]
    tiles = ''.join(f'<a class="scent" href="/stones/{k}/" style="--c:{stone_color(k)}"><b>{E(S.STONE_NAME[k])}</b><span>{E(stone_tile(S, k))}</span><small>{S.stone_any[k]} bracelets</small></a>' for k in keys)
    return f'<section class="wrap"><div class="sechead"><h2>Bracelets by stone</h2><a href="/stones/">All stones &rarr;</a></div><div class="scents">{tiles}</div></section>'
def _intents(S):
    chips = ''.join(f'<a class="chip" href="/intentions/{k}/">{E(S.INTENT_NAME[k])} <small>{S.intent_count[k]}</small></a>' for k in S.INTENT_KEYS)
    return f'<section class="wrap"><div class="sechead"><h2>By intention</h2></div><div class="chips">{chips}</div></section>'
def _near(S): return f'<section class="wrap"><div class="sechead"><h2>Directions to the bracelet wall</h2></div>{hood_list(S, "/near/")}</section>'
def _whys(S):
    return [(f'{S.N:,} bracelets', 'Sorted by bead size first, so stacks are easy to match.'),
            (f'{S.UNDER20:,} under $20', 'Stone bead bracelets at everyday prices, with live prices on every card.'),
            (('Pick up in store', f'Choose Pickup at checkout. {S.READY}.') if S.PICKUP_ON else ('', '')),
            ('One-tap stacks', 'Add a three-bracelet stack to your cart in one tap.'),
            ('By stone or intention', 'Every stone and intention has its own page.'),
            ('Open daily', 'From 11 AM on 14th Street at Fifth Avenue.')]
def _value(S): return S.by_rank([x for x in S.leaders if x['price'] < 12 and not x['noimg']])[:8]
def _best(S): return S.by_rank(S.leaders)[:8]
HOME_SECTIONS = [
 {'type': 'html', 'html': _stacks},
 {'type': 'grid', 'title': 'Top bracelets right now', 'select': _best, 'href': '/shop/', 'link': 'All bracelets', 'intro': 'By sales on namastebookshop.com, refreshed daily.'},
 {'type': 'html', 'html': _stones},
 {'type': 'visit'},
 {'type': 'html', 'html': _intents},
 {'type': 'grid', 'title': 'Best value: under $12', 'select': _value, 'href': '/bead-bracelets-under-15/', 'link': 'More value picks'},
 {'type': 'whys', 'title': 'Why the bracelet wall', 'items': _whys},
 {'type': 'quiz', 'title': 'Build your own stack', 'text': 'Choose an intention, a bead size and a budget.'},
 {'type': 'brands', 'title': 'Bracelet makers', 'n': 8},
 {'type': 'html', 'html': _near},
 {'type': 'review'},
 {'type': 'band', 'title': 'Reserve a stack, wear it home', 'text': lambda S: 'Every bracelet is a live listing. Reserve and pick up on 14th Street, or ship from New York City.',
  'steps': lambda S: [('Choose stones', 'By stone, intention, bead size or price.'), ('Pickup at checkout', f'Secure Shopify checkout. {S.READY or "Usually ready the same day"}.'), ('Stack and go', S.STORE_ADDR + '.')]},
]
def HOME_TITLE(S): return 'Namaste Bead Store | Stone Bead Bracelets by Stone & Intention, Union Square NYC'
def HOME_DESC(S): return f'{S.N:,} natural stone bead bracelets by stone, intention and bead size at {S.STORE_ADDR}. Ready-made stacks, most under $20. Pickup near Union Square.'
def SHOP_TITLE(S): return 'Shop Stone Bead Bracelets | Namaste Bead Store NYC'
def SHOP_DESC(S): return f'{S.N:,} stone bead bracelets from {S.money(S.MIN_PRICE)}. Filter by stone, size and price. Pick up at 2 West 14th Street or ship.'
SHOP_H1 = 'All stone bead bracelets'
def SHOP_SUB(S): return f'{S.N:,} bracelets in {len(S.AISLE_KEYS)} size aisles.'
def AISLE_TITLE(S, k): return f'{AISLES[k][0]} Stone Bracelets | Namaste Bead Store NYC'
def AISLE_DESC(S, k): return f'{AISLES[k][3]} {S.cat_count[k]} bracelets at 2 West 14th Street.'
def LANDINGS(S):
    return [{'path': '/bead-bracelets-under-15/', 'title': 'Stone Bead Bracelets Under $15 | Namaste Bead Store NYC', 'desc': f'{sum(1 for x in S.products if x["price"] < 15)} natural stone bracelets under $15 at 2 West 14th Street.', 'h1': 'Best value: under $15', 'sub': 'Real stone, small price.', 'filter': {'maxp': 15}},
            {'path': '/chakra-bracelets/', 'title': 'Chakra Bead Bracelets | Namaste Bead Store NYC', 'desc': 'Seven-stone chakra bracelets at 2 West 14th Street near Union Square.', 'h1': 'Chakra bracelets', 'sub': 'Seven stones for the seven chakras of yoga tradition.', 'filter': {'intent': ['chakra']}},
            {'path': '/lava-diffuser-bracelets/', 'title': 'Lava Stone Diffuser Bracelets | Namaste Bead Store NYC', 'desc': 'Lava bead bracelets that hold a drop of essential oil.', 'h1': 'Lava diffuser bracelets', 'sub': 'Porous lava beads take a drop of oil.', 'filter': {'q': 'lava'}}]
def stone_tile(S, k):
    tr = tradition(S, k); return f'Tradition: {plist(tr[:2])}' if tr else 'Natural stone beads'
def STONE_PAGE(S, k, xs):
    n = S.STONE_NAME[k]; tr = tradition(S, k); sizes = collections.Counter(S.AISLES[x['aisle']][1] for x in xs)
    lo = min(x['price'] for x in xs)
    return {'title': f'{n} Bead Bracelets from {S.money(lo)} | Namaste Bead Store NYC', 'desc': f'{len(xs)} {n.lower()} stone bead bracelets from {S.money(lo)}, by bead size, at 2 West 14th Street near Union Square.',
            'h1': f'{n} bracelets', 'sub': f'{len(xs)} bracelets from {S.money(lo)}',
            'intro': f'<p class="intro">By size: {", ".join(f"{n_} {s}" for s, n_ in sizes.most_common())}.</p>' + (f'<p class="note-belief">Crystal tradition connects {E(n.lower())} with {plist(tr)}. Stack it for the meaning; we do not claim it does anything.</p>' if tr else ''),
            'faq': [(f'What size {n.lower()} bracelet should I get?', '8 mm is the classic; 4 to 6 mm stacks easily; 10 to 12 mm is bold.'), (f'What goes with {n.lower()} in a stack?', 'Try one stone from the same intention, or a neutral like clear quartz, hematite or lava.')]}
def intent_tile(S, k): return f'{S.intent_count[k]} bracelets'
def INTENT_PAGE(S, k, xs):
    n = S.INTENT_NAME[k]; st = [S.STONE_NAME[s] for ik, _, sts, _ in S.INTENTS if ik == k for s in sts if s in S.STONE_NAME]
    stk = next((s for s in STACKS if s[2] == k), None)
    return {'title': f'{n} Bead Bracelets | Namaste Bead Store NYC', 'desc': f'{len(xs)} stone bead bracelets for {n.lower()}' + (f': {plist(st[:3]).lower()}' if st else '') + ', at 2 West 14th Street.',
            'h1': f'Bracelets for {n.lower()}', 'sub': f'{len(xs)} bracelets',
            'intro': (stack_html(S, *stk) if stk else '') + '<p class="note-belief">Stones on this page are the ones crystal tradition ties to this intention. We present it as lore only.</p>',
            'faq': [(f'Which stones are for {n.lower()}?', (f'Tradition most often names {plist(st[:5]).lower()}.' if st else 'See the bracelets above.') + ' This is belief, not a proven effect.')]}
def STONES_HUB(S): return {'title': 'Stone Bead Bracelets by Stone | Namaste Bead Store', 'desc': 'Every stone on our bracelet wall, with counts and prices.', 'h1': 'Bracelets by stone', 'lead': 'Choose a stone to see every size we have it in.'}
def INTENTS_HUB(S): return {'title': 'Bead Bracelets by Intention | Namaste Bead Store', 'desc': 'Stone bead bracelets grouped by intention, with ready-made stacks.', 'h1': 'Bracelets by intention', 'lead': 'Grouped by crystal tradition, offered as lore.'}
def brand_intro(S, k, st): return f'<p>{st["n"]} {E(S.BRAND_NAME[k])} bracelet{"s" if st["n"] != 1 else ""}, from {S.money(st["min"])}.</p>'
def brand_faq(S, k, st): return [(f'Where are {S.BRAND_NAME[k]} bracelets sold in NYC?', f'At {S.STORE_ADDR}; {st["n"]} in stock today.')]
def BRAND_H1(S, k): return f'{S.BRAND_NAME[k]} bracelets'
def BRAND_TITLE(S, k, st): return f'{S.BRAND_NAME[k]} Stone Bead Bracelets | Namaste Bead Store'
def BRAND_DESC(S, k, st): return f'{st["n"]} {S.BRAND_NAME[k]} stone bead bracelets from {S.money(st["min"])} at 2 West 14th Street, NYC.'
def BRANDS_TITLE(S): return 'Bracelet Makers A to Z | Namaste Bead Store'
def BRANDS_DESC(S): return 'Named makers of stone bead bracelets at Namaste Bead Store.'
BRANDS_H1 = 'Bracelet makers'
def BRANDS_LEAD(S, n): return f'{n} named makers; most bracelets are independent and easiest to browse <a href="/stones/">by stone</a>.'
PAIR = {'beaded': ['beaded'], 'bracelet': ['beaded']}
REL_BRAND = 'More from {brand}'
REL_SCENT = 'Other {scent} bracelets'
REL_PAIR = 'Stack it with'
REL_MORE = 'More in {aisle}'
def describe(S, x):
    stn = x['stones']; s = []
    s.append(f"{E(x['title'])}: a stone bead bracelet" + (f" in {E(plist([S.STONE_NAME[t] for t in stn[:3]]).lower())}" if stn else '') + (f", {x['mm']:g} mm beads" if x['mm'] else '') + '.')
    s.append({'mini': 'Fine beads like these are made for stacking three or four together.', 'six': 'A petite size that layers with almost anything.', 'eight': 'The classic 8 mm size: the easiest to stack and the widest choice of stones.',
              'bold': 'Big beads anchor a stack; pair with one or two finer strands.', 'mixed': 'A mixed or chip strand adds texture to a stack.'}.get(x['aisle'], ''))
    if stn and stn[0] not in S.NON_STONE and tradition(S, stn[0]): s.append(f"In crystal tradition {E(S.STONE_NAME[stn[0]].lower())} stands for {plist(tradition(S, stn[0]))}. A belief, not a claim.")
    s.append('Each stone is natural, so beads vary slightly from the photo. Roll on, roll off, and keep it dry to protect the stretch cord.')
    s.append('Pick it up at 2 West 14th Street near Union Square or ship from NYC. Checkout on Shopify through namastebookshop.com.')
    return [t for t in s if t]
def PRODUCT_DESC(S, x, v0): return f"{x['title']}, {S.money(v0['price'])}. Stone bead bracelet at 2 West 14th Street by Union Square" + (', pickup in about 2 hours.' if x['pickup'] else '.')
def ABOUT_DESC(S): return 'About Namaste Bead Store, the stone bead bracelet wall at 2 West 14th Street by Union Square. A brand of Wealth Edge Ventures Inc.'
ABOUT_H1 = 'About Namaste Bead Store'
def ABOUT(S):
    return f'''<p class="lead">Namaste Bead Store is a bracelet wall at {S.STORE_ADDR}: natural stone bead bracelets, sorted by bead size, by stone and by intention.</p>
<p>{S.N:,} bracelets are online with live prices, {S.UNDER20:,} of them under $20. Ready-made stacks put three together in one tap.{" Choose Pickup at checkout and collect on 14th Street." if S.PICKUP_ON else ""}</p>
<h2>Visit</h2><p>{S.STORE_ADDR}. Call <a href="tel:{S.TEL}">{S.PHONE}</a>.</p>{S.hours_html()}{S.visit_buttons()}
<h2>Who we are</h2><p>{S.LEGAL} Orders are checked out on Shopify through <a href="{S.SHOP}" rel="noopener">namastebookshop.com</a>.</p>
<h2>About intentions</h2><p>Our stacks follow what crystal traditions say about each stone. We share that as belief; it is not medical advice.</p>'''
VISIT_TITLE = 'Visit the Bracelet Wall near Union Square'
def VISIT_DESC(S): return f'Hours, directions and pickup for Namaste Bead Store at {S.STORE_ADDR}.'
def VISIT_LEAD(S): return f'Try a stack on at {S.STORE_ADDR}, on 14th Street just west of Fifth Avenue.'
def FAQ_DESC(S): return 'Stone bead bracelet questions: sizes, stacking, intentions, wrist fit, pickup and shipping.'
FAQ_H1 = 'Bracelet questions'
def FAQ(S):
    return [('How many bracelets should I stack?', 'Two to four is typical. See <a href="/guide/how-to-stack-bead-bracelets/">how to stack</a>.'),
            ('Which bead size is best?', '8 mm is the classic; mini 2 to 4 mm strands are great for layering; 10 to 12 mm is bold.'),
            ('Will it fit?', 'Stretch bracelets fit most wrists around 6.5 to 7 inches. Titles that say BIG Wrist run longer.'),
            ('Do the stacks really work?', 'Stacks follow crystal traditions. We present them as meaning and style, not as proven effects.'),
            ('How does Add the stack to cart work?', 'It puts every bracelet in the stack into your cart in one tap. You can change or remove any before you check out.'),
            ('Can I pick up today?', 'Choose Pickup at checkout.' + (f' Orders are {S.READY.lower()}.' if S.READY else '')),
            ('Where are you?', f'{S.STORE_ADDR}, a 4-minute walk from 14 St&ndash;Union Square.')]
def GUIDES(S):
    G = [{'path': '/stacks/', 'title': 'Stone Bead Bracelet Stacks by Intention | Namaste Bead Store', 'desc': 'Ready-made three-bracelet stacks for protection, love, calm, abundance, grounding and intuition.', 'h1': 'Ready-made stacks',
          'html': '<p class="lead">Three stones, one intention, one tap to cart. Stacks are rebuilt every day from what is in stock.</p>' + ''.join(stack_html(S, *s) for s in STACKS) + '<p class="note-belief">Stones are paired by crystal tradition. That is lore, not a claim.</p>'},
         {'path': '/guide/how-to-stack-bead-bracelets/', 'title': 'How to Stack Bead Bracelets', 'desc': 'Simple rules for stacking stone bead bracelets: sizes, colors and how many to wear.', 'h1': 'How to stack bead bracelets',
          'html': '''<p class="lead">A good stack mixes sizes, keeps one color story and leaves a little space.</p><ul><li><b>Anchor:</b> start with one 8 or 10 mm bracelet.</li><li><b>Layer:</b> add one or two 4 to 6 mm strands.</li><li><b>Texture:</b> finish with a chip or charm bracelet.</li><li><b>Color:</b> choose stones in one family, or one neutral (hematite, lava, clear quartz) with one bright stone.</li><li><b>Intention:</b> or pick three stones tradition ties to the same intention, like our <a href="/stacks/">ready-made stacks</a>.</li></ul>'''},
         {'path': '/bead-bracelets-nyc/', 'title': 'Stone Bead Bracelets in NYC near Union Square', 'store_ld': True, 'desc': f'{S.N:,} stone bead bracelets at {S.STORE_ADDR}, by Union Square.', 'h1': 'Stone bead bracelets in NYC',
          'html': f'<p class="lead">{S.N:,} bracelets, {S.UNDER20:,} under $20, on 14th Street at Fifth Avenue.</p>{hood_list(S, "/near/")}{S.visit_block()}'}]
    for key, name, intent, stones in STACKS:
        h = stack_html(S, key, name, intent, stones, link=False)
        if h: G.append({'path': f'/stacks/{key}/', 'title': f'{name}: Stone Bead Bracelet Set | Namaste Bead Store', 'desc': f'{name}: three stone bead bracelets crystal tradition links with {S.INTENT_NAME[intent].lower()}, in one tap.', 'h1': name,
                        'html': h + f'<p>Want to swap a stone? Browse <a href="/intentions/{intent}/">all {S.INTENT_NAME[intent].lower()} bracelets</a>.</p><p class="note-belief">Tradition, not a promise of effects.</p>'})
    return G
HOOD_LINE = {'union-square': 'From Union Square, the bracelet wall is a few minutes west on 14th Street.', 'east-village': 'From the East Village, take 14th Street west.', 'chelsea': 'From Chelsea, walk east on 14th.',
             'flatiron': 'From Flatiron, walk south on Fifth to 14th.', 'greenwich-village': 'From the Village, walk north on Fifth.', 'midtown': 'From Midtown, ride to 14th Street.'}
def HOODS(S):
    picks = S.by_rank([x for x in S.leaders if not x['noimg']])[:8]
    return [{'path': f'/near/{k}/', 'title': f'Stone Bead Bracelets near {n} | Namaste Bead Store', 'h1': f'Bead bracelets near {n}', 'desc': f'Stone bead bracelets near {n}, NYC: {S.N:,} at {S.STORE_ADDR}, most under $20.',
             'html': f'<p class="lead">{E(HOOD_LINE[k])}</p><h2>Getting here from {E(n)}</h2><p>{E(route)}</p><h2>On the wall now</h2>{S.grid(picks)}{S.visit_block()}<h2>Other neighborhoods</h2>{hood_list(S, "/near/", k)}'}
            for k, n, route in HOOD_DATA]
NOT_FOUND = 'That bracelet left the wall'

"""Single source of truth for the 80085.games project list.

Store status was checked 2026-11-24 as a logged-out visitor (Meta store pages,
iTunes lookup API, Playgama pages). Meta long descriptions and details come from
content/meta-about.json (scraped from the live store pages the same day).
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
META = json.load(open(os.path.join(ROOT, "content", "meta-about.json"), encoding="utf-8"))


def meta_url(app_id):
    return f"https://www.meta.com/experiences/{app_id}/"


def meta_about(key):
    t = META[key]["about"]
    # Touch to Match: the scrape caught the page head; keep only the About text
    if "\nLaunch\nAbout\n" in t:
        t = t.split("Reviews\nMore\n", 1)[1]
    t = t.split("\nmore...", 1)[0].strip()
    return t


def meta_details(key):
    m = META[key]
    rows = [
        ("Genres", m["genres"]), ("Game modes", m["modes"]), ("Play", m["player"]),
        ("Input", m["ctrl"]), ("Languages", m["langs"]), ("Comfort", m["comfort"]),
        ("Headsets", m["platforms"]), ("Released", m["release"]),
    ]
    return [(k, v) for k, v in rows if v]


APP_STORE_WS = "https://apps.apple.com/app/wrist-survivor/id6813660787"
APP_STORE_DICE = "https://apps.apple.com/app/dice-roller-d20-tarot/id6829247614"

# hover particles on the homepage card
FX = {'dead-fools-club': '💥 🔫 💀', 'wet-bottom': '🚢 💣 🌊', 'valxr': '👻 ⚔️ ✨', 'trrrack': '🏁 🚀 💨', 'touch-to-match': '💎 🍬 🍭', 'astrowitch': '🔮 ⭐ 🌙', 'dead-fools-club-manager': '💰 🪖 💥', 'tank-mania': '💥 🧱 🏁', 'wrist-survivors': '🔥 😈 💀', 'diceroller': '🎲 🪙 🃏', 'braid-rescue': '👑 🪙 🐍', 'gogogo': '⚫ ⚪', 'spanish-with-maria': '💬 🇪🇸 ❤️', 'english-with-maria': '💬 🇬🇧 ☕', 'diobooks': '📖 🏰 🎧', 'dead-fools-club-headshot': '🎯 💀 💥'}

# platform key -> label; links: platform -> store url (only live, verified)
PROJECTS = [
    dict(slug="dead-fools-club", id="dfc-3v3", name="Dead Fools Club: 3v3", featured=True,
         short="Tabletop 3v3 shooter on your real table: little fools with big guns, online or with bots.",
         image="dfc-3v3.jpg", platforms=["Quest"], soon=["iPhone"],
         links={"Quest": meta_url("1815373899772014")},
         about=meta_about("dfc-3v3"), details=meta_details("dfc-3v3")),
    dict(slug="wet-bottom", id="wet-bottom", name="Wet Bottom", wide=True,
         short="The classic sea battle as a glowing hologram on your table, played with your hands.",
         image="wet-bottom.jpg", platforms=["Quest"],
         links={"Quest": meta_url("1840880350554702")},
         about=meta_about("wet-bottom"), details=meta_details("wet-bottom")),
    dict(slug="valxr", id="valxr", name="VALXR",
         short="Tabletop survivor roguelite in MR: tiny heroes, endless ghosts, ridiculous upgrades.",
         image="valxr.jpg", platforms=["Quest"],
         links={"Quest": meta_url("1855915962384474")},
         about=meta_about("valxr"), details=meta_details("valxr")),
    dict(slug="trrrack", id="trrrack", name="TRRRack",
         short="Futuristic VR racing: starfighters, boost pads, loops and seven rivals who fight back.",
         image="trrrack.jpg", platforms=["Quest"], soon=["iPhone"],
         links={"Quest": meta_url("1828218085154262")},
         about=meta_about("trrrack"), details=meta_details("trrrack")),
    dict(slug="touch-to-match", id="touch-to-match", name="Touch to Match-3",
         short="Match-3 you can actually touch: the board floats in your room, you play with bare hands.",
         image="touch-to-match.jpg", platforms=["Quest"],
         links={"Quest": meta_url("3968429779890345")},
         about=meta_about("touch-to-match"), details=meta_details("touch-to-match")),
    dict(slug="astrowitch", id="astrowitch", name="AstroWitch",
         short="Lupita, a sly fortune teller, reads your stars, tarot and the I Ching by voice. 18+.",
         image="astrowitch.jpg", platforms=["Quest"],
         links={"Quest": meta_url("1841573847152019")},
         about=meta_about("astrowitch"), details=meta_details("astrowitch")),
    dict(slug="dead-fools-club-manager", id="dfc-manager", name="Dead Fools Club: Manager",
         short="Buy the gear, give the order, watch your squad of five fight it out on your table. Free.",
         image="dfc-manager.jpg", platforms=["Quest"],
         links={"Quest": meta_url("1855827625726641")},
         about=meta_about("dfc-manager"), details=meta_details("dfc-manager")),
    dict(slug="dead-fools-club-headshot", id="dfc-headshot", name="Dead Fools Club: Headshot",
         short="One hit to the head ends it: VR duels and 3v3 balloon brawls with fools who beg. Free to play.",
         image="dfc-headshot.jpg", platforms=["Quest"],
         links={"Quest": meta_url("1856281535681250")},
         about="""Welcome to the Dead Fools Club. Nobody remembers how they got here. Everyone has a number over their head.

DUEL — one on one. A single hit to the head or torso kills. No health bars, no second chances: read your opponent, take cover, take the shot. Every win moves your number up the ladder of 2400.

3 VS 3 BALLOONS — every hit inflates your head. Take too many and you float away and pop. First team to ten pops wins.

THEY TALK BACK — every fool in the club is a different person with a voice of their own. They were just teleported here. They plead, they cry, they scream when you hit them.

A NEW LOOK EVERY MATCH — dither, halftone, voxel, thermal, neon and more: the same fight never looks the same twice.

FREE TO PLAY. Join the club ($4.99) to dress your own fighter and open your own rooms for friends. Joining a friend's room is always free. Love the club? Support the servers with an optional donation — no gameplay advantage.

Contains blood, censored nudity and disturbing voices. Not for everyone.""",
         details=[("Genres", "Shooter, Action"), ("Game modes", "Single user, Multiplayer, Player versus player (PvP)"),
                  ("Play", "Standing"), ("Input", "Controllers"), ("Languages", "English"), ("Comfort", "Intense"),
                  ("Headsets", "Meta Quest 3S, Meta Quest 3, Meta Quest Pro, Meta Quest 2"), ("Released", "27 November 2026")]),
    dict(slug="tank-mania", id="tank-mania", name="Tank Mania",
         short="The classic tank game in VR: defend your HQ, alone or with a friend.",
         image="tank-mania.jpg", platforms=["Quest"],
         links={"Quest": meta_url("6649404315070257")},
         about=meta_about("tank-mania"), details=meta_details("tank-mania")),
    dict(slug="wrist-survivors", id="wrist-survivors", name="Wrist Survivors", own_page=True,
         short="A survivors-like that lives on your Apple Watch. Descend into hell, duel the bosses.",
         image="wrist-survivors.jpg", platforms=["Watch", "iPhone", "Web"],
         links={"Watch": APP_STORE_WS, "iPhone": APP_STORE_WS, "Web": "https://playgama.com/game/wrist-survivor"}),
    dict(slug="diceroller", id="dice-roller", name="Dice Roller: d20 & Tarot", icon=True,
         short="Dice, a coin, a d20, the Major Arcana and an Oracle Ball. Tap or shake to roll.",
         image="dice-roller.jpg", platforms=["iPhone", "Watch"],
         links={"iPhone": APP_STORE_DICE, "Watch": APP_STORE_DICE},
         about="""A pocket table for every game night — on Apple Watch and iPhone.

Tap anywhere (or shake) to roll. Six modes, each drawn with care:

• d20 — a gold-edged adventurer's die. Natural 20s burst into light, natural 1s glow red, with matching haptics.
• One die and two dice — glossy dice with the sum shown, in five colour schemes from Amber Resin to Casino Royal.
• Coin flip — a minted coin with a crown on one side and a laurel-wreathed "1" on the other.
• Tarot — draw one of the 22 Major Arcana on a gilded card.
• Oracle Ball — ask a yes-or-no question and watch the answer surface.

Made for the wrist:
• Works standalone on Apple Watch — no iPhone needed at the table.
• Big, readable results and haptics you can feel.
• The highlight on the dice follows the tilt of your wrist.

Private by design:
• No account, no ads, no tracking, no internet connection.
• Nothing leaves your device.

Free to use. Every tenth roll you'll be offered an optional tip — it unlocks nothing, it just keeps the dice rolling.""",
         details=[("Devices", "iPhone, Apple Watch (works standalone)"), ("Price", "Free, optional tips"), ("Data", "None collected")]),
    dict(slug="braid-rescue", id="braid-rescue", name="Braid Rescue",
         short="A snake-style arena in your browser: grow the longest braid, collect coins, cut rivals.",
         image="braid-rescue.jpg", platforms=["Web"],
         links={"Web": "https://playgama.com/game/braid-rescue"},
         about="Compete in this snake-style arena game to grow the longest braid by collecting coins and cutting rivals. Play it online for free on desktop, Android or iOS — right in the browser, nothing to install.",
         details=[("Where", "Playgama — desktop and mobile browsers"), ("Price", "Free")]),
    dict(slug="gogogo", id="gogogo", name="GoGoGo", status="soon",
         short="Learn and play Go in VR and MR: a voiced teacher, problems, bots and friends online.",
         image="gogogo.jpg", platforms=["Quest"], links={},
         about="""GoGoGo sits you at a wooden Go board in a quiet room — or puts the board on your own table in mixed reality — and teaches you the oldest strategy game in the world, one stone at a time.

LEARN FROM ZERO
• A teacher at the table explains every idea before using it, then lets you try it: liberties, capturing, ladders, nets, life and death
• Every lesson starts on a small board and grows with you: 5×5, 7×7, then 9×9
• Your first real games are "first capture wins", the way Go is taught to beginners in Japan

PLAY THE COMPUTER
• Novice, Club and Strong levels — the strong one is a neural network running right on your headset
• 9×9, 13×13 and 19×19 boards, Japanese rules, territory shown at the end
• Ask for a hint any time; take back a misplaced stone

SOLVE GO PROBLEMS
• Dozens of life-and-death and capturing problems, every one with a single right answer — proven by a solver
• Play a wrong move and see exactly how the opponent answers

PLAY A FRIEND ONLINE
• One button finds an opponent or opens a game and waits
• Invite a Meta friend straight to your table

FEELS LIKE A REAL BOARD
• Tap the point with your fingertip, or pinch a stone from the bowl and set it down
• Hand tracking first; Touch controllers work too
• English and Russian, with a voiced teacher in both""",
         details=[("Headsets", "Meta Quest 3, Meta Quest 3S"), ("Input", "Hands, Controllers"), ("Languages", "English, Russian")]),
    dict(slug="spanish-with-maria", id="spanish-with-maria", name="Spanish with Maria", status="soon",
         short="María, your Spanish teacher in VR: talk by voice, practise with your hands.",
         image="spanish-with-maria.jpg", platforms=["Quest"], links={},
         about="""Sit across the table from María, your Spanish teacher in VR on Meta Quest.

A TEACHER WHO TALKS WITH YOU
She speaks with you by voice, shows each new phrase on a card floating in front of you, waits for you to say it, and uses it with you in a tiny conversation — the way people actually learn a language.

PRACTISE WITH YOUR HANDS
Quizzes, words from scattered letters, sentences to fill, pairs to match — designed for hand tracking.

FREE TO START
A friendly level test with a real conversation and the first lessons are free. A separate 18+ pack teaches the street Spanish textbooks skip.

Adults only (18+). Speaking with María needs an internet connection.""",
         details=[("Input", "Hands, Voice"), ("Age", "18+")]),
    dict(slug="english-with-maria", id="english-with-maria", name="English with Maria", status="soon",
         short="María, your English teacher in VR: voice lessons, phrase cards, hands-on practice.",
         image="english-with-maria.jpg", platforms=["Quest"], links={},
         about="""Sit across the table from María, your English teacher in VR on Meta Quest.

A TEACHER WHO TALKS WITH YOU
She talks with you by voice, shows each phrase on a card in front of you and lets you practise with your hands — quizzes, words from scattered letters, pairs.

FREE TO START
A free level test and free first lessons. An 18+ pack teaches the street English textbooks skip.

Adults only (18+).""",
         details=[("Input", "Hands, Voice"), ("Age", "18+")]),
    dict(slug="diobooks", id="diobooks", name="DioBooks", status="soon",
         short="Classic audiobooks with layered dioramas of the scene rising around you.",
         image="diobooks.jpg", platforms=["Quest"], links={},
         about="""Listen to classic audiobooks while layered dioramas of the scene being read rise around you, in VR on Meta Quest.

Readers back the release of new DioBooks with Paragraph Coins and earn coins back when others buy them.""",
         details=[]),
]

for p in PROJECTS:
    p.setdefault("status", "live")
    p.setdefault("soon", [])
    p["page"] = f"/{p['slug']}/"
    p["fx"] = FX.get(p["slug"], "✨").split()

"""Copies store screenshots and trailers from the project folders into the site, web-sized.

Run: python3 tools/media.py   (needs sips + ffmpeg; skips files that already exist)
Output: img/shots/<slug>/NN.jpg (1280px, q70), video/<slug>.mp4 (720p) + video/<slug>.jpg poster.
"""
import glob, os, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.expanduser("~/Projects")

SHOTS = {
    "dead-fools-club": [f"{P}/IronBase/store/shots/*.png", f"{P}/IronBase/store/shots-b/*.png"],
    "dead-fools-club-manager": [f"{P}/IronBase-Auto/store/art-manager/screens/*.png"],
    "wet-bottom": [f"{P}/Wet Bottom Development/art-src/store/screenshot-*.png"],
    "valxr": [f"{P}/Publishing/games/valxr/store/art/screens/*.png"],
    "trrrack": [f"{P}/TRRRack/TRRRack Vault/90 Assets/store/screenshots/*.png"],
    "touch-to-match": [f"{P}/Publishing/games/touch-to-match/store/screenshots-v2/[0-9].png"],
    "astrowitch": [f"{P}/AstroWitch/AstroWitch Vault/08 Store/assets/screenshot_*.png"],
    "diceroller": [f"{P}/DiceRoller/store/screenshots/iphone-69/*.png", f"{P}/DiceRoller/store/screenshots/watch-ultra/*.png"],
    "gogogo": [f"{P}/Publishing/games/gogogo/store/pdp/screenshots/*.png"],
    "spanish-with-maria": [f"{P}/Uchilka/Uchilka-Development/store/screenshots/*.png"],
    "english-with-maria": [f"{P}/Uchilka/Uchilka-Development/store/screenshots_en/*.png"],
    "dead-fools-club-headshot": [f"{P}/Publishing/games/duel-royale/store/shots/*.png"],
}
VIDEOS = {
    "dead-fools-club": f"{P}/IronBase/store/trailer/DeadFoolsClub_trailer_B_outdoor.mp4",
    "wet-bottom": f"{P}/Publishing/games/wet-bottom/store/trailer/wetbottom-trailer-v4-2026-10-31.mp4",
    "trrrack": f"{P}/TRRRack/TRRRack Vault/90 Assets/store/trailer/trailer-v5-2026-10-17.mp4",
    "touch-to-match": f"{P}/Publishing/games/touch-to-match/store/ab-test-1/TouchToMatch_trailer_v3.mp4",
    "astrowitch": f"{P}/AstroWitch/AstroWitch Vault/08 Store/assets/trailer-v1-2026-11-01.mp4",
    "dead-fools-club-headshot": f"{P}/Publishing/games/duel-royale/store/DeadFoolsClub_Headshot_trailer.mp4",
}


def run(*a):
    subprocess.run(a, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def shots():
    for slug, pats in SHOTS.items():
        files = [f for p in pats for f in sorted(glob.glob(p))]
        d = os.path.join(ROOT, "img", "shots", slug)
        os.makedirs(d, exist_ok=True)
        for n, src in enumerate(files, 1):
            out = os.path.join(d, f"{n:02d}.jpg")
            if not os.path.exists(out):
                run("sips", "-s", "format", "jpeg", "-s", "formatOptions", "70", "-Z", "1280", src, "--out", out)
        print("shots", slug, len(files))


def videos():
    d = os.path.join(ROOT, "video")
    os.makedirs(d, exist_ok=True)
    for slug, src in VIDEOS.items():
        out = os.path.join(d, slug + ".mp4")
        if not os.path.exists(out):
            run("ffmpeg", "-y", "-i", src, "-vf", "scale=-2:720", "-c:v", "libx264", "-preset", "slow", "-crf", "29",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", out)
        poster = os.path.join(d, slug + ".jpg")
        if not os.path.exists(poster):
            run("ffmpeg", "-y", "-ss", "3", "-i", out, "-frames:v", "1", "-q:v", "5", poster)
        print("video", slug, os.path.getsize(out) // 1024, "KB")


if __name__ == "__main__":
    shots()
    videos()

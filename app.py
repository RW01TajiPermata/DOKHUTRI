import re
from datetime import datetime

import requests
from flask import Flask, abort, render_template, request

app = Flask(__name__)

# Ganti gambar banner utama "17 Agustus Desa Kita" di sini.
HOME_HERO = {
    "cover": "https://lh3.googleusercontent.com/d/1sZtrn6-Lg-lgRfHQUPRq2rkmMY61vjaj=w2000",
}

EVENTS = {
    "fun-match-badminton": {"title": "Fun Match Badminton", "category": "Olahraga", "description": "Pertandingan bulu tangkis penuh semangat dan sportivitas warga.", "folder_url": "https://drive.google.com/drive/folders/1jWy7DWcSSbEeDzWNppLqnYApjggkd-r6?usp=sharing", "cover": "https://lh3.googleusercontent.com/d/14wyTBvHNR3N2TMCPCmoCWx6ODoB3IBPf=w2000"},
    "lomba-anak-anak": {"title": "Lomba Anak-Anak", "category": "Perlombaan", "description": "Keceriaan anak-anak mengikuti aneka lomba kemerdekaan.", "folder_url": "https://drive.google.com/drive/folders/1PDi3BUB2WNJ3w9Gf9SlaI13LNGrloCdw?usp=sharing", "cover": "https://lh3.googleusercontent.com/d/1ZZ2oC6s2HW1ojcLEBEtJDVDjUHpDi9vf=w2000"},
    "lomba-ibu-ibu": {"title": "Lomba Ibu-ibu", "category": "Perlombaan", "description": "Keseruan dan kekompakan ibu-ibu dalam lomba 17 Agustus.", "folder_url": "https://drive.google.com/drive/folders/1jF_jvBylvF-7n7RjCU6IE45nDGftJ2GJ?usp=sharing", "cover": "https://lh3.googleusercontent.com/d/1ZZ2oC6s2HW1ojcLEBEtJDVDjUHpDi9vf=w2000"},
    "lomba-voli-bapak-bapak": {"title": "Lomba Voli Bapak-bapak", "category": "Olahraga", "description": "Pertandingan voli bapak-bapak yang seru dan penuh semangat.", "folder_url": "https://drive.google.com/drive/folders/1Iorran5cLYrgyCZNQWVBRYokP-IdymBW?usp=sharing", "cover": "https://lh3.googleusercontent.com/d/1ZZ2oC6s2HW1ojcLEBEtJDVDjUHpDi9vf=w2000"},
    "lomba-pemuda": {"title": "Lomba Pemuda", "category": "Perlombaan", "description": "Kegiatan kreatif dan kompetitif dari para pemuda desa.", "folder_url": "https://drive.google.com/drive/folders/1kB2y-6l8nllPNAPuT3qf-SFNOZbjA3cf?usp=sharing", "cover": "https://lh3.googleusercontent.com/d/1ZZ2oC6s2HW1ojcLEBEtJDVDjUHpDi9vf=w2000"},
    "malam-tirakatan": {"title": "Malam Tirakatan", "category": "Tradisi", "description": "Malam doa dan refleksi untuk mengenang perjuangan kemerdekaan.", "folder_url": "https://drive.google.com/drive/folders/1pvpT0qLd9C1vnSuPtWhgjM7BDuZXTMla?usp=sharing", "cover": "https://lh3.googleusercontent.com/d/1ZZ2oC6s2HW1ojcLEBEtJDVDjUHpDi9vf=w2000"},
    "malam-pentas-seni": {"title": "Malam Pentas Seni", "category": "Hiburan", "description": "Panggung seni, musik, dan kreativitas warga desa.", "folder_url": "https://drive.google.com/drive/folders/11QTKtgtDlMDT_VzRiEfkItZYyM9tcbFb?usp=sharing", "cover": "https://lh3.googleusercontent.com/d/1ZZ2oC6s2HW1ojcLEBEtJDVDjUHpDi9vf=w2000"},
    "jalan-sehat": {"title": "Jalan Sehat", "category": "Kebersamaan", "description": "Langkah sehat dan semangat kebersamaan seluruh warga.", "folder_url": "https://drive.google.com/drive/folders/1z40nXdB-aNFMyZK6vN44lcmNzjO-wWSi?usp=sharing", "cover": "https://lh3.googleusercontent.com/d/1ZZ2oC6s2HW1ojcLEBEtJDVDjUHpDi9vf=w2000"},
    "poster-hut-ri-81": {"title": "Poster HUT RI 81", "category": "Kreativitas", "description": "Koleksi poster peringatan Hari Ulang Tahun Republik Indonesia ke-81.", "folder_url": "https://drive.google.com/drive/folders/1GwHnL6T6IccWDqzOYGIxY7OrEfmYXht7?usp=sharing", "cover": "https://lh3.googleusercontent.com/d/1qatAO1ITRlKQYd_ZGttR_Zthj0mpJAEz=w2000"},
}

def drive_photos(folder_url):
    """Baca thumbnail file dari halaman folder Drive publik, tanpa API key."""
    if not folder_url:
        return []
    try:
        # endpoint tampilan folder publik; data thumbnail tersedia tanpa autentikasi
        response = requests.get(folder_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        # Google menyisipkan id file dalam data halaman. Hilangkan ID folder dan duplikasi.
        folder_id = re.search(r"/folders/([A-Za-z0-9_-]+)", folder_url)
        ignored_id = folder_id.group(1) if folder_id else ""
        file_ids = []
        # ID file dalam folder ini berformat 33 karakter dan diawali angka 1.
        # Pola ini menghindari teks JavaScript yang ikut dimuat oleh halaman Drive.
        for file_id in re.findall(r"(?<![A-Za-z0-9_-])1[A-Za-z0-9_-]{32}(?![A-Za-z0-9_-])", response.text):
            if file_id != ignored_id and file_id not in file_ids:
                file_ids.append(file_id)
        # lh3.googleusercontent menampilkan file gambar langsung di elemen <img>.
        return [{"id": file_id, "name": f"Dokumentasi {number}", "thumbnailLink": f"https://lh3.googleusercontent.com/d/{file_id}=w1000"} for number, file_id in enumerate(file_ids[:10], 1)]
    except requests.RequestException:
        return []

@app.context_processor
def inject_globals():
    return {"events": EVENTS, "year": datetime.now().year}

@app.route("/")
def index():
    query = request.args.get("q", "").strip()
    normalized_query = query.casefold()
    cards = []
    for slug, event in EVENTS.items():
        searchable_text = f"{event['title']} {event['category']} {event['description']}".casefold()
        if normalized_query and normalized_query not in searchable_text:
            continue
        # Cover kartu selalu memakai gambar cover event, bukan thumbnail Drive.
        # Dengan begitu cover tetap tampil meskipun folder Drive sedang tidak bisa dibaca.
        cards.append({**event, "slug": slug, "thumbnail": event["cover"]})
    return render_template("index.html", cards=cards, hero=HOME_HERO, search_query=query)

@app.route("/tentang")
def about():
    return render_template("about.html")

@app.route("/event/<slug>")
def event_detail(slug):
    event = EVENTS.get(slug)
    if not event:
        abort(404)
    folder_url = event.get("folder_url", "")
    photos = drive_photos(folder_url)
    is_demo = not photos
    if is_demo:
        photos = [{"name": f"Dokumentasi {i + 1}", "thumbnailLink": image} for i, image in enumerate(SAMPLE_PHOTOS)]
    return render_template("event.html", event=event, photos=photos, demo=is_demo, drive_url=folder_url or "#")

if __name__ == "__main__":
    app.run(debug=True)

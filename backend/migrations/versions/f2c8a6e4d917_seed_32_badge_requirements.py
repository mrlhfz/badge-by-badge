"""seed the requirements and groups of 32 badges that only existed in dev, restore Jaya Kumpulan IV, correct Peladang Muda details

Revision ID: f2c8a6e4d917
Revises: d4b7f0c9a582
Create Date: 2026-10-27 10:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f2c8a6e4d917"
down_revision: str | Sequence[str] | None = "d4b7f0c9a582"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# (badge name, group title, pick count, position, parent group title, applies when poultry)
GROUPS = [
    ("Ahli Koleksi Hobi", "Kumpul EMPAT daripada 8 perkara", 4, 1, None, False),
    ("Ahli Komunikasi Marin", "Lulus SEMUA ujian dalam SATU bahagian", 1, 1, None, False),
    ("Ahli Komunikasi Marin", "Bahagian A: Semaphore, Morse, bendera", 4, 2, "Lulus SEMUA ujian dalam SATU bahagian", False),
    ("Ahli Komunikasi Marin", "Bahagian B: Log, gelombang, semboyan, SKMM", 4, 3, "Lulus SEMUA ujian dalam SATU bahagian", False),
    ("Ahli Muzik", "Lulus semua ujian dalam SATU bahagian (A-E)", 1, 1, None, False),
    ("Ahli Muzik", "Bahagian A", 4, 2, "Lulus semua ujian dalam SATU bahagian (A-E)", False),
    ("Ahli Muzik", "Bahagian B", 3, 3, "Lulus semua ujian dalam SATU bahagian (A-E)", False),
    ("Ahli Muzik", "Bahagian C", 2, 4, "Lulus semua ujian dalam SATU bahagian (A-E)", False),
    ("Ahli Muzik", "Bahagian D", 6, 5, "Lulus semua ujian dalam SATU bahagian (A-E)", False),
    ("Ahli Muzik", "Bahagian E", 2, 6, "Lulus semua ujian dalam SATU bahagian (A-E)", False),
    ("Ahli Muzik", "Pilih SATU: lagu rakyat atau lagu dengan alat", 1, 7, "Bahagian C", False),
    ("Ahli Muzik", "Syarat asas muzik", 1, 8, "Bahagian C", False),
    ("Ahli Muzik", "Ahli pancaragam", 1, 9, "Bahagian E", False),
    ("Ahli Muzik", "Pilih SATU alat muzik", 1, 10, "Bahagian E", False),
    ("Ahli Muzik", "Gendang Iringan (Side Drum)", 6, 11, "Pilih SATU alat muzik", False),
    ("Ahli Muzik", "Gendang Suara Langsing (Tenor Drum)", 4, 12, "Pilih SATU alat muzik", False),
    ("Ahli Muzik", "Gendang Suara Rendah (Bass Drum)", 5, 13, "Pilih SATU alat muzik", False),
    ("Ahli Muzik", "Bugle atau Trumpet", 3, 14, "Pilih SATU alat muzik", False),
    ("Ahli Oseanografi", "Pilih SATU kajian: A, B, C atau D", 1, 1, None, False),
    ("Juru Masak di Khemah", "Pilih SATU: ikan panggang, roti berlauk atau bubur", 1, 1, None, False),
    ("Juru Masak di Khemah", "Pilih SATU: mee, ayam atau masakan biasa", 1, 2, None, False),
    ("Juru Masak di Khemah", "Pilih SATU makanan manis", 1, 3, None, False),
    ("Koordinator Pameran Pengakap Laut", "Pilih sekurang-kurangnya 7 daripada 11 aspek", 7, 1, None, False),
    ("Kuartermaster", "Lakukan Kumpulan ujian 1-6 ATAU 7-14", 1, 1, None, False),
    ("Kuartermaster", "Kumpulan ujian A (1-6)", 6, 2, "Lakukan Kumpulan ujian 1-6 ATAU 7-14", False),
    ("Kuartermaster", "Kumpulan ujian B (7-14)", 8, 3, "Lakukan Kumpulan ujian 1-6 ATAU 7-14", False),
    ("Lencana Jaya", "Kejayaan: lakukan SATU kemahiran", 1, 1, None, False),
    ("Lencana Maju", "Melakukan DUA perkara", 2, 1, None, False),
    ("Peladang Muda", "Pilih SATU Kumpulan: A, B, C atau D", 1, 1, None, False),
    ("Peladang Muda", "Kumpulan A (pusat ternakan)", 3, 2, "Pilih SATU Kumpulan: A, B, C atau D", False),
    ("Peladang Muda", "Kumpulan B (kebun)", 2, 3, "Pilih SATU Kumpulan: A, B, C atau D", False),
    ("Peladang Muda", "Kumpulan C (ternakan setahun)", 2, 4, "Pilih SATU Kumpulan: A, B, C atau D", False),
    ("Peladang Muda", "Kumpulan D (akuarium)", 2, 5, "Pilih SATU Kumpulan: A, B, C atau D", False),
    ("Peladang Muda", "Kumpulan C: asas (ujian 1 dan 2)", 2, 6, "Kumpulan C (ternakan setahun)", False),
    ("Peladang Muda", "Kumpulan C: unggas (ujian 3)", 1, 7, "Kumpulan C (ternakan setahun)", True),
    ("Pengail Muda", "Lempar atau labuh mata kail: pilih SATU", 1, 1, None, False),
    ("Pustakawan", "Pilih SATU: senarai 12 buku atau buku digemari", 1, 1, None, False),
    ("Pustakawan", "Pilihan 1: senarai 12 buku dibaca", 1, 2, "Pilih SATU: senarai 12 buku atau buku digemari", False),
    ("Pustakawan", "Pilihan 2: buku digemari", 3, 3, "Pilih SATU: senarai 12 buku atau buku digemari", False),
]

# (badge name, group title or None, position, text, detail)
REQUIREMENTS = [
    # Ahli Akuakultur
    ("Ahli Akuakultur", None, 1, "Kertas kerja projek penternakan ikan", "Menyediakan satu kertas kerja projek penternakan ikan air tawar atau masin."),
    ("Ahli Akuakultur", None, 2, "Penternakan ikan 3 bulan", "Melibatkan diri dalam penternakan ikan selama 3 bulan."),
    ("Ahli Akuakultur", None, 3, "Kitaran hidup ikan diternak", "Boleh menerangkan kepada Penguji tentang kitaran hidup ikan yang diternak."),
    ("Ahli Akuakultur", None, 4, "Penyelenggaraan medium penternakan", "Melaporkan kaedah penyelenggaraan medium penternakan (kolam, tanah, sungai)."),
    ("Ahli Akuakultur", None, 5, "Rekod jenis makanan ternakan", "Merekodkan jenis makanan yang diberikan kepada ternakan selama tempoh itu."),
    ("Ahli Akuakultur", None, 6, "Pembentangan agensi berkaitan", "Membuat pembentangan ringkas tentang satu agensi yang terlibat (Jabatan Perikanan, FAMA, LKIM)."),
    ("Ahli Akuakultur", None, 7, "Tulis laporan lengkap", "Menulis laporan lengkap tentang semua aktiviti di atas."),
    # Ahli Astronomi
    ("Ahli Astronomi", None, 1, "Beza galaksi, bintang, bulan, asteroid, meteor, komet", "Menerangkan perbezaan antara galaksi, bintang, bulan, asteroid, meteor dan komet."),
    ("Ahli Astronomi", None, 2, "Lawatan ke planetarium atau balai cerap", "Lawatan ke planetarium atau balai cerap bintang."),
    ("Ahli Astronomi", None, 3, "Kenali sekstan dan kegunaannya", "Mengenali sekstan dan kegunaannya."),
    ("Ahli Astronomi", None, 4, "Arah mata angin dengan jam dan bayang kayu", "Menunjukkan cara menentukan arah mata angin dengan jam tangan dan bayang kayu."),
    ("Ahli Astronomi", None, 5, "Bentuk buruj Big Dipper dan Orion", "Mengetahui bentuk dan kepentingan buruj Big Dipper (Ursa Major) dan Orion."),
    ("Ahli Astronomi", None, 6, "Arah mata angin dengan buruj Orion", "Menunjukkan cara menentukan arah mata angin dengan buruj Orion."),
    ("Ahli Astronomi", None, 7, "Kesan fasa bulan kepada pasang surut", "Mengetahui kesan fasa bulan terhadap pasang surut air laut."),
    ("Ahli Astronomi", None, 8, "Teleskop dan binokular untuk cerapan", "Mengetahui jenis teleskop dan binokular yang sesuai untuk cerapan bintang."),
    ("Ahli Astronomi", None, 9, "Cerapan 3 jam dengan teleskop atau binokular", "Merancang dan melibatkan diri dalam cerapan dengan teleskop/binokular sekurang-kurangnya 3 jam."),
    ("Ahli Astronomi", None, 10, "Tulis laporan lengkap", "Menulis laporan lengkap."),
    # Ahli Koleksi Hobi
    ("Ahli Koleksi Hobi", None, 1, "Kumpul satu jenis barang 6 bulan", "Mengumpul, menyusun dan mengatur dengan kemas dan menarik suatu jenis barang dalam tempoh tidak kurang 6 bulan."),
    ("Ahli Koleksi Hobi", None, 2, "Tahu sebab barang dipilih", "Mengetahui serba sedikit tentang barang yang dikumpul; membincangkan dengan Penilai sebab barang itu dipilih."),
    ("Ahli Koleksi Hobi", "Kumpul EMPAT daripada 8 perkara", 3, "Skaf Pengakap", "Mengumpul atau menyimpan skaf Pengakap."),
    ("Ahli Koleksi Hobi", "Kumpul EMPAT daripada 8 perkara", 4, "Lencana Pengakap", "Mengumpul atau menyimpan lencana Pengakap."),
    ("Ahli Koleksi Hobi", "Kumpul EMPAT daripada 8 perkara", 5, "Wogel", "Mengumpul atau menyimpan wogel."),
    ("Ahli Koleksi Hobi", "Kumpul EMPAT daripada 8 perkara", 6, "Topi (peak cap)", "Mengumpul atau menyimpan topi (peak cap)."),
    ("Ahli Koleksi Hobi", "Kumpul EMPAT daripada 8 perkara", 7, "Tali pinggang", "Mengumpul atau menyimpan tali pinggang."),
    ("Ahli Koleksi Hobi", "Kumpul EMPAT daripada 8 perkara", 8, "Kemeja-T", "Mengumpul atau menyimpan kemeja-T."),
    ("Ahli Koleksi Hobi", "Kumpul EMPAT daripada 8 perkara", 9, "Sampul surat Hari Pertama Jambori", "Mengumpul atau menyimpan sampul surat Hari Pertama Jambori."),
    ("Ahli Koleksi Hobi", "Kumpul EMPAT daripada 8 perkara", 10, "Majalah Pengakap", "Mengumpul atau menyimpan majalah Pengakap."),
    # Ahli Komunikasi Marin
    ("Ahli Komunikasi Marin", "Bahagian A: Semaphore, Morse, bendera", 1, "Semaphore dan isyarat huruf A-Z, nombor 0-9", "Semaphore dan isyarat huruf A-Z, nombor 0-9."),
    ("Ahli Komunikasi Marin", "Bahagian A: Semaphore, Morse, bendera", 2, "Berita mudah (S.O.S.)", "Menghantar dan menerima berita mudah (S.O.S.)."),
    ("Ahli Komunikasi Marin", "Bahagian A: Semaphore, Morse, bendera", 3, "Morse dengan buzzer atau flashing", "Menghantar dan menerima kod Morse dengan buzzer 100 m atau flashing."),
    ("Ahli Komunikasi Marin", "Bahagian A: Semaphore, Morse, bendera", 4, "Bendera abjad dan gada-gada INTERCO", "Bendera abjad dan gada-gada sistem INTERCO."),
    ("Ahli Komunikasi Marin", "Bahagian B: Log, gelombang, semboyan, SKMM", 5, "Buku Log 3 bulan", "Menyimpan Buku Log 3 bulan berkenaan penerimaan berita dari 20 stesen amatur."),
    ("Ahli Komunikasi Marin", "Bahagian B: Log, gelombang, semboyan, SKMM", 6, "Bincang gelombang dengan Penilai", "Membincangkan gelombang (frequency bands) dengan Penilai."),
    ("Ahli Komunikasi Marin", "Bahagian B: Log, gelombang, semboyan, SKMM", 7, "Kenal 10 semboyan Q", "Mengenal 10 jenis semboyan Q antarabangsa."),
    ("Ahli Komunikasi Marin", "Bahagian B: Log, gelombang, semboyan, SKMM", 8, "Peraturan SKMM walkie-talkie", "Mengetahui peraturan SKMM tentang walkie-talkie."),
    # Ahli Muzik
    ("Ahli Muzik", "Bahagian A", 1, "Lagu berkorus", "Menyanyi sebuah lagu yang ada korus."),
    ("Ahli Muzik", "Bahagian A", 2, "Baca titinada 3 lagu", "Membaca sendiri titinada muzik sekurang-kurangnya untuk 3 buah lagu (melodi)."),
    ("Ahli Muzik", "Bahagian A", 3, "Tanda tempo dan 3 contoh", "Mengetahui erti tanda tempo dan tanda muzik yang menunjukkan tinggi rendah, panjang pendek suara dalam titinada Sonata, Concerto dan Oratario serta memberi 3 contoh bagi tiap-tiap satu."),
    ("Ahli Muzik", "Bahagian A", 4, "Bincang 2 pertunjukan terbaru", "Membincangkan dengan Penilai sekurang-kurangnya dua pertunjukan hiburan terbaru yang dilihat atau didengari melalui televisyen atau radio."),
    ("Ahli Muzik", "Bahagian B", 5, "Menyanyi 2 lagu pilihan dan 1 lagu lagi", "Menyanyi 2 buah lagu yang dipilih sendiri dan sebuah lagu lagi yang sesuai untuk dinyanyikan dengan iringan muzik atau memainkannya dengan alat muzik."),
    ("Ahli Muzik", "Bahagian B", 6, "Lagu cepat dan lambat", "Menyanyi 2 buah lagu pilihan sendiri, satu bertempo cepat dan satu lagi bertempo lambat, dengan memainkan alat muzik sendiri atau dengan iringan muzik latar."),
    ("Ahli Muzik", "Bahagian B", 7, "Tanda tempo dan 3 contoh (B)", "Mengetahui erti tanda tempo Sonata, Concerto dan Oratario serta memberi 3 contoh bagi tiap-tiap satu."),
    ("Ahli Muzik", "Pilih SATU: lagu rakyat atau lagu dengan alat", 8, "Dua lagu rakyat tanpa iringan", "Menyanyi tanpa iringan alat muzik, dua jenis lagu rakyat yang berlainan jenisnya."),
    ("Ahli Muzik", "Pilih SATU: lagu rakyat atau lagu dengan alat", 9, "Lagu pilihan dengan alat muzik", "Menyanyi sebuah lagu pilihan sendiri dengan memainkan alat muzik seperti gambus, banjo, gitar, mandolin, harmonica dan sebagainya."),
    ("Ahli Muzik", "Syarat asas muzik", 10, "Prinsip asas muzik", "Mengetahui sedikit sebanyak prinsip asasi muzik seperti menala alat muzik, titinada, tali dan nada suara (bass)."),
    ("Ahli Muzik", "Bahagian D", 11, "Main bagpipe dengan memuaskan", "Menunjukkan kebolehan memainkan dan membunyikan alat muzik bagpipe dengan memuaskan."),
    ("Ahli Muzik", "Bahagian D", 12, "Bagpipe march 2/4 (2 lagu)", "Memainkan 2 lagu dengan bagpipe irama march dalam tempo 2/4."),
    ("Ahli Muzik", "Bahagian D", 13, "Bagpipe march 6/8 (2 lagu)", "Memainkan 2 lagu dengan bagpipe irama march dalam tempo 6/8."),
    ("Ahli Muzik", "Bahagian D", 14, "Bagpipe slow march (2 lagu)", "Memainkan 2 lagu dengan bagpipe irama slow march atau tiupan perlahan."),
    ("Ahli Muzik", "Bahagian D", 15, "Bagpipe march, strathspey, reel", "Memainkan satu lagu dengan bagpipe irama march, strathspey dan reel."),
    ("Ahli Muzik", "Bahagian D", 16, "Bincang muzik budaya dan artis", "Membincangkan dengan Penilai jenis muzik bercorak kebudayaan, artis biduan dan biduanita yang diminati serta memberi sebab pemilihan itu."),
    ("Ahli Muzik", "Ahli pancaragam", 17, "Ahli pancaragam", "Menjadi salah seorang ahli pancaragam, sama ada di sekolah dalam Kumpulan Pengakap atau dalam pertubuhan lain."),
    ("Ahli Muzik", "Gendang Iringan (Side Drum)", 18, "Jaga gendang iringan", "Menjaga alat muzik ini sentiasa berada dalam keadaan yang baik, bersih dan boleh digunakan bila-bila masa."),
    ("Ahli Muzik", "Gendang Iringan (Side Drum)", 19, "Berbaris dengan gendang iringan", "Berbaris berjalan dengan segak membawa gendang dan kayu pemukulnya sewajarnya."),
    ("Ahli Muzik", "Gendang Iringan (Side Drum)", 20, "Paluan tempo 2/3, 6/8, 3/4", "Memalu gendang dengan paluan tempo 2/3, 6/8 dan 3/4."),
    ("Ahli Muzik", "Gendang Iringan (Side Drum)", 21, "Paluan berhenti-henti (play off)", "Memalu gendang berhenti-henti (play off) dengan tempo 2/3, 6/8 dan 3/4."),
    ("Ahli Muzik", "Gendang Iringan (Side Drum)", 22, "Paluan bergulung 3, 5, 7 langkah", "Memalu gendang dengan paluan bergulung (roll): 3 langkah, 5 langkah dan 7 langkah bergulung."),
    ("Ahli Muzik", "Gendang Iringan (Side Drum)", 23, "6 perbarisan march", "Mengambil bahagian dengan memuaskan dalam 6 perbarisan march yang berlainan."),
    ("Ahli Muzik", "Gendang Suara Langsing (Tenor Drum)", 24, "Jaga gendang suara langsing", "Menjaga alat muzik ini supaya sentiasa berada dalam keadaan yang baik, bersih dan boleh digunakan bila-bila masa."),
    ("Ahli Muzik", "Gendang Suara Langsing (Tenor Drum)", 25, "Berbaris dengan gendang tenor", "Berbaris berjalan dengan segak membawa gendang dan kayu pemukulnya sewajarnya."),
    ("Ahli Muzik", "Gendang Suara Langsing (Tenor Drum)", 26, "Memalu baik dalam berhenti atau berjalan", "Menunjukkan kebolehan memalu dengan baik dalam masa berhenti atau berjalan."),
    ("Ahli Muzik", "Gendang Suara Langsing (Tenor Drum)", 27, "Berjalan 45 meter, slow time 116 langkah", "Berjalan march sejauh sekurang-kurangnya 45 meter dengan memalu gendang perlahan-lahan (slow time) 116 langkah pada satu minit."),
    ("Ahli Muzik", "Gendang Suara Rendah (Bass Drum)", 28, "Jaga gendang suara rendah", "Menjaga alat muzik ini supaya sentiasa berada dalam keadaan yang baik, bersih dan boleh digunakan bila-bila masa."),
    ("Ahli Muzik", "Gendang Suara Rendah (Bass Drum)", 29, "Berbaris dengan gendang bass", "Berbaris berjalan dengan segak membawa gendang dan kayu pemukulnya sewajarnya."),
    ("Ahli Muzik", "Gendang Suara Rendah (Bass Drum)", 30, "Memalu baik dalam berhenti atau berjalan", "Menunjukkan kebolehan memalu dengan baik dalam masa berhenti atau berjalan."),
    ("Ahli Muzik", "Gendang Suara Rendah (Bass Drum)", 31, "Berjalan 45 meter, 116 langkah", "Berjalan sejauh tidak kurang daripada 45 meter dengan memalu gendang 116 langkah pada satu minit."),
    ("Ahli Muzik", "Gendang Suara Rendah (Bass Drum)", 32, "Berjalan 45 meter, slow time 65 langkah", "Berjalan sejauh sekurang-kurangnya 45 meter dengan memalu gendang perlahan-lahan (slow time) 65 langkah pada satu minit."),
    ("Ahli Muzik", "Bugle atau Trumpet", 33, "Jaga bugle atau trumpet", "Menjaga alat muzik ini supaya sentiasa berada dalam keadaan yang baik, bersih dan boleh digunakan bila-bila masa."),
    ("Ahli Muzik", "Bugle atau Trumpet", 34, "Berjalan membawa bugle", "Berjalan dengan segak membawa bugle atau trumpet di tangan kanan diapit di hadapan pinggang dengan mengayunkan tangan kiri."),
    ("Ahli Muzik", "Bugle atau Trumpet", 35, "Lagu isyarat bugle", "Memainkan lagu Berkumpul (Fall In), Memasak (Cook-House), Padam Lampu (Light Out), Bangun Pagi (Reveille), Hormat (General Salute) dan Matahari Turun atau Undur (Sunset or Retreat)."),
    # Ahli Oseanografi
    ("Ahli Oseanografi", None, 1, "Maksud oseanografi dan 4 bahagian kajian", "Menerangkan maksud oseanografi dan 4 bahagian kajian."),
    ("Ahli Oseanografi", "Pilih SATU kajian: A, B, C atau D", 2, "Kajian hidupan laut", "A: kajian hidupan laut (plankton, jaring plankton) ATAU memerhati hidupan laut dan laporan."),
    ("Ahli Oseanografi", "Pilih SATU kajian: A, B, C atau D", 3, "Kajian air laut", "B: kajian komposisi dan sifat air laut (dua kawasan, laporan 300 patah) ATAU ukur suhu 3-4 kali seminggu, cakera Secchi."),
    ("Ahli Oseanografi", "Pilih SATU kajian: A, B, C atau D", 4, "Kajian ombak, arus dan cuaca", "C: kajian ombak, arus dan cuaca (simulasi ombak, pantulan, biasan) ATAU kajian pasang surut 24 jam."),
    ("Ahli Oseanografi", "Pilih SATU kajian: A, B, C atau D", 5, "Kajian ciri geografi laut", "D: kajian ciri geografi laut (keratan rentas: pentas benua, cerun benua, dataran abbys, gunung dasar laut, rabung lautan dan lain-lain)."),
    # Ahli Penyelamat Nyawa
    ("Ahli Penyelamat Nyawa", None, 1, "Lencana Ahli Renang (prasyarat)", "Telah memperoleh Lencana Ahli Renang."),
    ("Ahli Penyelamat Nyawa", None, 2, "Dua cara menyelamat diri", "Menunjukkan dua cara penyelamatan bagi melepaskan diri pertama di darat dan kedua di dalam air."),
    ("Ahli Penyelamat Nyawa", None, 3, "Chin tow, cross tow, extended tow", "Menunjukkan: (a) chin tow; (b) cross tow; (c) extended tow."),
    ("Ahli Penyelamat Nyawa", None, 4, "Lempar tali penyelamat 10 meter", "Melemparkan tali penyelamat sepanjang 10 meter di antara 2 pancang, jaraknya 1 meter, dengan kejayaan 2 kali daripada 3 kali lemparan."),
    ("Ahli Penyelamat Nyawa", None, 5, "Selamat mangsa dari bahaya", "Menunjukkan cara menyelamatkan mangsa dari rumah terbakar, gas racun, jalan raya dan kena kejutan elektrik."),
    ("Ahli Penyelamat Nyawa", None, 6, "CPR/EAR dengan patung", "Menunjukkan cara pemulihan pernafasan mulut ke mulut (CPR/EAR) dengan patung."),
    # Ahli Perahu Dayung
    ("Ahli Perahu Dayung", None, 1, "Berenang 20 meter berpakaian lengkap", "Berenang 20 meter berpakaian lengkap."),
    ("Ahli Perahu Dayung", None, 2, "Lukis dan nama bahagian perahu", "Melukis dan menamakan semua bahagian perahu."),
    ("Ahli Perahu Dayung", None, 3, "Pengetahuan perahu dayung dan ikatan", "(a) Pengetahuan berhubung perahu dayung dan alatannya; (b) membaiki kerosakan kecil pada perahu dayung; (c) terangkan kegunaan ikatan: Tindih Kasih Air (water bowline), Bunga Geti Berganda (double sheet bend), Ikatan Pengail (fisherman's bend), Lilit Dua Simpul (round turn two half hitches); (d) mengawal hujung tali yang pecah."),
    ("Ahli Perahu Dayung", None, 4, "Langkah keselamatan berdayung", "Pengetahuan tentang langkah keselamatan semasa berdayung."),
    ("Ahli Perahu Dayung", None, 5, "Berdayung seorang diri", "Berdayung seorang diri: (a) ke tembok tinggi, tepi pantai, tebing sungai; (b) berkayuh ke hadapan, belakang dan berpusing."),
    # Ahli Perahu Layar
    ("Ahli Perahu Layar", None, 1, "Beza perahu Optimist, Laser, 420", "Menerangkan perbezaan perahu layar Optimist, Laser dan International 420."),
    ("Ahli Perahu Layar", None, 2, "Sediakan perahu Optimist atau Laser", "Terhadap Optimist atau Laser: (a) sediakan perahu layar; (b) komponen perahu layar; (c) teknik asas pelayaran; (d) latihan keselamatan untuk perahu yang terbalik (capsized)."),
    ("Ahli Perahu Layar", None, 3, "Tonton dan laporkan regatta", "Menonton satu regatta di televisyen dan melaporkan keputusan dan insiden penting."),
    ("Ahli Perahu Layar", None, 4, "Sediakan laporan lengkap", "Menyediakan laporan lengkap."),
    # Ahli Pertahanan Diri
    ("Ahli Pertahanan Diri", None, 1, "Ahli seni mempertahankan diri 6 bulan", "Menjadi ahli seni mempertahankan diri selama 6 bulan (Silat, Kung Fu, Karate, Tae Kwon Do, Judo, Akido, dll.)."),
    ("Ahli Pertahanan Diri", None, 2, "Sejarah seni mempertahankan diri", "Mengetahui sejarah seni mempertahankan diri yang berkenaan."),
    ("Ahli Pertahanan Diri", None, 3, "Prinsip seni mempertahankan diri", "Mengetahui prinsip yang terkandung dalam seni itu."),
    ("Ahli Pertahanan Diri", None, 4, "Kekuda, pergerakan, tangkisan dan serangan", "Mengetahui jenis kekuda, pergerakan asas, jenis tangkisan dan jenis serangan tangan dan kaki."),
    ("Ahli Pertahanan Diri", None, 5, "One-step sparring dan free-sparring", "Menunjukkan cara membuat penyerangan dan menangkis dengan kemahiran (One-Step Sparring dan Free-Sparring)."),
    # Ahli Pertolongan Cemas
    ("Ahli Pertolongan Cemas", None, 1, "Susunan anggota jasmani", "Menerangkan susunan anggota jasmani dan fungsi tiap-tiap satu."),
    ("Ahli Pertolongan Cemas", None, 2, "Urat nadi dan henti pendarahan", "Mengetahui kedudukan urat nadi dan tahu bagaimana memberhentikan keluaran darah."),
    ("Ahli Pertolongan Cemas", None, 3, "Pulihkan orang terkejut", "Menunjukkan cara memulihkan seorang yang terkejut (shock), termasuk yang terkena kejutan elektrik."),
    ("Ahli Pertolongan Cemas", None, 4, "Balutan tiga segi", "Menggunakan balutan tiga segi pada luka di kepala, tangan, kaki, lutut dan siku."),
    ("Ahli Pertolongan Cemas", None, 5, "Tulang selangka patah", "Menunjukkan cara mengendalikan tulang selangka patah dan cara menjaga supaya yang patah tidak disyaki patah."),
    ("Ahli Pertolongan Cemas", None, 6, "Pemulihan pernafasan CPR/EAR", "Menunjukkan cara pemulihan pernafasan (CPR/EAR)."),
    ("Ahli Pertolongan Cemas", None, 7, "Hantar berita kecemasan", "Menunjukkan cara menghantar berita kecemasan dengan betul secara lisan, bertulis dan telefon."),
    # Ahli Renang
    ("Ahli Renang", None, 1, "Berenang 100 meter", "Berenang 100 meter dengan sebarang cara atau gaya."),
    ("Ahli Renang", None, 2, "Berenang dua cara", "Berenang dengan 2 cara dipilih: front crawl 50m; back crawl 50m; breast stroke 50m; butterfly 50m."),
    ("Ahli Renang", None, 3, "Terjun ke air", "Terjun ke permukaan air dari tepi kolam atau tempat renang."),
    ("Ahli Renang", None, 4, "Berenang di air cetek", "Berenang di air cetek 25m berpakaian ringan; berjalan di air 1 minit; tanggalkan pakaian dalam air."),
    ("Ahli Renang", None, 5, "Menyelamat orang lemas", "Berenang 25m ke arah orang lemas, bawa ke tepi dengan cara menyelamat; tunjuk pemulihan pernafasan."),
    ("Ahli Renang", None, 6, "Menyelam 2 meter", "Menyelam 2 meter dan ambil satu benda dengan kedua-dua tangan."),
    # Ahli Snorkel
    ("Ahli Snorkel", None, 1, "Terangkan peralatan snorkel", "Menerangkan peralatan yang diperlukan untuk snorkel."),
    ("Ahli Snorkel", None, 2, "Terangkan langkah keselamatan snorkel", "Menghuraikan langkah keselamatan snorkel di kawasan tertutup atau laut lepas."),
    ("Ahli Snorkel", None, 3, "Snorkel 3 kali di lokasi berlainan", "Melakukan snorkel dengan jayanya sekurang-kurangnya 3 kali di lokasi berlainan."),
    ("Ahli Snorkel", None, 4, "Kaji lokasi strategik snorkel", "Membuat kajian ringkas tentang lokasi strategik untuk snorkel dengan kelebihan lokasi tersebut."),
    ("Ahli Snorkel", None, 5, "Aktiviti tambahan mengikut arahan Penguji", "Melakukan aktiviti tambahan mengikut arahan Penguji (mengumpul cengkerang, foto, bersihkan pantai)."),
    ("Ahli Snorkel", None, 6, "Tulis laporan lengkap", "Menulis laporan lengkap tentang aktiviti yang dijalankan."),
    # Ahli Survival Laut
    ("Ahli Survival Laut", None, 1, "Terangkan rakit penyelamat", "Menerangkan rakit penyelamat (life raft) dan komponennya."),
    ("Ahli Survival Laut", None, 2, "Posisi terapung di laut", "Mengetahui posisi yang sesuai ketika terapung di laut."),
    ("Ahli Survival Laut", None, 3, "Air tawar dan tangkap ikan", "Mengetahui cara mendapatkan air tawar dan menangkap ikan secara survival."),
    ("Ahli Survival Laut", None, 4, "Elak hypothermia, sun burn, isyarat", "Menerangkan cara mengelakkan hypothermia, sun burn dan isyarat kecemasan."),
    ("Ahli Survival Laut", None, 5, "Isyarat kecemasan siang dan malam", "Menghuraikan isyarat kecemasan waktu siang, malam, di tepi pantai dan tengah laut."),
    # Eksplorasi Marin
    ("Eksplorasi Marin", None, 1, "Tonton satu filem kelautan", "Menonton SATU filem tentang aspek kelautan (contoh: Master and Commander, Cast Away)."),
    ("Eksplorasi Marin", None, 2, "Guna satu simulator kapal", "Menggunakan SATU simulator komputer untuk pengendalian kapal (contoh: Ship Simulator, Virtual Skipper, Sail Simulator)."),
    ("Eksplorasi Marin", None, 3, "Tonton satu dokumentari kepelautan", "Menonton SATU dokumentari berkaitan kepelautan (contoh: Man Vs. Wild, National Geographic)."),
    ("Eksplorasi Marin", None, 4, "Tulis laporan dan bentang", "Menulis laporan penuh dengan sinopsis dan ilmu yang diperoleh; hasil dibentangkan kepada Penguji."),
    # Juru Masak di Khemah
    ("Juru Masak di Khemah", None, 1, "Masak dua jenis makanan tanpa perkakas dapur", "Memasak DUA jenis makanan dengan tidak menggunakan perkakas dapur, untuk diri sendiri dan seorang lagi."),
    ("Juru Masak di Khemah", "Pilih SATU: ikan panggang, roti berlauk atau bubur", 2, "Ikan panggang", "Memasak dan menghidangkan dengan sempurna SATU daripada: ikan panggang."),
    ("Juru Masak di Khemah", "Pilih SATU: ikan panggang, roti berlauk atau bubur", 3, "Roti berlauk", "Memasak dan menghidangkan dengan sempurna SATU daripada: roti berlauk."),
    ("Juru Masak di Khemah", "Pilih SATU: ikan panggang, roti berlauk atau bubur", 4, "Bubur", "Memasak dan menghidangkan dengan sempurna SATU daripada: bubur."),
    ("Juru Masak di Khemah", "Pilih SATU: mee, ayam atau masakan biasa", 5, "Mee rebus atau goreng", "Memasak dan menghidangkan dengan sempurna SATU daripada: mee rebus atau goreng."),
    ("Juru Masak di Khemah", "Pilih SATU: mee, ayam atau masakan biasa", 6, "Ayam atau daging masak panggang atau salai", "Memasak dan menghidangkan dengan sempurna SATU daripada: ayam atau daging masak panggang atau salai."),
    ("Juru Masak di Khemah", "Pilih SATU: mee, ayam atau masakan biasa", 7, "Masakan biasa", "Memasak dan menghidangkan dengan sempurna SATU daripada: masakan biasa."),
    ("Juru Masak di Khemah", "Pilih SATU makanan manis", 8, "Sejenis makanan manis", "Memasak dan menghidangkan dengan sempurna SATU daripada: sejenis makanan manis."),
    ("Juru Masak di Khemah", "Pilih SATU makanan manis", 9, "Halua buah-buahan", "Memasak dan menghidangkan dengan sempurna SATU daripada: halua buah-buahan."),
    ("Juru Masak di Khemah", "Pilih SATU makanan manis", 10, "Gula-gula manisan", "Memasak dan menghidangkan dengan sempurna SATU daripada: gula-gula manisan."),
    ("Juru Masak di Khemah", "Pilih SATU makanan manis", 11, "Lengkong", "Memasak dan menghidangkan dengan sempurna SATU daripada: lengkong."),
    ("Juru Masak di Khemah", "Pilih SATU makanan manis", 12, "Manis-manisan pilihan sendiri", "Memasak dan menghidangkan dengan sempurna SATU daripada: manis-manisan yang disediakan atas pilihan sendiri."),
    ("Juru Masak di Khemah", None, 13, "Menyediakan dua jenis menu untuk patrol 6 orang", "Menyediakan DUA jenis menu dengan sukatan sekali untuk satu patrol seramai 6 orang; tidak semuanya makanan itu perlu dimasak. Ingatan: semua hidangan hendaklah dimasak dalam keadaan berkhemah."),
    # Koordinator Pameran Pengakap Laut
    ("Koordinator Pameran Pengakap Laut", None, 1, "Koordinator dua pameran", "Menjadi koordinator dalam DUA pameran Pengakap Laut."),
    ("Koordinator Pameran Pengakap Laut", "Pilih sekurang-kurangnya 7 daripada 11 aspek", 2, "Aspek: sejarah Pengakap Laut", "Sejarah Pengakap Laut dipamerkan."),
    ("Koordinator Pameran Pengakap Laut", "Pilih sekurang-kurangnya 7 daripada 11 aspek", 3, "Aspek: pakaian seragam", "Pakaian seragam dipamerkan."),
    ("Koordinator Pameran Pengakap Laut", "Pilih sekurang-kurangnya 7 daripada 11 aspek", 4, "Aspek: komunikasi marin", "Komunikasi marin dipamerkan."),
    ("Koordinator Pameran Pengakap Laut", "Pilih sekurang-kurangnya 7 daripada 11 aspek", 5, "Aspek: simpulan dan ikatan", "Simpulan dan ikatan dipamerkan."),
    ("Koordinator Pameran Pengakap Laut", "Pilih sekurang-kurangnya 7 daripada 11 aspek", 6, "Aspek: survival di laut", "Survival di laut dipamerkan."),
    ("Koordinator Pameran Pengakap Laut", "Pilih sekurang-kurangnya 7 daripada 11 aspek", 7, "Aspek: jenis ikan", "Jenis ikan dipamerkan."),
    ("Koordinator Pameran Pengakap Laut", "Pilih sekurang-kurangnya 7 daripada 11 aspek", 8, "Aspek: alatan navigasi", "Alatan navigasi dipamerkan."),
    ("Koordinator Pameran Pengakap Laut", "Pilih sekurang-kurangnya 7 daripada 11 aspek", 9, "Aspek: ilmu kaji cuaca", "Ilmu kaji cuaca dipamerkan."),
    ("Koordinator Pameran Pengakap Laut", "Pilih sekurang-kurangnya 7 daripada 11 aspek", 10, "Aspek: ilmu penyelamat nyawa", "Ilmu penyelamat nyawa dipamerkan."),
    ("Koordinator Pameran Pengakap Laut", "Pilih sekurang-kurangnya 7 daripada 11 aspek", 11, "Aspek: istiadat maritim", "Istiadat maritim dipamerkan."),
    ("Koordinator Pameran Pengakap Laut", "Pilih sekurang-kurangnya 7 daripada 11 aspek", 12, "Aspek: ilmu pelayaran dan kelautan", "Ilmu pelayaran dan kelautan dipamerkan."),
    ("Koordinator Pameran Pengakap Laut", None, 13, "Tulis laporan lengkap", "Menulis laporan lengkap."),
    # Kuartermaster
    ("Kuartermaster", "Kumpulan ujian A (1-6)", 1, "Bantu Kuartermaster 6 bulan; tali-menali", "Telah membantu Kuartermaster pasukan dengan baiknya selama enam bulan. Cara menjaga tali-menali: membuat pemecut, mematikan hujung tali, menganyam, memintal, melingkar, memeriksa dan menyimpannya."),
    ("Kuartermaster", "Kumpulan ujian A (1-6)", 2, "Khemah dan alatan", "b) Cara menjaga khemah: memperbaiki tali penarik, menampal atau menjahit koyak kecil, mengalis supaya tahan hujan, memeriksa dan menyimpannya. c) Cara menjaga alatan: mengasah, membersihkan, memeriksa dan menyimpannya."),
    ("Kuartermaster", "Kumpulan ujian A (1-6)", 3, "Rekod keluar dan masuk alatan", "Cara menyimpan rekod yang mudah dan berkesan termasuk catatan keluar dan masuk segala alatan Kumpulan."),
    ("Kuartermaster", "Kumpulan ujian A (1-6)", 4, "Simpan alatan dengan kod", "a) Cara menyimpan alatan kegunaan Pengakap. b) Cara menyimpan dengan sistem warna, nombor atau kod berkenaan dengan barang pekerjaan tangan."),
    ("Kuartermaster", "Kumpulan ujian A (1-6)", 5, "Jaga alatan pandang dengar", "Cara menjaga dan menyimpan alatan pandang dengar Kumpulan seperti model, carta dinding, bahan lukisan, kertas lukisan."),
    ("Kuartermaster", "Kumpulan ujian A (1-6)", 6, "Nilai barang dan harga", "Cara menilai barang dan harga barang yang hendak dibeli."),
    ("Kuartermaster", "Kumpulan ujian B (7-14)", 7, "Bantu Kuartermaster dalam perkhemahan", "Telah membantu Kuartermaster dalam satu perkhemahan Pasukan Pengakap atau PEK bercuti Pengakap Kanak-Kanak dengan baiknya selama lima hari."),
    ("Kuartermaster", "Kumpulan ujian B (7-14)", 8, "Jaga semua alatan perkhemahan", "Cara menjaga semua alatan perkhemahan: (a) tali-menali: menggulung, memeriksa dan menyimpan; (b) khemah: memperbaiki tali penarik, menjahit khemah terkoyak dengan segera, memeriksa khemah; (c) alatan: mengasah, membersih, memeriksa, menyimpan; (d) alatan masak: membersih, memeriksa, menyimpan."),
    ("Kuartermaster", "Kumpulan ujian B (7-14)", 9, "Rekod alatan dalam perkhemahan", "Cara menyimpan rekod yang mudah dan berkesan termasuk catatan keluar dan masuk alatan dalam perkhemahan."),
    ("Kuartermaster", "Kumpulan ujian B (7-14)", 10, "Jaga alat khas perkhemahan", "Cara menjaga semua alat khas dalam perkhemahan: pakaian seragam, alatan mengembara, alatan mendaki bukit atau gunung dan perahu."),
    ("Kuartermaster", "Kumpulan ujian B (7-14)", 11, "Daftar makanan 48 jam", "Menunjukkan satu daftar makanan dalam perkhemahan selama 48 jam dan membincangkannya dengan penilai."),
    ("Kuartermaster", "Kumpulan ujian B (7-14)", 12, "Penyimpanan barang makanan", "Menerangkan cara mengendalikan penyimpanan barang makanan dalam perkhemahan."),
    ("Kuartermaster", "Kumpulan ujian B (7-14)", 13, "Senarai alatan dan pembaikan segera", "Menunjukkan satu senarai alatan yang perlu dibawa bagi satu perkhemahan dan cara memperbaiki alatan dengan segera dalam kecemasan. Buktikan sebab tiap alat dibawa."),
    ("Kuartermaster", "Kumpulan ujian B (7-14)", 14, "Kebersihan dalam perkhemahan", "Mengetahui kebersihan sebagai kunci kejayaan Kuartermaster. Menerangkan cara mencapainya dalam urusan perkhemahan sebagai pembantu KM."),
    # Lencana Ahli Bot
    ("Lencana Ahli Bot", None, 1, "Latihan terapung dengan jaket keselamatan atau pelampung", "Menyertai latihan terapung dengan jaket keselamatan atau pelampung selama 15 minit."),
    ("Lencana Ahli Bot", None, 2, "Sejarah ringkas Pengakap Laut Sedunia", None),
    ("Lencana Ahli Bot", None, 3, "Lilit dua simpul di tombol bot dan tarik tali penyelamat", "Membuat lilit dua simpul di tombol bot (thwart) dan tahu menarik tali penyelamat dari bot."),
    ("Lencana Ahli Bot", None, 4, "Sauh, sambung dua tali dan lilit pemati kejap", "Menyediakan sauh, menyambung dua tali dan menyirat lilit pemati kejap (rolling hitch)."),
    ("Lencana Ahli Bot", None, 5, "Unsur tiupan angin, pasang surut dan arus", "Menerangkan unsur tiupan angin, air pasang surut, pergerakan arus; mengenali carta pasang surut yang dikeluarkan oleh TLDM."),
    ("Lencana Ahli Bot", None, 6, "Tanggungjawab setiap krew dalam pelayaran", None),
    ("Lencana Ahli Bot", None, 7, "Wisel Boatswain", "Menunjukkan cara meniup wisel Boatswain bagi isyarat Still, Carry-On, General Call dan Pipe the Side."),
    ("Lencana Ahli Bot", None, 8, "Asas komunikasi laut", "Abjad fonetik, kod morse, semaphore dan abjad yang sering digunakan di kapal."),
    ("Lencana Ahli Bot", None, 9, "Asas bot enjin sangkut (OBM)", "Mengendalikan bot dengan enjin sangkut (OBM) berukuran sekurang-kurangnya 10 kaki dan 5 kuasa kuda, serta menguruskan kebocoran kecil pada bot dengan bahan yang bersesuaian."),
    ("Lencana Ahli Bot", None, 10, "Simbol-simbol Carta Laut", None),
    ("Lencana Ahli Bot", None, 11, "Cara menyelamat secara berpasukan", "Secara berpasukan (minimum 2 orang) dengan pelempar live buoy dan seorang perenang."),
    # Lencana Jaya
    ("Lencana Jaya", None, 1, "Organisasi Ibu Pejabat, Biro Pengakap Sedunia dan Biro Wilayah Asia Pasifik", None),
    ("Lencana Jaya", None, 2, "Sejarah tertubuhnya Malaysia", None),
    ("Lencana Jaya", None, 3, "Jata Negara dan Lambang Negeri", None),
    ("Lencana Jaya", None, 4, "Tugas kerja Dewan Undangan Negeri", None),
    ("Lencana Jaya", None, 5, "Ketua Pengakap Negara dan Ketua Pesuruhjaya Pengakap Negara", None),
    ("Lencana Jaya", None, 6, "Latihan asas perbarisan", None),
    ("Lencana Jaya", None, 7, "Kawat tongkat semasa berjalan", None),
    ("Lencana Jaya", None, 8, "Halangan komando", None),
    ("Lencana Jaya", None, 9, "Menghadiri Kursus Ketua Patrol atau melatih 2 orang untuk Lencana Maju", None),
    ("Lencana Jaya", None, 10, "Kebolehan kepimpinan", "Merancang dan menjalankan pengembaraan; merancang Malam Pengakap; menjalankan Mesyuarat Ketua Patrol."),
    ("Lencana Jaya", None, 11, "Membawa bendera", None),
    ("Lencana Jaya", "Kejayaan: lakukan SATU kemahiran", 12, "Kumpulan I: Cabaran", "Mendayung perahu atau melayarkan sampan layar; mendaki bukit; pengembaraan malam 8 jam."),
    ("Lencana Jaya", "Kejayaan: lakukan SATU kemahiran", 13, "Kumpulan II: Amali", "Pekerjaan tangan atau tukang gambar; mekanik; kod fonetik antarabangsa; khidmat masyarakat."),
    ("Lencana Jaya", "Kejayaan: lakukan SATU kemahiran", 14, "Kumpulan III: Kesungguhan", "Pengembaraan 24 km atau 50 km berbasikal; gimnastik atau seni mempertahankan diri; bekalan makanan kering; satu kegiatan luar (memanah, memancing, kajian barang purba, kajian isi bumi, pemeliharaan alam sekitar)."),
    ("Lencana Jaya", "Kejayaan: lakukan SATU kemahiran", 15, "Kumpulan IV: Masyarakat", "1) Menyedia, memasak dan melayan; 2) Pertunjukkan hiburan amatur; 3) Perkhidmatan dan menjalankan Malam Pengakap."),
    ("Lencana Jaya", "Kejayaan: lakukan SATU kemahiran", 16, "Kumpulan V: Kemahiran Berpengakap", "Simpulan dan ikatan (Abah-Abah (manharness knot), Rolling Hitch, Middleman's Knot, Water Bowline, Fisherman's Knot, Eye Splice, Floor/Snake Lashing, Tripod/Figure-8 Lashing); mendirikan pondok sementara; projek perintis."),
    ("Lencana Jaya", None, 17, "Rawatan dan pertolongan cemas", "Rawatan patah tulang; usungan pesakit."),
    ("Lencana Jaya", None, 18, "Kegunaan kayu tuap", None),
    ("Lencana Jaya", None, 19, "Sistem pemulihan pernafasan mulut ke mulut", None),
    ("Lencana Jaya", None, 20, "Perkhidmatan 6 jam", None),
    # Lencana Juragan
    ("Lencana Juragan", None, 1, "Compass Head dan Navigation Light", "Boleh membaca Compass Head dan Navigation Light, serta menentukan sesuatu perairan tempatan berdasarkan carta laut."),
    ("Lencana Juragan", None, 2, "Beaufort wind and sea scales", "Membincangkan Beaufort wind and sea scales, dan mengetahui sekurang-kurangnya dua tanda keadaan cuaca, sama ada dalam keadaan baik atau buruk di kawasan perairan tempatan."),
    ("Lencana Juragan", None, 3, "Jenis pengangkutan di laut", "Mengenali jenis pengangkutan di laut (seagoing vessels) dan fungsi setiap kelas kapal komersil."),
    ("Lencana Juragan", None, 4, "Lampu isyarat kapal", "Mengenali lampu-lampu isyarat kapal dan kedudukannya."),
    ("Lencana Juragan", None, 5, "Bendera abjad INTERCO", "Mengetahui dan menerangkan maksud bendera abjad berdasarkan International Code of Signals (INTERCO)."),
    ("Lencana Juragan", None, 6, "Operasi menyelamat", "Merancang operasi menyelamat termasuk peralatan dan tugas krew bagi setiap operasi."),
    ("Lencana Juragan", None, 7, "Menyelamat dengan kayak", "Mengendalikan kayak dengan cekap dan menunjukkan cara menyelamat menggunakan X-Rescue, H-Rescue dan T-Rescue."),
    ("Lencana Juragan", None, 8, "Anyaman dan kemasan tali jut", "Lilit pemati selit, simpul kepala lalat, sambat balik, sambat mata dan sambat pendek."),
    ("Lencana Juragan", None, 9, "Man overboard", "Latihan menunjuk cara menyelamatkan orang yang jatuh ke dalam air (man overboard) menggunakan pelampung dan seumpamanya dari daratan atau dari bot."),
    ("Lencana Juragan", None, 10, "Menyelamatkan diri semasa kecemasan di dalam air", None),
    ("Lencana Juragan", None, 11, "Patrol dan perjalanan air", "Menguruskan satu patrol sekurang-kurangnya tujuh orang untuk perjalanan di air sejauh 5 km (kenderaan sendiri) atau 10 km (kenderaan air awam), termasuk membuat persediaan dan persiapan menentukan keselamatan ahli-ahli serta kenderaan airnya dalam semua keadaan."),
    # Lencana Juragan Muda
    ("Lencana Juragan Muda", None, 1, "Undang-Undang Antarabangsa untuk Mengelakkan Pelanggaran di Laut 1972", "Memahami Bahagian B (Peraturan 4 hingga 19)."),
    ("Lencana Juragan Muda", None, 2, "Asas ilmu kaji cuaca", "Jenis awan, penggunaan barometer, jangka suhu dan tolok hujan serta kegunaannya."),
    ("Lencana Juragan Muda", None, 3, "Isyarat perairan tempatan", "Tahu dan boleh menunjukkan cara membaca isyarat perairan tempatan."),
    ("Lencana Juragan Muda", None, 4, "Peralatan bot", "Menyediakan peralatan bot dan boleh menamakan alatan tersebut."),
    ("Lencana Juragan Muda", None, 5, "Tali buangan (heaving line)", "Tahu membuat dan menyediakan tali buangan."),
    ("Lencana Juragan Muda", None, 6, "Simpulan dan ikatan pelayaran", "Simpul manuk (clove hitch), simpul tindih kasih (bowline), lilit kejap (rolling hitch), Midshipman hitch dan simpul penahan (stopper knot)."),
    ("Lencana Juragan Muda", None, 7, "Ekspedisi memancing", "Mengikuti satu ekspedisi memancing 2 hari 1 malam di bawah pengawasan orang dewasa dengan menyimpan rekod dan gambar ke dalam buku log."),
    ("Lencana Juragan Muda", None, 8, "Latihan bot atau ekspedisi mini kayak", "Mendapatkan pengalaman bot atau ekspedisi mini kayak semasa latihan atau perkhemahan."),
    ("Lencana Juragan Muda", None, 9, "Teknik asas pelayaran perahu layar", "Running, reaching, tacking dan gybing, serta kegunaan kompas."),
    ("Lencana Juragan Muda", None, 10, "Rakit daripada buluh", "Membuat rakit daripada buluh atau kombinasi buluh dan tiub pelampung, tidak lebih 4 orang."),
    # Lencana Keahlian
    ("Lencana Keahlian", None, 1, "Peraturan pakaian seragam Pengakap", None),
    ("Lencana Keahlian", None, 2, "Prinsip Rukun Negara", None),
    ("Lencana Keahlian", None, 3, "Lambang Pengakap Malaysia dan Lambang Pengakap Sedunia", None),
    ("Lencana Keahlian", None, 4, "Persetiaan Pengakap dan Undang-Undang Pengakap", None),
    ("Lencana Keahlian", None, 5, "Hormat Pengakap dan Cogankata Pengakap", None),
    ("Lencana Keahlian", None, 6, "Sejarah Pengakap Malaysia dan Sejarah Lord Baden Powell", None),
    ("Lencana Keahlian", None, 7, "Simpulan dan ikatan", "Simpulan dan ikatan: Buku Sila (reef knot), Bunga Geti (sheet bend), Simpul Manuk (clove hitch), Tindih Kasih (bowline), Lilit Dua Simpul (round turn and two half hitches), Lilit Pemati Biasa (common whipping)."),
    # Lencana Maju
    ("Lencana Maju", None, 1, "Organisasi kumpulan, PPM daerah dan PPM negeri", None),
    ("Lencana Maju", None, 2, "Melukis bendera semua negeri di Malaysia", None),
    ("Lencana Maju", None, 3, "Nama penuh Ketua Pesuruhjaya Negeri, Pesuruhjaya Daerah dan Penolong Pesuruhjaya Daerah", None),
    ("Lencana Maju", None, 4, "Undang-Undang Pengakap", None),
    ("Lencana Maju", None, 5, "Latihan asas perbarisan", None),
    ("Lencana Maju", None, 6, "Kawat tongkat", None),
    ("Lencana Maju", None, 7, "Upacara mengibarkan dan menurunkan bendera", None),
    ("Lencana Maju", None, 8, "Memanjat tali atau pokok setinggi 5 meter", None),
    ("Lencana Maju", None, 9, "Menjaga, mengasah dan menyimpan kapak dan gergaji", None),
    ("Lencana Maju", None, 10, "Teknik menggunakan kapak", None),
    ("Lencana Maju", None, 11, "Simpulan dan ikatan", "Tindih Kasih Ganda, Belit Lucut, Lilit Pasdul, Simpul Kerusi, Lilit Pemati Selit, Simpul Kepala Lalat, Sambat Balik, Ikat Silang Gunting."),
    ("Lencana Maju", None, 12, "Memasak makanan rimba (backwoods)", "Menghidupkan api; Roti Liat; Ikan."),
    ("Lencana Maju", None, 13, "Model projek perintis", None),
    ("Lencana Maju", None, 14, "Kajian", "Kajian 1 perkara: burung, binatang dan pokok tempatan; lawatan bangunan atau kawasan penting; kawasan tempatan."),
    ("Lencana Maju", None, 15, "Berkhemah sekurang-kurangnya 8 malam", None),
    ("Lencana Maju", None, 16, "Langkah keselamatan berenang", None),
    ("Lencana Maju", None, 17, "Langkah keselamatan kegiatan kerja luar", None),
    ("Lencana Maju", "Melakukan DUA perkara", 18, "Dapur gas, lampu gas atau dapur minyak tanah", None),
    ("Lencana Maju", "Melakukan DUA perkara", 19, "Keperluan berkhemah", None),
    ("Lencana Maju", "Melakukan DUA perkara", 20, "Memasak untuk 2 orang", None),
    ("Lencana Maju", None, 21, "Jenis kompas dan membaca bearing", None),
    ("Lencana Maju", None, 22, "Sistem kontur, rujukan grid, skil dan kunci peta", None),
    ("Lencana Maju", None, 23, "Mengembara 16 km berjalan kaki", "Mengembara 16 km berjalan kaki dalam patrol dan bermalam di luar dengan mendirikan khemah. Menyediakan laporan bertulis dalam Buku log."),
    ("Lencana Maju", None, 24, "Ikhtiar hidup", None),
    ("Lencana Maju", None, 25, "Balutan: kepala, lutut dan lengan", None),
    ("Lencana Maju", None, 26, "Tindakan kecemasan", None),
    ("Lencana Maju", None, 27, "Memanggil Polis, Bomba dan Ambulan", None),
    ("Lencana Maju", None, 28, "Khidmat sukarela", None),
    # Lencana Usaha
    ("Lencana Usaha", None, 1, "Bendera Malaysia dan Bendera Negeri masing-masing", None),
    ("Lencana Usaha", None, 2, "Lagu Negaraku dan lagu negeri masing-masing", None),
    ("Lencana Usaha", None, 3, "Menaikkan bendera", None),
    ("Lencana Usaha", None, 4, "Orang-orang kenamaan", "Nama penuh DYMM Sultan/Raja, TYT Yang Dipertua Negeri, Menteri Besar dan Ketua Menteri."),
    ("Lencana Usaha", None, 5, "Persetiaan Pengakap dan Undang-Undang Pengakap", None),
    ("Lencana Usaha", None, 6, "Asas perbarisan", None),
    ("Lencana Usaha", None, 7, "Kawat tongkat", None),
    ("Lencana Usaha", None, 8, "Isyarat-isyarat tangan Pengakap", None),
    ("Lencana Usaha", None, 9, "Halangan komando", None),
    ("Lencana Usaha", None, 10, "Melipat dan mengibarkan bendera", None),
    ("Lencana Usaha", None, 11, "Menjaga dan menyimpan pisau serta parang", None),
    ("Lencana Usaha", None, 12, "Simpulan dan ikatan", "Simpul Himpit (fisherman's knot), Simpul Pulih (sheep shank knot), Bunga Geti Ganda (double sheet bend), Lilit Balak (timber hitch), Lilit Taut (taut line), Ikat Seraya (square lashing), Ikat Serong (diagonal lashing)."),
    ("Lencana Usaha", None, 13, "Undang-undang lalu lintas jalan raya", None),
    ("Lencana Usaha", None, 14, "Memilih tapak perkhemahan", None),
    ("Lencana Usaha", None, 15, "Keperluan peribadi untuk berkhemah", None),
    ("Lencana Usaha", None, 16, "Alatan pertolongan cemas peribadi", None),
    ("Lencana Usaha", None, 17, "Menghidupkan api", None),
    ("Lencana Usaha", None, 18, "Berkhemah sekurang-kurangnya 1 malam", None),
    ("Lencana Usaha", None, 19, "Arah mata angin dan mengenali peta topo", None),
    ("Lencana Usaha", None, 20, "Isyarat sulit Pengakap", None),
    ("Lencana Usaha", None, 21, "Mengembara sejauh 8 km berjalan kaki dalam patrol", "Mengembara sejauh 8 km berjalan kaki dalam patrolnya, dan membuat laporan bertulis dalam buku log."),
    ("Lencana Usaha", None, 22, "Kraftangan", None),
    ("Lencana Usaha", None, 23, "Plaster cast", None),
    ("Lencana Usaha", None, 24, "Rekod 12 orang sahabat pena", None),
    ("Lencana Usaha", None, 25, "Balutan anduh", "Melipat kain anduh; anduh tangan dan kaki."),
    ("Lencana Usaha", None, 26, "Tindakan kecemasan", None),
    ("Lencana Usaha", None, 27, "Memandu orang", None),
    # Pengail Muda
    ("Pengail Muda", None, 1, "Peraturan keselamatan air", "Mengetahui peraturan keselamatan dalam air, bahaya air dan tindakan sebelum mengharunginya."),
    ("Pengail Muda", None, 2, "Mengail 6 kali", "Mengail di air tawar atau masin sekurang-kurangnya 6 kali dalam tempoh 3 bulan; rekod ikan, jenis, ukuran, berat, umpan, cuaca."),
    ("Pengail Muda", None, 3, "Mengenali 12 jenis ikan", "(a) Mengenali 12 jenis ikan tempatan yang direkodkan; (b) pengetahuan arah lubuk, umpan dan saiz mata kail dan batu ladung."),
    ("Pengail Muda", "Lempar atau labuh mata kail: pilih SATU", 4, "Lempar mata kail 6 kali", "Melempar mata kail 6 kali berturut-turut sejauh tidak kurang 5 meter."),
    ("Pengail Muda", "Lempar atau labuh mata kail: pilih SATU", 5, "Labuh mata kail dengan batu ladung", "Melabuhkan mata kail dengan batu ladung ke dalam air sedalam lebih kurang 1 meter."),
    ("Pengail Muda", None, 6, "Mengenali 6 jenis alat mengail", "Mengenali sekurang-kurangnya 6 jenis alat mengail (joran, batu ladung, takal, tali kail, mata kail dll.)."),
    # Peladang Muda
    ("Peladang Muda", "Kumpulan A (pusat ternakan)", 1, "Pengurusan pusat ternakan luar bandar", "Mengetahui cara pengurusan suatu pusat ternakan di kawasan luar bandar atau desa."),
    ("Peladang Muda", "Kumpulan A (pusat ternakan)", 2, "Perubahan pusat ternakan dan latihan praktik", "Menunjukkan cara pengelolaan harian bagi sesuatu pusat ternakan. Menghuraikan kepada Penilai perubahan yang berlaku di pusat ternakan di kawasan serta beri sebab perubahan itu dibuat. Melakukan latihan praktik di suatu pusat ternakan yang baru ditubuhkan."),
    ("Peladang Muda", "Kumpulan A (pusat ternakan)", 3, "12 gambar dan 8 kerja musim", "Mengadakan 12 keping gambar yang diambil sendiri di pusat ternakan pilihannya dengan menunjukkan sekurang-kurangnya 8 jenis kerja musim dalam sebulan serta memberi keterangan ringkas mengenai gambar-gambar itu."),
    ("Peladang Muda", "Kumpulan B (kebun)", 4, "Tanam kebun 11 meter persegi selama setahun", "Menanam dengan jayanya di suatu kawasan seluas sekurang-kurangnya 11 meter persegi, selama setahun 3 jenis pokok bunga yang tahan lama, 3 jenis sayuran, 3 jenis pokok bebawang, rumput-rumpai atau pokok ros (sebagai pilihan 8 jenis sayuran boleh ditanam). Ingatan: Penilai hendaklah melawat kebun itu sekurang-kurangnya 4 kali dalam tempoh setahun."),
    ("Peladang Muda", "Kumpulan B (kebun)", 5, "Terangkan kerja kebun dan hasil", "Menerangkan kepada Penilai berbagai kerja yang telah dijalankan dalam kebun itu dan hasil yang diperoleh."),
    ("Peladang Muda", "Kumpulan D (akuarium)", 6, "Akuarium air tawar dengan 3 jenis ikan", "Mengadakan sebuah akuarium air tawar, lengkap dengan rumput-rumpainya, yang mengandungi sekurang-kurangnya 3 jenis ikan."),
    ("Peladang Muda", "Kumpulan D (akuarium)", 7, "Cara jaga akuarium sepanjang tahun", "Menerangkan kepada Penilai cara menjaga akuarium itu sepanjang tahun khasnya tentang masalah yang terdapat."),
    ("Peladang Muda", "Kumpulan C: asas (ujian 1 dan 2)", 8, "Tabiat dan kandang binatang kecil", "Bagi binatang kecil seperti anjing, kucing, arnab, tikus, kura-kura dan seumpamanya, mengerti tentang tabiat, kelakuan binatang itu dan cara memberi makan dan menyediakan kandang atau sangkarnya."),
    ("Peladang Muda", "Kumpulan C: asas (ujian 1 dan 2)", 9, "Makan, kandang dan kegunaan ternakan", "Bagi binatang ternakan seperti kuda, lembu, kambing atau kambing biri-biri, mengerti tentang memberi makan, menyediakan kandangnya, tabiat dan kelakuan serta kegunaan binatang itu dari segi ekonomi (seperti menjual susunya) dan pengangkutan."),
    ("Peladang Muda", "Kumpulan C: unggas (ujian 3)", 10, "Burung belaan bersangkar", "Jika binatang itu unggas: burung belaan bersangkar, mengetahui menjaganya."),
    ("Peladang Muda", "Kumpulan C: unggas (ujian 3)", 11, "Burung yang boleh dimakan", "Jika binatang itu unggas: burung yang boleh dimakan seperti ayam, punai atau merpati, mengetahui menjaganya."),
    # Pelukis
    ("Pelukis", None, 1, "Lukis pemandangan dari cerita", "Melukis satu pemandangan dari sebuah cerita yang dipilih oleh Penilai."),
    ("Pelukis", None, 2, "Lukis wajah bengis, senyum atau sedih", "Melukis rupa seorang manusia yang wajahnya bengis, tersenyum atau sedih."),
    ("Pelukis", None, 3, "Lukis pemandangan alam dan warna", "Melukis satu pemandangan keindahan alam semulajadi, dan mengetahui kaedah mewarna di atas pelbagai jenis objek."),
    ("Pelukis", None, 4, "Poster simpulan dan ikatan", "Melukis poster gambar simpulan dan ikatan yang telah dipelajarinya."),
    ("Pelukis", None, 5, "Layout perkhemahan ideal", "Melukis gambar perkhemahan (layout) yang ideal."),
    ("Pelukis", None, 6, "Tiga gejet penting perkhemahan", "Melukis sekurang-kurangnya tiga gejet yang penting dalam perkhemahan."),
    ("Pelukis", None, 7, "Lambang Pengakap pada bahan", "Melukis lambang Pengakap pada apa-apa bahan seperti kadbod, papan lapis, polystyrene dan sebagainya."),
    ("Pelukis", None, 8, "Kumpul lukisan dari akhbar dan majalah", "Mengumpul berbagai lukisan dari keratan akhbar dan majalah untuk dijadikan rujukan dan panduan."),
    # Pembantu Regatta
    ("Pembantu Regatta", None, 1, "Pembantu pertandingan pelayaran 24 jam", "Menjadi pembantu dalam satu pertandingan pelayaran atau sukan air selama tidak kurang 24 jam."),
    # Pemelihara Ekologi Marin
    ("Pemelihara Ekologi Marin", None, 1, "Sertai kempen pemeliharaan ekologi marin", "Sertai secara aktif SATU kempen pemeliharaan ekologi marin yang relevan (sungai, pantai, mangrove, hidupan laut)."),
    ("Pemelihara Ekologi Marin", None, 2, "Laporan lengkap yang disahkan", "Menulis laporan lengkap, disahkan oleh pihak sekolah dan pihak berkuasa (contoh: Kementerian Sumber Asli, Jabatan Perikanan, WWF)."),
    # Pewaris Maritim
    ("Pewaris Maritim", None, 1, "Lawatan ke organisasi maritim", "Lawatan ke SATU organisasi maritim (contoh: Pangkalan TLDM, Pejabat Jabatan Laut, APMM, Jabatan Perikanan)."),
    ("Pewaris Maritim", None, 2, "Lawatan ke institusi pendidikan marin", "Lawatan ke SATU institusi pendidikan marin (contoh: ALAM, Pusat Marin, Jabatan Sains Marin universiti)."),
    ("Pewaris Maritim", None, 3, "Lawatan ke lokasi maritim", "Lawatan ke SATU lokasi maritim (contoh: pelabuhan komersil, taman laut, limbungan kapal, muzium maritim, akuarium)."),
    ("Pewaris Maritim", None, 4, "Tulis laporan lengkap dengan gambar", "Menulis laporan lengkap bagi setiap lawatan, bersama gambar."),
    # Pustakawan
    ("Pustakawan", "Pilihan 1: senarai 12 buku dibaca", 1, "Senarai 12 buku dibaca", "Memberikan senarai sekurang-kurangnya 12 jenis buku yang dibaca dalam tempoh 12 bulan lalu; terangkan sebab buku-buku itu dibaca, pendapat mengenai buku-buku itu dan menjawab soalan berkenaan. Ingatan: senarai hendaklah mengandungi cerita fiksyen dan tidak fiksyen, tidak melebihi 3 buah buku oleh seorang pengarang, dan tidak termasuk buku teks sekolah."),
    ("Pustakawan", "Pilihan 2: buku digemari", 2, "Senarai buku digemari", "Memberikan senarai buku yang digemari; terangkan sebab buku-buku itu dipilih dan jawab soalan berkenaan kandungan buku-buku itu."),
    ("Pustakawan", "Pilihan 2: buku digemari", 3, "Buku Rujukan", "Mengetahui apa yang dikatakan Buku Rujukan dan apakah maklumat yang diperoleh daripada buku itu."),
    ("Pustakawan", "Pilihan 2: buku digemari", 4, "Cara mengatur dan menyusun buku", "Menerangkan dengan ringkas cara mengatur dan menyusun buku supaya mudah dicari."),
]

# Peladang Muda position 1 and 2 were corrected by mistake in an earlier migration, so the details are set here by position.
PELADANG_DETAIL_FIXES = [
    (1, "Mengetahui cara pengurusan suatu pusat ternakan di kawasan luar bandar atau desa."),
    (2, "Menunjukkan cara pengelolaan harian bagi sesuatu pusat ternakan. Menghuraikan kepada Penilai perubahan yang berlaku di pusat ternakan di kawasan serta beri sebab perubahan itu dibuat. Melakukan latihan praktik di suatu pusat ternakan yang baru ditubuhkan."),
]


def _insert_group(badge_name: str, title: str, pick_count: int, position: int, parent_title: str | None, poultry: bool) -> None:
    op.execute(
        sa.text("""
            insert into requirement_groups (badge_id, title, pick_count, position, parent_group_id, applies_when_poultry)
            select b.id, :title, :pick_count, :position,
                   (select p.id from requirement_groups p
                    where p.badge_id = b.id and p.title = :parent_title),
                   :poultry
            from badges b
            join levels l on l.id = b.level_id
            where b.name = :badge_name
              and l.name = 'Pengakap Muda'
              and not exists (
                  select 1 from requirement_groups g
                  where g.badge_id = b.id and g.title = :title
              )
        """).bindparams(
            title=title,
            pick_count=pick_count,
            position=position,
            parent_title=parent_title,
            poultry=poultry,
            badge_name=badge_name,
        )
    )


def _insert_requirement(badge_name: str, group_title: str | None, position: int, text: str, detail: str | None) -> None:
    op.execute(
        sa.text("""
            insert into requirements (badge_id, stream_id, group_id, position, text, detail)
            select b.id, null,
                   (select g.id from requirement_groups g
                    where g.badge_id = b.id and g.title = :group_title),
                   :position, :text, :detail
            from badges b
            join levels l on l.id = b.level_id
            where b.name = :badge_name
              and l.name = 'Pengakap Muda'
              and not exists (
                  select 1 from requirements r
                  where r.badge_id = b.id and r.position = :position
              )
        """).bindparams(
            group_title=group_title,
            position=position,
            text=text,
            detail=detail,
            badge_name=badge_name,
        )
    )


def _set_peladang_detail(position: int, detail: str) -> None:
    op.execute(
        sa.text("""
            update requirements r
            set detail = :detail
            from badges b
            where b.id = r.badge_id
              and b.name = 'Peladang Muda'
              and r.position = :position
        """).bindparams(detail=detail, position=position)
    )


def upgrade() -> None:
    # Groups first, parents before children, so each parent exists when its children are inserted.
    for badge_name, title, pick_count, position, parent_title, poultry in GROUPS:
        _insert_group(badge_name, title, pick_count, position, parent_title, poultry)
    for badge_name, group_title, position, text, detail in REQUIREMENTS:
        _insert_requirement(badge_name, group_title, position, text, detail)
    for position, detail in PELADANG_DETAIL_FIXES:
        _set_peladang_detail(position, detail)


def downgrade() -> None:
    # Nothing is removed. The dev database already had these badges' rows before this migration,
    # so deleting them here would delete real data. A fresh database can be rebuilt by upgrading.
    pass

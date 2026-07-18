#!/usr/bin/env python3
"""Generate the Unravel Trigger Instagram carousel (1080x1350) and export PNGs.

Usage:  python3 build.py            # writes slides/*.html and export/*.png
Requires Google Chrome for the PNG export step.
"""
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

CSS = """
  @font-face{font-family:'Oswald';src:url('../fonts/oswald.woff2') format('woff2');font-weight:300 700}
  @font-face{font-family:'Cormorant Garamond';src:url('../fonts/cormorant.woff2') format('woff2');font-weight:300 700}
  @font-face{font-family:'Lora';src:url('../fonts/lora.woff2') format('woff2');font-weight:400 700}
  :root{
    --ink:#0b101c; --panel:#131b2d; --frost:#e8ecf4; --body:#b9c1d1;
    --gilt:#b3925a; --gilt-dim:rgba(179,146,90,.42); --gilt-hair:rgba(179,146,90,.20);
    --trigger:#c22745;
    --display:'Cormorant Garamond','Hiragino Mincho ProN',Georgia,serif;
    --serif:'Lora',Georgia,serif;
    --label:'Oswald','Hiragino Kaku Gothic ProN',Arial,sans-serif;
  }
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{width:1080px;height:1350px;overflow:hidden}
  body{background:var(--ink);color:var(--body);font-family:var(--serif);position:relative}
  .plate{position:absolute;inset:36px;border:1px solid var(--gilt-dim);pointer-events:none;z-index:5}
  .slide{position:absolute;inset:0;padding:104px 100px;display:flex;flex-direction:column}

  /* content slide header */
  .head{display:flex;align-items:baseline;gap:30px;margin-bottom:26px}
  .numeral{font-family:var(--display);font-weight:700;font-size:112px;line-height:.8;
           color:transparent;-webkit-text-stroke:1.5px var(--gilt-dim);flex:0 0 auto}
  .file-label{font-family:var(--label);font-weight:500;font-size:25px;letter-spacing:.3em;
              text-transform:uppercase;color:var(--gilt)}
  .rule{height:1px;background:var(--gilt-hair);position:relative;margin-bottom:40px}
  .rule::after{content:"\\2316";position:absolute;left:0;top:50%;translate:0 -50%;
               color:var(--trigger);font-size:20px;background:var(--ink);padding-right:14px}

  .frame{border:1px solid var(--gilt-dim);padding:10px;margin-bottom:52px;background:var(--panel)}
  .frame img{display:block;width:100%;height:430px;object-fit:cover}

  /* flags / duo variants */
  .trio{display:flex;gap:22px;margin-bottom:14px}
  .trio .frame{flex:1;margin-bottom:0}
  .trio .frame img{height:200px}
  .trio-caps{display:flex;gap:22px;margin-bottom:44px}
  .trio-caps span{flex:1;text-align:center;font-family:var(--label);font-weight:400;font-size:17px;
                  letter-spacing:.2em;text-transform:uppercase;color:var(--body)}
  .trio-caps b{color:var(--gilt);font-weight:500}
  .duo{display:flex;gap:22px;margin-bottom:52px}
  .duo .frame{flex:1;margin-bottom:0}
  .duo .frame img{height:300px}

  .copy{font-size:29px;line-height:1.66;color:var(--body);max-width:880px}
  .copy + .copy{margin-top:24px}
  .copy strong{color:var(--frost);font-weight:600}
  .copy em{font-family:var(--display);font-style:italic;color:var(--gilt)}

  .foot{display:flex;align-items:center;justify-content:space-between;
        border-top:1px solid var(--gilt-hair);padding-top:26px;margin-top:auto}
  .foot .name{font-family:var(--label);font-weight:400;font-size:19px;letter-spacing:.22em;
              text-transform:uppercase;color:var(--gilt)}
  .index{font-family:var(--display);font-style:italic;font-size:24px;color:var(--body)}
  .index b{color:var(--gilt);font-weight:600;font-style:normal}

  /* cover */
  .cover-bg{position:absolute;inset:0;background:url('../images/hero.jpg') center 30%/cover}
  .cover-scrim{position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,16,28,.45),rgba(11,16,28,.08) 34%,rgba(11,16,28,.2) 56%,rgba(11,16,28,.93) 84%,var(--ink))}
  .cover .slide{justify-content:flex-end;padding-bottom:120px}
  .kicker{display:flex;align-items:center;gap:20px;font-family:var(--label);font-weight:500;font-size:23px;
          letter-spacing:.26em;text-transform:uppercase;color:var(--frost);margin-bottom:40px;
          text-shadow:0 1px 3px rgba(0,0,0,.95),0 2px 18px rgba(0,0,0,.9)}
  .kicker::before{content:"";width:60px;height:1px;background:rgba(232,236,244,.6);flex:0 0 auto}
  .cover-logo{width:760px;filter:drop-shadow(0 4px 26px rgba(0,0,0,.8))}
  .cover-tag{font-family:var(--label);font-weight:300;font-size:24px;letter-spacing:.2em;color:var(--body);
             margin-top:30px;text-shadow:0 1px 8px rgba(0,0,0,.9)}
  .cover-meta{display:flex;margin-top:52px;border-top:1px solid var(--gilt-hair);padding-top:30px;
              font-family:var(--label);font-weight:400;font-size:21px;letter-spacing:.14em;
              text-transform:uppercase;color:rgba(232,236,244,.92)}
  .cover-meta span+span::before{content:"\\25c9";font-size:12px;vertical-align:3px;color:var(--trigger);margin:0 22px}

  /* verdict */
  .verdict .slide{align-items:center;text-align:center}
  .rating-label{font-family:var(--label);font-weight:500;font-size:23px;letter-spacing:.34em;
                text-transform:uppercase;color:var(--gilt);margin:auto 0 0}
  .stamp{width:210px;height:210px;border:5px double var(--trigger);border-radius:50%;margin:44px auto 0;
         display:flex;align-items:center;justify-content:center;transform:rotate(-8deg);
         box-shadow:0 0 0 2px rgba(194,39,69,.25) inset,0 0 54px rgba(194,39,69,.30)}
  .stamp .grade{font-family:var(--display);font-weight:700;font-size:130px;line-height:1;color:var(--trigger);
                text-shadow:0 0 28px rgba(194,39,69,.55);margin-top:-8px}
  .score{font-family:var(--display);line-height:1;display:flex;align-items:baseline;gap:20px;
         justify-content:center;margin-top:34px}
  .score .big{font-weight:700;color:var(--frost);font-size:150px}
  .score .of{font-style:italic;font-weight:500;color:var(--gilt);font-size:64px}
  .rounds{display:flex;gap:16px;justify-content:center;margin-top:30px}
  .round{width:22px;height:22px;border-radius:50%;border:2px solid var(--trigger)}
  .round.full{background:var(--trigger)}
  .round.part{background:linear-gradient(90deg,var(--trigger) 60%,transparent 60%)}
  .verdict .copy{text-align:center;margin:56px 0 auto;font-size:30px;max-width:840px}
  .verdict .foot{width:100%;margin-top:0}
"""

TOTAL = 16

CSS_DIR = ROOT / 'assets' / 'css'
CSS_DIR.mkdir(parents=True, exist_ok=True)
(CSS_DIR / 'slides.css').write_text(CSS)

def page(body, cls=''):
    return (f'<!doctype html><html><head><meta charset="utf-8">'
            f'<link rel="stylesheet" href="../assets/css/slides.css"></head>'
            f'<body class="{cls}"><div class="plate"></div>{body}</body></html>')

def foot(n):
    return (f'<div class="foot"><span class="name">Unravel Trigger — Visual Novel Review</span>'
            f'<span class="index"><b>{n:02d}</b> / {TOTAL}</span></div>')

def head(n, label):
    return (f'<div class="head"><span class="numeral">{n:02d}</span>'
            f'<p class="file-label">{label}</p></div><div class="rule"></div>')

def content_slide(n, label, img, *paras):
    copy = ''.join(f'<p class="copy">{p}</p>' for p in paras)
    return page(f'''
  <div class="slide">
    {head(n, label)}
    <div class="frame"><img src="../assets/images/{img}" alt=""></div>
    {copy}
    {foot(n)}
  </div>''')

def trio_slide(n, label, *paras):
    copy = ''.join(f'<p class="copy">{p}</p>' for p in paras)
    return page(f'''
  <div class="slide">
    {head(n, label)}
    <div class="trio">
      <div class="frame"><img src="../assets/images/flag-kaarg.jpg" alt=""></div>
      <div class="frame"><img src="../assets/images/flag-vilcar.jpg" alt=""></div>
      <div class="frame"><img src="../assets/images/flag-ymir.jpg" alt=""></div>
    </div>
    <div class="trio-caps">
      <span><b>Kaarg</b> · Hyume</span><span><b>Vilcar</b> · Vamp</span><span><b>Ymir</b> · Anima</span>
    </div>
    {copy}
    {foot(n)}
  </div>''')

def duo_slide(n, label, img1, img2, *paras):
    copy = ''.join(f'<p class="copy">{p}</p>' for p in paras)
    return page(f'''
  <div class="slide">
    {head(n, label)}
    <div class="duo">
      <div class="frame"><img src="../assets/images/{img1}" alt=""></div>
      <div class="frame"><img src="../assets/images/{img2}" alt=""></div>
    </div>
    {copy}
    {foot(n)}
  </div>''')

slides = {}

slides['slide-01-cover'] = page(f'''
  <div class="cover-bg"></div><div class="cover-scrim"></div>
  <div class="slide">
    <p class="kicker">Archive · Visual Novel Review</p>
    <img class="cover-logo" src="../assets/images/titlelogo.png" alt="Unravel Trigger">
    <p class="cover-tag">──ここが平和（センソウ）を巡る最前線</p>
    <div class="cover-meta"><span>2024</span><span>Japanese</span><span>Long · 30–50h</span><span>18+</span></div>
  </div>''', 'cover')

slides['slide-02-sinopsis-1'] = content_slide(2, 'Sinopsis · I', 'diplomacy.jpg',
    'Pecahnya peperangan antara <strong>Federasi Kaarg</strong> dan <strong>Kekaisaran '
    'Vilcar</strong> akhirnya memasuki titik jenuh sehingga terjadilah gencatan senjata '
    'melalui cara diplomatis.',
    'Teritori Kaarg yang masuk zona peperangan diperebutkan oleh kedua belah pihak, sampai '
    'akhirnya Republik Ymir turun tangan sebagai penengah — wilayah tersebut pun menjadi '
    '<strong>Zona Buffer</strong> atau Zona Netral Perang dibawah regulasi Republik Ymir.')

slides['slide-03-sinopsis-2'] = content_slide(3, 'Sinopsis · II', 'yuzuriha-saina.jpg',
    'Peperangan seperti pada umumnya merenggut banyak hal berharga, termasuk '
    '<strong>Yuzuriha Saina</strong>, <em>Osananajimi</em> dari protagonis kita, '
    '<strong>Sakaki Kai</strong>.',
    'Cerita berpusat pada Kai yang mencari teman dekatnya itu setelah mendapat info bahwa '
    'dia sebenernya belum mati dan berada di wilayah sekitar Zona Netral. Kai juga menggarap '
    'sebagai detektif untuk menghidupi kebutuhannya sekaligus melacak keberadaan Saina.')

slides['slide-04-latar-1'] = content_slide(4, 'Latar Konflik · I', 'frost-neutral-territory.jpg',
    'Terdapat 3 kekuatan besar dalam alur VN ini: Federasi Kaarg dihuni ras <strong>Hyume</strong> '
    '(Manusia), Kekaisaran Vilcar teritori ras <strong>Vamp</strong> (Vampir) berdarah murni, '
    'dan wilayah ras <strong>Anima</strong> (<em>Half Beast</em>) yaitu Republik Ymir.',
    '<strong>Frost Neutral Territory</strong>, panggung utama cerita, merupakan Zona Buffer '
    'sekaligus tempat perhunian ketiga ras tadi — nah, apa jadinya jika dua musuh perang '
    'yang masih anget bermukim di tempat yang sama?')

slides['slide-05-latar-2'] = content_slide(5, 'Latar Konflik · II', 'hero.jpg',
    'Perang adalah sebuah akar dari rantai kebencian. Patriotisme dan rasa sakit ditinggalkan '
    'orang terdekat merupakan bubuk mesiu yang paling efektif, massa serta media ibarat '
    'kerangka penopang, dan pemerintahlah yang punya kontrol terhadap pelatuk.',
    'Gerakan separatis, terorisme, grup2 radikal menggumpal di Frost Neutral Territory — '
    'belum lagi diktatorat dan rasisme yang menjadi pemandangan sehari2 — membuat latar VN '
    'ini seolah olah <strong>bom yang bisa meledak kapanpun</strong>.')

slides['slide-06-ideologi'] = trio_slide(6, 'Demokrat · Komunis · Nazi',
    '3 Kekuatan besar disini punya korelasi serta inspirasi dari dunia nyata: Federasi Kaarg '
    'merepresentasikan negara demokrasi pada umumnya, contohnya <strong>United States</strong>; '
    'Republik Ymir digambar dengan pondasi <strong>Soviet Union</strong> yang pekat dengan komunisme.',
    'Dan yang paling menarik — Kekaisaran Vilcar diilustrasikan sebagai Jerman pada masa '
    '<strong>Third Reich</strong>, menganut ideologi2 Nazi seperti propaganda ras superior, '
    'genosida, rasisme, dan lainnya.')

slides['slide-07-hyume'] = content_slide(7, 'Ras · Hyume', 'flag-kaarg.jpg',
    'Ras disini punya keunggulannya masing2. <strong>Hyume</strong> (Manusia) unggul dalam '
    'teknologi dan terobosan sains; beberapa diantaranya memegang gelar <em>Legacy</em> — '
    'manusia terpilih dengan rasio <strong>1/10.000</strong> yang memiliki berkat kekuatan alami.',
    'Contohnya protagonis kita, Kai, yang memiliki kemampuan <strong>psikokinesis</strong> — '
    'digabungkan dengan kecerdikan serta kemahirannya bermain senjata api, menjadikannya '
    'unggul dalam banyak pertempuran.')

slides['slide-08-anima'] = content_slide(8, 'Ras · Anima', 'anima-power.jpg',
    '<strong>Anima</strong> (<em>Half-Beast</em>) diberkahi kemampuan fisik luar biasa, '
    'membuatnya selalu unggul dalam hal <em>raw power</em> — namun bukan berarti ras yang '
    'satu ini lemah dalam permainan otak.',
    '<strong>Sophia Noscova</strong>, pemegang wewenang tertinggi badan intelejensi di Frost '
    'Neutral Territory, pandai menyusun rencana — musuh external maupun internal, politik '
    'maupun militer, gk mau main main dengannya.')

slides['slide-09-vamp'] = content_slide(9, 'Ras · Vamp', 'vamp-power.jpg',
    '<strong>Vamp</strong> (<em>Vampire</em>) memiliki tubuh abadi — tidak bisa dibunuh '
    'kecuali dipenggal atau kepalanya hancur (dan umur) — serta bakat alamiah mengendalikan '
    'darah selayaknya senjata, ibarat <em>Machine Gun</em> tanpa wujud yang dapat beraksi kapanpun.',
    'Atribut2 semacam itulah yang membuat ras ini beranggapan merekalah sang '
    '<strong>apex predator</strong> yang sepantasnya berada diatas ras2 lain.')

slides['slide-10-heroine'] = content_slide(10, 'Para Heroine', 'heroines-group.jpg',
    '<strong>Main Heroine</strong> disini disejajarkan dengan 3 faksi utama dalam cerita, '
    'mengeksplorasi masing2 ideologi politik pada domisili asalnya sehingga menjadikan tiap '
    '<em>route</em> nya khas dan menjamin <em>reading experience</em> yang berwarna.')

slides['slide-11-reiri'] = content_slide(11, 'Route · Reiri', 'reiri-illumination.jpg',
    'Dari faksi manusia: <strong>Kohanai Reiri</strong>, <em>Heroine</em> dengan <em>troupe</em> '
    'utama <em>Joushi Koukousei</em> (cewek sekolahan) yang posesif dan gk mau ngalah.',
    'Route Reiri bisa dibilang <em>route</em> paling “damai” karena temanya berhubungan dengan '
    'sistem politik demokrasi — dengan bumbu tindakan ekstrim dari pihak radikal yang membuat '
    'route ini punya keseruannya sendiri.')

slides['slide-12-sophia'] = content_slide(12, 'Route · Sophia', 'sophia.jpg',
    '<strong>Sophia Noscova</strong>, Jendral Badan Intelejensi republik Ymir di zona netral. '
    'Kemampuan nalar tinggi, selalu mengutamakan logika diatas perasaan — penampilan serta '
    'gerak geriknya sebatas topeng untuk mengelabui lawan dan kawan.',
    'Konflik routenya menyangkut tanah airnya yang belum lama terjadi <strong>Revolusi</strong> '
    '— mengubah sistem pemerintahan dari Monarki menjadi Komunis — sehingga banyak menyentuh '
    'ide kesetaraan dan diktatorat.')

slides['slide-13-millicent-1'] = content_slide(13, 'Grand Route · I', 'milicent_speech.jpg',
    'Dan yang terakhir — Hidangan Utama serta <strong>Grand Route</strong> dari Unravel '
    'Trigger: Route putri kerajaan ras Vamp, <strong>Millicent Fried Leonhard</strong>.',
    'Mili adalah pribadi yang idealis, ambisius, dan juga seorang <em>Philantrophist</em>!. '
    'Idealisme tinggi akan perdamaian antar ras merupakan pondasi utama dirinya menjadi '
    '<em>Ambassador</em> di Frost Neutral Territory — menjaga <em>status quo</em>, mencegah '
    'perang lanjutan, menciptakan dunia bebas konflik.')

slides['slide-14-millicent-2'] = content_slide(14, 'Grand Route · II', 'millicent-nightdance.jpg',
    'Tentu kenyataannya gak semudah itu — Mili sang pasifis, tipe2 orang yang kalau ditanya '
    'mengenai <em>Trolley Problem</em> bakal jawab akan menyelematkan semuanya, adalah '
    '<strong>ancaman</strong> di mata berbagai pihak.',
    'Sikap positif serta baik hati merupakan kekuatan sekaligus kelemahannya — dieksekusi '
    'dengan baik di routenya, menjadikan <strong>Route Heroine yang paling impresif dan '
    'paling seru</strong> menurut gw pribadi.')

slides['slide-15-extra'] = duo_slide(15, 'Extra Story', 'extra-story1.jpg', 'extra-story2.jpg',
    'Unravel Trigger juga memiliki hidangan penutup berupa <em>IF route</em> para ajudan '
    'Main Heroine dan <em>After Story</em> tiap heroine.',
    'Seperti <em>After Story</em> pada umumnya, chapter2 ini tidak memiliki jalan cerita — '
    'hanya menyuguhkan momen para Heroine sampingan yang gak kebagian porsi di cerita utama.')

slides['slide-16-verdict'] = page(f'''
  <div class="slide">
    <p class="rating-label">Final Verdict</p>
    <div class="stamp"><span class="grade">A</span></div>
    <div class="score"><span class="big">3.6</span><span class="of">/ 5</span></div>
    <div class="rounds">
      <span class="round full"></span><span class="round full"></span><span class="round full"></span><span class="round part"></span><span class="round"></span>
    </div>
    <p class="copy">Unravel Trigger memiliki konsep yang unik — konflik yang merefleksikan realita memberikan bobot pada cerita dan pengalaman membaca yang impresif, ditambah bumbu2 <em>moege</em> yang pada kadarnya. Sayangnya <em>action scene</em> dan karakter utamanya kurang memuaskan. VN ini cocok jika kamu mencari <em>story</em> yang menarik diiringi konflik yang kritis dengan <em>length</em> yg gak begitu panjang.</p>
    {foot(16)}
  </div>''', 'verdict')

for name, html in slides.items():
    (ROOT / 'slides' / f'{name}.html').write_text(html)
    print('wrote slides/' + name + '.html')

for name in slides:
    out = ROOT / 'export' / f'{name}.png'
    subprocess.run([CHROME, '--headless', f'--screenshot={out}',
                    '--window-size=1080,1350', '--hide-scrollbars',
                    '--force-device-scale-factor=1', '--disable-gpu',
                    str(ROOT / 'slides' / f'{name}.html')],
                   check=True, capture_output=True)
    print('exported export/' + name + '.png')

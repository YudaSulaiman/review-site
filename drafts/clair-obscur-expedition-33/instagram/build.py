#!/usr/bin/env python3
"""Generate the Instagram carousel slides (1080x1350) and export them as PNGs.

Usage:  python3 build.py            # writes slides/*.html and export/*.png
Requires Google Chrome for the PNG export step.
"""
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

CSS = """
  @font-face{font-family:'Playfair Display';src:url('../assets/fonts/playfair-normal.woff2') format('woff2');font-weight:400 800;font-style:normal}
  @font-face{font-family:'Playfair Display';src:url('../assets/fonts/playfair-italic.woff2') format('woff2');font-weight:400 800;font-style:italic}
  :root{
    --ink:#0f0d11; --panel:#191521; --ivory:#eae2d3; --body:#b9ae9c;
    --gilt:#c4a165; --gilt-dim:rgba(196,161,101,.32); --gilt-hair:rgba(196,161,101,.18);
    --display:'Playfair Display',Didot,Georgia,serif;
    --serif:Charter,'Iowan Old Style',Georgia,serif;
  }
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{width:1080px;height:1350px;overflow:hidden}
  body{background:var(--ink);color:var(--body);font-family:var(--serif);position:relative}
  .plate{position:absolute;inset:36px;border:1px solid var(--gilt-dim);pointer-events:none;z-index:5}
  .slide{position:absolute;inset:0;padding:104px 100px;display:flex;flex-direction:column}

  /* content slide header */
  .head{display:flex;align-items:baseline;gap:30px;margin-bottom:30px}
  .numeral{font-family:var(--display);font-weight:700;font-size:112px;line-height:.8;
           color:transparent;-webkit-text-stroke:1.5px var(--gilt-dim);flex:0 0 auto}
  .acte-label{font-size:27px;letter-spacing:.3em;text-transform:uppercase;color:var(--gilt)}
  .rule{height:1px;background:var(--gilt-hair);position:relative;margin-bottom:40px}
  .rule::after{content:"◆";position:absolute;left:0;top:50%;translate:0 -50%;color:var(--gilt);font-size:11px;background:var(--ink);padding-right:14px}

  .frame{border:1px solid var(--gilt-dim);padding:10px;margin-bottom:52px;
         background:linear-gradient(160deg,rgba(196,161,101,.05),rgba(196,161,101,0) 45%)}
  .frame img{display:block;width:100%;height:430px;object-fit:cover}

  .copy{font-size:29px;line-height:1.66;color:var(--body);max-width:880px}
  .copy + .copy{margin-top:24px}
  .copy strong{color:var(--ivory);font-weight:600}
  .copy em{font-family:var(--display);font-style:italic;color:var(--gilt)}

  .foot{display:flex;align-items:center;justify-content:space-between;
        border-top:1px solid var(--gilt-hair);padding-top:26px;margin-top:auto}
  .foot .name{font-size:19px;letter-spacing:.22em;text-transform:uppercase;color:var(--gilt)}
  .index{font-family:var(--display);font-style:italic;font-size:24px;color:var(--body)}
  .index b{color:var(--gilt);font-weight:600}

  /* cover */
  .cover-bg{position:absolute;inset:0;background:url('../assets/images/hero.jpg') center 30%/cover}
  .cover-scrim{position:absolute;inset:0;background:linear-gradient(180deg,rgba(15,13,17,.5),rgba(15,13,17,.05) 32%,rgba(15,13,17,.15) 55%,rgba(15,13,17,.92) 84%,var(--ink))}
  .cover .slide{justify-content:flex-end;padding-bottom:120px}
  .kicker{display:flex;align-items:center;gap:20px;font-size:23px;font-weight:700;letter-spacing:.26em;
          text-transform:uppercase;color:#eeddb2;margin-bottom:34px;
          text-shadow:0 1px 3px rgba(0,0,0,.95),0 2px 18px rgba(0,0,0,.9)}
  .kicker::before{content:"";width:60px;height:1px;background:rgba(238,221,178,.6);flex:0 0 auto}
  h1{font-family:var(--display);font-weight:600;color:var(--ivory);font-size:104px;line-height:1.03;
     text-shadow:0 2px 30px rgba(15,13,17,.85)}
  h1 .num{color:var(--gilt);font-style:italic;font-weight:500}
  .cover-meta{display:flex;margin-top:56px;border-top:1px solid var(--gilt-hair);padding-top:30px;
              font-size:21px;letter-spacing:.14em;text-transform:uppercase;color:rgba(234,226,211,.92)}
  .cover-meta span+span::before{content:"◆";font-size:10px;vertical-align:4px;color:var(--gilt);margin:0 22px}

  /* verdict */
  .verdict .slide{align-items:center;text-align:center}
  .rating-label{font-size:23px;letter-spacing:.34em;text-transform:uppercase;color:var(--gilt);margin:auto 0 0}
  .score{font-family:var(--display);line-height:1;display:flex;align-items:baseline;gap:24px;justify-content:center}
  .score .big{font-weight:700;color:var(--ivory);font-size:300px}
  .score .of{font-style:italic;font-weight:500;color:var(--gilt);font-size:88px}
  .diamonds{font-size:32px;letter-spacing:32px;margin:30px 0 0 32px;color:var(--gilt)}
  .diamonds .off{color:var(--gilt-dim)}
  .verdict .copy{text-align:center;margin:64px 0 auto;font-size:30px;max-width:830px}
  .verdict .foot{width:100%;margin-top:0}
"""

TOTAL = 14

def page(body, cls=''):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>'
            f'<body class="{cls}"><div class="plate"></div>{body}</body></html>')

def foot(n):
    return (f'<div class="foot"><span class="name">Clair Obscur : Expedition 33 — Review</span>'
            f'<span class="index"><b>{n:02d}</b> / {TOTAL}</span></div>')

def content_slide(n, label, img, *paras):
    copy = ''.join(f'<p class="copy">{p}</p>' for p in paras)
    return page(f'''
  <div class="slide">
    <div class="head">
      <span class="numeral">{n:02d}</span>
      <p class="acte-label">{label}</p>
    </div>
    <div class="rule"></div>
    <div class="frame"><img src="../assets/images/{img}" alt=""></div>
    {copy}
    {foot(n)}
  </div>''')

slides = {}

slides['slide-01-cover'] = page(f'''
  <div class="cover-bg"></div><div class="cover-scrim"></div>
  <div class="slide">
    <p class="kicker">Sandfall Interactive · Game Review</p>
    <h1>Clair Obscur<br>Expedition <span class="num">33</span></h1>
    <div class="cover-meta"><span>PC / PS5</span><span>2025</span><span>~70h played</span></div>
  </div>''', 'cover')

slides['slide-02-intro'] = content_slide(2, 'Introduction', 'lumiere.jpg',
    '<strong>Clair Obscur: Expedition 33</strong> is the debut RPG from Sandfall Interactive, '
    'a small French studio — set in a dreamlike world inspired by the '
    '<em>Belle Époque</em> era.',
    'Released in April 2025 for PC and PS5, it went on to win the '
    '<strong>Game of the Year</strong> award.')

slides['slide-03-gommage'] = content_slide(3, 'The World', 'gommage.jpg',
    'Society lives under the shadow of a yearly phenomenon called the <strong>Gommage</strong>: '
    'a godlike entity known as the <strong>Paintress</strong> awakens and paints a single number '
    'on a distant monolith — and every person whose age matches that number is instantly '
    '<strong>erased from existence</strong>.',
    'The number drops by one each year. <em>A slow, creeping countdown toward total annihilation.</em>')

slides['slide-04-expedition'] = content_slide(4, 'The Mission', 'overlook.jpg',
    'In response, the people of <strong>Lumière</strong> have been sending out expeditions across '
    'a shattered, surreal continent to find and kill the Paintress and end the cycle once and '
    'for all. <strong>Every expedition has failed.</strong>',
    'With only one year remaining before they too are erased, Gustave and the members of '
    '<em>Expedition 33</em> set out on a final, desperate mission.')

slides['slide-05-storytelling'] = content_slide(5, 'The Narrative · I', 'renoir.jpg',
    'The narrative is divided into two sections: <strong>Question Arcs</strong> and '
    '<strong>Answer Arcs</strong>. You keep pondering what the hell happens in Lumière, '
    'connecting the dots from scattered info fragments and dialogue between mysterious people —',
    '— then get struck with <strong>huge revelations and plot twists</strong>. Sandfall built '
    'the hype throughout the game and <em>gracefully executed a supreme ending</em>.')

slides['slide-06-ending'] = content_slide(6, 'The Narrative · II', 'gustave.jpg',
    'Clair Obscur does not give a typical ending you see in a game. It is a <strong>choice</strong> '
    '— and a very messed up one. There is no True End, no best outcome; it questions your '
    '<strong>morality and creed</strong>.',
    'An ending worthy of discussion and debate — and those lingering feelings are a major '
    'factor in its <em>Game of the Year</em> win.')

slides['slide-07-jrpg'] = content_slide(7, 'The Flavor', 'monoco.jpg',
    'People say Clair Obscur is a <strong>JRPG without the Anime</strong>, and it shows: '
    'fighting gods, recruiting strange creatures as teammates, a relationship feature, a '
    'heroine with a mysterious backstory, and silly minigames for special outfits.',
    'Classic JRPG tropes, modified to be consumable for a broader audience — '
    '<em>in a unique French style indeed</em>.')

slides['slide-08-art'] = content_slide(8, 'Art & Graphics', 'sciel.jpg',
    '<em>Clair Obscur</em> means <strong>“Light and Dark”</strong> in French. Its design is '
    'centered on strong contrast between light and dark — the illusion of volume and depth, '
    'and an artistic, unique game UI without sacrificing clarity.',
    'It also runs surprisingly smooth on the infamous <strong>Unreal Engine 5</strong>.')

slides['slide-09-sound'] = content_slide(9, 'Presentation', 'boss.jpg',
    'If one word could describe Clair Obscur, it would be <strong>“Cinematic.”</strong> '
    'A generously huge amount of top-quality cutscenes that feel straight out of movies — '
    'and boss attacks you gaze at in awe even as they are meant to kill you.',
    'Add an <strong>orchestra-level OST</strong> in every part of the game, and the music '
    'becomes <em>the game’s identity itself</em>.')

slides['slide-10-combat'] = content_slide(10, 'Gameplay · I', 'creature.jpg',
    'Combat is <strong>turn-based</strong>: Attack, Skills, Items, and aimed shots, all paid '
    'for with <strong>AP</strong>. But when the enemy strikes, you can '
    '<strong>parry or dodge in real time</strong>.',
    'Every successful parry rewards damage, skill points and break gauge — and a perfect '
    'one <em>nullifies all the damage</em>.')

slides['slide-11-parry'] = content_slide(11, 'Gameplay · II', 'parry.jpg',
    'The parry mechanics are <strong>unbalanced</strong>. Easy to execute — whenever, whoever, '
    'against <strong>ANYTHING</strong> — and too rewarding. Why bother building a proper '
    'character, synergizing team members, or investing in HP and defense, when parries do it all?',
    'EVERY turn can become YOUR turn after a few observations of the enemy’s attack '
    'pattern. Suddenly it is just <em>a QTE game disguised as a turn-based game</em>.')

slides['slide-12-punishment'] = content_slide(12, 'Gameplay · III', 'march.jpg',
    'Worse: there are like <strong>ZERO PUNISHING MECHANICS</strong> in this game. Even on '
    'Expert Mode, you can instantly retry or just undo a lost encounter like nothing happened.',
    'Strange, gigantic, exotic-looking creatures wander all around the continent — and the '
    'game tells you they can be approached without <strong>ANY</strong> consequences. '
    '<em>It completely kills the suspense and anticipation.</em>')

slides['slide-13-gun'] = content_slide(13, 'Gameplay · IV', 'turnbased.jpg',
    'The gun mechanic, <strong>“Free Aim,”</strong> on the other hand, is creative and '
    'balanced enough. A single bullet costs one AP, it does not end the character’s turn, '
    'and some enemies hide <strong>weak points</strong> you can shoot for a huge chunk of damage.',
    'Stack the right passives and you gain AP back per shot — turning your revolver into a '
    '<strong>semi-automatic machine gun</strong>. <em>They really added an FPS playstyle '
    'instead of improving the turn-based system.</em>')

slides['slide-14-verdict'] = page(f'''
  <div class="slide">
    <p class="rating-label">Final Verdict</p>
    <div class="score"><span class="big">3</span><span class="of">/ 5</span></div>
    <div class="diamonds">◆◆◆<span class="off">◆◆</span></div>
    <p class="copy">Clair Obscur excels in <strong>presentation</strong> — scenes and music orchestrated so well it is akin to witnessing a <em>grand opera</em>. Highly recommended even for the narrative experience alone. As for the gameplay: it is forgiving. <strong>Too forgiving.</strong> You will probably enjoy the game too — <em>if you are, at least, not a masochist</em>.</p>
    {foot(14)}
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

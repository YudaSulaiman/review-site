#!/usr/bin/env python3
"""Generate the Instagram carousel slides (1080x1350) and export them as PNGs.

Usage:  python3 build.py            # writes slides/*.html and export/*.png
Requires Google Chrome for the PNG export step.
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).parent

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

  /* ── layout variants ─────────────────────────────────────── */

  /* full-bleed: artwork fills the slide, copy sits on the bottom scrim */
  .full-bg{position:absolute;inset:0}
  .full-bg img{width:100%;height:100%;object-fit:cover}
  .full-scrim{position:absolute;inset:0;background:linear-gradient(180deg,
      rgba(15,13,17,.88),rgba(15,13,17,.22) 24%,rgba(15,13,17,.14) 42%,
      rgba(15,13,17,.94) 62%,var(--ink) 90%)}
  .full .slide{position:absolute}
  .full .numeral{-webkit-text-stroke:1.5px rgba(196,161,101,.6)}
  .full .acte-label{text-shadow:0 1px 4px rgba(0,0,0,.9)}
  .full .rule{background:rgba(196,161,101,.3)}
  .full .rule::after{background:none}
  .full .copy{margin-top:auto;text-shadow:0 1px 3px rgba(0,0,0,.9)}
  .full .copy + .copy{margin-top:24px}
  .full .foot{margin-top:52px}

  /* text-first: copy leads, framed image anchors the bottom */
  .textfirst .frame{margin-top:auto;margin-bottom:0}
  .textfirst .foot{margin-top:52px}

  /* split: copy column beside a tall portrait plate */
  .split .row{display:flex;gap:52px;flex:1;min-height:0}
  .split .col{flex:1;display:flex;flex-direction:column;gap:24px;justify-content:center}
  .split .copy{font-size:28px}
  .split .frame{flex:0 0 400px;margin-bottom:0;display:flex}
  .split .frame img{height:100%;width:100%;object-fit:cover}
  .split .foot{margin-top:52px}

  /* text-only: argument slides too long for an image; generous leading */
  .textonly .copy{font-size:30px;line-height:1.72;max-width:880px;margin-top:6px}
  .textonly .copy + .copy{margin-top:28px}
  .textonly .endmark{color:var(--gilt);font-size:15px;letter-spacing:14px;margin-top:auto;
                     padding-top:44px}
  .textonly .foot{margin-top:40px}

  /* pull-quote: one line from the review, set large — no image */
  .lead-in{margin-top:10px}
  .quote-mark{font-family:var(--display);color:var(--gilt-dim);font-size:170px;
              line-height:.55;margin:auto 0 0;height:80px;padding-top:56px}
  .pull{font-family:var(--display);font-style:italic;font-weight:500;color:var(--ivory);
        font-size:57px;line-height:1.4;max-width:850px;margin-bottom:auto}
  .pull strong{color:var(--gilt);font-weight:500}
  .quoteslide .foot{margin-top:52px}
"""

TOTAL = 15

def page(body, cls=''):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>'
            f'<body class="{cls}"><div class="plate"></div>{body}</body></html>')

def foot(n):
    return (f'<div class="foot"><span class="name">Clair Obscur : Expedition 33 — Review</span>'
            f'<span class="index"><b>{n:02d}</b> / {TOTAL}</span></div>')

def head(n, label):
    return (f'<div class="head"><span class="numeral">{n:02d}</span>'
            f'<p class="acte-label">{label}</p></div><div class="rule"></div>')

def content_slide(n, label, img, *paras, img_h=430):
    copy = ''.join(f'<p class="copy">{p}</p>' for p in paras)
    return page(f'''
  <div class="slide">
    {head(n, label)}
    <div class="frame"><img src="../assets/images/{img}" alt="" style="height:{img_h}px"></div>
    {copy}
    {foot(n)}
  </div>''')

def full_slide(n, label, img, *paras):
    """Artwork fills the whole slide; copy sits on the bottom scrim."""
    copy = ''.join(f'<p class="copy">{p}</p>' for p in paras)
    return page(f'''
  <div class="full-bg"><img src="../assets/images/{img}" alt=""></div>
  <div class="full-scrim"></div>
  <div class="slide">
    {head(n, label)}
    {copy}
    {foot(n)}
  </div>''', 'full')

def textfirst_slide(n, label, img, *paras, img_h=430):
    """Copy leads; the framed image anchors the bottom of the slide."""
    copy = ''.join(f'<p class="copy">{p}</p>' for p in paras)
    return page(f'''
  <div class="slide">
    {head(n, label)}
    {copy}
    <div class="frame"><img src="../assets/images/{img}" alt="" style="height:{img_h}px"></div>
    {foot(n)}
  </div>''', 'textfirst')

def split_slide(n, label, img, side, *paras, pos='50%'):
    """Copy column beside a tall portrait plate. side: 'left'|'right' = image side.
    pos: horizontal object-position — where the subject sits in the source image."""
    copy = ''.join(f'<p class="copy">{p}</p>' for p in paras)
    frame = (f'<div class="frame"><img src="../assets/images/{img}" alt="" '
             f'style="object-position:{pos} 50%"></div>')
    col = f'<div class="col">{copy}</div>'
    row = frame + col if side == 'left' else col + frame
    return page(f'''
  <div class="slide">
    {head(n, label)}
    <div class="row">{row}</div>
    {foot(n)}
  </div>''', 'split')

def quote_slide(n, label, lead, pull, closing):
    """One line of the review set large in the display face; no image."""
    return page(f'''
  <div class="slide quoteslide">
    {head(n, label)}
    <p class="copy lead-in">{lead}</p>
    <div class="quote-mark">“</div>
    <p class="pull">{pull}</p>
    <p class="copy">{closing}</p>
    {foot(n)}
  </div>''', 'quoteslide')

def textonly_slide(n, label, *paras):
    """No image — for stretches of argument too long to share a slide with one."""
    copy = ''.join(f'<p class="copy">{p}</p>' for p in paras)
    return page(f'''
  <div class="slide">
    {head(n, label)}
    {copy}
    <div class="endmark">◆◆◆</div>
    {foot(n)}
  </div>''', 'textonly')

slides = {}

slides['slide-01-cover'] = page(f'''
  <div class="cover-bg"></div><div class="cover-scrim"></div>
  <div class="slide">
    <p class="kicker">Sandfall Interactive · Game Review</p>
    <h1>Clair Obscur<br>Expedition <span class="num">33</span></h1>
    <div class="cover-meta"><span>PC / PS5</span><span>2025</span><span>~70h played</span></div>
  </div>''', 'cover')

slides['slide-02-premise1'] = content_slide(2, 'Premise · I', 'lumiere.jpg',
    'Set in a dreamlike world inspired by the <em>Belle Époque</em> era, where society lives '
    'under the shadow of a yearly phenomenon called the <strong>Gommage</strong>. Every year, '
    'a godlike entity known as the <strong>Paintress</strong> awakens and paints a single '
    'number on a distant monolith, and every person whose age matches that number is '
    'instantly erased from existence.',
    'The number drops by one each year. A slow, creeping countdown toward total annihilation.')

slides['slide-03-premise2'] = full_slide(3, 'Premise · II', 'gommage.jpg',
    'In response, the people of <strong>Lumière</strong> have been sending out expeditions '
    'across a shattered, surreal continent to find and kill the <strong>Paintress</strong> '
    'and end the cycle once and for all. Every expedition has failed.',
    'With only one year remaining before they too are erased, <strong>Gustave</strong> and '
    'the members of <em>Expedition 33</em> set out on a final, desperate mission.')

slides['slide-04-narrative1'] = textfirst_slide(4, 'Narrative Perspective · I', 'overlook.jpg',
    "I really love how Clair Obscur's narrative method is mainly divided into two sections, "
    'the <em>Question Arcs and the Answer Arcs</em>.',
    "It's a huge point for <strong>immersiveness</strong> and really helps players engage "
    'with the story, from constantly pondering and questioning what the hell happens in '
    'Lumière, trying to connect the dots with scattered info fragments, guessing the meaning '
    'behind dialogue between mysterious people and so on, to later get struck with '
    '<em>huge revelations and plot twists</em>.')

slides['slide-05-narrative2'] = quote_slide(5, 'Narrative Perspective · II',
    'Sandfall Team succeeded in building hype throughout the game and gracefully executed a '
    "supreme ending. <em>It's a choice</em> — you can choose how the game will end and it's "
    'a very <strong>messed up</strong> one.',
    'There is nothing like a True End or one that is able to give the best outcome — it '
    'questions your <strong>morality and creed</strong>.',
    "It's an ending worthy of discussion and debate because of how much <strong>personal "
    'weight</strong> it carries, strengthening the impression even after you finish the game.')

slides['slide-06-artngraphic1'] = full_slide(6, 'Art & Graphic Perspective · I', 'gustave.jpg',
    'If I had one word to describe Clair Obscur, it would be <em>“Cinematic”</em> They put a '
    'generously huge amount of top quality cutscenes that feel <strong>straight out of '
    'movies</strong>, and that also applies to many boss attack patterns as well.',
    "I can't help but sometimes <strong>gaze in awe</strong> witnessing boss moves that are "
    'literally meant to kill you.')

slides['slide-07-artngraphic2'] = split_slide(7, 'Art & Graphic Perspective · II', 'monoco.jpg', 'left',
    "As if that doesn't do enough justice, they put along an <strong>orchestra-level "
    "OST</strong> in like every part of the game that it becomes the game's "
    '<em>identity</em> itself.',
    'Watching incredible scenes unfold symphonized with grand composed music, I can say '
    'Clair Obscur is a literal <strong>piece of art</strong> successfully conveyed into a '
    'medium called “Game.”')

slides['slide-08-gameplay1'] = content_slide(8, 'Gameplay Perspective · I', 'sciel.jpg',
    'Clair Obscur renowned gameplay is their unique <em>Turn-Based “Parry”</em> gameplay. '
    'Players can take an action on enemy turn such as parrying and dodging and honestly that '
    'is also where the <strong>main problem</strong> lies.',
    "Sure it feels new and fresh 7 hours into the game, but for the rest of the 60 hours? "
    "Well, I don't think adding a parry mechanic to a turn-based game is a "
    '<strong>great idea</strong>.')

slides['slide-09-gameplay2'] = full_slide(9, 'Gameplay Perspective · II', 'boss.jpg',
    'The parry mechanics are <strong>unbalanced</strong>. It is easy to execute (as in no '
    "restriction, whenever, whoever, and against ANYTHING) and it's too rewarding. Damage, "
    'Action Points (AP), break gauge, all the advantages are gained through just a '
    '<strong>couple of successful</strong> parries.',
    "<strong>EVERY turn can become YOUR turn</strong> after a few observations of the enemy's "
    "attack pattern. And suddenly it's just a <strong>QTE game disguised as a turn-based "
    'game.</strong>')

slides['slide-10-gameplay3'] = content_slide(10, 'Gameplay Perspective · III', 'creature.jpg',
    "Playing Clair Obscur made me realize that one of the turn-based genre's charms is the "
    '<strong>inevitable pain</strong> your characters are going to endure.',
    'Balancing your comp synergy for both sustain and damage, racking your brain after '
    'failed attempts, getting one-shotted from <strong>unavoidable bullshit boss '
    "damage</strong> because you did not stack enough defense buffs, that's what makes a "
    'turn-based game exciting, and Clair Obscur just abolished it with one '
    '<strong>overused game mechanic.</strong>',
    img_h=330)

slides['slide-11-gameplay4'] = textfirst_slide(11, 'Gameplay Perspective · IV', 'parry.jpg',
    'The parry system also successfully <strong>RUINED</strong> the first half storytelling '
    'experience.',
    'An unconquered continent that <strong>massacred</strong> ALL 67 expeditions, thousands '
    'of soldiers, granting a tragic end for everyone that dares to challenge it should be '
    'unforgiving, threatening, full of suspense and thrill yet it turns out to have a FULL '
    'lineup of creatures that bend with just one <strong>simple motion</strong>. Suddenly '
    'all enemies look <strong>trivial</strong>, defeatable with just enough consistency.')

slides['slide-12-gameplay5'] = textonly_slide(12, 'Gameplay Perspective · V',
    'Even if they manage to fix the <strong>problematic</strong> mechanics, they still have '
    'a lot of <strong>homework</strong> to finish. A perfect example is the '
    "<strong>unbalanced</strong> damage output the player can bring (yes, I'm staring at "
    'you, Maelle).',
    'Throughout the game, enemy difficulty and HP scale gradually, but the damage you, the '
    'player can deal scales <strong>EXPONENTIALLY</strong>. Well, luckily the devs are aware '
    'of this, but instead of fixing it, they decided to add a <strong>simple In-Game '
    'Mods</strong>. You can cap your own damage and multiply enemy HP up to 100x so it '
    "doesn't end too quickly.",
    'When a game needs mods just to make it at least fun, that is arguably an example of '
    '<em>bad game design</em>.')

slides['slide-13-gameplay6'] = content_slide(13, 'Gameplay Perspective · VI', 'turnbased.jpg',
    'The gun mechanic, or <strong>“Free Aim”</strong> on the other hand, is creative and '
    "balanced enough. It doesn't end the character's turn which gives the player more "
    '<strong>versatility</strong> to execute a strategy.',
    'A single bullet costs <strong>one AP (Action Point)</strong>, meaning it drains your '
    'capacity to use certain skills. Some enemies also have <strong>weak points</strong> you '
    'can shoot for a huge chunk of damage, and <strong>destructible objects</strong> you can '
    'break through shooting.',
    img_h=380)

slides['slide-14-gameplay7'] = textfirst_slide(14, 'Gameplay Perspective · VII', 'turnbased.jpg',
    'Many passives and skills also gain benefits from Free Aim that you can '
    '<strong>stack</strong> for great advantage. For example, you can deal a huge amount of '
    'damage without ending a turn, slap debuffs onto opponents, or even better, '
    '<strong>gain more AP</strong>.',
    'If a single bullet costs 1 AP and you can gain AP from shooting, that means you can '
    'turn your revolver into a semi-automatic machine gun capable to deals more damage than '
    "using endgame skills, and it's a fully approved playstyle. <em>They really added an "
    'FPS playstyle instead of improving the turn-based system.</em>',
    img_h=310)

slides['slide-15-verdict'] = page(f'''
  <div class="slide">
    <p class="rating-label">Final Verdict</p>
    <div class="score"><span class="big">3</span><span class="of">/ 5</span></div>
    <div class="diamonds">◆◆◆<span class="off">◆◆</span></div>
    <p class="copy">Clair Obscur excels in <strong>presentation</strong> — scenes and music orchestrated so well it is akin to witnessing a <em>grand opera</em>. Highly recommended even for the narrative experience alone. As for the gameplay, it is <strong>Too forgiving.</strong> Ideal for people with little to no experience in the turn-based genre. And what about seasoned players, you ask?. Well You will probably enjoy the game too <em>only if you are, at least, not a masochist</em>.</p>
    {foot(15)}
  </div>''', 'verdict')

for name, html in slides.items():
    (ROOT / 'slides' / f'{name}.html').write_text(html)
    print('wrote slides/' + name + '.html')

# PNG export lives in export.py (slides/ → export/); build.py just authors the HTML.
sys.stdout.flush()
subprocess.run([sys.executable, str(ROOT / 'export.py')], check=True)

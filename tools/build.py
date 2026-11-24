"""Builds the BuildMarque inner pages and keeps the shared header/footer in sync.

Run:  python3 tools/build.py
"""
import html
import re
from pathlib import Path

from content import INDUSTRIES, PROJECTS, ALL_PROJECTS, FAQ_GENERAL, FAQ_ABOUT, FAQ_INDUSTRIES, U

ROOT = Path(__file__).resolve().parent.parent
V = "30"  # asset version (cache busting)
e = html.escape

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
CHEV = '<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>'
PLUS = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12h14"/></svg>'
LOGO = "https://www.buildmarque.com.au/wp-content/uploads/2026/02/logo-1.png.webp"


# ------------------------------------------------------------------ shared parts
def head(title, desc=""):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)} | BuildMarque</title>
  <meta name="description" content="{e(desc)}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/style.css?v={V}">
</head>
<body>
'''


def nav(active=""):
    a = lambda k: ' class="active"' if active == k else ""
    ind = "\n".join(f'          <a href="{i["slug"]}.html">{i["nav"]}</a>' for i in INDUSTRIES)
    return f'''<nav aria-label="Main">
      <a href="index.html"{a("home")}>Home</a>
      <a href="about.html"{a("about")}>About Us</a>
      <div class="dd">
        <a href="industries.html"{a("industries")}>Industries {CHEV}</a>
        <div class="dd-menu">
{ind}
        </div>
      </div>
      <div class="dd">
        <a href="projects.html"{a("projects")}>Projects {CHEV}</a>
        <div class="dd-menu">
          <a href="projects.html">All Projects</a>
        </div>
      </div>
      <a href="faq.html"{a("faq")}>FAQ</a>
      <a href="contact.html"{a("contact")}>Contact Us</a>
    </nav>'''


def header(active=""):
    return f'''
<header class="site-header">
  <div class="wrap">
    <a class="logo" href="index.html" aria-label="BuildMarque home">
      <img src="{LOGO}" alt="BuildMarque Commercial Interiors">
    </a>
    {nav(active)}
    <div class="header-cta">
      <a class="phone" href="tel:1300601871"><small>Call us</small>1300 601 871</a>
      <a class="btn btn-primary" href="contact.html">Get A Quote</a>
    </div>
    <button class="menu-toggle" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
</header>
'''


def footer():
    fb = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M13.5 21v-7.5h2.5l.4-3h-2.9V8.6c0-.9.3-1.5 1.5-1.5h1.5V4.4c-.3 0-1.2-.1-2.2-.1-2.2 0-3.7 1.3-3.7 3.8v2.4H8v3h2.6V21h2.9z"/></svg>'
    li = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M6.9 8.8H3.6V20h3.3V8.8zM5.2 3.5a1.9 1.9 0 100 3.8 1.9 1.9 0 000-3.8zM20.4 13.6c0-3-1.6-5-4.3-5-1.6 0-2.6.9-3 1.6V8.8H9.9V20h3.3v-5.6c0-1.5.5-2.8 2.1-2.8 1.5 0 1.8 1.4 1.8 2.9V20h3.3v-6.4z"/></svg>'
    ig = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r="1" fill="currentColor" stroke="none"/></svg>'
    return f'''<footer>
  <div class="wrap">
    <div class="cols">
      <div>
        <img class="flogo" src="{LOGO}" alt="BuildMarque">
        <p style="max-width:40ch">BuildMarque is led by a multidisciplinary team of architects, project managers, and site managers who bring deep technical knowledge and hands-on delivery experience to every project.</p>
        <div class="fbadges">
          <img src="https://www.buildmarque.com.au/wp-content/uploads/2026/03/logo-.png.webp" alt="Building and Plumbing Commission">
          <img src="https://www.buildmarque.com.au/wp-content/uploads/2026/01/banner-logo-2.png.webp" alt="ADIA member">
          <img src="https://www.buildmarque.com.au/wp-content/uploads/2026/01/banner-logo-3.png.webp" alt="Master Builders Victoria">
          <img src="https://www.buildmarque.com.au/wp-content/uploads/2026/01/banner-logo-4.png.webp" alt="Registered Building Practitioner">
        </div>
      </div>
      <div><h4>Quick Links</h4><ul><li><a href="index.html">Home</a></li><li><a href="about.html">About Us</a></li><li><a href="industries.html">Industries</a></li><li><a href="projects.html">Projects</a></li><li><a href="faq.html">FAQ</a></li><li><a href="contact.html">Contact Us</a></li><li><a href="https://www.buildmarque.com.au/user-sitemap/" target="_blank" rel="noopener">User Sitemap</a></li></ul></div>
      <div><h4>Get In Touch</h4><ul class="contact-list"><li><a href="https://maps.app.goo.gl/CQ9kJdqJ7uKTg1127" target="_blank" rel="noopener"><i><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 21s-7-6.2-7-11.5a7 7 0 0114 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg></i><span>L19, 180 Lonsdale Street,<br>Melbourne VIC 3000</span></a></li><li><a href="tel:1300601871"><i><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2z"/></svg></i><span>1300 601 871</span></a></li><li><a href="mailto:info@buildmarque.com.au"><i><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 6.5l8.5 6 8.5-6"/></svg></i><span>info@buildmarque.com.au</span></a></li></ul>
        <div class="socials">
          <a href="https://www.facebook.com/people/BuildMarque/100067384023327/" target="_blank" rel="noopener" aria-label="Facebook">{fb}</a>
          <a href="https://www.linkedin.com/company/buildmarqueinteriors" target="_blank" rel="noopener" aria-label="LinkedIn">{li}</a>
          <a href="https://www.instagram.com/buildmarque.ltd/" target="_blank" rel="noopener" aria-label="Instagram">{ig}</a>
        </div></div>
    </div>
    <div class="base"><span>Copyright © 2026 - BuildMarque. All rights reserved.</span><span>Designed By <a href="https://www.digitalmovement.com.au/" target="_blank" rel="noopener">Digital Movement</a></span></div>
  </div>
</footer>
'''


def tail():
    return f'<script src="assets/js/main.js?v={V}"></script>\n</body>\n</html>\n'


def page_hero(img, eyebrow, h1, lead="", crumbs=(), buttons=True, short=False):
    cr = " / ".join([f'<a href="{h}">{e(t)}</a>' if h else e(t) for t, h in crumbs])
    btns = f'''
      <div class="hero-actions" style="margin-top:30px">
        <a class="btn btn-primary" href="contact.html">Book A Free Consultation {ARROW}</a>
        <a class="btn btn-ghost" href="tel:1300601871">1300 601 871</a>
      </div>''' if buttons else ""
    return f'''
<section class="page-hero{' short' if short else ''}">
  <img src="{img}" alt="">
  <div class="wrap">
    <div class="crumbs">{cr}</div>
    <span class="eyebrow light">{e(eyebrow)}</span>
    <h1 class="page-title">{h1}</h1>
    {f'<p class="page-lead">{e(lead)}</p>' if lead else ''}{btns}
  </div>
</section>
'''


def faq_items(faqs, start_open=True, cat=None):
    out = []
    for i, (q, a) in enumerate(faqs):
        op = start_open and i == 0
        c = f' data-cat="{cat}"' if cat else ""
        out.append(f'''        <div class="faq-item{' open' if op else ''}"{c}>
          <button aria-expanded="{'true' if op else 'false'}"><span><span class="n">{i+1:02d}</span>{e(q)}</span><span class="pm">{PLUS}</span></button>
          <div class="ans"><div>{''.join(f'<p>{e(x)}</p>' for x in a)}</div></div>
        </div>''')
    return "\n".join(out)


def faq_section(faqs, h2="Questions, <em>answered</em>.", lead="", img=U + "02/homepage-slider-banner-7-1.jpg", more=True):
    return f'''
<section class="faq">
  <div class="wrap faq-grid">
    <div class="faq-side">
      <span class="eyebrow reveal">FAQs</span>
      <h2 class="h2 reveal">{h2}</h2>
      {f'<p class="lead reveal">{e(lead)}</p>' if lead else ''}
      <div class="faq-card reveal">
        <img loading="lazy" src="{img}" alt="">
        <div><h3>Still have a question?</h3><a class="tel" href="tel:1300601871">1300 601 871</a></div>
      </div>
      {f'<a class="text-link reveal" href="faq.html">View All FAQs {ARROW}</a>' if more else ''}
    </div>
    <div class="faq-list">
{faq_items(faqs)}
    </div>
  </div>
</section>
'''


def cta_band(h2="Have a project in mind? <em>Let’s talk.</em>", p="Tell us about your space. We’ll come back with a concept design and budget proposal.", img=U + "02/homepage-slider-banner-6-1.jpg"):
    return f'''
<section class="cta center">
  <img loading="lazy" src="{img}" alt="">
  <div class="wrap">
    <span class="eyebrow light">Start your project</span>
    <h2 class="h2">{h2}</h2>
    <p class="lead">{e(p)}</p>
    <div class="cta-actions">
      <a class="btn btn-primary" href="contact.html">Book A Free Consultation {ARROW}</a>
      <a class="btn btn-ghost" href="tel:1300601871">1300 601 871</a>
    </div>
  </div>
</section>
'''


SECTOR_LABEL = dict(dental="Dental", medical="Medical", allied="Allied health", corporate="Corporate", opg="OPG &amp; plant rooms")


def project_cards(items):
    out = []
    for n, s, img, link in items:
        out.append(f'''      <a class="p-card reveal" data-sector="{s}" href="{link or 'projects.html#' + s}">
        <div class="ph"><img loading="lazy" src="{U}{img}" alt="{e(n)}"></div>
        <div class="p-meta"><h3>{n if "&amp;" in n else e(n)}</h3><span>{SECTOR_LABEL[s]}</span></div>
        <span class="arrow">{ARROW}</span>
      </a>''')
    return "\n".join(out)


def logo_grid(name, n, cls):
    base = "https://www.buildmarque.com.au/wp-content/uploads/2026/01/"
    tiles = "".join(f'\n      <div class="logo-tile"><img loading="lazy" src="{base}{name}-{k}.jpg.webp" alt=""></div>' for k in range(1, n + 1))
    return f'<div class="logo-grid {cls}">{tiles}\n    </div>'


def write(name, body):
    (ROOT / name).write_text(body)
    print("wrote", name)


# ------------------------------------------------------------------ industry page
def industry_page(d):
    paras = "".join(f'<p class="reveal">{e(p)}</p>' for p in d["intro"])
    lst = "".join(f'<li class="reveal"><span class="n">{i+1:02d}</span>{e(x)}</li>' for i, x in enumerate(d["list"]))
    feats = ""
    if d["features"]:
        cards = "".join(f'<div class="feature reveal"><h3>{e(t)}</h3><p>{e(x)}</p></div>' for t, x in d["features"])
        feats = f'''
<section class="features">
  <div class="wrap">
    <div class="section-head">
      <div><span class="eyebrow reveal">Why it matters</span>
      <h2 class="h2 reveal">Built to <em>perform</em>, from day one.</h2></div>
      <p class="lead reveal">Every technical, regulatory and operational detail is addressed by one accountable team.</p>
    </div>
    <div class="feature-grid">{cards}</div>
  </div>
</section>
'''
    rel = ""
    if d["sector"]:
        items = [p for p in PROJECTS if p[1] == d["sector"]][:6]
        rel = f'''
<section class="projects related">
  <div class="wrap">
    <div class="section-head">
      <div><span class="eyebrow reveal">Our work</span>
      <h2 class="h2 reveal">Recent {e(d["nav"].lower())} <em>projects</em>.</h2></div>
      <div style="justify-self:end"><a class="btn btn-line" href="projects.html#{d["sector"]}">View All Projects {ARROW}</a></div>
    </div>
    <div class="project-grid">
{project_cards(items)}
    </div>
  </div>
</section>
'''
    gal = ""
    if d["gallery"]:
        g = "".join(f'<figure class="reveal"><img loading="lazy" src="{x}" alt=""></figure>' for x in d["gallery"])
        gal = f'''
<section class="ind-gallery">
  <div class="wrap">
    <span class="eyebrow reveal">Gallery</span>
    <div class="ind-gallery-grid n{len(d["gallery"])}">{g}</div>
  </div>
</section>
'''
    others = "".join(f'<a class="chip-link" href="{i["slug"]}.html">{i["nav"]} {ARROW}</a>' for i in INDUSTRIES if i["slug"] != d["slug"])
    body = (head(d["title"], d["lead"]) + header("industries")
            + page_hero(d["banner"], d["eyebrow"], e(d["h1"]), d["lead"], crumbs=(("Home", "index.html"), ("Industries", "industries.html"), (d["nav"], "")))
            + f'''
<section class="ind-intro">
  <div class="wrap ind-intro-grid">
    <div class="ind-copy">
      <span class="eyebrow reveal">Overview</span>
      <h2 class="h2 reveal">{e(d["intro_h2"])}</h2>
      {paras}
    </div>
    <div class="ind-imgs reveal">
      <img loading="lazy" src="{d["intro_imgs"][0]}" alt="">
      <img loading="lazy" src="{d["intro_imgs"][1]}" alt="">
    </div>
  </div>
</section>

<section class="included">
  <div class="wrap">
    <div class="section-head">
      <div><span class="eyebrow reveal">Scope</span>
      <h2 class="h2 reveal">{e(d["list_h2"])}</h2></div>
      <p class="lead reveal" style="color:rgba(255,255,255,.72)">One team takes care of design, approvals and construction, so nothing falls between the gaps.</p>
    </div>
    <ul class="included-list">{lst}</ul>
  </div>
</section>
''' + feats + gal + rel
            + faq_section(d["faqs"], h2=f'{e(d["nav"])} <em>FAQs</em>.', lead="Common questions from practice owners and operators.")
            + cta_band(h2=f'{e(d["closing_h2"])}', p=d["closing"])
            + f'''
<section class="other-inds">
  <div class="wrap">
    <span class="eyebrow">Other industries</span>
    <div class="chip-links">{others}</div>
  </div>
</section>
''' + footer() + tail())
    write(f'{d["slug"]}.html', body)


# ------------------------------------------------------------------ industries overview
def industries_page():
    cards = "".join(f'''
      <a class="ind-card reveal" href="{d["slug"]}.html">
        <div class="ph"><img loading="lazy" src="{d["card_img"]}" alt=""></div>
        <div class="body"><span class="num">{i+1:02d}</span><h3>{e(d["nav"])}</h3><p>{e(d["card_text"])}</p><span class="go">Explore {ARROW}</span></div>
      </a>''' for i, d in enumerate(INDUSTRIES))
    body = (head("Industries We Deliver Specialist Fitouts For", "Medical, dental, corporate, allied health, radiology, veterinary, pharmacy and gym fitouts across Victoria.") + header("industries")
            + page_hero(U + "02/industries-banner-c.jpg", "Industries", "Industries we deliver <em>specialist</em> fitouts for", "Every industry has different regulatory, clinical and operational needs. We design and build around yours.", crumbs=(("Home", "index.html"), ("Industries", "")))
            + f'''
<section class="ind-overview">
  <div class="wrap">
    <div class="section-head">
      <div><span class="eyebrow reveal">Nine specialisms</span>
      <h2 class="h2 reveal">Find your <em>industry</em>.</h2></div>
      <p class="lead reveal">Rather than applying a standard commercial layout, our design and construction process adapts to the workflow, equipment and compliance needs of each practice or workspace.</p>
    </div>
    <div class="ind-cards">{cards}
    </div>
  </div>
</section>

<section class="ind-intro alt">
  <div class="wrap ind-intro-grid">
    <div class="ind-copy">
      <span class="eyebrow reveal">Design &amp; equipment</span>
      <h2 class="h2 reveal">Skilled designers for healthcare <em>interiors</em>.</h2>
      <p class="reveal">Our experts create healthcare interiors that enhance a clinic’s appeal while leaving the right space for medical equipment. We assess and measure every space to prepare accurate layouts.</p>
      <p class="reveal">We also help you choose quality medical fitouts, equipment and machines that improve functionality and help you treat patients better.</p>
      <p class="reveal">For corporate, residential and industrial clients we offer commercial interior design services that meet your vision while staying practical.</p>
    </div>
    <div class="ind-imgs reveal">
      <img loading="lazy" src="{U}02/consult-img.jpg" alt="">
      <img loading="lazy" src="{U}02/best-img.jpg" alt="">
    </div>
  </div>
</section>
''' + faq_section(FAQ_INDUSTRIES, h2="Industry <em>FAQs</em>.", lead="How we tailor each fitout to the people who use it.")
            + cta_band() + footer() + tail())
    write("industries.html", body)


# ------------------------------------------------------------------ about
def about_page():
    services = ["Concept and interior design", "Detailed construction drawings and specifications", "Building permit and authority approvals", "Materials, finishes, fixtures and equipment selection", "Services coordination and consultant management", "Fit-out, refurbishment, extensions and new builds", "Full turnkey construction, commissioning and handover"]
    lst = "".join(f'<li class="reveal"><span class="n">{i+1:02d}</span>{e(x)}</li>' for i, x in enumerate(services))
    quals = [("2005", "Bachelor of Architectural Engineering"), ("2010", "Project Management Professional (PMP), Project Management Institute"), ("2014", "LEED Green Associate, U.S. Green Building Council"), ("2018", "Diploma of Building and Construction, Victoria"), ("2019", "Registered Building Practitioner, VBA, Commercial Builder (CBL)"), ("2023", "Active Member, Australian Dental Industry Association (ADIA)"), ("2024", "Active Member, Master Builders Victoria")]
    ql = "".join(f'<li><b>{y}</b><span>{e(t)}</span></li>' for y, t in quals)
    body = (head("About BuildMarque, Melbourne Fitout Designers and Builders", "Australian-owned specialist healthcare design and construction company delivering dental, medical and allied health interiors across Victoria.") + header("about")
            + page_hero(U + "02/about-us-banner.jpg", "About us", "Designers and builders of <em>healthcare</em> interiors", "Australian owned and operated, delivering dental, medical and allied health environments across Victoria.", crumbs=(("Home", "index.html"), ("About Us", "")))
            + f'''
<section class="about-intro">
  <div class="wrap">
    <div class="about-grid">
      <div class="about-photo reveal"><img loading="lazy" src="{U}05/bout-Us.jpg" alt="Melbourne Dental Group reception by BuildMarque"></div>
      <div>
        <span class="eyebrow reveal">About BuildMarque</span>
        <p class="statement reveal" style="margin-top:20px">We work exclusively in sectors where compliance, safety and operational performance are critical, delivering spaces that are functional, compliant and <em>architecturally refined</em>.</p>
        <p class="lead reveal" style="margin-top:28px;max-width:62ch">Our strength lies in our people. BuildMarque is led by a multidisciplinary team of architects, project managers and site managers who bring deep technical knowledge and hands-on delivery experience to every project, managing complexity, controlling risk and staying accountable from the first design discussion to final handover.</p>
      </div>
    </div>
    <div class="stats reveal">
      <div class="stat"><b data-count="200" data-suffix="+">200+</b><span>Projects delivered</span></div>
      <div class="stat"><b data-count="20" data-suffix="+">20+</b><span>Years’ experience</span></div>
      <div class="stat"><b>0</b><span>Incidents on site</span></div>
      <div class="stat"><b>1</b><span>Team, design to handover</span></div>
    </div>
  </div>
</section>

<section class="ind-intro alt">
  <div class="wrap ind-intro-grid">
    <div class="ind-copy">
      <span class="eyebrow reveal">Specialists</span>
      <h2 class="h2 reveal">Healthcare interior design &amp; construction <em>specialists</em>.</h2>
      <p class="reveal">Healthcare environments demand precision and technical understanding well beyond standard commercial interiors. We have extensive experience designing and building dental and medical practices, including new builds, extensions, refurbishments and live-environment upgrades.</p>
      <p class="reveal">Our team understands clinical workflows, infection control, equipment coordination, services integration, acoustic and lighting performance, and the regulations governing healthcare facilities, and builds them into every design.</p>
      <p class="reveal">Just as importantly, we create calm, professional interiors that enhance patient confidence while supporting staff efficiency and wellbeing.</p>
    </div>
    <div class="ind-imgs reveal">
      <img loading="lazy" src="{U}02/about-img-2.jpg" alt="">
      <img loading="lazy" src="{U}02/melton-dental-house-4-1.jpg" alt="">
    </div>
  </div>
</section>

<section class="ind-intro">
  <div class="wrap ind-intro-grid rev">
    <div class="ind-copy">
      <span class="eyebrow reveal">How we work</span>
      <h2 class="h2 reveal">Design-led. <em>Build-focused.</em></h2>
      <p class="reveal">We start at concept design, investing time to understand your vision, clinical requirements, operational objectives and brand identity.</p>
      <p class="reveal">From there we move through full construction documentation, consultant coordination and building permit approvals, with drawings developed for buildability, compliance and cost certainty.</p>
      <p class="reveal">We also guide you through materials, finishes, fixtures, fittings and healthcare-specific equipment, so every selection meets regulations while achieving a cohesive, refined result.</p>
    </div>
    <div class="ind-imgs reveal">
      <img loading="lazy" src="{U}02/work-img-1.jpg" alt="">
      <img loading="lazy" src="{U}02/what-img-2.jpg" alt="">
    </div>
  </div>
</section>

<section class="included">
  <div class="wrap">
    <div class="section-head">
      <div><span class="eyebrow reveal">True turnkey service</span>
      <h2 class="h2 reveal">One point of responsibility, <em>start to finish</em>.</h2></div>
      <p class="lead reveal" style="color:rgba(255,255,255,.72)">Continuity between design intent and construction, with confidence, transparency and control for our clients.</p>
    </div>
    <ul class="included-list">{lst}</ul>
  </div>
</section>

<section class="features">
  <div class="wrap">
    <div class="section-head">
      <div><span class="eyebrow reveal">Safety &amp; quality</span>
      <h2 class="h2 reveal">No margin for <em>error</em>.</h2></div>
      <p class="lead reveal">Rigorous safety management, licensed and insured trades, and compliance checks at every stage.</p>
    </div>
    <div class="feature-grid">
      <div class="feature reveal"><h3>Zero-incident record</h3><p>Disciplined planning, proactive risk management and strong site supervision across every project.</p></div>
      <div class="feature reveal"><h3>Licensed &amp; insured trades</h3><p>All subcontractors are fully licensed, qualified and carry the required insurances, including public liability.</p></div>
      <div class="feature reveal"><h3>Built-in quality control</h3><p>Compliance checks at every stage ensure works meet or exceed Australian standards and healthcare regulations.</p></div>
    </div>
  </div>
</section>

<section class="leader">
  <div class="wrap leader-grid">
    <div class="leader-photo reveal"><img loading="lazy" src="{U}05/About-Us.jpg" alt="Matthew Issa, Founder and Director of BuildMarque"></div>
    <div class="leader-copy">
      <span class="eyebrow reveal">Leadership</span>
      <h2 class="h2 reveal">Muhannad (Matthew) <em>Issa</em></h2>
      <p class="role reveal">Founder &amp; Director · Principal Architectural Designer · Registered Commercial Builder (VIC)</p>
      <p class="reveal">Matthew brings over 20 years of international experience delivering complex healthcare, commercial and government projects, the past 10 years in Australia, with earlier work across the Middle East and the United States.</p>
      <p class="reveal">His background spans architectural engineering, project management, sustainability and statutory building practice. His leadership is hands-on and detail-driven, ensuring senior-level oversight and accountability on every project.</p>
      <ul class="quals reveal">{ql}</ul>
    </div>
  </div>
</section>

<section class="logos">
  <div class="wrap">
    <div class="logo-block">
      <div class="logo-head"><span class="eyebrow">Our recent clients</span></div>
    {logo_grid("client-logo", 41, "clients")}
    </div>
  </div>
</section>
''' + faq_section(FAQ_ABOUT, h2="About <em>BuildMarque</em>.", lead="Who we are and how we work.")
            + cta_band() + footer() + tail())
    write("about.html", body)


# ------------------------------------------------------------------ FAQ
def faq_page():
    groups = [("general", "General", FAQ_GENERAL), ("about", "About BuildMarque", FAQ_ABOUT), ("industries", "Industries", FAQ_INDUSTRIES)]
    tabs = '<button class="on" data-cat="all">All</button>' + "".join(f'<button data-cat="{k}">{t}</button>' for k, t, _ in groups)
    items = []
    n = 0
    for k, t, fs in groups:
        for q, a in fs:
            n += 1
            op = n == 1
            items.append(f'''        <div class="faq-item{' open' if op else ''}" data-cat="{k}">
          <button aria-expanded="{'true' if op else 'false'}"><span><span class="n">{n:02d}</span>{e(q)}</span><span class="pm">{PLUS}</span></button>
          <div class="ans"><div>{''.join(f'<p>{e(x)}</p>' for x in a)}</div></div>
        </div>''')
    body = (head("Frequently Asked Questions", "Answers to common questions about commercial and healthcare fitouts with BuildMarque.") + header("faq")
            + page_hero(U + "02/homepage-slider-banner-4-1.jpg", "FAQ", "Frequently asked <em>questions</em>", "Everything practice owners usually ask before starting a fitout.", crumbs=(("Home", "index.html"), ("FAQ", "")), buttons=False, short=True)
            + f'''
<section class="faq faq-page">
  <div class="wrap faq-grid">
    <div class="faq-side">
      <span class="eyebrow">Browse by topic</span>
      <div class="filters faq-tabs">{tabs}</div>
      <div class="faq-card">
        <img loading="lazy" src="{U}02/homepage-slider-banner-7-1.jpg" alt="">
        <div><h3>Still have a question?</h3><a class="tel" href="tel:1300601871">1300 601 871</a></div>
      </div>
      <a class="text-link" href="contact.html">Send Us A Message {ARROW}</a>
    </div>
    <div class="faq-list">
{chr(10).join(items)}
    </div>
  </div>
</section>
''' + cta_band() + footer() + tail())
    write("faq.html", body)


# ------------------------------------------------------------------ contact
def contact_page():
    body = (head("Contact Us | Book a Free Fitout Consultation", "Call 1300 601 871 or send a message to book a free fitout consultation with BuildMarque.") + header("contact")
            + page_hero(U + "02/homepage-slider-banner-6-1.jpg", "Contact us", "Have a project in mind? <em>Let’s make it happen.</em>", "Book a free consultation and we’ll come back with a concept design and budget proposal.", crumbs=(("Home", "index.html"), ("Contact Us", "")), buttons=False, short=True)
            + f'''
<section class="contact-main">
  <div class="wrap contact-grid">
    <div class="contact-info">
      <span class="eyebrow reveal">Get in touch</span>
      <h2 class="h2 reveal">Talk to the <em>team</em>.</h2>
      <p class="lead reveal">Ready to transform your workspace? Call, email or send us a few details and we’ll respond promptly.</p>
      <div class="info-cards">
        <a class="info-card reveal" href="tel:1300601871"><small>Call</small><b>1300 601 871</b></a>
        <a class="info-card reveal" href="mailto:info@buildmarque.com.au"><small>Email</small><b>info@buildmarque.com.au</b></a>
        <a class="info-card reveal" href="https://www.google.com/maps/dir/?api=1&amp;destination=180+Lonsdale+Street+Melbourne+VIC+3000" target="_blank" rel="noopener"><small>Visit</small><b>Level 19, 180 Lonsdale Street<br>Melbourne VIC 3000</b></a>
      </div>
    </div>
    <div class="contact-form reveal">
      <h3>Request a free consultation</h3>
      <form class="quote light">
        <label>Name<input type="text" required></label>
        <label>Phone<input type="tel"></label>
        <label class="full">Email<input type="email" required></label>
        <div class="field"><span class="flabel">Project type</span>
          <select><option>Dental practice</option><option>Medical centre</option><option>Allied health</option><option>Corporate office</option><option>Radiology</option><option>Veterinary</option><option>Pharmacy</option><option>Gym</option><option>Other</option></select>
        </div>
        <div class="field"><span class="flabel">Stage</span>
          <select><option>Just exploring</option><option>Have a site</option><option>Ready to build</option></select>
        </div>
        <label class="full">Tell us about the project<textarea></textarea></label>
        <button class="btn btn-dark" type="submit">Request A Consultation {ARROW}</button>
      </form>
    </div>
  </div>
</section>

<section class="visit" id="visit">
  <iframe title="BuildMarque office on Google Maps" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
    src="https://maps.google.com/maps?q=180%20Lonsdale%20Street%2C%20Melbourne%20VIC%203000&z=16&output=embed"></iframe>
  <div class="wrap">
    <div class="visit-card reveal">
      <span class="eyebrow">Visit us</span>
      <h3>Our Melbourne office</h3>
      <address>Level 19, 180 Lonsdale Street<br>Melbourne VIC 3000</address>
      <div class="lines"><a href="tel:1300601871">1300 601 871</a><a href="mailto:info@buildmarque.com.au">info@buildmarque.com.au</a></div>
      <a class="btn btn-dark" href="https://www.google.com/maps/dir/?api=1&amp;destination=180+Lonsdale+Street+Melbourne+VIC+3000" target="_blank" rel="noopener">Get Directions {ARROW}</a>
    </div>
  </div>
</section>
''' + faq_section(FAQ_GENERAL[:5], h2="Before you <em>call</em>.", lead="Quick answers to the questions we hear most.")
            + footer() + tail())
    write("contact.html", body)



# ------------------------------------------------------------------ projects archive
def projects_page():
    tabs = [("all", "All projects"), ("dental", "Dental"), ("medical", "Medical"), ("allied", "Allied health"), ("corporate", "Corporate"), ("opg", "OPG &amp; plant rooms")]
    t = "".join(f'<button{" class=\"on\"" if k == "all" else ""} data-filter="{k}">{v}</button>' for k, v in tabs)
    body = (head("Projects | Healthcare & Commercial Fitouts", "Dental, medical, allied health and corporate fitouts designed and built by BuildMarque across Victoria.") + header("projects")
            + page_hero(U + "05/Home_Banner_04.jpg", "Projects", "Projects that define <em>our</em> standard", "Every project below was designed and built by BuildMarque, many inside practices that stayed open throughout.", crumbs=(("Home", "index.html"), ("Projects", "")), buttons=False, short=True)
            + f'''
<section class="projects" id="work">
  <div class="wrap">
    <div class="section-head">
      <div>
        <span class="eyebrow reveal">All projects · <b data-count-shown>{len(ALL_PROJECTS)}</b> shown</span>
        <h2 class="h2 reveal">Selected <em>work</em>.</h2>
      </div>
      <p class="lead reveal">Filter by sector to explore dental practices, medical centres, allied health clinics, offices and specialist rooms.</p>
    </div>
    <div class="filters" role="tablist">{t}</div>
    <div class="project-grid">
{project_cards(ALL_PROJECTS)}
    </div>
  </div>
</section>
''' + cta_band(h2="Your practice could be <em>next</em>.") + footer() + tail())
    write("projects.html", body)


# ------------------------------------------------------------------ sync existing pages
def sync_existing():
    for name, active in [("index.html", "home"), ("project.html", "projects")]:
        p = ROOT / name
        s = p.read_text()
        s = re.sub(r'<nav aria-label="Main">.*?</nav>', nav(active), s, count=1, flags=re.S)
        s = re.sub(r"<footer>.*?</footer>\n", footer(), s, count=1, flags=re.S)
        s = re.sub(r'assets/css/style\.css\?v=\d+', f"assets/css/style.css?v={V}", s)
        s = re.sub(r'assets/js/main\.js\?v=\d+', f"assets/js/main.js?v={V}", s)
        s = s.replace('class="btn btn-primary" href="#contact">Get A Quote', 'class="btn btn-primary" href="contact.html">Get A Quote')
        s = s.replace('class="btn btn-primary" href="index.html#contact">Get A Quote', 'class="btn btn-primary" href="contact.html">Get A Quote')
        if name == "index.html":
            for slug, sec in [("dental-practices", "dental"), ("medical-centres", "medical"), ("allied-health", "allied"), ("corporate-offices", "corporate")]:
                s = s.replace(f'<a class="panel" href="projects.html#{sec}">', f'<a class="panel" href="{slug}.html">')
            if "View All FAQs" not in s:
                s = s.replace('''        <div><h3>Still have a question?</h3><a class="tel" href="tel:1300601871">1300 601 871</a></div>
      </div>
    </div>''', f'''        <div><h3>Still have a question?</h3><a class="tel" href="tel:1300601871">1300 601 871</a></div>
      </div>
      <a class="text-link" href="faq.html">View All FAQs {ARROW}</a>
    </div>''', 1)
        p.write_text(s)
        print("synced", name)


if __name__ == "__main__":
    for d in INDUSTRIES:
        industry_page(d)
    industries_page()
    about_page()
    faq_page()
    contact_page()
    projects_page()
    sync_existing()

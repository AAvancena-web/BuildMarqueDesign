# BuildMarque — website redesign concept

Static prototype of the redesigned **buildmarque.com.au**, for client review before the design is rebuilt on the existing WordPress site.

## Pages
- `index.html` — homepage: full-screen video hero with "Watch the film" modal, intro + stats, drag-to-scroll photo showcase, featured project spotlight, filterable project grid, sectors, process, curated reviews, client logos, enquiry form.
- `project.html` — case study template (Melbourne Dental Group): hero, write-up, "The job in short" facts table, sticky enquiry box, full photo gallery with lightbox, client quote.
- `projects.html` — All projects: same equal-size card grid as the homepage, with sector filters (supports links like `projects.html#dental`).

- Inner pages: `about.html`, `industries.html`, 9 industry pages (`medical-centres`, `dental-practices`, `corporate-offices`, `allied-health`, `radiology-fitouts`, `healthcare-fitouts`, `veterinary-fitouts`, `pharmacy-fitouts`, `gym-fitouts`), `faq.html`, `contact.html`.

## Editing
Inner pages are generated: edit copy in `tools/content.py` (or layout in `tools/build.py`), then run `python3 tools/build.py`. It also keeps the menu and footer in sync on `index.html`, `project.html` and `projects.html`.
Copy comes from the live site, shortened and lightly tidied; industry pages show 3–5 of each page's FAQs. The ~680 SEO/suburb pages in the live sitemap are left for the WordPress build.

## Inspiration (Awwwards)
- Hero video that shrinks into a framed card as you scroll — PDA Architecture (pda.archi)
- Full-height sector image panels that expand on hover — LPAS (lpas.com)
- Split screens: sticky text beside scrolling photos (intro + process) — BCG Building Design (bcgbuildingdesign.com.au)
- "The job in short" table + sticky enquiry box on case studies — DC Carpentry & Construction (dcspaces.co.uk)
- (Archive timeline idea from Archivio Garonzi was replaced by the homepage-style grid at client request)

## Notes for the WordPress rebuild
- All photos and the hero video are loaded directly from the live site's media library — nothing new needs uploading for review.
- Project photos on the live site are only 537 px wide and carry a "Bm" watermark. For the final build, ask the client for the original high-resolution, un-watermarked photos.
- Items marked **To confirm** on the case study (location, size, surgeries, build time) need input from BuildMarque.
- The enquiry form is visual only; in WordPress it would connect to the existing form plugin.
- Sector panel and process photos are stand-ins taken from the homepage banners; swap for the right project photos per sector.
- Fonts: Instrument Serif (headings) + Manrope (body), from Google Fonts.

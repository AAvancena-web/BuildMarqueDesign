// BuildMarque redesign prototype — interactions
(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];

  // Header: solid background once the hero is scrolled past a little
  const header = $('.site-header');
  const onScroll = () => header && header.classList.toggle('scrolled', window.scrollY > 60);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  // Mobile menu
  const toggle = $('.menu-toggle');
  const nav = $('.site-header nav');
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      nav.classList.toggle('open');
      document.body.style.overflow = nav.classList.contains('open') ? 'hidden' : '';
    });
    $$('a', nav).forEach(a => a.addEventListener('click', () => {
      nav.classList.remove('open');
      document.body.style.overflow = '';
    }));
  }

  // Reveal on scroll
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
  $$('.reveal').forEach(el => io.observe(el));

  // Count-up stats
  const counters = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      const el = e.target, end = +el.dataset.count, suffix = el.dataset.suffix || '';
      const t0 = performance.now(), dur = 1600;
      const tick = t => {
        const p = Math.min(1, (t - t0) / dur), v = Math.round(end * (1 - Math.pow(1 - p, 3)));
        el.textContent = v + suffix;
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
      counters.unobserve(el);
    });
  }, { threshold: 0.6 });
  $$('[data-count]').forEach(el => counters.observe(el));

  // Drag-to-scroll showcase strip
  $$('.strip').forEach(strip => {
    let down = false, startX = 0, startLeft = 0;
    strip.addEventListener('pointerdown', e => {
      if (e.pointerType !== 'mouse') return;
      down = true; startX = e.clientX; startLeft = strip.scrollLeft; strip.classList.add('dragging');
    });
    window.addEventListener('pointerup', () => { down = false; strip.classList.remove('dragging'); });
    window.addEventListener('pointermove', e => { if (down) strip.scrollLeft = startLeft - (e.clientX - startX); });
    const wrap = strip.closest('section');
    const step = () => strip.clientWidth * 0.6;
    wrap && $('[data-strip="prev"]', wrap)?.addEventListener('click', () => strip.scrollBy({ left: -step(), behavior: 'smooth' }));
    wrap && $('[data-strip="next"]', wrap)?.addEventListener('click', () => strip.scrollBy({ left: step(), behavior: 'smooth' }));
  });

  // Project filters
  const filterBtns = $$('.filters button');
  filterBtns.forEach(btn => btn.addEventListener('click', () => {
    filterBtns.forEach(b => b.classList.toggle('on', b === btn));
    const f = btn.dataset.filter;
    $$('.p-card').forEach(card => card.classList.toggle('hide', f !== 'all' && card.dataset.sector !== f));
  }));

  // Gentle parallax on spotlight image
  const para = $$('[data-parallax]');
  if (para.length && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const run = () => {
      para.forEach(img => {
        const r = img.parentElement.getBoundingClientRect();
        if (r.bottom < 0 || r.top > innerHeight) return;
        const p = (r.top + r.height / 2 - innerHeight / 2) / innerHeight;
        img.style.transform = `translateY(${p * -60 - 40}px)`;
      });
    };
    run();
    window.addEventListener('scroll', () => requestAnimationFrame(run), { passive: true });
  }

  // Film modal
  const filmModal = $('#film');
  if (filmModal) {
    const v = $('video', filmModal);
    const open = () => { filmModal.classList.add('open'); v.currentTime = 0; v.muted = false; v.play().catch(() => {}); };
    const close = () => { filmModal.classList.remove('open'); v.pause(); };
    $$('[data-film]').forEach(b => b.addEventListener('click', open));
    $('.close', filmModal).addEventListener('click', close);
    filmModal.addEventListener('click', e => { if (e.target === filmModal) close(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
  }

  // Gallery lightbox
  const lb = $('#lightbox');
  if (lb) {
    const items = $$('.gallery button');
    const img = $('img', lb), count = $('.count', lb);
    let i = 0;
    const show = n => {
      i = (n + items.length) % items.length;
      img.src = items[i].dataset.full;
      count.textContent = `${i + 1} / ${items.length}`;
    };
    items.forEach((b, n) => b.addEventListener('click', () => { show(n); lb.classList.add('open'); }));
    $('.prev', lb).addEventListener('click', () => show(i - 1));
    $('.next', lb).addEventListener('click', () => show(i + 1));
    $('.close', lb).addEventListener('click', () => lb.classList.remove('open'));
    lb.addEventListener('click', e => { if (e.target === lb) lb.classList.remove('open'); });
    document.addEventListener('keydown', e => {
      if (!lb.classList.contains('open')) return;
      if (e.key === 'Escape') lb.classList.remove('open');
      if (e.key === 'ArrowLeft') show(i - 1);
      if (e.key === 'ArrowRight') show(i + 1);
    });
  }

  // Prototype form: don't actually submit
  $$('form.quote').forEach(f => f.addEventListener('submit', e => {
    e.preventDefault();
    const b = $('button', f);
    b.textContent = 'Thanks — prototype only';
  }));

  // ---------- v2 ----------
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Hero video shrinks into a framed card as you scroll
  const hero = $('.hero'), heroMedia = $('.hero-media'), heroContent = $('.hero-content');
  if (hero && heroMedia) {
    const run = () => {
      const p = Math.min(1, Math.max(0, window.scrollY / hero.offsetHeight));
      if (!reduce) {
        const inset = p * 7;
        heroMedia.style.clipPath = `inset(${inset}% ${inset}% ${inset}% ${inset}% round ${p * 22}px)`;
        if (heroContent) {
          heroContent.style.opacity = String(1 - p * 1.6);
          heroContent.style.transform = `translateY(${p * -60}px)`;
        }
      }
      const cue = $('.scroll-cue'); if (cue) cue.style.opacity = String(1 - p * 3);
    };
    run();
    window.addEventListener('scroll', () => requestAnimationFrame(run), { passive: true });
  }

  // Process: highlight the step whose image is in view; click a step to jump to its image
  const stepItems = $$('.steps li');
  if (stepItems.length) {
    const figs = $$('.process .split-media figure');
    const sio = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (!e.isIntersecting) return;
        const n = e.target.dataset.step;
        stepItems.forEach(li => li.classList.toggle('on', li.dataset.step === n));
      });
    }, { rootMargin: '-45% 0px -45% 0px' });
    figs.forEach(f => sio.observe(f));
    stepItems.forEach(li => li.addEventListener('click', () => {
      const f = figs.find(x => x.dataset.step === li.dataset.step);
      if (f) window.scrollTo({ top: f.getBoundingClientRect().top + scrollY - innerHeight * 0.04, behavior: 'smooth' });
    }));
  }

  // All projects timeline: wheel scrolls sideways, drag, progress bar, filters (+ #hash)
  const tl = $('.timeline');
  if (tl) {
    tl.addEventListener('wheel', e => {
      if (Math.abs(e.deltaY) > Math.abs(e.deltaX)) {
        const atStart = tl.scrollLeft <= 0 && e.deltaY < 0;
        const atEnd = tl.scrollLeft + tl.clientWidth >= tl.scrollWidth - 1 && e.deltaY > 0;
        if (!atStart && !atEnd) { e.preventDefault(); tl.scrollLeft += e.deltaY; }
      }
    }, { passive: false });
    let down = false, sx = 0, sl = 0, moved = false;
    tl.addEventListener('pointerdown', e => { if (e.pointerType !== 'mouse') return; down = true; moved = false; sx = e.clientX; sl = tl.scrollLeft; });
    window.addEventListener('pointermove', e => { if (!down) return; if (Math.abs(e.clientX - sx) > 4) { moved = true; tl.classList.add('dragging'); } tl.scrollLeft = sl - (e.clientX - sx); });
    window.addEventListener('pointerup', () => { down = false; tl.classList.remove('dragging'); });
    tl.addEventListener('click', e => { if (moved) { e.preventDefault(); moved = false; } }, true);
    const bar = $('.progress i');
    const upd = () => { if (bar) bar.style.width = (tl.scrollLeft / Math.max(1, tl.scrollWidth - tl.clientWidth) * 100) + '%'; };
    tl.addEventListener('scroll', upd, { passive: true }); upd();

    const btns = $$('.index-head .filters button');
    const count = $('[data-count-shown]');
    const apply = f => {
      btns.forEach(b => b.classList.toggle('on', b.dataset.filter === f));
      let n = 0;
      $$('.col', tl).forEach(c => { const show = f === 'all' || c.dataset.sector === f; c.classList.toggle('hide', !show); if (show) n++; });
      if (count) count.textContent = n;
      tl.scrollLeft = 0; upd();
    };
    btns.forEach(b => b.addEventListener('click', () => { apply(b.dataset.filter); history.replaceState(null, '', b.dataset.filter === 'all' ? location.pathname : '#' + b.dataset.filter); }));
    const hash = location.hash.slice(1);
    if (hash && btns.some(b => b.dataset.filter === hash)) apply(hash);
  }
})();

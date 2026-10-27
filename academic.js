(() => {
  const body = document.body;
  const theme = document.querySelector('.theme-toggle');
  let saved;
  try { saved = localStorage.getItem('site-theme'); } catch (_) {}
  const setTheme = dark => {
    body.classList.toggle('dark', dark);
    theme?.setAttribute('aria-label', `Switch to ${dark ? 'light' : 'dark'} theme`);
    theme?.setAttribute('aria-pressed', String(dark));
  };
  setTheme(saved ? saved === 'dark' : window.matchMedia('(prefers-color-scheme: dark)').matches);
  theme?.addEventListener('click', () => {
    const dark = !body.classList.contains('dark');
    setTheme(dark);
    try { localStorage.setItem('site-theme', dark ? 'dark' : 'light'); } catch (_) {}
  });
  const header = document.querySelector('.site-header');
  const menu = document.querySelector('.menu-toggle');
  const closeMenu = () => {
    header?.classList.remove('is-open');
    menu?.setAttribute('aria-expanded', 'false');
    menu?.setAttribute('aria-label', 'Open navigation');
  };
  menu?.addEventListener('click', () => {
    const open = header.classList.toggle('is-open');
    menu.setAttribute('aria-expanded', String(open));
    menu.setAttribute('aria-label', `${open ? 'Close' : 'Open'} navigation`);
  });
  document.querySelectorAll('nav a').forEach(link => link.addEventListener('click', closeMenu));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') { closeMenu(); if (document.activeElement?.closest('nav')) menu?.focus(); } });
  const filters = document.querySelectorAll('[data-filter]');
  const projects = document.querySelectorAll('[data-category]');
  filters.forEach(button => button.addEventListener('click', () => {
    filters.forEach(filter => filter.setAttribute('aria-pressed', String(filter === button)));
    let count = 0;
    projects.forEach(project => {
      project.hidden = button.dataset.filter !== 'all' && button.dataset.filter !== project.dataset.category;
      if (!project.hidden) count++;
    });
    const status = document.querySelector('.filter-count');
    if (status) status.textContent = `${count} ${count === 1 ? 'project' : 'projects'}`;
  }));
})();

// Numbered news pages: hover on desktop, focus for keyboards, click for touch.
(() => {
  const news = document.querySelector('[data-news-items]');
  const controls = document.querySelector('[data-news-pagination]');
  if (!news || !controls) return;
  const items = Array.from(news.querySelectorAll('article'));
  const pageSize = 4;
  const pageCount = Math.ceil(items.length / pageSize);
  if (pageCount < 2) return;
  const status = document.querySelector('[data-news-status]');
  const buttons = [];
  const showPage = page => {
    items.forEach((item, index) => { item.hidden = Math.floor(index / pageSize) !== page; });
    news.querySelectorAll('[data-news-year]').forEach(group => {
      group.hidden = !Array.from(group.querySelectorAll('article')).some(item => !item.hidden);
    });
    buttons.forEach((button, index) => {
      button.setAttribute('aria-pressed', String(index === page));
      if (index === page) button.setAttribute('aria-current', 'page');
      else button.removeAttribute('aria-current');
    });
    if (status) status.textContent = `Page ${page + 1} of ${pageCount}`;
  };
  for (let page = 0; page < pageCount; page++) {
    const button = document.createElement('button');
    button.type = 'button';
    button.textContent = String(page + 1);
    button.setAttribute('aria-label', `Show updates page ${page + 1}`);
    button.setAttribute('aria-controls', news.id);
    button.addEventListener('pointerenter', event => {
      if (event.pointerType === 'mouse') showPage(page);
    });
    button.addEventListener('focus', () => showPage(page));
    button.addEventListener('click', () => showPage(page));
    button.addEventListener('keydown', event => {
      let target;
      if (event.key === 'ArrowRight') target = (page + 1) % pageCount;
      if (event.key === 'ArrowLeft') target = (page + pageCount - 1) % pageCount;
      if (event.key === 'Home') target = 0;
      if (event.key === 'End') target = pageCount - 1;
      if (target !== undefined) { event.preventDefault(); buttons[target].focus(); }
    });
    controls.append(button);
    buttons.push(button);
  }
  controls.hidden = false;
  showPage(0);
})();

// Share bars accept a section URL or a future article's individual URL.
document.querySelectorAll('[data-copy-share-link]').forEach(button => {
  button.addEventListener('click', async () => {
    const bar = button.closest('[data-share-url]');
    const status = bar.querySelector('.blog-share-status');
    const url = bar.dataset.shareUrl;
    try {
      await navigator.clipboard.writeText(url);
      status.textContent = 'Link copied.';
    } catch (_) {
      status.textContent = 'Copy this link: ' + url;
    }
  });
});
// Keep the mobile menu state consistent when returning to a desktop layout.
window.matchMedia('(min-width: 1051px)').addEventListener('change', event => {
  if (!event.matches) return;
  document.querySelector('.site-header')?.classList.remove('is-open');
  const button = document.querySelector('.menu-toggle');
  button?.setAttribute('aria-expanded', 'false');
  button?.setAttribute('aria-label', 'Open navigation');
});

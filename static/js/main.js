/* Profimize main.js — vanilla JS, defer loaded */
(function () {
  'use strict';

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── 1. Header condense on scroll ── */
  const header = document.getElementById('site-header');
  if (header) {
    const onScroll = () => {
      header.classList.toggle('condensed', window.scrollY > 40);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ── 2. Mobile drawer ── */
  const hamburger = document.getElementById('hamburger');
  const drawer = document.getElementById('mobile-drawer');
  const drawerClose = document.getElementById('drawer-close');
  const backdrop = document.getElementById('drawer-backdrop');

  function openDrawer() {
    drawer.classList.add('open');
    hamburger.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
    drawerClose && drawerClose.focus();
  }
  function closeDrawer() {
    drawer.classList.remove('open');
    hamburger && hamburger.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
    hamburger && hamburger.focus();
  }
  hamburger && hamburger.addEventListener('click', openDrawer);
  drawerClose && drawerClose.addEventListener('click', closeDrawer);
  backdrop && backdrop.addEventListener('click', closeDrawer);
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && drawer && drawer.classList.contains('open')) closeDrawer();
  });

  /* ── 3. Scroll reveal via IntersectionObserver ── */
  // Hero uses CSS @keyframes — exclude those from IO observer
  const REVEAL_SEL = '.reveal, .fx-l, .fx-r, .fx-u, .fx-scale';
  const HERO_ANIM  = '.hero-badge-anim,.hero-title-anim,.hero-desc-anim,.hero-actions-anim,.hero-trust-anim';

  if (!reduced) {
    const allReveal = document.querySelectorAll(REVEAL_SEL);
    // Filter out elements that are inside the hero (those animate via keyframes)
    const heroEl = document.querySelector('.hero');
    const reveals = Array.from(allReveal).filter((el) => !heroEl || !heroEl.contains(el));

    if (reveals.length && 'IntersectionObserver' in window) {
      const io = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              entry.target.classList.add('in-view');
              io.unobserve(entry.target);
            }
          });
        },
        /* trigger when 6% visible; -8% rootMargin = fires as element
           enters from bottom — clearly visible on all screen sizes */
        { threshold: 0.06, rootMargin: '0px 0px -8% 0px' }
      );
      reveals.forEach((el) => io.observe(el));
    } else {
      allReveal.forEach((el) => el.classList.add('in-view'));
    }
  } else {
    document.querySelectorAll(REVEAL_SEL + ',' + HERO_ANIM).forEach((el) => {
      el.classList.add('in-view');
      el.style.opacity = '1';
      el.style.transform = 'none';
      el.style.animation = 'none';
    });
  }

  /* ── 4. Parallax on hero blobs (mouse + scroll) ── */
  if (!reduced) {
    const blobs = document.querySelectorAll('.hero-blob');
    if (blobs.length) {
      let ticking = false;
      const applyParallax = (mx, my) => {
        blobs.forEach((b, i) => {
          const factor = i === 0 ? 0.02 : -0.015;
          b.style.transform = `translate(${mx * factor}px, ${my * factor}px)`;
        });
      };
      document.addEventListener('mousemove', (e) => {
        if (!ticking) {
          requestAnimationFrame(() => {
            applyParallax(e.clientX - window.innerWidth / 2, e.clientY - window.innerHeight / 2);
            ticking = false;
          });
          ticking = true;
        }
      }, { passive: true });
    }
  }

  /* ── 5. Portfolio filter ── */
  const filterBtns = document.querySelectorAll('.filter-btn[data-filter]');
  const projectCards = document.querySelectorAll('.project-card[data-filter]');
  if (filterBtns.length) {
    filterBtns.forEach((btn) => {
      btn.addEventListener('click', () => {
        filterBtns.forEach((b) => b.classList.remove('active'));
        btn.classList.add('active');
        const filter = btn.dataset.filter;
        projectCards.forEach((card) => {
          const match = filter === 'all' || card.dataset.filter === filter;
          if (match) {
            card.removeAttribute('hidden');
          } else {
            card.setAttribute('hidden', '');
          }
        });
      });
    });
  }

  /* ── 6. Testimonial carousel ── */
  const carousel = document.getElementById('testimonials-carousel');
  if (carousel) {
    const slides = carousel.querySelectorAll('.testimonial-slide');
    const dots = document.querySelectorAll('.carousel-dot');
    let current = 0;
    let timer;

    function goTo(idx) {
      slides[current].classList.remove('active');
      dots[current] && dots[current].classList.remove('active');
      current = (idx + slides.length) % slides.length;
      slides[current].classList.add('active');
      dots[current] && dots[current].classList.add('active');
    }

    function startAuto() {
      timer = setInterval(() => goTo(current + 1), 5000);
    }
    function stopAuto() { clearInterval(timer); }

    if (slides.length > 1) {
      dots.forEach((dot, i) => {
        dot.addEventListener('click', () => { stopAuto(); goTo(i); startAuto(); });
      });

      // Touch/swipe support
      let startX = 0;
      carousel.addEventListener('touchstart', (e) => { startX = e.touches[0].clientX; }, { passive: true });
      carousel.addEventListener('touchend', (e) => {
        const dx = e.changedTouches[0].clientX - startX;
        if (Math.abs(dx) > 50) {
          stopAuto();
          goTo(dx < 0 ? current + 1 : current - 1);
          startAuto();
        }
      }, { passive: true });

      startAuto();
      carousel.addEventListener('mouseenter', stopAuto);
      carousel.addEventListener('mouseleave', startAuto);
    }
  }

  /* ── 7. Stats counter animation ── */
  function animateCounter(el) {
    const raw = el.dataset.target || el.textContent;
    const suffix = raw.replace(/[\d.]/g, '');
    const end = parseFloat(raw);
    if (isNaN(end)) return;
    const duration = 1600;
    const start = performance.now();
    const step = (now) => {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const ease = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.round(end * ease) + suffix;
      if (progress < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }

  if (!reduced) {
    const statValues = document.querySelectorAll('.stat-value[data-target]');
    if (statValues.length && 'IntersectionObserver' in window) {
      const sio = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            animateCounter(entry.target);
            sio.unobserve(entry.target);
          }
        });
      }, { threshold: 0.5 });
      statValues.forEach((el) => sio.observe(el));
    }
  }

  /* ── 8. YouTube Lightbox ── */
  const lightbox = document.getElementById('yt-lightbox');
  const ytPlayer = document.getElementById('yt-player');
  const ytClose = document.getElementById('yt-close');
  const ytBackdrop = document.getElementById('yt-backdrop');
  let focusTrapEls = [];
  let lastFocused;

  function openLightbox(videoId) {
    if (!lightbox || !ytPlayer || !videoId) return;
    lastFocused = document.activeElement;
    const iframe = document.createElement('iframe');
    iframe.src = `https://www.youtube-nocookie.com/embed/${videoId}?autoplay=1&rel=0&modestbranding=1`;
    iframe.title = 'YouTube video player';
    iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
    iframe.allowFullscreen = true;
    iframe.width = '100%';
    iframe.height = '100%';
    iframe.style.border = 'none';
    ytPlayer.innerHTML = '';
    ytPlayer.appendChild(iframe);
    lightbox.removeAttribute('hidden');
    document.body.style.overflow = 'hidden';
    ytClose && ytClose.focus();
    // Trap focus in lightbox
    focusTrapEls = Array.from(lightbox.querySelectorAll('button, [href], iframe, [tabindex]:not([tabindex="-1"])'));
  }

  function closeLightbox() {
    if (!lightbox) return;
    ytPlayer.innerHTML = '';
    lightbox.setAttribute('hidden', '');
    document.body.style.overflow = '';
    lastFocused && lastFocused.focus();
  }

  document.addEventListener('keydown', (e) => {
    if (!lightbox || lightbox.hasAttribute('hidden')) return;
    if (e.key === 'Escape') { closeLightbox(); return; }
    if (e.key === 'Tab' && focusTrapEls.length) {
      const first = focusTrapEls[0];
      const last = focusTrapEls[focusTrapEls.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault(); last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault(); first.focus();
      }
    }
  });

  ytClose && ytClose.addEventListener('click', closeLightbox);
  ytBackdrop && ytBackdrop.addEventListener('click', closeLightbox);

  // Play overlay buttons
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('.play-overlay[data-video-id]');
    if (btn) {
      e.preventDefault();
      openLightbox(btn.dataset.videoId);
    }
  });

  /* ── 9. Share buttons ── */
  const copyBtn = document.getElementById('copy-link-btn');
  if (copyBtn) {
    copyBtn.addEventListener('click', async () => {
      const url = copyBtn.dataset.url || location.href;
      const label = document.getElementById('copy-label');
      try {
        if (navigator.share) {
          await navigator.share({ url, title: document.title });
        } else {
          await navigator.clipboard.writeText(url);
          if (label) {
            label.textContent = 'Copied!';
            setTimeout(() => (label.textContent = 'Copy Link'), 2000);
          }
        }
      } catch (_) {
        // User cancelled or clipboard not available
      }
    });
  }

  /* ── 10. Form UX (disable submit on submit) ── */
  document.querySelectorAll('#contact-form').forEach((form) => {
    form.addEventListener('submit', () => {
      const btn = form.querySelector('#submit-btn');
      if (btn) {
        btn.disabled = true;
        btn.textContent = 'Sending…';
      }
    });
  });

  /* ── Auto-dismiss alerts after 5s ── */
  document.querySelectorAll('.alert').forEach((alert) => {
    setTimeout(() => {
      alert.style.transition = 'opacity .4s';
      alert.style.opacity = '0';
      setTimeout(() => alert.remove(), 400);
    }, 5000);
  });

})();

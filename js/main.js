/* ============================================================
   АКАДЕМИЯ НА РУССКОМ — main.js
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* --- Header scroll shadow --- */
  const header = document.querySelector('.header');
  if (header) {
    window.addEventListener('scroll', () => {
      header.classList.toggle('scrolled', window.scrollY > 20);
    }, { passive: true });
  }

  /* --- Mobile nav drawer --- */
  const hamburger = document.querySelector('.hamburger');
  const navDrawer = document.querySelector('.nav-drawer');
  if (hamburger && navDrawer) {
    hamburger.addEventListener('click', () => {
      const open = navDrawer.classList.toggle('open');
      hamburger.classList.toggle('active', open);
      hamburger.setAttribute('aria-expanded', open);
      document.body.style.overflow = open ? 'hidden' : '';
    });
    // Close on link click
    navDrawer.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navDrawer.classList.remove('open');
        hamburger.classList.remove('active');
        hamburger.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      });
    });
  }

  /* --- FAQ accordion --- */
  document.querySelectorAll('.faq-question').forEach(btn => {
    btn.addEventListener('click', () => {
      const item = btn.closest('.faq-item');
      const isOpen = item.classList.contains('open');
      // Close all
      document.querySelectorAll('.faq-item.open').forEach(i => i.classList.remove('open'));
      // Toggle current
      if (!isOpen) item.classList.add('open');
    });
  });

  /* --- Fade-in on scroll --- */
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('fade-in--visible', 'visible');
        observer.unobserve(e.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

  document.querySelectorAll('.fade-in, .fade-in-up').forEach(el => observer.observe(el));

  /* --- Active nav link --- */
  const currentPage = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav__link, .nav-drawer__link').forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPage || (currentPage === '' && href === 'index.html')) {
      link.classList.add('nav__link--active', 'nav-drawer__link--active');
    }
  });

  /* --- Smooth counter animation --- */
  function animateCounter(el) {
    const target = parseInt(el.dataset.target, 10);
    const duration = 1800;
    const start = performance.now();
    const update = (time) => {
      const progress = Math.min((time - start) / duration, 1);
      const ease = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.floor(ease * target).toLocaleString('ru-RU');
      if (progress < 1) requestAnimationFrame(update);
      else el.textContent = target.toLocaleString('ru-RU') + (el.dataset.suffix || '');
    };
    requestAnimationFrame(update);
  }

  const counterObs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        animateCounter(e.target);
        counterObs.unobserve(e.target);
      }
    });
  }, { threshold: 0.5 });

  document.querySelectorAll('[data-target]').forEach(el => counterObs.observe(el));

  /* --- Contact form --- */
  const form = document.getElementById('enrollForm');
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const btn = form.querySelector('[type="submit"]');
      const original = btn.textContent;
      btn.textContent = 'Отправляем...';
      btn.disabled = true;
      // Simulate send
      setTimeout(() => {
        form.innerHTML = `
          <div style="text-align:center;padding:3rem 0;">
            <div style="font-size:3rem;margin-bottom:1rem;">✅</div>
            <h3 style="margin-bottom:.5rem;">Заявка отправлена!</h3>
            <p style="color:var(--color-text-light);">Мы свяжемся с вами в течение нескольких часов.<br>Проверьте Telegram или WhatsApp.</p>
          </div>`;
      }, 1200);
    });
  }

  /* --- Language switcher (stub) --- */
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('lang-btn--active'));
      btn.classList.add('lang-btn--active');
      // In production: redirect to /en/ or swap content
    });
  });

});

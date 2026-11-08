/* ============================================================
   AHMAD SHEHZAD – PORTFOLIO  |  script.js
   ============================================================ */

/* ---------- Typed Text ---------- */
const typedEl = document.getElementById('typed-text');
const roles = [
  'AI Engineer',
  'Python Developer',
  'N8N Automation Expert',
  'Web Scraping Developer',
  'AI Agents Builder',
  'Workflow Automation Pro',
];
let ri = 0, ci = 0, deleting = false;
function typeLoop() {
  const word = roles[ri];
  if (!deleting) {
    typedEl.textContent = word.slice(0, ++ci);
    if (ci === word.length) { deleting = true; setTimeout(typeLoop, 1800); return; }
  } else {
    typedEl.textContent = word.slice(0, --ci);
    if (ci === 0) { deleting = false; ri = (ri + 1) % roles.length; }
  }
  setTimeout(typeLoop, deleting ? 60 : 100);
}
typeLoop();

/* ---------- Navbar scroll ---------- */
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 30);
  updateActiveLink();
  toggleBackToTop();
});

/* ---------- Hamburger ---------- */
const hamburger  = document.getElementById('hamburger');
const navLinks   = document.getElementById('nav-links');
hamburger.addEventListener('click', () => {
  hamburger.classList.toggle('open');
  navLinks.classList.toggle('open');
});
navLinks.querySelectorAll('.nav-link').forEach(l => l.addEventListener('click', () => {
  hamburger.classList.remove('open');
  navLinks.classList.remove('open');
}));

/* ---------- Active nav link ---------- */
function updateActiveLink() {
  const sections = document.querySelectorAll('section[id]');
  const scrollY  = window.scrollY + 100;
  sections.forEach(s => {
    const link = document.querySelector(`.nav-link[href="#${s.id}"]`);
    if (!link) return;
    const inView = scrollY >= s.offsetTop && scrollY < s.offsetTop + s.offsetHeight;
    link.classList.toggle('active', inView);
  });
}

/* ---------- Back to top ---------- */
const backBtn = document.getElementById('back-to-top');
function toggleBackToTop() { backBtn.classList.toggle('show', window.scrollY > 400); }
backBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

/* ---------- Skill bar animation ---------- */
const bars = document.querySelectorAll('.skill-bar');
const barObserver = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      const fill = e.target.querySelector('.fill');
      fill.style.width = e.target.dataset.percent + '%';
      barObserver.unobserve(e.target);
    }
  });
}, { threshold: 0.3 });
bars.forEach(b => barObserver.observe(b));

/* ---------- Fade-in on scroll ---------- */
document.querySelectorAll(
  '.about-card, .skill-category, .timeline-card, .edu-card, .project-card, .achievement-card, .contact-item'
).forEach(el => {
  el.classList.add('fade-in');
  new IntersectionObserver(([e]) => {
    if (e.isIntersecting) { el.classList.add('visible'); }
  }, { threshold: 0.15 }).observe(el);
});

/* ---------- Floating particles ---------- */
function createParticles() {
  const container = document.getElementById('particles');
  if (!container) return;
  for (let i = 0; i < 20; i++) {
    const p = document.createElement('div');
    p.className = 'particle';
    const size = Math.random() * 6 + 2;
    Object.assign(p.style, {
      width:  size + 'px',
      height: size + 'px',
      left:   Math.random() * 100 + '%',
      animationDuration: (Math.random() * 15 + 10) + 's',
      animationDelay:    (Math.random() * 10) + 's',
    });
    container.appendChild(p);
  }
}
createParticles();

/* ---------- Contact form ---------- */
document.getElementById('contact-form').addEventListener('submit', function (e) {
  e.preventDefault();
  const status = document.getElementById('form-status');
  const btn    = this.querySelector('button[type="submit"]');
  btn.disabled = true;
  btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending…';
  setTimeout(() => {
    btn.disabled = false;
    btn.innerHTML = '<i class="fas fa-paper-plane"></i> Send Message';
    status.style.color = '#a855f7';
    status.textContent = '✅ Message sent! Ahmed will get back to you soon.';
    this.reset();
    setTimeout(() => (status.textContent = ''), 5000);
  }, 1500);
});

/* ---------- Footer year ---------- */
document.getElementById('year').textContent = new Date().getFullYear();

/* ---------- Smooth scroll for all anchor links ---------- */
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth' }); }
  });
});

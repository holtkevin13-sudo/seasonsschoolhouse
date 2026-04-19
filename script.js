// ─── DROPDOWN — Mobile click only, desktop uses CSS hover ──────
document.querySelectorAll('.dropdown-btn').forEach(function (btn) {
  btn.addEventListener('click', function (e) {
    e.stopPropagation();
    const targetId = btn.getAttribute('data-target');
    const menu = document.getElementById(targetId);
    if (!menu) return;
    const isOpen = menu.classList.contains('open');
    document.querySelectorAll('.dropdown-menu').forEach(m => m.classList.remove('open'));
    if (!isOpen) menu.classList.add('open');
  });
});

// Close mobile dropdowns on outside click
document.addEventListener('click', function (e) {
  if (!e.target.closest('.dropdown')) {
    document.querySelectorAll('.dropdown-menu').forEach(m => m.classList.remove('open'));
  }
});

// ─── HAMBURGER ─────────────────────────────────────────────────
var hamburger = document.getElementById('hamburger');
var navLinks  = document.getElementById('nav-links');

if (hamburger && navLinks) {
  hamburger.addEventListener('click', function (e) {
    e.stopPropagation();
    navLinks.classList.toggle('open');
  });
  document.addEventListener('click', function (e) {
    if (!navLinks.contains(e.target)) {
      navLinks.classList.remove('open');
    }
  });
}

// ─── CONTACT FORM ──────────────────────────────────────────────
function submitForm() {
  var name  = document.getElementById('f-name');
  var email = document.getElementById('f-email');
  if (!name || !email) return;
  if (!name.value.trim() || !email.value.trim()) {
    alert('Please fill in your name and email address.');
    return;
  }
  var form    = document.getElementById('contact-form');
  var success = document.getElementById('form-success');
  if (form)    form.style.display    = 'none';
  if (success) success.style.display = 'block';
}

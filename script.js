// ─── Dropdown Toggle ───────────────────────────────────────────
function toggleDropdown(id, e) {
  if (e) e.stopPropagation();
  const menu = document.getElementById(id);
  if (!menu) return;
  const isOpen = menu.classList.contains('open');
  // Close all first
  document.querySelectorAll('.dropdown-menu').forEach(m => m.classList.remove('open'));
  if (!isOpen) menu.classList.add('open');
}

// Close dropdowns only when clicking OUTSIDE a dropdown
document.addEventListener('click', function (e) {
  if (!e.target.closest('.dropdown')) {
    document.querySelectorAll('.dropdown-menu').forEach(m => m.classList.remove('open'));
  }
});

// Prevent clicks inside dropdown menus from bubbling and closing the menu
document.querySelectorAll('.dropdown-menu').forEach(function (menu) {
  menu.addEventListener('click', function (e) {
    e.stopPropagation();
  });
});

// ─── Hamburger Menu ────────────────────────────────────────────
const hamburger = document.getElementById('hamburger');
const navLinks  = document.getElementById('nav-links');

if (hamburger && navLinks) {
  hamburger.addEventListener('click', function (e) {
    e.stopPropagation();
    navLinks.classList.toggle('open');
  });
}

// Close mobile menu when clicking outside
document.addEventListener('click', function (e) {
  if (navLinks && navLinks.classList.contains('open')) {
    if (!navLinks.contains(e.target) && e.target !== hamburger) {
      navLinks.classList.remove('open');
    }
  }
});

// ─── Contact Form ───────────────────────────────────────────────
function submitForm() {
  const name  = document.getElementById('f-name');
  const email = document.getElementById('f-email');
  if (!name || !email) return;
  if (!name.value.trim() || !email.value.trim()) {
    alert('Please fill in your name and email address.');
    return;
  }
  const form    = document.getElementById('contact-form');
  const success = document.getElementById('form-success');
  if (form)    form.style.display    = 'none';
  if (success) success.style.display = 'block';
}

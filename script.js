// ─── Dropdown Toggle ───
function toggleDropdown(id, e) {
  if (e) e.stopPropagation();
  const menu = document.getElementById(id);
  if (!menu) return;
  const isOpen = menu.classList.contains('open');
  // Close all dropdowns first
  document.querySelectorAll('.dropdown-menu').forEach(m => m.classList.remove('open'));
  if (!isOpen) menu.classList.add('open');
}

// Close dropdowns on outside click
document.addEventListener('click', function () {
  document.querySelectorAll('.dropdown-menu').forEach(m => m.classList.remove('open'));
});

// ─── Hamburger Menu ───
const hamburger = document.getElementById('hamburger');
const navLinks  = document.getElementById('nav-links');

if (hamburger) {
  hamburger.addEventListener('click', function (e) {
    e.stopPropagation();
    navLinks.classList.toggle('open');
  });
}

document.addEventListener('click', function (e) {
  if (navLinks && !navLinks.contains(e.target) && e.target !== hamburger) {
    navLinks.classList.remove('open');
  }
});

// Close mobile menu when a link is clicked
if (navLinks) {
  navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      navLinks.classList.remove('open');
    });
  });
}

// ─── Contact Form ───
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

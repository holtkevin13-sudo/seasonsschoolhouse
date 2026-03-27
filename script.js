// ─── Section Navigation ───
function showSection(id) {
  document.querySelectorAll('section').forEach(s => s.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ─── Hamburger Menu ───
document.getElementById('hamburger').addEventListener('click', function () {
  document.getElementById('nav-links').classList.toggle('open');
});

function closeMenu() {
  document.getElementById('nav-links').classList.remove('open');
}

// ─── Pages Dropdown (click-based) ───
function toggleDropdown(e) {
  e.stopPropagation();
  document.getElementById('pages-dropdown').classList.toggle('open');
}

function closeAll() {
  document.getElementById('pages-dropdown').classList.remove('open');
  closeMenu();
}

// Close dropdown when clicking outside
document.addEventListener('click', function (e) {
  const dropdown = document.querySelector('.dropdown');
  if (dropdown && !dropdown.contains(e.target)) {
    document.getElementById('pages-dropdown').classList.remove('open');
  }
});

// ─── Contact Form (visual submission) ───
function submitForm() {
  const name  = document.getElementById('f-name').value.trim();
  const email = document.getElementById('f-email').value.trim();
  if (!name || !email) {
    alert('Please fill in your name and email address.');
    return;
  }
  document.getElementById('contact-form').style.display = 'none';
  document.getElementById('form-success').style.display = 'block';
}

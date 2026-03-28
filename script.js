// ─── SECTION NAVIGATION ───
function showSection(id) {
  document.querySelectorAll('section').forEach(s => s.classList.remove('active'));
  const el = document.getElementById(id);
  if (el) {
    el.classList.add('active');
    window.scrollTo({ top: 0, behavior: 'instant' });
  }
  closeAll();
}

// ─── DROPDOWN ───
function closeAll() {
  document.getElementById('about-dropdown')?.classList.remove('open');
}

function closeMenu() {
  document.getElementById('nav-links')?.classList.remove('open');
  closeAll();
}

function toggleAboutDropdown(e) {
  e.stopPropagation();
  document.getElementById('about-dropdown').classList.toggle('open');
}

// ─── GALLERY ───
const galleryPhotos = [
  'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1400&auto=format&q=80',
  'https://images.unsplash.com/photo-1448375240586-882707db888b?w=1400&auto=format&q=80',
  'https://images.unsplash.com/photo-1518173946687-a4c8892bbd9f?w=1400&auto=format&q=80',
  'https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=1400&auto=format&q=80',
  'https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?w=1400&auto=format&q=80',
];

let galleryIndex = 0;

function initGallery() {
  const slides = document.querySelectorAll('.gallery-img');
  if (!slides.length) return;
  slides[0].classList.add('active');

  setInterval(() => {
    slides[galleryIndex].classList.remove('active');
    galleryIndex = (galleryIndex + 1) % slides.length;
    slides[galleryIndex].classList.add('active');

    // Update dots
    document.querySelectorAll('.gallery-dot').forEach((dot, i) => {
      dot.classList.toggle('active', i === galleryIndex);
    });
  }, 5000);
}

function goToSlide(i) {
  const slides = document.querySelectorAll('.gallery-img');
  slides[galleryIndex].classList.remove('active');
  galleryIndex = i;
  slides[galleryIndex].classList.add('active');
  document.querySelectorAll('.gallery-dot').forEach((dot, idx) => {
    dot.classList.toggle('active', idx === galleryIndex);
  });
}

// ─── FORMS ───
function submitForm() {
  document.getElementById('contact-form').style.display = 'none';
  document.getElementById('form-success').style.display = 'block';
}

function submitApply() {
  const name = document.getElementById('a-name')?.value;
  const email = document.getElementById('a-email')?.value;
  if (!name || !email) {
    alert('Please fill in your name and email before submitting.');
    return;
  }
  document.getElementById('apply-form').style.display = 'none';
  document.getElementById('apply-success').style.display = 'block';
}

// ─── INIT ───
document.addEventListener('DOMContentLoaded', function () {

  // Hamburger toggle
  document.getElementById('hamburger').addEventListener('click', function (e) {
    e.stopPropagation();
    document.getElementById('nav-links').classList.toggle('open');
  });

  // Close nav/dropdown on outside click
  document.addEventListener('click', function () {
    document.getElementById('nav-links')?.classList.remove('open');
    closeAll();
  });

  // Prevent nav from closing when clicking inside it
  document.querySelector('nav').addEventListener('click', function (e) {
    e.stopPropagation();
  });

  // Init gallery
  initGallery();
});

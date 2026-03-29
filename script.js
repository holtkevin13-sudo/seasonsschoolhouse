// ─── SECTION NAVIGATION ───
function showSection(id) {
  document.querySelectorAll('section').forEach(s => s.classList.remove('active'));
  const el = document.getElementById(id);
  if (el) {
    el.classList.add('active');
    // Force scroll to very top of page
    document.documentElement.scrollTop = 0;
    document.body.scrollTop = 0;
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
let galleryIndex = 0;
let homeGalleryIndex = 0;

function initGallery() {
  // Full gallery page
  const slides = document.querySelectorAll('#gallery .gallery-img');
  if (slides.length) {
    slides[0].classList.add('active');
    setInterval(() => {
      slides[galleryIndex].classList.remove('active');
      galleryIndex = (galleryIndex + 1) % slides.length;
      slides[galleryIndex].classList.add('active');
      document.querySelectorAll('#gallery .gallery-dot').forEach((dot, i) => {
        dot.classList.toggle('active', i === galleryIndex);
      });
    }, 5000);
  }

  // Home page gallery
  const homeSlides = document.querySelectorAll('.home-gallery .gallery-img');
  if (homeSlides.length) {
    homeSlides[0].classList.add('active');
    setInterval(() => {
      homeSlides[homeGalleryIndex].classList.remove('active');
      homeGalleryIndex = (homeGalleryIndex + 1) % homeSlides.length;
      homeSlides[homeGalleryIndex].classList.add('active');
      document.querySelectorAll('.home-dot').forEach((dot, i) => {
        dot.classList.toggle('active', i === homeGalleryIndex);
      });
    }, 5000);
  }
}

function goToSlide(i) {
  const slides = document.querySelectorAll('#gallery .gallery-img');
  slides[galleryIndex].classList.remove('active');
  galleryIndex = i;
  slides[galleryIndex].classList.add('active');
  document.querySelectorAll('#gallery .gallery-dot').forEach((dot, idx) => {
    dot.classList.toggle('active', idx === galleryIndex);
  });
}

function goToHomeSlide(i) {
  const slides = document.querySelectorAll('.home-gallery .gallery-img');
  slides[homeGalleryIndex].classList.remove('active');
  homeGalleryIndex = i;
  slides[homeGalleryIndex].classList.add('active');
  document.querySelectorAll('.home-dot').forEach((dot, idx) => {
    dot.classList.toggle('active', idx === homeGalleryIndex);
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

# Seasons Schoolhouse Website

A K–8 homeschool enrichment co-op website. Earthy, minimal, community-centered.

---

## Files

| File | Purpose |
|------|---------|
| `index.html` | Main website |
| `style.css` | All styles |
| `script.js` | Navigation & form logic |
| `logo.png` | Site logo (also used for social sharing) |
| `favicon.ico` | Browser tab icon |
| `apple-touch-icon.png` | iOS home screen icon |

---

## How to publish with GitHub Pages

1. Create a new repository on [github.com](https://github.com) (e.g. `seasons-schoolhouse`)
2. Upload all files in this folder to the repository
3. Go to **Settings → Pages**
4. Under **Source**, select `main` branch and `/ (root)` folder
5. Click **Save**
6. Your site will be live at `https://yourusername.github.io/seasons-schoolhouse/`

---

## One-time update after publishing

Once your site is live, open `index.html` and replace the relative `og:image` path with your full URL so social sharing works correctly:

```html
<!-- Change this: -->
<meta property="og:image" content="logo.png" />

<!-- To this (use your actual GitHub Pages URL): -->
<meta property="og:image" content="https://yourusername.github.io/seasons-schoolhouse/logo.png" />
```

---

## To update social media handles

In `index.html`, find these lines in the Contact section and replace with your handles:

```html
<div class="contact-detail"><span class="contact-icon">📸</span><span>Instagram — coming soon</span></div>
<div class="contact-detail"><span class="contact-icon">👥</span><span>Band — coming soon</span></div>
```

Replace with something like:
```html
<div class="contact-detail"><span class="contact-icon">📸</span><a href="https://instagram.com/yourhandle" target="_blank">@yourhandle</a></div>
<div class="contact-detail"><span class="contact-icon">👥</span><a href="https://band.us/yourlink" target="_blank">Join our Band</a></div>
```

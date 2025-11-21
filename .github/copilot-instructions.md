# Copilot / AI agent instructions — static-site

Purpose: Fast, practical guidance to edit and maintain this tiny static site.

**Big picture**
- Single-page static website: `index.html` (markup) + `styles.css` (styles) + `script.js` (behavior).
- No build system, frameworks, or backend—everything is edited in-place and deployed as static assets.
- Contact form posts to a third-party (Formspree); no server-side processing in this repo.

**Primary files**
- `index.html`: main content and markup. Key IDs/classes: `nav`, `mobile-menu-toggle`, `nav-links`, `about`, `contact`, `contact-form`, `form-status`.
- `styles.css`: design tokens in `:root` (e.g. `--brand-navy`, `--brand-orange`), responsive rules, and the hero background (local `assets/hero.jpg`).
- `script.js`: mobile menu toggle, smooth scrolling (subtracts `nav` height), and AJAX contact form handler (fetch to `form.action`).
- `CHANGELOG.md`: human summary of site scope and history.

**Concrete patterns & examples (do this here)**
- Change colors: edit variables at the top of `styles.css` (example: `--brand-navy`, `--brand-orange`).
- Mobile nav: use `id="mobile-menu-toggle"` and `id="nav-links"`. Toggling adds/removes the `active` class on `#nav-links` (see `script.js`).
- Smooth scroll: anchors are `href="#section"`; the script computes `targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navHeight`. Keep this when adjusting nav height.
- Contact form: form element uses `id="contact-form"` and contains hidden metadata inputs: `source`, `page`, `submitted_at`, `utm_source`, `utm_medium`, `utm_campaign`. The JS populates `submitted_at` and UTM fields before sending.
- Form submission: `fetch(form.action, { method: form.method, headers: { 'Accept': 'application/json' }, body: formData })`. On success the script replaces the form with a `thank-you` card (no redirect).

**Integration points & assets**
- External form endpoint (current): `https://formspree.io/f/xvgdopwr` — change only the `action` to swap providers.
- Logo and hero images: `assets/staticSiteLogo.svg`, `assets/hero.jpg`. The `styles.css` hero background references `assets/hero.jpg` (preferred for offline hosting).

**Local developer workflows**
- Quick preview: open `index.html` directly in a browser (`open index.html` on macOS).
- Local server (recommended to replicate fetch behavior): run `python3 -m http.server 8000` and visit `http://localhost:8000`.
- Test contact form: use a Formspree test form ID or temporarily set `action="mailto:you@example.com"` for manual verification. Check Network tab for the POST payload when using AJAX.

**Do / Don't (repo-specific)**
- Do: edit HTML/CSS/JS directly; prefer CSS class toggles over inline JS changes for UI state.
- Do: preserve accessibility hooks — `#form-status` has `role="status" aria-live="polite"` and should be used for form feedback.
- Don't: introduce a package manager, CI, or tooling that requires build steps without owner approval.

**PR checklist for non-trivial changes**
- Short description of user-visible changes.
- Files changed and rationale (list file paths).
- Manual test plan: open `index.html` or `http://localhost:8000`, verify hero loads, nav toggle works on mobile widths, anchor links scroll with offset, submit contact form and confirm thank-you UI.

If anything here is unclear or you want a different format (more verbose examples, a runnable dev script, or a local test harness), tell me which parts to expand.

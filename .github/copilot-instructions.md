# Copilot / AI agent instructions — static-site

Purpose: Help an AI coding agent quickly understand, modify, and extend this tiny static site.

Key facts (big picture)
- This is a single-page static website: `index.html` + `styles.css` + `script.js`.
- No build tools, package managers, server code, or tests in the repo. Edits are made directly to source files.
- The site is deployed as static assets (upload the folder to any static host or drop `index.html` in a webroot).

Primary files to read and edit
- `index.html` — semantic content, section structure, contact form. Major sections: nav, #about (hero), #info, #contact, footer.
- `styles.css` — global design, brand variables (see `:root`). Change colors, spacing and responsive breakpoints here.
- `script.js` — small DOM behavior: mobile menu toggle and smooth scrolling logic. Look for element IDs `mobile-menu-toggle` and `nav-links`.
- `CHANGELOG.md` — plain-language summary of what the site contains and how it is intended to be used.

Patterns & conventions (concrete, not aspirational)
- Design tokens: CSS variables are declared in `:root` at the top of `styles.css`. To change brand colors update `--brand-navy` and `--brand-orange`.
  Example: `:root { --brand-navy: #1e3a5f; --brand-orange: #ff6b35; }`
- Mobile nav: the hamburger uses id `mobile-menu-toggle`. Toggling adds/removes `active` on `#nav-links` (see `script.js`). Modify classes/styles rather than adding inline JS when possible.
- Smooth scroll: anchors use `href="#..."` and the JS subtracts the `nav` height when calculating target position. Preserve that offset calculation when changing navigation height.
- Contact form: currently posts to Formspree (action `https://formspree.io/f/xwpaeodq`) with `method="post"` and `enctype="text/plain"`. To swap providers, update `action` only.

Integration points / external dependencies
- Background image in the hero uses an external Unsplash URL (in `styles.css`). Consider downloading assets into `assets/` if you want offline hosting.
- The contact form endpoint (Formspree) is the only external form integration; there is no backend.

Developer workflows (how to test changes locally)
- No build: open `index.html` in a browser (double-click or `open index.html` on macOS).
- Quick dev iterate: edit files, refresh browser. For local testing of form submission, use Formspree test endpoint or change form action to `mailto:` for manual testing.

Small examples to reference
- Mobile toggle (from `script.js`):
  - `const mobileMenuToggle = document.getElementById('mobile-menu-toggle');`
  - toggles `navLinks.classList.toggle('active')` and closes menu when links are clicked.
- CSS variables (from `styles.css`):
  - `:root { --brand-navy: #1e3a5f; --brand-orange: #ff6b35; }`

What NOT to assume
- There is no CI, tests, or package.json — do not add automation that requires a package manager without checking with the maintainer.
- There is no server-side form handling here; form behavior is entirely client-side and via an external service.

If you need to make larger changes
- For multi-file or risky changes (e.g., redesign, swapping to a static-site generator), create a small PR and include:
  1. A short description of user-visible changes
  2. Files changed and why
  3. A brief manual test plan (open `index.html`, verify hero, nav, contact form)

Contact / follow-up
- If something is unclear (e.g., intended form provider, desired branding palette, or deploying domain), ask the repo owner before introducing new tooling.

— End of instructions

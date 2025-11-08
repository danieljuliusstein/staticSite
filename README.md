Resilience Solutions — static-site

Quick overview
- Single-page static site: `index.html`, `styles.css`, `script.js`.
- No build tools or server components; edit files and open `index.html` in a browser.

Local hero image
- Place your hero image at `assets/hero.jpg` (see `assets/README.md`).
- `styles.css` already references `assets/hero.jpg` for the hero background.

Contact form
- The contact form action is a placeholder: `https://example.com/your-form-endpoint`.
- To use a provider: replace the `action` attribute on the `<form>` in `index.html`.
  Examples:
  - Formspree: `action="https://formspree.io/f/YOUR_FORM_ID"` (method POST)
  - Netlify Forms: add `data-netlify="true"` to the form and leave `action` empty

Branding and styling
- Change colors via CSS variables at the top of `styles.css`:
  :root {
    --brand-navy: #1e3a5f;
    --brand-orange: #ff6b35;
  }

How to test locally (macOS)
- Open the site in your browser:

```bash
open index.html
```

- Edit files in your editor and refresh the browser to see changes.

Notes & next steps you may want me to do
- I did not download the Unsplash image automatically; please save it as `assets/hero.jpg` (instructions in `assets/README.md`).
- I set the form `action` to a placeholder so you can plug your provider. I can update it to Formspree, Netlify, or a backend endpoint if you tell me which one and provide the form ID or endpoint.

Contact
- If you want me to swap the form provider or download the hero image into the repo, tell me which provider/URL to use and I will update the files.

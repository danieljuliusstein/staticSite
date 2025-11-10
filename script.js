// Mobile menu toggle
const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
const navLinks = document.getElementById('nav-links');

if (mobileMenuToggle) {
  mobileMenuToggle.addEventListener('click', () => {
    navLinks.classList.toggle('active');
  });

  // Close menu when clicking a link
  navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      navLinks.classList.remove('active');
    });
  });
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      const navHeight = document.querySelector('nav').offsetHeight;
      const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navHeight;
      window.scrollTo({
        top: targetPosition,
        behavior: 'smooth'
      });
    }
  });
});

// AJAX contact form submission with accessible feedback and hidden metadata
(function attachContactFormHandler() {
  const form = document.getElementById('contact-form') || document.querySelector('.contact-form');
  if (!form) return;

  const statusEl = document.getElementById('form-status') || (() => {
    const d = document.createElement('div');
    d.id = 'form-status';
    d.className = 'form-status';
    d.setAttribute('role', 'status');
    d.setAttribute('aria-live', 'polite');
    form.prepend(d);
    return d;
  })();

  function setStatus(text, isError = false) {
    statusEl.textContent = text;
    statusEl.style.color = isError ? '#b91c1c' : 'var(--brand-navy)';
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    setStatus('Sending…');

    // Simple client-side validation (required fields)
    const nameEl = form.querySelector('input[name="name"]');
    const emailEl = form.querySelector('input[name="email"]');
    const messageEl = form.querySelector('textarea[name="message"]');

    // clear previous error styles
    form.querySelectorAll('.input-error').forEach(el => el.classList.remove('input-error'));

    const errors = [];
    if (!nameEl || !nameEl.value.trim()) errors.push({el: nameEl, msg: 'Please enter your name.'});
    if (!emailEl || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailEl.value.trim())) errors.push({el: emailEl, msg: 'Please enter a valid email.'});
    if (!messageEl || !messageEl.value.trim()) errors.push({el: messageEl, msg: 'Please enter a message.'});

    if (errors.length) {
      setStatus(errors[0].msg, true);
      errors.forEach(err => { if (err.el) err.el.classList.add('input-error'); });
      return;
    }

    // Populate hidden metadata fields
    const submittedAtInput = form.querySelector('input[name="submitted_at"]');
    if (submittedAtInput) submittedAtInput.value = new Date().toISOString();
    const pageInput = form.querySelector('input[name="page"]');
    if (pageInput) pageInput.value = window.location.pathname || 'index';

    // UTM parameters from URL
    const params = new URLSearchParams(window.location.search);
    ['utm_source','utm_medium','utm_campaign','utm_term','utm_content'].forEach(k => {
      const input = form.querySelector(`input[name="${k}"]`);
      const val = params.get(k);
      if (input && val) input.value = val;
    });

    // Send as FormData (Formspree accepts form posts). Ask for JSON response.
    const formData = new FormData(form);

    // disable submit button while sending
    const submitBtn = form.querySelector('[type="submit"]');
    if (submitBtn) submitBtn.disabled = true;

    try {
      const resp = await fetch(form.action, {
        method: form.method || 'POST',
        headers: {
          'Accept': 'application/json'
        },
        body: formData
      });

      const data = await resp.json().catch(() => null);

      if (resp.ok) {
        // Show full thank-you replacement UI
        const thankYou = document.createElement('div');
        thankYou.className = 'thank-you-card container';
        thankYou.innerHTML = `
          <h2>Thanks — we'll be in touch!</h2>
          <p>We received your message and will get back to you shortly. If you'd like immediate help, email <a href=\"mailto:resiliencesolutions.us@gmail.com\">resiliencesolutions.us@gmail.com</a>.</p>
        `;
        form.replaceWith(thankYou);

        // If Formspree returned a next path, redirect after a short delay
        if (data && data.next) {
          // Respect absolute or relative URLs
          const nextUrl = data.next;
          setTimeout(() => {
            if (/^https?:\/\//i.test(nextUrl) || nextUrl.startsWith('/')) {
              window.location.href = nextUrl;
            } else {
              // relative path
              window.location.href = window.location.origin.replace(/\/$/, '') + '/' + nextUrl.replace(/^\//, '');
            }
          }, 1600);
        }
      } else {
        const msg = (data && (data.error || data.message)) ? (data.error || data.message) : 'There was a problem sending your message.';
        setStatus(msg, true);
        if (submitBtn) submitBtn.disabled = false;
      }
    } catch (err) {
      setStatus('Network error — please try again later.', true);
      if (submitBtn) submitBtn.disabled = false;
    }
  });
})();

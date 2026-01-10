# Social Media Integration Guide

## Current Status

Social media links are **prepared but commented out** in the footer to avoid broken/fake links. The CSS styling is in place and ready to use.

## When to Activate Social Links

Uncomment the social media section in footer HTML files **only after** creating real, active social media accounts for Resilience Solutions.

---

## Step 1: Create Social Media Accounts

### Recommended Platforms for Home Remodeling Business:

1. **Facebook Business Page** (Priority: HIGH)
   - Best for local business visibility
   - Enables customer reviews and ratings
   - Create at: https://www.facebook.com/pages/create
   - Suggested handle: `@ResilienceSolutionsGA`

2. **Instagram Business Account** (Priority: HIGH)
   - Perfect for showcasing before/after photos
   - Strong engagement with homeowners
   - Create at: https://www.instagram.com/accounts/emailsignup/
   - Suggested handle: `@resiliencesolutionsga`

3. **X/Twitter** (Priority: MEDIUM)
   - Good for sharing tips and blog posts
   - Less critical for local home services
   - Create at: https://twitter.com/i/flow/signup
   - Suggested handle: `@ResilienceSolGA`

### Account Setup Checklist:

- [ ] Use consistent branding (logo, colors, tagline)
- [ ] Complete all profile fields (bio, contact info, website)
- [ ] Add business hours and location
- [ ] Post at least 5-10 pieces of content before linking
- [ ] Enable messaging/DMs for customer inquiries
- [ ] Link back to resiliencesolutionsga.com in bio

---

## Step 2: Add Real URLs to Website

Once accounts are created and active, update the footer in these files:

### Files to Update:

1. `/index.html` (homepage)
2. `/projects.html`
3. `/privacy.html`
4. `/blog/index.html`
5. `/services/interior-painting/index.html`
6. All location-specific service pages (alpharetta.html, etc.)
7. Any other pages with footers

### How to Update:

Find this commented section in each footer:

```html
<!-- TODO: Uncomment and add real social media URLs when accounts are created
<div class="footer-social">
  <a href="https://www.facebook.com/YourPageHere" target="_blank" rel="noopener" aria-label="Facebook">
    ...
  </a>
  ...
</div>
-->
```

**Replace with:**

```html
<div class="footer-social">
  <a href="https://www.facebook.com/ResilienceSolutionsGA" target="_blank" rel="noopener" aria-label="Facebook">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M9 8h-3v4h3v12h5v-12h3.642l.358-4h-4v-1.667c0-.955.192-1.333 1.115-1.333h2.885v-5h-3.808c-3.596 0-5.192 1.583-5.192 4.615v3.385z"/></svg>
  </a>
  <a href="https://www.instagram.com/resiliencesolutionsga" target="_blank" rel="noopener" aria-label="Instagram">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
  </a>
  <a href="https://twitter.com/ResilienceSolGA" target="_blank" rel="noopener" aria-label="Twitter/X">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
  </a>
</div>
```

---

## Step 3: Add Social Schema Markup (Optional but Recommended)

Once social accounts are active, add them to the JSON-LD schema in `/index.html`:

Find the existing schema block and add `sameAs` property:

```json
{
  "@context": "https://schema.org",
  "@type": "HomeAndConstructionBusiness",
  "name": "Resilience Solutions",
  "url": "https://resiliencesolutionsga.com/",
  "telephone": "+1-678-697-1957",
  "sameAs": [
    "https://www.facebook.com/ResilienceSolutionsGA",
    "https://www.instagram.com/resiliencesolutionsga",
    "https://twitter.com/ResilienceSolGA"
  ],
  "address": {
    "@type": "PostalAddress",
    ...
  }
}
```

This helps search engines understand your social presence and can display social links in search results.

---

## Step 4: Test All Links

After uncommenting and updating URLs:

1. Clear browser cache
2. Visit resiliencesolutionsga.com
3. Scroll to footer
4. Click each social icon to verify:
   - Link opens in new tab
   - Link goes to correct profile
   - Profile is public and accessible
5. Test on mobile devices
6. Verify icons display correctly

---

## Content Strategy for Social Media

### Facebook:
- Share completed project photos
- Post customer testimonials (with permission)
- Share blog post links
- Respond to reviews promptly
- Post monthly promotions/specials

### Instagram:
- Before/after transformation photos
- Behind-the-scenes work shots
- Time-lapse videos of projects
- Color palette inspiration
- Use hashtags: #CummingGA #HomeRemodeling #InteriorPainting

### X/Twitter:
- Share blog post snippets
- Quick home improvement tips
- Industry news and trends
- Engage with local community accounts

---

## Important Notes

⚠️ **Do NOT uncomment social links until accounts are live and active.**

Broken social links harm credibility more than having no social links at all.

✅ **The CSS styling is already in place** - social icons will display correctly as soon as you uncomment the HTML.

📱 **Mobile responsive** - Social icons are optimized for all screen sizes.

♿ **Accessible** - Icons include proper `aria-label` attributes for screen readers.

---

## Verification Checklist

Before going live with social links:

- [ ] All accounts created and fully configured
- [ ] At least 5-10 posts on each platform
- [ ] Profile photos/cover images uploaded
- [ ] Business information complete (hours, location, contact)
- [ ] Website linked in all bios
- [ ] HTML updated with real URLs (no "YourPageHere" placeholders)
- [ ] JSON-LD schema updated with `sameAs` URLs
- [ ] All links tested in browser
- [ ] Mobile display verified
- [ ] Analytics tracking set up (optional)

---

**Last Updated:** January 10, 2026  
**Status:** Ready to activate once social accounts are created

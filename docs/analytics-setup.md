# Analytics & Tracking Setup Guide

## Google Analytics 4 (GA4) Setup

### Step 1: Create GA4 Property
1. Go to [Google Analytics](https://analytics.google.com/)
2. Click "Admin" (gear icon in bottom left)
3. Under "Property" column, click "Create Property"
4. Enter property details:
   - Property name: "Resilience Solutions Website"
   - Reporting time zone: "United States - Eastern Time"
   - Currency: "US Dollar"
5. Click "Next" and complete business information
6. Click "Create" and accept Terms of Service

### Step 2: Set Up Data Stream
1. After creating property, select "Web" platform
2. Enter website details:
   - Website URL: `https://resiliencesolutionsga.com`
   - Stream name: "Resilience Solutions Main Site"
3. Click "Create stream"
4. **Copy the Measurement ID** (format: `G-XXXXXXXXXX`)

### Step 3: Install Tracking Code
Add the following code to the `<head>` section of all HTML pages, replacing `G-XXXXXXXXXX` with your actual Measurement ID:

```html
<!-- Google Analytics 4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

**Files to update:**
- `/index.html`
- `/projects.html`
- `/privacy.html`
- `/blog/index.html`
- All blog post HTML files (6 files)
- `/services/interior-painting/index.html`
- All other service pages when populated
- `/thanks/index.html`

### Step 4: Verify Installation
1. Visit your website after deploying the tracking code
2. In GA4, go to "Reports" → "Realtime"
3. You should see your own visit appear within 30 seconds
4. Navigate to different pages to test page view tracking

---

## Google Search Console Setup

### Step 1: Add Property
1. Go to [Google Search Console](https://search.google.com/search-console)
2. Click "Add Property"
3. Choose "URL prefix" method
4. Enter: `https://resiliencesolutionsga.com`
5. Click "Continue"

### Step 2: Verify Ownership (HTML tag method - Recommended)
1. Select "HTML tag" verification method
2. Copy the meta tag provided (looks like: `<meta name="google-site-verification" content="abc123xyz...">`)
3. Add it to the `<head>` section of `/index.html` **before** the closing `</head>` tag
4. Deploy the updated file to your live site
5. Return to Search Console and click "Verify"

**Example meta tag location in index.html:**
```html
  <!-- Google Search Console Verification -->
  <meta name="google-site-verification" content="YOUR-VERIFICATION-CODE-HERE">
  
  <script defer src="/script.js"></script>
</head>
```

### Step 3: Submit Sitemap
1. After verification, in Search Console dashboard, click "Sitemaps" in left sidebar
2. Enter sitemap URL: `https://resiliencesolutionsga.com/sitemap.xml`
3. Click "Submit"
4. Wait 24-48 hours for Google to crawl your sitemap

### Step 4: Request Indexing for Key Pages
1. In Search Console, use "URL Inspection" tool (top of page)
2. Enter URLs to request indexing:
   - `https://resiliencesolutionsga.com/`
   - `https://resiliencesolutionsga.com/projects.html`
   - `https://resiliencesolutionsga.com/blog/`
   - `https://resiliencesolutionsga.com/services/interior-painting/`
3. Click "Request Indexing" for each URL
4. Repeat for other high-priority pages

---

## Facebook Pixel (Optional - if running ads)

If you plan to run Facebook/Instagram ads, add the Facebook Pixel:

### Step 1: Create Pixel
1. Go to [Facebook Events Manager](https://business.facebook.com/events_manager)
2. Click "Connect Data Sources" → "Web" → "Facebook Pixel"
3. Name your pixel: "Resilience Solutions Website"
4. Copy the Pixel ID

### Step 2: Install Base Code
Add to `<head>` of all pages:

```html
<!-- Facebook Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', 'YOUR-PIXEL-ID');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=YOUR-PIXEL-ID&ev=PageView&noscript=1"
/></noscript>
<!-- End Facebook Pixel Code -->
```

### Step 3: Track Conversions
Add conversion tracking to `/thanks/index.html`:

```html
<script>
  fbq('track', 'Lead');
</script>
```

---

## Tracking Best Practices

### Event Tracking (GA4)
Add custom event tracking for important user actions:

**Contact form submission** (in `/script.js` after form success):
```javascript
if (typeof gtag !== 'undefined') {
  gtag('event', 'form_submit', {
    'event_category': 'Contact',
    'event_label': 'Contact Form'
  });
}
```

**Phone number clicks**:
```html
<a href="tel:678-697-1957" onclick="gtag('event', 'click', {'event_category': 'Contact', 'event_label': 'Phone Call'});">
  678-697-1957
</a>
```

**Email clicks**:
```html
<a href="mailto:resiliencesolutions.us@gmail.com" onclick="gtag('event', 'click', {'event_category': 'Contact', 'event_label': 'Email'});">
  resiliencesolutions.us@gmail.com
</a>
```

### Privacy Considerations
Since you have a privacy policy at `/privacy.html`, update it to mention:
1. Use of Google Analytics for website performance tracking
2. Use of cookies for analytics purposes
3. User's ability to opt-out using browser settings or [Google Analytics Opt-out Add-on](https://tools.google.com/dlpage/gaoptout)

---

## Implementation Checklist

- [ ] Create GA4 property and get Measurement ID
- [ ] Add GA4 tracking code to all HTML pages
- [ ] Verify GA4 is receiving data (check Realtime reports)
- [ ] Add property to Google Search Console
- [ ] Verify ownership using HTML meta tag
- [ ] Submit sitemap.xml to Search Console
- [ ] Request indexing for key pages
- [ ] Add event tracking for contact form submissions
- [ ] Add event tracking for phone/email clicks
- [ ] Update privacy policy to mention analytics
- [ ] (Optional) Set up Facebook Pixel if running ads
- [ ] Test all tracking in incognito/private browsing mode

---

## Monitoring & Optimization

### Weekly Checks (First Month)
- Review GA4 Realtime reports to confirm tracking works
- Check Search Console "Coverage" report for indexing issues
- Monitor "Performance" report for ranking improvements
- Review "Search queries" to see what keywords drive traffic

### Monthly Reviews (Ongoing)
- Analyze top landing pages in GA4
- Review conversion rates (form submissions)
- Check Search Console for new ranking keywords
- Identify high-bounce pages and optimize content
- Review mobile vs desktop traffic split
- Monitor page load speeds in GA4

### Quarterly Optimization
- Review top performing blog posts and create similar content
- Identify pages with high exit rates and improve CTAs
- Analyze geographic data to focus marketing efforts
- Review top referral sources and build relationships
- Update content on pages with declining traffic

---

**Last Updated:** January 10, 2026  
**Next Review:** After GA4 and Search Console setup (within 1 week)

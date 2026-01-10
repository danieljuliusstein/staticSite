# Email DNS Configuration for resiliencesolutionsga.com

## Current SPF Record

The domain currently has the following SPF record configured:

```
v=spf1 include:_spf.porkbun.com ~all
```

**What this means:**
- `v=spf1` - SPF version 1
- `include:_spf.porkbun.com` - Allows Porkbun mail servers to send email on behalf of this domain
- `~all` - Soft fail for all other servers (logged but not rejected)

## Recommended DMARC Record

To improve email deliverability and protect against spoofing, add the following DMARC record:

**DNS Record Type:** TXT  
**Host/Name:** `_dmarc.resiliencesolutionsga.com` or `_dmarc` (depending on your DNS provider)  
**Value:**
```
v=DMARC1; p=none; rua=mailto:resiliencesolutions.us@gmail.com; adkim=s; aspf=s
```

### DMARC Policy Explanation

- `v=DMARC1` - DMARC version 1
- `p=none` - Policy is set to "none" (monitoring mode - no action taken on failures)
- `rua=mailto:resiliencesolutions.us@gmail.com` - Aggregate reports sent to this email address
- `adkim=s` - Strict DKIM alignment (domain must match exactly)
- `aspf=s` - Strict SPF alignment (domain must match exactly)

### DMARC Deployment Strategy

**Phase 1 - Monitoring (Start Here):**
- Use `p=none` to monitor email authentication without blocking any messages
- Review aggregate reports for 2-4 weeks to identify legitimate senders
- Fix any authentication issues with legitimate email sources

**Phase 2 - Quarantine (After Monitoring):**
- Change to `p=quarantine` to send failing messages to spam/junk folders
- Monitor for another 2-4 weeks
- Ensure all legitimate email passes authentication

**Phase 3 - Reject (Final Step):**
- Change to `p=reject` to block all unauthenticated emails
- This provides maximum protection against spoofing and phishing
- Only implement after confirming all legitimate sources pass authentication

### Example Progressive DMARC Records

**Phase 1 (Current Recommendation):**
```
v=DMARC1; p=none; rua=mailto:resiliencesolutions.us@gmail.com; adkim=s; aspf=s
```

**Phase 2 (After 2-4 weeks):**
```
v=DMARC1; p=quarantine; rua=mailto:resiliencesolutions.us@gmail.com; adkim=s; aspf=s
```

**Phase 3 (Final):**
```
v=DMARC1; p=reject; rua=mailto:resiliencesolutions.us@gmail.com; adkim=s; aspf=s
```

## Additional Recommendations

1. **DKIM Signing:** Ensure your email provider (Porkbun) has DKIM configured and the public key is in your DNS records.

2. **Monitor Reports:** Check aggregate reports regularly at resiliencesolutions.us@gmail.com to identify authentication issues.

3. **Test Before Deployment:** Use tools like [MXToolbox DMARC Analyzer](https://mxtoolbox.com/dmarc.aspx) to validate your DMARC record syntax.

4. **Document Email Sources:** Keep a list of all services that send email on behalf of your domain (contact forms, CRM, etc.).

## How to Add DMARC Record

1. Log into your DNS provider (Porkbun)
2. Navigate to DNS management for resiliencesolutionsga.com
3. Add new TXT record:
   - **Type:** TXT
   - **Host:** `_dmarc`
   - **Value:** `v=DMARC1; p=none; rua=mailto:resiliencesolutions.us@gmail.com; adkim=s; aspf=s`
   - **TTL:** 3600 (or default)
4. Save changes
5. Wait 24-48 hours for DNS propagation
6. Verify using `dig _dmarc.resiliencesolutionsga.com TXT` or online DMARC checker

## Verification Commands

Check SPF record:
```bash
dig resiliencesolutionsga.com TXT +short | grep spf
```

Check DMARC record:
```bash
dig _dmarc.resiliencesolutionsga.com TXT +short
```

Check DKIM record (replace `selector` with actual DKIM selector):
```bash
dig selector._domainkey.resiliencesolutionsga.com TXT +short
```

---

**Last Updated:** January 10, 2026  
**Next Review:** After implementing Phase 1 DMARC (2-4 weeks)

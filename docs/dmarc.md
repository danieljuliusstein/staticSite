# DMARC Implementation Guide for resiliencesolutionsga.com

## Overview
DMARC (Domain-based Message Authentication, Reporting, and Conformance) helps prevent email spoofing and phishing by ensuring that emails claiming to be from your domain are legitimate.

## Prerequisites
Before implementing DMARC, ensure you have:
1. **SPF (Sender Policy Framework)** configured
2. **DKIM (DomainKeys Identified Mail)** configured

## Step 1: Verify Current SPF Status
1. Go to https://mxtoolbox.com/spf.aspx
2. Enter: `resiliencesolutionsga.com`
3. Verify you have an SPF record that looks like:
   ```
   v=spf1 include:_spf.google.com ~all
   ```
   (Adjust based on your actual email provider)

## Step 2: Verify Current DKIM Status
1. Go to https://mxtoolbox.com/dkim.aspx
2. Enter your domain and selector (usually `default` or `google`)
3. Verify DKIM is configured correctly

⚠️ **IMPORTANT**: Do NOT proceed with DMARC until SPF and DKIM are working.

## Step 3: Create DMARC Record (Monitoring Phase)
Add a new DNS TXT record in Cloudflare:

**Record Details:**
- **Type**: TXT
- **Name**: `_dmarc`
- **Content**: 
  ```
  v=DMARC1; p=none; rua=mailto:dmarc-reports@resiliencesolutionsga.com; ruf=mailto:dmarc-forensic@resiliencesolutionsga.com; fo=1; adkim=s; aspf=s; pct=100
  ```

**What each parameter means:**
- `v=DMARC1` - Version identifier (required)
- `p=none` - Policy (start with "none" for monitoring only)
- `rua=` - Aggregate report email (where daily summaries go)
- `ruf=` - Forensic report email (where failure details go)
- `fo=1` - Generate forensic reports if any auth fails
- `adkim=s` - Strict DKIM alignment
- `aspf=s` - Strict SPF alignment
- `pct=100` - Apply policy to 100% of messages

## Step 4: Set Up Report Mailbox
**Option A: Use your existing email**
- Forward `dmarc-reports@resiliencesolutionsga.com` to `resiliencesolutions.us@gmail.com`
- Be prepared to receive multiple reports per day

**Option B: Use a DMARC report service (Recommended)**
- Services like Postmark, Dmarcian, or Google Postmaster Tools can parse reports
- These services provide dashboards instead of raw XML emails
- Many offer free tiers for small domains

⚠️ **WARNING**: DMARC reports are sent as XML attachments and can be difficult to read manually. Consider using a parsing service.

## Step 5: Monitor for 2-4 Weeks
After adding the DMARC record with `p=none`:
1. Check reports daily for the first week
2. Look for:
   - Any legitimate emails failing DKIM or SPF
   - Sources sending email claiming to be from your domain
   - Percentage of emails passing authentication

3. Common issues to fix:
   - Contact form emails not properly configured
   - Third-party services (Formspree, etc.) not aligned
   - Forwarding rules breaking authentication

## Step 6: Move to Quarantine Policy
After 2-4 weeks of monitoring with no issues, update your DMARC record:

```
v=DMARC1; p=quarantine; rua=mailto:dmarc-reports@resiliencesolutionsga.com; ruf=mailto:dmarc-forensic@resiliencesolutionsga.com; fo=1; adkim=s; aspf=s; pct=10
```

Changes:
- `p=quarantine` - Failed emails go to spam
- `pct=10` - Only apply to 10% of mail (gradual rollout)

Monitor for another 2 weeks. If no issues, increase `pct=` to 25, 50, 75, then 100.

## Step 7: Move to Reject Policy (Final Step)
Once you're confident all legitimate email is passing:

```
v=DMARC1; p=reject; rua=mailto:dmarc-reports@resiliencesolutionsga.com; ruf=mailto:dmarc-forensic@resiliencesolutionsga.com; fo=1; adkim=s; aspf=s; pct=100
```

Changes:
- `p=reject` - Failed emails are rejected outright
- `pct=100` - Apply to all email

## Implementation Checklist
- [ ] Verify SPF is configured
- [ ] Verify DKIM is configured
- [ ] Set up report email or service
- [ ] Add DMARC TXT record with `p=none`
- [ ] Monitor reports for 2-4 weeks
- [ ] Fix any authentication issues
- [ ] Upgrade to `p=quarantine` with `pct=10`
- [ ] Gradually increase `pct=` to 100
- [ ] Monitor for 2 more weeks
- [ ] Upgrade to `p=reject` with `pct=100`
- [ ] Continue monitoring indefinitely

## Cloudflare DNS Instructions
1. Log into Cloudflare dashboard
2. Select `resiliencesolutionsga.com`
3. Go to **DNS** → **Records**
4. Click **Add record**
5. Set:
   - Type: `TXT`
   - Name: `_dmarc`
   - Content: (paste DMARC record from Step 3)
   - TTL: Auto
6. Click **Save**
7. Wait 5-15 minutes for DNS propagation
8. Verify: https://mxtoolbox.com/dmarc.aspx

## Verification
After adding the record, verify it's working:
```bash
dig TXT _dmarc.resiliencesolutionsga.com
```

Or use: https://mxtoolbox.com/dmarc.aspx

## Troubleshooting
**Issue**: No reports received after 24 hours
- Verify DNS record is correct (no typos)
- Check report email is valid and receiving mail
- Some senders may not send reports

**Issue**: High failure rate in reports
- Check SPF includes all legitimate sending sources
- Verify DKIM selector matches email service
- Review forensic reports for specific failures

**Issue**: Legitimate email being rejected
- Immediately revert to `p=none`
- Investigate which emails are failing
- Fix authentication before re-enabling stricter policy

## Additional Resources
- [DMARC.org Official Guide](https://dmarc.org/overview/)
- [Google DMARC Setup](https://support.google.com/a/answer/2466580)
- [MXToolbox DMARC Checker](https://mxtoolbox.com/dmarc.aspx)
- [Postmark DMARC Guide](https://postmarkapp.com/guides/dmarc)

## Notes
- DMARC does **not** prevent spam from being sent from your domain
- It **does** help receiving servers identify and reject spoofed messages
- Always start with `p=none` and monitor before enforcing
- Keep reports enabled even after full deployment

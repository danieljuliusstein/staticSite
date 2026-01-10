#!/usr/bin/env python3
"""
Site Validation Script for resiliencesolutionsga.com
Validates SEO audit compliance and checks for common issues.
"""

import os
import re
from pathlib import Path
from collections import defaultdict

# Configuration
SITE_ROOT = Path(__file__).parent.parent
REPORT_FILE = SITE_ROOT / "tools" / "validate_report.md"

# Expected values
EXPECTED_SOCIAL_URLS = {
    "facebook": "https://www.facebook.com/people/Resilience-Solutions/61575021121406/",
    "instagram": "https://www.instagram.com/resilience_solutions/",
    "x": "https://x.com/ResilienceSolGA"
}

# Results
errors = []
warnings = []
passed = []


def find_html_files():
    """Find all HTML files in the site."""
    html_files = []
    for root, dirs, files in os.walk(SITE_ROOT):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['tools', 'docs']]
        for file in files:
            if file.endswith('.html'):
                html_files.append(Path(root) / file)
    return html_files


def check_no_http_protocol(file_path, content):
    """Check for http:// (insecure) references."""
    http_matches = re.findall(r'http://resiliencesolutionsga\.com', content, re.IGNORECASE)
    if http_matches:
        errors.append(f"{file_path.name}: Contains insecure http:// reference to own domain")
        return False
    return True


def check_no_www_subdomain(file_path, content):
    """Check for www subdomain (canonical is apex)."""
    www_matches = re.findall(r'www\.resiliencesolutionsga\.com', content, re.IGNORECASE)
    # Filter out social links which legitimately use www.facebook.com, etc.
    domain_www = [m for m in www_matches if 'facebook' not in m.lower() and 'instagram' not in m.lower()]
    if domain_www:
        errors.append(f"{file_path.name}: Contains www subdomain (canonical is apex domain)")
        return False
    return True


def check_directory_trailing_slash(file_path, content):
    """Check that directory links use trailing slashes."""
    # Check for /blog without trailing slash
    blog_no_slash = re.findall(r'href=["\']\/blog["\']', content)
    if blog_no_slash:
        errors.append(f"{file_path.name}: Link to /blog missing trailing slash (should be /blog/)")
        return False
    
    # Check for service directory links without trailing slash
    service_no_slash = re.findall(r'href=["\']\/services\/[^"\']*[^\/]["\']', content)
    if service_no_slash:
        warnings.append(f"{file_path.name}: Service directory links may be missing trailing slashes")
    
    return True


def check_social_urls(file_path, content):
    """Verify social media URLs match expected values."""
    issues = []
    
    # Check Facebook
    fb_matches = re.findall(r'href=["\']([^"\']*facebook\.com[^"\']*)["\']', content, re.IGNORECASE)
    for match in fb_matches:
        if match != EXPECTED_SOCIAL_URLS["facebook"]:
            issues.append(f"Incorrect Facebook URL: {match}")
    
    # Check Instagram
    ig_matches = re.findall(r'href=["\']([^"\']*instagram\.com[^"\']*)["\']', content, re.IGNORECASE)
    for match in ig_matches:
        if match != EXPECTED_SOCIAL_URLS["instagram"]:
            issues.append(f"Incorrect Instagram URL: {match}")
    
    # Check X/Twitter
    x_matches = re.findall(r'href=["\']([^"\']*(?:x\.com|twitter\.com)[^"\']*)["\']', content, re.IGNORECASE)
    for match in x_matches:
        if 'x.com' in match.lower() and match != EXPECTED_SOCIAL_URLS["x"]:
            issues.append(f"Incorrect X URL: {match}")
    
    if issues:
        errors.append(f"{file_path.name}: {', '.join(issues)}")
        return False
    return True


def check_external_link_security(file_path, content):
    """Check that external links with target=_blank have proper rel attributes."""
    # Find all <a> tags with target="_blank"
    blank_links = re.findall(r'<a\s+[^>]*target=["\']_blank["\'][^>]*>', content, re.IGNORECASE)
    
    issues = []
    for link in blank_links:
        # Check if it has both noopener and noreferrer
        if 'rel=' not in link.lower():
            issues.append("Missing rel attribute")
        elif 'noopener' not in link.lower() or 'noreferrer' not in link.lower():
            issues.append("Missing noopener or noreferrer")
    
    if issues:
        errors.append(f"{file_path.name}: {len(issues)} external link(s) missing security attributes")
        return False
    return True


def check_homepage_title_length():
    """Check that homepage title is 50-60 characters."""
    index_file = SITE_ROOT / "index.html"
    if not index_file.exists():
        errors.append("index.html not found")
        return False
    
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title_match = re.search(r'<title>([^<]+)</title>', content, re.IGNORECASE)
    if not title_match:
        errors.append("Homepage: No <title> tag found")
        return False
    
    title = title_match.group(1)
    title_len = len(title)
    
    if title_len < 50:
        errors.append(f"Homepage: Title too short ({title_len} chars, need 50-60)")
        return False
    elif title_len > 60:
        errors.append(f"Homepage: Title too long ({title_len} chars, need 50-60)")
        return False
    else:
        passed.append(f"Homepage: Title length optimal ({title_len} chars)")
        return True


def generate_report():
    """Generate validation report."""
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write("# Site Validation Report\n\n")
        f.write("**Script**: validate_site.py\n\n")
        
        # Summary
        f.write("## Summary\n\n")
        f.write(f"- ✅ Passed: {len(passed)}\n")
        f.write(f"- ⚠️  Warnings: {len(warnings)}\n")
        f.write(f"- ❌ Errors: {len(errors)}\n\n")
        
        if errors:
            f.write("---\n\n")
            f.write("## ❌ Errors (Must Fix)\n\n")
            for error in errors:
                f.write(f"- {error}\n")
            f.write("\n")
        
        if warnings:
            f.write("---\n\n")
            f.write("## ⚠️ Warnings (Should Fix)\n\n")
            for warning in warnings:
                f.write(f"- {warning}\n")
            f.write("\n")
        
        if passed:
            f.write("---\n\n")
            f.write("## ✅ Passed Checks\n\n")
            for check in passed:
                f.write(f"- {check}\n")
            f.write("\n")
        
        # Final verdict
        f.write("---\n\n")
        if errors:
            f.write("## Verdict: ❌ FAIL\n\n")
            f.write(f"Found {len(errors)} error(s) that must be fixed.\n")
        elif warnings:
            f.write("## Verdict: ⚠️  PASS WITH WARNINGS\n\n")
            f.write(f"Found {len(warnings)} warning(s) that should be reviewed.\n")
        else:
            f.write("## Verdict: ✅ PASS\n\n")
            f.write("All validation checks passed!\n")
    
    print(f"\nReport written to: {REPORT_FILE}")


def main():
    """Run all validation checks."""
    print("="*60)
    print("SITE VALIDATION SCRIPT")
    print("="*60)
    print()
    
    # Check homepage title first
    print("Checking homepage title length...")
    check_homepage_title_length()
    
    # Find all HTML files
    html_files = find_html_files()
    print(f"Found {len(html_files)} HTML files\n")
    
    print("Running validation checks...")
    file_checks = 0
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Run all checks
            check_no_http_protocol(file_path, content)
            check_no_www_subdomain(file_path, content)
            check_directory_trailing_slash(file_path, content)
            check_social_urls(file_path, content)
            check_external_link_security(file_path, content)
            
            file_checks += 1
            
        except Exception as e:
            errors.append(f"{file_path.name}: Error reading file - {e}")
    
    # Add pass count
    if not errors and not warnings:
        passed.append(f"All {file_checks} HTML files validated successfully")
    
    # Generate report
    generate_report()
    
    # Print summary
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)
    print(f"Files checked: {file_checks}")
    print(f"✅ Passed: {len(passed)}")
    print(f"⚠️  Warnings: {len(warnings)}")
    print(f"❌ Errors: {len(errors)}")
    print("="*60)
    
    if errors:
        print("\n❌ VALIDATION FAILED")
        print("Check validate_report.md for details")
        return 1
    elif warnings:
        print("\n⚠️  VALIDATION PASSED WITH WARNINGS")
        print("Check validate_report.md for details")
        return 0
    else:
        print("\n✅ ALL VALIDATION CHECKS PASSED!")
        return 0


if __name__ == "__main__":
    exit(main())

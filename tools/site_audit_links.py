#!/usr/bin/env python3
"""
Link Validation Script for static-site
Scans all HTML files, validates internal links, checks anchor IDs, and verifies external link security attributes.
"""

import os
import re
from pathlib import Path
from urllib.parse import urlparse, urljoin
from collections import defaultdict

# Configuration
SITE_ROOT = Path(__file__).parent.parent
DOMAIN = "https://resiliencesolutionsga.com"
REPORT_FILE = SITE_ROOT / "tools" / "audit_report.md"

# Results storage
broken_links = []
broken_anchors = []
missing_security_attrs = []
all_html_files = []
all_internal_links = []
all_external_links = []
anchor_ids = defaultdict(list)  # file -> list of IDs


def find_html_files():
    """Find all HTML files in the site."""
    html_files = []
    for root, dirs, files in os.walk(SITE_ROOT):
        # Skip hidden directories and tools folder
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'tools']
        for file in files:
            if file.endswith('.html'):
                html_files.append(Path(root) / file)
    return html_files


def extract_links_and_ids(file_path):
    """Extract all href links and id attributes from an HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return [], [], []

    # Extract href attributes
    href_pattern = r'href=["\']([^"\']+)["\']'
    hrefs = re.findall(href_pattern, content)

    # Extract id attributes
    id_pattern = r'id=["\']([^"\']+)["\']'
    ids = re.findall(id_pattern, content)

    # Extract external links with their full <a> tags to check rel/target
    external_link_pattern = r'<a\s+[^>]*href=["\'](?:https?://|//)(?!resiliencesolutionsga\.com)[^"\']+["\'][^>]*>'
    external_full_tags = re.findall(external_link_pattern, content, re.IGNORECASE)

    return hrefs, ids, external_full_tags


def is_external(href):
    """Check if a link is external."""
    parsed = urlparse(href)
    if parsed.scheme in ('http', 'https') or href.startswith('//'):
        # It's external unless it's our domain
        return 'resiliencesolutionsga.com' not in href
    return False


def is_valid_internal_link(href, current_file, all_files, all_ids):
    """Check if an internal link is valid (file exists and anchor ID exists if specified)."""
    # Skip special hrefs
    if href.startswith(('#', 'mailto:', 'tel:', 'javascript:')):
        return True, None
    
    # Skip absolute URLs (canonical links, etc.)
    if href.startswith('http://') or href.startswith('https://'):
        return True, None
    
    # Skip query-string-only files (CSS/JS with version params)
    if '?' in href and not href.startswith('?'):
        # Remove query string for file checking
        href = href.split('?')[0]

    # Parse anchor
    if '#' in href:
        path_part, anchor = href.split('#', 1)
    else:
        path_part, anchor = href, None

    # Resolve path relative to current file
    if path_part == '':
        # Just an anchor on the current page
        target_file = current_file
    elif path_part == '/':
        # Root with anchor (e.g., /#about points to index.html)
        target_file = SITE_ROOT / 'index.html'
    elif path_part.startswith('/'):
        # Absolute path from site root
        target_file = SITE_ROOT / path_part.lstrip('/')
        # If it's a directory, assume index.html
        if target_file.is_dir():
            target_file = target_file / 'index.html'
    else:
        # Relative path
        target_file = (current_file.parent / path_part).resolve()
        if target_file.is_dir():
            target_file = target_file / 'index.html'

    # Check if file exists (skip if it's a CSS/JS/asset file)
    if target_file.suffix in ['.css', '.js', '.svg', '.jpg', '.png', '.webp', '.ico', '.xml', '.txt']:
        return True, None  # Don't validate asset existence
    
    if not target_file.exists():
        return False, f"File not found: {target_file.relative_to(SITE_ROOT)}"

    # Check anchor if specified
    if anchor:
        if target_file not in all_ids or anchor not in all_ids[target_file]:
            return False, f"Anchor #{anchor} not found in {target_file.relative_to(SITE_ROOT)}"

    return True, None


def check_external_link_security(full_tag):
    """Check if an external link has proper security attributes."""
    # Extract href
    href_match = re.search(r'href=["\']([^"\']+)["\']', full_tag)
    if not href_match:
        return True, None
    
    href = href_match.group(1)
    
    # Check for target="_blank"
    has_target_blank = 'target="_blank"' in full_tag or "target='_blank'" in full_tag
    
    # Check for rel="noopener noreferrer"
    has_proper_rel = ('rel="noopener noreferrer"' in full_tag or 
                      'rel="noreferrer noopener"' in full_tag or
                      "rel='noopener noreferrer'" in full_tag or
                      "rel='noreferrer noopener'" in full_tag)
    
    if not has_target_blank or not has_proper_rel:
        return False, href
    
    return True, None


def generate_report():
    """Generate markdown report."""
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write("# Site Audit Link Validation Report\n\n")
        f.write(f"**Generated:** {Path(__file__).name}\n\n")
        f.write(f"**Files Scanned:** {len(all_html_files)}\n\n")
        
        # Summary
        f.write("## Summary\n\n")
        f.write(f"- Total HTML files: {len(all_html_files)}\n")
        f.write(f"- Total internal links: {len(all_internal_links)}\n")
        f.write(f"- Total external links: {len(all_external_links)}\n")
        f.write(f"- Broken internal links: {len(broken_links)}\n")
        f.write(f"- Broken anchors: {len(broken_anchors)}\n")
        f.write(f"- External links missing security attrs: {len(missing_security_attrs)}\n\n")
        
        # Status
        if not broken_links and not broken_anchors and not missing_security_attrs:
            f.write("✅ **All checks passed!**\n\n")
        else:
            f.write("⚠️ **Issues found** - see details below.\n\n")
        
        # Broken Links
        if broken_links:
            f.write("## Broken Internal Links\n\n")
            for file, href, error in broken_links:
                f.write(f"- **{file.relative_to(SITE_ROOT)}**\n")
                f.write(f"  - Link: `{href}`\n")
                f.write(f"  - Error: {error}\n\n")
        
        # Broken Anchors
        if broken_anchors:
            f.write("## Broken Anchor Links\n\n")
            for file, href, error in broken_anchors:
                f.write(f"- **{file.relative_to(SITE_ROOT)}**\n")
                f.write(f"  - Link: `{href}`\n")
                f.write(f"  - Error: {error}\n\n")
        
        # Missing Security Attributes
        if missing_security_attrs:
            f.write("## External Links Missing Security Attributes\n\n")
            f.write("These external links should have `target=\"_blank\" rel=\"noopener noreferrer\"`:\n\n")
            for file, href in missing_security_attrs:
                f.write(f"- **{file.relative_to(SITE_ROOT)}**\n")
                f.write(f"  - Link: `{href}`\n\n")
    
    print(f"Report written to: {REPORT_FILE}")


def main():
    """Main validation logic."""
    print("Starting link validation...")
    
    # Find all HTML files
    global all_html_files
    all_html_files = find_html_files()
    print(f"Found {len(all_html_files)} HTML files")
    
    # First pass: collect all IDs
    print("Collecting anchor IDs...")
    for file_path in all_html_files:
        _, ids, _ = extract_links_and_ids(file_path)
        anchor_ids[file_path] = ids
    
    # Second pass: validate links
    print("Validating links...")
    for file_path in all_html_files:
        hrefs, _, external_tags = extract_links_and_ids(file_path)
        
        for href in hrefs:
            if is_external(href):
                all_external_links.append((file_path, href))
            else:
                all_internal_links.append((file_path, href))
                # Validate internal link
                valid, error = is_valid_internal_link(href, file_path, all_html_files, anchor_ids)
                if not valid:
                    if '#' in href:
                        broken_anchors.append((file_path, href, error))
                    else:
                        broken_links.append((file_path, href, error))
        
        # Check external link security
        for full_tag in external_tags:
            secure, href = check_external_link_security(full_tag)
            if not secure:
                missing_security_attrs.append((file_path, href))
    
    # Generate report
    generate_report()
    
    # Print summary to console
    print("\n" + "="*60)
    print("LINK VALIDATION SUMMARY")
    print("="*60)
    print(f"Files scanned: {len(all_html_files)}")
    print(f"Internal links: {len(all_internal_links)}")
    print(f"External links: {len(all_external_links)}")
    print(f"Broken links: {len(broken_links)}")
    print(f"Broken anchors: {len(broken_anchors)}")
    print(f"Missing security attributes: {len(missing_security_attrs)}")
    print("="*60)
    
    if broken_links or broken_anchors or missing_security_attrs:
        print("⚠️  Issues found - check audit_report.md for details")
        return 1
    else:
        print("✅ All link checks passed!")
        return 0


if __name__ == "__main__":
    exit(main())

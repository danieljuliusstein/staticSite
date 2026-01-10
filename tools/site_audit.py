#!/usr/bin/env python3
"""
Site Audit Script for resiliencesolutionsga.com
Validates internal links, assets, and anchor references across all HTML files.
"""

import os
import re
import json
from pathlib import Path
from urllib.parse import urlparse, urljoin
from collections import defaultdict
from html.parser import HTMLParser

class LinkParser(HTMLParser):
    """Parse HTML and extract links, assets, and IDs"""
    
    def __init__(self):
        super().__init__()
        self.links = []
        self.assets = []
        self.ids = set()
        self.anchors = []
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        # Extract IDs
        if 'id' in attrs_dict:
            self.ids.add(attrs_dict['id'])
        
        # Extract links
        if tag == 'a' and 'href' in attrs_dict:
            self.links.append(attrs_dict['href'])
            if attrs_dict['href'].startswith('#'):
                self.anchors.append(attrs_dict['href'][1:])
        
        # Extract assets
        if tag == 'img' and 'src' in attrs_dict:
            self.assets.append(('img', attrs_dict['src']))
        elif tag == 'script' and 'src' in attrs_dict:
            self.assets.append(('script', attrs_dict['src']))
        elif tag == 'link' and 'href' in attrs_dict:
            href = attrs_dict['href']
            # Only check internal stylesheets and local resources
            if not href.startswith(('http://', 'https://', '//')):
                self.assets.append(('link', href))

def find_html_files(root_dir):
    """Recursively find all HTML files"""
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        # Skip hidden directories and node_modules
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return html_files

def normalize_path(path, base_path, root_dir):
    """Normalize a path to be relative to root_dir"""
    # Remove query strings and fragments for file existence checks
    path = path.split('?')[0].split('#')[0]
    
    # Skip external URLs
    if path.startswith(('http://', 'https://', '//', 'mailto:', 'tel:')):
        return None
    
    # Handle root-relative paths
    if path.startswith('/'):
        return os.path.join(root_dir, path.lstrip('/'))
    
    # Handle relative paths
    base_dir = os.path.dirname(base_path)
    return os.path.normpath(os.path.join(base_dir, path))

def check_file_exists(path, root_dir):
    """Check if a file or directory exists, handling index.html"""
    if not path:
        return True, None
    
    # Check if exact file exists
    if os.path.isfile(path):
        return True, path
    
    # Check if directory with index.html exists
    if os.path.isdir(path):
        index_path = os.path.join(path, 'index.html')
        if os.path.isfile(index_path):
            return True, index_path
        return False, f"Directory exists but no index.html: {path}"
    
    return False, f"File not found: {path}"

def validate_anchor(anchor, target_file, all_ids):
    """Check if anchor ID exists in target file"""
    if not target_file or target_file not in all_ids:
        return False, f"Target file not parsed: {target_file}"
    
    if anchor in all_ids[target_file]:
        return True, None
    
    return False, f"Anchor #{anchor} not found in {target_file}"

def audit_site(root_dir):
    """Main audit function"""
    results = {
        'total_files': 0,
        'broken_links': [],
        'broken_assets': [],
        'broken_anchors': [],
        'valid_links': 0,
        'valid_assets': 0,
        'valid_anchors': 0,
        'external_links': 0
    }
    
    # Find all HTML files
    html_files = find_html_files(root_dir)
    results['total_files'] = len(html_files)
    
    # Parse all files and collect IDs
    all_ids = {}
    all_data = {}
    
    print(f"Parsing {len(html_files)} HTML files...")
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
                parser = LinkParser()
                parser.feed(content)
                all_ids[html_file] = parser.ids
                all_data[html_file] = {
                    'links': parser.links,
                    'assets': parser.assets,
                    'anchors': parser.anchors
                }
        except Exception as e:
            print(f"Error parsing {html_file}: {e}")
    
    print(f"Validating links and assets...")
    
    # Validate each file
    for html_file, data in all_data.items():
        rel_path = os.path.relpath(html_file, root_dir)
        
        # Check links
        for link in data['links']:
            # Skip external links
            if link.startswith(('http://', 'https://', '//', 'mailto:', 'tel:')):
                results['external_links'] += 1
                continue
            
            # Handle anchor-only links (#about)
            if link.startswith('#'):
                anchor = link[1:]
                is_valid, error = validate_anchor(anchor, html_file, all_ids)
                if is_valid:
                    results['valid_anchors'] += 1
                else:
                    results['broken_anchors'].append({
                        'file': rel_path,
                        'link': link,
                        'error': error
                    })
                continue
            
            # Handle links with anchors (page.html#section or /#section)
            if '#' in link:
                path_part, anchor_part = link.split('#', 1)
                
                # Normalize path
                target_path = normalize_path(path_part if path_part else html_file, html_file, root_dir)
                
                if target_path:
                    # Check file exists
                    exists, resolved_path = check_file_exists(target_path, root_dir)
                    if not exists:
                        results['broken_links'].append({
                            'file': rel_path,
                            'link': link,
                            'error': resolved_path
                        })
                        continue
                    
                    # Check anchor exists
                    is_valid, error = validate_anchor(anchor_part, resolved_path, all_ids)
                    if is_valid:
                        results['valid_anchors'] += 1
                    else:
                        results['broken_anchors'].append({
                            'file': rel_path,
                            'link': link,
                            'error': error
                        })
                else:
                    results['valid_links'] += 1
                
                continue
            
            # Regular page links
            target_path = normalize_path(link, html_file, root_dir)
            if target_path:
                exists, error = check_file_exists(target_path, root_dir)
                if exists:
                    results['valid_links'] += 1
                else:
                    results['broken_links'].append({
                        'file': rel_path,
                        'link': link,
                        'error': error
                    })
        
        # Check assets
        for asset_type, asset_path in data['assets']:
            # Skip external assets
            if asset_path.startswith(('http://', 'https://', '//')):
                results['external_links'] += 1
                continue
            
            target_path = normalize_path(asset_path, html_file, root_dir)
            if target_path:
                exists, error = check_file_exists(target_path, root_dir)
                if exists:
                    results['valid_assets'] += 1
                else:
                    results['broken_assets'].append({
                        'file': rel_path,
                        'type': asset_type,
                        'asset': asset_path,
                        'error': error
                    })
    
    return results

def generate_report(results, output_dir):
    """Generate JSON and Markdown reports"""
    
    # JSON report
    json_path = os.path.join(output_dir, 'audit_report.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    # Markdown report
    md_path = os.path.join(output_dir, 'audit_report.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write("# Site Audit Report\n\n")
        f.write(f"**Generated:** {Path(__file__).stat().st_mtime}\n\n")
        
        f.write("## Summary\n\n")
        f.write(f"- **Total HTML files scanned:** {results['total_files']}\n")
        f.write(f"- **Valid internal links:** {results['valid_links']}\n")
        f.write(f"- **Valid assets:** {results['valid_assets']}\n")
        f.write(f"- **Valid anchors:** {results['valid_anchors']}\n")
        f.write(f"- **External links (not checked):** {results['external_links']}\n")
        f.write(f"- **Broken internal links:** {len(results['broken_links'])}\n")
        f.write(f"- **Broken assets:** {len(results['broken_assets'])}\n")
        f.write(f"- **Broken anchors:** {len(results['broken_anchors'])}\n\n")
        
        if results['broken_links']:
            f.write("## Broken Internal Links\n\n")
            for item in results['broken_links']:
                f.write(f"- **File:** `{item['file']}`\n")
                f.write(f"  - **Link:** `{item['link']}`\n")
                f.write(f"  - **Error:** {item['error']}\n\n")
        
        if results['broken_assets']:
            f.write("## Broken Assets\n\n")
            for item in results['broken_assets']:
                f.write(f"- **File:** `{item['file']}`\n")
                f.write(f"  - **Type:** {item['type']}\n")
                f.write(f"  - **Asset:** `{item['asset']}`\n")
                f.write(f"  - **Error:** {item['error']}\n\n")
        
        if results['broken_anchors']:
            f.write("## Broken Anchor Links\n\n")
            for item in results['broken_anchors']:
                f.write(f"- **File:** `{item['file']}`\n")
                f.write(f"  - **Link:** `{item['link']}`\n")
                f.write(f"  - **Error:** {item['error']}\n\n")
        
        if not results['broken_links'] and not results['broken_assets'] and not results['broken_anchors']:
            f.write("## ✅ All Clear!\n\n")
            f.write("No broken links, assets, or anchors detected.\n")
    
    print(f"\nReports generated:")
    print(f"  - {json_path}")
    print(f"  - {md_path}")

def main():
    # Determine script and project root
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent
    
    print(f"Auditing site at: {root_dir}\n")
    
    # Run audit
    results = audit_site(str(root_dir))
    
    # Generate reports
    generate_report(results, script_dir)
    
    # Print summary
    print("\n" + "="*50)
    print("AUDIT SUMMARY")
    print("="*50)
    print(f"Total files scanned: {results['total_files']}")
    print(f"Valid links: {results['valid_links']}")
    print(f"Valid assets: {results['valid_assets']}")
    print(f"Valid anchors: {results['valid_anchors']}")
    print(f"Broken links: {len(results['broken_links'])}")
    print(f"Broken assets: {len(results['broken_assets'])}")
    print(f"Broken anchors: {len(results['broken_anchors'])}")
    
    # Exit with error if any broken items found
    total_broken = len(results['broken_links']) + len(results['broken_assets']) + len(results['broken_anchors'])
    if total_broken > 0:
        print(f"\n❌ {total_broken} broken items found!")
        return 1
    else:
        print("\n✅ All links, assets, and anchors are valid!")
        return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())

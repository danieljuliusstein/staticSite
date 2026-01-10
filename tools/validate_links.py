#!/usr/bin/env python3
"""
Link and anchor validation script for static site
Checks all internal links and anchor references for broken links
"""

import os
import re
from pathlib import Path
from urllib.parse import urlparse, urljoin
from html.parser import HTMLParser
from collections import defaultdict

class LinkParser(HTMLParser):
    """Parse HTML to extract links and anchors"""
    
    def __init__(self):
        super().__init__()
        self.links = []
        self.anchors = set()
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        # Extract links from <a> tags
        if tag == 'a' and 'href' in attrs_dict:
            self.links.append(attrs_dict['href'])
        
        # Extract id attributes (potential anchor targets)
        if 'id' in attrs_dict:
            self.anchors.add(attrs_dict['id'])

def find_html_files(root_dir):
    """Find all HTML files in the directory"""
    html_files = []
    root_path = Path(root_dir)
    
    for file_path in root_path.rglob('*.html'):
        html_files.append(file_path)
    
    return html_files

def parse_html_file(file_path):
    """Parse an HTML file and extract links and anchors"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        parser = LinkParser()
        parser.feed(content)
        
        return parser.links, parser.anchors
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return [], set()

def check_internal_link(link, base_file, all_files, all_anchors):
    """Check if an internal link is valid"""
    # Skip external links
    if link.startswith(('http://', 'https://', 'mailto:', 'tel:')):
        return True, None
    
    # Skip empty or javascript links
    if not link or link.startswith('javascript:') or link == '#':
        return True, None
    
    # Parse the link
    parsed = urlparse(link)
    path = parsed.path
    fragment = parsed.fragment
    
    # Handle anchor-only links (e.g., #contact)
    if not path:
        if fragment:
            # Check if anchor exists in the current file
            base_file_str = str(base_file)
            if base_file_str in all_anchors and fragment in all_anchors[base_file_str]:
                return True, None
            else:
                return False, f"Anchor #{fragment} not found in {base_file}"
        return True, None
    
    # Normalize path (remove leading slash for comparison)
    if path.startswith('/'):
        path = path[1:]
    
    # Check if the file exists
    root_dir = Path(__file__).parent.parent
    target_file = root_dir / path
    
    # Handle directory paths (should have index.html)
    if target_file.is_dir():
        target_file = target_file / 'index.html'
    
    # Check if file exists
    if not target_file.exists():
        return False, f"File not found: {path}"
    
    # Check fragment if present
    if fragment:
        target_file_str = str(target_file)
        if target_file_str in all_anchors and fragment not in all_anchors[target_file_str]:
            return False, f"Anchor #{fragment} not found in {path}"
    
    return True, None

def main():
    """Main validation function"""
    print("=" * 80)
    print("INTERNAL LINK AND ANCHOR VALIDATION")
    print("=" * 80)
    print()
    
    # Get the root directory (parent of tools/)
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent
    
    print(f"Scanning directory: {root_dir}")
    print()
    
    # Find all HTML files
    html_files = find_html_files(root_dir)
    print(f"Found {len(html_files)} HTML files")
    print()
    
    # Parse all files and collect links and anchors
    all_links = defaultdict(list)
    all_anchors = {}
    
    for file_path in html_files:
        links, anchors = parse_html_file(file_path)
        all_links[str(file_path)] = links
        all_anchors[str(file_path)] = anchors
    
    # Validate all internal links
    broken_links = []
    total_links_checked = 0
    
    for file_path, links in all_links.items():
        for link in links:
            # Only check internal links
            if not link.startswith(('http://', 'https://', 'mailto:', 'tel:')):
                total_links_checked += 1
                is_valid, error = check_internal_link(
                    link, 
                    Path(file_path), 
                    html_files, 
                    all_anchors
                )
                
                if not is_valid:
                    rel_path = Path(file_path).relative_to(root_dir)
                    broken_links.append({
                        'file': str(rel_path),
                        'link': link,
                        'error': error
                    })
    
    # Report results
    print("RESULTS")
    print("-" * 80)
    print(f"Total HTML files scanned: {len(html_files)}")
    print(f"Total internal links checked: {total_links_checked}")
    print(f"Broken links found: {len(broken_links)}")
    print()
    
    if broken_links:
        print("BROKEN LINKS:")
        print("-" * 80)
        for item in broken_links:
            print(f"File: {item['file']}")
            print(f"Link: {item['link']}")
            print(f"Error: {item['error']}")
            print()
    else:
        print("✅ All internal links are valid!")
        print()
    
    # Summary of new blog articles
    print("NEW BLOG ARTICLES ADDED:")
    print("-" * 80)
    new_articles = [
        '/blog/build-backlinks-local-businesses.html',
        '/blog/anchor-text-dofollow-nofollow.html'
    ]
    
    for article in new_articles:
        article_path = root_dir / article[1:]  # Remove leading slash
        if article_path.exists():
            print(f"✅ {article}")
        else:
            print(f"❌ {article} (NOT FOUND)")
    print()
    
    return len(broken_links)

if __name__ == '__main__':
    exit_code = main()
    exit(exit_code)

#!/usr/bin/env python3
"""
Generate podcast cover art with Jaxon logo composite.
1. Generate base design with DALL-E 3
2. Overlay actual Jaxon logo using PIL
"""
import os
import sys
import json
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw
import subprocess

# Get API key
api_key = os.environ.get('OPENAI_API_KEY')
if not api_key:
    print("Error: OPENAI_API_KEY environment variable not set")
    sys.exit(1)

# Logo path
LOGO_PATH = Path('/Users/bgerby/Library/CloudStorage/OneDrive-Personal/Documents/_Jaxon Digital/logo/jaxon-logo-black.svg')

# Updated prompt - leave space for logo
prompt = """Create a professional podcast cover art background with the following specifications:

Title text: "RESEARCH FEED" (leave space at top for company logo)
Subtitle: "AI Strategy & Market Intelligence"

IMPORTANT: Leave a clean area at the TOP CENTER (about 20% of height) for a company logo to be added later.

Style: Modern, tech-forward, professional
Theme: Artificial Intelligence, business strategy, market research
Color palette: Deep blues, teals, and silver/white accents with gradient backgrounds
Mood: Authoritative, forward-thinking, intelligent

Design elements:
- Abstract tech/AI visual elements (neural networks, data flows, geometric patterns)
- Professional podcast aesthetic for business/tech audience
- Square format (1024x1024)
- Clean, modern layout with breathing room
- Gradient or abstract background that complements a logo at top

Layout:
- Top 20%: OPEN SPACE for logo (clean, possibly lighter background)
- Middle: "RESEARCH FEED" title text
- Lower: Subtitle and abstract tech elements

The design should be a sophisticated background that will complement a corporate logo."""

print("=" * 70)
print("JAXON RESEARCH FEED - PODCAST COVER WITH LOGO")
print("=" * 70)
print("\nStep 1: Generating base design with DALL-E 3...")
print("(This creates a background optimized for logo placement)")
print()

try:
    # Generate base image with DALL-E 3
    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "dall-e-3",
        "prompt": prompt,
        "size": "1024x1024",
        "quality": "hd",
        "n": 1
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers=headers,
        method='POST'
    )

    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))

    image_url = result['data'][0]['url']
    print("✓ Base design generated!")

    # Download base image
    base_path = Path(__file__).parent / "cover-base.png"
    urllib.request.urlretrieve(image_url, base_path)
    print(f"✓ Base image saved: {base_path}")

    print("\nStep 2: Converting SVG logo to PNG...")

    # Convert SVG to PNG using cairosvg
    logo_png = Path(__file__).parent / "jaxon-logo.png"

    try:
        import cairosvg
        cairosvg.svg2png(
            url=str(LOGO_PATH),
            write_to=str(logo_png),
            output_width=500,
            output_height=150
        )
        print("✓ Logo converted with cairosvg")
    except Exception as e:
        print(f"⚠️  Could not convert SVG: {e}")
        print("Will use text-only design")
        logo_png = None

    if logo_png and logo_png.exists():
        print("\nStep 3: Compositing logo onto cover art...")

        # Open images
        base = Image.open(base_path).convert('RGBA')
        logo = Image.open(logo_png).convert('RGBA')

        # Calculate logo position (centered at top, with some padding)
        logo_x = (base.width - logo.width) // 2
        logo_y = 60  # 60px from top

        # Composite logo onto base
        base.paste(logo, (logo_x, logo_y), logo)

        # Save final result
        output_path = Path(__file__).parent / "cover-art.png"
        base.save(output_path, 'PNG')

        print(f"✓ Final cover art saved: {output_path}")
        print(f"  File size: {output_path.stat().st_size / 1024:.1f} KB")
    else:
        print("\n⚠️  Skipping logo composite (conversion failed)")
        print(f"Using base design only: {base_path}")

    print("\n" + "=" * 70)
    print("NEXT STEPS:")
    print("=" * 70)
    print("1. Review the generated cover art")
    print("2. If satisfied, upload to Google Drive")
    print("3. Update RSS feed with cover image URL")
    print("4. Commit and push to GitHub Pages")

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

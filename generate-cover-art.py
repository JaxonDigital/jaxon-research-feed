#!/usr/bin/env python3
"""
Generate podcast cover art using DALL-E 3.
Creates professional cover image for Jaxon Research Feed podcast.
"""
import os
import sys
import json
import urllib.request
from pathlib import Path

# Get API key
api_key = os.environ.get('OPENAI_API_KEY')
if not api_key:
    print("Error: OPENAI_API_KEY environment variable not set")
    sys.exit(1)

# Prompt for podcast cover art
prompt = """Create a professional podcast cover art for "Jaxon Research Feed" with subtitle "AI Strategy & Market Intelligence".

Design specifications:
- Modern, sophisticated business aesthetic with tech elements
- Color palette: Deep navy blue, bright teal/cyan accents, white/silver highlights
- Typography: Clean, professional sans-serif fonts - make text HIGHLY READABLE
- Square 1024x1024 format for podcast apps

Visual composition:
- Title "Jaxon Research Feed" should be prominent and crystal clear
- Subtitle "AI Strategy & Market Intelligence" in smaller text
- Abstract background: flowing data streams, neural network patterns, or geometric tech elements
- Gradient backgrounds work well (navy to teal)
- Professional, not overly busy - leave breathing room

Style references: Think high-end tech conference branding, enterprise software marketing, or prestigious business podcast covers like "Masters of Scale" or "a16z Podcast".

The overall aesthetic should convey: Authority, innovation, strategic intelligence, and cutting-edge AI insights for business leaders."""

print("=" * 60)
print("JAXON RESEARCH FEED - PODCAST COVER ART GENERATOR")
print("=" * 60)
print(f"\nPrompt:\n{prompt}\n")
print("Generating image with DALL-E 3...")
print("This may take 10-15 seconds...\n")

try:
    # Prepare API request
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

    # Make API request
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers=headers,
        method='POST'
    )

    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))

    image_url = result['data'][0]['url']
    revised_prompt = result['data'][0].get('revised_prompt', 'N/A')

    print("✓ Image generated successfully!")
    print(f"\nImage URL:\n{image_url}")
    print(f"\nRevised prompt:\n{revised_prompt}")

    # Download and save the image
    output_path = Path(__file__).parent / "cover-art.png"
    print(f"\nDownloading image to: {output_path}")

    urllib.request.urlretrieve(image_url, output_path)

    print(f"✓ Image saved: {output_path}")
    print(f"  File size: {output_path.stat().st_size / 1024:.1f} KB")

    print("\n" + "=" * 60)
    print("NEXT STEPS:")
    print("=" * 60)
    print("1. Review the generated image")
    print("2. If satisfied, upload to Google Drive")
    print("3. Update RSS feed with cover image URL")
    print("4. Commit and push to GitHub Pages")
    print("\nTo regenerate with different prompt, edit this script and run again.")

except urllib.error.HTTPError as e:
    error_body = e.read().decode('utf-8')
    print(f"✗ HTTP Error {e.code}: {error_body}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error generating image: {e}")
    sys.exit(1)

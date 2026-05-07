#!/usr/bin/env python3
"""
RideResQ GEO Page Generator

Usage:
    python generate.py san-antonio    # Generate pages for San Antonio
    python generate.py --all          # Generate all cities
    python generate.py --list         # List available cities
"""

import yaml
import os
import sys
from pathlib import Path
from datetime import date

SCRIPT_DIR = Path(__file__).parent
CITIES_DIR = SCRIPT_DIR / "cities"
TEMPLATES_DIR = SCRIPT_DIR / "templates"
OUTPUT_DIR = SCRIPT_DIR.parent / "docs"


def load_city(city_slug: str) -> dict:
    """Load city config from YAML."""
    yaml_path = CITIES_DIR / f"{city_slug}.yaml"
    if not yaml_path.exists():
        raise FileNotFoundError(f"City config not found: {yaml_path}")
    
    with open(yaml_path) as f:
        return yaml.safe_load(f)


def format_areas(areas: dict, style: str = "list") -> str:
    """Format areas dict into HTML list."""
    lines = []
    
    area_labels = {
        "central": "Central",
        "west": "West",
        "east": "East", 
        "north": "North",
        "south": "South",
        "far_south": "Far South",
        "tech_center": "Tech Center",
        "suburbs": "Suburbs",
        "highways": "Highways",
        "airport": "Airport",
    }
    
    for key, locations in areas.items():
        label = area_labels.get(key, key.replace("_", " ").title())
        locations_str = ", ".join(locations)
        lines.append(f'            <li><strong>{label}:</strong> {locations_str}</li>')
    
    return "\n".join(lines)


def format_phone(phone: str) -> str:
    """Format phone for display."""
    # Remove +1 prefix and format
    clean = phone.replace("+1-", "").replace("+1", "").replace("-", "")
    if len(clean) == 10:
        return f"({clean[:3]}) {clean[3:6]}-{clean[6:]}"
    return phone


def generate_towing_page(city: dict) -> str:
    """Generate towing page HTML."""
    c = city
    city_lower = c['city'].lower().replace(" ", "-")
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cheap Towing in {c['city']} | No Surge Pricing | RideResQ</title>
    <meta name="description" content="Need a tow in {c['city']}? RideResQ finds you local towing at ${c['pricing']['tow_min']}-${c['pricing']['tow_max']} — no surge pricing. AI-powered dispatch connects you to vetted tow trucks in {c['eta_min']}-{c['eta_max']} minutes.">
    <link rel="canonical" href="https://rideresq.com/towing-{city_lower}/">
    
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": "Towing Service",
        "provider": {{ "@type": "Organization", "name": "RideResQ" }},
        "areaServed": {{ "@type": "Place", "name": "{c['metro']}, {c['state']}" }},
        "description": "Affordable towing in {c['city']} without surge pricing. AI finds local tow trucks at ${c['pricing']['tow_min']}-${c['pricing']['tow_max']}.",
        "offers": {{ "@type": "Offer", "priceRange": "${c['pricing']['tow_min']}-${c['pricing']['tow_max']}", "priceCurrency": "USD" }}
    }}
    </script>
    
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {{
                "@type": "Question",
                "name": "How much does a tow cost in {c['city']}?",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "Through RideResQ, local towing in {c['city']} costs ${c['pricing']['tow_min']}-${c['pricing']['tow_max']}. Traditional services often charge ${c['pricing']['tow_surge']}+ during surge periods."
                }}
            }},
            {{
                "@type": "Question",
                "name": "How fast can a tow truck get to me in {c['city']}?",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "RideResQ connects you with local tow trucks in the {c['metro']} with an average response time of {c['eta_min']}-{c['eta_max']} minutes."
                }}
            }},
            {{
                "@type": "Question",
                "name": "Does RideResQ charge surge pricing for towing?",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "No. RideResQ never charges surge pricing. We connect you directly with local tow companies at their standard rates."
                }}
            }}
        ]
    }}
    </script>
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --asphalt: #0d0d0f;
            --concrete: #1a1a1e;
            --steel: #2a2a32;
            --amber: #ffb800;
            --headlight: #f0f0f0;
            --fog: #888894;
            --success: #34c759;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'IBM Plex Mono', monospace;
            background: var(--asphalt);
            color: var(--headlight);
            line-height: 1.7;
        }}
        .container {{ max-width: 700px; margin: 0 auto; padding: 2rem 1.5rem; }}
        .logo {{
            font-family: 'Archivo Black', sans-serif;
            font-size: 1.5rem;
            text-decoration: none;
            color: var(--headlight);
        }}
        .logo span {{ color: var(--amber); }}
        header {{
            border-bottom: 1px solid var(--steel);
            padding-bottom: 1rem;
            margin-bottom: 2rem;
        }}
        h1 {{
            font-family: 'Archivo Black', sans-serif;
            font-size: 2rem;
            margin-bottom: 1rem;
            line-height: 1.2;
        }}
        h2 {{
            font-family: 'Archivo Black', sans-serif;
            font-size: 1.3rem;
            color: var(--amber);
            margin: 2rem 0 1rem;
        }}
        p {{ color: var(--fog); margin-bottom: 1rem; }}
        strong {{ color: var(--headlight); }}
        ul, ol {{ color: var(--fog); padding-left: 1.5rem; margin-bottom: 1rem; }}
        li {{ margin-bottom: 0.5rem; }}
        .price-card {{
            background: var(--concrete);
            border: 2px solid var(--amber);
            padding: 1.5rem;
            margin: 2rem 0;
            text-align: center;
        }}
        .price-card .label {{
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: var(--fog);
        }}
        .price-card .price {{
            font-family: 'Archivo Black', sans-serif;
            font-size: 2.5rem;
            color: var(--amber);
        }}
        .price-card .compare {{
            font-size: 0.85rem;
            color: var(--success);
        }}
        .cta {{
            display: block;
            background: var(--amber);
            color: var(--asphalt);
            font-family: 'Archivo Black', sans-serif;
            font-size: 1.2rem;
            padding: 1.25rem 2rem;
            text-decoration: none;
            text-align: center;
            margin: 2rem 0;
        }}
        .cta:hover {{ background: var(--headlight); }}
        .faq {{ margin: 2rem 0; }}
        .faq-item {{
            background: var(--concrete);
            border-left: 3px solid var(--amber);
            padding: 1rem;
            margin-bottom: 1rem;
        }}
        .faq-item h3 {{
            font-family: 'Archivo Black', sans-serif;
            font-size: 1rem;
            margin-bottom: 0.5rem;
        }}
        .faq-item p {{ margin-bottom: 0; }}
        footer {{
            border-top: 1px solid var(--steel);
            padding-top: 2rem;
            margin-top: 3rem;
            text-align: center;
        }}
        footer p {{ font-size: 0.8rem; }}
        footer a {{ color: var(--amber); }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <a href="/" class="logo">Ride<span>ResQ</span></a>
        </header>
        
        <h1>🚛 Cheap Towing in {c['city']} — No Surge Pricing</h1>
        
        <p>Need a tow truck in {c['city']}? <strong>RideResQ connects you with local towing services at fair prices</strong> — no surge fees, no membership required. Our AI finds available tow trucks near you and shows you the price upfront.</p>
        
        <div class="price-card">
            <div class="label">Local Towing in {c['city']}</div>
            <div class="price">${c['pricing']['tow_min']}–${c['pricing']['tow_max']}</div>
            <div class="compare">vs ${c['pricing']['tow_surge']}+ surge pricing elsewhere</div>
        </div>
        
        <a href="/" class="cta">📍 Get a Tow Now</a>
        
        <h2>How Much Does Towing Cost in {c['city']}?</h2>
        <p>The average cost of a local tow in {c['city']} ranges from <strong>${c['pricing']['tow_min']} to ${c['pricing']['tow_max']}</strong> through RideResQ. Traditional roadside services often charge ${c['pricing']['tow_surge']} or more during peak hours. Here's what affects your towing cost:</p>
        <ul>
            <li><strong>Distance:</strong> Most local tows (under 10 miles) are ${c['pricing']['tow_min']}-${c['pricing']['tow_max']}</li>
            <li><strong>Time of day:</strong> Some services add night/weekend fees — RideResQ doesn't</li>
            <li><strong>Vehicle type:</strong> Motorcycles, SUVs, and trucks may have different rates</li>
            <li><strong>Special equipment:</strong> Flatbed towing for AWD/luxury vehicles may cost more</li>
        </ul>
        
        <h2>Average Tow Truck Response Time in {c['city']}</h2>
        <p>RideResQ connects you with local tow trucks in <strong>{c['eta_min']}-{c['eta_max']} minutes</strong> on average. Response times depend on your location, traffic, and provider availability.</p>
        
        <h2>{c['city']} Areas We Serve</h2>
        <p>RideResQ provides towing throughout the {c['metro']}:</p>
        <ul>
{format_areas(c['areas'])}
        </ul>
        
        <h2>Why RideResQ for Towing?</h2>
        <ul>
            <li><strong>No surge pricing</strong> — Same fair rates any time of day</li>
            <li><strong>No membership fees</strong> — Pay only when you need help</li>
            <li><strong>Transparent pricing</strong> — Know the cost before you commit</li>
            <li><strong>Local providers</strong> — Vetted {c['city']}-area tow companies</li>
            <li><strong>Fast response</strong> — {c['eta_min']}-{c['eta_max']} minute average arrival</li>
        </ul>
        
        <a href="/" class="cta">📍 Get a Tow Now</a>
        
        <div class="faq">
            <h2>Frequently Asked Questions</h2>
            
            <div class="faq-item">
                <h3>How much does a tow cost in {c['city']}?</h3>
                <p>Through RideResQ, local towing in {c['city']} costs ${c['pricing']['tow_min']}-${c['pricing']['tow_max']}. Traditional services often charge ${c['pricing']['tow_surge']}+ during surge periods.</p>
            </div>
            
            <div class="faq-item">
                <h3>How fast can a tow truck get to me in {c['city']}?</h3>
                <p>RideResQ connects you with local tow trucks in the {c['metro']} with an average response time of {c['eta_min']}-{c['eta_max']} minutes.</p>
            </div>
            
            <div class="faq-item">
                <h3>Does RideResQ charge surge pricing for towing?</h3>
                <p>No. RideResQ never charges surge pricing. We connect you directly with local tow companies at their standard rates.</p>
            </div>
            
            <div class="faq-item">
                <h3>Do I need a membership like AAA?</h3>
                <p>No membership required. Unlike AAA, you only pay when you need a tow. No annual fees.</p>
            </div>
        </div>
        
        <footer>
            <p><a href="/">← Back to RideResQ</a></p>
            <p>RideResQ — AI-powered towing in {c['city']}. No surge pricing.</p>
            <p>© {date.today().year} RideResQ. {c['city']}, {c['state']}.</p>
        </footer>
    </div>
</body>
</html>
'''


def generate_service_pages(city_slug: str, dry_run: bool = False):
    """Generate all service pages for a city."""
    city = load_city(city_slug)
    city_lower = city['city'].lower().replace(" ", "-")
    
    pages = [
        (f"towing-{city_lower}", generate_towing_page(city)),
        # Add more: jump-start, lockout, flat-tire, roadside-assistance
    ]
    
    for page_slug, html in pages:
        output_path = OUTPUT_DIR / page_slug / "index.html"
        
        if dry_run:
            print(f"Would create: {output_path}")
        else:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                f.write(html)
            print(f"Created: {output_path}")
    
    print(f"\n✅ Generated {len(pages)} pages for {city['city']}")
    print(f"Don't forget to update sitemap.xml!")


def list_cities():
    """List all available city configs."""
    print("Available cities:")
    for yaml_file in CITIES_DIR.glob("*.yaml"):
        city = load_city(yaml_file.stem)
        print(f"  - {yaml_file.stem}: {city['city']}, {city['state']}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    cmd = sys.argv[1]
    
    if cmd == "--list":
        list_cities()
    elif cmd == "--all":
        for yaml_file in CITIES_DIR.glob("*.yaml"):
            if yaml_file.stem != "denver":  # Skip Denver, already manually created
                generate_service_pages(yaml_file.stem)
    else:
        generate_service_pages(cmd)


if __name__ == "__main__":
    main()

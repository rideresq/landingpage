# RideResQ GEO Page Generator

Generate SEO/GEO optimized landing pages for new cities.

## Quick Start

```bash
# List available cities
python generate.py --list

# Generate pages for San Antonio
python generate.py san-antonio

# Generate all cities (except Denver which is manual)
python generate.py --all
```

## Adding a New City

1. Create a config file: `cities/your-city.yaml`
2. Copy from `cities/san-antonio.yaml` as a template
3. Update:
   - City name, state, metro area
   - Phone number (when you have one)
   - Pricing (research local market)
   - Service areas (neighborhoods, highways)
4. Run: `python generate.py your-city`
5. Update `docs/sitemap.xml` with new pages
6. Commit and push

## City Config Fields

| Field | Description |
|-------|-------------|
| `city` | City name (e.g., "San Antonio") |
| `state` | Full state name |
| `state_abbr` | Two-letter state code |
| `metro` | Metro area name for copy |
| `phone` | Local phone number |
| `pricing.*` | Price ranges for each service |
| `eta_min/max` | Response time range in minutes |
| `areas.*` | Service areas by region |
| `local_context` | Optional local flavor for content |

## Generated Pages

For each city, generates:
- `/towing-{city}/`
- `/jump-start-{city}/` (TODO)
- `/lockout-{city}/` (TODO)
- `/flat-tire-{city}/` (TODO)
- `/roadside-assistance-{city}/` (TODO)

## After Generating

1. Review the generated HTML
2. Add pages to `sitemap.xml`
3. Push to GitHub
4. Submit new URLs to Google Search Console

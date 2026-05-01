# RideResQ Landing Page

Marketing website for RideResQ — AI-powered dispatch for tow operators and repair shops.

🌐 **Live:** [rideresq.com](https://rideresq.com)

## Overview

This repo contains the public-facing marketing site:
- **Customer page** (`/`) — For stranded drivers needing help
- **Business page** (`/business`) — For tow operators and repair shops to sign up

## Structure

```
docs/                    # GitHub Pages root
├── index.html           # Customer landing page
└── business/
    └── index.html       # B2B sales page
schema.sql               # Database schema (reference)
```

## Deployment

Hosted via **GitHub Pages** from the `docs/` folder on `main` branch.

Any push to `main` automatically deploys.

### DNS Setup

Point `rideresq.com` to GitHub Pages:
- A record: `185.199.108.153` (and .109, .110, .111)
- Or CNAME: `rideresq.github.io`

## Design

**Aesthetic:** Industrial roadside — dark asphalt tones, amber warning colors, hazard stripes

**Fonts:**
- Archivo Black (headlines)
- IBM Plex Mono (body)

**Key colors:**
- `--asphalt: #0d0d0f`
- `--amber: #ffb800`
- `--headlight: #f0f0f0`

## Business Model

**Outcome-as-a-Service** — Providers pay only when they complete a job. No monthly fees, no setup fees.

**Target customers:**
- Tow truck operators
- Auto repair shops
- Roadside assistance providers

**Market:** Denver metro (initial), expanding to surrounding areas

## Contact

Business line: **(720) 650-0250**

## Related Repos

| Repo | Description | Access |
|------|-------------|--------|
| `rideresq/app` | Provider mobile app (PWA + Capacitor) | Private |
| `rideresq/providers` | Prospect lists and provider data | Private |
| `rideresq/api` | FastAPI backend (coming soon) | Private |

## License

Proprietary. All rights reserved.

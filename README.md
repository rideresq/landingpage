# RideResQ Landing Page

Marketing website for RideResQ — AI-powered roadside assistance marketplace.

🌐 **Live:** [rideresq.com](https://rideresq.com)

## Overview

This repo contains the public-facing marketing site:
- **Consumer page** (`/`) — For stranded drivers needing help
- **Business page** (`/business`) — For tow operators and repair shops to partner

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   THIS SITE     │────►│   BACKEND API   │◄────│  ELEVENLABS     │
│   rideresq.com  │     │ api.rideresq.com│     │  Voice Agent    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

**Consumer flow:**
1. User lands on site → shares GPS location
2. Site POSTs to `api.rideresq.com/api/sessions/create`
3. User calls (720) 650-0250
4. ElevenLabs agent handles call, dispatches help

## Structure

```
docs/                        # GitHub Pages root
├── index.html               # Consumer landing (GPS capture + call CTA)
├── business/
│   └── index.html           # B2B partner signup page
elevenlabs/
├── agent-config.json        # Voice agent configuration
├── README.md                # Agent documentation
├── LOCATION-FLOW.md         # Location capture flow docs
```

## Key Features

**Consumer page:**
- GPS location capture on first tap
- "AI finds you the best price" messaging
- Trust badges (Local shops, Fair pricing, No hidden fees)
- Live estimate card with price comparison
- Emergency Mode banner after location confirmed

**Business page:**
- "We Send You Jobs. AI Handles the Rest."
- Visual flow diagram (Driver → RideResQ AI → Your Business)
- Clear pricing: 10-15% per completed job
- AI profit messaging (+$500/mo saved jobs, 2+ hrs/day saved)

## Deployment

Hosted via **GitHub Pages** from the `docs/` folder on `main` branch.

Push to `main` → automatically deploys.

## Related Repos

| Repo | Purpose |
|------|---------|
| [rideresq/backend](https://github.com/rideresq/backend) | FastAPI + Postgres (api.rideresq.com) |
| [rideresq/app](https://github.com/rideresq/app) | Provider PWA + mobile app (private) |
| [rideresq/providers](https://github.com/rideresq/providers) | Prospect lists (private) |

## Contact

- **Phone:** (720) 650-0250
- **Domain:** rideresq.com
- **API:** api.rideresq.com

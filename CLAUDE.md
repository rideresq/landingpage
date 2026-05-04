# CLAUDE.md — Landing Page Repo

## What This Is

Public marketing site for RideResQ — AI-powered roadside assistance marketplace.

Two pages:
1. **Consumer** (`/`) — Stranded drivers share location, then call for help
2. **Business** (`/business`) — Tow/repair shops sign up as partners

## Architecture

```
User visits rideresq.com
        │
        ▼
   Shares GPS location
        │
        ▼
POST api.rideresq.com/api/sessions/create  ←── THIS SITE DOES THIS
        │
        ▼
   User calls (720) 650-0250
        │
        ▼
   ElevenLabs voice agent handles call
```

## Quick Commands

```bash
# Preview locally
cd docs && python3 -m http.server 8000

# Deploy (automatic on push)
git push origin main
```

## Key Files

| File | Purpose |
|------|---------|
| `docs/index.html` | Consumer landing (GPS capture + call CTA) |
| `docs/business/index.html` | B2B partner signup page |
| `elevenlabs/agent-config.json` | Voice agent configuration |
| `elevenlabs/README.md` | Agent documentation |

## Backend Integration

The site POSTs to `api.rideresq.com` when user shares location:

```javascript
// In docs/index.html → storeLocation()
fetch('https://api.rideresq.com/api/sessions/create', {
    method: 'POST',
    body: JSON.stringify({
        latitude: data.lat,
        longitude: data.lng,
        address: data.address,
        location_source: 'gps'
    })
});
```

Session ID stored in `localStorage` for later use.

## Design System

**DO NOT** deviate from the established aesthetic.

**Fonts:**
- `Archivo Black` — Headlines only
- `IBM Plex Mono` — Everything else

**Colors:**
```css
--asphalt: #0d0d0f      /* Background */
--concrete: #1a1a1e     /* Cards */
--steel: #2a2a32        /* Borders */
--amber: #ffb800        /* Primary accent */
--headlight: #f0f0f0    /* Text */
--fog: #888894          /* Secondary text */
--success: #34c759      /* Positive */
--danger: #ff3b30       /* Negative */
```

**Visual elements:**
- Hazard stripes (black/amber repeating gradient)
- Angled clip-path buttons
- Grid overlay on backgrounds

## Phone Number

**(720) 650-0250** — ElevenLabs voice agent

If updating, change in BOTH pages. Search for `720`.

## Pricing Model (for /business page)

**Outcome-as-a-Service:**
- $0 setup, $0 monthly
- 10-15% per completed job
- If customer cancels, provider pays nothing

## Deploy

Push to `main` → GitHub Pages auto-deploys.

```bash
GIT_SSH_COMMAND="ssh -i ~/.rideresq-keys/landing_key_v3 -o IdentitiesOnly=yes" git push origin main
```

## Related Repos

| Repo | Purpose |
|------|---------|
| `rideresq/backend` | FastAPI + Postgres (api.rideresq.com) |
| `rideresq/app` | Provider PWA + mobile app |
| `rideresq/providers` | Prospect lists (private) |

## Don't

- Don't commit API keys or secrets
- Don't change the visual aesthetic without discussion
- Don't use generic fonts (Inter, Roboto)
- Don't break the hazard stripe motif

# CLAUDE.md — Landing Page Repo

## What This Is

The public marketing site for RideResQ. Two pages:
1. Customer-facing (`/`) — stranded drivers text/call for help
2. Business-facing (`/business`) — tow/repair shops sign up

## Quick Commands

```bash
# Preview locally
cd docs && python3 -m http.server 8000

# Deploy (automatic on push)
git push origin main
```

## Key Files

- `docs/index.html` — Customer landing page
- `docs/business/index.html` — B2B sales/signup page
- `schema.sql` — Database schema (for reference, actual DB is in API repo)

## Design System

Follow the existing aesthetic. Do NOT use generic fonts or purple gradients.

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
- Staggered fade-up animations on load

## Phone Number

Business line: `(720) 650-0250`

If updating, change in BOTH:
- `docs/index.html`
- `docs/business/index.html`

Search for `720` to find all instances.

## Pricing Model

**Outcome-as-a-Service:**
- $0 setup
- $0 monthly
- Small % per completed job
- If customer no-shows or cancels, provider pays nothing

## Deploy Keys

Deploy key is stored locally, not in repo. If you need to push:
```bash
GIT_SSH_COMMAND="ssh -i ./landingpage_deploy_key -o IdentitiesOnly=yes" git push origin main
```

## Related Repos

- `rideresq/app` — Provider mobile app
- `rideresq/providers` — Prospect data
- `rideresq/api` — Backend (coming soon)

## Don't

- Don't commit API keys or secrets
- Don't change the visual aesthetic without discussion
- Don't remove the hazard stripe motif — it's the brand identity

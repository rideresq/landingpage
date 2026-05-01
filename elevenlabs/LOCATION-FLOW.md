# Location Capture Integration

## Overview

Instead of asking callers to describe their location verbally, we send them a link that captures their GPS coordinates automatically.

## Flow

### Consumer (Stranded Driver)

1. Agent identifies caller needs help
2. Agent: "I'm going to text you a link. Tap it to share your exact location so I can send help fast."
3. Send SMS: `https://rideresq.com/locate?t=c&s={{session_id}}`
4. User taps link → page requests GPS → shows address → user confirms
5. Backend receives location with session_id
6. Agent receives webhook notification with location
7. Agent: "Got it, you're at [address]. I'm dispatching help now."

### Provider (Business Location)

1. Agent identifies caller is a provider
2. Agent: "Let me get your business location. I'll text you a quick link."
3. Send SMS: `https://rideresq.com/locate?t=p&s={{session_id}}`
4. User taps link → page requests GPS → shows address → user confirms
5. Backend receives location with session_id
6. Agent: "Got it, I see you're based in [area]. Let me tell you how RideResQ works..."

## URL Parameters

| Param | Full | Description |
|-------|------|-------------|
| `t` | `type` | `c` or `consumer` / `p` or `provider` |
| `s` | `session` | Call session ID for webhook correlation |

## SMS Templates

**Consumer:**
```
RideResQ here! Tap to share your location so we can send help fast: https://rideresq.com/locate?t=c&s={{session_id}}
```

**Provider:**
```
RideResQ here! Tap to share your business location: https://rideresq.com/locate?t=p&s={{session_id}}
```

## Backend Webhook

When user submits location, POST to `/api/location/submit`:

```json
{
  "lat": 39.7392,
  "lng": -104.9903,
  "accuracy": 15,
  "address": "123 Main St, Denver, CO",
  "source": "gps",
  "caller_type": "consumer",
  "session_id": "call_abc123",
  "timestamp": "2026-05-01T22:00:00Z"
}
```

Backend should:
1. Store location data
2. Notify ElevenLabs agent via webhook (or poll endpoint)
3. Agent can then reference location in conversation

## Fallback

If user can't/won't use the link:
- Agent falls back to verbal collection
- "No problem, just tell me the nearest intersection or business you can see."

## Privacy Note

- GPS coordinates are only used for dispatch
- Location data retained for job record only
- Nominatim (OpenStreetMap) used for geocoding — no Google dependency

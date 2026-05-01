# RideResQ ElevenLabs Voice Agent

AI voice agent for handling inbound and outbound calls for RideResQ.

## Overview

This agent handles two types of callers:

1. **Consumers** — People who need roadside help (tow, jump start, flat tire, lockout)
2. **Providers** — Tow truck operators and repair shops wanting to partner with RideResQ

## Phone Number

**Inbound:** (720) 650-0250 — Routes to this agent via Twilio

## Call Flows

### Consumer Flow

```
Caller → Identify Problem → Get Location → Get Vehicle Info → Dispatch → Confirm → End
```

1. Greet and ask what's wrong
2. Collect location (address or cross streets)
3. Collect vehicle info (year, make, model)
4. Dispatch job to available providers via API
5. Confirm help is on the way, send tracking text
6. End call

### Provider Flow

```
Caller → Collect Business Info → Explain Model → Interest Check → Send Signup Link → End
                                       ↓
                                  Answer Questions
```

1. Greet and collect business name + type
2. Explain the outcome-based model (pay per completed job)
3. Answer any questions about fees, payment, etc.
4. If interested, send signup link via SMS
5. End call

## Configuration

### Required Environment Variables

Set these in ElevenLabs or replace in the config:

| Variable | Description |
|----------|-------------|
| `{{RIDERESQ_API_URL}}` | Backend API URL (e.g., `https://api.rideresq.com`) |
| `{{RIDERESQ_API_KEY}}` | API key for dispatch_job webhook |
| `{{TWILIO_CONNECTION_ID}}` | ElevenLabs Twilio integration connection ID |
| `{{POST_CALL_WEBHOOK_ID}}` | Webhook ID for post-call transcript delivery |

### Tools

| Tool | Purpose |
|------|---------|
| `dispatch_job` | Create roadside job and notify providers |
| `register_provider_interest` | Log provider interest for follow-up |
| `twilio_send_message` | Send SMS (tracking link, signup link) |
| `end_call` | End the call |
| `language_detection` | Detect Spanish and switch |
| `voicemail_detection` | Leave voicemail if no answer |

## Voice Settings

- **Voice:** Default ElevenLabs voice (can customize)
- **Model:** eleven_flash_v2 (low latency)
- **Speed:** 1.05x
- **Languages:** English (primary), Spanish (auto-detected)

## Workflow Nodes

### Consumer Path
- `node_caller_router` — Initial routing
- `node_consumer_intake` — Identify the problem
- `node_get_location` — Collect location
- `node_get_vehicle` — Collect vehicle info
- `node_dispatch` — Create job, dispatch provider
- `node_consumer_confirm` — Confirm and close

### Provider Path
- `node_provider_onboard` — Collect business info
- `node_provider_explain` — Explain business model
- `node_provider_questions` — Answer FAQ
- `node_provider_interested` — Send signup link
- `node_provider_notinterested` — Handle decline gracefully

## Testing

1. Import `agent-config.json` into ElevenLabs
2. Connect Twilio integration
3. Test inbound call flow
4. Test outbound call flow (for callbacks)

## Deployment

1. Create agent in ElevenLabs dashboard
2. Import this config
3. Connect to Twilio phone number (720) 650-0250
4. Set up post-call webhook for transcripts
5. Configure backend API endpoints

## API Endpoints Needed

The agent calls these backend endpoints:

### POST /api/jobs/dispatch
Create and dispatch a new job.

```json
{
  "caller_phone": "+17205551234",
  "caller_name": "John",
  "issue_type": "tow",
  "vehicle_year": "2019",
  "vehicle_make": "Honda",
  "vehicle_model": "Accord",
  "location": "123 Main St, Denver CO",
  "notes": "Car won't start"
}
```

### POST /api/providers/register-interest
Log provider interest for follow-up.

```json
{
  "business_name": "Denver Towing Co",
  "business_type": "tow",
  "phone": "+17205559999",
  "service_areas": "Denver, Aurora, Lakewood",
  "contact_name": "Mike"
}
```

## Costs

ElevenLabs pricing applies:
- Per-minute voice cost
- LLM cost (GPT-4o)
- Twilio SMS/voice costs separate

Estimate: ~$0.10-0.15 per minute of conversation.

-- RideResQ Database Schema
-- PostgreSQL

-- Clients (tow operators, repair shops)
CREATE TABLE clients (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            VARCHAR(255) NOT NULL,
    business_type   VARCHAR(50) NOT NULL CHECK (business_type IN ('tow', 'repair', 'both')),
    phone           VARCHAR(20) NOT NULL,
    twilio_number   VARCHAR(20) NOT NULL UNIQUE,
    email           VARCHAR(255),
    address         TEXT,
    timezone        VARCHAR(50) DEFAULT 'America/Denver',
    sms_template    TEXT DEFAULT 'Hey! Sorry we missed you. What''s going on with your car?',
    active          BOOLEAN DEFAULT true,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Conversations between clients and their customers
CREATE TABLE conversations (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id       UUID NOT NULL REFERENCES clients(id),
    customer_phone  VARCHAR(20) NOT NULL,
    status          VARCHAR(20) DEFAULT 'open' CHECK (status IN ('open', 'closed', 'converted')),
    started_at      TIMESTAMPTZ DEFAULT NOW(),
    ended_at        TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    
    -- One active conversation per client-customer pair
    UNIQUE (client_id, customer_phone, status)
);

-- Individual messages within conversations
CREATE TABLE messages (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id),
    direction       VARCHAR(10) NOT NULL CHECK (direction IN ('inbound', 'outbound')),
    channel         VARCHAR(10) NOT NULL CHECK (channel IN ('sms', 'call', 'voicemail')),
    body            TEXT,
    duration_secs   INTEGER,  -- For calls
    recording_url   TEXT,     -- For voicemails
    twilio_sid      VARCHAR(50),
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Track missed calls that triggered the workflow
CREATE TABLE missed_calls (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id       UUID NOT NULL REFERENCES clients(id),
    conversation_id UUID REFERENCES conversations(id),
    caller_phone    VARCHAR(20) NOT NULL,
    call_sid        VARCHAR(50),
    texted_back     BOOLEAN DEFAULT false,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_conversations_client ON conversations(client_id);
CREATE INDEX idx_conversations_customer ON conversations(customer_phone);
CREATE INDEX idx_conversations_status ON conversations(status);
CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_messages_created ON messages(created_at);
CREATE INDEX idx_missed_calls_client ON missed_calls(client_id);
CREATE INDEX idx_missed_calls_created ON missed_calls(created_at);

-- Updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER clients_updated_at
    BEFORE UPDATE ON clients
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER conversations_updated_at
    BEFORE UPDATE ON conversations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER messages_updated_at
    BEFORE UPDATE ON messages
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

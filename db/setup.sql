DROP DATABASE nc_plus_one;
CREATE DATABASE nc_plus_one;

-- CREATE TABLE users (
--     user_id SERIAL PRIMARY KEY,
--     email VARCHAR(255) UNIQUE NOT NULL,
--     password VARCHAR(255) NOT NULL,
--     name VARCHAR(255) NOT NULL,
--     created_at TIMESTAMPTZ DEFAULT NOW
-- );

-- CREATE TABLE venues(
--     venue_id SERIAL PRIMARY KEY,
--     name VARCHAR(255) NOT NULL,
--     address TEXT,
--     capacity INTEGER
-- );

-- CREATE TABLE rsvps (
--     rsvp_id SERIAL PRIMARY KEY,
--     attendee_id INTEGER REFERENCES users(user_id),
--     event_id INTEGER REFERENCES venues(venue_id),
--     created_at TIMESTAMPTZ DEFAULT NOW
-- );

-- CREATE TABLE events (
--     event_id SERIAL PRIMARY KEY,
--     title VARCHAR(255) NOT NULL,
--     description VARCHAR(255),
--     starts_at TIMESTAMPTZ NOT NULL,
--     ends_at TIMESTAMPTZ NOT NULL,
--     organiser_id INTEGER REFERENCES users(user_id),
--     venue_id INTEGER REFERENCES venues(venue_id),
--     created_at TIMESTAMPTZ DEFAULT NOW
-- );
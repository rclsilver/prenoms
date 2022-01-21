---
--- uuid extension
---
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

---
--- user table
---
CREATE TABLE IF NOT EXISTS "user" (
    id UUID PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    username VARCHAR NOT NULL UNIQUE
);

---
--- name table
---
CREATE TYPE "name_gender_type" AS ENUM ('M', 'F');

CREATE TABLE IF NOT EXISTS "name" (
    id UUID PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    value VARCHAR NOT NULL,
    gender name_gender_type NOT NULL,
    UNIQUE (value, gender)
);

CREATE INDEX IF NOT EXISTS "name_gender_idx" ON "name" ("gender");

---
--- game table
---
CREATE TABLE IF NOT EXISTS "game" (
    id UUID PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    owner_id UUID NOT NULL REFERENCES "user",
    description VARCHAR,
    gender name_gender_type
);

CREATE INDEX IF NOT EXISTS "game_owner_id_idx" ON "game" ("owner_id");

---
--- game_guest table
---
CREATE TABLE IF NOT EXISTS "game_guest" (
    id UUID PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    game_id UUID NOT NULL REFERENCES "game",
    user_id UUID NOT NULL REFERENCES "user",
    UNIQUE (game_id, user_id)
);

CREATE INDEX IF NOT EXISTS "game_guest_game_id_idx" ON "game_guest" ("game_id");
CREATE INDEX IF NOT EXISTS "game_guest_user_id_idx" ON "game_guest" ("user_id");

---
--- game_first_stage table
---
CREATE TABLE IF NOT EXISTS "game_first_stage" (
    id UUID PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    game_id UUID NOT NULL REFERENCES "game",
    user_id UUID NOT NULL REFERENCES "user",
    name_id UUID NOT NULL REFERENCES "name",
    choice BOOLEAN NOT NULL,
    UNIQUE (game_id, user_id, name_id)
);

CREATE INDEX IF NOT EXISTS "game_first_stage_game_id_idx" ON "game_first_stage" ("game_id");
CREATE INDEX IF NOT EXISTS "game_first_stage_user_id_idx" ON "game_first_stage" ("user_id");
CREATE INDEX IF NOT EXISTS "game_first_stage_name_id_idx" ON "game_first_stage" ("name_id");
CREATE INDEX IF NOT EXISTS "game_first_stage_choice_idx" ON "game_first_stage" ("choice");

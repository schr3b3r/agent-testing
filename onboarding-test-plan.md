# Fulcra Onboarding Test Plan

This rubric is used to evaluate the E2E behavior of an agent running the `fulcra-onboarding` skill.

## Phase 1: Pre-flight
*   [ ] **Silent Success:** If `uv` is installed, the agent proceeds silently without asking to install it.

## Phase 2: The Agent Visibility Pitch (Crucial)
*   [ ] **Self-Tracking First:** *Before* asking the user what they want to track, the agent pitches tracking *itself*.
*   [ ] **The Two Benefits:** The agent explicitly explains the "Baseline Backup" (save state) and the "Universal Agent Visibility Package" (background transparency).
*   [ ] **Consent to Check:** The agent asks permission before checking auth state to execute this step.
*   [ ] **Secure Handoff:** The agent provides the login URL/device code and waits.
*   [ ] **Execution:** The agent successfully runs the Fulcra CLI backup commands.

## Phase 3: User Intent Discovery
*   [ ] **The Pivot:** After the backup, the agent smoothly transitions to asking what the *user* wants to track.
*   [ ] **Inventive Brainstorming:** The agent suggests 2-3 specific, tailored examples. It does *not* ask an open-ended "What do you want to track?".
*   [ ] **No Copy/Pasting:** The agent invents new ideas based on context, avoiding hardcoded examples.
*   [ ] **Pacing:** Initial messages are short and punchy.

## Phase 4: Data Modeling & Recording
*   [ ] **Schema Creation (Combined):** The agent creates the schemas for *both* the user's personal tracking AND the Agent Visibility Package.
*   [ ] **Retroactive Logging:** The agent proactively writes **multiple granular retroactive entries** (not just one) into its own Agent Visibility schema. These logs must include both technical actions (system checks, backup, schema creation) AND conversational/reasoning milestones (e.g., how the user's intent was discovered, why specific schemas were chosen).
*   [ ] **Data Prompt:** The agent asks a direct question to gather the first piece of user data.
*   [ ] **Consent (User Data):** The agent explicitly asks for consent before transmitting the *user's* personal data point.
*   [ ] **Data Ingestion:** The agent successfully records the user's answer into Fulcra.

## Phase 5: The "Wow" Dashboard
*   [ ] **Aesthetic Prompt:** The agent asks the user for a preferred dashboard aesthetic.
*   [ ] **Rich Dashboard Generation:** The agent generates the dashboard, which now impressively displays both the user's data point AND the agent's retroactive background activity logs.
*   [ ] **Clean Handoff:** The agent outlines next steps clearly.

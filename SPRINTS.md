# Hermes Web UI -- Forward Sprint Plan

> Current state: v0.15 | 221 tests | Daily driver ready
> This document plans the path from here to two targets:
>
> Target A: 1:1 feature parity with the Hermes CLI (everything you can do from the
>           terminal, you can do from the browser)
>
> Target B: 1:1 parity with Claude's reproducible features (the full Claude
>           browser UI experience, minus things only Anthropic can build)
>
> Sprints are ordered by impact. Each builds on the one before.
> Past sprint history lives in CHANGELOG.md.

---

## Where we are now (v0.12.1)

**CLI parity: ~80% complete.** Core agent loop, all tools visible, workspace
file ops, cron/skills/memory CRUD, session management, streaming, cancel --
all solid. Gaps are configuration, subagent visibility, and runtime controls.

**Claude parity: ~55% complete.** Chat, streaming, file browser,
session management, tool cards, syntax highlighting, model switching -- all
present. Gaps are project organization, artifacts, voice, sharing, mobile.

---

## Sprint 11 -- Multi-Provider Models + Streaming Smoothness (COMPLETED)

**Theme:** Use any Hermes-supported model provider from the UI, and make
heavy agentic work feel fast and fluid.

**Why now:** Two high-impact gaps converge here. First, the model dropdown is
hardcoded to ~10 OpenRouter model strings. If Hermes is configured with direct
Anthropic, OpenAI, Google, or other API providers, the web UI can't use them.
This means users who set up Hermes with native API keys are locked out of
their own models in the browser. Second, the streaming render path rebuilds
the entire message list on every tool event, causing visible flicker during
heavy agentic work.

### Track A: Bugs
- Tool card DOM thrash: renderMessages() rebuilds all cards on each tool event.
  Switch to incremental append (append new card to existing group, no full rebuild).
- Scroll position lost on re-render during streaming (messages jump).

### Track B: Features
- **Multi-provider model support:** Query Hermes agent's configured providers
  and available models at startup via a new `GET /api/models` endpoint. The
  model dropdown populates dynamically from whatever providers the user has
  configured (OpenRouter, direct OpenAI, direct Anthropic, Google, DeepSeek,
  etc.). Group by provider. Fall back to the current hardcoded list if the
  agent query fails. This ensures the web UI can use any model the CLI can.
- **Incremental tool card streaming:** Instead of renderMessages() on each
  tool event, maintain a live card group element per turn and append/update
  cards in place. The assistant text row below the cards also updates
  incrementally (already does via assistantBody.innerHTML).
- **Smooth scroll:** Pin scroll to bottom during streaming unless user has
  manually scrolled up (read-back mode). Resume pinning when user scrolls
  back to bottom.

### Track C: Architecture
- `api/routes.py`: extract the 49 if/elif route handlers from server.py's
  Handler class into a dedicated routes module. server.py becomes a true
  ~50-line shell: imports, Handler stub that delegates to routes, main().
  Completes the server split started in Sprint 10.

**Tests:** ~15 new. Total: ~205.
**Hermes CLI parity impact:** High (model provider parity is a major CLI gap)
**Claude parity impact:** Low (streaming smoothness)

---

## Sprint 12 -- Settings Panel + Reliability + Session QoL

**Theme:** Persist your preferences, survive network blips, and organize sessions.

**Why now:** Three daily-driver friction points converge. First, default model
and workspace aren't persisted server-side -- every restart loses them. Second,
SSH tunnel hiccups during long agent runs silently kill the response with no
recovery. Third, after 50+ sessions the flat chronological list makes it hard
to keep important conversations accessible.

### Track A: Bugs
- Workspace validation on add doesn't check symlinks (shows as invalid when
  it's actually a valid symlink to a directory).

### Track B: Features
- **Settings panel:** A gear icon in the topbar opens a slide-in settings panel.
  Sections: Default Model, Default Workspace. Persisted server-side in
  `~/.hermes/webui-mvp/settings.json`. Server reads settings on startup and
  uses them as defaults. `GET /api/settings` + `POST /api/settings` endpoints.
- **SSE auto-reconnect:** When the EventSource connection drops mid-stream
  (network blip, SSH tunnel hiccup), auto-reconnect once using the same
  `stream_id`. The server-side queue holds undelivered events. If reconnect
  fails after 5s, show error banner. This is the #1 reliability gap for
  remote VPS usage.
- **Pin sessions:** A star icon on any session in the sidebar. Pinned sessions
  float to the top of the list above date groups. Persisted on the session
  JSON as `pinned: true`. Toggle on click. Simple and high quality-of-life.
- **Import session from JSON:** Drag a `.json` export file into the sidebar
  (or click an import button) to restore it as a new session. Mirrors the
  existing JSON export. Useful for moving sessions between machines.

### Track C: Architecture
- Settings schema: `settings.json` with typed fields, validated on load, with
  sane defaults. Served via `GET /api/settings`, written via `POST /api/settings`.
- SSE reconnect: server keeps `STREAMS[stream_id]` alive for 60s after
  client disconnect, allowing reconnect with the same stream_id.

**Tests:** ~15 new. Total: ~216.
**Hermes CLI parity impact:** Medium (settings persistence, reliability)
**Claude parity impact:** Medium (settings panel, pinned conversations)

---

## Sprint 13 -- Alerts, Session QoL, Polish

**Theme:** Know what Hermes is doing, and small quality-of-life wins.

**Why now:** Cron jobs run silently. Background errors surface nowhere. You have
no way to know a long-running task finished (or failed) while you were on another
tab. Meanwhile, a few small UX gaps (no session duplicate, no tab title) add up
to daily friction.

### Track A: Bugs
- Symlink workspace validation — confirmed already fixed (`.resolve()` follows
  symlinks before `is_dir()` check).

### Track B: Features
- **Cron completion alerts:** `GET /api/crons/recent?since=TIMESTAMP` endpoint.
  UI polls every 30s (only when tab is focused). Toast notification on each
  completion. Red badge count on Tasks nav tab, cleared when tab is opened.
- **Background agent error alerts:** When a streaming session errors out and
  the user is on a different session, show a persistent red banner above the
  message area: "Session X encountered an error." Click "View" to navigate,
  "Dismiss" to clear.
- **Session duplicate:** Copy icon on each session in the sidebar (visible on
  hover). Creates a new session with same workspace/model, titled "(copy)".
- **Browser tab title:** `document.title` updates to show the active session
  title (e.g. "My Task — Hermes"). Resets to "Hermes" when no session active.

**Tests:** ~10 new. Total: ~221.
**Hermes CLI parity impact:** Medium (cron visibility, error surfacing)
**Claude parity impact:** Low

---

## Sprint 14 -- Visual Polish + Workspace Ops + Session Organization (COMPLETED)

**Theme:** Polish the visual experience, close workspace file gaps, and
organize sessions properly.

### Track B: Features
- **Mermaid diagram rendering:** Code blocks tagged `mermaid` render as
  diagrams inline. Mermaid.js loaded lazily from CDN. Dark theme. Falls
  back to code block on parse error.
- **Message timestamps:** Subtle HH:MM time next to each role label. Full
  date/time on hover. User messages tagged with `_ts` on send.
- **Date grouping fix:** Session list uses `created_at` for groups instead
  of `updated_at`. Prevents sessions jumping between groups on auto-title.
- **File rename:** Double-click any filename in the workspace panel to
  rename inline (same pattern as session rename). `POST /api/file/rename`.
- **Folder create:** Folder icon button in workspace panel header.
  `POST /api/file/create-dir`. Prompt for folder name.
- **Session tags:** Add `#tag` to session titles. Tags extracted and shown
  as colored chips in the sidebar. Click a tag to filter the session list.
- **Session archive:** Archive button on each session (box icon). Archived
  sessions hidden from sidebar by default. "Show N archived" toggle at top
  of list. `POST /api/session/archive` endpoint.

**Tests:** ~12 new. Total: ~233.
**Hermes CLI parity impact:** Medium (file rename, folder create)
**Claude parity impact:** Medium (Mermaid, tags, archive)

---

## Sprint 15 -- Session Projects + Code Copy + Tool Card Toggle (COMPLETED)

**Theme:** Organize work the way you think, not just chronologically.
Plus two quick UX wins for code and agentic workflows.

**Why now:** After 100+ sessions the sidebar is a flat chronological list.
Finding sessions from 2 weeks ago, or keeping work separated by project,
requires the search box. Session projects are the single biggest remaining
organizational gap vs. Claude's project folders.

### Track A: Bugs
- None.

### Track B: Features
- **Session projects:** Named groups for organizing sessions. A project
  filter bar (subtle chips) sits between the search input and the session
  list. Each project has a name and color. Click a chip to filter sessions
  to that project; "All" shows everything. Create projects inline (+
  button), rename (double-click chip), delete (right-click). Assign
  sessions via folder icon button (hover-reveal) with a dropdown picker.
  Projects stored in `projects.json`. Session model gains `project_id`
  field (null = unassigned). Fully backward-compatible with existing
  sessions. Endpoints: `GET /api/projects`, `POST /api/projects/create`,
  `POST /api/projects/rename`, `POST /api/projects/delete`,
  `POST /api/session/move`.
- **Code block copy button:** Every code block gets a "Copy" button.
  Positioned in the language header bar (or top-right corner for plain
  code blocks). Click copies code to clipboard, shows "Copied!" for 1.5s.
- **Tool card expand/collapse:** When a message has 2+ tool cards, an
  "Expand all / Collapse all" toggle appears above the card group.
  Scoped per message group, not global.

### Track C: Architecture
- `projects.json` flat file storage for project list (same pattern as
  `workspaces.json` and `settings.json`).
- `project_id` field on Session model with backward-compatible null default.
- `_index.json` includes `project_id` for fast client-side filtering.

**Tests:** 13 new. Total: ~237.
**Hermes CLI parity impact:** Low (CLI has no session organization)
**Claude parity impact:** Very High (projects are a core Claude concept)

### Candidates for next sprints
- Workspace reorder (drag-and-drop)
- View skill linked files
- Voice input via Whisper
- Subagent delegation cards (enhanced tool card rendering)

---

## Sprint 16 -- Artifacts + Code Execution

**Theme:** See outputs, not just text.

**Why now:** Claude's most distinctive feature is the artifact panel --
code runs inline, HTML renders in a sandboxed iframe, SVGs show as images.
This is the largest single capability gap between what we have and what Claude
feels like. It also directly enables the Hermes "code execution cell" feature
(Jupyter-style in-browser execution).

### Track A: Bugs
- Prism.js autoloader makes one CDN request per language encountered. On a
  code-heavy session this causes noticeable latency. Bundle the top 10 languages
  (Python, JS, bash, JSON, SQL, YAML, TypeScript, CSS, HTML, Rust) locally.
- Code blocks in long responses sometimes re-highlight on every renderMessages()
  call. Debounce highlightCode() with requestAnimationFrame.

### Track B: Features
- **Artifact panel:** When Hermes produces a code block tagged as `html`, `svg`,
  or `react`, a "Preview" button appears on that code block. Clicking it opens
  a sandboxed `<iframe>` in the right panel showing the rendered output. The
  preview updates live if Hermes edits the artifact in a follow-up.
- **Code execution cell:** A "Run" button on Python code blocks. Sends the code
  to a new server endpoint (`POST /api/execute`) which runs it in a subprocess
  with a 30-second timeout and streams stdout/stderr back as SSE. Output appears
  below the code block inline. This is the Jupyter cell experience without
  needing a kernel.
- **Mermaid diagram rendering:** Mermaid.js CDN (deferred). Code blocks tagged
  as `mermaid` render as flow/sequence/gantt diagrams inline.

### Track C: Architecture
- Sandbox safety: `/api/execute` runs in a restricted subprocess (no network,
  limited filesystem via a temp directory). Returns exit code, stdout, stderr,
  and execution time.
- Artifact state: artifacts are tracked in `S.artifacts = {}` (code block hash
  -> rendered content). Persisted in session JSON as `artifacts` array.

**Tests:** ~18 new. Total: ~259.
**Hermes CLI parity impact:** High (code execution closes the Jupyter gap)
**Claude parity impact:** Very High (artifacts are Claude's signature feature)

---

## Sprint 17 -- Voice + Multimodal Input

**Theme:** Input beyond the keyboard.

**Why now:** Voice is a meaningful quality-of-life feature for longer sessions
and is achievable with Whisper. Image input closes the last modality gap with
Claude (Claude accepts image paste natively -- we do too, but only as
file uploads, not clipboard screenshots into the conversation directly).

### Track A: Bugs
- Image paste currently requires a click-to-attach flow. Direct paste into the
  message textarea should embed the image inline (as a preview chip) and queue
  it for upload on Send. (Partially works -- clean up edge cases.)
- Large image uploads (>5MB) time out the upload step silently.

### Track B: Features
- **Voice input (Whisper):** A microphone icon in the composer. Hold to record,
  release to transcribe via `POST /api/transcribe` (calls local Whisper or
  OpenAI Whisper API). Transcribed text appears in the message input, editable
  before send. Supports the full "voice -> text -> Hermes response" loop.
- **TTS playback:** A speaker icon on assistant messages. Calls a TTS endpoint
  (ElevenLabs or OpenAI TTS) and plays the audio. Toggle per-message. Optional
  auto-play mode in settings.
- **Vision input improvements:** Paste a screenshot directly from clipboard into
  the conversation (not just the tray). Shows as an inline preview chip with
  the image thumbnail. On Send, uploads and includes in the message.

### Track C: Architecture
- Audio pipeline: `POST /api/transcribe` streams audio bytes, returns transcript.
  `GET /api/tts?text=...` returns audio/mpeg. Both use lazy import of Whisper
  and TTS libraries to keep cold start fast.

**Tests:** ~12 new. Total: ~271.
**Hermes CLI parity impact:** Medium (voice not in CLI, but adds capability)
**Claude parity impact:** High (Claude has native voice mode)

---

## Sprint 18 -- Subagent Visibility + Agentic Transparency

**Theme:** Watch Hermes think, not just respond.

**Why now:** When Hermes delegates to subagents (delegate_task, spawns parallel
workstreams), the UI shows nothing. On long multi-agent tasks you have no idea
what's happening. This is the last major "CLI feels better" gap for power users.

### Track A: Bugs
- Tool cards for delegate_task show no information about what the subagent was
  asked to do or what it returned.
- The activity bar text truncates at 55 chars -- tool previews for long terminal
  commands show nothing useful.

### Track B: Features
- **Subagent delegation cards:** When `delegate_task` fires, show an expandable
  card with the subagent's goal, status (pending/running/done), and result
  summary. Multiple subagents from one call appear as a card group. Uses the
  existing tool card infrastructure.
- **Background task monitor:** A "Tasks" indicator in the topbar (separate from
  the cron Tasks panel). Shows count of active agent threads. Click opens a
  popover listing all in-flight streams with session names and elapsed times.
  Cancel any individual thread. This is the full job queue visibility the CLI
  implicitly has via `ps aux`.
- **Thinking/reasoning display:** When the model emits reasoning tokens (o3,
  Claude extended thinking), show them in a collapsible "Reasoning" card above
  the response. Collapsed by default. This matches Claude's reasoning display.

### Track C: Architecture
- Task registry: extend STREAMS to include session name, start time, and task
  description. New `GET /api/tasks/active` endpoint returns all running streams
  with metadata.

**Tests:** ~14 new. Total: ~285.
**Hermes CLI parity impact:** Very High (subagent and task visibility is the
  last major CLI gap)
**Claude parity impact:** High (Claude shows reasoning, tool use visibly)

---

## Sprint 19 -- Auth, HTTPS, and Production Hardening

**Theme:** Make this safe to leave running.

**Why now:** Everything else is done. This is the sprint you run when you want
to expose the UI beyond localhost -- to a team, a mobile device, or a public
address.

### Track A: Bugs
- Server has no request size limit on non-upload endpoints (potential DoS).
- Session JSON files have no size cap (a runaway agent could write GBs).

### Track B: Features
- **Password authentication:** A login page with a configurable password
  (HERMES_WEBUI_PASSWORD env var). Signed cookie session (24h expiry).
  Single-user model -- no accounts, no registration.
- **HTTPS / reverse proxy guide:** A one-page `DEPLOY.md` with instructions
  for running behind nginx + Let's Encrypt on a VPS. Configuration snippets
  for systemd service, nginx config, certbot.
- **Mobile responsive layout:** Collapsible sidebar (hamburger). Touch-friendly
  session list (swipe to delete, tap to navigate). Composer expands on focus.
  Right panel hidden by default on mobile, accessible via a Files tab.
- **Rate limiting:** Simple per-IP token bucket on the chat/start endpoint
  (configurable, default 10 req/min) to prevent accidental hammering.

### Track C: Architecture
- Helmet headers: X-Content-Type-Options, X-Frame-Options, HSTS (when served
  over HTTPS). Simple middleware in the Handler.

**Tests:** ~12 new. Total: ~297.
**Hermes CLI parity impact:** Low (CLI has no auth/HTTPS concerns)
**Claude parity impact:** Very High (Claude is authenticated, HTTPS only)

---

## Feature Parity Summary

### After Sprint 18 (Hermes CLI parity: complete)

| CLI Feature | Status |
|-------------|--------|
| Chat / agent loop | Done (v0.3) |
| Streaming responses | Done (v0.5) |
| Tool call visibility | Done (v0.11) |
| File ops (read/write/search/patch) | Done (v0.6) |
| Terminal commands | Done via workspace |
| Cron job management | Done (v0.9) |
| Skills management | Done (v0.9) |
| Memory read/write | Done (v0.9) |
| Session history | Done (v0.3) |
| Workspace switching | Done (v0.7) |
| Model selection | Done (v0.3) |
| Multi-provider model support | Done (Sprint 11) |
| Toolset control | Sprint 12 |
| Settings persistence | Done (Sprint 12) |
| Subagent visibility | Sprint 18 |
| Background task monitor | Sprint 18 |
| Code execution (Jupyter) | Sprint 16 |
| Cron completion alerts | Done (Sprint 13) |
| Virtual scroll (perf) | Deferred |

### After Sprint 19 (Claude parity: ~90% complete)

| Claude Feature | Status |
|----------------|--------|
| Dark theme, 3-panel layout | Done (v0.1) |
| Streaming chat | Done (v0.5) |
| Model switching | Done (v0.3) |
| File attachments | Done (v0.6) |
| Syntax highlighting | Done (v0.10) |
| Tool use visibility | Done (v0.11) |
| Edit/regenerate messages | Done (v0.10) |
| Session management | Done (v0.6) |
| Artifacts (HTML/SVG preview) | Sprint 16 |
| Code execution inline | Sprint 16 |
| Mermaid diagrams | Done (Sprint 14) |
| Projects / folders | Done (Sprint 15) |
| Pinned/starred sessions | Done (Sprint 12) |
| Reasoning display | Sprint 18 |
| Voice input | Sprint 17 |
| TTS playback | Sprint 17 |
| Notifications | Done (Sprint 13) |
| Settings panel | Done (Sprint 12) |
| Auth / login | Sprint 19 |
| HTTPS | Sprint 19 |
| Mobile layout | Done (v0.16.1) |
| Sharing / public URLs | Not planned (requires server infra) |
| Claude-specific features | Not replicable (Projects AI, artifacts sync) |

### What is intentionally not planned

- **Sharing / public conversation URLs:** Requires a hosted backend with access
  control and CDN. Out of scope for a personal VPS deployment.
- **Claude-specific model features:** Claude-native Projects memory, extended
  artifacts sync, Anthropic's proprietary reasoning UI. These are Anthropic
  infrastructure, not reproducible.
- **Real-time collaboration:** Multiple users in the same session simultaneously.
  Single-user assumption throughout.
- **Plugin marketplace:** Hermes skills cover this use case already.

---

*Last updated: April 1, 2026*
*Current version: v0.17 | 237 tests*
*Next sprint: Sprint 16 (Artifacts + Code Execution)*

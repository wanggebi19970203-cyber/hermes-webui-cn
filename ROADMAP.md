# Hermes Web UI: Full Parity Roadmap

> Goal: Full 1:1 parity with the Hermes CLI experience via a clean dark web UI.
> Everything you can do from the CLI terminal, you can do from this UI.
>
> Last updated: Sprint 15 (April 1, 2026)
> Tests: 237 passing
> Source: <repo>/

---

## Sprint History (Completed)

| Sprint | Theme | Highlights | Tests |
|--------|-------|-----------|-------|
| Sprint 1 | Bug fixes + foundations | B1-B11 fixed, LOCK on SESSIONS, section headers, request logging | 19 |
| Sprint 2 | Rich file preview | Image preview, rendered markdown, table support, smart icons | 27 |
| Sprint 3 | Panel nav + viewers | Sidebar tabs, cron/skills/memory panels, B6/B10/B14, Phase D start | 48 |
| Sprint 4 | Relocation + power features | Source to <repo>/, CSS extracted, session rename/search, file ops | 68 |
| Sprint 5 | Phase A complete + workspace | JS extracted (server.py 1778->1042 lines), workspace management, copy message, file editor, session index | 86 |
| Test hardening | Isolated test environment | Port 8788 test server, conftest autouse, cleanup_zero_message, 5 test files rewritten | 90 |
| Sprint 6 | Polish + Phase E complete | HTML to static/, resizable panels, cron create, session JSON export, Escape from editor | 106 |
| Sprint 7 | Wave 2 Core: CRUD + Search | Cron edit/delete, skill create/edit/delete, memory write, session content search, health improvements, git init | 125 |
| Sprint 8 | Daily Driver Finish Line | Edit+regenerate user messages, regenerate last response, clear conversation, Prism.js syntax highlighting, reconnect banner fix, session list scroll fix | 139 |
| Sprint 8 hotfix | Message queue + INFLIGHT fix | Queue messages while busy (toast + badge + auto-drain), INFLIGHT-first loadSession (message stays on switch-away/back) | 139 |
| Sprint 9 | Codebase health + daily driver gaps | app.js deleted and replaced by 6 modules, tool call cards inline, attachment persistence on reload, todo list panel | 149 |
| Sprint 10 | Server health + operational polish | server.py split into api/ modules, background task cancel, cron run history viewer, tool card UX polish | 167 |
| Sprint 10 fixes | Import regressions + regression tests | uuid, AIAgent, has_pending, SSE cancel loop, Session.__init__ tool_calls; test_regressions.py | 177 |
| Concurrency sweeps | Multi-session correctness | Approval cross-session (R10), activity bar per-session (R11), live cards on switch-back (R12), tool cards after done (R13), session model authoritative (R14), newSession cards (R15) | 190 |
| Sprint 11 | Multi-provider models + streaming | Dynamic model dropdown (any Hermes provider), smooth scroll pinning, routes extracted to api/routes.py (server.py 704→76 lines) | 201 |
| Sprint 12 | Settings + reliability + session QoL | Settings panel (gear icon, settings.json), SSE auto-reconnect, pin sessions, import session from JSON | 211 |
| Sprint 13 | Alerts + polish | Cron completion alerts (polling + badge), background error banner, session duplicate, browser tab title | 221 |
| Sprint 14 | Visual polish + workspace ops | Mermaid diagrams, message timestamps, file rename, folder create, session tags, session archive | 233 |
| Sprint 15 | Session projects + code copy | Session projects/folders, code block copy button, tool card expand/collapse toggle | 237 |

---

## Current Architecture Status

| Layer | Location | Status |
|-------|----------|--------|
| Python server | <repo>/server.py (~76 lines) + api/ modules (~1900 lines) | Thin shell + business logic in api/ |
| HTML template | <repo>/static/index.html | Served from disk |
| CSS | <repo>/static/style.css | Served from disk |
| JavaScript | <repo>/static/{ui,workspace,sessions,messages,panels,boot}.js | 6 modules, ~2250 lines total |
| Runtime state | ~/.hermes/webui-mvp/sessions/ | Session JSON files |
| Test server | Port 8788, state dir ~/.hermes/webui-mvp-test/ | Isolated, wiped per run |
| Production server | Port 8787 | SSH tunnel from Mac |

---

## Feature Parity Checklist

### Chat and Agent
- [x] Send messages, get SSE-streaming responses
- [x] Switch models per session (10 models, grouped by provider)
- [x] Multi-provider API support: use any Hermes agent API provider (OpenAI, Anthropic, Google, etc.) directly, not just OpenRouter (Sprint 11)
- [x] Upload files to workspace (drag-drop, click, clipboard paste)
- [x] File tray with remove button
- [x] Tool progress shown in activity bar above composer
- [x] Approval card for dangerous commands (Allow once/session/always, Deny)
- [x] Approval polling + SSE-pushed approval events
- [x] INFLIGHT guard: switch sessions mid-request without losing response
- [x] Session restores from localStorage on page load
- [x] Reconnect banner if page reloaded mid-stream
- [x] Copy message to clipboard (hover icon on each bubble)
- [x] Edit last user message and regenerate
- [ ] Branch/fork conversation (Wave 3)
- [ ] Token/cost estimate per message (Wave 3)

### Tool Visibility
- [x] Tool progress in activity bar (moved out of composer footer)
- [x] Approval card with all 4 choices
- [x] Tool call cards inline (collapsed, show name/args/result)

### Workspace / Files
- [x] Browse workspace directory tree with type icons
- [x] Preview text/code files (read-only)
- [x] Preview markdown files (rendered, tables supported)
- [x] Preview image files (PNG, JPG, GIF, SVG, WEBP inline)
- [x] Edit files inline (Edit button, Enter to save, Escape to cancel)
- [x] Create new file (+ button in panel header)
- [x] Delete file (hover trash, confirm dialog)
- [x] File name truncation with tooltip for long names
- [x] Right panel resizable (drag inner edge)
- [x] Syntax highlighted code preview (Prism.js)
- [x] Rename file (Sprint 14)
- [x] Create folder (Sprint 14)

### Sessions
- [x] Create session (+ button or Cmd/Ctrl+K)
- [x] Load session (click in sidebar)
- [x] Delete session (hover trash, toast, correct fallback)
- [x] Auto-title from first user message
- [x] Rename session title (double-click in sidebar, Enter saves, Escape cancels)
- [x] Filter/search sessions by title (live filter box)
- [x] Date group headers (Today / Yesterday / Earlier)
- [x] Download session as Markdown transcript
- [x] Export session as JSON (full messages + metadata)
- [x] Session inherits last-used workspace on creation
- [x] Session content search (search message text across sessions)
- [x] Session tags / labels (Sprint 14)
- [x] Archive sessions (Sprint 14)
- [x] Clear conversation (wipe messages, keep session) (Wave 3)
- [x] Import session from JSON (Sprint 12)
- [x] Pin/star sessions to top of list (Sprint 12)
- [x] Duplicate session (Sprint 13)
- [x] Session projects / folders (Sprint 15)

### Workspace Management
- [x] Add workspace with path validation (must be existing directory)
- [x] Remove workspace
- [x] Rename workspace display name
- [x] Quick-switch workspace from topbar dropdown
- [x] Sidebar live workspace display (name + path, updates in real time)
- [x] New sessions inherit last used workspace
- [x] Workspace list persists to workspaces.json
- [ ] Workspace reorder (drag) (Wave 2)

### Scheduled Tasks (Cron)
- [x] View all cron jobs (Tasks sidebar tab)
- [x] View last run output per job (auto-loaded on expand)
- [x] Expand job to see prompt, schedule, last output
- [x] Run job manually (Run now button)
- [x] Pause / Resume job
- [x] Create cron job from UI (+ New job form with name, schedule, prompt, delivery)
- [x] Edit existing cron job
- [x] Delete cron job
- [x] View full cron run history (expandable per job)
- [ ] Skill picker in cron create form (Wave 3)

### Skills
- [x] List all skills grouped by category (Skills sidebar tab)
- [x] Search/filter skills by name, description, category
- [x] View full SKILL.md content in right preview panel
- [x] Create skill
- [x] Edit skill
- [x] Delete skill
- [ ] View skill linked files (Wave 3)

### Memory
- [x] View personal notes (MEMORY.md) rendered as markdown (Memory tab)
- [x] View user profile (USER.md) rendered as markdown (Memory tab)
- [x] Last-modified timestamp on each section
- [x] Add/edit memory entry inline

### Configuration
- [x] Settings panel (default model, default workspace) (Sprint 12)
- [ ] Enable/disable toolsets per session (deferred)

### Notifications
- [x] Cron job completion alerts (Sprint 13)
- [x] Background agent error alerts (Sprint 13)

### Advanced / Future
- [ ] Voice input via Whisper (Wave 6)
- [ ] TTS playback of responses (Wave 6)
- [ ] Subagent delegation cards (Wave 6)
- [x] Background task cancel (activity bar Cancel button)
- [ ] Code execution cell (Wave 6)
- [ ] Password authentication (Wave 7)
- [ ] HTTPS / reverse proxy (Wave 7)
- [ ] Mobile responsive layout (Wave 7)
- [ ] Virtual scroll for large lists (Wave 7)

---

## Sprint 7: Wave 2 Core -- Cron/Skill/Memory CRUD + Session Content Search (COMPLETED)

**Theme:** "Wave 2 Core -- Cron/Skill/Memory CRUD + Session Content Search"

### Track A: Bug Fixes
| Item | Description |
|------|-------------|
| Activity bar sizing | Activity bar sometimes overlaps first message on short viewports |
| Model dropdown sync | Model chip in topbar sometimes shows stale model after session switch |
| Cron output truncation | Long cron output in the tasks panel overflows its container |

### Track B: Features
| Feature | What | Value |
|---------|------|-------|
| Session content search | Search message text across all sessions, not just titles. GET /api/sessions/search already does title search; extend to message content with a configurable depth limit | High: the single most-requested nav feature after rename |
| Cron edit + delete | Edit an existing cron job (name, schedule, prompt, delivery) inline in the tasks panel. Delete with confirm. POST /api/crons/update and /api/crons/delete | High: closes the cron CRUD gap (create was Sprint 6) |
| Skill create + edit | A "New skill" form in the Skills panel. Name, category, SKILL.md content in a textarea editor. Save calls POST /api/skills/save (writes to ~/.hermes/skills/). Edit opens existing skill in the same editor | High: biggest remaining CLI gap after cron |

### Track C: Architecture
| Item | What |
|------|------|
| Phase E: app.js module split (start) | Split app.js (1332 lines) into logical modules: sessions.js, chat.js, workspace.js, panels.js, ui.js. Serve via ES module imports in index.html. This is Phase E completion. |
| Health endpoint improvement | Add active_streams, uptime_seconds to /health response (Phase G) |
| Git init | git init <repo>, first commit, push to private GitHub repo |

### Tests
- ~20 new pytest tests (cron update/delete, skill save, session content search)
- TESTING.md: Sections 29-31 (cron edit, skill edit, session search)
- Estimated total after Sprint 7: ~126

---

## Wave 2: Full CRUD and Interaction Parity

**Status:** In progress. Sprint 6 completed cron create and workspace management.
Remaining Wave 2 items targeted for Sprints 7-8.

### Sprint 2.0: Workspace Management (COMPLETE Sprint 5+6)
All workspace features delivered: add/validate/remove/rename workspaces, topbar quick-switch,
sidebar live display, new sessions inherit last workspace. See Sprint 5 completed section.

### Sprint 2.1: Cron Job Management (Partial -- Sprint 7 for remaining)
- [x] View all jobs (Sprint 3)
- [x] Run / pause / resume (Sprint 3)
- [x] Create job from UI (Sprint 6)
- [x] Edit job
- [x] Delete job
- [x] Full cron run history

### Sprint 2.2: Skill Management (Partial -- Sprint 7 for remaining)
- [x] List all skills with categories (Sprint 3)
- [x] View SKILL.md content (Sprint 3)
- [x] Create skill
- [x] Edit skill
- [x] Delete skill

### Sprint 2.3: Memory Write (Sprint 7)
- [x] View notes + profile (Sprint 3)
- [x] Edit notes inline

### Sprint 2.4: Todo Management (Wave 2)
- [x] View current todo list (sidebar Todo panel, parsed from session history)

### Sprint 2.5: Session Content Search (Sprint 7)
- [x] Session title search (Sprint 4)
- [x] Message content search across sessions

### Sprint 2.6: Session Rename (COMPLETE Sprint 4)
Double-click any session title in the left sidebar to edit inline.
Enter saves, Escape cancels. Topbar updates immediately.

---

## Wave 3: Power Features and Developer Experience

### Sprint 3.1: Tool Call Visibility Inline
Show tool calls as collapsible cards in the conversation.
Collapsed: tool name badge + one-line preview. Expanded: full args + result.

### Sprint 3.2: Multi-Model Expansion
Add more models. Group by provider. Model info tooltip on hover.
(Partially done: 10 models in dropdown from Sprint 1.)

### Sprint 3.2b: Resizable Panel Widths (COMPLETE Sprint 6)
Both sidebar and workspace panel are drag-resizable with localStorage persistence.

### Sprint 3.3: Workspace File Actions
- [ ] Rename file (inline, double-click) (Wave 3)
- [ ] Create folder (Wave 3)
- [x] Syntax highlighted code preview (Prism.js)

### Sprint 3.4: Conversation Controls
- [x] Copy message (Sprint 5)
- [x] Edit last user message + regenerate
- [x] Regenerate last assistant response
- [x] Clear conversation (wipe messages, keep session)

---

## Wave 4: Settings, Configuration, Notifications

### Sprint 4.1: Settings Panel
Full settings overlay: default model, default workspace, enabled toolsets, config viewer.

### Sprint 4.2: Notification Panel
Bell icon with unread count. SSE endpoint for cron completions and errors. Toast pop-ups.

### Sprint 4.3: Delivery Target Config
Configure and test-ping delivery targets (Discord, Telegram, Slack, email) for cron jobs.

---

## Wave 5: Honcho Integration and Long-term Memory

### Sprint 5.1: Honcho Memory Panel
User representation panel, cross-session context, Honcho search, memory write.

### Sprint 5.2: Session Continuity Features
"What were we working on?" button, session tags, session archive.

---

## Wave 6: Realtime and Agentic Features

### Sprint 6.1: Background Task Monitor
Live list of running agent threads. Cancel button. Queue visibility.

### Sprint 6.2: Subagent Delegation Cards
When delegate_task fires, show subagent progress inline in chat.

### Sprint 6.3: Code Execution Panel
Jupyter-style inline code cell. Stateful kernel per session.

### Sprint 6.4: Voice Mode
Push-to-talk mic button. Whisper transcription. Optional TTS playback.

---

## Wave 7: Production Hardening and Mobile

### Sprint 7.1: Authentication
HERMES_WEBUI_PASSWORD env var gate. Signed cookie. Login page.

### Sprint 7.2: HTTPS and Reverse Proxy
Nginx + Let's Encrypt. CORS headers for external domain.

### Sprint 7.3: Mobile Responsive Layout
Collapsible sidebar hamburger. Touch-friendly controls. Swipe gestures.

### Sprint 7.4: Performance and Scale
Virtual scroll for session/message lists. Incremental message loading.

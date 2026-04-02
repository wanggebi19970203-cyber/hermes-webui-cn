# Bugs Backlog

This file tracks UI bugs and polish items to address in a future sprint.

## ~~Conversation list title truncation / hover actions~~ — Fixed (Sprint 16)

- **Was:** Action icons reserved ~30px of space even when invisible, truncating titles.
- **Fix:** Wrapped all action buttons in a `.session-actions` overlay container with `position:absolute`. Titles now use full available width. Actions appear on hover with a gradient fade from the right edge.

## ~~Folder/project assignment interaction feels sticky~~ — Fixed (Sprint 16)

- **Was:** Folder icon stayed permanently visible (blue, 60% opacity) when a session belonged to a project.
- **Fix:** Replaced `.has-project` persistent button with a colored left border matching the project color. The folder button now only appears in the hover overlay like all other actions.

## Notes

- Both issues resolved in Sprint 16 (Session Sidebar Visual Polish).
- Icons replaced from inconsistent emoji HTML entities to monochrome SVG line icons.

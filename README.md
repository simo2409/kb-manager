# KB Manager

A lightweight, single-page web application to manage your knowledge-base projects and launch them instantly in your favourite tools.

## What it does

KB Manager keeps a list of your projects (Obsidian vaults, code repositories, documentation folders, …). For each project you can:

- **Open** it in Finder, VS Code, Obsidian or Ghostty with one click.
- **Track** folder size, last-modified time and a per-project log extracted from `wiki/log.md`.
- **Favourite** the projects you use most and reorder them via drag & drop.
- **Search** across project names, paths and descriptions.

All project data is stored in the browser’s `localStorage`. No database required.

## Running the app

### Quick start (file:// mode)

Open `kb_manager.html` directly in your browser.  
In this mode the app works as a static page, but **launching external applications is disabled**; instead a copy-paste command is shown.

### Full experience (recommended)

Start the small Python helper server:

```bash
python3 launcher_server.py
```

Then open http://localhost:8765.

The local server adds:

- One-click launch of Finder, VS Code, Obsidian and Ghostty.
- Automatic folder-size calculation.
- Detection of the most recent file change inside each project.
- Extraction of the latest dated section from `wiki/log.md`.
- Bulk import of existing folders as new projects.

## Creating a project

1. Click **New project**.
2. Fill in the project name and the absolute path to the folder.
3. Optionally add a description and an Obsidian vault name.
4. Choose which shortcuts (Finder, VS Code, Obsidian, Ghostty) should appear for this project.
5. Click **Save project**.

If the folder does not exist yet, it will be created inside the *parent path* defined in **Settings**.

## Data & settings

- **Settings** – configure the default parent path for new projects and the colour-coded “last update” ranges (green / orange / red).
- **Export** – download a JSON backup of all your projects and settings.
- **Import** – restore a previously exported JSON file (overwrites current data).
- **Fetch** – scan the parent path and bulk-import existing folders as projects.

## Keyboard / accessibility

- The interface is fully keyboard-navigable.
- A skip-link lets you jump directly to the main content.
- Focus management and ARIA attributes are handled inside all dialogs.

## Requirements

- A modern web browser.
- Python 3 (only if you want the local server for full functionality).
- macOS (the server uses `open`, `code`, and `obsidian://` URIs).

## Project structure

```
.
├── kb_manager.html        # Main application (single-page)
├── launcher_server.py     # Python local server for macOS integration
└── design_system_v2/      # UI components, CSS, fonts and theme
```

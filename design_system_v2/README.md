# Design System v2

A dark-first, glassmorphism-driven design system for the Simone Dall'Angelo brand identity. Built with vanilla HTML, CSS and JavaScript.

## What's included

- **Foundation** — typography scale (Biennale font), color tokens, spacing scale, shadows and radius tokens.
- **Components** — buttons, forms, cards, navigation, feedback, layout and icons.
- **Themes** — dark mode by default with an automatic/light manual toggle.
- **Icons** — full [Phosphor Icons](https://phosphoricons.com/) integration via CDN, with a searchable gallery page.
- **Accessibility** — WCAG 2.2 aware patterns: focus-visible states, colour contrast, semantic HTML and ARIA attributes where needed.

## Structure

```
design_system_v2/
├── index.html              # Overview and quick reference
├── README.md               # This file
├── ds.css                  # Tokens + component styles
├── theme.js                # Theme toggle + mobile navigation
├── components/
│   ├── foundation.html     # Typography, colours, spacing
│   ├── buttons.html        # Button variants, sizes, split buttons
│   ├── forms.html          # Inputs, selects, checkboxes, switches
│   ├── cards.html          # Glass, flat, interactive, selected, code-block cards
│   ├── navigation.html     # Navbar, tabs, breadcrumbs
│   ├── feedback.html       # Alerts, badges, loaders, modals, tooltips
│   ├── layout.html         # Accordions, lists, tables, dividers
│   └── icons.html          # Phosphor Icons gallery with live search
└── fonts/
    └── Biennale/           # Brand typeface
```

## Quick start

Open `index.html` in a modern browser and use the top navigation to browse each component category.

## Usage in a project

1. Copy `ds.css` and `theme.js` into your project.
2. Include the Biennale font and Phosphor Icons CDN in your HTML:

```html
<link rel="stylesheet" href="fonts/Biennale/Biennale.css">
<link rel="stylesheet" href="ds.css">
<script src="https://unpkg.com/@phosphor-icons/web"></script>
<script src="theme.js"></script>
```

3. Use the utility classes and component classes defined in `ds.css`. Every component page contains copy-paste ready markup and a unique ID (e.g. `DS-BTN-001`) for traceability across design, development and QA.

## Browser support

Modern evergreen browsers. The system uses CSS custom properties, `color-mix()`, `backdrop-filter`, CSS Grid and container-friendly flex layouts.

## License

Built for the Simone Dall'Angelo brand identity. Usage rights are defined by the brand owner.

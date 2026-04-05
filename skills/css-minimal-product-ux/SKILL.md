---
name: css-minimal-product-ux
description: >-
  Build polished, minimal product UIs with CSS and UX patterns inspired by
  modern developer brands (clear hierarchy, token-based theming, dark mode,
  accessible interactions). Use when creating or refactoring HTML/CSS for any
  website or app surface — marketing pages, dashboards, docs, or static sites —
  especially when the goal is a calm, professional look without a heavy framework.
---

# Minimal product CSS and UX (portable)

This skill encodes **design and implementation rules** for a restrained,
product-grade UI: neutral palette, system typography, token-driven light/dark,
and accessible interactions. It is **domain-agnostic** — use the same rules for
SaaS, internal tools, marketing, docs, or content sites.

## When agents should use this skill

- New pages, sections, or components need to **match a restrained, product-grade** aesthetic.
- The stack is **plain HTML/CSS** (or CSS modules / scoped CSS) without a design system library.
- You need **light and dark** that respect system preference and optional user override.
- You are asked for **consistent spacing, type, and interaction** without reinventing patterns each time.

## UX principles (non-negotiables)

1. **Clarity over decoration** — One clear primary action per view; secondary actions are visually quieter. Avoid noisy gradients and heavy borders unless they encode meaning.
2. **Predictable hierarchy** — Title → supporting line → body. Headings use tighter letter-spacing and stronger weight; body uses comfortable line-height (~1.6) and muted secondary color for descriptions.
3. **Calm motion** — Short transitions (about 120–200ms, ease). Hover can lift slightly (`translateY(-1px)`) and add a soft shadow; do not animate large layout properties aggressively.
4. **Readable at any width** — Use `clamp()` for hero headings; cap line length for paragraphs (~52–68ch) where long reading matters.
5. **Accessible by default** — Sufficient contrast for text and controls; visible focus states; `aria-label` / `title` on icon-only buttons; respect `prefers-reduced-motion` for non-essential animation.

## CSS architecture

### 1. Design tokens on `:root`

Define **semantic UI variables** (colors, radius, shadow, font stacks, transition)
on `:root`. Components should consume **only variables**, not raw hex values,
so theming and dark mode stay maintainable.

- **Neutrals**: A small gray scale (e.g. 50–900) plus explicit `--black` / `--white` used as *semantic* text/surface roles (in dark mode, “black” may map to a light text color).
- **Semantic colors**: `--link`, `--link-hover`, optional `--success`, `--warning`, `--danger` for states.
- **Elevation**: `--shadow-sm`, `--shadow`, `--shadow-lg` kept subtle (low alpha).

### 2. Dark mode: explicit theme + system fallback

Support both:

- **User choice**: e.g. `data-theme="dark"` / `data-theme="light"` on `html` or `:root`.
- **System default**: `@media (prefers-color-scheme: dark)` on `:root:not([data-theme="light"])` so unauthenticated first paint matches OS.

**Mirror every override** — If you set nav or toggle styles under `[data-theme="dark"]`, duplicate the same rules under `prefers-color-scheme: dark` for `:root:not([data-theme="light"])` so behavior matches when the user has not toggled yet.

### 3. Typography

- **Body**: system UI stack (`-apple-system`, `BlinkMacSystemFont`, `Segoe UI`, `system-ui`, sans-serif), antialiased, ~15px base, line-height ~1.65.
- **Code**: monospace stack with slightly smaller inline size and pill background using a subtle surface token.
- **Headings**: Negative letter-spacing on large titles; section titles smaller and bold; subtitles use muted gray token.

### 4. Layout rhythm

- **Page container**: `max-width` ~1000–1200px, horizontal padding ~24px, vertical section spacing ~56px.
- **Nav**: Sticky top, bottom border, semi-transparent background + `backdrop-filter: blur` for a light glass effect; high `z-index` so content scrolls under it.
- **Grids**: `repeat(auto-fill, minmax(280px, 1fr))` (or similar) for card grids; consistent gap (~16px).

### 5. Components (patterns to reuse)

| Pattern        | UX intent |
|----------------|-----------|
| **Primary button** | Filled neutral (or brand) surface, light text; hover darkens slightly + shadow + tiny lift. |
| **Outline button** | Surface background, hairline border; hover darkens border and adds light shadow. |
| **Card** | Border + radius; hover strengthens border and shadow — feedback without clutter. |
| **Hero** | Centered column, badge optional, one H1, one short paragraph, CTA row with wrap. |
| **Page header** | For inner pages: breadcrumb, H1, one-line description — distinct from marketing hero. |

### 6. Focus and keyboard

- Do not remove outlines without replacement. Prefer `:focus-visible` with a ring or offset outline using token colors.
- Interactive cards that wrap links: keep a single focusable target or use careful nested markup so keyboard users are not trapped.

### 7. Reduced motion

Wrap non-essential transitions in:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

(Adjust if the project already has a more granular policy.)

## Agent workflow checklist

When implementing or editing UI:

1. **Tokens first** — Add or adjust variables before hard-coding colors in selectors.
2. **Dark parity** — Every new surface/border/text rule has a dark (and `prefers-color-scheme`) counterpart if the site supports dark mode.
3. **One source of spacing** — Prefer shared padding on `.container`, `.section`, and card classes over per-element magic numbers.
4. **Contrast check** — Muted text on muted backgrounds is a common failure; use a darker gray token for small text if needed.
5. **Semantic HTML** — `nav`, `main`, `section`, heading levels in order; buttons for actions, anchors for navigation.

## Where to install the skill (Cursor)

Cursor loads skills from `.cursor/skills/<skill-name>/SKILL.md`. Put this folder
there (create `.cursor/skills/` if needed). Reload the editor window if the skill
does not appear immediately.

Optional companion file in the **same folder** as `SKILL.md`:

```text
.cursor/skills/css-minimal-product-ux/SKILL.md
.cursor/skills/css-minimal-product-ux/tokens-starter.css
```

Import `tokens-starter.css` into your app’s styles only if you want the starter
tokens; extend variables for your brand (one accent color is often enough).

For other assistants or tools, place `SKILL.md` (and optional companion assets)
where that tool expects skills; the rules in the body stay the same.

## Companion file

- `tokens-starter.css` — Minimal `:root` token set and dark-mode scaffolding you
  can paste and rename. It is a **starting point**, not a full design system.

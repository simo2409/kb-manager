/**
 * Design System v2 — Theme toggle
 * Aggiunge/rimuove la classe .ds-theme-light sull'<html>
 * e salva la preferenza in localStorage.
 */
(function () {
  const STORAGE_KEY = 'ds-theme';
  const LIGHT_CLASS = 'ds-theme-light';
  const html = document.documentElement;
  const media = window.matchMedia('(prefers-color-scheme: light)');

  function applyTheme(theme) {
    const isLight = theme === 'light';
    html.classList.toggle(LIGHT_CLASS, isLight);
    const toggle = document.getElementById('ds-theme-toggle');
    if (toggle) {
      toggle.checked = isLight;
      toggle.setAttribute('aria-checked', String(isLight));
      toggle.setAttribute('aria-label', isLight ? 'Switch to dark theme' : 'Switch to light theme');
      const label = toggle.closest('label')?.querySelector('.ds-small');
      if (label) label.textContent = isLight ? 'Dark' : 'Light';
    }
  }

  function getStoredTheme() {
    try {
      return localStorage.getItem(STORAGE_KEY);
    } catch (e) {
      return null;
    }
  }

  function resolveTheme() {
    const stored = getStoredTheme();
    if (stored === 'light' || stored === 'dark') {
      return stored;
    }
    return media.matches ? 'light' : 'dark';
  }

  applyTheme(resolveTheme());

  media.addEventListener('change', function () {
    if (getStoredTheme() === null) {
      applyTheme(media.matches ? 'light' : 'dark');
    }
  });

  document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.getElementById('ds-theme-toggle');
    if (!toggle) return;

    applyTheme(resolveTheme());

    toggle.addEventListener('change', function () {
      const theme = toggle.checked ? 'light' : 'dark';
      try {
        localStorage.setItem(STORAGE_KEY, theme);
      } catch (e) {
        // Ignore private-browsing restrictions.
      }
      applyTheme(theme);
    });
  });

  // Mobile navigation toggle
  document.addEventListener('DOMContentLoaded', function () {
    const hamburger = document.getElementById('ds-hamburger');
    const mobileNav = document.getElementById('ds-mobile-nav');
    const mobileClose = document.getElementById('ds-mobile-close');
    if (!hamburger || !mobileNav) return;

    function openMenu() {
      mobileNav.hidden = false;
      hamburger.setAttribute('aria-expanded', 'true');
      if (mobileClose) mobileClose.focus();
      document.addEventListener('keydown', handleEscape);
    }

    function closeMenu() {
      mobileNav.hidden = true;
      hamburger.setAttribute('aria-expanded', 'false');
      hamburger.focus();
      document.removeEventListener('keydown', handleEscape);
    }

    function handleEscape(e) {
      if (e.key === 'Escape') closeMenu();
    }

    hamburger.addEventListener('click', openMenu);
    if (mobileClose) mobileClose.addEventListener('click', closeMenu);
  });
})();

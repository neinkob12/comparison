// Eigene SVG-Icons im CR-Stil: Elixiertropfen, Krone. Einbinden mit <span data-icon="elixir" data-n="4">
const ICONS = {
  elixir: n => `<svg viewBox="0 0 120 140"><defs><radialGradient id="e" cx="40%" cy="55%" r="65%"><stop offset="0" stop-color="#ff9cf5"/><stop offset=".55" stop-color="#e23fd6"/><stop offset="1" stop-color="#8a148a"/></radialGradient></defs><path d="M60 6 C60 6 12 62 12 92 a48 44 0 0 0 96 0 C108 62 60 6 60 6Z" fill="url(#e)" stroke="#0b1020" stroke-width="8"/><ellipse cx="40" cy="80" rx="10" ry="18" fill="#fff" opacity=".55"/></svg>`,
  crownR: () => `<svg viewBox="0 0 100 80"><path d="M8 70 L14 20 L34 42 L50 8 L66 42 L86 20 L92 70Z" fill="#ff4d5e" stroke="#0b1020" stroke-width="7" stroke-linejoin="round"/><rect x="8" y="62" width="84" height="12" rx="4" fill="#c81d36" stroke="#0b1020" stroke-width="6"/></svg>`,
  crownB: () => `<svg viewBox="0 0 100 80"><path d="M8 70 L14 20 L34 42 L50 8 L66 42 L86 20 L92 70Z" fill="#4da3ff" stroke="#0b1020" stroke-width="7" stroke-linejoin="round"/><rect x="8" y="62" width="84" height="12" rx="4" fill="#1c5fd6" stroke="#0b1020" stroke-width="6"/></svg>`,
  crownG: () => `<svg viewBox="0 0 100 80"><path d="M8 70 L14 20 L34 42 L50 8 L66 42 L86 20 L92 70Z" fill="#ffd23f" stroke="#0b1020" stroke-width="7" stroke-linejoin="round"/><rect x="8" y="62" width="84" height="12" rx="4" fill="#e09a00" stroke="#0b1020" stroke-width="6"/></svg>`,
};
document.querySelectorAll('[data-icon]').forEach(el => {
  const k = el.dataset.icon;
  if (k === 'elixir') { el.classList.add('elixir', 't'); el.innerHTML = ICONS.elixir() + `<span>${el.dataset.n}</span>`; }
  else el.innerHTML = ICONS[k]();
});

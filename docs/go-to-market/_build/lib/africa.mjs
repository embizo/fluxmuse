// Africa tile-grid cartogram data shared by the coverage map, status matrix and market-entry graphics.
// [iso, name, col, row]. The 23 tiles are the countries our payment partners, banks and mobile money wallets
// can reach once each market opens, NOT live coverage. Status 2026-10-11 (CURRENT_OFFER.md §3): only South Africa
// is open for paid sign-up (card and EFT). Which partner covers which country is internal (00_FACTS §3); never print it.
// A '*' after a name = payouts only. SOON = coming soon (no payment partner covers them yet).
export const COUNTRIES = [
  ['SN', 'Senegal', 0, 0], ['BF', 'Burkina Faso', 2, 0], ['SS', 'South Sudan*', 7, 0], ['ET', 'Ethiopia', 8, 0],
  ['SL', 'Sierra Leone', 0, 1], ['CI', "Côte d'Ivoire", 1, 1], ['GH', 'Ghana', 2, 1], ['BJ', 'Benin', 3, 1], ['NG', 'Nigeria', 4, 1], ['CM', 'Cameroon', 5, 1], ['UG', 'Uganda', 7, 1], ['KE', 'Kenya', 8, 1],
  ['GA', 'Gabon', 4, 2], ['CG', 'Rep. of the Congo', 5, 2], ['CD', 'DR Congo', 6, 2], ['RW', 'Rwanda', 7, 2], ['TZ', 'Tanzania', 8, 2],
  ['ZM', 'Zambia', 6, 3], ['MW', 'Malawi', 7, 3], ['MZ', 'Mozambique', 8, 3],
  ['ZW', 'Zimbabwe*', 7, 4],
  ['ZA', 'South Africa', 6, 5], ['LS', 'Lesotho', 7, 5],
];
// Coming soon: no payment partner covers them yet (facts §3). NA north-west of ZA, BW directly north of ZA.
export const SOON = [['NA', 'Namibia', 5, 4], ['BW', 'Botswana', 6, 4]];

// Billing currency once a market opens (facts §2): ZAR live; NGN/KES/GHS and USD priced, not yet on sale.
export const billingOf = (iso) => ({ ZA: 'ZAR', NG: 'NGN', KE: 'KES', GH: 'GHS' }[iso] || 'USD');
// Sales status: 'live' (paid sign-up open), 'priced' (local prices set, not on sale), 'pending' (partner coverage, not open yet).
export const statusOf = (iso) => (iso === 'ZA' ? 'live' : ['NG', 'KE', 'GH'].includes(iso) ? 'priced' : 'pending');

// Small tile-grid motif. hi(iso) -> 'on' | 'soft' | 'soon' | 'off'
export function miniMap({ ts = 26, tg = 4, dark = false, hi, orange = '#FF6A00' }) {
  const all = [...COUNTRIES.map((c) => [c[0], c[2], c[3], false]), ...SOON.map((c) => [c[0], c[2], c[3], true])];
  const W = 9 * (ts + tg) - tg, H = 6 * (ts + tg) - tg;
  const off = dark ? '#26313C' : '#E3E6EA', soft = dark ? '#5A3A22' : '#FFD9BA', dash = dark ? '#8A96A3' : '#8A949E';
  return `<div style="position:relative;width:${W}px;height:${H}px">${all.map(([iso, c, r, soon]) => {
    const st = hi(iso, soon);
    const style = st === 'on' ? `background:${orange}` : st === 'soft' ? `background:${soft}` : st === 'soon' ? `border:2px dashed ${dash}` : `background:${off}`;
    return `<span style="position:absolute;left:${c * (ts + tg)}px;top:${r * (ts + tg)}px;width:${ts}px;height:${ts}px;border-radius:${Math.round(ts / 4)}px;box-sizing:border-box;${style}"></span>`;
  }).join('')}</div>`;
}

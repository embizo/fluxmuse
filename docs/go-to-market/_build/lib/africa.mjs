// Africa tile-grid cartogram data shared by the coverage map, rails matrix and market-entry graphics.
// [iso, name, col, row, rails]. Rails ending in '*' = payouts only. soon = coming soon (no rail yet).
export const COUNTRIES = [
  ['SN', 'Senegal', 0, 0, ['pawaPay', 'Fincra']], ['BF', 'Burkina Faso', 2, 0, ['pawaPay', 'Fincra']], ['SS', 'South Sudan*', 7, 0, ['Fincra*']], ['ET', 'Ethiopia', 8, 0, ['pawaPay']],
  ['SL', 'Sierra Leone', 0, 1, ['pawaPay']], ['CI', "Côte d'Ivoire", 1, 1, ['Paystack', 'pawaPay', 'Fincra']], ['GH', 'Ghana', 2, 1, ['Paystack', 'pawaPay', 'Fincra']], ['BJ', 'Benin', 3, 1, ['pawaPay', 'Fincra']], ['NG', 'Nigeria', 4, 1, ['Paystack', 'pawaPay', 'Fincra']], ['CM', 'Cameroon', 5, 1, ['pawaPay', 'Fincra']], ['UG', 'Uganda', 7, 1, ['pawaPay', 'Fincra']], ['KE', 'Kenya', 8, 1, ['Paystack', 'pawaPay', 'Fincra']],
  ['GA', 'Gabon', 4, 2, ['pawaPay', 'Fincra']], ['CG', 'Rep. of the Congo', 5, 2, ['pawaPay', 'Fincra']], ['CD', 'DR Congo', 6, 2, ['pawaPay', 'Fincra']], ['RW', 'Rwanda', 7, 2, ['Paystack', 'pawaPay', 'Fincra']], ['TZ', 'Tanzania', 8, 2, ['pawaPay', 'Fincra']],
  ['ZM', 'Zambia', 6, 3, ['pawaPay', 'Fincra']], ['MW', 'Malawi', 7, 3, ['pawaPay']], ['MZ', 'Mozambique', 8, 3, ['pawaPay']],
  ['ZW', 'Zimbabwe*', 7, 4, ['Fincra*']],
  ['ZA', 'South Africa', 6, 5, ['Yoco', 'Ozow', 'Paystack', 'Fincra']], ['LS', 'Lesotho', 7, 5, ['pawaPay']],
];
// Coming soon: no secured rail covers them yet (facts §3). NA north-west of ZA, BW directly north of ZA.
export const SOON = [['NA', 'Namibia', 5, 4], ['BW', 'Botswana', 6, 4]];

// Billing currency per rail-covered country (facts §2): ZAR, local NGN/KES/GHS, USD for the other 19.
export const billingOf = (iso) => ({ ZA: 'ZAR', NG: 'NGN', KE: 'KES', GH: 'GHS' }[iso] || 'USD');

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

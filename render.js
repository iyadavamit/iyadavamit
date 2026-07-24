// Render dark_mode.svg -> dark_mode.png (crisp 2x). Font is deterministic in CI.
const { Resvg } = require('@resvg/resvg-js');
const fs = require('fs');
const svg = fs.readFileSync('dark_mode.svg', 'utf8');
const r = new Resvg(svg, {
  fitTo: { mode: 'width', value: 1800 },
  font: { loadSystemFonts: true, defaultFontFamily: process.env.CARD_FONT || 'DejaVu Sans Mono' },
});
fs.writeFileSync('dark_mode.png', r.render().asPng());
console.log('rendered dark_mode.png');

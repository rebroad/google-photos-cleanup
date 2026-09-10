(function (root) {
  const lines = {
    welcome: "Right. I shall provide the commentary. You provide the questionable angles.",
    down: "Charming. I know when I’m not wanted.",
    breathe: "Can I come up to breathe soon?",
    air: "Ah. Air. A much underrated feature.",
    flat1: "Making myself comfortable, am I?",
    flat2: "A little lie-down. Excellent career move.",
    flat3: "Horizontal thinking. I approve.",
    upright1: "Ah, upright again. A triumph of civilisation.",
    upright2: "There we are. Looking terribly productive.",
    upright3: "At attention. Shall I salute?",
    side1: "Taking a sideways view of things?",
    side2: "A change of perspective. How refreshing.",
    side3: "Does this angle make my pixels look big?",
    shake1: "Steady on. I'm doing my best.",
    shake2: "I'm a phone, not a cocktail.",
    shake3: "The opinions are already quite well stirred."
  };
  if (typeof module === 'object' && module.exports) module.exports = lines;
  else root.CheekyLines = lines;
})(typeof globalThis === 'object' ? globalThis : this);

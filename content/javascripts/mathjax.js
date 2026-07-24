window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"], ["$", "$"]],
    displayMath: [["\\[", "\\]"], ["$$", "$$"]],
    processEscapes: true,
    packages: { "[+]": ["noerrors"] },
  },
  options: {
    ignoreHtmlClass: "^(?:code|pre)$",
  },
};

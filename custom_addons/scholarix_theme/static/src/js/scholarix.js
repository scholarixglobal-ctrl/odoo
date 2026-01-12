/** Scholarix UI helpers: logo sizing + minor tweaks */
const setLogoSize = () => {
  const logos = document.querySelectorAll('.sx-logo');
  const w = window.innerWidth;
  const size = w < 768 ? 40 : (w < 1024 ? 50 : 60);
  logos.forEach(el => { el.style.maxHeight = `${size}px`; });
};

window.addEventListener('resize', setLogoSize);
document.addEventListener('DOMContentLoaded', setLogoSize);

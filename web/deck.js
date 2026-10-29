const slides = [...document.querySelectorAll('.slide')];
const jump = document.querySelector('#jump');
let current = 0;
function go(i) {
  i = Math.max(0, Math.min(slides.length - 1, i));
  slides[i].scrollIntoView({block: 'start'});
}
jump.addEventListener('change', () => go(Number(jump.value)));
document.querySelector('#prev').addEventListener('click', () => go(current - 1));
document.querySelector('#next').addEventListener('click', () => go(current + 1));
document.querySelector('#fullscreen').addEventListener('click', async () => {
  if (document.fullscreenElement) await document.exitFullscreen();
  else await document.documentElement.requestFullscreen();
});
document.addEventListener('keydown', event => {
  if (event.altKey || event.ctrlKey || event.metaKey || /INPUT|TEXTAREA|SELECT|BUTTON|IFRAME/.test(event.target.tagName) || event.target.isContentEditable) return;
  const moves = {ArrowDown: 1, ArrowRight: 1, PageDown: 1, ' ': event.shiftKey ? -1 : 1, ArrowUp: -1, ArrowLeft: -1, PageUp: -1};
  if (event.key in moves) {event.preventDefault(); go(current + moves[event.key]);}
  if (event.key === 'Home') {event.preventDefault(); go(0);}
  if (event.key === 'End') {event.preventDefault(); go(slides.length - 1);}
});
const observer = new IntersectionObserver(entries => {
  for (const entry of entries) if (entry.isIntersecting && entry.intersectionRatio >= 0.55) {
    current = slides.indexOf(entry.target);
    jump.value = String(current);
    history.replaceState(null, '', '#' + entry.target.id);
  }
}, {threshold: [0.55]});
slides.forEach(slide => observer.observe(slide));
const start = slides.findIndex(slide => '#' + slide.id === location.hash);
if (start >= 0) requestAnimationFrame(() => go(start));

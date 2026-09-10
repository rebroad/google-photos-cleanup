(() => {
  'use strict';
  const { Surface, Renderer, clamp } = CheekyWater, $ = id => document.getElementById(id);
  const surface = new Surface(), renderer = new Renderer($('water'), surface);
  surface.tilt(0, 1);
  for (let i = 0; i < 480; i++) surface.step(1 / 120);
  const preference = matchMedia('(prefers-reduced-motion: reduce)');
  let running = false, frame = 0, last = 0, accumulator = 0, time = 0, target = 0, manual = false, expensive = 0;
  let pointer = null, lastTouch = 0, lastDraw = 0;
  function tick(now) {
    frame = 0;
    if (document.hidden || !running) return;
    const elapsed = Math.min(last ? (now - last) / 1000 : 1 / 60, .05); last = now; time += elapsed;
    accumulator += elapsed;
    while (accumulator >= 1 / 120) { surface.step(1 / 120, preference.matches); accumulator -= 1 / 120; }
    if (now - lastDraw >= (renderer.low || preference.matches ? 32 : 15)) {
      const began = performance.now(); renderer.draw(time, target, preference.matches, (now - (lastDraw || now - 16)) / 1000); lastDraw = now;
      expensive = performance.now() - began > 12 ? expensive + 1 : Math.max(0, expensive - 1);
      if (expensive > 60 && !renderer.low) { renderer.low = true; renderer.resize(); }
    }
    frame = requestAnimationFrame(tick);
  }
  function start() { running = true; last = lastDraw = 0; if (!frame && !document.hidden) frame = requestAnimationFrame(tick); }
  function pause() { running = false; cancelAnimationFrame(frame); frame = 0; last = 0; accumulator = 0; }
  function draw() { renderer.draw(time, target, preference.matches, 0); }
  const scene = window.cheekyScene = {
    surface, renderer, start, pause, draw,
    get manual() { return manual; },
    gravity(g) { if (!manual) surface.tilt(g.x, g.y); },
    acceleration(a) { if (!manual) surface.accelerate(a.x, a.y, preference.matches); },
    underwater(down, preview = false) {
      target = down ? 1 : 0;
      document.body.classList.toggle('submerged', down);
      $('water-state').textContent = down ? (preview ? 'UNDERWATER · PREVIEW' : 'UNDERWATER') : 'BACK IN THE BOWL';
      $('scene-caption').textContent = down ? 'An unexpectedly immersive experience.' : 'Air restored. Bowl discreetly refilled.';
    },
    reset() { target = 0; renderer.under = 0; surface.reset(Number($('level').value) / 100); scene.underwater(false); draw(); },
    useSensors() { manual = false; $('tilt-x').value = $('tilt-y').value = '0'; surface.tilt(0, 0); $('input-state').textContent = 'PHONE MOTION'; },
    get running() { return running; },
    get calm() { return preference.matches; }
  };
  function tilt() {
    manual = true; surface.tilt(Math.sin(Number($('tilt-x').value) * Math.PI / 180), Math.sin(Number($('tilt-y').value) * Math.PI / 180));
    $('input-state').textContent = 'SIMULATED TILT';
    if (!running) { for (let i = 0; i < 180; i++) surface.step(1 / 120, preference.matches); draw(); }
  }
  ['tilt-x', 'tilt-y'].forEach(id => $(id).addEventListener('input', tilt));
  $('sensors').addEventListener('click', () => scene.useSensors());
  $('level').addEventListener('input', () => { surface.level = Number($('level').value) / 100; $('level-readout').value = $('level').value; if (!running) { surface.reset(); draw(); } });
  $('water').addEventListener('pointerdown', e => { pointer = e.pointerId; $('water').setPointerCapture(pointer); disturb(e); });
  $('water').addEventListener('pointermove', e => { if (pointer === e.pointerId && performance.now() - lastTouch > 35) disturb(e); });
  function disturb(e) {
    lastTouch = performance.now(); const r = $('water').getBoundingClientRect();
    surface.disturb(clamp((e.clientX - r.left) / r.width, 0, 1), clamp((e.clientY - r.top) / r.height, 0, 1), preference.matches ? .25 : 1.15);
    window.dispatchEvent(new CustomEvent('cheeky-splash'));
    if (!running) { for (let i = 0; i < 12; i++) surface.step(1 / 120, preference.matches); draw(); }
  }
  ['pointerup','pointercancel','lostpointercapture'].forEach(event => $('water').addEventListener(event, () => { pointer = null; }));
  $('water').addEventListener('keydown', e => {
    const key = { ArrowLeft: ['tilt-x', -8], ArrowRight: ['tilt-x', 8], ArrowUp: ['tilt-y', -8], ArrowDown: ['tilt-y', 8] }[e.key];
    if (key) { e.preventDefault(); $(key[0]).value = Number($(key[0]).value) + key[1]; tilt(); }
    else if (e.key === ' ') { e.preventDefault(); surface.disturb(.5, .5, preference.matches ? .3 : 1.3); }
  });
  new ResizeObserver(() => { renderer.resize(); draw(); }).observe($('water'));
  preference.addEventListener('change', draw);
  draw();
})();

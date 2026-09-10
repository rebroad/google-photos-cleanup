(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.CheekyWater = api;
})(typeof globalThis === 'object' ? globalThis : this, () => {
  'use strict';
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const radians = degrees => degrees * Math.PI / 180;
  // Device axes are fixed to the natural screen. Screen angle is counterclockwise.
  function screenVector(x, y, angle = 0) {
    const c = Math.cos(radians(angle)), s = Math.sin(radians(angle));
    return { x: x * c + y * s, y: -x * s + y * c };
  }
  function gravity(beta, gamma, angle = 0) {
    const b = radians(beta), g = radians(gamma);
    return { ...screenVector(Math.cos(b) * Math.sin(g), Math.sin(b), angle), z: Math.cos(b) * Math.cos(g) };
  }
  class PoseGate {
    constructor() { this.reset(); this.lastLine = -Infinity; }
    reset() { this.down = false; this.since = null; }
    observe(z, now) {
      if (!Number.isFinite(z)) return null;
      const crossing = this.down ? z > -0.30 : z < -0.65;
      if (!crossing) { this.since = null; return null; }
      if (this.since === null) this.since = now;
      return this.tick(now);
    }
    tick(now) {
      // Orientation is a position event; browsers may emit nothing while held still.
      if (this.since === null) return null;
      if (now - this.since < (this.down ? 300 : 1100)) return null;
      this.down = !this.down; this.since = null;
      return this.down ? 'down' : 'up';
    }
    allowLine(now) {
      if (now - this.lastLine < 12000) return false;
      this.lastLine = now; return true;
    }
  }
  class Surface {
    constructor(nx = 37, ny = 21) {
      this.nx = nx; this.ny = ny;
      this.h = new Float64Array(nx * ny); this.v = new Float64Array(nx * ny);
      this.next = new Float64Array(nx * ny); this.level = .55;
      this.gx = 0; this.gy = 0; this.reset();
    }
    reset(level = this.level) { this.level = clamp(level, .15, .85); this.h.fill(this.level); this.v.fill(0); }
    tilt(x, y) { this.gx = clamp(x, -1, 1); this.gy = clamp(y, -1, 1); }
    disturb(x, y, strength = .6) {
      const { nx, ny, v } = this;
      for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
        const d = ((i / (nx - 1) - x) ** 2 + (j / (ny - 1) - y) ** 2) / .008;
        v[j * nx + i] += clamp(strength, -1.8, 1.8) * (1 - d) * Math.exp(-d);
      }
    }
    accelerate(x, y, calm = false) {
      const strength = calm ? .014 : .05;
      for (let j = 0; j < this.ny; j++) for (let i = 0; i < this.nx; i++) {
        this.v[j * this.nx + i] += strength * (clamp(x, -12, 12) * (i / (this.nx - 1) - .5) + clamp(y, -12, 12) * (j / (this.ny - 1) - .5));
      }
    }
    step(dt, calm = false) {
      const { nx, ny, h, v, next } = this;
      dt = clamp(dt, 0, 1 / 90);
      if (!dt) return;
      const damping = calm ? 4.2 : 1.7;
      for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
        const k = j * nx + i;
        const lap = h[j * nx + Math.max(i - 1, 0)] + h[j * nx + Math.min(i + 1, nx - 1)] + h[Math.max(j - 1, 0) * nx + i] + h[Math.min(j + 1, ny - 1) * nx + i] - 4 * h[k];
        const target = this.level + 6.5 * this.gx * (i / (nx - 1) - .5) + 6.5 * this.gy * (j / (ny - 1) - .5);
        v[k] = clamp(v[k] + (220 * lap + 19 * (target - h[k]) - damping * v[k]) * dt, -2.8, 2.8);
        next[k] = h[k] + v[k] * dt;
      }
      // Project onto a bounded, volume-conserving height field. No hidden water creation on tilt.
      let low = -2, high = 2;
      for (let n = 0; n < 24; n++) {
        const shift = (low + high) / 2;
        let total = 0;
        for (const value of next) total += clamp(value + shift, .018, .975);
        if (total / next.length > this.level) high = shift; else low = shift;
      }
      const shift = (low + high) / 2;
      let meanV = 0;
      for (let k = 0; k < h.length; k++) {
        const projected = clamp(next[k] + shift, .018, .975);
        // A blocked column cannot keep accumulating momentum against the glass.
        v[k] = clamp((projected - h[k]) / dt, -2.8, 2.8);
        h[k] = projected;
        meanV += v[k];
      }
      meanV /= h.length;
      for (let k = 0; k < v.length; k++) v[k] -= meanV;
    }
    sample(x, y) { return this.h[Math.round(clamp(y, 0, 1) * (this.ny - 1)) * this.nx + Math.round(clamp(x, 0, 1) * (this.nx - 1))]; }
    energy() { return this.v.reduce((sum, v) => sum + v * v, 0) / this.v.length; }
  }
  class Renderer {
    constructor(canvas, surface) {
      this.canvas = canvas; this.ctx = canvas.getContext('2d', { alpha: false }); this.surface = surface;
      this.under = 0; this.low = (globalThis.navigator?.hardwareConcurrency || 8) <= 4;
      this.bubbles = Array.from({ length: 26 }, (_, i) => ({ x: ((i * 47) % 97) / 97, y: ((i * 31) % 89) / 89, r: 2 + i % 5 }));
      this.resize();
    }
    resize() {
      const rect = this.canvas.getBoundingClientRect(); this.w = rect.width; this.h = rect.height;
      const scale = Math.min(globalThis.devicePixelRatio || 1, this.low ? 1 : 1.5);
      this.canvas.width = Math.round(this.w * scale); this.canvas.height = Math.round(this.h * scale);
      this.ctx.setTransform(scale, 0, 0, scale, 0, 0);
    }
    point(x, y) { return [14 + x * (this.w - 28), 14 + y * (this.h - 28)]; }
    path(points, fill, stroke, width = 1) {
      if (!points.length) return;
      const c = this.ctx; c.beginPath(); points.forEach((p, i) => i ? c.lineTo(...p) : c.moveTo(...p)); c.closePath();
      if (fill) { c.fillStyle = fill; c.fill(); }
      if (stroke) { c.strokeStyle = stroke; c.lineWidth = width; c.stroke(); }
    }
    draw(time, target, calm = false, dt = 1 / 60) {
      if (!this.ctx || !this.w) return;
      const c = this.ctx, w = this.w, h = this.h, s = this.surface;
      this.under += (target - this.under) * (1 - Math.exp(-dt * (target ? 2.1 : 1.8)));
      if (Math.abs(this.under - target) < .001) this.under = target;
      const u = this.under, p = (x, y) => this.point(x, y);
      const bg = c.createLinearGradient(0, 0, w, h); bg.addColorStop(0, '#102b2d'); bg.addColorStop(.5, '#0b2327'); bg.addColorStop(1, '#041219');
      c.fillStyle = bg; c.fillRect(0, 0, w, h);
      const halo = c.createRadialGradient(w * .25, h * .35, 0, w * .25, h * .35, w * .85);
      halo.addColorStop(0, '#43857922'); halo.addColorStop(1, '#07161900'); c.fillStyle = halo; c.fillRect(0, 0, w, h);
      c.save(); c.beginPath(); c.roundRect(13, 13, w - 26, h - 26, 17); c.clip();
      // Top-down view: the glass reservoir is the screen, with a visible dry floor when tilted.
      for (let i = 1; i < 9; i++) {
        c.beginPath(); c.moveTo(w * i / 9, 0); c.lineTo(w * i / 9, h); c.strokeStyle = '#d3eecc05'; c.lineWidth = 1; c.stroke();
      }
      c.save();
      const spill = clamp(1 - u * 2.9, 0, 1);
      c.globalAlpha = clamp(1 - u * 1.6, 0, 1);
      if (!calm && u > 0) { c.translate(w / 2, h); c.transform(1, u * .35, u * .3, 1 - u * .55, 0, u * h * .3); c.translate(-w / 2, -h); }
      const stride = this.low ? 2 : 1, edge = .025;
      const waterMask = new Path2D(); const contours = [];
      for (let j = 0; j < s.ny - 1; j += stride) for (let i = 0; i < s.nx - 1; i += stride) {
        const i2 = Math.min(i + stride, s.nx - 1), j2 = Math.min(j + stride, s.ny - 1);
        const corners = [[i, j], [i2, j], [i2, j2], [i, j2]].map(([a, b]) => ({ x: a / (s.nx - 1), y: b / (s.ny - 1), z: s.h[b * s.nx + a] * spill }));
        const polygon = [], crossings = [];
        for (let k = 0; k < 4; k++) {
          const a = corners[k], b = corners[(k + 1) % 4];
          if (a.z > edge) polygon.push(p(a.x, a.y));
          if ((a.z > edge) !== (b.z > edge)) {
            const f = (edge - a.z) / (b.z - a.z), cross = p(a.x + (b.x - a.x) * f, a.y + (b.y - a.y) * f);
            polygon.push(cross); crossings.push(cross);
          }
        }
        if (polygon.length < 3) continue;
        const depth = corners.reduce((sum, a) => sum + a.z, 0) / 4;
        const dx = (corners[1].z - corners[0].z) * (s.nx - 1) / stride, dy = (corners[3].z - corners[0].z) * (s.ny - 1) / stride;
        const normal = Math.sqrt(dx * dx + dy * dy + 1);
        const glint = Math.pow(Math.max(0, (-dx * .34 - dy * .23 + .91) / normal), 24) * 25;
        const shade = clamp(39 - depth * 17 + (dx - dy) * 9 + glint, 16, 66);
        const color = `hsl(${180 + depth * 12},${58 + depth * 12}%,${shade}%)`;
        this.path(polygon, color, color, .7);
        polygon.forEach((point, k) => k ? waterMask.lineTo(...point) : waterMask.moveTo(...point)); waterMask.closePath();
        if (crossings.length > 1) contours.push(crossings);
      }
      c.save(); c.clip(waterMask);
      const depthLight = c.createRadialGradient(w * .18, h * .25, 0, w * .18, h * .25, Math.max(w, h));
      depthLight.addColorStop(0, '#adfff04a'); depthLight.addColorStop(.4, '#4adbdd12'); depthLight.addColorStop(1, '#00142435'); c.fillStyle = depthLight; c.fillRect(0, 0, w, h);
      // Caustics and reflected window light refract through the actual surface normals.
      for (let k = 0; k < 17; k++) {
        c.beginPath(); const band = k / 16;
        for (let i = 0; i <= 64; i++) {
          const x = i / 64, z = s.sample(x, band), phase = calm ? 0 : time * .28;
          const y = band + Math.sin(x * 17 + band * 22 + phase) * .017 + Math.sin(x * 7 - band * 13 - phase) * .013 + (z - s.level) * .05;
          const q = p(x, y); i ? c.lineTo(...q) : c.moveTo(...q);
        }
        c.strokeStyle = k % 3 ? '#b9fff01a' : '#d4fff02b'; c.lineWidth = k % 3 ? 1 : 1.6; c.stroke();
      }
      for (const band of [.18, .22, .83]) {
        const left = [], right = [];
        for (let k = 0; k <= 35; k++) {
          const y = k / 35, wave = (s.sample(band + .025, y) - s.sample(band - .025, y)) * .35;
          left.push(p(band + wave + y * .08, y)); right.push(p(band + wave + y * .08 + (band === .22 ? .008 : .025), y));
        }
        this.path([...left, ...right.reverse()], band === .22 ? '#e3fff31a' : '#e3fff30b');
      }
      for (const b of this.bubbles.slice(0, calm ? 5 : 16)) {
        const phase = (b.y + time * (calm ? .008 : .023)) % 1;
        const pos = p(b.x, .1 + b.y * .8);
        c.beginPath(); c.arc(...pos, b.r * (.3 + phase), 0, Math.PI * 2); c.strokeStyle = `rgba(205,255,249,${.32 * Math.sin(phase * Math.PI)})`; c.lineWidth = .8; c.stroke();
      }
      c.restore();
      for (const points of contours) {
        c.beginPath(); c.moveTo(...points[0]); c.lineTo(...points[1]); c.strokeStyle = '#cdfff499'; c.lineWidth = 2.3; c.stroke();
        if (points.length === 4) { c.beginPath(); c.moveTo(...points[2]); c.lineTo(...points[3]); c.stroke(); }
      }
      c.restore();
      // Thin glass bevel, looking straight down. No detached aquarium or floating blue plane.
      c.strokeStyle = '#c1f6e157'; c.lineWidth = 2; c.strokeRect(14, 14, w - 28, h - 28);
      c.restore();
      const rim = c.createLinearGradient(0, 0, w, h); rim.addColorStop(0, '#e0fff0a6'); rim.addColorStop(.25, '#8acab933'); rim.addColorStop(.6, '#639ba921'); rim.addColorStop(1, '#baffeb88');
      c.beginPath(); c.roundRect(8, 8, w - 16, h - 16, 21); c.strokeStyle = rim; c.lineWidth = 3; c.stroke();
      c.beginPath(); c.roundRect(13, 13, w - 26, h - 26, 17); c.strokeStyle = '#02141799'; c.lineWidth = 4; c.stroke();
      if (u > .005) {
        const crest = h * (1.11 - u * 1.23);
        c.save(); c.beginPath(); c.moveTo(0, h);
        for (let x = 0; x <= w + 8; x += 8) c.lineTo(x, crest + Math.sin(x / w * 10 + time * (calm ? .2 : 2.4)) * (calm ? 3 : 18) * Math.sin(Math.PI * u));
        c.lineTo(w, h); c.closePath(); c.clip();
        const ocean = c.createLinearGradient(0, 0, 0, h); ocean.addColorStop(0, '#327f87'); ocean.addColorStop(.35, '#0c687b'); ocean.addColorStop(1, '#032e49'); c.fillStyle = ocean; c.fillRect(0, 0, w, h);
        for (let i = 0; i < 6; i++) {
          const x = w * (i - 1) / 4 + Math.sin(time * .22 + i) * (calm ? 0 : 12);
          this.path([[x, 0], [x + w * .06, 0], [x + w * .4, h], [x + w * .16, h]], '#befce80c');
        }
        for (const b of this.bubbles.slice(0, calm ? 7 : 26)) {
          const x = b.x * w + Math.sin(time + b.y * 30) * (calm ? 1 : 9), y = h * (1 - (b.y + time * (calm ? .018 : .065)) % 1);
          c.beginPath(); c.ellipse(x, y, b.r * 1.2, b.r * 1.55, .15, 0, Math.PI * 2); c.strokeStyle = '#d1ffff63'; c.lineWidth = 1; c.stroke();
          c.beginPath(); c.arc(x - b.r * .35, y - b.r * .6, Math.max(.8, b.r * .17), 0, Math.PI * 2); c.fillStyle = '#e6fffbbc'; c.fill();
        }
        c.restore();
        if (crest > -10) { c.beginPath(); for (let x = 0; x <= w; x += 6) { const y = crest + Math.sin(x / w * 10 + time * (calm ? .2 : 2.4)) * (calm ? 3 : 18) * Math.sin(Math.PI * u); x ? c.lineTo(x, y) : c.moveTo(x, y); } c.strokeStyle = '#c5fffba0'; c.lineWidth = 3; c.stroke(); }
      }
    }
  }
  return { clamp, screenVector, gravity, PoseGate, Surface, Renderer };
});

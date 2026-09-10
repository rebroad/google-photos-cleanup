(() => {
  'use strict';
  const $ = id => document.getElementById(id), scene = window.cheekyScene;
  const { gravity, screenVector, PoseGate } = CheekyWater, gate = new PoseGate();
  const synth = window.speechSynthesis;
  const audio = new CheekyAudio(message => { $('voice-note').textContent = message; });
  const kinds = { flat: ['flat1','flat2','flat3'], upright: ['upright1','upright2','upright3'], side: ['side1','side2','side3'], shake: ['shake1','shake2','shake3'] };
  let active = false, generation = 0, sequence = 0, timer = null, down = false, preview = false;
  let started = 0, received = false, lastOrientation = -Infinity, lastMotion = 0, lastInput = -Infinity;
  let previousGravity = null, previousVector = null, candidate = '', candidateSince = 0, spokenPose = '';
  let lastSpoken = -Infinity, lastLine = '', breatheAt = null, voices = [], voiceChosen = false;
  let allowed = [false, false], lastShake = 0, lastUpright = -Infinity;
  const screenAngle = () => screen.orientation?.angle ?? (Number(window.orientation) || 0);
  const valid = value => value && ['x','y','z'].every(key => Number.isFinite(value[key]));
  function selectedVoice() { return voices.find(v => v.voiceURI === $('voice').value); }
  function recorded() {
    const voice = selectedVoice();
    return $('voice').value === 'recorded:george' || !!(voice?.localService && voice.lang === 'en-GB' && ['Microsoft George', 'Microsoft George - English (United Kingdom)'].includes(voice.name));
  }
  function voiceNote() {
    $('voice-note').textContent = recorded()
      ? 'George’s matching recordings: the same speaker above and below water. Underwater speech is muffled and gently warbling.'
      : 'This device voice stays unfiltered underwater, with quiet bubbles. Select George · recorded for muffled, warbling speech.';
  }
  function populateVoices() {
    const old = $('voice').value;
    voices = synth?.getVoices() || [];
    $('voice').replaceChildren(new Option('Device default', ''), new Option('George · recorded, underwater ready', 'recorded:george'));
    voices.forEach(v => $('voice').add(new Option(v.name + ' · ' + v.lang, v.voiceURI)));
    if (old === 'recorded:george' || voices.some(v => v.voiceURI === old) || (voiceChosen && old === '')) $('voice').value = old;
    else if (!voiceChosen) $('voice').value = voices.find(v => v.lang === 'en-GB' && v.localService)?.voiceURI || '';
    else { $('voice').value = ''; $('voice-note').textContent = 'Your chosen device voice is no longer available. Choose a voice to continue.'; return; }
    voiceNote();
  }
  function choose(kind) { const choices = kinds[kind].filter(id => id !== lastLine); return choices[Math.floor(Math.random() * choices.length)] || kinds[kind][0]; }
  function invalidate() { sequence++; breatheAt = null; audio.stop(); }
  function say(id, force = false, wet = down) {
    const now = performance.now();
    if (document.hidden || (!force && (audio.busy || down || now - lastSpoken < Number($('gap').value) * 1000))) return Promise.resolve(false);
    lastSpoken = now; lastLine = id;
    $('remark').textContent = '“' + CheekyLines[id] + '”';
    return audio.say(id, selectedVoice(), recorded(), wet);
  }
  function setSubmerged(value, isPreview = false, narrate = true) {
    if (down === value) return;
    invalidate(); down = value;
    scene.underwater(value, isPreview);
    $('preview').setAttribute('aria-pressed', String(preview));
    $('preview').textContent = preview ? 'Return to air' : 'Preview underwater';
    if (value) {
      $('pose').textContent = isPreview ? 'Underwater preview · keep the screen in view' : 'Screen facing down · reclining, perhaps?';
      $('status').textContent = isPreview ? 'On · underwater preview' : 'On · submerged';
      const ticket = sequence;
      if (narrate && gate.allowLine(performance.now())) {
        say('down', true, true).then(completed => {
          if (completed && ticket === sequence && active && down && !document.hidden) breatheAt = performance.now() + 5000;
        });
      }
      audio.ambient(true);
    } else {
      lastUpright = performance.now(); candidate = ''; spokenPose = '';
      $('pose').textContent = 'Back above water';
      $('status').textContent = 'On · water restored';
      if (narrate) say('air', true, false);
    }
  }
  function resetPose() {
    gate.reset(); candidate = ''; spokenPose = ''; previousGravity = previousVector = null;
    lastOrientation = lastInput = -Infinity; lastMotion = 0; candidateSince = performance.now();
  }
  function consider(vector, now) {
    received = true; lastInput = now;
    if (preview || scene.manual) return;
    const event = gate.observe(vector.z, now);
    if (event === 'down') setSubmerged(true);
    else if (event === 'up') setSubmerged(false);
    if (down) return;
    $('status').textContent = 'On · motion available';
    if (!scene.manual) $('input-state').textContent = 'PHONE MOTION';
    const kind = vector.z > .8 ? 'flat' : Math.abs(vector.x) > .65 ? 'side' : 'upright';
    $('pose').textContent = { flat: 'Screen facing up · taking it easy', upright: 'Phone upright', side: 'Phone tilted sideways' }[kind];
    if (candidate !== kind) { candidate = kind; candidateSince = now; return; }
    if (vector.z < -.3 || now - lastUpright < 4000) return;
    if (now - candidateSince >= 1800 && spokenPose !== kind && !audio.busy && now - lastSpoken >= Number($('gap').value) * 1000) {
      spokenPose = kind; say(choose(kind));
    }
  }
  function orientation(event) {
    if (!active || document.hidden || !Number.isFinite(event.beta) || !Number.isFinite(event.gamma)) return;
    const now = performance.now(), vector = gravity(event.beta, event.gamma, screenAngle()); lastOrientation = now;
    if (!preview) {
      scene.gravity(vector);
      if (previousVector) scene.acceleration({ x: (vector.x - previousVector.x) * 16, y: (vector.y - previousVector.y) * 16 });
      previousVector = vector;
    }
    consider(vector, now);
  }
  function motion(event) {
    if (!active || document.hidden) return;
    const now = performance.now(), delta = lastMotion ? Math.min((now - lastMotion) / 1000, .05) : 1 / 60; lastMotion = now;
    const a = event.acceleration, g = event.accelerationIncludingGravity;
    let acceleration = valid(a) ? a : null;
    if (valid(g)) {
      if (!acceleration && previousGravity) acceleration = { x: g.x - previousGravity.x, y: g.y - previousGravity.y, z: g.z - previousGravity.z };
      if (!previousGravity) previousGravity = { ...g };
      else ['x','y','z'].forEach(key => { previousGravity[key] += (g[key] - previousGravity[key]) * Math.min(1, delta * 4); });
      const norm = Math.hypot(g.x, g.y, g.z);
      if (now - lastOrientation > 1200 && norm > 5 && norm < 15) {
        const vector = { ...screenVector(-g.x / norm, g.y / norm, screenAngle()), z: g.z / norm };
        if (!preview) scene.gravity(vector);
        consider(vector, now);
      }
    }
    if (acceleration) {
      const vector = screenVector(-acceleration.x, acceleration.y, screenAngle());
      if (!preview) scene.acceleration({ x: vector.x * delta * 60, y: vector.y * delta * 60 });
      if (!down && Math.hypot(acceleration.x, acceleration.y, acceleration.z) > 12 && now - lastShake > 2500) { lastShake = now; say(choose('shake')); }
    }
  }
  function detach() { window.removeEventListener('deviceorientation', orientation); window.removeEventListener('devicemotion', motion); }
  function attach() { detach(); if (allowed[0]) window.addEventListener('deviceorientation', orientation); if (allowed[1]) window.addEventListener('devicemotion', motion); }
  function stop() {
    generation++; active = false; clearInterval(timer); timer = null; detach(); invalidate(); resetPose();
    down = preview = false; scene.pause(); scene.reset(); audio.suspend();
    $('start').disabled = false; $('stop').disabled = true; $('preview').disabled = true;
    $('preview').setAttribute('aria-pressed', 'false'); $('preview').textContent = 'Preview underwater';
    $('start').textContent = 'Start the commentary'; $('status').textContent = 'Off · commentary stopped';
    $('pose').textContent = 'Water still. Opinions temporarily suspended.';
    $('help').textContent = 'Stopped. Tap Start to play again. Sample comments and tilt controls are still available.';
  }
  function heartbeat() {
    if (!active || document.hidden) return;
    const now = performance.now();
    const sourcePresent = lastMotion > 0 ? now - lastMotion < 1500 || now - lastOrientation < 1500 : Number.isFinite(lastOrientation);
    if (!preview && !scene.manual) {
      if (!sourcePresent) gate.since = null;
      else {
        const event = gate.tick(now);
        if (event === 'down') setSubmerged(true);
        else if (event === 'up') setSubmerged(false);
      }
    }
    if (breatheAt !== null && now >= breatheAt) {
      breatheAt = null;
      if (down && (preview || sourcePresent)) say('breathe', true, true);
    }
    if (!received && now - started > 6000 && !preview) {
      $('status').textContent = 'On · use touch or simulated tilt';
      $('input-state').textContent = scene.manual ? 'SIMULATED TILT' : 'NO SENSOR READINGS';
      $('help').textContent = 'No sensor readings yet. Touch the water, use the tilt sliders or Preview underwater. Phone motion can be enabled in your browser’s site permissions.';
    }
  }
  $('start').addEventListener('click', async () => {
    const ticket = ++generation; active = true; resetPose(); started = performance.now(); received = false;
    $('start').disabled = true; $('stop').disabled = false; $('preview').disabled = false;
    $('status').textContent = 'On · checking motion access';
    $('pose').textContent = 'Touch the water or tilt gently.';
    audio.mute($('mute').checked); audio.unlock(); scene.start();
    say('welcome', true, false);
    // Both prompts begin synchronously in the original Start gesture, including Safari.
    const request = C => {
      try { return window.isSecureContext && C ? (typeof C.requestPermission === 'function' ? C.requestPermission() : Promise.resolve('granted')) : Promise.resolve('unavailable'); }
      catch (error) { return Promise.reject(error); }
    };
    const grants = await Promise.allSettled([request(window.DeviceOrientationEvent), request(window.DeviceMotionEvent)]);
    if (ticket !== generation || !active) return;
    allowed = grants.map(result => result.status === 'fulfilled' && result.value === 'granted');
    if (!document.hidden) attach();
    $('status').textContent = document.hidden ? 'Paused · page hidden' : allowed.some(Boolean) ? 'On · waiting for a sensor reading' : 'On · motion unavailable';
    $('help').textContent = allowed.some(Boolean)
      ? 'Tilt gently. Hold screen-down to go underwater. Touch or drag to make ripples; Preview underwater keeps everything visible.'
      : 'Motion access was denied or is unsupported. Touch, tilt sliders, sample comments and Preview underwater still work.';
    clearInterval(timer); timer = setInterval(heartbeat, 100);
  });
  $('stop').addEventListener('click', stop);
  ['tilt-x','tilt-y'].forEach(id => $(id).addEventListener('input', () => {
    if (down && !preview) setSubmerged(false, false, false);
    gate.reset(); candidate = ''; spokenPose = '';
  }));
  $('sensors').addEventListener('click', resetPose);
  $('preview').addEventListener('click', () => {
    if (!active || document.hidden) return;
    if (down) { preview = false; gate.reset(); setSubmerged(false); }
    else { preview = true; setSubmerged(true, true); }
  });
  $('refill').addEventListener('click', () => {
    invalidate(); down = preview = false; resetPose(); scene.useSensors(); scene.reset();
    $('preview').setAttribute('aria-pressed', 'false'); $('preview').textContent = 'Preview underwater';
    $('pose').textContent = 'Refilled. Dignity almost restored.';
    $('status').textContent = active ? 'On · bowl reset' : 'Off · bowl reset';
  });
  $('sample').addEventListener('click', () => {
    invalidate(); audio.unlock(); const wet = down;
    say(wet ? 'down' : choose(['flat','upright','side','shake'][Math.floor(Math.random() * 4)]), true, wet);
    if (wet && active) audio.ambient(true);
  });
  $('mute').addEventListener('change', () => { invalidate(); audio.mute($('mute').checked); voiceNote(); });
  $('voice').addEventListener('change', () => { voiceChosen = true; invalidate(); voiceNote(); });
  window.addEventListener('cheeky-splash', () => { if (active && !document.hidden) audio.bubble(); });
  function rotate() { previousVector = null; previousGravity = null; gate.since = null; candidate = ''; }
  screen.orientation?.addEventListener('change', rotate); window.addEventListener('orientationchange', rotate);
  document.addEventListener('visibilitychange', () => {
    invalidate(); resetPose(); down = preview = false; scene.pause(); scene.reset();
    $('preview').setAttribute('aria-pressed', 'false'); $('preview').textContent = 'Preview underwater';
    detach();
    if (document.hidden) { audio.suspend(); if (active) $('status').textContent = 'Paused · page hidden'; }
    else if (active) {
      attach(); scene.start(); audio.unlock(); received = false; started = performance.now(); lastSpoken = performance.now();
      $('status').textContent = 'On · waiting for fresh motion';
      $('help').textContent = 'Welcome back. Hold a fresh pose to resume; unfinished comments have been cleared.';
    }
  });
  window.addEventListener('pagehide', stop);
  synth?.addEventListener('voiceschanged', populateVoices);
  populateVoices();
})();

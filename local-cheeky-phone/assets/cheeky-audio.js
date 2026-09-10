(() => {
  'use strict';
  class CheekyAudio {
    constructor(note) {
      this.note = note; this.context = null; this.master = null; this.buffer = null; this.loading = null;
      this.version = 0; this.finish = null; this.voiceNodes = []; this.effects = new Set(); this.ambientTimer = null;
      this.busy = false; this.muted = false; this.under = false; this.lastBubble = 0;
    }
    unlock() {
      const C = window.AudioContext || window.webkitAudioContext;
      if (!C) { this.note('Web Audio is unavailable. Device speech and text still work; underwater filtering is unavailable.'); return Promise.resolve(false); }
      if (!this.context) {
        this.context = new C(); this.master = this.context.createGain();
        this.master.gain.value = this.muted ? 0 : .8; this.master.connect(this.context.destination);
        const silent = this.context.createBufferSource(); silent.buffer = this.context.createBuffer(1, 1, this.context.sampleRate); silent.connect(this.master); silent.start(); silent.onended = () => silent.disconnect();
      }
      this.ready = this.context.resume().then(() => this.context.state === 'running').catch(() => { this.note('Tap Start or Try a comment to restore audio.'); return false; });
      return this.ready;
    }
    prepare() {
      if (this.buffer) return Promise.resolve(this.buffer);
      if (!this.context) return Promise.reject(new Error('Start audio first'));
      if (!this.loading) this.loading = fetch('/assets/cheeky-george.mp3?v=water1', { credentials: 'same-origin' })
        .then(response => { if (!response.ok) throw new Error('Recording unavailable'); return response.arrayBuffer(); })
        .then(bytes => this.context.decodeAudioData(bytes)).then(buffer => { this.buffer = buffer; return buffer; })
        .catch(error => { this.loading = null; throw error; });
      return this.loading;
    }
    static route(context, source, destination, underwater) {
      const nodes = [], oscillators = [];
      const output = context.createGain(); output.gain.value = .92; output.connect(destination); nodes.push(output);
      if (!underwater) { source.connect(output); return { nodes, oscillators }; }
      const hp = context.createBiquadFilter(); hp.type = 'highpass'; hp.frequency.value = 110;
      const lp = context.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 1450; lp.Q.value = .65;
      const main = context.createGain(); main.gain.value = .76;
      const delay = context.createDelay(.04); delay.delayTime.value = .014;
      const wet = context.createGain(); wet.gain.value = .24;
      source.connect(hp); hp.connect(lp); lp.connect(main); main.connect(output); lp.connect(delay); delay.connect(wet); wet.connect(output);
      const lfo = context.createOscillator(); lfo.frequency.value = 2.6;
      const depth = context.createGain(); depth.gain.value = .002;
      lfo.connect(depth); depth.connect(delay.delayTime);
      const shimmer = context.createGain(); shimmer.gain.value = 180; lfo.connect(shimmer); shimmer.connect(lp.frequency);
      lfo.start(); nodes.push(hp, lp, main, delay, wet, lfo, depth, shimmer); oscillators.push(lfo);
      return { nodes, oscillators };
    }
    cancelSpeech() {
      this.version++;
      if (this.finish) this.finish(false);
      window.speechSynthesis?.cancel();
      this.busy = false;
      document.body.classList.remove('speaking');
    }
    stop() {
      this.cancelSpeech(); this.ambient(false);
      for (const effect of this.effects) effect();
      this.effects.clear();
    }
    mute(value) { this.muted = value; if (this.master) this.master.gain.value = value ? 0 : .8; if (value) this.stop(); }
    suspend() { this.stop(); return this.context?.suspend().catch(() => {}); }
    async say(id, voice, recorded, underwater) {
      this.cancelSpeech(); const ticket = this.version; this.busy = true;
      return new Promise(resolve => {
        let timer = null, source = null, graph = null, utterance = null, finished = false;
        const done = completed => {
          if (finished) return; finished = true; clearTimeout(timer);
          if (source) { source.onended = null; try { source.stop(); } catch {} source.disconnect(); }
          graph?.oscillators.forEach(node => { try { node.stop(); } catch {} }); graph?.nodes.forEach(node => node.disconnect());
          if (utterance) { utterance.onend = utterance.onerror = utterance.onstart = null; }
          this.utterance = null;
          if (this.finish === done) { this.finish = null; this.busy = false; document.body.classList.remove('speaking'); }
          resolve(completed);
        };
        this.finish = done;
        // Quiet mode has readable captions and a bounded reading interval, with no synthesis.
        if (this.muted) { timer = setTimeout(() => done(true), 3200); return; }
        if (recorded) {
          timer = setTimeout(() => { this.note('The recording did not load. Text is still available; try again or choose a device voice.'); done(false); }, 12000);
          Promise.all([this.prepare(), this.ready || Promise.resolve(this.context?.state === 'running')]).then(([buffer]) => {
            if (ticket !== this.version || finished || document.hidden || this.muted) return;
            clearTimeout(timer);
            if (this.context.state !== 'running') { this.note('Audio is paused. Tap Try a comment to restore it.'); done(false); return; }
            source = this.context.createBufferSource(); source.buffer = buffer;
            graph = CheekyAudio.route(this.context, source, this.master, underwater);
            const [offset, duration] = CheekyClips[id];
            source.onended = () => done(true); source.start(0, offset, duration);
            document.body.classList.add('speaking');
            timer = setTimeout(() => done(false), (duration + 2) * 1000);
          }).catch(() => { if (ticket === this.version && !finished) { this.note('The George recording is unavailable. Text is still shown; select a device voice to hear speech.'); done(false); } });
          return;
        }
        if (!window.speechSynthesis || !window.SpeechSynthesisUtterance) { this.note('Device speech is unavailable. Select the recorded George voice, or use text.'); done(false); return; }
        utterance = new SpeechSynthesisUtterance(CheekyLines[id]); this.utterance = utterance;
        utterance.lang = voice?.lang || 'en-GB'; utterance.rate = .92;
        if (voice) utterance.voice = voice;
        utterance.onstart = () => { if (ticket === this.version) document.body.classList.add('speaking'); };
        utterance.onend = () => done(true);
        utterance.onerror = event => { if (!['canceled','interrupted'].includes(event.error)) this.note('Speech was unavailable. Try another voice or use text.'); done(false); };
        window.speechSynthesis.speak(utterance);
        timer = setTimeout(() => { if (ticket === this.version) window.speechSynthesis.cancel(); done(false); }, 20000);
      });
    }
    bubble(force = false) {
      if (!this.context || this.context.state !== 'running' || this.muted || document.hidden) return;
      const now = this.context.currentTime;
      if (!force && now - this.lastBubble < .24) return; this.lastBubble = now;
      const osc = this.context.createOscillator(), gain = this.context.createGain();
      const duration = .16 + Math.random() * .08; osc.type = 'sine';
      osc.frequency.setValueAtTime(280 + Math.random() * 230, now); osc.frequency.exponentialRampToValueAtTime(850 + Math.random() * 350, now + duration);
      gain.gain.setValueAtTime(.0001, now); gain.gain.exponentialRampToValueAtTime(this.busy ? .012 : .023, now + .025); gain.gain.exponentialRampToValueAtTime(.0001, now + duration);
      osc.connect(gain); gain.connect(this.master);
      let removed = false;
      const cleanup = () => { if (removed) return; removed = true; osc.onended = null; try { osc.stop(); } catch {} osc.disconnect(); gain.disconnect(); this.effects.delete(cleanup); };
      this.effects.add(cleanup); osc.onended = cleanup; osc.start(); osc.stop(now + duration + .02);
    }
    ambient(on) {
      clearInterval(this.ambientTimer); this.ambientTimer = null; this.under = on;
      if (on && !this.muted) { this.bubble(true); this.ambientTimer = setInterval(() => this.bubble(), 870); }
    }
  }
  window.CheekyAudio = CheekyAudio;
})();

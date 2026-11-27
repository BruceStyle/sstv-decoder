(() => {
  const I18N = {
    "zh-CN": {
      page_title: "SSTV Decoder · 抬头，就能收到来自太空的画面",
      cover_title_1: "抬头，",
      cover_title_2: "就能收到来自太空的画面",
      cover_lead: "国际空间站每 92 分钟绕地球一圈。ARISS 活动期间，它会用无线电向地面播送图片。一台手台就能收到，剩下的交给 AI。",
      cover_cta: "开始接收",
      chart_note: "示意过境轨迹",
      nav_receive: "接收",
      nav_signal: "原理",
      nav_captures: "档案",
      nav_access: "接入",
      nav_about: "作者",
      hero_title_1: "把空间站的电波",
      hero_title_2: "解成画面",
      hero_subtitle: "录下国际空间站过境时的 SSTV 音频，交给你的 AI。它会找到信号，逐行还原出 320×240 的原图。",
      tab_install: "终端安装",
      tab_prompt: "对 AI 说",
      copy_btn: "复制",
      copied_btn: "已复制",
      cmd_install: "npx skills add BruceStyle/sstv-decoder",
      cmd_prompt: "帮我安装 SSTV 解码插件：https://github.com/BruceStyle/sstv-decoder",
      compat_line: "适用于 Claude Code · Cursor · Codex · Antigravity · Gemini CLI 等 75+ 个 Agent",
      footnote_req: "需要 FFmpeg 与 uv",
      signal_tag: "02 · 信号原理",
      signal_title_1: "每一行像素，",
      signal_title_2: "都是 150 毫秒的音调",
      signal_lead: "Robot 36 把图像的亮度和色彩编码成 1200 到 2300 Hz 之间的频率。在左边的图上选一行，看看它在电波里长什么样。",
      slider_label: "选择扫描行",
      step_1_title: "过境预报",
      step_1_desc: "查好国际空间站飞过头顶的时间",
      step_2_title: "录音",
      step_2_desc: "手台对准天空，把 145.800 MHz 录成音频",
      step_3_title: "寻帧",
      step_3_desc: "在整段录音里找到 VIS 08 识别头",
      step_4_title: "行同步",
      step_4_desc: "校准 150 ms 扫描时钟，抵消多普勒漂移",
      step_5_title: "成像",
      step_5_desc: "输出 320×240 PNG 和同步报告",
      owner_you: "你",
      owner_plugin: "插件",
      handover_label: "插件从这里接管",
      captures_tag: "03 · 实测档案",
      captures_title_1: "两次过境，",
      captures_title_2: "两张来自太空的明信片",
      captures_lead: "以下画面均由本插件从真实录音中解出，未经修图。",
      render_pixel: "原始像素",
      render_smooth: "平滑视图",
      cap_1_title: "ARISS 第 2 帧 · Student Education 2026",
      cap_date_dt: "日期",
      cap_1_date: "2026-10-06 下午过境",
      cap_offset_dt: "录音位置",
      cap_1_offset: "04:48 至 05:24",
      cap_channel_dt: "声道",
      cap_1_channel: "右声道",
      cap_sync_dt: "同步覆盖",
      cap_output_dt: "输出",
      cap_2_title: "Sputnik-1 纪念图传",
      cap_2_date: "2026-10-05 过境",
      cap_call_dt: "呼号",
      cap_recovery_dt: "恢复方式",
      cap_2_recovery: "弱信号噪声协方差恢复",
      access_tag: "04 · 接入方式",
      access_title_1: "一条指令，",
      access_title_2: "或者任何你习惯的方式",
      access_lead: "基于开放的 Agent Skills 与 MCP 标准，不绑定任何一家 AI 客户端，也不需要上架商店。",
      acc_a_title: "Agent Skill（推荐）",
      acc_a_desc: "一行安装到本机所有兼容的 Agent。",
      acc_b_title: "本地 MCP 服务",
      acc_b_desc: "适用于只支持 MCP 的客户端，如 Claude Desktop。",
      acc_b_hint: "发布至 PyPI 前，请将 \"uvx\", \"sstv-decoder-mcp\" 替换为 \"uvx\", \"--from\", \"git+https://github.com/BruceStyle/sstv-decoder\", \"sstv-decoder-mcp\"。",
      acc_c_title: "命令行",
      acc_c_desc: "不经过 AI，直接解码一段录音。",
      acc_c_hint: "发布至 PyPI 前，请改用 uvx --from git+https://github.com/BruceStyle/sstv-decoder sstv-decoder ...。",
      access_req: "环境要求：Python 3.11+ · FFmpeg / ffprobe · uv（推荐）",
      access_docs: "完整说明见 GitHub README ↗",
      about_tag: "05 · 关于作者",
      about_title_1: "我在楼顶，",
      about_title_2: "等过一次空间站",
      about_statement: "我是一名业余无线电爱好者。我希望把从空间站电波里解出图片这件事，交给每个人身边的 AI。",
      about_p1: "2026 年 10 月，我举着手台和便携八木天线在楼顶守候国际空间站过境，录下了来自 400 公里高空的音频信号，并借助 AI 把嘈杂频调声逐步还原成了清晰的太空明信片。",
      about_p2: "后来我曾将这套能力做成单一平台插件，却因为商店绑卡门槛没能上架。于是我决定改用开放的 Agent Skills 与 MCP 标准重构并彻底开源，统一成一条跨 Agent 指令，让每位同好都能直接用上。",
      qsl_to: "TO · 每一位同好",
      qsl_role_dt: "身份",
      qsl_role_dd: "业余无线电爱好者 · 开源作者",
      qsl_repo_dt: "仓库",
      qsl_email_dt: "邮箱",
      qsl_license_dt: "协议",
      footer_top: "返回顶部",
      seg_sync_sub: "同步",
      seg_luma_sub: "亮度",
      seg_chroma_sub: "色度",
      sample_0_meta: "2026-10-06 下午过境 · NA1SS · 同步 98.3%",
      sample_1_meta: "2026-10-05 过境 · RS0ISS · 弱信号恢复"
    },
    en: {
      page_title: "SSTV Decoder · Look up and catch pictures from space",
      cover_title_1: "Look up, ",
      cover_title_2: "and catch pictures from space",
      cover_lead: "The ISS circles Earth every 92 minutes. During ARISS events it beams pictures down by radio. A handheld can catch them; your AI does the rest.",
      cover_cta: "Start receiving",
      chart_note: "Illustrative pass",
      nav_receive: "Receive",
      nav_signal: "Signal",
      nav_captures: "Captures",
      nav_access: "Connect",
      nav_about: "Author",
      hero_title_1: "Turn space station radio",
      hero_title_2: "into pictures",
      hero_subtitle: "Record an ISS pass, hand the audio to your AI agent, and get the original 320×240 image back, line by line.",
      tab_install: "Terminal",
      tab_prompt: "Ask AI",
      copy_btn: "Copy",
      copied_btn: "Copied",
      cmd_install: "npx skills add BruceStyle/sstv-decoder",
      cmd_prompt: "Install the SSTV decoder plugin from https://github.com/BruceStyle/sstv-decoder",
      compat_line: "Works with Claude Code · Cursor · Codex · Antigravity · Gemini CLI and 75+ agents",
      footnote_req: "Requires FFmpeg & uv",
      signal_tag: "02 · How the signal works",
      signal_title_1: "Every line of pixels ",
      signal_title_2: "is 150 ms of sound",
      signal_lead: "Robot 36 encodes brightness and color as tones between 1200 and 2300 Hz. Pick a line on the image to see how it sounds on air.",
      slider_label: "Select scan line",
      step_1_title: "Predict the pass",
      step_1_desc: "Find when the ISS flies overhead",
      step_2_title: "Record",
      step_2_desc: "Point a handheld at the sky and record 145.800 MHz",
      step_3_title: "Find the frame",
      step_3_desc: "Locate the VIS 08 header in the recording",
      step_4_title: "Sync lines",
      step_4_desc: "Lock the 150 ms line clock and correct Doppler drift",
      step_5_title: "Build the image",
      step_5_desc: "Output a 320×240 PNG and a sync report",
      owner_you: "You",
      owner_plugin: "Plugin",
      handover_label: "Plugin takes over",
      captures_tag: "03 · Captures",
      captures_title_1: "Two passes, ",
      captures_title_2: "two postcards from space",
      captures_lead: "Both frames were decoded by this plugin from real recordings, with no retouching.",
      render_pixel: "Raw pixels",
      render_smooth: "Smoothed",
      cap_1_title: "ARISS frame 2 · Student Education 2026",
      cap_date_dt: "Date",
      cap_1_date: "2026-10-06 afternoon pass",
      cap_offset_dt: "In recording",
      cap_1_offset: "04:48 to 05:24",
      cap_channel_dt: "Channel",
      cap_1_channel: "Right",
      cap_sync_dt: "Sync coverage",
      cap_output_dt: "Output",
      cap_2_title: "Sputnik-1 commemorative slide",
      cap_2_date: "2026-10-05 pass",
      cap_call_dt: "Callsign",
      cap_recovery_dt: "Recovery",
      cap_2_recovery: "Weak-signal covariance recovery",
      access_tag: "04 · Ways to connect",
      access_title_1: "One command, ",
      access_title_2: "or whatever you already use",
      access_lead: "Built on the open Agent Skills and MCP standards. No lock-in to a single AI client, no app store.",
      acc_a_title: "Agent Skill (recommended)",
      acc_a_desc: "One line installs it into every compatible agent on this machine.",
      acc_b_title: "Local MCP server",
      acc_b_desc: "For MCP-only clients such as Claude Desktop.",
      acc_b_hint: "Before PyPI publication, replace \"uvx\", \"sstv-decoder-mcp\" with \"uvx\", \"--from\", \"git+https://github.com/BruceStyle/sstv-decoder\", \"sstv-decoder-mcp\".",
      acc_c_title: "Command line",
      acc_c_desc: "Decode a recording directly, no AI involved.",
      acc_c_hint: "Before PyPI publication, run via uvx --from git+https://github.com/BruceStyle/sstv-decoder sstv-decoder ...",
      access_req: "Requires Python 3.11+ · FFmpeg / ffprobe · uv (recommended)",
      access_docs: "Full docs on GitHub ↗",
      about_tag: "05 · About",
      about_title_1: "I waited on a rooftop ",
      about_title_2: "for the space station",
      about_statement: "I am an amateur radio enthusiast working to bring orbital SSTV signal recovery to every AI agent.",
      about_p1: "In October 2026, I stood on a rooftop with a handheld transceiver and portable Yagi antenna to record ISS passes from 400 km overhead and decoded those audio tones into images with AI.",
      about_p2: "When store billing requirements blocked a single-platform plugin release, I rebuilt the engine on open Agent Skills and MCP standards as a single cross-agent command.",
      qsl_to: "TO · Every listener",
      qsl_role_dt: "Role",
      qsl_role_dd: "Amateur radio operator · Open-source author",
      qsl_repo_dt: "Repo",
      qsl_email_dt: "Email",
      qsl_license_dt: "License",
      footer_top: "Back to top",
      seg_sync_sub: "sync",
      seg_luma_sub: "luma",
      seg_chroma_sub: "chroma",
      sample_0_meta: "2026-10-06 afternoon pass · NA1SS · sync 98.3%",
      sample_1_meta: "2026-10-05 pass · RS0ISS · weak-signal recovery"
    }
  };

  const SAMPLES = [
    {
      key: "na1ss",
      src: "assets/decoded-iss-2026-10-06.png",
      channel: "CH R · ROBOT 36",
      metaKey: "sample_0_meta"
    },
    {
      key: "rs0iss",
      src: "assets/decoded-iss-2026-10-05.png",
      channel: "CH L · ROBOT 36",
      metaKey: "sample_1_meta"
    }
  ];

  let currentLang = "zh-CN";
  let cmdMode = "install";
  let activeSampleIdx = 0;
  let scanRow = 0;
  let holdMs = 0;
  let lastTick = 0;
  let rafId = null;
  let heroVisible = !("IntersectionObserver" in window);
  let selectedScopeRow = 120;
  let copyTimer = null;

  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  // Elements
  const passMetaEl = document.getElementById("pass-meta");
  const monitorChannelEl = document.getElementById("monitor-channel");
  const heroLineReadout = document.getElementById("hero-line-readout");
  const heroFreqReadout = document.getElementById("hero-freq-readout");
  const scanCanvas = document.getElementById("hero-scan-canvas");
  const waterfallCanvas = document.getElementById("hero-waterfall-canvas");
  const scanCtx = scanCanvas.getContext("2d");
  const waterfallCtx = waterfallCanvas.getContext("2d");

  const cmdBar = document.querySelector("#install .cmd-bar");
  const cmdPrefix = document.getElementById("cmd-prefix");
  const cmdText = document.getElementById("cmd-text");
  const copyBtn = document.getElementById("copy-btn");
  const cmdTabs = Array.from(document.querySelectorAll("#install .cmd-tab"));
  const langBtns = Array.from(document.querySelectorAll(".lang-btn"));

  const thumbWrap = document.getElementById("thumb-wrap");
  const thumbScanline = document.getElementById("thumb-scanline");
  const lineSlider = document.getElementById("line-slider");
  const pickerReadout = document.getElementById("picker-readout");
  const scopeCanvas = document.getElementById("scope-canvas");
  const scopeCtx = scopeCanvas.getContext("2d");

  // Pre-build deterministic 320x240 blue-grey static substrate
  const staticCanvas = document.createElement("canvas");
  staticCanvas.width = 320;
  staticCanvas.height = 240;
  const staticCtx = staticCanvas.getContext("2d");
  (() => {
    const imgData = staticCtx.createImageData(320, 240);
    const d = imgData.data;
    let seed = 42197;
    for (let i = 0; i < d.length; i += 4) {
      seed = (seed * 16807) % 2147483647;
      const v = 12 + ((seed % 32) | 0);
      d[i] = v;
      d[i + 1] = v + 4;
      d[i + 2] = v + 11;
      d[i + 3] = 255;
    }
    staticCtx.putImageData(imgData, 0, 0);
  })();

  // Offscreen pixel extractor (handles file:// canvas taint gracefully)
  const extractCanvas = document.createElement("canvas");
  extractCanvas.width = 320;
  extractCanvas.height = 240;
  const extractCtx = extractCanvas.getContext("2d", { willReadFrequently: true });

  function buildFallbackBuffers(seedBase) {
    const lum = new Uint8Array(320 * 240);
    const rgba = new Uint8ClampedArray(320 * 240 * 4);
    let seed = seedBase;
    for (let y = 0; y < 240; y++) {
      const band = Math.sin(y * 0.085) * 42 + Math.cos(y * 0.031) * 28;
      for (let x = 0; x < 320; x++) {
        seed = (seed * 16807) % 2147483647;
        const p = y * 320 + x;
        const wave = Math.sin(x * 0.045 + y * 0.02) * 38;
        const l = Math.max(12, Math.min(242, Math.round(118 + band + wave + ((seed % 36) - 18))));
        lum[p] = l;
        const idx = p * 4;
        rgba[idx] = Math.max(0, Math.min(255, l + Math.round(Math.sin(x * 0.03) * 35)));
        rgba[idx + 1] = l;
        rgba[idx + 2] = Math.max(0, Math.min(255, l + Math.round(Math.cos(y * 0.04) * 35)));
        rgba[idx + 3] = 255;
      }
    }
    return { lum, rgba };
  }

  const sampleStore = new Map();

  function loadSample(idx) {
    const item = SAMPLES[idx];
    if (sampleStore.has(item.key)) return;
    const img = new Image();
    img.onload = () => {
      let lum = null;
      let rgba = null;
      try {
        extractCtx.clearRect(0, 0, 320, 240);
        extractCtx.drawImage(img, 0, 0, 320, 240);
        const data = extractCtx.getImageData(0, 0, 320, 240).data;
        rgba = data;
        lum = new Uint8Array(320 * 240);
        for (let i = 0, p = 0; i < data.length; i += 4, p++) {
          lum[p] = Math.round(0.299 * data[i] + 0.587 * data[i + 1] + 0.114 * data[i + 2]);
        }
      } catch {
        const fb = buildFallbackBuffers(idx === 0 ? 918273 : 372819);
        lum = fb.lum;
        rgba = fb.rgba;
      }
      sampleStore.set(item.key, { img, lum, rgba });
      if (idx === activeSampleIdx) {
        drawHeroFrame(scanRow);
      }
      if (idx === 0) {
        drawScope();
      }
    };
    img.src = item.src;
  }

  SAMPLES.forEach((_, idx) => loadSample(idx));

  // Sizing with DPR
  function syncCanvasSize(canvas) {
    const rect = canvas.getBoundingClientRect();
    if (rect.width <= 0 || rect.height <= 0) return false;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const w = Math.round(rect.width * dpr);
    const h = Math.round(rect.height * dpr);
    if (canvas.width !== w || canvas.height !== h) {
      canvas.width = w;
      canvas.height = h;
    }
    return true;
  }

  function syncAllCanvases() {
    syncCanvasSize(scanCanvas);
    syncCanvasSize(waterfallCanvas);
    syncCanvasSize(scopeCanvas);
    drawHeroFrame(scanRow);
    drawScope();
  }

  // Waterfall color ramp: transparent -> #12305a -> #1fa3c9 -> #f2d03b -> #ff5b24
  function waterfallColor(e) {
    const t = Math.max(0, Math.min(1, e));
    if (t < 0.04) return null;
    const stops = [
      [0.04, 18, 48, 90, 0.2],
      [0.3, 18, 48, 90, 0.92],
      [0.56, 31, 163, 201, 0.96],
      [0.8, 242, 208, 59, 0.98],
      [1.0, 255, 91, 36, 1.0]
    ];
    for (let i = 1; i < stops.length; i++) {
      if (t <= stops[i][0]) {
        const a = stops[i - 1];
        const b = stops[i];
        const u = (t - a[0]) / (b[0] - a[0]);
        const r = Math.round(a[1] + (b[1] - a[1]) * u);
        const g = Math.round(a[2] + (b[2] - a[2]) * u);
        const bl = Math.round(a[3] + (b[3] - a[3]) * u);
        const al = (a[4] + (b[4] - a[4]) * u).toFixed(3);
        return `rgba(${r}, ${g}, ${bl}, ${al})`;
      }
    }
    return "rgb(255, 91, 36)";
  }

  function drawHeroFrame(rowFloat) {
    const w = scanCanvas.width;
    const h = scanCanvas.height;
    if (!w || !h) return;

    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const sample = SAMPLES[activeSampleIdx];
    const data = sampleStore.get(sample.key);

    // Monitor: static substrate + horizontal scanlines
    scanCtx.imageSmoothingEnabled = false;
    scanCtx.drawImage(staticCanvas, 0, 0, w, h);

    const stepPx = Math.max(3, Math.round(4 * dpr));
    scanCtx.fillStyle = "rgba(11, 12, 14, 0.5)";
    for (let y = 0; y < h; y += stepPx) {
      scanCtx.fillRect(0, y, w, Math.max(1, Math.round(dpr)));
    }

    const rows = Math.min(240, Math.max(0, Math.floor(rowFloat)));
    const destH = Math.round((rows / 240) * h);

    if (data && data.img && destH > 0) {
      const srcH = Math.max(1, Math.round((rows / 240) * data.img.height));
      scanCtx.drawImage(data.img, 0, 0, data.img.width, srcH, 0, 0, w, destH);
    }

    // Active scan beam
    if (rows < 240) {
      const glowH = Math.round(14 * dpr);
      const grad = scanCtx.createLinearGradient(0, Math.max(0, destH - glowH), 0, destH);
      grad.addColorStop(0, "rgba(255, 255, 255, 0)");
      grad.addColorStop(1, "rgba(255, 255, 255, 0.36)");
      scanCtx.fillStyle = grad;
      scanCtx.fillRect(0, Math.max(0, destH - glowH), w, glowH);

      scanCtx.fillStyle = "#ff5b24";
      scanCtx.fillRect(0, destH, w, Math.max(2, Math.round(2 * dpr)));
    }

    // Waterfall strip (row-aligned with monitor)
    const ww = waterfallCanvas.width;
    const wh = waterfallCanvas.height;
    if (ww && wh) {
      waterfallCtx.fillStyle = "#0b0c0e";
      waterfallCtx.fillRect(0, 0, ww, wh);

      const minF = 1100;
      const maxF = 2400;
      const spanF = maxF - minF;
      const bins = 48;
      const binW = ww / bins;
      const rowH = wh / 240;

      // Three vertical reference lines at 1200, 1500, 2300 Hz
      waterfallCtx.strokeStyle = "rgba(255, 255, 255, 0.14)";
      waterfallCtx.lineWidth = Math.max(1, Math.round(dpr));
      for (const f of [1200, 1500, 2300]) {
        const x = Math.round(((f - minF) / spanF) * ww) + 0.5;
        waterfallCtx.beginPath();
        waterfallCtx.moveTo(x, 0);
        waterfallCtx.lineTo(x, wh);
        waterfallCtx.stroke();
      }

      if (data && rows > 0) {
        const syncBin = Math.floor(((1200 - minF) / spanF) * (bins - 1));
        for (let r = 0; r < rows; r++) {
          const energy = new Float32Array(bins);
          energy[syncBin] = 0.9;
          if (syncBin > 0) energy[syncBin - 1] = 0.28;
          if (syncBin + 1 < bins) energy[syncBin + 1] = 0.28;

          const rowOff = r * 320;
          for (let col = 0; col < 320; col += 4) {
            const lum = data.lum[rowOff + col];
            const f = 1500 + (lum / 255) * 800;
            const b = Math.min(bins - 1, Math.max(0, Math.floor(((f - minF) / spanF) * (bins - 1))));
            energy[b] += 0.14;
          }

          const y = r * rowH;
          const drawH = Math.ceil(rowH) + 0.5;
          for (let b = 0; b < bins; b++) {
            const colStr = waterfallColor(energy[b]);
            if (!colStr) continue;
            waterfallCtx.fillStyle = colStr;
            waterfallCtx.fillRect(b * binW, y, Math.ceil(binW), drawH);
          }
        }

        if (rows < 240) {
          waterfallCtx.fillStyle = "#ff5b24";
          waterfallCtx.fillRect(0, Math.round((rows / 240) * wh), ww, Math.max(2, Math.round(2 * dpr)));
        }
      }
    }

    // Readouts
    const shownRow = Math.min(240, rows);
    const padRow = String(shownRow).padStart(3, "0");
    heroLineReadout.textContent = `LINE ${padRow} / 240`;

    let meanLum = 128;
    if (data && rows > 0) {
      const rIdx = Math.min(239, rows - 1);
      const off = rIdx * 320;
      let sum = 0;
      for (let x = 0; x < 320; x++) {
        sum += data.lum[off + x];
      }
      meanLum = sum / 320;
    }
    const freqHz = Math.round(1500 + (meanLum / 255) * 800);
    heroFreqReadout.textContent = `Y ${freqHz} Hz`;
  }

  function updateHeroSampleMeta() {
    const dict = I18N[currentLang] || I18N["zh-CN"];
    const sample = SAMPLES[activeSampleIdx];
    monitorChannelEl.textContent = sample.channel;
    passMetaEl.textContent = dict[sample.metaKey];
  }

  function stepHero(ts) {
    if (!lastTick) lastTick = ts;
    const dt = Math.min(64, ts - lastTick);
    lastTick = ts;

    if (scanRow < 240) {
      scanRow = Math.min(240, scanRow + dt * 0.04);
      drawHeroFrame(scanRow);
    } else {
      holdMs += dt;
      if (holdMs >= 3500) {
        holdMs = 0;
        scanRow = 0;
        activeSampleIdx = (activeSampleIdx + 1) % SAMPLES.length;
        updateHeroSampleMeta();
        drawHeroFrame(0);
      }
    }

    if (heroVisible && !document.hidden && !reducedMotion.matches) {
      rafId = window.requestAnimationFrame(stepHero);
    } else {
      rafId = null;
    }
  }

  function startHeroLoop() {
    if (reducedMotion.matches) {
      scanRow = 240;
      drawHeroFrame(240);
      return;
    }
    if (!rafId && heroVisible && !document.hidden) {
      lastTick = 0;
      rafId = window.requestAnimationFrame(stepHero);
    }
  }

  function stopHeroLoop() {
    if (rafId) {
      window.cancelAnimationFrame(rafId);
      rafId = null;
    }
  }

  // Header contrast switch across dark / paper sections
  const siteHeader = document.querySelector(".site-header");
  const paperSections = Array.from(document.querySelectorAll(".is-paper"));
  function syncHeaderSurface() {
    if (!siteHeader) return;
    const headerH = siteHeader.getBoundingClientRect().height || 56;
    const y = headerH * 0.6;
    const onPaper = paperSections.some((sec) => {
      const rect = sec.getBoundingClientRect();
      return rect.top <= y && rect.bottom > y;
    });
    if (onPaper) {
      siteHeader.classList.add("is-on-paper");
      siteHeader.classList.remove("is-scrolled");
    } else {
      siteHeader.classList.remove("is-on-paper");
      siteHeader.classList.toggle("is-scrolled", window.scrollY > 40);
    }
  }
  syncHeaderSurface();
  window.addEventListener("scroll", syncHeaderSurface, { passive: true });
  window.addEventListener("resize", syncHeaderSurface, { passive: true });

  // Pause hero animation when scrolled out of view or hidden
  const heroSection = document.getElementById("receive");
  if ("IntersectionObserver" in window && heroSection) {
    const obs = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          heroVisible = entry.isIntersecting;
          if (heroVisible) startHeroLoop();
          else stopHeroLoop();
        }
      },
      { threshold: 0.05 }
    );
    obs.observe(heroSection);
  }

  document.addEventListener("visibilitychange", () => {
    if (document.hidden) stopHeroLoop();
    else startHeroLoop();
  });

  // Command Tabs & Copy
  function syncCommandBlock() {
    const dict = I18N[currentLang] || I18N["zh-CN"];
    if (cmdBar) cmdBar.classList.toggle("is-prompt", cmdMode === "prompt");
    cmdPrefix.textContent = cmdMode === "prompt" ? ">" : "$";
    cmdText.textContent = cmdMode === "prompt" ? dict.cmd_prompt : dict.cmd_install;
    copyBtn.textContent = dict.copy_btn;
  }

  for (const tab of cmdTabs) {
    tab.addEventListener("click", () => {
      cmdMode = tab.dataset.mode || "install";
      for (const t of cmdTabs) {
        t.setAttribute("aria-selected", String(t === tab));
      }
      syncCommandBlock();
    });
  }

  copyBtn.addEventListener("click", async () => {
    const text = cmdText.textContent || "";
    const dict = I18N[currentLang] || I18N["zh-CN"];
    let ok = false;
    try {
      await navigator.clipboard.writeText(text);
      ok = true;
    } catch {
      const ta = document.createElement("textarea");
      ta.value = text;
      ta.style.position = "fixed";
      ta.style.opacity = "0";
      document.body.append(ta);
      ta.select();
      ok = document.execCommand("copy");
      ta.remove();
    }
    if (ok) {
      copyBtn.textContent = dict.copied_btn;
      if (copyTimer) window.clearTimeout(copyTimer);
      copyTimer = window.setTimeout(() => {
        copyBtn.textContent = dict.copy_btn;
      }, 1800);
    }
  });

  // Language switcher
  function applyLanguage(lang) {
    currentLang = lang;
    const dict = I18N[lang] || I18N["zh-CN"];
    document.documentElement.lang = lang;
    document.title = dict.page_title;
    for (const el of document.querySelectorAll("[data-i18n]")) {
      const key = el.getAttribute("data-i18n");
      if (key && dict[key] !== undefined) {
        el.textContent = dict[key];
      }
    }
    for (const btn of langBtns) {
      btn.setAttribute("aria-pressed", String(btn.dataset.lang === lang));
    }
    updateHeroSampleMeta();
    syncCommandBlock();
    drawScope();
  }

  for (const btn of langBtns) {
    btn.addEventListener("click", () => {
      if (btn.dataset.lang) applyLanguage(btn.dataset.lang);
    });
  }

  // Section 02: Interactive Robot 36 150ms line waveform
  function updatePickerRow(row) {
    selectedScopeRow = Math.max(0, Math.min(239, Math.round(row)));
    lineSlider.value = String(selectedScopeRow);
    const pct = ((selectedScopeRow + 0.5) / 240) * 100;
    thumbScanline.style.top = `${pct}%`;
    const chromaLabel = selectedScopeRow % 2 === 0 ? "R-Y" : "B-Y";
    pickerReadout.textContent = `LINE ${String(selectedScopeRow).padStart(3, "0")} / 240 · ${chromaLabel}`;
    drawScope();
  }

  function pickRowFromPointer(e) {
    const rect = thumbWrap.getBoundingClientRect();
    const ratio = Math.max(0, Math.min(0.999, (e.clientY - rect.top) / rect.height));
    updatePickerRow(Math.floor(ratio * 240));
  }

  let draggingThumb = false;
  thumbWrap.addEventListener("pointerdown", (e) => {
    draggingThumb = true;
    thumbWrap.setPointerCapture(e.pointerId);
    pickRowFromPointer(e);
  });
  thumbWrap.addEventListener("pointermove", (e) => {
    if (draggingThumb) pickRowFromPointer(e);
  });
  thumbWrap.addEventListener("pointerup", () => {
    draggingThumb = false;
  });
  thumbWrap.addEventListener("pointercancel", () => {
    draggingThumb = false;
  });
  lineSlider.addEventListener("input", () => {
    updatePickerRow(Number(lineSlider.value));
  });

  function drawScope() {
    const w = scopeCanvas.width;
    const h = scopeCanvas.height;
    if (!w || !h) return;

    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const cssW = w / dpr;
    const isCompact = window.innerWidth < 760 || cssW < 480;
    const dict = I18N[currentLang] || I18N["zh-CN"];

    scopeCtx.clearRect(0, 0, w, h);
    scopeCtx.fillStyle = "#e7e9e5";
    scopeCtx.fillRect(0, 0, w, h);

    const padLeft = Math.round((isCompact ? 42 : 58) * dpr);
    const padRight = Math.round(14 * dpr);
    const padTop = Math.round((isCompact ? 34 : 44) * dpr);
    const padBottom = Math.round(28 * dpr);
    const plotW = w - padLeft - padRight;
    const plotH = h - padTop - padBottom;
    if (plotW <= 20 || plotH <= 20) return;

    const minF = 1100;
    const maxF = 2400;
    const totalMs = 150;
    const xOfMs = (ms) => padLeft + (ms / totalMs) * plotW;
    const yOfHz = (hz) => padTop + (1 - (hz - minF) / (maxF - minF)) * plotH;

    // 6 Robot 36 segments (sum = 150 ms)
    const segments = [
      { name: "SYNC", dur: "9 ms", start: 0, end: 9, sub: dict.seg_sync_sub, tint: true },
      { name: "PORCH", dur: "3 ms", start: 9, end: 12, sub: "", tint: false },
      { name: "Y", dur: "88 ms", start: 12, end: 100, sub: dict.seg_luma_sub, tint: true },
      { name: "SEP", dur: "4.5 ms", start: 100, end: 104.5, sub: "", tint: false },
      { name: "PORCH", dur: "1.5 ms", start: 104.5, end: 106, sub: "", tint: false },
      { name: selectedScopeRow % 2 === 0 ? "R-Y" : "B-Y", dur: "44 ms", start: 106, end: 150, sub: dict.seg_chroma_sub, tint: true }
    ];

    // Segment alternating fills and top labels
    const labelFontPx = Math.round((isCompact ? 9.5 : 11) * dpr);
    const subFontPx = Math.round((isCompact ? 9 : 10) * dpr);
    scopeCtx.textBaseline = "alphabetic";

    for (const seg of segments) {
      const x0 = xOfMs(seg.start);
      const x1 = xOfMs(seg.end);
      if (seg.tint) {
        scopeCtx.fillStyle = "rgba(14, 16, 19, 0.045)";
        scopeCtx.fillRect(x0, padTop, x1 - x0, plotH);
      }

      // Segment boundary ticks
      scopeCtx.strokeStyle = "rgba(14, 16, 19, 0.12)";
      scopeCtx.lineWidth = Math.max(1, dpr);
      scopeCtx.beginPath();
      scopeCtx.moveTo(Math.round(x0) + 0.5, padTop);
      scopeCtx.lineTo(Math.round(x0) + 0.5, padTop + plotH);
      scopeCtx.stroke();

      const centerX = (x0 + x1) / 2;
      scopeCtx.fillStyle = "#0e1013";
      scopeCtx.font = `500 ${labelFontPx}px "IBM Plex Mono", monospace`;

      if (seg.name === "SYNC") {
        scopeCtx.strokeStyle = "#ff5b24";
        scopeCtx.lineWidth = Math.max(1.2, 1.4 * dpr);
        scopeCtx.strokeRect(x0 + 0.5, padTop + 0.5, x1 - x0 - 1, plotH - 1);

        scopeCtx.textAlign = "left";
        scopeCtx.fillText(isCompact ? "SYNC" : "SYNC 9 ms", x0, padTop - Math.round(20 * dpr));
        if (!isCompact && seg.sub) {
          scopeCtx.fillStyle = "#575d66";
          scopeCtx.font = `400 ${subFontPx}px "IBM Plex Mono", "Noto Sans SC", sans-serif`;
          scopeCtx.fillText(seg.sub, x0, padTop - Math.round(6 * dpr));
        }
      } else if (seg.start === 9) {
        if (!isCompact) {
          scopeCtx.textAlign = "left";
          scopeCtx.fillStyle = "#575d66";
          scopeCtx.font = `400 ${subFontPx}px "IBM Plex Mono", monospace`;
          scopeCtx.fillText("PORCH 3 ms", x0 + 2 * dpr, padTop - Math.round(6 * dpr));
        }
      } else if (seg.name === "Y" || seg.name === "R-Y" || seg.name === "B-Y") {
        scopeCtx.textAlign = "center";
        scopeCtx.fillText(isCompact ? seg.name : `${seg.name} ${seg.dur}`, centerX, padTop - Math.round(20 * dpr));
        if (!isCompact && seg.sub) {
          scopeCtx.fillStyle = "#575d66";
          scopeCtx.font = `400 ${subFontPx}px "IBM Plex Mono", "Noto Sans SC", sans-serif`;
          scopeCtx.fillText(seg.sub, centerX, padTop - Math.round(6 * dpr));
        }
      } else if (seg.name === "SEP") {
        if (!isCompact) {
          scopeCtx.textAlign = "center";
          scopeCtx.fillStyle = "#575d66";
          scopeCtx.font = `400 ${subFontPx}px "IBM Plex Mono", monospace`;
          scopeCtx.fillText("SEP 4.5 ms", xOfMs(102.25), padTop - Math.round(20 * dpr));
        }
      } else if (seg.start === 104.5) {
        if (!isCompact) {
          scopeCtx.textAlign = "center";
          scopeCtx.fillStyle = "#575d66";
          scopeCtx.font = `400 ${subFontPx}px "IBM Plex Mono", monospace`;
          scopeCtx.fillText("PORCH 1.5 ms", xOfMs(105.25), padTop - Math.round(6 * dpr));
        }
      }
    }

    // Horizontal frequency grid lines: 1200 / 1500 / 1900 / 2300 Hz
    scopeCtx.font = `400 ${Math.round(10.5 * dpr)}px "IBM Plex Mono", monospace`;
    scopeCtx.textAlign = "right";
    scopeCtx.textBaseline = "middle";
    for (const hz of [1200, 1500, 1900, 2300]) {
      const y = Math.round(yOfHz(hz)) + 0.5;
      scopeCtx.strokeStyle = "rgba(14, 16, 19, 0.14)";
      scopeCtx.lineWidth = Math.max(1, dpr);
      scopeCtx.beginPath();
      scopeCtx.moveTo(padLeft, y);
      scopeCtx.lineTo(padLeft + plotW, y);
      scopeCtx.stroke();

      scopeCtx.fillStyle = "#575d66";
      scopeCtx.fillText(isCompact ? `${hz}` : `${hz} Hz`, padLeft - Math.round(8 * dpr), y);
    }

    // Bottom X-axis ticks: 0 to 150 ms every 25 ms
    scopeCtx.textAlign = "center";
    scopeCtx.textBaseline = "top";
    scopeCtx.fillStyle = "#575d66";
    for (let ms = 0; ms <= 150; ms += 25) {
      const x = Math.round(xOfMs(ms)) + 0.5;
      scopeCtx.strokeStyle = "rgba(14, 16, 19, 0.2)";
      scopeCtx.beginPath();
      scopeCtx.moveTo(x, padTop + plotH);
      scopeCtx.lineTo(x, padTop + plotH + Math.round(5 * dpr));
      scopeCtx.stroke();
      const label = ms === 150 ? "150 ms" : `${ms}`;
      const tx = ms === 0 ? x + 4 * dpr : ms === 150 ? x - 14 * dpr : x;
      scopeCtx.fillText(label, tx, padTop + plotH + Math.round(8 * dpr));
    }

    // Plot outer frame border
    scopeCtx.strokeStyle = "rgba(14, 16, 19, 0.22)";
    scopeCtx.lineWidth = Math.max(1, dpr);
    scopeCtx.strokeRect(padLeft + 0.5, padTop + 0.5, plotW - 1, plotH - 1);

    // Build waveform points from sample 0 row
    const sample0 = sampleStore.get(SAMPLES[0].key);
    const pts = [];
    const isEven = selectedScopeRow % 2 === 0;

    // 1. SYNC 0..9 ms @ 1200 Hz
    pts.push([xOfMs(0), yOfHz(1200)]);
    pts.push([xOfMs(9), yOfHz(1200)]);

    // 2. PORCH 9..12 ms @ 1500 Hz
    pts.push([xOfMs(9), yOfHz(1500)]);
    pts.push([xOfMs(12), yOfHz(1500)]);

    // 3. Y 12..100 ms: 320 samples
    for (let col = 0; col < 320; col++) {
      const ms = 12 + (col / 319) * 88;
      const lum = sample0 ? sample0.lum[selectedScopeRow * 320 + col] : 128;
      const f = 1500 + (lum / 255) * 800;
      pts.push([xOfMs(ms), yOfHz(f)]);
    }

    // 4. SEP 100..104.5 ms: 1500 Hz even / 2300 Hz odd
    const sepHz = isEven ? 1500 : 2300;
    pts.push([xOfMs(100), yOfHz(sepHz)]);
    pts.push([xOfMs(104.5), yOfHz(sepHz)]);

    // 5. PORCH 104.5..106 ms @ 1900 Hz
    pts.push([xOfMs(104.5), yOfHz(1900)]);
    pts.push([xOfMs(106), yOfHz(1900)]);

    // 6. R-Y / B-Y 106..150 ms: 160 samples (pairs of pixels)
    for (let i = 0; i < 160; i++) {
      const col = i * 2;
      const ms = 106 + (i / 159) * 44;
      let val = 128;
      if (sample0) {
        const idx = (selectedScopeRow * 320 + col) * 4;
        const r = sample0.rgba[idx];
        const g = sample0.rgba[idx + 1];
        const b = sample0.rgba[idx + 2];
        const yVal = 0.299 * r + 0.587 * g + 0.114 * b;
        val = isEven
          ? 128 + 0.713 * (r - yVal)
          : 128 + 0.564 * (b - yVal);
        val = Math.max(0, Math.min(255, val));
      }
      const f = 1500 + (val / 255) * 800;
      pts.push([xOfMs(ms), yOfHz(f)]);
    }

    scopeCtx.beginPath();
    scopeCtx.strokeStyle = "#0e1013";
    scopeCtx.lineWidth = 1.5 * dpr;
    scopeCtx.lineJoin = "round";
    for (let i = 0; i < pts.length; i++) {
      const [px, py] = pts[i];
      if (i === 0) scopeCtx.moveTo(px, py);
      else scopeCtx.lineTo(px, py);
    }
    scopeCtx.stroke();
  }

  // Cover: Starfield Canvas & Polar Sky Chart SVG
  const coverSection = document.getElementById("top");
  const starsCanvas = document.getElementById("cover-stars");
  const starsCtx = starsCanvas ? starsCanvas.getContext("2d") : null;
  const passReadoutEl = document.getElementById("pass-readout");
  const skyGrid = document.getElementById("sky-grid");
  const skyTrack = document.getElementById("sky-track");
  const skyRings = document.getElementById("sky-rings");
  const skyMarkers = document.getElementById("sky-markers");
  const skyIss = document.getElementById("sky-iss");

  // Seeded starfield (~260 stars, bottom 18% attenuated for atmospheric extinction)
  const STARS = (() => {
    const list = [];
    let seed = 884217;
    const rand = () => {
      seed = (seed * 16807) % 2147483647;
      return (seed - 1) / 2147483646;
    };
    for (let i = 0; i < 260; i++) {
      const x = rand();
      const y = rand();
      const r = 0.4 + rand() * 0.9;
      let alpha = 0.15 + rand() * 0.6;
      if (y > 0.82) alpha *= 0.4;
      const warm = rand() < 0.04;
      list.push({ x, y, r, alpha, warm });
    }
    return list;
  })();

  function drawCoverStars() {
    if (!starsCanvas || !starsCtx) return;
    if (!syncCanvasSize(starsCanvas)) return;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const w = starsCanvas.width;
    const h = starsCanvas.height;
    starsCtx.clearRect(0, 0, w, h);
    for (const s of STARS) {
      starsCtx.beginPath();
      starsCtx.arc(s.x * w, s.y * h, s.r * dpr, 0, Math.PI * 2);
      starsCtx.fillStyle = s.warm
        ? `rgba(255, 214, 170, ${s.alpha.toFixed(3)})`
        : `rgba(223, 230, 240, ${s.alpha.toFixed(3)})`;
      starsCtx.fill();
    }
  }

  const SVG_NS = "http://www.w3.org/2000/svg";
  function svgEl(tag, attrs = {}) {
    const el = document.createElementNS(SVG_NS, tag);
    for (const [k, v] of Object.entries(attrs)) {
      el.setAttribute(k, String(v));
    }
    return el;
  }

  function polarToXY(elDeg, azDeg, radius = 100) {
    const r = (radius * (90 - elDeg)) / 90;
    const rad = (azDeg * Math.PI) / 180;
    return {
      x: r * Math.sin(rad),
      y: -r * Math.cos(rad)
    };
  }

  const EARTH_R_KM = 6371;
  const ISS_ALT_KM = 420;
  const ORBIT_R_KM = EARTH_R_KM + ISS_ALT_KM;
  const PASS_EL_MAX_RAD = (68 * Math.PI) / 180;
  const PASS_AZ_TCA_RAD = (45 * Math.PI) / 180;   // NE
  const PASS_AZ_TRACK_RAD = (135 * Math.PI) / 180; // NW -> SE
  const PASS_ALPHA0 = Math.acos((EARTH_R_KM / ORBIT_R_KM) * Math.cos(PASS_EL_MAX_RAD)) - PASS_EL_MAX_RAD;
  const PASS_PSI_MAX = Math.acos(EARTH_R_KM / (ORBIT_R_KM * Math.cos(PASS_ALPHA0)));
  const ISS_OMEGA_RAD_S = Math.sqrt(398600.4418 / (ORBIT_R_KM * ORBIT_R_KM * ORBIT_R_KM));
  const RX_FREQ_KHZ = 145800;
  const SPEED_OF_LIGHT_KMS = 299792.458;

  function passPoint(t) {
    const psi = (2 * t - 1) * PASS_PSI_MAX;
    const cosPsi = Math.cos(psi);
    const sinPsi = Math.sin(psi);
    const u = ORBIT_R_KM * sinPsi;
    const v = ORBIT_R_KM * cosPsi * Math.sin(PASS_ALPHA0);
    const w = ORBIT_R_KM * cosPsi * Math.cos(PASS_ALPHA0) - EARTH_R_KM;
    const horiz = Math.hypot(u, v);
    const el = Math.max(0, (Math.atan2(w, horiz) * 180) / Math.PI);
    const east = u * Math.sin(PASS_AZ_TRACK_RAD) + v * Math.sin(PASS_AZ_TCA_RAD);
    const north = u * Math.cos(PASS_AZ_TRACK_RAD) + v * Math.cos(PASS_AZ_TCA_RAD);
    const az = ((Math.atan2(east, north) * 180) / Math.PI + 360) % 360;
    const slant = Math.hypot(horiz, w);
    const rangeRate = ((EARTH_R_KM * ORBIT_R_KM * Math.cos(PASS_ALPHA0) * sinPsi) / slant) * ISS_OMEGA_RAD_S;
    const df = -RX_FREQ_KHZ * (rangeRate / SPEED_OF_LIGHT_KMS);
    const pos = polarToXY(el, az, 100);
    return { az, el, df, x: pos.x, y: pos.y };
  }

  let trailPath = null;
  let trailGlowPath = null;
  let trailTotalLen = 0;
  let trailCumLen = [0];
  let trailSteps = 160;
  let issHalo = null;
  let issDot = null;
  let issLabel = null;

  function trailLenAt(t) {
    const clamped = Math.max(0, Math.min(1, t));
    const idxFloat = clamped * trailSteps;
    const i0 = Math.floor(idxFloat);
    const i1 = Math.min(trailSteps, i0 + 1);
    const frac = idxFloat - i0;
    const approx = trailCumLen[i0] + (trailCumLen[i1] - trailCumLen[i0]) * frac;
    const totalApprox = trailCumLen[trailSteps] || 1;
    return approx * (trailTotalLen / totalApprox);
  }

  function buildSkyChart() {
    if (!skyGrid || !skyTrack || !skyMarkers || !skyIss) return;
    skyGrid.replaceChildren();
    skyTrack.replaceChildren();
    skyMarkers.replaceChildren();
    skyIss.replaceChildren();

    // Elevation circles: 0, 30, 60 deg
    const elevCircles = [
      { el: 0, stroke: "rgba(255, 255, 255, 0.22)" },
      { el: 30, stroke: "rgba(255, 255, 255, 0.12)" },
      { el: 60, stroke: "rgba(255, 255, 255, 0.12)" }
    ];
    for (const c of elevCircles) {
      const r = (100 * (90 - c.el)) / 90;
      skyGrid.append(
        svgEl("circle", {
          cx: 0,
          cy: 0,
          r: r.toFixed(2),
          fill: "none",
          stroke: c.stroke,
          "stroke-width": 0.25
        })
      );
    }

    // Center zenith crosshair (length 6)
    skyGrid.append(
      svgEl("line", { x1: -3, y1: 0, x2: 3, y2: 0, stroke: "rgba(255,255,255,0.2)", "stroke-width": 0.25 }),
      svgEl("line", { x1: 0, y1: -3, x2: 0, y2: 3, stroke: "rgba(255,255,255,0.2)", "stroke-width": 0.25 })
    );

    // Azimuth radials (every 30 deg) & outer degree ticks (every 10 deg / 30 deg)
    for (let deg = 0; deg < 360; deg += 10) {
      const rad = (deg * Math.PI) / 180;
      const sx = Math.sin(rad);
      const cy = -Math.cos(rad);
      const isMajor = deg % 30 === 0;
      if (isMajor) {
        skyGrid.append(
          svgEl("line", {
            x1: 0,
            y1: 0,
            x2: (100 * sx).toFixed(2),
            y2: (100 * cy).toFixed(2),
            stroke: "rgba(255, 255, 255, 0.05)",
            "stroke-width": 0.25
          })
        );
      }
      const rIn = isMajor ? 95 : 98;
      skyGrid.append(
        svgEl("line", {
          x1: (rIn * sx).toFixed(2),
          y1: (rIn * cy).toFixed(2),
          x2: (100 * sx).toFixed(2),
          y2: (100 * cy).toFixed(2),
          stroke: isMajor ? "rgba(255, 255, 255, 0.24)" : "rgba(255, 255, 255, 0.12)",
          "stroke-width": 0.25
        })
      );
    }

    // Cardinal direction labels at r = 108
    const cardinals = [
      { label: "N", deg: 0 },
      { label: "E", deg: 90 },
      { label: "S", deg: 180 },
      { label: "W", deg: 270 }
    ];
    for (const dir of cardinals) {
      const rad = (dir.deg * Math.PI) / 180;
      const tx = 108 * Math.sin(rad);
      const ty = -108 * Math.cos(rad);
      const t = svgEl("text", {
        x: tx.toFixed(2),
        y: ty.toFixed(2),
        fill: "#8b9099",
        "font-family": '"IBM Plex Mono", monospace',
        "font-size": 4.2,
        "text-anchor": "middle",
        "dominant-baseline": "central"
      });
      t.textContent = dir.label;
      skyGrid.append(t);
    }

    // Elevation angle labels along north axis inside each ring (x + 2)
    for (const el of [0, 30, 60]) {
      const r = (100 * (90 - el)) / 90;
      const t = svgEl("text", {
        x: 2,
        y: (-r + 4.8).toFixed(2),
        fill: "#8b9099",
        "font-family": '"IBM Plex Mono", monospace',
        "font-size": 4.2
      });
      t.textContent = `${el}°`;
      skyGrid.append(t);
    }

    // Trajectory path (160 segments)
    let d = "";
    const steps = trailSteps;
    trailCumLen = [0];
    let prevPt = null;
    for (let i = 0; i <= steps; i++) {
      const p = passPoint(i / steps);
      d += (i === 0 ? "M" : "L") + `${p.x.toFixed(2)} ${p.y.toFixed(2)}`;
      if (prevPt) {
        trailCumLen.push(trailCumLen[i - 1] + Math.hypot(p.x - prevPt.x, p.y - prevPt.y));
      }
      prevPt = p;
    }

    skyTrack.append(
      svgEl("path", {
        d,
        fill: "none",
        stroke: "rgba(255, 255, 255, 0.35)",
        "stroke-width": 0.35,
        "stroke-dasharray": "1.2 1.6"
      })
    );

    trailGlowPath = svgEl("path", {
      d,
      fill: "none",
      stroke: "#ff5b24",
      "stroke-width": 2.4,
      opacity: 0.18,
      "stroke-linecap": "round"
    });
    trailPath = svgEl("path", {
      d,
      fill: "none",
      stroke: "#ff5b24",
      "stroke-width": 0.9,
      "stroke-linecap": "round"
    });
    skyTrack.append(trailGlowPath, trailPath);

    trailTotalLen = trailPath.getTotalLength ? trailPath.getTotalLength() : 210;
    for (const pEl of [trailGlowPath, trailPath]) {
      pEl.style.strokeDasharray = `${trailTotalLen}`;
      pEl.style.strokeDashoffset = `${trailTotalLen}`;
    }

    // AOS / TCA / LOS markers
    const milestones = [
      { t: 0, text: "AOS 18:42:10", dx: 4, dy: -3.5, anchor: "start" },
      { t: 0.5, text: "TCA 18:47:05 · 68°", dx: 4, dy: -3.5, anchor: "start" },
      { t: 1, text: "LOS 18:52:00", dx: -4, dy: 5.5, anchor: "end" }
    ];
    for (const m of milestones) {
      const pt = passPoint(m.t);
      skyMarkers.append(
        svgEl("circle", {
          cx: pt.x.toFixed(2),
          cy: pt.y.toFixed(2),
          r: 1.2,
          fill: "#f2f3f0"
        })
      );
      const lbl = svgEl("text", {
        x: (pt.x + m.dx).toFixed(2),
        y: (pt.y + m.dy).toFixed(2),
        fill: "#8b9099",
        "font-family": '"IBM Plex Mono", monospace',
        "font-size": 4.2,
        "text-anchor": m.anchor
      });
      lbl.textContent = m.text;
      skyMarkers.append(lbl);
    }

    // ISS active dot + halo + label
    issHalo = svgEl("circle", { cx: 0, cy: 0, r: 5, fill: "#ff5b24", opacity: 0.18 });
    issDot = svgEl("circle", { cx: 0, cy: 0, r: 2.2, fill: "#ff5b24" });
    issLabel = svgEl("text", {
      x: 4,
      y: -4,
      fill: "#f2f3f0",
      "font-family": '"IBM Plex Mono", monospace',
      "font-size": 4.2
    });
    issLabel.textContent = "ISS";
    skyIss.append(issHalo, issDot, issLabel);
  }

  let coverT = 0.22;
  let coverHoldMs = 0;
  let coverLastTs = 0;
  let coverRafId = null;
  let coverVisible = true;
  let ringAccumMs = 2200;
  const activeRings = [];

  function formatPassTime(t) {
    const startSec = 18 * 3600 + 42 * 60 + 10;
    const totalSec = Math.round(startSec + t * 590);
    const hh = String(Math.floor(totalSec / 3600)).padStart(2, "0");
    const mm = String(Math.floor((totalSec % 3600) / 60)).padStart(2, "0");
    const ss = String(totalSec % 60).padStart(2, "0");
    return `${hh}:${mm}:${ss}`;
  }

  function renderCoverState(t) {
    const pt = passPoint(t);
    const offset = Math.max(0, trailTotalLen - trailLenAt(t));
    if (trailPath) trailPath.style.strokeDashoffset = `${offset.toFixed(2)}`;
    if (trailGlowPath) trailGlowPath.style.strokeDashoffset = `${offset.toFixed(2)}`;

    if (issHalo && issDot && issLabel) {
      const cx = pt.x.toFixed(2);
      const cy = pt.y.toFixed(2);
      issHalo.setAttribute("cx", cx);
      issHalo.setAttribute("cy", cy);
      issDot.setAttribute("cx", cx);
      issDot.setAttribute("cy", cy);
      issLabel.setAttribute("x", (pt.x + 4).toFixed(2));
      issLabel.setAttribute("y", (pt.y - 4).toFixed(2));
    }

    if (passReadoutEl) {
      const azStr = String(Math.round(pt.az) % 360).padStart(3, "0");
      const elStr = String(Math.round(pt.el)).padStart(2, "0");
      const roundedDf = Math.abs(pt.df) < 0.05 ? 0 : pt.df;
      const sign = roundedDf >= 0 ? "+" : "-";
      const dfAbs = Math.abs(roundedDf).toFixed(1);
      passReadoutEl.textContent = `AZ ${azStr}° · EL ${elStr}° · Δf ${sign}${dfAbs} kHz · ${formatPassTime(t)}`;
    }
  }

  function spawnWaveRing(x, y) {
    if (!skyRings) return;
    while (activeRings.length >= 3) {
      const oldest = activeRings.shift();
      oldest.el.remove();
    }
    const el = svgEl("circle", {
      cx: x.toFixed(2),
      cy: y.toFixed(2),
      r: 2,
      fill: "none",
      stroke: "#ff5b24",
      "stroke-width": 0.3,
      opacity: 0.5
    });
    skyRings.append(el);
    activeRings.push({ el, ageMs: 0 });
  }

  function stepCover(ts) {
    if (!coverLastTs) coverLastTs = ts;
    const dt = Math.min(64, ts - coverLastTs);
    coverLastTs = ts;

    if (coverT < 1) {
      coverT = Math.min(1, coverT + dt / 16000);
      ringAccumMs += dt;
      if (ringAccumMs >= 2200) {
        ringAccumMs %= 2200;
        const pt = passPoint(coverT);
        spawnWaveRing(pt.x, pt.y);
      }
    } else {
      coverHoldMs += dt;
      if (coverHoldMs >= 1500) {
        coverHoldMs = 0;
        coverT = 0;
        ringAccumMs = 2200;
      }
    }

    // Update pulsing radio rings (1.4s expansion from r=2 to 16)
    for (let i = activeRings.length - 1; i >= 0; i--) {
      const ring = activeRings[i];
      ring.ageMs += dt;
      const p = ring.ageMs / 1400;
      if (p >= 1) {
        ring.el.remove();
        activeRings.splice(i, 1);
      } else {
        ring.el.setAttribute("r", (2 + p * 14).toFixed(2));
        ring.el.setAttribute("opacity", (0.5 * (1 - p)).toFixed(3));
      }
    }

    renderCoverState(coverT);

    if (coverVisible && !document.hidden && !reducedMotion.matches) {
      coverRafId = window.requestAnimationFrame(stepCover);
    } else {
      coverRafId = null;
    }
  }

  function startCoverLoop() {
    if (reducedMotion.matches) {
      coverT = 0.5;
      renderCoverState(0.5);
      return;
    }
    if (!coverRafId && coverVisible && !document.hidden) {
      coverLastTs = 0;
      coverRafId = window.requestAnimationFrame(stepCover);
    }
  }

  function stopCoverLoop() {
    if (coverRafId) {
      window.cancelAnimationFrame(coverRafId);
      coverRafId = null;
    }
  }

  if ("IntersectionObserver" in window && coverSection) {
    const coverObs = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          coverVisible = entry.isIntersecting;
          if (coverVisible) startCoverLoop();
          else stopCoverLoop();
        }
      },
      { threshold: 0.05 }
    );
    coverObs.observe(coverSection);
  }

  document.addEventListener("visibilitychange", () => {
    if (document.hidden) stopCoverLoop();
    else startCoverLoop();
  });

  // Captures pixel/smooth render tabs
  const captureGrid = document.getElementById("capture-grid");
  const renderTabs = Array.from(document.querySelectorAll(".render-tab"));
  for (const tab of renderTabs) {
    tab.addEventListener("click", () => {
      const mode = tab.dataset.render === "smooth" ? "smooth" : "pixelated";
      for (const t of renderTabs) {
        t.setAttribute("aria-selected", String(t === tab));
      }
      if (captureGrid) {
        captureGrid.classList.toggle("is-smooth", mode === "smooth");
      }
    });
  }

  // Generic mini copy buttons (.copy-mini)
  async function copyTextToClipboard(text) {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch {
      const ta = document.createElement("textarea");
      ta.value = text;
      ta.style.position = "fixed";
      ta.style.opacity = "0";
      document.body.append(ta);
      ta.select();
      const ok = document.execCommand("copy");
      ta.remove();
      return ok;
    }
  }

  const miniTimers = new WeakMap();
  for (const btn of document.querySelectorAll(".copy-mini")) {
    btn.addEventListener("click", async () => {
      const targetId = btn.dataset.copyTarget;
      const targetEl = targetId ? document.getElementById(targetId) : null;
      if (!targetEl) return;
      const ok = await copyTextToClipboard(targetEl.textContent || "");
      if (ok) {
        const dict = I18N[currentLang] || I18N["zh-CN"];
        btn.textContent = dict.copied_btn;
        const prev = miniTimers.get(btn);
        if (prev) window.clearTimeout(prev);
        const timer = window.setTimeout(() => {
          const activeDict = I18N[currentLang] || I18N["zh-CN"];
          btn.textContent = activeDict.copy_btn;
        }, 1800);
        miniTimers.set(btn, timer);
      }
    });
  }

  // Init
  const initialLang = new URLSearchParams(window.location.search).get("lang");
  if (initialLang === "en") {
    applyLanguage("en");
  }
  buildSkyChart();
  drawCoverStars();
  renderCoverState(reducedMotion.matches ? 0.5 : coverT);
  startCoverLoop();

  updateHeroSampleMeta();
  syncCommandBlock();
  syncAllCanvases();
  updatePickerRow(120);
  startHeroLoop();

  window.addEventListener("resize", () => {
    drawCoverStars();
    syncAllCanvases();
  });
})();

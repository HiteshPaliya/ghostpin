"""
GhostPin v5.0 — Web UI HTML
Single-file, self-contained frontend for the GhostPin platform.
"""

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>GhostPin</title>
<link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>
<link rel="preload" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Syne:wght@400;600;700;800&display=swap" as="style" onload="this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Syne:wght@400;600;700;800&display=swap"></noscript>
<style>
:root{
  --ink:#080b12;--ink1:#0d1018;--ink2:#111520;--ink3:#171c29;--ink4:#1d2333;--ink5:#232a3e;
  --rim:#252d42;--rim2:#2e3850;--rim3:#3a4866;
  --lime:#b8ff47;--lime2:#8fd630;--lime3:#4a7a10;
  --limebg:rgba(184,255,71,.07);--limeglow:0 0 28px rgba(184,255,71,.3);
  --cyan:#3de8ff;--cyanbg:rgba(61,232,255,.07);
  --red:#ff4d6a;--redbg:rgba(255,77,106,.08);
  --amber:#ffaa33;--amberbg:rgba(255,170,51,.08);
  --mint:#2effa0;--mintbg:rgba(46,255,160,.07);
  --violet:#b47aff;--violetbg:rgba(180,122,255,.07);
  --txt:#d8e0f4;--txt2:#8892bc;--txt3:#4a5278;--txt4:#272c42;
  --mono:'JetBrains Mono','Cascadia Code','Fira Code','Consolas','Courier New',monospace;
  --sans:'Syne','Inter','Segoe UI','Helvetica Neue',system-ui,sans-serif;
  --nav:58px;--side:252px;--top:50px;--r:8px;--rl:14px;
  --theme-transition: background-color .2s ease,color .2s ease,border-color .2s ease,box-shadow .2s ease;
}

/* ── LIGHT MODE OVERRIDES ────────────────────────────────────── */
[data-theme="light"]{
  --ink:#f0f2fa;--ink1:#e8eaf5;--ink2:#dfe2f0;--ink3:#d4d8eb;--ink4:#c8cde3;--ink5:#bdc2db;
  --rim:#c4c9e0;--rim2:#b0b6d0;--rim3:#9aa1bf;
  --lime:#4a8a00;--lime2:#3d7200;--lime3:#b8ff47;
  --limebg:rgba(74,138,0,.09);--limeglow:0 0 20px rgba(74,138,0,.18);
  --cyan:#0080a0;--cyanbg:rgba(0,128,160,.08);
  --red:#c42040;--redbg:rgba(196,32,64,.08);
  --amber:#b06000;--amberbg:rgba(176,96,0,.08);
  --mint:#008855;--mintbg:rgba(0,136,85,.08);
  --violet:#6030b8;--violetbg:rgba(96,48,184,.08);
  --txt:#1a1e38;--txt2:#383e62;--txt3:#6870a0;--txt4:#b0b8d8;
}
[data-theme="light"] *,[data-theme="light"] *::before,[data-theme="light"] *::after{
  transition:var(--theme-transition);
}
[data-theme="light"] code{background:rgba(74,138,0,.1);}
[data-theme="light"] .logo-box{filter:none;}
[data-theme="light"] .term{background:#1a1e38;border-color:#2a2e50;}
[data-theme="light"] .term-hd{background:#13162e;border-color:#2a2e50;}
[data-theme="light"] .ca{background:#1a1e38;color:#d8e0f4;border-color:#2a2e50;}
[data-theme="light"] .ca:focus{border-color:var(--lime);}

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html,body{height:100%;overflow:hidden;background:var(--ink);color:var(--txt);font-family:var(--mono);font-size:13px;-webkit-font-smoothing:antialiased;}
::-webkit-scrollbar{width:4px;height:4px;}
::-webkit-scrollbar-track{background:var(--ink2);}
::-webkit-scrollbar-thumb{background:var(--rim2);border-radius:2px;}
::-webkit-scrollbar-thumb:hover{background:var(--rim3);}

#shell{display:grid;grid-template-columns:var(--nav) var(--side) minmax(0,1fr);grid-template-rows:var(--top) minmax(0,1fr);height:100vh;}

/* TOPBAR */
#topbar{grid-column:1/-1;background:var(--ink1);border-bottom:1px solid var(--rim);display:flex;align-items:center;padding:0 16px;gap:10px;z-index:100;position:sticky;top:0;}
.logo-box{width:32px;height:32px;border-radius:8px;background:var(--lime);display:flex;align-items:center;justify-content:center;font-family:var(--sans);font-weight:800;font-size:16px;color:#000;box-shadow:var(--limeglow);flex-shrink:0;}
.brand{font-family:var(--sans);font-size:15px;font-weight:800;letter-spacing:-.3px;}
.brand b{color:var(--lime);}
.ver-tag{font-size:10px;color:var(--txt3);background:var(--ink3);padding:2px 8px;border-radius:4px;border:1px solid var(--rim);letter-spacing:.5px;flex-shrink:0;}
.theme-btn{width:32px;height:32px;border-radius:8px;border:1px solid var(--rim2);background:var(--ink3);color:var(--txt2);cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:15px;flex-shrink:0;transition:all .15s;}
.theme-btn:hover{background:var(--ink4);color:var(--txt);border-color:var(--rim3);}
.sep{width:1px;height:20px;background:var(--rim);flex-shrink:0;}
.tb-page{font-family:var(--sans);font-size:13px;font-weight:700;color:var(--txt2);}
.flex1{flex:1;}
.sb{display:flex;align-items:center;gap:5px;padding:4px 10px;border-radius:20px;font-size:10px;font-weight:600;border:1px solid;cursor:default;letter-spacing:.3px;white-space:nowrap;transition:all .2s;}
.sb-dot{width:5px;height:5px;border-radius:50%;flex-shrink:0;}
.sb-ok{border-color:rgba(46,255,160,.25);color:var(--mint);background:var(--mintbg);}
.sb-ok .sb-dot{background:var(--mint);box-shadow:0 0 6px var(--mint);animation:sbpulse 2s infinite;}
.sb-warn{border-color:rgba(255,170,51,.25);color:var(--amber);background:var(--amberbg);}
.sb-warn .sb-dot{background:var(--amber);}
.sb-off{border-color:var(--rim);color:var(--txt3);}
.sb-off .sb-dot{background:var(--txt3);}
.sb-err{border-color:rgba(255,77,106,.25);color:var(--red);background:var(--redbg);}
.sb-err .sb-dot{background:var(--red);}
@keyframes sbpulse{0%,100%{opacity:1;}50%{opacity:.35;}}

/* RAIL */
#rail{grid-row:2;background:var(--ink1);border-right:1px solid var(--rim);display:flex;flex-direction:column;align-items:center;padding:10px 0;gap:2px;overflow:visible;z-index:50;}
.rb{width:40px;height:40px;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:17px;cursor:pointer;color:var(--txt3);transition:all .15s;border:1px solid transparent;position:relative;flex-shrink:0;user-select:none;}
.rb:hover{background:var(--ink3);color:var(--txt2);}
.rb.on{background:var(--limebg);color:var(--lime);border-color:rgba(184,255,71,.22);box-shadow:inset 0 0 20px rgba(184,255,71,.06);}
.rb-tip{position:absolute;left:48px;top:50%;transform:translateY(-50%);background:var(--ink4);border:1px solid var(--rim2);color:var(--txt);font-size:11px;padding:4px 10px;border-radius:5px;white-space:nowrap;opacity:0;pointer-events:none;transition:opacity .12s;z-index:9999;}
.rb:hover .rb-tip{opacity:1;}
.rdiv{width:26px;height:1px;background:var(--rim);margin:4px 0;flex-shrink:0;}
.rspc{flex:1;}
.rbadge{position:absolute;top:4px;right:4px;background:var(--red);color:#fff;font-size:8px;font-weight:700;min-width:14px;height:14px;border-radius:7px;display:flex;align-items:center;justify-content:center;padding:0 3px;border:1.5px solid var(--ink1);}

/* SIDEBAR */
#sidebar{grid-row:2;background:var(--ink1);border-right:1px solid var(--rim);display:flex;flex-direction:column;overflow:hidden;}
.sbh{padding:9px 14px 8px;border-bottom:1px solid var(--rim);flex-shrink:0;}
.sbh-title{font-family:var(--sans);font-size:11px;font-weight:800;letter-spacing:.8px;text-transform:uppercase;color:var(--txt2);}
.sbh-sub{font-size:10px;color:var(--txt3);margin-top:2px;}
.sbb{flex:1;overflow-y:auto;padding:6px 4px;min-height:0;}
.ng{margin-bottom:2px;}
.ng-lbl{font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--txt4);padding:3px 8px 2px;display:block;font-weight:700;}
.ni{display:flex;align-items:center;gap:8px;padding:5px 10px;border-radius:6px;cursor:pointer;font-size:12px;color:var(--txt3);transition:all .12s;border:1px solid transparent;user-select:none;}
.ni:hover{background:var(--ink3);color:var(--txt2);}
.ni.on{background:var(--limebg);color:var(--lime);border-color:rgba(184,255,71,.15);}
.ni-ic{font-size:14px;width:18px;text-align:center;flex-shrink:0;}
.ni-lbl{flex:1;}
.pill{font-size:9px;font-weight:700;padding:2px 6px;border-radius:4px;letter-spacing:.5px;text-transform:uppercase;}
.p-new{background:rgba(184,255,71,.15);color:var(--lime);}
.p-live{background:rgba(255,77,106,.15);color:var(--red);}
.p-beta{background:rgba(61,232,255,.12);color:var(--cyan);}
.p-n{background:var(--ink4);color:var(--txt2);}

/* MAIN */
#main{grid-row:2;overflow-y:auto;padding:24px;background:var(--ink);min-height:0;min-width:0;}
.page{display:none;}
.page.on{display:block;}

/* PAGE HEADER */
.ph{margin-bottom:22px;}
.pt{font-family:var(--sans);font-size:22px;font-weight:800;letter-spacing:-.5px;}
.pt b{color:var(--lime);}
.ps{font-size:12px;color:var(--txt3);margin-top:4px;line-height:1.6;}
.pa{display:flex;gap:8px;margin-top:12px;flex-wrap:wrap;}

/* CARDS */
.card{background:var(--ink2);border:1px solid var(--rim);border-radius:var(--rl);overflow:hidden;transition:border-color .2s;}
.card:hover{border-color:var(--rim2);}
.ch{display:flex;align-items:center;justify-content:space-between;padding:12px 16px;border-bottom:1px solid var(--rim);gap:8px;flex-shrink:0;}
.ct{font-family:var(--sans);font-size:13px;font-weight:700;display:flex;align-items:center;gap:7px;}
.cb{padding:16px;}
.cb0{padding:0;}
.cf{padding:10px 16px;border-top:1px solid var(--rim);background:var(--ink3);display:flex;gap:8px;align-items:center;}

/* STATS */
.sc{background:var(--ink2);border:1px solid var(--rim);border-radius:var(--rl);padding:18px 20px;transition:all .2s;position:relative;overflow:hidden;}
.sc::before{content:'';position:absolute;inset:0;background:linear-gradient(135deg,rgba(255,255,255,.02),transparent);pointer-events:none;}
.sc:hover{border-color:var(--rim2);transform:translateY(-1px);}
.sc-acc{width:3px;height:34px;border-radius:2px;position:absolute;left:0;top:50%;transform:translateY(-50%);}
.sc-num{font-family:var(--sans);font-size:32px;font-weight:800;line-height:1;}
.sc-lbl{font-size:10px;text-transform:uppercase;letter-spacing:1.5px;color:var(--txt3);margin-top:5px;}
.sc-sub{font-size:11px;color:var(--txt3);margin-top:3px;}

/* BUTTONS */
.btn{display:inline-flex;align-items:center;gap:7px;padding:8px 16px;border-radius:7px;font-family:var(--mono);font-size:12px;font-weight:600;cursor:pointer;border:1px solid;transition:all .15s;text-decoration:none;white-space:nowrap;user-select:none;letter-spacing:.2px;}
.btn:disabled,.btn.disabled{opacity:.4;cursor:not-allowed;pointer-events:none;}
.btn-lime{background:var(--lime);color:#000;border-color:var(--lime);box-shadow:0 0 18px rgba(184,255,71,.2);}
.btn-lime:hover{background:#ccff5c;box-shadow:0 0 28px rgba(184,255,71,.4);}
.btn-ghost{background:transparent;color:var(--txt2);border-color:var(--rim2);}
.btn-ghost:hover{background:var(--ink3);color:var(--txt);border-color:var(--rim3);}
.btn-danger{background:var(--redbg);color:var(--red);border-color:rgba(255,77,106,.3);}
.btn-danger:hover{background:rgba(255,77,106,.15);}
.btn-cyan{background:var(--cyanbg);color:var(--cyan);border-color:rgba(61,232,255,.25);}
.btn-cyan:hover{background:rgba(61,232,255,.12);}
.btn-mint{background:var(--mintbg);color:var(--mint);border-color:rgba(46,255,160,.25);}
.btn-mint:hover{background:rgba(46,255,160,.12);}
.btn-sm{padding:5px 12px;font-size:11px;}
.btn-xs{padding:3px 9px;font-size:10px;}

/* FORMS */
.fg{margin-bottom:14px;}
.fl{display:block;font-size:10px;color:var(--txt3);margin-bottom:5px;letter-spacing:.8px;text-transform:uppercase;font-weight:600;}
.fi,.fsl,.fta{width:100%;padding:9px 12px;background:var(--ink);border:1px solid var(--rim2);border-radius:7px;color:var(--txt);font-family:var(--mono);font-size:12px;transition:border-color .15s;outline:none;appearance:none;}
.fi:focus,.fsl:focus,.fta:focus{border-color:var(--lime);box-shadow:0 0 0 2px rgba(184,255,71,.1);}
.fsl{cursor:pointer;}
.fta{min-height:90px;resize:vertical;line-height:1.65;}
.tw{display:flex;align-items:center;gap:10px;cursor:pointer;}
.tg{width:38px;height:20px;border-radius:10px;background:var(--rim2);border:1px solid var(--rim3);position:relative;transition:all .2s;flex-shrink:0;}
.tg::after{content:'';position:absolute;left:2px;top:2px;width:14px;height:14px;border-radius:7px;background:var(--txt3);transition:all .2s;}
.tg.on{background:var(--lime);border-color:var(--lime2);}
.tg.on::after{left:20px;background:#000;}
.tl{font-size:12px;color:var(--txt2);}

/* TAGS */
.tag{display:inline-flex;align-items:center;padding:2px 8px;border-radius:4px;font-size:10px;font-weight:700;letter-spacing:.4px;text-transform:uppercase;white-space:nowrap;}
.t-and{background:rgba(46,255,160,.1);color:var(--mint);border:1px solid rgba(46,255,160,.2);}
.t-ios{background:rgba(180,122,255,.1);color:var(--violet);border:1px solid rgba(180,122,255,.2);}
.t-ssl{background:rgba(184,255,71,.1);color:var(--lime);border:1px solid rgba(184,255,71,.2);}
.t-easy{background:var(--mintbg);color:var(--mint);border:1px solid rgba(46,255,160,.2);}
.t-medium{background:var(--amberbg);color:var(--amber);border:1px solid rgba(255,170,51,.2);}
.t-hard{background:var(--redbg);color:var(--red);border:1px solid rgba(255,77,106,.2);}
.t-expert{background:var(--violetbg);color:var(--violet);border:1px solid rgba(180,122,255,.2);}
.t-evasion{background:var(--cyanbg);color:var(--cyan);border:1px solid rgba(61,232,255,.2);}
.t-grpc{background:var(--amberbg);color:var(--amber);border:1px solid rgba(255,170,51,.2);}
.t-native{background:var(--redbg);color:var(--red);border:1px solid rgba(255,77,106,.2);}
.t-obfusc{background:var(--violetbg);color:var(--violet);border:1px solid rgba(180,122,255,.2);}
.t-flutter{background:var(--cyanbg);color:var(--cyan);border:1px solid rgba(61,232,255,.2);}
.t-both{background:var(--ink4);color:var(--txt2);border:1px solid var(--rim2);}
.t-critical{background:rgba(255,77,106,.18);color:var(--red);border:1px solid rgba(255,77,106,.3);}
.t-high{background:rgba(255,170,51,.14);color:var(--amber);border:1px solid rgba(255,170,51,.25);}
.t-medium2{background:var(--cyanbg);color:var(--cyan);border:1px solid rgba(61,232,255,.2);}
.t-low{background:var(--ink4);color:var(--txt2);border:1px solid var(--rim);}
.t-usb{background:var(--ink4);color:var(--txt2);border:1px solid var(--rim2);}
.t-wifi{background:var(--cyanbg);color:var(--cyan);border:1px solid rgba(61,232,255,.2);}
.t-root{background:var(--redbg);color:var(--red);border:1px solid rgba(255,77,106,.2);}
.t-noroot{background:var(--ink4);color:var(--txt3);border:1px solid var(--rim);}
.t-frida{background:var(--mintbg);color:var(--mint);border:1px solid rgba(46,255,160,.2);}
.t-nofrida{background:var(--ink4);color:var(--txt3);border:1px solid var(--rim);}

/* TABLE */
.tbl{width:100%;border-collapse:collapse;font-size:12px;}
.tbl th{text-align:left;padding:8px 14px;font-size:10px;text-transform:uppercase;letter-spacing:1px;color:var(--txt3);border-bottom:1px solid var(--rim);background:var(--ink3);font-weight:700;}
.tbl td{padding:8px 14px;border-bottom:1px solid var(--rim);color:var(--txt2);vertical-align:middle;}
.tbl tr:last-child td{border-bottom:none;}
.tbl tr:hover td{background:var(--ink3);}
.tbl code{font-family:var(--mono);font-size:11px;color:var(--lime);background:rgba(184,255,71,.07);padding:2px 6px;border-radius:4px;}

/* KV rows */
.kv{display:flex;gap:6px;padding:6px 0;border-bottom:1px solid var(--rim);}
.kv:last-child{border-bottom:none;}
.kv-k{width:140px;font-size:11px;color:var(--txt3);flex-shrink:0;padding-top:1px;}
.kv-v{font-size:12px;color:var(--txt);word-break:break-all;}

/* GRID */
.g2{display:grid;grid-template-columns:1fr 1fr;gap:16px;}
.g3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;}
.g4{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;}
.ga{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px;}

/* DEVICE CARD */
.dvc{background:var(--ink2);border:1px solid var(--rim);border-radius:var(--rl);padding:14px 16px;cursor:pointer;transition:all .15s;display:flex;align-items:flex-start;gap:12px;}
.dvc:hover{border-color:var(--rim2);background:var(--ink3);}
.dvc.sel{border-color:rgba(184,255,71,.4);background:var(--limebg);}
.dvc.fri{border-color:rgba(46,255,160,.3);}
.dv-ic{font-size:26px;flex-shrink:0;margin-top:2px;}
.dv-info{flex:1;min-width:0;}
.dv-name{font-family:var(--sans);font-size:13px;font-weight:700;}
.dv-ser{font-size:10px;color:var(--txt3);margin-top:1px;}
.dv-meta{font-size:11px;color:var(--txt3);margin-top:3px;}
.dv-tags{display:flex;gap:4px;margin-top:8px;flex-wrap:wrap;}
.dv-acts{display:flex;gap:5px;margin-top:10px;}

/* SCRIPT CARD */
.scc{background:var(--ink2);border:1px solid var(--rim);border-radius:var(--rl);padding:14px;cursor:pointer;transition:all .15s;position:relative;overflow:hidden;user-select:none;}
.scc::before{content:'';position:absolute;left:0;top:0;bottom:0;width:3px;background:transparent;transition:background .15s;}
.scc:hover{border-color:var(--rim2);background:var(--ink3);}
.scc.sel{border-color:rgba(184,255,71,.35);}
.scc.sel::before{background:var(--lime);}
.sc-ck{position:absolute;top:12px;right:12px;width:18px;height:18px;border-radius:5px;border:1.5px solid var(--rim2);background:var(--ink);display:flex;align-items:center;justify-content:center;font-size:11px;color:transparent;transition:all .15s;}
.scc.sel .sc-ck{background:var(--lime);border-color:var(--lime);color:#000;}
.sc-nm{font-family:var(--sans);font-size:13px;font-weight:700;padding-right:28px;}
.sc-ds{font-size:11px;color:var(--txt3);margin-top:4px;line-height:1.5;}
.sc-tg{display:flex;gap:5px;margin-top:10px;flex-wrap:wrap;}

/* TERMINAL */
.term{background:#050810;border:1px solid var(--rim);border-radius:var(--r);overflow:hidden;font-family:var(--mono);display:flex;flex-direction:column;}
.term-hd{display:flex;align-items:center;gap:7px;padding:8px 12px;background:var(--ink2);border-bottom:1px solid var(--rim);flex-shrink:0;}
.tdot{width:10px;height:10px;border-radius:50%;}
.term-bd{flex:1;overflow-y:auto;padding:10px 14px;line-height:1.65;}
.ll{display:flex;gap:8px;margin-bottom:1px;}
.lts{color:var(--txt4);font-size:10px;flex-shrink:0;padding-top:1px;white-space:nowrap;}
.llv{font-size:10px;font-weight:700;width:48px;flex-shrink:0;text-transform:uppercase;}
.lv-info{color:var(--txt3);}
.lv-frida{color:var(--lime);}
.lv-error{color:var(--red);}
.lv-warn{color:var(--amber);}
.lv-success{color:var(--mint);}
.lv-inject{color:var(--cyan);}
.lm{color:var(--txt2);word-break:break-all;flex:1;font-size:12px;}

/* PROGRESS */
.pbar{height:4px;background:var(--ink4);border-radius:2px;overflow:hidden;}
.pfill{height:100%;border-radius:2px;background:var(--lime);transition:width .4s ease;}
.stl{display:flex;flex-direction:column;gap:4px;}
.sti{display:flex;align-items:center;gap:8px;font-size:12px;padding:3px 0;}
.stdt{width:8px;height:8px;border-radius:50%;flex-shrink:0;}
.stdt.done{background:var(--mint);box-shadow:0 0 6px var(--mint);}
.stdt.act{background:var(--lime);animation:sbpulse 1s infinite;}
.stdt.idle{background:var(--txt4);}
.stdt.err{background:var(--red);}

/* DETECTION CARD */
.det{background:var(--ink3);border:1px solid var(--rim);border-radius:8px;padding:11px 14px;display:flex;align-items:flex-start;gap:10px;margin-bottom:8px;}
.det-ic{font-size:18px;flex-shrink:0;}
.det-tp{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.7px;}
.det-dt{font-size:11px;color:var(--txt3);margin-top:2px;}

/* TOOL GRID */
.tool-i{display:flex;align-items:center;gap:10px;padding:10px 14px;border-radius:8px;background:var(--ink3);border:1px solid var(--rim);}
.ti-nm{font-size:13px;font-weight:600;}
.ti-pt{font-size:10px;color:var(--txt3);margin-top:1px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}

/* CODE EDITOR */
.ced{background:#050810;border:1px solid var(--rim);border-radius:var(--r);overflow:hidden;}
.ced-hd{display:flex;align-items:center;gap:8px;padding:8px 12px;background:var(--ink2);border-bottom:1px solid var(--rim);}
.ca{width:100%;background:transparent;border:none;color:#b8ff47;font-family:var(--mono);font-size:12px;padding:14px;outline:none;resize:vertical;line-height:1.75;tab-size:2;}
.ca::placeholder{color:var(--txt4);}

/* SESSION ITEM */
.ssi{background:var(--ink2);border:1px solid var(--rim);border-radius:10px;padding:14px 16px;display:flex;align-items:center;gap:14px;transition:all .15s;}
.ssi:hover{border-color:var(--rim2);}
.ssi-ic{font-size:22px;flex-shrink:0;}
.ssi-nm{font-family:var(--sans);font-size:13px;font-weight:700;}
.ssi-mt{font-size:11px;color:var(--txt3);margin-top:2px;}
.ssi-acts{display:flex;gap:6px;flex-shrink:0;margin-left:auto;}

/* SPINNER */
.spin{display:inline-block;width:14px;height:14px;border:2px solid var(--rim2);border-top-color:var(--lime);border-radius:50%;animation:spinning .7s linear infinite;}
@keyframes spinning{to{transform:rotate(360deg);}}

/* TOAST */
#toasts{position:fixed;bottom:20px;right:20px;display:flex;flex-direction:column;gap:8px;z-index:9999;pointer-events:none;}
.toast{display:flex;align-items:center;gap:10px;padding:11px 16px;border-radius:10px;background:var(--ink3);border:1px solid var(--rim2);font-size:12px;pointer-events:all;box-shadow:0 4px 24px rgba(0,0,0,.6);animation:tslide .25s ease;max-width:340px;}
.toast.ok{border-color:rgba(46,255,160,.3);}
.toast.err{border-color:rgba(255,77,106,.3);}
.toast.warn{border-color:rgba(255,170,51,.3);}
@keyframes tslide{from{transform:translateX(20px);opacity:0;}to{transform:none;opacity:1;}}

/* MISC */
.div{height:1px;background:var(--rim);margin:18px 0;}
.stitle{font-family:var(--sans);font-size:15px;font-weight:800;margin-bottom:14px;display:flex;align-items:center;gap:8px;}
.mb8{margin-bottom:8px;}
.mb12{margin-bottom:12px;}
.mb16{margin-bottom:16px;}
.mb20{margin-bottom:20px;}
.mt8{margin-top:8px;}
.mt12{margin-top:12px;}
.flex{display:flex;}
.gap6{gap:6px;}
.gap8{gap:8px;}
.gap12{gap:12px;}
.fxc{align-items:center;}
.fxb{justify-content:space-between;}
.fx1{flex:1;}
.empty{text-align:center;padding:40px 20px;color:var(--txt3);}
.empty-ic{font-size:36px;margin-bottom:10px;}
.empty-tt{font-family:var(--sans);font-size:14px;font-weight:700;color:var(--txt2);}
.empty-sb{font-size:12px;margin-top:4px;}
code{font-family:var(--mono);font-size:11px;background:rgba(184,255,71,.07);color:var(--lime);padding:2px 6px;border-radius:4px;}

/* ANALYSIS PROGRESS BAR (animated) */
@keyframes indeterminate{0%{left:-40%;width:40%;}100%{left:100%;width:40%;}}
.pbar-indeterminate{height:3px;background:var(--ink4);border-radius:2px;overflow:hidden;position:relative;}
.pbar-indeterminate::after{content:'';position:absolute;top:0;height:100%;background:var(--lime);border-radius:2px;animation:indeterminate 1.2s infinite ease-in-out;}

/* Live session activity pulse */
@keyframes livepulse{0%{box-shadow:0 0 0 0 rgba(255,77,106,.5);}70%{box-shadow:0 0 0 8px rgba(255,77,106,0);}100%{box-shadow:0 0 0 0 rgba(255,77,106,0);}}
.live-dot{width:8px;height:8px;border-radius:50%;background:var(--red);animation:livepulse 1.5s infinite;flex-shrink:0;}

@media(max-width:1100px){:root{--side:210px;}}
@media(max-width:900px){#sidebar{display:none;}#shell{grid-template-columns:var(--nav) 1fr;}}
</style>
</head>
<body>
<div id="shell">

<!-- TOPBAR -->
<div id="topbar">
  <div class="logo-box">G</div>
  <div class="brand">Ghost<b>Pin</b></div>
  <div class="ver-tag">Enterprise v5.0</div>
  <div class="sep"></div>
  <div class="tb-page" id="tb-title">Dashboard</div>
  <div class="flex1"></div>
  <button class="theme-btn" id="theme-btn" onclick="toggleTheme()" title="Toggle light / dark mode">&#9790;</button>
  <div class="sb sb-off" id="sb-dev"><div class="sb-dot"></div><span id="sb-dev-t">No Devices</span></div>
  <div class="sb sb-off" id="sb-fri"><div class="sb-dot"></div><span id="sb-fri-t">Frida Off</span></div>
  <div class="sb sb-off" id="sb-sess"><div class="sb-dot"></div><span id="sb-sess-t">No Session</span></div>
  <div class="sb sb-off" id="sb-prx"><div class="sb-dot"></div><span id="sb-prx-t">Proxy Off</span></div>
  <button class="btn btn-ghost btn-xs" onclick="refreshAll()" style="margin-left:6px">&#8635; Refresh</button>
</div>

<!-- RAIL -->
<div id="rail">
  <div class="rb on" id="rb-dashboard" onclick="go('dashboard')">&#127968;<div class="rb-tip">Dashboard</div></div>
  <div class="rb" id="rb-devices" onclick="go('devices')">&#128241;<div class="rb-tip">Devices</div><div class="rbadge" id="rb-dev-badge" style="display:none">0</div></div>
  <div class="rdiv"></div>
  <div class="rb" id="rb-bypass" onclick="go('bypass')">&#9889;<div class="rb-tip">Run Bypass</div></div>
  <div class="rb" id="rb-scripts" onclick="go('scripts')">&#128218;<div class="rb-tip">Script Library</div></div>
  <div class="rb" id="rb-editor" onclick="go('editor')">&#9998;<div class="rb-tip">Script Editor</div></div>
  <div class="rdiv"></div>
  <div class="rb" id="rb-analyzer" onclick="go('analyzer')">&#128269;<div class="rb-tip">APK/IPA Analyzer</div></div>
  <div class="rb" id="rb-proxy" onclick="go('proxy')">&#127760;<div class="rb-tip">Proxy &amp; QUIC</div></div>
  <div class="rb" id="rb-cert" onclick="go('cert')">&#128271;<div class="rb-tip">CA Injection</div></div>
  <div class="rdiv"></div>
  <div class="rb" id="rb-sessions" onclick="go('sessions')">&#128203;<div class="rb-tip">Sessions</div></div>
  <div class="rb" id="rb-tools" onclick="go('tools')">&#128295;<div class="rb-tip">Tool Check</div></div>
  
  <div class="rdiv"></div>
  <div class="rb" id="rb-scanner" onclick="go('scanner')">🔍<div class="rb-tip">Vuln Scanner</div></div>
  <div class="rb" id="rb-monitor" onclick="go('monitor')">🔬<div class="rb-tip">API Monitor</div></div>
  <div class="rb" id="rb-fuzzer" onclick="go('fuzzer')">🔗<div class="rb-tip">Intent Fuzzer</div></div>
  <div class="rb" id="rb-tracer" onclick="go('tracer')">🔭<div class="rb-tip">Class Tracer</div></div>
  <div class="rb" id="rb-mdm" onclick="go('mdm')">🏢<div class="rb-tip">MDM Profiler</div></div>
  <div class="rb" id="rb-reports" onclick="go('reports')">📊<div class="rb-tip">Reports</div>
  <div class="rb" id="rb-cve" onclick="go('cve')">🛡<div class="rb-tip">CVE Checker</div></div>
  <div class="rb" id="rb-diff" onclick="go('diff')">🔀<div class="rb-tip">APK Diff</div></div>
  <div class="rb" id="rb-traffic" onclick="go('traffic')">🌐<div class="rb-tip">Traffic Replay</div></div>
  <div class="rb" id="rb-checklist" onclick="go('checklist')">✅<div class="rb-tip">Guided Tests</div></div>
  <div class="rb" id="rb-workspaces" onclick="go('workspaces')">💼<div class="rb-tip">Workspaces</div></div></div>
  <div class="rspc"></div>
  <div class="rb" id="rb-settings" onclick="go('settings')">&#9881;<div class="rb-tip">Settings</div></div>
</div>

<!-- SIDEBAR -->
<div id="sidebar">
  <div class="sbh">
    <div class="sbh-title">Navigation</div>
    <div class="sbh-sub" id="sb-dev-label">No device connected</div>
  </div>
  <div class="sbb">
    <div class="ng">
      <span class="ng-lbl">Core</span>
      <div class="ni on" id="ni-dashboard" onclick="go('dashboard')"><span class="ni-ic">&#127968;</span><span class="ni-lbl">Dashboard</span></div>
      <div class="ni" id="ni-devices" onclick="go('devices')"><span class="ni-ic">&#128241;</span><span class="ni-lbl">Device Manager</span><span class="pill p-n" id="ni-dev-count">0</span></div>
    </div>
    <div class="ng">
      <span class="ng-lbl">Bypass Engine</span>
      <div class="ni" id="ni-bypass" onclick="go('bypass')"><span class="ni-ic">&#9889;</span><span class="ni-lbl">Run Bypass</span><span class="pill p-live">LIVE</span></div>
      <div class="ni" id="ni-scripts" onclick="go('scripts')"><span class="ni-ic">&#128218;</span><span class="ni-lbl">Script Library</span><span class="pill p-n" id="ni-scr-count">14</span></div>
      <div class="ni" id="ni-editor" onclick="go('editor')"><span class="ni-ic">&#9998;</span><span class="ni-lbl">Script Editor</span></div>
    </div>
    <div class="ng">
      <span class="ng-lbl">Analysis &amp; Config</span>
      <div class="ni" id="ni-analyzer" onclick="go('analyzer')"><span class="ni-ic">&#128269;</span><span class="ni-lbl">APK/IPA Analyzer</span></div>
      <div class="ni" id="ni-proxy" onclick="go('proxy')"><span class="ni-ic">&#127760;</span><span class="ni-lbl">Proxy &amp; QUIC</span></div>
      <div class="ni" id="ni-cert" onclick="go('cert')"><span class="ni-ic">&#128271;</span><span class="ni-lbl">CA Injection</span><span class="pill p-new">NEW</span></div>
    </div>
    <div class="ng">
      <span class="ng-lbl">Ops</span>
      <div class="ni" id="ni-sessions" onclick="go('sessions')"><span class="ni-ic">&#128203;</span><span class="ni-lbl">Sessions</span></div>
      <div class="ni" id="ni-tools" onclick="go('tools')"><span class="ni-ic">&#128295;</span><span class="ni-lbl">Tool Check</span></div>
      <div class="ni" id="ni-settings" onclick="go('settings')"><span class="ni-ic">&#9881;</span><span class="ni-lbl">Settings</span></div>
    </div>
  
    <div class="ng">
      <span class="ng-lbl">Security Research</span>
      <div class="ni" id="ni-scanner" onclick="go('scanner')"><span class="ni-ic">🔍</span><span class="ni-lbl">Vuln Scanner</span><span class="pill p-new">NEW</span></div>
      <div class="ni" id="ni-monitor" onclick="go('monitor')"><span class="ni-ic">🔬</span><span class="ni-lbl">API Monitor</span><span class="pill p-new">NEW</span></div>
      <div class="ni" id="ni-fuzzer" onclick="go('fuzzer')"><span class="ni-ic">🔗</span><span class="ni-lbl">Intent Fuzzer</span><span class="pill p-new">NEW</span></div>
      <div class="ni" id="ni-tracer" onclick="go('tracer')"><span class="ni-ic">🔭</span><span class="ni-lbl">Class Tracer</span><span class="pill p-new">NEW</span></div>
      <div class="ni" id="ni-mdm" onclick="go('mdm')"><span class="ni-ic">🏢</span><span class="ni-lbl">MDM Profiler</span><span class="pill p-new">NEW</span></div>
      <div class="ni" id="ni-reports" onclick="go('reports')"><span class="ni-ic">📊</span><span class="ni-lbl">Reports</span><span class="pill p-new">NEW</span></div>
    </div>
    <div class="ng">
      <span class="ng-lbl">Phase 2 Tools</span>
      <div class="ni" id="ni-cve" onclick="go('cve')"><span class="ni-ic">🛡</span><span class="ni-lbl">CVE Checker</span><span class="pill p-new">NEW</span></div>
      <div class="ni" id="ni-diff" onclick="go('diff')"><span class="ni-ic">🔀</span><span class="ni-lbl">APK Diff</span><span class="pill p-new">NEW</span></div>
      <div class="ni" id="ni-traffic" onclick="go('traffic')"><span class="ni-ic">🌐</span><span class="ni-lbl">Traffic Replay</span><span class="pill p-new">NEW</span></div>
      <div class="ni" id="ni-checklist" onclick="go('checklist')"><span class="ni-ic">✅</span><span class="ni-lbl">Guided Tests</span><span class="pill p-new">NEW</span></div>
      <div class="ni" id="ni-workspaces" onclick="go('workspaces')"><span class="ni-ic">💼</span><span class="ni-lbl">Workspaces</span><span class="pill p-new">NEW</span></div>
    </div>
  </div>
</div>

<!-- MAIN CONTENT -->
<div id="main">

<!-- ===== DASHBOARD ===== -->
<div class="page on" id="pg-dashboard">
  <div class="ph">
    <div class="pt">Ghost<b>Pin</b> Enterprise</div>
    <div class="ps">SSL Pinning Bypass Platform &middot; Real ADB &middot; Live Frida Injection &middot; APK Analysis &middot; Enterprise-Grade</div>
  </div>
  <div style="background:linear-gradient(135deg,rgba(255,77,106,.08),rgba(255,170,51,.05));border:1px solid rgba(255,77,106,.2);border-radius:10px;padding:11px 16px;font-size:12px;color:var(--amber);display:flex;align-items:center;gap:10px;margin-bottom:16px;">
    <span style="font-size:16px">&#9888;</span>
    <span><strong>Authorized Use Only.</strong> For penetration testers with explicit written authorization. Unauthorized interception is illegal under CFAA, CMA, and equivalent statutes.</span>
  </div>
  <div class="g4 mb16">
    <div class="sc"><div class="sc-acc" style="background:var(--lime)"></div><div class="sc-num" id="ds-dev" style="color:var(--lime)">0</div><div class="sc-lbl">Devices</div><div class="sc-sub">Connected via ADB/USB</div></div>
    <div class="sc"><div class="sc-acc" style="background:var(--red)"></div><div class="sc-num" id="ds-sess" style="color:var(--red)">0</div><div class="sc-lbl">Active Sessions</div><div class="sc-sub">Live Frida injections</div></div>
    <div class="sc"><div class="sc-acc" style="background:var(--cyan)"></div><div class="sc-num" id="ds-scr" style="color:var(--cyan)">17</div><div class="sc-lbl">Bypass Scripts</div><div class="sc-sub">Built-in + custom</div></div>
    <div class="sc"><div class="sc-acc" style="background:var(--mint)"></div><div class="sc-num" id="ds-tools" style="color:var(--mint)">0/15</div><div class="sc-lbl">Tools Ready</div><div class="sc-sub">Required toolchain</div></div>
  </div>
  <div class="g2 mb16">
    <div class="card">
      <div class="ch"><div class="ct">&#128640; Quick Start Guide</div></div>
      <div class="cb">
        <div class="stl">
          <div class="sti"><div class="stdt done"></div><div>Connect device &amp; verify ADB &rarr; <span style="color:var(--lime);cursor:pointer" onclick="go('devices')">Device Manager</span></div></div>
          <div class="sti"><div class="stdt idle"></div><div>Push frida-server (auto-detect ABI &amp; version)</div></div>
          <div class="sti"><div class="stdt idle"></div><div>Analyze APK/IPA &rarr; <span style="color:var(--lime);cursor:pointer" onclick="go('analyzer')">APK Analyzer</span></div></div>
          <div class="sti"><div class="stdt idle"></div><div>Select scripts &amp; inject &rarr; <span style="color:var(--lime);cursor:pointer" onclick="go('bypass')">Run Bypass</span></div></div>
          <div class="sti"><div class="stdt idle"></div><div>Configure proxy &amp; verify traffic &rarr; <span style="color:var(--lime);cursor:pointer" onclick="go('proxy')">Proxy Config</span></div></div>
        </div>
      </div>
    </div>
    <div class="card">
      <div class="ch"><div class="ct">&#128241; Connected Devices</div><button class="btn btn-ghost btn-xs" onclick="refreshDevices()">&#8635;</button></div>
      <div class="cb0" id="dash-devlist" style="max-height:200px;overflow-y:auto">
        <div class="empty" style="padding:28px"><div class="empty-ic">&#128241;</div><div class="empty-tt">No devices</div><div class="empty-sb">Connect via USB &middot; <code>adb start-server</code></div></div>
      </div>
    </div>
  </div>
  <div class="card">
    <div class="ch"><div class="ct">&#127919; Platform Coverage</div></div>
    <div class="cb">
      <div class="g3">
        <div>
          <div style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:var(--lime);font-weight:700;margin-bottom:10px">SSL BYPASS</div>
          <div style="display:flex;flex-direction:column;gap:5px;font-size:12px;color:var(--txt2)">
            <div>&#10003; OkHttp3 CertificatePinner</div><div>&#10003; SSLContext / TrustManager</div>
            <div>&#10003; Conscrypt (Android 7&ndash;14+)</div><div>&#10003; TrustKit iOS + Android</div>
            <div>&#10003; AFNetworking / Alamofire</div><div>&#10003; Flutter / BoringSSL</div>
            <div>&#10003; Native OpenSSL/BoringSSL</div><div>&#10003; gRPC / Netty</div>
          </div>
        </div>
        <div>
          <div style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:var(--cyan);font-weight:700;margin-bottom:10px">EVASION</div>
          <div style="display:flex;flex-direction:column;gap:5px;font-size:12px;color:var(--txt2)">
            <div>&#10003; Root detection (RootBeer++)</div><div>&#10003; Frida /proc/maps evasion</div>
            <div>&#10003; iOS Jailbreak detection</div><div>&#10003; Obfuscation-resilient hooks</div>
            <div>&#10003; Build.TAGS spoofing</div><div>&#10003; exec() / Runtime blocking</div>
            <div>&#10003; Magisk / KSU hiding</div><div>&#10003; Unity/IL2CPP exports</div>
          </div>
        </div>
        <div>
          <div style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:var(--mint);font-weight:700;margin-bottom:10px">ANALYSIS</div>
          <div style="display:flex;flex-direction:column;gap:5px;font-size:12px;color:var(--txt2)">
            <div>&#10003; APK/IPA static analysis</div><div>&#10003; DEX framework detection</div>
            <div>&#10003; NSC XML pinning parse</div><div>&#10003; mTLS client cert detect</div>
            <div>&#10003; Native lib fingerprint</div><div>&#10003; Obfuscation scoring</div>
            <div>&#10003; QUIC/HTTP3 blocking</div><div>&#10003; Smart script recommendations</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- ===== DEVICES ===== -->
<div class="page" id="pg-devices">
  <div class="ph">
    <div class="pt">Device <b>Manager</b></div>
    <div class="ps">ADB + iOS device management &middot; Frida server lifecycle &middot; Process enumeration &middot; ADB Shell</div>
    <div class="pa">
      <button class="btn btn-lime" onclick="refreshDevices()">&#8635; Refresh Devices</button>
      <button class="btn btn-ghost" onclick="adbStartServer()">&#9654; adb start-server</button>
    </div>
  </div>
  <div class="g2 mb16">
    <div>
      <div class="stitle">&#128241; Connected Devices</div>
      <div id="dev-full-list" style="display:flex;flex-direction:column;gap:10px">
        <div class="empty"><div class="empty-ic" style="font-size:24px">&#128269;</div><div class="empty-tt">Scanning...</div></div>
      </div>
    </div>
    <div>
      <div class="stitle">&#128203; Device Details</div>
      <div id="dev-detail"></div>
      <div id="fs-panel" style="display:none;margin-top:14px">
        <div class="card">
          <div class="ch"><div class="ct">&#9879; Frida Server Manager</div></div>
          <div class="cb">
            <div class="fg"><label class="fl">Server Binary Path</label><input class="fi" id="fs-path" placeholder="/path/to/frida-server-16.x-android-arm64"></div>
            <div style="display:flex;gap:8px;flex-wrap:wrap">
              <button class="btn btn-lime btn-sm" onclick="pushFrida()">&#11014; Push &amp; Start</button>
              <button class="btn btn-danger btn-sm" onclick="stopFrida()">&#9632; Stop</button>
              <button class="btn btn-ghost btn-sm" onclick="fwdFrida()">&#8644; Forward Port</button>
            </div>
            <div id="fs-log" class="stl mt12" style="display:none"></div>
          </div>
        </div>
      </div>
      <div id="proc-panel" style="display:none;margin-top:14px">
        <div class="card">
          <div class="ch">
            <div class="ct">&#9881; Running Processes</div>
            <div class="flex gap6 fxc">
              <input class="fi" id="proc-filter" placeholder="Filter processes..." style="width:150px;padding:5px 10px;font-size:11px" oninput="filterProcs()">
              <button class="btn btn-ghost btn-xs" onclick="loadProcs()">&#8635;</button>
            </div>
          </div>
          <div class="cb0" id="proc-list" style="max-height:260px;overflow-y:auto">
            <div style="padding:14px;color:var(--txt3);font-size:12px">Select a device first</div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="div"></div>
  <div class="stitle">&#9000; ADB Shell Console</div>
  <div class="card">
    <div class="ch">
      <div class="ct">&#128187; Interactive Shell</div>
      <div id="adb-dev-select-wrap" style="display:flex;gap:8px;align-items:center">
        <select class="fsl" id="adb-dev-sel" style="width:200px;padding:5px 10px;font-size:11px"></select>
      </div>
    </div>
    <div class="cb">
      <div class="fg">
        <label class="fl">Command</label>
        <div class="flex gap8">
          <input class="fi" id="adb-cmd" placeholder="e.g. getprop ro.product.model" onkeydown="if(event.key==='Enter')runShell()">
          <button class="btn btn-lime btn-sm" onclick="runShell()">&#9654; Run</button>
        </div>
      </div>
      <div style="margin-bottom:8px;display:flex;gap:6px;flex-wrap:wrap">
        <button class="btn btn-ghost btn-xs" onclick="quickCmd('getprop ro.product.model')">Model</button>
        <button class="btn btn-ghost btn-xs" onclick="quickCmd('pm list packages -3')">3rd party apps</button>
        <button class="btn btn-ghost btn-xs" onclick="quickCmd('id')">Check UID</button>
        <button class="btn btn-ghost btn-xs" onclick="quickCmd('pgrep -f frida')">Frida PID</button>
        <button class="btn btn-ghost btn-xs" onclick="quickCmd('settings get global http_proxy')">Proxy</button>
        <button class="btn btn-ghost btn-xs" onclick="quickCmd('cat /proc/net/tcp6 | head -20')">TCP sockets</button>
      </div>
    </div>
    <div class="term" style="border-top:none;border-left:none;border-right:none;border-bottom:none;border-top:1px solid var(--rim)">
      <div class="term-hd">
        <div class="tdot" style="background:#ff5f57"></div>
        <div class="tdot" style="background:#febc2e"></div>
        <div class="tdot" style="background:#28c840"></div>
        <span style="font-size:10px;color:var(--txt3);margin-left:4px">adb shell</span>
        <div class="flex1"></div>
        <button class="btn btn-ghost btn-xs" onclick="clearShell()">Clear</button>
      </div>
      <div class="term-bd" id="shell-out" style="min-height:150px;max-height:220px">
        <div class="ll"><span class="lm" style="color:var(--txt4)">Ready &mdash; select a device and run a command</span></div>
      </div>
    </div>
  </div>
</div>

<!-- ===== BYPASS ===== -->
<div class="page" id="pg-bypass">
  <div class="ph">
    <div class="pt">Run <b>Bypass</b></div>
    <div class="ps">Configure target &middot; Select scripts &middot; Inject via Frida &middot; Real-time log streaming</div>
  </div>
  <div class="g2 mb16">
    <div class="card">
      <div class="ch"><div class="ct">&#127919; Target Configuration</div></div>
      <div class="cb">
        <div class="fg"><label class="fl">Device</label><select class="fsl" id="bp-dev"></select></div>
        <div class="fg"><label class="fl">Platform</label>
          <select class="fsl" id="bp-plat" onchange="updatePlatform()">
            <option value="android">Android</option>
            <option value="ios">iOS</option>
          </select>
        </div>
        <div class="fg"><label class="fl">Target (package name or PID)</label><input class="fi" id="bp-target" placeholder="com.example.app or 1234"></div>
        <div class="fg"><label class="fl">Injection Mode</label>
          <select class="fsl" id="bp-mode">
            <option value="attach">Attach to running process</option>
            <option value="spawn">Spawn (start + inject)</option>
          </select>
        </div>
      </div>
    </div>
    <div class="card">
      <div class="ch"><div class="ct">&#128737; Anti-Detection Layer</div></div>
      <div class="cb" style="display:flex;flex-direction:column;gap:14px">
        <label class="tw" onclick="antiToggle('root')">
          <div class="tg" id="at-root"></div>
          <div><div class="tl">Root Detection Bypass</div><div style="font-size:11px;color:var(--txt3)">RootBeer, file checks, Build.TAGS, exec() blocking</div></div>
        </label>
        <label class="tw" onclick="antiToggle('frida')">
          <div class="tg" id="at-frida"></div>
          <div><div class="tl">Frida Detection Evasion</div><div style="font-size:11px;color:var(--txt3)">/proc/maps filter, port hiding, name obfuscation</div></div>
        </label>
        <label class="tw" onclick="antiToggle('jailbreak')">
          <div class="tg" id="at-jb"></div>
          <div><div class="tl">Jailbreak Detection Bypass (iOS)</div><div style="font-size:11px;color:var(--txt3)">NSFileManager, canOpenURL, Cydia/Sileo evasion</div></div>
        </label>
        <label class="tw" onclick="antiToggle('emulator')">
          <div class="tg" id="at-emu"></div>
          <div><div class="tl">Emulator Detection Bypass</div><div style="font-size:11px;color:var(--txt3)">Build.FINGERPRINT, IMEI, sensor spoofing</div></div>
        </label>
      </div>
    </div>
  </div>

  <div class="flex fxc fxb mb12">
    <div class="stitle" style="margin-bottom:0">&#128218; Select Bypass Scripts <span style="font-size:12px;color:var(--txt3);font-family:var(--mono);font-weight:400">(<span id="scr-sel-cnt">1</span> selected)</span></div>
    <div class="flex gap6">
      <button class="btn btn-ghost btn-xs" onclick="selAllScripts()">Select All</button>
      <button class="btn btn-ghost btn-xs" onclick="clearSelScripts()">Clear</button>
    </div>
  </div>
  <div class="ga mb16" id="bp-script-grid"></div>

  <div class="card mb16">
    <div class="ch"><div class="ct">&#9998; Custom Script Snippet <span style="font-size:11px;color:var(--txt3);font-weight:400">&mdash; appended after selected scripts</span></div>
      <button class="btn btn-ghost btn-xs" onclick="clearCustom()">Clear</button>
    </div>
    <div class="ced" style="border:none;border-radius:0">
      <div class="ced-hd"><span style="font-size:10px;color:var(--txt3)">JavaScript &middot; Frida API &middot; send() for logging</span></div>
      <textarea class="ca" id="custom-script" style="min-height:90px;max-height:200px" placeholder="// Optional: your custom Frida hook appended after all selected scripts&#10;// send('[Custom] Hook fired on: ' + target);"></textarea>
    </div>
  </div>

  <div style="display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-bottom:16px">
    <button class="btn btn-lime" style="font-size:14px;padding:11px 28px" id="bp-start-btn" onclick="startBypass()">&#9889; Inject Now</button>
    <button class="btn btn-danger" id="bp-stop-btn" style="display:none" onclick="stopBypass()">&#9632; Stop Session</button>
    <button class="btn btn-ghost btn-sm" id="bp-save-btn" style="display:none" onclick="saveSession()">&#128190; Save Session</button>
    <button class="btn btn-ghost btn-sm" id="bp-export-btn" style="display:none" onclick="exportLog()">&#8595; Export Log</button>
    <div id="bp-status" style="font-size:12px;color:var(--txt3);display:flex;align-items:center;gap:8px"></div>
  </div>

  <div class="term" style="height:380px">
    <div class="term-hd">
      <div class="tdot" style="background:#ff5f57"></div>
      <div class="tdot" style="background:#febc2e"></div>
      <div class="tdot" style="background:#28c840"></div>
      <span style="font-size:10px;color:var(--txt3);margin-left:4px">frida injection log</span>
      <div id="live-indicator" style="display:none;margin-left:8px;display:none;align-items:center;gap:6px;font-size:10px;color:var(--red)">
        <div class="live-dot"></div>LIVE
      </div>
      <div class="flex1"></div>
      <span id="bp-log-count" style="font-size:10px;color:var(--txt3);margin-right:8px">0 lines</span>
      <button class="btn btn-ghost btn-xs" onclick="clearBpLog()">&#10005; Clear</button>
    </div>
    <div class="term-bd" id="bp-log" style="max-height:320px">
      <div class="ll"><span class="lm" style="color:var(--txt4)">GhostPin ready &mdash; configure target and click Inject</span></div>
    </div>
  </div>
</div>

<!-- ===== SCRIPT LIBRARY ===== -->
<div class="page" id="pg-scripts">
  <div class="ph">
    <div class="pt">Script <b>Library</b></div>
    <div class="ps">14 enterprise-grade bypass scripts &middot; Android + iOS &middot; Custom script management</div>
    <div class="pa">
      <button class="btn btn-lime" onclick="go('editor')">+ New Script</button>
      <select class="fsl" id="lib-filter" onchange="renderLib()" style="width:180px;padding:7px 12px;font-size:12px">
        <option value="all">All Scripts</option>
        <option value="android">Android Only</option>
        <option value="ios">iOS Only</option>
        <option value="ssl">SSL Bypass</option>
        <option value="evasion">Evasion</option>
        <option value="flutter">Flutter</option>
        <option value="native">Native / BoringSSL</option>
        <option value="grpc">gRPC / Netty</option>
        <option value="easy">Easy</option>
        <option value="hard">Hard / Expert</option>
      </select>
    </div>
  </div>
  <div class="ga" id="lib-grid"></div>
</div>

<!-- ===== SCRIPT EDITOR ===== -->
<div class="page" id="pg-editor">
  <div class="ph">
    <div class="pt">Script <b>Editor</b></div>
    <div class="ps">Write, edit and save custom Frida scripts &middot; Full Frida API available</div>
  </div>
  <div class="g2">
    <div>
      <div class="card mb12">
        <div class="ch"><div class="ct">&#128196; Script Metadata</div></div>
        <div class="cb">
          <div class="fg"><label class="fl">Script ID</label><input class="fi" id="ed-id" placeholder="my-custom-script-name"></div>
          <div class="fg"><label class="fl">Load from Built-in Library</label>
            <select class="fsl" id="ed-load-sel" onchange="loadIntoEditor()">
              <option value="">-- Load a built-in script --</option>
            </select>
          </div>
          <div style="display:flex;gap:8px">
            <button class="btn btn-lime btn-sm" onclick="saveEditorScript()">&#128190; Save</button>
            <button class="btn btn-ghost btn-sm" onclick="clearEditor()">&#10005; Clear</button>
            <button class="btn btn-cyan btn-sm" onclick="injectEditor()">&#9889; Inject Direct</button>
          </div>
        </div>
      </div>
      <div class="card">
        <div class="ch"><div class="ct">&#128216; Frida API Quick Reference</div></div>
        <div class="cb" style="font-size:11px;color:var(--txt3);line-height:2">
          <code>Java.perform(fn)</code> Enter Java context<br>
          <code>Java.use('pkg.ClassName')</code> Load class<br>
          <code>cls.method.overloads</code> All overloads<br>
          <code>Java.enumerateLoadedClasses()</code> All classes<br>
          <code>Interceptor.attach(ptr, cb)</code> Native hook<br>
          <code>Module.findExportByName(m,f)</code> Find export<br>
          <code>Memory.scan(base,sz,pat,cb)</code> Pattern scan<br>
          <code>Process.enumerateModules()</code> List modules<br>
          <code>ObjC.available</code> iOS ObjC runtime<br>
          <code>ObjC.classes['ClassName']</code> iOS class<br>
          <code>send('msg')</code> Log to GhostPin
        </div>
      </div>
    </div>
    <div class="card">
      <div class="ch">
        <div class="ct">&#9000; Editor</div>
        <span id="ed-status" style="font-size:11px;color:var(--txt3)">Unsaved</span>
      </div>
      <div class="ced" style="border:none;border-radius:0">
        <div class="ced-hd">
          <span style="font-size:10px;color:var(--txt3)">JavaScript &middot; Frida API</span>
          <div class="flex1"></div>
          <span style="font-size:10px;color:var(--txt4)" id="ed-chars">0 chars</span>
        </div>
        
    <div id="monaco-container" style="flex:1;border:1px solid var(--rim);border-radius:6px;overflow:hidden;min-height:460px;background:#1e1e1e"></div>
    <textarea id="ed-code" style="display:none"></textarea>
    <!-- Load Monaco -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.38.0/min/vs/loader.min.js"></script>
    <script>
      var MONACO_INSTANCE = null;
      require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.38.0/min/vs' }});
      require(['vs/editor/editor.main'], function() {
        var defaultVal = `// Write your Frida script here
Java.perform(function() {
  var log = function(m) { send('[Custom] ' + m); };
  // Your hooks here...
});`;
        MONACO_INSTANCE = monaco.editor.create(document.getElementById('monaco-container'), {
          value: defaultVal,
          language: 'javascript',
          theme: 'vs-dark',
          automaticLayout: true,
          minimap: { enabled: false },
          fontSize: 12,
          fontFamily: "'JetBrains Mono', monospace"
        });
        MONACO_INSTANCE.onDidChangeModelContent(function() {
          document.getElementById('ed-code').value = MONACO_INSTANCE.getValue();
          edChanged();
        });
      });
      // Override standard set value
      var _origLoad = (typeof loadScriptToEditor!=='undefined'?loadScriptToEditor:null);
      if(_origLoad) {
        loadScriptToEditor = function(id) {
          if (!id) return;
          api('/api/scripts/'+id).then(function(d) {
            ED_CURRENT = id; ED_DIRTY = false;
            var val = d.content || '// empty script';
            document.getElementById('ed-code').value = val;
            if (MONACO_INSTANCE) MONACO_INSTANCE.setValue(val);
            document.getElementById('ed-save-btn').classList.remove('btn-lime');
            document.getElementById('ed-title').textContent = 'Editing: ' + id + (d.custom?' (Custom)':' (Built-in)');
            
            // Show reset button for custom scripts
            var rb = document.getElementById('ed-reset-btn');
            if(rb) rb.style.display = d.custom ? 'inline-block' : 'none';
          });
        };
      }
    </script>
    
      </div>
    </div>
  </div>
</div>

<!-- ===== ANALYZER ===== -->
<div class="page" id="pg-analyzer">
  <div class="ph">
    <div class="pt">APK/IPA <b>Analyzer</b></div>
    <div class="ps">Static analysis &middot; Framework detection &middot; Pinning fingerprinting &middot; mTLS detection &middot; Smart script recommendations</div>
  </div>
  <div class="card mb16" id="drop-card">
    <div class="cb">
      <div id="drop-zone"
        style="border:2px dashed var(--rim2);border-radius:12px;padding:48px;text-align:center;cursor:pointer;transition:all .2s;"
        onclick="document.getElementById('apk-input').click()"
        ondragover="event.preventDefault();this.style.borderColor='var(--lime)';this.style.background='var(--limebg)'"
        ondragleave="this.style.borderColor='var(--rim2)';this.style.background=''"
        ondrop="handleDrop(event)">
        <div style="font-size:44px;margin-bottom:14px">&#128230;</div>
        <div style="font-family:var(--sans);font-size:17px;font-weight:800">Drop APK / IPA / XAPK here</div>
        <div style="font-size:12px;color:var(--txt3);margin-top:6px">or click to browse &middot; .apk &middot; .ipa &middot; .xapk &middot; .apks</div>
        <input type="file" id="apk-input" accept=".apk,.ipa,.xapk,.apks" style="display:none" onchange="analyzeFile(this.files[0])">
      </div>
    </div>
  </div>
  <div id="az-loading" style="display:none;text-align:center;padding:60px">
    <div class="pbar-indeterminate" style="max-width:300px;margin:0 auto 20px"></div>
    <div style="font-family:var(--sans);font-size:16px;font-weight:700">Analyzing</div>
    <div style="font-size:12px;color:var(--txt3);margin-top:4px" id="az-log">Decompiling APK...</div>
  </div>
  <div id="az-result" style="display:none">
    <div class="g2 mb16">
      <div class="card">
        <div class="ch"><div class="ct">&#128203; App Info</div><button class="btn btn-ghost btn-xs" onclick="resetAnalyzer()">&#8592; New</button></div>
        <div class="cb" id="az-info"></div>
      </div>
      <div class="card">
        <div class="ch"><div class="ct">&#128270; Security Detections</div></div>
        <div class="cb" id="az-dets"></div>
      </div>
    </div>
    <div class="g2 mb16">
      <div class="card">
        <div class="ch"><div class="ct">&#128218; Frameworks Detected</div></div>
        <div class="cb" id="az-fw"></div>
      </div>
      <div class="card">
        <div class="ch"><div class="ct">&#128279; Native Libraries</div></div>
        <div class="cb0" id="az-libs" style="max-height:200px;overflow-y:auto;padding:12px 14px"></div>
      </div>
    </div>
    <div class="card">
      <div class="ch"><div class="ct">&#9889; Recommended Bypass Scripts</div><button class="btn btn-lime btn-sm" onclick="applyRec()">Apply All &rarr; Bypass</button></div>
      <div class="cb" id="az-rec"></div>
    </div>
  </div>
</div>

<!-- ===== PROXY ===== -->
<div class="page" id="pg-proxy">
  <div class="ph">
    <div class="pt">Proxy &amp; <b>QUIC</b></div>
    <div class="ps">HTTP proxy setup &middot; QUIC/HTTP3 blocking &middot; ADB port forwarding &middot; Network interception</div>
  </div>
  <div class="g2 mb16">
    <div class="card">
      <div class="ch"><div class="ct">&#127760; HTTP/HTTPS Proxy</div></div>
      <div class="cb">
        <div class="fg"><label class="fl">Device</label><select class="fsl" id="prx-dev"></select></div>
        <div class="g2">
          <div class="fg"><label class="fl">Proxy Host</label><input class="fi" id="prx-host" value="192.168.1.100" placeholder="Burp/mitmproxy host"></div>
          <div class="fg"><label class="fl">Port</label><input class="fi" id="prx-port" value="8080" type="number"></div>
        </div>
        <div style="display:flex;gap:8px;flex-wrap:wrap">
          <button class="btn btn-lime btn-sm" onclick="setProxy()">&#10003; Set Proxy</button>
          <button class="btn btn-danger btn-sm" onclick="clearProxy()">&#10005; Clear Proxy</button>
        </div>
        <div id="prx-status" class="mt8"></div>
      </div>
    </div>
    <div class="card">
      <div class="ch"><div class="ct">&#128683; QUIC / HTTP3 Blocker</div></div>
      <div class="cb">
        <div style="font-size:12px;color:var(--txt3);line-height:1.75;margin-bottom:14px">
          Blocks UDP 443/80 via iptables on the device to force HTTP/2 fallback.
          <strong style="color:var(--amber)">Root required.</strong>
          Essential for intercepting apps that use QUIC/HTTP3 with Burp or mitmproxy.
        </div>
        <div class="fg"><label class="fl">Device</label><select class="fsl" id="quic-dev"></select></div>
        <button class="btn btn-danger btn-sm" onclick="blockQUIC()">&#128683; Block QUIC/UDP443</button>
        <div id="quic-status" class="mt8"></div>
      </div>
    </div>
  </div>
  <div class="card">
    <div class="ch"><div class="ct">&#8644; Port Forwarding</div></div>
    <div class="cb">
      <div class="g2">
        <div>
          <div class="fg"><label class="fl">Device</label><select class="fsl" id="fwd-dev"></select></div>
          <div class="flex gap8 mb12">
            <div class="fg fx1"><label class="fl">Local Port</label><input class="fi" id="fwd-local" value="27042" type="number"></div>
            <div class="fg fx1"><label class="fl">Remote Port</label><input class="fi" id="fwd-remote" value="27042" type="number"></div>
          </div>
          <button class="btn btn-cyan btn-sm" onclick="fwdPort()">&#8644; Forward</button>
          <div id="fwd-status" class="mt8"></div>
        </div>
        <div style="font-size:11px;color:var(--txt3);line-height:2">
          <strong style="color:var(--txt2)">Common ports:</strong><br>
          <code>27042</code> Frida server (default)<br>
          <code>8080</code> HTTP proxy (Burp/mitmproxy)<br>
          <code>8443</code> HTTPS proxy<br>
          <code>5555</code> ADB TCP/IP mode<br>
          <code>1234</code> LLDB debugger
        </div>
      </div>
    </div>
  </div>
</div>

<!-- ===== CERT ===== -->
<div class="page" id="pg-cert">
  <div class="ph">
    <div class="pt">CA <b>Injection</b></div>
    <div class="ps">Install Burp Suite / mitmproxy CA as system-trusted certificate &middot; Android 7&ndash;14+ including APEX</div>
  </div>
  <div class="g2 mb16">
    <div class="card">
      <div class="ch"><div class="ct">&#128220; Certificate Setup</div></div>
      <div class="cb">
        <div class="fg"><label class="fl">Device</label><select class="fsl" id="cert-dev"></select></div>
        <div class="fg"><label class="fl">Platform</label>
          <select class="fsl" id="cert-plat">
            <option value="android">Android</option>
            <option value="ios">iOS</option>
          </select>
        </div>
        <div class="fg"><label class="fl">CA Certificate Path (PEM)</label><input class="fi" id="cert-path" placeholder="/path/to/burp-ca.pem or mitmproxy-ca-cert.pem"></div>
        <button class="btn btn-lime btn-sm" onclick="injectCert()">&#11014; Inject as System CA</button>
        <div id="cert-steps" class="stl mt12" style="display:none"></div>
      </div>
    </div>
    <div class="card">
      <div class="ch"><div class="ct">&#128214; Instructions</div></div>
      <div class="cb" style="font-size:12px;color:var(--txt3);line-height:1.9">
        <strong style="color:var(--txt2)">Burp Suite &rarr; DER export:</strong><br>
        Proxy &rarr; Proxy settings &rarr; Import/export CA cert<br>
        Then: <code>openssl x509 -inform DER -in burp.der -out burp.pem</code>
        <div class="div" style="margin:10px 0"></div>
        <strong style="color:var(--txt2)">mitmproxy CA location:</strong><br>
        <code>~/.mitmproxy/mitmproxy-ca-cert.pem</code><br>
        Or: Browse to <code>mitm.it</code> on the device.
        <div class="div" style="margin:10px 0"></div>
        <strong style="color:var(--txt2)">Android 14+ APEX note:</strong><br>
        Uses conscrypt APEX mount. Cert is lost on reboot.<br>
        For persistence, use a Magisk module.
      </div>
    </div>
  </div>
</div>

<!-- ===== SESSIONS ===== -->
<div class="page" id="pg-sessions">
  <div class="ph">
    <div class="pt">Bypass <b>Sessions</b></div>
    <div class="ps">View, replay and export saved bypass sessions</div>
    <div class="pa"><button class="btn btn-lime" onclick="loadSessions()">&#8635; Refresh</button></div>
  </div>
  <div id="sessions-list" style="display:flex;flex-direction:column;gap:10px">
    <div class="empty"><div class="empty-ic">&#128203;</div><div class="empty-tt">No sessions saved</div><div class="empty-sb">Run a bypass and click "Save Session"</div></div>
  </div>
</div>

<!-- ===== TOOLS ===== -->
<div class="page" id="pg-tools">
  <div class="ph">
    <div class="pt">Tool <b>Check</b></div>
    <div class="ps">Verify required toolchain &middot; Installation guidance</div>
    <div class="pa"><button class="btn btn-lime" onclick="runToolCheck()">&#8635; Re-scan</button></div>
  </div>
  <div class="ga mb16" id="tool-grid">
    <div class="empty"><div class="empty-ic">&#128269;</div><div class="empty-tt">Scanning tools...</div></div>
  </div>
  <div class="card">
    <div class="ch"><div class="ct">&#128230; Installation Guide</div></div>
    <div class="cb">
      <div class="g3">
        <div><div style="color:var(--lime);font-weight:700;margin-bottom:8px;font-size:12px">Frida Toolchain</div>
          <code style="display:block;margin-bottom:4px">pip install frida-tools</code>
          <code style="display:block;margin-bottom:4px">pip install objection</code>
          <code style="display:block">pip install apk-mitm</code>
        </div>
        <div><div style="color:var(--cyan);font-weight:700;margin-bottom:8px;font-size:12px">Android Tools</div>
          <code style="display:block;margin-bottom:4px">brew install android-tools</code>
          <code style="display:block;margin-bottom:4px">brew install apktool jadx</code>
          <code style="display:block">sudo apt install adb apktool</code>
        </div>
        <div><div style="color:var(--mint);font-weight:700;margin-bottom:8px;font-size:12px">Proxy Tools</div>
          <code style="display:block;margin-bottom:4px">pip install mitmproxy</code>
          <code style="display:block">brew install --cask burp-suite</code>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- ===== SETTINGS ===== -->
<div class="page" id="pg-settings">
  <div class="ph">
    <div class="pt">Platform <b>Settings</b></div>
    <div class="ps">Configure GhostPin preferences &amp; behavior</div>
  </div>
  <div class="g2">
    <div class="card">
      <div class="ch"><div class="ct">&#9881; General Configuration</div></div>
      <div class="cb">
        <div class="fg"><label class="fl">Default Frida Port</label><input class="fi" id="cfg-fport" value="27042" type="number"></div>
        <div class="fg"><label class="fl">Device Poll Interval (seconds)</label><input class="fi" id="cfg-poll" value="5" type="number" min="1" max="60"></div>
        <div class="fg"><label class="fl">Log Level</label>
          <select class="fsl" id="cfg-loglevel">
            <option value="all">All (debug + frida + info)</option>
            <option value="info">Info + Frida + Errors</option>
            <option value="warn">Warnings + Errors</option>
            <option value="error">Errors Only</option>
          </select>
        </div>
        <div class="fg"><label class="fl">Max Log Lines (terminal)</label><input class="fi" id="cfg-maxlog" value="2000" type="number"></div>
        <button class="btn btn-lime btn-sm" onclick="saveSettings()">Save Settings</button>
      </div>
    </div>
    <div class="card">
      <div class="ch"><div class="ct">&#8505; About GhostPin</div></div>
      <div class="cb">
        <div class="kv"><div class="kv-k">Version</div><div class="kv-v" style="color:var(--lime)">5.0.0 Enterprise</div></div>
        <div class="kv"><div class="kv-k">Platform</div><div class="kv-v">Python 3 + Flask REST + SSE</div></div>
        <div class="kv"><div class="kv-k">Scripts</div><div class="kv-v">14 built-in bypass scripts</div></div>
        <div class="kv"><div class="kv-k">Protocols</div><div class="kv-v">REST API + Server-Sent Events</div></div>
        <div class="kv"><div class="kv-k">Data Dir</div><div class="kv-v"><code>~/.ghostpin</code></div></div>
        <div class="kv"><div class="kv-k">Source</div><div class="kv-v">Based on PinBreaker Pro v3 (Electron)</div></div>
      </div>
    </div>
  </div>
</div>


<!-- ===== VULN SCANNER ===== -->
<div class="page" id="pg-scanner">
  <div class="ph">
    <div class="pt">Vulnerability <b>Scanner</b></div>
    <div class="ps">SAST static analysis · Hardcoded secrets · Weak crypto · Android misconfigurations · Security grading</div>
  </div>
  <div class="card mb16" id="scan-drop-card">
    <div class="cb">
      <div id="scan-drop-zone" style="border:2px dashed var(--rim2);border-radius:12px;padding:48px;text-align:center;cursor:pointer;transition:all .2s;"
        onclick="document.getElementById('scan-input').click()"
        ondragover="event.preventDefault();this.style.borderColor='var(--lime)'"
        ondragleave="this.style.borderColor='var(--rim2)'"
        ondrop="handleScanDrop(event)">
        <div style="font-size:44px;margin-bottom:14px">🔍</div>
        <div style="font-family:var(--sans);font-size:17px;font-weight:800">Drop APK for SAST Scan</div>
        <div style="font-size:12px;color:var(--txt3);margin-top:6px">30+ patterns · Secrets · Weak crypto · Misconfigs · Security grade</div>
        <input type="file" id="scan-input" accept=".apk,.ipa" style="display:none" onchange="runVulnScan(this.files[0])">
      </div>
    </div>
  </div>
  <div id="scan-loading" style="display:none;text-align:center;padding:60px">
    <div class="pbar-indeterminate" style="max-width:300px;margin:0 auto 20px"></div>
    <div style="font-size:15px;font-weight:700">Scanning for vulnerabilities...</div>
    <div style="font-size:12px;color:var(--txt3);margin-top:4px">Checking secrets, weak crypto, misconfigurations</div>
  </div>
  <div id="scan-result" style="display:none">
    <div class="g4 mb16" id="scan-stats"></div>
    <div id="scan-findings"></div>
    <div class="cf mt8">
      <button class="btn btn-lime btn-sm" onclick="generateReportFromScan()">📊 Generate Report</button>
      <button class="btn btn-ghost btn-sm" onclick="resetScan()">↩ New Scan</button>
    </div>
  </div>
  <div class="card mt8">
    <div class="ch"><div class="ct">📖 What does each finding mean?</div></div>
    <div class="cb" style="font-size:12px;color:var(--txt3);line-height:2">
      <b style="color:var(--red)">CRITICAL</b> — Immediately exploitable. Hardcoded cloud keys, private keys, Stripe live secrets.<br>
      <b style="color:var(--amber)">HIGH</b> — Likely exploitable. Firebase URLs, OAuth secrets, MD5/DES crypto, cleartext HTTP, debug mode.<br>
      <b style="color:var(--cyan)">MEDIUM</b> — Context-dependent risk. JWT tokens, internal IPs, SHA-1, backup enabled, exported components.<br>
      <b style="color:var(--txt2)">LOW</b> — Informational. Minor misconfigs, dev artifacts.
    </div>
  </div>
</div>

<!-- ===== API MONITOR ===== -->
<div class="page" id="pg-monitor">
  <div class="ph">
    <div class="pt">Runtime API <b>Monitor</b></div>
    <div class="ps">Live Frida hooks · Every crypto/file/network call logged · Essential for fintech &amp; banking apps</div>
    <div class="pa">
      <button class="btn btn-lime" id="mon-start-btn" onclick="startMonitor()">▶ Start Monitor</button>
      <button class="btn btn-danger" id="mon-stop-btn" style="display:none" onclick="stopMonitor()">■ Stop</button>
      <button class="btn btn-ghost btn-sm" onclick="clearMonLog()">✕ Clear</button>
    </div>
  </div>
  <div class="g2 mb16">
    <div class="card">
      <div class="ch"><div class="ct">⚙ Monitor Configuration</div></div>
      <div class="cb">
        <div class="fg"><label class="fl">Device</label><select class="fsl" id="mon-dev"></select></div>
        <div class="fg"><label class="fl">Target (package or PID)</label><input class="fi" id="mon-target" placeholder="com.bank.app or 1234"></div>
        <div class="fg"><label class="fl">Injection Mode</label>
          <select class="fsl" id="mon-mode">
            <option value="attach">Attach to running process</option>
            <option value="spawn">Spawn (start + inject)</option>
          </select>
        </div>
        <div class="fg"><label class="fl">Monitor Categories</label>
          <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:4px">
            <label style="display:flex;align-items:center;gap:6px;font-size:12px;cursor:pointer"><input type="checkbox" id="mon-crypto" checked> 🔐 Crypto APIs</label>
            <label style="display:flex;align-items:center;gap:6px;font-size:12px;cursor:pointer"><input type="checkbox" id="mon-file" checked> 📁 File I/O</label>
            <label style="display:flex;align-items:center;gap:6px;font-size:12px;cursor:pointer"><input type="checkbox" id="mon-network" checked> 🌐 Network</label>
          </div>
        </div>
      </div>
    </div>
    <div class="card">
      <div class="ch"><div class="ct">📈 Live Stats</div></div>
      <div class="cb">
        <div class="g3" style="gap:10px">
          <div class="sc" style="padding:12px"><div class="sc-num" id="mon-crypto-cnt" style="color:var(--violet);font-size:24px">0</div><div class="sc-lbl">Crypto Calls</div></div>
          <div class="sc" style="padding:12px"><div class="sc-num" id="mon-file-cnt" style="color:var(--amber);font-size:24px">0</div><div class="sc-lbl">File Ops</div></div>
          <div class="sc" style="padding:12px"><div class="sc-num" id="mon-net-cnt" style="color:var(--cyan);font-size:24px">0</div><div class="sc-lbl">Network Calls</div></div>
        </div>
        <div style="margin-top:14px">
          <div class="fg"><label class="fl">Filter log</label><input class="fi" id="mon-filter" placeholder="e.g. Cipher, /secret/, okhttp3" oninput="filterMonLog()"></div>
        </div>
      </div>
    </div>
  </div>
  <div class="term" style="height:420px">
    <div class="term-hd">
      <div class="tdot" style="background:#ff5f57"></div><div class="tdot" style="background:#febc2e"></div><div class="tdot" style="background:#28c840"></div>
      <span style="font-size:10px;color:var(--txt3);margin-left:4px">api monitor log</span>
      <div id="mon-live-ind" style="display:none;margin-left:8px;align-items:center;gap:6px;font-size:10px;color:var(--red)"><div class="live-dot"></div>LIVE</div>
      <div class="flex1"></div>
      <span id="mon-log-count" style="font-size:10px;color:var(--txt3);margin-right:8px">0 calls</span>
    </div>
    <div class="term-bd" id="mon-log" style="max-height:360px">
      <div class="ll"><span class="lm" style="color:var(--txt4)">API Monitor ready — configure target and click Start Monitor</span></div>
    </div>
  </div>
</div>

<!-- ===== INTENT FUZZER ===== -->
<div class="page" id="pg-fuzzer">
  <div class="ph">
    <div class="pt">Deep Link &amp; Intent <b>Fuzzer</b></div>
    <div class="ps">Enumerate exported components · Fire crafted Intents · SQLi / path traversal / overflow payloads · ADB-driven</div>
  </div>
  <div class="g2 mb16">
    <div class="card">
      <div class="ch"><div class="ct">⚙ Fuzzer Setup</div></div>
      <div class="cb">
        <div class="fg"><label class="fl">Device</label><select class="fsl" id="fz-dev"></select></div>
        <div class="fg"><label class="fl">Target Package</label><input class="fi" id="fz-pkg" placeholder="com.mybank.app"></div>
        <div style="display:flex;gap:8px;flex-wrap:wrap">
          <button class="btn btn-lime btn-sm" onclick="enumComponents()">🔎 Enumerate Components</button>
        </div>
        <div id="fz-comp-list" class="mt12" style="display:none">
          <div class="fg"><label class="fl">Component to Fuzz</label><select class="fsl" id="fz-comp"></select></div>
          <div class="fg"><label class="fl">Component Type</label>
            <select class="fsl" id="fz-type">
              <option value="activity">Activity</option>
              <option value="service">Service</option>
              <option value="broadcast">Broadcast Receiver</option>
            </select>
          </div>
          <div class="fg"><label class="fl">Payload Categories</label>
            <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:4px">
              <label style="display:flex;align-items:center;gap:6px;font-size:12px;cursor:pointer"><input type="checkbox" id="fz-sqli" checked> SQLi</label>
              <label style="display:flex;align-items:center;gap-6px;font-size:12px;cursor:pointer"><input type="checkbox" id="fz-trav" checked> Path Traversal</label>
              <label style="display:flex;align-items:center;gap:6px;font-size:12px;cursor:pointer"><input type="checkbox" id="fz-uri" checked> URI Schemes</label>
              <label style="display:flex;align-items:center;gap:6px;font-size:12px;cursor:pointer"><input type="checkbox" id="fz-overflow"> Overflow</label>
              <label style="display:flex;align-items:center;gap:6px;font-size:12px;cursor:pointer"><input type="checkbox" id="fz-xss"> XSS</label>
            </div>
          </div>
          <button class="btn btn-danger btn-sm" onclick="startFuzz()">💥 Start Fuzzing</button>
        </div>
      </div>
    </div>

    <div class="card mb16">
      <div class="ch">
        <div class="ct">🛠️ 1-Click Auto-Patcher (apk-mitm)</div>
      </div>
      <div class="cb">
        <p style="font-size:12px;color:var(--txt3);margin-bottom:12px">
          Testing on a non-rooted Android device or non-jailbroken iPhone? Upload the APK/IPA to automatically inject the Frida Gadget and bypass Network Security Configs before side-loading.
        </p>
        <div style="display:flex;gap:10px;align-items:center;">
          <input type="file" id="patch-file" class="form-control" style="flex:1">
          <button class="btn btn-primary" onclick="runAutoPatcher()">Patch & Download</button>
        </div>
        <div id="patcher-status" style="margin-top:10px;font-size:12px;color:var(--lime);display:none;"></div>
      </div>
    </div>

    <div class="card mb16">
      <div class="ch">
        <div class="ct">📲 1-Click Device APK Extractor</div>
      </div>
      <div class="cb">
        <p style="font-size:12px;color:var(--txt3);margin-bottom:12px">
          Don't have the APK file on your computer? If the app is installed on your connected Android device, type its package name below to pull it directly into GhostPin.
        </p>
        <div style="display:flex;gap:10px;align-items:center;">
          <input type="text" id="extract-package" class="input-dark" style="flex:1" placeholder="com.example.app">
          <button class="btn btn-outline" onclick="runAPKExtractor()">Extract & Download</button>
        </div>
        <div id="extractor-status" style="margin-top:10px;font-size:12px;color:var(--lime);display:none;"></div>
      </div>
    </div>


    <div class="card">
      <div class="ch"><div class="ct">📊 Results</div></div>
      <div class="cb0" id="fz-results" style="max-height:340px;overflow-y:auto;padding:12px 14px">
        <div class="empty" style="padding:30px"><div class="empty-ic">🔗</div><div class="empty-tt">No results yet</div><div class="empty-sb">Enumerate components and start fuzzing</div></div>
      </div>
    </div>
  </div>
  <div class="card">
    <div class="ch"><div class="ct">📖 What to look for in fuzz results?</div></div>
    <div class="cb" style="font-size:12px;color:var(--txt3);line-height:2">
      🔴 <b style="color:var(--red)">Crashes / NullPointerException</b> — unvalidated input reaches business logic<br>
      🟡 <b style="color:var(--amber)">SecurityException without crash</b> — component exists but is permission-protected<br>
      🟢 <b style="color:var(--mint)">Activity launches with crafted data</b> — potential intent injection / open redirect<br>
      ⚪ <b style="color:var(--txt2)">content:// URI accepted</b> — possible ContentProvider data leakage
    </div>
  </div>
</div>

<!-- ===== CLASS TRACER ===== -->
<div class="page" id="pg-tracer">
  <div class="ph">
    <div class="pt">Class Dump &amp; Method <b>Tracer</b></div>
    <div class="ps">Live Java/ObjC class enumeration · Method hooking with args &amp; return values · Runtime reverse engineering</div>
    <div class="pa">
      <button class="btn btn-lime" onclick="startTrace()">▶ Start Trace</button>
      <button class="btn btn-ghost btn-sm" onclick="clearTraceLog()">✕ Clear</button>
    </div>
  </div>
  <div class="g2 mb16">
    <div class="card">
      <div class="ch"><div class="ct">⚙ Tracer Config</div></div>
      <div class="cb">
        <div class="fg"><label class="fl">Device</label><select class="fsl" id="tr-dev"></select></div>
        <div class="fg"><label class="fl">Target (package or PID)</label><input class="fi" id="tr-target" placeholder="com.secret.app"></div>
        <div class="fg"><label class="fl">Mode</label>
          <select class="fsl" id="tr-mode">
            <option value="attach">Attach</option>
            <option value="spawn">Spawn</option>
          </select>
        </div>
        <div class="fg"><label class="fl">Trace Mode</label>
          <select class="fsl" id="tr-trace-mode" onchange="updateTracerMode()">
            <option value="dump">Class Dump (enumerate all classes)</option>
            <option value="method">Method Tracer (hook specific class)</option>
          </select>
        </div>
        <div class="fg"><label class="fl">Class Filter / Target Class</label>
          <input class="fi" id="tr-filter" placeholder="e.g. ssl, okhttp3, com.bank.auth.PinManager">
        </div>
        <div class="fg"><label class="fl">Platform</label>
          <select class="fsl" id="tr-platform"><option value="android">Android (Java)</option><option value="ios">iOS (ObjC)</option></select>
        </div>
      </div>
    </div>
    <div class="card">
      <div class="ch"><div class="ct">💡 Tips</div></div>
      <div class="cb" style="font-size:12px;color:var(--txt3);line-height:2">
        <b style="color:var(--lime)">Class Dump mode</b><br>
        Lists all loaded classes matching your filter.<br>
        Try filters: <code>ssl</code>, <code>pin</code>, <code>trust</code>, <code>auth</code><br><br>
        <b style="color:var(--cyan)">Method Tracer mode</b><br>
        Hooks every method on the target class and logs all calls with arguments and return values.<br>
        Example: <code>okhttp3.CertificatePinner</code>
      </div>
    </div>
  </div>
  <div class="term" style="height:400px">
    <div class="term-hd">
      <div class="tdot" style="background:#ff5f57"></div><div class="tdot" style="background:#febc2e"></div><div class="tdot" style="background:#28c840"></div>
      <span style="font-size:10px;color:var(--txt3);margin-left:4px">class tracer output</span>
      <div class="flex1"></div>
      <span id="tr-count" style="font-size:10px;color:var(--txt3);margin-right:8px">0 entries</span>
    </div>
    <div class="term-bd" id="tr-log" style="max-height:340px">
      <div class="ll"><span class="lm" style="color:var(--txt4)">Class Tracer ready — configure and click Start Trace</span></div>
    </div>
  </div>
</div>

<!-- ===== MDM PROFILER ===== -->
<div class="page" id="pg-mdm">
  <div class="ph">
    <div class="pt">MDM &amp; Enterprise <b>Profiler</b></div>
    <div class="ps">Detect Intune · MobileIron · Jamf · AirWatch · Knox · Work Profiles · Policy restrictions</div>
    <div class="pa">
      <button class="btn btn-lime" onclick="runMdmProfile()">🏢 Profile Device</button>
    </div>
  </div>
  <div class="g2 mb16">
    <div class="card">
      <div class="ch"><div class="ct">⚙ Profile Setup</div></div>
      <div class="cb">
        <div class="fg"><label class="fl">Device</label><select class="fsl" id="mdm-dev"></select></div>
        <div id="mdm-result" style="display:none"></div>
      </div>
    </div>
    <div class="card">
      <div class="ch"><div class="ct">📖 Why MDM Matters</div></div>
      <div class="cb" style="font-size:12px;color:var(--txt3);line-height:2">
        Enterprise apps deployed via MDM often have <b style="color:var(--amber)">additional security policies</b> enforced at the OS level that Frida injection alone cannot bypass.<br><br>
        MDM can restrict: USB debugging disablement, VPN enforcement, screen capture blocking, app sideloading, and system certificate trust anchors.<br><br>
        Identifying the MDM vendor lets you look up vendor-specific bypass techniques.
      </div>
    </div>
  </div>
</div>

<!-- ===== REPORTS ===== -->
<div class="page" id="pg-reports">
  <div class="ph">
    <div class="pt">Security <b>Reports</b></div>
    <div class="ps">Generate professional HTML pentest reports · Combine bypass + SAST + API monitor findings</div>
    <div class="pa">
      <button class="btn btn-lime" onclick="loadReports()">↺ Refresh</button>
    </div>
  </div>
  <div class="g2 mb16">
    <div class="card">
      <div class="ch"><div class="ct">📊 Generate Report</div></div>
      <div class="cb">
        <div class="fg"><label class="fl">App / Target Name</label><input class="fi" id="rep-app" placeholder="Banking App v1.2.3"></div>
        <div class="fg"><label class="fl">Platform</label>
          <select class="fsl" id="rep-plat"><option value="android">Android</option><option value="ios">iOS</option></select>
        </div>
        <div class="fg"><label class="fl">Tester Name</label><input class="fi" id="rep-tester" placeholder="Your Name / Organization"></div>
        <div class="fg"><label class="fl">Bypass Session ID (optional)</label><input class="fi" id="rep-sess" placeholder="sess_xxxx (from active session)"></div>
        <button class="btn btn-lime btn-sm" onclick="generateReport()">📊 Generate Report</button>
        <div id="rep-status" class="mt8" style="font-size:12px;color:var(--txt3)"></div>
      </div>
    </div>
    <div class="card">
      <div class="ch"><div class="ct">📁 Saved Reports</div></div>
      <div class="cb0" id="rep-list" style="max-height:300px;overflow-y:auto">
        <div class="empty" style="padding:30px"><div class="empty-ic">📊</div><div class="empty-tt">No reports yet</div><div class="empty-sb">Generate a report after an assessment</div></div>
      </div>
    </div>
  </div>
</div>

<!-- ===== CVE CHECKER ===== -->
<div class="page" id="pg-cve">
  <div class="ph">
    <div class="pt">CVE &amp; Library <b>Checker</b></div>
    <div class="ps">Detect SDK versions in APK · Query OSV.dev · Find known CVEs for OkHttp, Firebase, Log4j, BouncyCastle &amp; 10+ more</div>
  </div>
  <div class="card mb16" id="cve-drop-card">
    <div class="cb">
      <div id="cve-drop-zone" style="border:2px dashed var(--rim2);border-radius:12px;padding:40px;text-align:center;cursor:pointer;transition:all .2s;"
        onclick="document.getElementById('cve-input').click()"
        ondragover="event.preventDefault();this.style.borderColor='var(--lime)'"
        ondragleave="this.style.borderColor='var(--rim2)'"
        ondrop="handleCveDrop(event)">
        <div style="font-size:44px;margin-bottom:14px">🛡</div>
        <div style="font-family:var(--sans);font-size:17px;font-weight:800">Drop APK for CVE Scan</div>
        <div style="font-size:12px;color:var(--txt3);margin-top:6px">Queries OSV.dev · 15+ library patterns · Offline fallback DB</div>
        <input type="file" id="cve-input" accept=".apk,.ipa" style="display:none" onchange="runCveCheck(this.files[0])">
      </div>
    </div>
  </div>
  <div id="cve-loading" style="display:none;text-align:center;padding:60px">
    <div class="pbar-indeterminate" style="max-width:300px;margin:0 auto 20px"></div>
    <div style="font-size:15px;font-weight:700">Detecting libraries &amp; querying CVE databases...</div>
  </div>
  <div id="cve-result" style="display:none"></div>
</div>

<!-- ===== APK DIFF ===== -->
<div class="page" id="pg-diff">
  <div class="ph">
    <div class="pt">APK Version <b>Diff</b></div>
    <div class="ps">Compare two APK versions · Detect permission changes · Find removed certificate pins · Flag security regressions</div>
  </div>
  <div class="g2 mb16">
    <div class="card">
      <div class="ch"><div class="ct">📦 APK Version A (Old)</div></div>
      <div class="cb">
        <div id="diff-drop-a" style="border:2px dashed var(--rim2);border-radius:8px;padding:24px;text-align:center;cursor:pointer;" onclick="document.getElementById('diff-input-a').click()">
          <div id="diff-label-a" style="font-size:13px;color:var(--txt3)">Drop or click — older version</div>
          <input type="file" id="diff-input-a" accept=".apk" style="display:none" onchange="setDiffFile('a',this.files[0])">
        </div>
      </div>
    </div>
    <div class="card">
      <div class="ch"><div class="ct">📦 APK Version B (New)</div></div>
      <div class="cb">
        <div id="diff-drop-b" style="border:2px dashed var(--rim2);border-radius:8px;padding:24px;text-align:center;cursor:pointer;" onclick="document.getElementById('diff-input-b').click()">
          <div id="diff-label-b" style="font-size:13px;color:var(--txt3)">Drop or click — newer version</div>
          <input type="file" id="diff-input-b" accept=".apk" style="display:none" onchange="setDiffFile('b',this.files[0])">
        </div>
      </div>
    </div>
  </div>
  <button class="btn btn-lime" onclick="runApkDiff()">🔀 Compare APKs</button>
  <div id="diff-loading" style="display:none;margin-top:20px;text-align:center"><div class="pbar-indeterminate" style="max-width:300px;margin:0 auto"></div></div>
  <div id="diff-result" style="display:none;margin-top:16px"></div>
</div>

<!-- ===== TRAFFIC REPLAY ===== -->
<div class="page" id="pg-traffic">
  <div class="ph">
    <div class="pt">Traffic Intercept &amp; <b>Replay</b></div>
    <div class="ps">Launch mitmproxy · Capture HTTP/S flows · Replay with modifications · Requires: pip install mitmproxy</div>
    <div class="pa">
      <button class="btn btn-lime" id="tr-start-btn" onclick="startTrafficCapture()">▶ Start Capture</button>
      <button class="btn btn-danger" id="tr-stop-btn" style="display:none" onclick="stopTrafficCapture()">■ Stop</button>
      <button class="btn btn-ghost btn-sm" onclick="loadTrafficFlows()">↺ Refresh Flows</button>
    </div>
  </div>
  <div class="g2 mb16">
    <div class="card">
      <div class="ch"><div class="ct">⚙ Setup</div></div>
      <div class="cb">
        <div class="fg"><label class="fl">Intercept Port</label><input class="fi" id="tr-port" value="8877" type="number"></div>
        <div style="font-size:11px;color:var(--txt3);margin-top:4px">Set device proxy → this machine:port<br>GhostPin will launch mitmdump automatically</div>
        <div id="tr-status" class="mt8" style="font-size:12px;color:var(--txt3)"></div>
      </div>
    </div>
    <div class="card">
      <div class="ch"><div class="ct">📊 Flow Stats</div></div>
      <div class="cb">
        <div class="g3" style="gap:10px">
          <div class="sc" style="padding:12px"><div class="sc-num" id="tr-flow-cnt" style="color:var(--cyan);font-size:24px">0</div><div class="sc-lbl">Captured Flows</div></div>
          <div class="sc" style="padding:12px"><div class="sc-num" id="tr-err-cnt" style="color:var(--red);font-size:24px">0</div><div class="sc-lbl">Error Responses</div></div>
          <div class="sc" style="padding:12px"><div class="sc-num" id="tr-https-cnt" style="color:var(--mint);font-size:24px">0</div><div class="sc-lbl">HTTPS Flows</div></div>
        </div>
      </div>
    </div>
  </div>
  <div id="tr-flows" class="card">
    <div class="ch"><div class="ct">📋 Captured Flows</div></div>
    <div class="cb0" id="tr-flow-list" style="max-height:300px;overflow-y:auto">
      <div class="empty" style="padding:30px"><div class="empty-ic">🌐</div><div class="empty-tt">No flows yet</div><div class="empty-sb">Start capture, then use your target app</div></div>
    </div>
  </div>
  <div id="tr-detail-panel" class="card mt8" style="display:none">
    <div class="ch"><div class="ct" id="tr-detail-title">Flow Detail</div>
      <div style="margin-left:auto;display:flex;gap:8px">
        <button class="btn btn-lime btn-xs" onclick="replayCurrentFlow()">↺ Replay</button>
        <button class="btn btn-ghost btn-xs" onclick="document.getElementById('tr-detail-panel').style.display='none'">✕</button>
      </div>
    </div>
    <div class="cb" style="font-size:11px;font-family:var(--mono)">
      <div style="margin-bottom:8px;font-weight:700;color:var(--txt2)">REQUEST</div>
      <pre id="tr-req-body" style="background:#050810;padding:10px;border-radius:6px;overflow-x:auto;white-space:pre-wrap;max-height:200px;overflow-y:auto"></pre>
      <div style="margin:8px 0;font-weight:700;color:var(--txt2)">RESPONSE</div>
      <pre id="tr-resp-body" style="background:#050810;padding:10px;border-radius:6px;overflow-x:auto;white-space:pre-wrap;max-height:200px;overflow-y:auto"></pre>
      <div style="margin:8px 0;font-weight:700;color:var(--txt2)">MODIFIED REPLAY BODY (optional)</div>
      <textarea id="tr-replay-body" class="fi" style="height:80px;font-family:var(--mono);font-size:11px;resize:vertical" placeholder="Leave empty to replay as-is, or paste modified request body"></textarea>
    </div>
  </div>
</div>

<!-- ===== GUIDED CHECKLIST ===== -->
<div class="page" id="pg-checklist">
  <div class="ph">
    <div class="pt">Guided Testing <b>Checklist</b></div>
    <div class="ps">App-type workflows · Step-by-step guidance · Recommended scripts per scenario</div>
  </div>
  <div class="g4 mb16" id="checklist-types"></div>
  <div id="checklist-active" style="display:none">
    <div class="card">
      <div class="ch">
        <div class="ct" id="checklist-name">Checklist</div>
        <div style="margin-left:auto"><button class="btn btn-ghost btn-xs" onclick="closeChecklist()">✕ Close</button></div>
      </div>
      <div class="cb0" id="checklist-steps" style="padding:4px 0"></div>
    </div>
  </div>
</div>

<!-- ===== WORKSPACES ===== -->
<div class="page" id="pg-workspaces">
  <div class="ph">
    <div class="pt">Target <b>Workspaces</b></div>
    <div class="ps">Per-app settings persistence · Remember scripts, proxy, session history per package</div>
    <div class="pa">
      <button class="btn btn-lime" onclick="loadWorkspaces()">↺ Refresh</button>
    </div>
  </div>
  <div class="g2 mb16">
    <div class="card">
      <div class="ch"><div class="ct">➕ Create / Open Workspace</div></div>
      <div class="cb">
        <div class="fg"><label class="fl">Package Name</label><input class="fi" id="ws-pkg" placeholder="com.mybank.app"></div>
        <button class="btn btn-lime btn-sm" onclick="openWorkspace()">Open Workspace</button>
      </div>
    </div>
    <div class="card">
      <div class="ch"><div class="ct">📁 Recent Workspaces</div></div>
      <div class="cb0" id="ws-list" style="max-height:200px;overflow-y:auto">
        <div class="empty" style="padding:20px"><div class="empty-ic">💼</div><div class="empty-tt">No workspaces yet</div></div>
      </div>
    </div>
  </div>
  <div id="ws-detail" style="display:none" class="card">
    <div class="ch"><div class="ct" id="ws-title">Workspace</div>
      <div style="margin-left:auto"><button class="btn btn-danger btn-xs" onclick="deleteWorkspace()">Delete</button></div>
    </div>
    <div class="cb" id="ws-body"></div>
  </div>
</div>


<!-- ===== API MAP ===== -->
<div class="page" id="pg-map">
  <div class="page-header">
    <div class="ph-title">API Endpoint Auto-Discovery</div>
    <div class="ph-sub">Automatically extracts URLs/GraphQL from SAST scans and dynamic live traffic.</div>
  </div>
  
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
    <div>
      <button class="btn btn-lime" onclick="refreshApiMap()">🔄 Refresh Map</button>
      <button class="btn btn-ghost" onclick="extractStaticApis()">🔍 Force Static Extraction (from last scan)</button>
    </div>
    <button class="btn btn-primary" onclick="exportPostman()">📦 Export to Postman / Burp</button>
  </div>
  
  <div id="map-stats" style="margin-bottom:16px;font-size:12px;color:var(--txt3);">0 hosts • 0 endpoints</div>
  
  <div id="api-map-results" style="display:flex;flex-direction:column;gap:16px;">
    <div style="padding:40px;text-align:center;color:var(--txt3);border:1px dashed var(--rim);border-radius:6px;">
      Map is empty. Run a Vulnerability Scan or intercept traffic via Replay to populate.
    </div>
  </div>
</div>

</div><!-- #main -->
</div><!-- #shell -->
<div id="toasts"></div>

<script>
// ================================================================
// GHOSTPIN v5.0 — Frontend Engine
// ================================================================

// ── State ──────────────────────────────────────────────────────
var S = {
  devices: [],
  selDev: null,
  selScripts: new Set(['universal-android-bypass']),
  anti: {root:false, frida:false, jailbreak:false, emulator:false},
  curSession: null,
  curSSE: null,
  allProcs: [],
  toolStatus: {},
  analysisResult: null,
  logLineCount: 0,
  settings: {fridaPort:27042, pollInterval:5, logLevel:'all', maxLog:2000},
  pollTimer: null
};

// ── Script definitions ─────────────────────────────────────────
var SCRIPTS = [
  {id:'universal-android-bypass', name:'Universal Android SSL', desc:'OkHttp3, TrustManager, SSLContext, Conscrypt, TrustKit, WebView, NSC Android 14+', tags:['android','ssl'], diff:'easy', platform:'android'},
  {id:'obfuscation-resilient', name:'Obfuscation Resilient', desc:'Method-signature matching defeats ProGuard/R8/DexGuard obfuscation', tags:['android','obfusc'], diff:'medium', platform:'android'},
  {id:'root-detection-bypass', name:'Root Detection Bypass', desc:'RootBeer, file checks, Build.TAGS, exec() blocking, Magisk/KSU', tags:['android','evasion'], diff:'easy', platform:'android'},
  {id:'frida-evasion', name:'Frida Detection Evasion', desc:'/proc/maps filter, port hiding, frida-agent module cloaking', tags:['android','evasion'], diff:'medium', platform:'android'},
  {id:'ios-universal', name:'iOS Universal SSL', desc:'SecTrustEvaluate, NSURLSession, TrustKit, AFNetworking, SSLHandshake', tags:['ios','ssl'], diff:'easy', platform:'ios'},
  {id:'ios-jailbreak-bypass', name:'iOS Jailbreak Bypass', desc:'NSFileManager, canOpenURL, Cydia/Sileo/Zebra detection evasion', tags:['ios','evasion'], diff:'medium', platform:'ios'},
  {id:'flutter-android', name:'Flutter Android', desc:'libflutter.so BoringSSL — pattern scan + ssl_crypto_x509 export hook', tags:['android','flutter'], diff:'hard', platform:'android'},
  {id:'flutter-ios', name:'Flutter iOS', desc:'Flutter.framework BoringSSL with architecture-aware pattern scan', tags:['ios','flutter'], diff:'hard', platform:'ios'},
  {id:'native-openssl', name:'Native OpenSSL/BoringSSL', desc:'SSL_CTX_set_verify, X509_verify_cert, ssl_verify_peer_cert native hooks', tags:['android','native'], diff:'hard', platform:'both'},
  {id:'grpc-bypass', name:'gRPC / Netty', desc:'NettyChannelBuilder, OkHttp grpc transport, SslHandler, InsecureTrustManager', tags:['android','grpc'], diff:'hard', platform:'android'},
  {id:'xamarin-bypass', name:'Xamarin / MAUI', desc:'Mono ServicePointMgr, AndroidMessageHandler, HttpClientHandler', tags:['android','ios'], diff:'medium', platform:'both'},
  {id:'certificate-transparency', name:'Certificate Transparency', desc:'CTVerifier, PolicyCompliance, NetworkSecurityConfig CT enforcement', tags:['android','ssl'], diff:'hard', platform:'android'},
  {id:'unity-il2cpp', name:'Unity / IL2CPP', desc:'Mono runtime + IL2CPP export enumeration + pattern-scan fallback', tags:['android','ios','native'], diff:'expert', platform:'both'},
  {id:'quic-blocker', name:'QUIC/HTTP3 Blocker', desc:'CronetEngine disabler + iptables UDP 443 block — forces HTTP/2 fallback', tags:['android','grpc'], diff:'medium', platform:'android'}
];

var PAGE_TITLES = {
  dashboard:'Dashboard', devices:'Device Manager', bypass:'Run Bypass',
  analyzer:'APK/IPA Analyzer', scripts:'Script Library', editor:'Script Editor',
  proxy:'Proxy & QUIC', cert:'CA Injection', sessions:'Bypass Sessions',
  tools:'Tool Check', settings:'Settings'
};

// ── Navigation ─────────────────────────────────────────────────
function go(id) {
  document.querySelectorAll('.page').forEach(function(p){ p.classList.remove('on'); });
  document.querySelectorAll('.ni, .rb').forEach(function(el){ el.classList.remove('on'); });

  var pg = document.getElementById('pg-' + id);
  if (pg) pg.classList.add('on');

  var ni = document.getElementById('ni-' + id);
  if (ni) ni.classList.add('on');
  var rb = document.getElementById('rb-' + id);
  if (rb) rb.classList.add('on');

  var title = PAGE_TITLES[id] || id;
  document.getElementById('tb-title').textContent = title;

  if (id === 'sessions') loadSessions();
  if (id === 'tools') runToolCheck();
  if (id === 'scripts') renderLib();
  if (id === 'editor') populateEditorSel();
  if (id === 'bypass') renderBpGrid();
}

// ── Theme ──────────────────────────────────────────────────────
function toggleTheme() {
  var isLight = document.documentElement.getAttribute('data-theme') === 'light';
  var next = isLight ? 'dark' : 'light';
  applyTheme(next);
  try { localStorage.setItem('gp-theme', next); } catch(e) {}
}
function applyTheme(t) {
  var btn = document.getElementById('theme-btn');
  if (t === 'light') {
    document.documentElement.setAttribute('data-theme', 'light');
    if (btn) btn.innerHTML = '&#9728;'; // ☀ sun = currently light, click for dark
    if (btn) btn.title = 'Switch to dark mode';
  } else {
    document.documentElement.removeAttribute('data-theme');
    if (btn) btn.innerHTML = '&#9790;'; // ☾ moon = currently dark, click for light
    if (btn) btn.title = 'Switch to light mode';
  }
}
(function() {
  try {
    var saved = localStorage.getItem('gp-theme');
    if (saved === 'light') document.documentElement.setAttribute('data-theme', 'light');
  } catch(e) {}
})();

// ── Toast ──────────────────────────────────────────────────────
function toast(msg, type) {
  type = type || 'ok';
  var icons = {ok:'&#10003;', err:'&#10007;', warn:'&#9888;'};
  var colors = {ok:'var(--mint)', err:'var(--red)', warn:'var(--amber)'};
  var el = document.createElement('div');
  el.className = 'toast ' + type;
  el.innerHTML = '<span style="color:' + colors[type] + ';font-weight:700;font-size:14px">' + icons[type] + '</span><span>' + msg + '</span>';
  document.getElementById('toasts').appendChild(el);
  setTimeout(function(){ if(el.parentNode) el.parentNode.removeChild(el); }, 3500);
}

// ── API ────────────────────────────────────────────────────────
function api(path, method, body) {
  method = method || 'GET';
  var opts = {method: method, headers: {}};
  if (body) {
    opts.headers['Content-Type'] = 'application/json';
    opts.body = JSON.stringify(body);
  }
  return fetch(path, opts).then(function(r){ return r.json(); }).catch(function(e){
    console.error('API error:', e);
    return null;
  });
}

// ── Devices ────────────────────────────────────────────────────
function refreshDevices() {
  api('/api/devices').then(function(data) {
    if (!data) { toast('Cannot reach server', 'err'); return; }
    S.devices = data;
    renderDeviceUI(data);
  });
}

function renderDeviceUI(devs) {
  var cnt = devs.length;
  document.getElementById('ds-dev').textContent = cnt;
  document.getElementById('ni-dev-count').textContent = cnt;

  var badge = document.getElementById('rb-dev-badge');
  if (cnt > 0) { badge.style.display = 'flex'; badge.textContent = cnt; }
  else badge.style.display = 'none';

  var sbDev = document.getElementById('sb-dev');
  var sbDevT = document.getElementById('sb-dev-t');
  if (cnt > 0) {
    sbDev.className = 'sb sb-ok';
    sbDevT.textContent = cnt + ' Device' + (cnt > 1 ? 's' : '');
    document.getElementById('sb-dev-label').textContent = (devs[0].model || devs[0].serial);
  } else {
    sbDev.className = 'sb sb-off';
    sbDevT.textContent = 'No Devices';
    document.getElementById('sb-dev-label').textContent = 'No device connected';
  }

  var hasFrida = devs.some(function(d){ return d.fridaRunning; });
  var sbFri = document.getElementById('sb-fri');
  sbFri.className = 'sb ' + (hasFrida ? 'sb-ok' : 'sb-off');
  document.getElementById('sb-fri-t').textContent = hasFrida ? 'Frida On' : 'Frida Off';

  // Dashboard mini list
  var dlist = document.getElementById('dash-devlist');
  if (cnt === 0) {
    dlist.innerHTML = '<div class="empty" style="padding:28px"><div class="empty-ic">&#128241;</div><div class="empty-tt">No devices</div><div class="empty-sb">Connect via USB &middot; <code>adb start-server</code></div></div>';
  } else {
    dlist.innerHTML = devs.map(function(d) {
      return '<div style="display:flex;align-items:center;gap:10px;padding:10px 16px;border-bottom:1px solid var(--rim);cursor:pointer" onclick="go(\\x27devices\\x27);selectDev(\\x27' + esc(d.serial) + '\\x27)">' +
        '<span style="font-size:22px">' + (d.platform==='ios'?'&#127822;':'&#129302;') + '</span>' +
        '<div style="flex:1;min-width:0">' +
          '<div style="font-family:var(--sans);font-size:13px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">' + esc((d.manufacturer||'')+' '+(d.model||d.serial)) + '</div>' +
          '<div style="font-size:10px;color:var(--txt3);margin-top:1px">' + esc(d.serial) + ' &middot; ' + (d.platform==='android'?'Android '+(d.androidVersion||'?'):'iOS') + '</div>' +
        '</div>' +
        '<div style="display:flex;gap:4px;flex-wrap:wrap">' +
          '<span class="tag ' + (d.isRooted?'t-root':'t-noroot') + '">' + (d.isRooted?'root':'no root') + '</span>' +
          '<span class="tag ' + (d.fridaRunning?'t-frida':'t-nofrida') + '">' + (d.fridaRunning?'frida &#10003;':'frida &#10007;') + '</span>' +
        '</div>' +
      '</div>';
    }).join('');
  }

  // Full device list
  var flist = document.getElementById('dev-full-list');
  if (flist) {
    if (cnt === 0) {
      flist.innerHTML = '<div class="empty"><div class="empty-ic">&#128241;</div><div class="empty-tt">No devices</div><div class="empty-sb">Ensure ADB running: <code>adb start-server</code></div></div>';
    } else {
      flist.innerHTML = devs.map(devCard).join('');
    }
  }

  // Populate all device selects
  var selHtml = cnt === 0
    ? '<option value="">-- No devices --</option>'
    : devs.map(function(d){ return '<option value="' + esc(d.serial) + '">' + esc((d.manufacturer||'')+' '+(d.model||d.serial)+' ('+d.serial+')') + '</option>'; }).join('');
  ['bp-dev','cert-dev','prx-dev','quic-dev','fwd-dev','adb-dev-sel'].forEach(function(id){
    var el = document.getElementById(id);
    if (el) el.innerHTML = selHtml;
  });
}

function devCard(d) {
  var sel = S.selDev && S.selDev.serial === d.serial;
  return '<div class="dvc ' + (sel?'sel':'') + ' ' + (d.fridaRunning?'fri':'') + '" onclick="selectDev(\\x27' + esc(d.serial) + '\\x27)">' +
    '<div class="dv-ic">' + (d.platform==='ios'?'&#127822;':'&#129302;') + '</div>' +
    '<div class="dv-info">' +
      '<div class="dv-name">' + esc((d.manufacturer||'')+' '+(d.model||d.serial)) + '</div>' +
      '<div class="dv-ser">' + esc(d.serial) + '</div>' +
      '<div class="dv-meta">' + (d.platform==='android' ? 'Android '+(d.androidVersion||'?')+' (API '+(d.apiLevel||'?')+') &middot; '+(d.abi||'?') : 'iOS Device') + (d.battery!=null?' &middot; &#128267;'+d.battery+'%':'') + '</div>' +
      '<div class="dv-tags">' +
        '<span class="tag ' + (d.platform==='android'?'t-and':'t-ios') + '">' + d.platform + '</span>' +
        '<span class="tag ' + (d.type==='network'?'t-wifi':'t-usb') + '">' + (d.type||'usb') + '</span>' +
        '<span class="tag ' + (d.isRooted?'t-root':'t-noroot') + '">' + (d.isRooted?'rooted':'no root') + '</span>' +
        '<span class="tag ' + (d.fridaRunning?'t-frida':'t-nofrida') + '">' + (d.fridaRunning?'frida running':'frida off') + '</span>' +
      '</div>' +
      '<div class="dv-acts">' +
        '<button class="btn btn-lime btn-xs" onclick="event.stopPropagation();selectDev(\\x27' + esc(d.serial) + '\\x27)">Select</button>' +
        '<button class="btn btn-ghost btn-xs" onclick="event.stopPropagation();loadProcs(\\x27' + esc(d.serial) + '\\x27)">Processes</button>' +
        '<button class="btn btn-ghost btn-xs" onclick="event.stopPropagation();showFsPanel()">Frida</button>' +
      '</div>' +
    '</div>' +
  '</div>';
}

function selectDev(serial) {
  S.selDev = S.devices.find(function(d){ return d.serial === serial; });
  renderDeviceUI(S.devices);
  showDevDetail(S.selDev);
  document.getElementById('fs-panel').style.display = 'block';
  document.getElementById('proc-panel').style.display = 'block';
  loadProcs(serial);
  toast('Device: ' + (S.selDev.model || serial), 'ok');
}

function showDevDetail(d) {
  var el = document.getElementById('dev-detail');
  if (!d) { el.innerHTML = '<div class="empty"><div class="empty-ic">&#128073;</div><div class="empty-tt">Select a device</div></div>'; return; }
  el.innerHTML = '<div class="card"><div class="ch"><div class="ct">&#128203; Device Info</div></div><div class="cb">' +
    kv('Model', esc((d.manufacturer||'')+' '+(d.model||'--'))) +
    kv('Serial', '<code>'+esc(d.serial)+'</code>') +
    kv('Android', esc((d.androidVersion||'--')+' (API '+(d.apiLevel||'--')+')')) +
    kv('Architecture', esc(d.abi||'--')) +
    kv('Build Type', esc(d.buildType||'--')) +
    kv('Root', '<span style="color:' + (d.isRooted?'var(--mint)':'var(--red)') + '">' + (d.isRooted?'&#10003; Rooted':'&#10007; Not Rooted') + '</span>') +
    kv('Frida Server', '<span style="color:' + (d.fridaRunning?'var(--mint)':'var(--red)') + '">' + (d.fridaRunning?'&#10003; Running':'&#10007; Not Running') + '</span>') +
    (d.battery!=null ? kv('Battery', d.battery+'%') : '') +
  '</div></div>';
}

function kv(k, v) {
  return '<div class="kv"><div class="kv-k">' + k + '</div><div class="kv-v">' + v + '</div></div>';
}

function showFsPanel() {
  document.getElementById('fs-panel').style.display = 'block';
}

function loadProcs(serial) {
  var s = serial || (S.selDev && S.selDev.serial);
  if (!s) return;
  var plist = document.getElementById('proc-list');
  plist.innerHTML = '<div style="padding:14px;font-size:12px;color:var(--txt3)"><span class="spin"></span> Loading...</div>';
  var plat = S.selDev ? S.selDev.platform : 'android';
  api('/api/processes?serial=' + encodeURIComponent(s) + '&platform=' + plat).then(function(data) {
    S.allProcs = data || [];
    renderProcs(S.allProcs);
  });
}

function renderProcs(procs) {
  var el = document.getElementById('proc-list');
  if (!procs.length) {
    el.innerHTML = '<div style="padding:14px;font-size:12px;color:var(--txt3)">No processes found (is frida-ps installed?)</div>';
    return;
  }
  el.innerHTML = '<table class="tbl"><thead><tr><th>PID</th><th>Process</th><th></th></tr></thead><tbody>' +
    procs.map(function(p) {
      return '<tr><td style="color:var(--txt3)">' + esc(p.pid) + '</td><td>' + esc(p.name) + '</td>' +
        '<td><button class="btn btn-ghost btn-xs" onclick="useProc(\\x27' + esc(p.pid) + '\\x27,\\x27' + esc(p.name).replace(/'/g,'') + '\\x27)">&#8594; Use</button></td></tr>';
    }).join('') +
  '</tbody></table>';
}

function filterProcs() {
  var q = document.getElementById('proc-filter').value.toLowerCase();
  renderProcs(S.allProcs.filter(function(p){ return p.name.toLowerCase().includes(q) || String(p.pid).includes(q); }));
}

function useProc(pid, name) {
  go('bypass');
  document.getElementById('bp-target').value = name;
  toast('Target: ' + name + ' (PID ' + pid + ')', 'ok');
}

// ── ADB Shell ──────────────────────────────────────────────────
function runShell() {
  var serial = document.getElementById('adb-dev-sel').value || (S.selDev && S.selDev.serial);
  if (!serial) { toast('Select a device first', 'warn'); return; }
  var cmd = document.getElementById('adb-cmd').value.trim();
  if (!cmd) return;
  var out = document.getElementById('shell-out');
  appendShell(out, '$ ' + cmd, 'var(--lime)');
  api('/api/adb/shell', 'POST', {serial: serial, cmd: cmd}).then(function(data) {
    if (!data) { appendShell(out, 'Error: no response', 'var(--red)'); return; }
    if (data.stdout) appendShell(out, data.stdout, 'var(--txt2)');
    if (data.stderr) appendShell(out, data.stderr, 'var(--amber)');
    if (data.rc !== 0 && !data.stdout && !data.stderr) appendShell(out, 'Exit: ' + data.rc, 'var(--red)');
  });
}

function appendShell(el, txt, color) {
  var div = document.createElement('div');
  div.className = 'll';
  div.innerHTML = '<span class="lm" style="color:' + color + '">' + esc(txt) + '</span>';
  el.appendChild(div);
  el.scrollTop = el.scrollHeight;
}

function clearShell() { document.getElementById('shell-out').innerHTML = ''; }

function quickCmd(cmd) {
  document.getElementById('adb-cmd').value = cmd;
  runShell();
}

function adbStartServer() {
  toast('Running adb start-server...', 'ok');
  refreshDevices();
}

// ── Frida Server ───────────────────────────────────────────────
function pushFrida() {
  var serial = S.selDev && S.selDev.serial;
  if (!serial) { toast('Select a device first', 'warn'); return; }
  var path = document.getElementById('fs-path').value.trim();
  if (!path) { toast('Enter frida-server binary path', 'warn'); return; }
  var logEl = document.getElementById('fs-log');
  logEl.style.display = 'flex';
  logEl.innerHTML = stepItem('act', 'Pushing frida-server...');
  api('/api/frida/push', 'POST', {serial: serial, serverPath: path}).then(function(data) {
    if (!data) { logEl.innerHTML = stepItem('err', 'Request failed'); return; }
    logEl.innerHTML = data.steps.map(function(s) {
      var t = s.startsWith('&#10003;') || s.includes('OK') || s.includes('RUNNING') ? 'done' : s.includes('FAILED') || s.includes('NOT RUNNING') ? 'err' : 'act';
      return stepItem(t, s);
    }).join('');
    if (data.ok) { toast('Frida server started!', 'ok'); refreshDevices(); }
    else toast('Frida server failed — check log', 'err');
  });
}

function stopFrida() {
  var serial = S.selDev && S.selDev.serial;
  if (!serial) return;
  api('/api/frida/stop', 'POST', {serial: serial}).then(function(){ toast('Frida server stopped', 'ok'); refreshDevices(); });
}

function fwdFrida() {
  var serial = S.selDev && S.selDev.serial;
  if (!serial) return;
  var port = S.settings.fridaPort;
  api('/api/adb/forward', 'POST', {serial: serial, localPort: port, remotePort: port}).then(function(data) {
    if (data && data.ok) toast('Port ' + port + ' forwarded', 'ok');
    else toast('Forward failed', 'err');
  });
}

function stepItem(state, text) {
  return '<div class="sti"><div class="stdt ' + state + '"></div><div style="font-size:11px">' + text + '</div></div>';
}

// ── Bypass ─────────────────────────────────────────────────────
function renderBpGrid() {
  var plat = document.getElementById('bp-plat') ? document.getElementById('bp-plat').value : 'android';
  var grid = document.getElementById('bp-script-grid');
  var filtered = SCRIPTS.filter(function(s){ return s.platform === 'both' || s.platform === plat; });
  grid.innerHTML = filtered.map(scriptCard).join('');
  updateSelCount();
}

function scriptCard(s) {
  var sel = S.selScripts.has(s.id);
  return '<div class="scc ' + (sel?'sel':'') + '" onclick="toggleScript(\\x27' + s.id + '\\x27)">' +
    '<div class="sc-ck">' + (sel?'&#10003;':'') + '</div>' +
    '<div class="sc-nm">' + s.name + '</div>' +
    '<div class="sc-ds">' + s.desc + '</div>' +
    '<div class="sc-tg">' +
      s.tags.map(function(t){ return '<span class="tag t-' + t + '">' + t + '</span>'; }).join('') +
      '<span class="tag t-' + s.diff + '">' + s.diff + '</span>' +
    '</div>' +
  '</div>';
}

function toggleScript(id) {
  if (S.selScripts.has(id)) S.selScripts.delete(id); else S.selScripts.add(id);
  renderBpGrid();
}

function updateSelCount() {
  var el = document.getElementById('scr-sel-cnt');
  if (el) el.textContent = S.selScripts.size;
}

function selAllScripts() {
  var plat = document.getElementById('bp-plat').value;
  SCRIPTS.filter(function(s){ return s.platform==='both'||s.platform===plat; }).forEach(function(s){ S.selScripts.add(s.id); });
  renderBpGrid();
}

function clearSelScripts() {
  S.selScripts.clear();
  renderBpGrid();
}

function updatePlatform() {
  S.selScripts.clear();
  var plat = document.getElementById('bp-plat').value;
  S.selScripts.add(plat === 'ios' ? 'ios-universal' : 'universal-android-bypass');
  renderBpGrid();
}

function antiToggle(key) {
  S.anti[key] = !S.anti[key];
  var el = document.getElementById('at-' + (key==='jailbreak'?'jb':key==='emulator'?'emu':key));
  if (el) el.className = 'tg' + (S.anti[key]?' on':'');
}

function clearCustom() { document.getElementById('custom-script').value = ''; }

function startBypass() {
  var serial = document.getElementById('bp-dev').value;
  var target = document.getElementById('bp-target').value.trim();
  var plat = document.getElementById('bp-plat').value;
  var spawnMode = document.getElementById('bp-mode').value === 'spawn';
  var custom = document.getElementById('custom-script').value;

  if (!serial) { toast('Select a device', 'warn'); return; }
  if (!target) { toast('Enter target package or PID', 'warn'); return; }
  if (S.selScripts.size === 0) { toast('Select at least one script', 'warn'); return; }

  var logEl = document.getElementById('bp-log');
  logEl.innerHTML = '';
  S.logLineCount = 0;

  bpLog('info', 'Starting GhostPin bypass session...');
  bpLog('info', 'Target: ' + target + ' | Platform: ' + plat + ' | Mode: ' + (spawnMode?'spawn':'attach'));
  bpLog('info', 'Scripts: ' + Array.from(S.selScripts).join(', '));

  document.getElementById('bp-start-btn').style.display = 'none';
  document.getElementById('bp-stop-btn').style.display = 'inline-flex';
  document.getElementById('bp-save-btn').style.display = 'inline-flex';
  document.getElementById('bp-export-btn').style.display = 'inline-flex';
  document.getElementById('bp-status').innerHTML = '<div class="live-dot"></div><span style="color:var(--red)">Session active</span>';
  document.getElementById('live-indicator').style.display = 'flex';
  document.getElementById('sb-sess').className = 'sb sb-ok';
  document.getElementById('sb-sess-t').textContent = 'Session Active';
  document.getElementById('ds-sess').textContent = '1';

  api('/api/bypass/start', 'POST', {
    serial: serial,
    target: target,
    platform: plat,
    scriptIds: Array.from(S.selScripts),
    spawnMode: spawnMode,
    antiDetection: S.anti,
    customScript: custom
  }).then(function(data) {
    if (!data || !data.sessionId) {
      toast('Failed to start session', 'err');
      resetBpUI();
      return;
    }
    S.curSession = data.sessionId;
    toast('Bypass session started!', 'ok');

    if (S.curSSE) S.curSSE.close();
    var sse = new EventSource('/api/bypass/stream/' + data.sessionId);
    S.curSSE = sse;
    sse.onmessage = function(e) {
      try {
        var entry = JSON.parse(e.data);
        bpLog(entry.level, entry.msg, entry.ts);
      } catch(err) {}
    };
    sse.onerror = function() {
      bpLog('warn', 'Stream ended or session completed');
      resetBpUI();
    };
  });
}

function bpLog(level, msg, ts) {
  var el = document.getElementById('bp-log');
  var t = ts ? new Date(ts).toTimeString().slice(0,8) : new Date().toTimeString().slice(0,8);
  var lvMap = {info:'lv-info', frida:'lv-frida', error:'lv-error', warn:'lv-warn', success:'lv-success', inject:'lv-inject'};
  var div = document.createElement('div');
  div.className = 'll';
  div.innerHTML = '<span class="lts">' + t + '</span>' +
    '<span class="llv ' + (lvMap[level]||'lv-info') + '">' + (level||'info').slice(0,5) + '</span>' +
    '<span class="lm">' + esc(msg) + '</span>';
  el.appendChild(div);
  S.logLineCount++;
  var maxLog = S.settings.maxLog || 2000;
  while (el.children.length > maxLog) el.removeChild(el.firstChild);
  el.scrollTop = el.scrollHeight;
  var cnt = document.getElementById('bp-log-count');
  if (cnt) cnt.textContent = S.logLineCount + ' lines';
}

function stopBypass() {
  if (S.curSSE) { S.curSSE.close(); S.curSSE = null; }
  if (S.curSession) {
    api('/api/bypass/stop', 'POST', {sessionId: S.curSession});
  }
  resetBpUI();
  toast('Session stopped', 'warn');
}

function resetBpUI() {
  document.getElementById('bp-start-btn').style.display = 'inline-flex';
  document.getElementById('bp-stop-btn').style.display = 'none';
  document.getElementById('bp-status').innerHTML = '';
  document.getElementById('live-indicator').style.display = 'none';
  document.getElementById('sb-sess').className = 'sb sb-off';
  document.getElementById('sb-sess-t').textContent = 'No Session';
  document.getElementById('ds-sess').textContent = '0';
}

function saveSession() {
  if (!S.curSession) return;
  var name = prompt('Session name:', 'Bypass ' + new Date().toLocaleString());
  if (!name) return;
  api('/api/sessions/save', 'POST', {sessionId: S.curSession, name: name}).then(function(d) {
    if (d && d.ok) toast('Session saved!', 'ok'); else toast('Save failed', 'err');
  });
}

function exportLog() {
  var lines = Array.from(document.querySelectorAll('#bp-log .ll')).map(function(l){ return l.textContent; }).join('\\n');
  var blob = new Blob([lines], {type:'text/plain'});
  var a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'ghostpin-' + (S.curSession||'log') + '.txt';
  a.click();
}

function clearBpLog() {
  document.getElementById('bp-log').innerHTML = '';
  S.logLineCount = 0;
  document.getElementById('bp-log-count').textContent = '0 lines';
}

// ── Script Library ─────────────────────────────────────────────
function renderLib() {
  var filter = document.getElementById('lib-filter') ? document.getElementById('lib-filter').value : 'all';
  var filtered = filter === 'all' ? SCRIPTS : SCRIPTS.filter(function(s) {
    if (filter === 'android' || filter === 'ios') return s.platform === filter || s.platform === 'both';
    if (filter === 'easy' || filter === 'hard') return s.diff === filter || (filter === 'hard' && s.diff === 'expert');
    return s.tags.includes(filter);
  });
  var grid = document.getElementById('lib-grid');
  grid.innerHTML = filtered.map(function(s) {
    return '<div class="scc" style="cursor:default">' +
      '<div class="sc-nm">' + s.name + '</div>' +
      '<div class="sc-ds">' + s.desc + '</div>' +
      '<div class="sc-tg">' +
        s.tags.map(function(t){ return '<span class="tag t-' + t + '">' + t + '</span>'; }).join('') +
        '<span class="tag t-' + s.diff + '">' + s.diff + '</span>' +
        '<span class="tag ' + (s.platform==='android'?'t-and':s.platform==='ios'?'t-ios':'t-both') + '">' + s.platform + '</span>' +
      '</div>' +
      '<div style="margin-top:10px;display:flex;gap:6px">' +
        '<button class="btn btn-ghost btn-xs" onclick="loadScriptToEdit(\\x27' + s.id + '\\x27)">&#9998; Edit</button>' +
        '<button class="btn btn-lime btn-xs" onclick="addScriptToBp(\\x27' + s.id + '\\x27)">+ Add to Bypass</button>' +
      '</div>' +
    '</div>';
  }).join('');
}

function loadScriptToEdit(id) {
  go('editor');
  document.getElementById('ed-id').value = id;
  api('/api/scripts/' + id).then(function(data) {
    if (data && data.content) {
      document.getElementById('ed-code').value = data.content;
      edChanged();
      toast('Loaded: ' + id, 'ok');
    }
  });
}

function addScriptToBp(id) {
  S.selScripts.add(id);
  renderBpGrid();
  toast('Added: ' + id, 'ok');
}

// ── Script Editor ──────────────────────────────────────────────
function populateEditorSel() {
  var sel = document.getElementById('ed-load-sel');
  if (!sel) return;
  sel.innerHTML = '<option value="">-- Load a built-in script --</option>' +
    SCRIPTS.map(function(s){ return '<option value="' + s.id + '">' + s.name + '</option>'; }).join('');
}

function loadIntoEditor() {
  var id = document.getElementById('ed-load-sel').value;
  if (!id) return;
  api('/api/scripts/' + id).then(function(data) {
    if (data && data.content) {
      document.getElementById('ed-id').value = id;
      document.getElementById('ed-code').value = data.content;
      edChanged();
    }
  });
}

function edChanged() {
  var code = document.getElementById('ed-code').value;
  document.getElementById('ed-chars').textContent = code.length + ' chars';
  document.getElementById('ed-status').textContent = 'Unsaved';
  document.getElementById('ed-status').style.color = 'var(--amber)';
}

function saveEditorScript() {
  var id = document.getElementById('ed-id').value.trim();
  var code = document.getElementById('ed-code').value;
  if (!id) { toast('Enter a script ID', 'warn'); return; }
  api('/api/scripts/' + id, 'POST', {content: code}).then(function(){
    document.getElementById('ed-status').textContent = 'Saved';
    document.getElementById('ed-status').style.color = 'var(--mint)';
    toast('Script saved: ' + id, 'ok');
  });
}

function clearEditor() {
  document.getElementById('ed-code').value = '';
  document.getElementById('ed-id').value = '';
  document.getElementById('ed-chars').textContent = '0 chars';
}

function injectEditor() {
  var code = document.getElementById('ed-code').value.trim();
  if (!code) { toast('No code to inject', 'warn'); return; }
  document.getElementById('custom-script').value = code;
  go('bypass');
  toast('Script loaded into bypass custom slot', 'ok');
}

// ── APK Analyzer ───────────────────────────────────────────────
function handleDrop(e) {
  e.preventDefault();
  document.getElementById('drop-zone').style.borderColor = 'var(--rim2)';
  document.getElementById('drop-zone').style.background = '';
  var f = e.dataTransfer.files[0];
  if (f) analyzeFile(f);
}

function analyzeFile(f) {
  if (!f) return;
  var ext = f.name.split('.').pop().toLowerCase();
  if (!['apk','ipa','xapk','apks'].includes(ext)) { toast('Unsupported file type: .' + ext, 'err'); return; }

  document.getElementById('az-loading').style.display = 'block';
  document.getElementById('az-result').style.display = 'none';

  var steps = ['Uploading file...', 'Decompiling APK...', 'Scanning DEX bytecode...', 'Detecting frameworks...', 'Analyzing native libs...', 'Finalizing...'];
  var si = 0;
  var logEl = document.getElementById('az-log');
  var stepTimer = setInterval(function() {
    if (si < steps.length) { logEl.textContent = steps[si++]; }
  }, 700);

  var fd = new FormData();
  fd.append('file', f);
  fetch('/api/apk/analyze', {method:'POST', body:fd})
    .then(function(r){ return r.json(); })
    .then(function(result) {
      clearInterval(stepTimer);
      document.getElementById('az-loading').style.display = 'none';
      S.analysisResult = result;
      renderAnalysis(result);
    })
    .catch(function(e) {
      clearInterval(stepTimer);
      document.getElementById('az-loading').style.display = 'none';
      toast('Analysis failed: ' + e.message, 'err');
    });
}

function renderAnalysis(r) {
  document.getElementById('az-result').style.display = 'block';

  // App info
  var sizeStr = r.size > 1048576 ? (r.size/1048576).toFixed(1)+' MB' : (r.size/1024).toFixed(1)+' KB';
  document.getElementById('az-info').innerHTML =
    kv('File', esc(r.file)) +
    kv('Size', sizeStr) +
    kv('Platform', '<span class="tag ' + (r.platform==='ios'?'t-ios':'t-and') + '">' + r.platform + '</span>') +
    kv('NSC Pinning', r.hasNSC ? '<span style="color:var(--red)">&#9888; Detected</span>' : '<span style="color:var(--mint)">&#10003; None</span>') +
    kv('mTLS Client Cert', r.mTLS ? '<span style="color:var(--red)">&#9888; Found in APK</span>' : '<span style="color:var(--mint)">&#10003; Not detected</span>') +
    kv('Obfuscated', r.obfuscated ? '<span style="color:var(--amber)">&#9888; ProGuard/R8 likely</span>' : '<span style="color:var(--mint)">&#10003; Not detected</span>');

  // Detections
  var sevMap = {critical:'t-critical', high:'t-high', medium:'t-medium2', low:'t-low'};
  document.getElementById('az-dets').innerHTML = r.detections && r.detections.length
    ? r.detections.map(function(d) {
        return '<div class="det"><div class="det-ic">' + (d.severity==='critical'?'&#128308;':d.severity==='high'?'&#128992;':'&#129000;') + '</div>' +
          '<div><div class="det-tp"><span class="tag ' + (sevMap[d.severity]||'t-low') + '">' + esc(d.severity) + '</span> ' + esc(d.type) + '</div>' +
          '<div class="det-dt">' + esc(d.detail) + '</div></div></div>';
      }).join('')
    : '<div class="empty" style="padding:20px"><div style="font-family:var(--sans);font-size:14px;font-weight:700;color:var(--mint)">&#10003; No pinning detected</div><div style="font-size:12px;color:var(--txt3);margin-top:4px">App may use default trust or runtime-only pinning</div></div>';

  // Frameworks
  document.getElementById('az-fw').innerHTML = r.frameworks && r.frameworks.length
    ? '<div style="display:flex;flex-wrap:wrap;gap:6px">' + r.frameworks.map(function(f){ return '<span class="tag t-ssl">' + esc(f) + '</span>'; }).join('') + '</div>'
    : '<span style="color:var(--txt3);font-size:12px">No specific frameworks detected</span>';

  // Native libs
  document.getElementById('az-libs').innerHTML = r.nativeLibs && r.nativeLibs.length
    ? r.nativeLibs.map(function(l){ return '<code style="display:block;margin-bottom:3px;font-size:10px">' + esc(l) + '</code>'; }).join('')
    : '<span style="color:var(--txt3);font-size:12px">No native libs</span>';

  // Recommendations
  var recs = (r.recommendedScripts||[]).map(function(id){ return SCRIPTS.find(function(s){ return s.id===id; }); }).filter(Boolean);
  document.getElementById('az-rec').innerHTML = recs.length
    ? '<div class="ga">' + recs.map(scriptCard).join('') + '</div>'
    : '<span style="color:var(--txt3);font-size:12px">Universal bypass recommended for most apps</span>';
}

function applyRec() {
  var r = S.analysisResult;
  if (!r || !r.recommendedScripts) return;
  r.recommendedScripts.forEach(function(id){ S.selScripts.add(id); });
  renderBpGrid();
  go('bypass');
  toast('Applied ' + r.recommendedScripts.length + ' recommended scripts', 'ok');
}

function resetAnalyzer() {
  document.getElementById('az-result').style.display = 'none';
  S.analysisResult = null;
}

// ── Proxy ──────────────────────────────────────────────────────
function setProxy() {
  var serial = document.getElementById('prx-dev').value;
  var host = document.getElementById('prx-host').value;
  var port = document.getElementById('prx-port').value;
  if (!serial) { toast('Select a device', 'warn'); return; }
  api('/api/proxy/set', 'POST', {serial:serial, host:host, port:parseInt(port)}).then(function(d) {
    if (d && d.ok) {
      toast('Proxy set: ' + host + ':' + port, 'ok');
      document.getElementById('prx-status').innerHTML = '<span style="color:var(--mint)">&#10003; Active: ' + host + ':' + port + '</span>';
      document.getElementById('sb-prx').className = 'sb sb-ok';
      document.getElementById('sb-prx-t').textContent = 'Proxy :' + port;
    } else toast('Proxy set failed', 'err');
  });
}

function clearProxy() {
  var serial = document.getElementById('prx-dev').value;
  if (!serial) return;
  api('/api/proxy/clear', 'POST', {serial:serial}).then(function() {
    toast('Proxy cleared', 'ok');
    document.getElementById('prx-status').innerHTML = '';
    document.getElementById('sb-prx').className = 'sb sb-off';
    document.getElementById('sb-prx-t').textContent = 'Proxy Off';
  });
}

function blockQUIC() {
  var serial = document.getElementById('quic-dev').value;
  if (!serial) { toast('Select a device', 'warn'); return; }
  api('/api/proxy/blockquic', 'POST', {serial:serial}).then(function(d) {
    if (d && d.ok) {
      toast('QUIC blocked via iptables', 'ok');
      document.getElementById('quic-status').innerHTML = d.results.map(function(r) {
        return '<div style="font-size:11px;margin-top:3px">' + (r.ok?'&#10003;':'&#10007;') + ' ' + esc(r.cmd.slice(0,60)) + '</div>';
      }).join('');
    } else toast('Block QUIC failed', 'err');
  });
}

function fwdPort() {
  var serial = document.getElementById('fwd-dev').value;
  if (!serial) { toast('Select a device', 'warn'); return; }
  var local = parseInt(document.getElementById('fwd-local').value);
  var remote = parseInt(document.getElementById('fwd-remote').value);
  api('/api/adb/forward', 'POST', {serial:serial, localPort:local, remotePort:remote}).then(function(d) {
    var ok = d && d.ok;
    if (ok) toast('tcp:' + local + ' -> tcp:' + remote, 'ok');
    else toast('Forward failed', 'err');
    document.getElementById('fwd-status').innerHTML = '<span style="color:' + (ok?'var(--mint)':'var(--red)') + '">' + (ok?'&#10003; tcp:'+local+' -> tcp:'+remote : '&#10007; Failed: '+(d&&d.err?esc(d.err.slice(0,60)):'')) + '</span>';
  });
}

// ── Cert Injection ─────────────────────────────────────────────
function injectCert() {
  var serial = document.getElementById('cert-dev').value;
  var certPath = document.getElementById('cert-path').value.trim();
  var plat = document.getElementById('cert-plat').value;
  if (!serial) { toast('Select a device', 'warn'); return; }
  if (!certPath) { toast('Enter certificate path', 'warn'); return; }
  var stepsEl = document.getElementById('cert-steps');
  stepsEl.style.display = 'flex';
  stepsEl.innerHTML = stepItem('act', 'Injecting certificate...');
  api('/api/cert/inject', 'POST', {serial:serial, certPath:certPath, platform:plat}).then(function(d) {
    if (!d) { stepsEl.innerHTML = stepItem('err', 'Request failed'); return; }
    stepsEl.innerHTML = d.steps.map(function(s) {
      return stepItem(s.startsWith('&#10003;')||s.includes('OK')?'done':s.startsWith('&#10007;')?'err':'act', s);
    }).join('');
    if (d.ok) toast('Certificate injected!', 'ok'); else toast('Cert injection issues — check log', 'err');
  });
}

// ── Sessions ───────────────────────────────────────────────────
function loadSessions() {
  api('/api/sessions').then(function(data) {
    var el = document.getElementById('sessions-list');
    if (!data || !data.length) {
      el.innerHTML = '<div class="empty"><div class="empty-ic">&#128203;</div><div class="empty-tt">No sessions saved</div><div class="empty-sb">Run a bypass and click "Save Session"</div></div>';
      return;
    }
    el.innerHTML = data.map(function(s) {
      return '<div class="ssi">' +
        '<div class="ssi-ic">&#9889;</div>' +
        '<div style="flex:1;min-width:0">' +
          '<div class="ssi-nm">' + esc(s.name) + '</div>' +
          '<div class="ssi-mt">' + esc(s.target||'') + ' &middot; ' + new Date(s.savedAt).toLocaleString() + '</div>' +
          '<div style="font-size:10px;color:var(--txt3);margin-top:2px">' + ((s.logCount||0)) + ' log entries</div>' +
        '</div>' +
        '<div class="ssi-acts">' +
          '<button class="btn btn-ghost btn-xs" onclick="viewSessionLog(\\x27' + esc(s.id) + '\\x27)">&#128203; View</button>' +
          '<button class="btn btn-ghost btn-xs" onclick="exportSess(' + "'" + esc(JSON.stringify(s)) + "'" + ')">&#8595; Export</button>' +
        '</div>' +
      '</div>';
    }).join('');
  });
}

function viewSessionLog(id) {
  api('/api/bypass/logs/' + id).then(function(logs) {
    go('bypass');
    document.getElementById('bp-log').innerHTML = '';
    S.logLineCount = 0;
    (logs||[]).forEach(function(l){ bpLog(l.level, l.msg, l.ts); });
  });
}

function exportSess(jsonStr) {
  var blob = new Blob([decodeURIComponent(escape(atob(btoa(jsonStr))))], {type:'application/json'});
  var a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'ghostpin-session.json';
  a.click();
}

// ── Tool Check ─────────────────────────────────────────────────
var TOOL_META = {
  adb:{ic:'&#129302;',d:'Android Debug Bridge'},
  frida:{ic:'&#128300;',d:'Dynamic instrumentation toolkit'},
  'frida-ps':{ic:'&#128300;',d:'Frida process lister'},
  'frida-trace':{ic:'&#128300;',d:'Frida function tracer'},
  objection:{ic:'&#127919;',d:'Runtime mobile explorer'},
  apktool:{ic:'&#128230;',d:'APK decompiler / rebuilder'},
  jadx:{ic:'&#9749;',d:'DEX to Java decompiler'},
  openssl:{ic:'&#128272;',d:'SSL/TLS certificate toolkit'},
  mitmproxy:{ic:'&#127760;',d:'Interactive HTTPS proxy'},
  mitmweb:{ic:'&#127760;',d:'mitmproxy web UI'},
  ideviceinfo:{ic:'&#127822;',d:'iOS device info (libimobiledevice)'},
  'ios-deploy':{ic:'&#127822;',d:'iOS app deployer'},
  'apk-mitm':{ic:'&#128296;',d:'APK patcher for MITM'},
  keytool:{ic:'&#128273;',d:'Java key/cert manager'},
  xz:{ic:'&#128476;',d:'XZ compression (frida-server)'}
};

function runToolCheck() {
  var grid = document.getElementById('tool-grid');
  grid.innerHTML = '<div class="empty"><div class="spin" style="width:24px;height:24px;border-width:2px;margin:0 auto 12px"></div><div class="empty-tt">Scanning tools...</div></div>';
  api('/api/tools').then(function(data) {
    if (!data) return;
    S.toolStatus = data;
    var ready = Object.values(data).filter(function(t){ return t.found; }).length;
    var total = Object.keys(data).length;
    document.getElementById('ds-tools').textContent = ready + '/' + total;
    grid.innerHTML = Object.entries(data).map(function(entry) {
      var name = entry[0], t = entry[1];
      var meta = TOOL_META[name] || {ic:'&#128295;',d:name};
      return '<div class="tool-i">' +
        '<span style="font-size:20px;flex-shrink:0">' + meta.ic + '</span>' +
        '<div style="flex:1;min-width:0"><div class="ti-nm">' + esc(name) + '</div>' +
        '<div class="ti-pt">' + (t.found ? esc(t.path||meta.d) : esc(meta.d)) + '</div>' +
        (t.version ? '<div style="font-size:10px;color:var(--txt3);margin-top:1px">' + esc(t.version.slice(0,60)) + '</div>' : '') +
        '</div>' +
        '<span style="font-size:14px;font-weight:700;flex-shrink:0;color:' + (t.found?'var(--mint)':'var(--red)') + '">' + (t.found?'&#10003;':'&#10007;') + '</span>' +
      '</div>';
    }).join('');
  });
}

// ── Settings ───────────────────────────────────────────────────
function saveSettings() {
  S.settings.fridaPort = parseInt(document.getElementById('cfg-fport').value)||27042;
  S.settings.pollInterval = parseInt(document.getElementById('cfg-poll').value)||5;
  S.settings.logLevel = document.getElementById('cfg-loglevel').value;
  S.settings.maxLog = parseInt(document.getElementById('cfg-maxlog').value)||2000;
  try { localStorage.setItem('ghostpin-cfg', JSON.stringify(S.settings)); } catch(e){}
  restartPoll();
  toast('Settings saved', 'ok');
}

function loadSettings() {
  try {
    var s = JSON.parse(localStorage.getItem('ghostpin-cfg')||'{}');
    Object.assign(S.settings, s);
  } catch(e){}
  try {
    document.getElementById('cfg-fport').value = S.settings.fridaPort;
    document.getElementById('cfg-poll').value = S.settings.pollInterval;
    document.getElementById('cfg-loglevel').value = S.settings.logLevel;
    document.getElementById('cfg-maxlog').value = S.settings.maxLog;
  } catch(e){}
}

// ── Polling ────────────────────────────────────────────────────
function restartPoll() {
  if (S.pollTimer) clearInterval(S.pollTimer);
  S.pollTimer = setInterval(refreshDevices, (S.settings.pollInterval||5)*1000);
}

function refreshAll() {
  refreshDevices();
  runToolCheck();
}

// ── Utility ────────────────────────────────────────────────────
function esc(s) {
  if (s == null) return '';
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

// ── Init ───────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function() {
  loadSettings();
  renderBpGrid();
  renderLib();
  populateEditorSel();
  refreshDevices();
  runToolCheck();
  restartPoll();
  go('dashboard');
});


// ── Page title map additions ───────────────────────────────────
PAGE_TITLES['scanner'] = 'Vulnerability Scanner';
PAGE_TITLES['monitor'] = 'API Monitor';
PAGE_TITLES['fuzzer']  = 'Intent Fuzzer';
PAGE_TITLES['tracer']  = 'Class Tracer';
PAGE_TITLES['mdm']     = 'MDM Profiler';
PAGE_TITLES['reports'] = 'Reports';

// ── Monitor state ──────────────────────────────────────────────
var MON = { sessionId: null, sse: null, cryptoCnt: 0, fileCnt: 0, netCnt: 0, allLines: [] };

function startMonitor() {
  var serial = document.getElementById('mon-dev').value;
  var target = document.getElementById('mon-target').value.trim();
  if (!serial) { toast('Select a device', 'warn'); return; }
  if (!target) { toast('Enter target package or PID', 'warn'); return; }
  var cats = [];
  if (document.getElementById('mon-crypto').checked) cats.push('crypto');
  if (document.getElementById('mon-file').checked) cats.push('file');
  if (document.getElementById('mon-network').checked) cats.push('network');
  MON.cryptoCnt = 0; MON.fileCnt = 0; MON.netCnt = 0; MON.allLines = [];
  document.getElementById('mon-crypto-cnt').textContent = '0';
  document.getElementById('mon-file-cnt').textContent = '0';
  document.getElementById('mon-net-cnt').textContent = '0';
  document.getElementById('mon-log').innerHTML = '';
  var spawnMode = document.getElementById('mon-mode').value === 'spawn';
  api('/api/monitor/start', 'POST', {serial:serial, target:target, categories:cats, spawnMode:spawnMode}).then(function(d) {
    if (!d || !d.sessionId) { toast('Failed to start monitor', 'err'); return; }
    MON.sessionId = d.sessionId;
    toast('API Monitor started!', 'ok');
    document.getElementById('mon-start-btn').style.display = 'none';
    document.getElementById('mon-stop-btn').style.display = 'inline-flex';
    document.getElementById('mon-live-ind').style.display = 'flex';
    if (MON.sse) MON.sse.close();
    var sse = new EventSource('/api/monitor/stream/' + d.sessionId);
    MON.sse = sse;
    sse.onmessage = function(e) {
      try {
        var entry = JSON.parse(e.data);
        var msg = entry.msg || '';
        MON.allLines.push(entry);
        if (msg.includes('Crypto')) { MON.cryptoCnt++; document.getElementById('mon-crypto-cnt').textContent = MON.cryptoCnt; }
        if (msg.includes('File')) { MON.fileCnt++; document.getElementById('mon-file-cnt').textContent = MON.fileCnt; }
        if (msg.includes('Net')) { MON.netCnt++; document.getElementById('mon-net-cnt').textContent = MON.netCnt; }
        var filter = document.getElementById('mon-filter').value.toLowerCase();
        if (!filter || msg.toLowerCase().includes(filter)) appendMonLog(entry);
        document.getElementById('mon-log-count').textContent = MON.allLines.length + ' calls';
      } catch(err) {}
    };
    sse.onerror = function() { document.getElementById('mon-live-ind').style.display = 'none'; };
  });
}

function stopMonitor() {
  if (MON.sse) { MON.sse.close(); MON.sse = null; }
  if (MON.sessionId) api('/api/monitor/stop', 'POST', {sessionId: MON.sessionId});
  document.getElementById('mon-start-btn').style.display = 'inline-flex';
  document.getElementById('mon-stop-btn').style.display = 'none';
  document.getElementById('mon-live-ind').style.display = 'none';
  toast('Monitor stopped', 'warn');
}

function appendMonLog(entry) {
  var el = document.getElementById('mon-log');
  var color = entry.msg.includes('Crypto') ? 'var(--violet)' :
              entry.msg.includes('File')   ? 'var(--amber)'  :
              entry.msg.includes('Net')    ? 'var(--cyan)'   : 'var(--txt2)';
  var div = document.createElement('div');
  div.className = 'll';
  div.innerHTML = '<span class="lts">' + new Date().toTimeString().slice(0,8) + '</span>' +
                  '<span class="lm" style="color:' + color + '">' + esc(entry.msg) + '</span>';
  el.appendChild(div);
  if (el.children.length > 2000) el.removeChild(el.firstChild);
  el.scrollTop = el.scrollHeight;
}

function filterMonLog() {
  var filter = document.getElementById('mon-filter').value.toLowerCase();
  document.getElementById('mon-log').innerHTML = '';
  MON.allLines.filter(function(e) { return !filter || e.msg.toLowerCase().includes(filter); })
    .forEach(appendMonLog);
}

function clearMonLog() {
  document.getElementById('mon-log').innerHTML = '';
  MON.allLines = []; MON.cryptoCnt = 0; MON.fileCnt = 0; MON.netCnt = 0;
  document.getElementById('mon-crypto-cnt').textContent = '0';
  document.getElementById('mon-file-cnt').textContent = '0';
  document.getElementById('mon-net-cnt').textContent = '0';
  document.getElementById('mon-log-count').textContent = '0 calls';
}

// ── Vuln Scanner ───────────────────────────────────────────────
var SCAN_RESULT = null;

function handleScanDrop(e) {
  e.preventDefault();
  document.getElementById('scan-drop-zone').style.borderColor = 'var(--rim2)';
  var f = e.dataTransfer.files[0];
  if (f) runVulnScan(f);
}

function runVulnScan(f) {
  if (!f) return;
  document.getElementById('scan-loading').style.display = 'block';
  document.getElementById('scan-result').style.display = 'none';
  var fd = new FormData(); fd.append('file', f);
  fetch('/api/scan/apk', {method:'POST', body:fd})
    .then(function(r){ return r.json(); })
    .then(function(result) {
      document.getElementById('scan-loading').style.display = 'none';
      SCAN_RESULT = result;
      renderScanResult(result);
    }).catch(function(err) {
      document.getElementById('scan-loading').style.display = 'none';
      toast('Scan failed: ' + err.message, 'err');
    });
}

function renderScanResult(r) {
  document.getElementById('scan-result').style.display = 'block';
  var s = r.summary || {};
  var sevColor = {'critical':'var(--red)','high':'var(--amber)','medium':'var(--cyan)','low':'var(--txt2)'};
  document.getElementById('scan-stats').innerHTML =
    statCard(s.critical||0, 'Critical', 'var(--red)') +
    statCard(s.high||0, 'High', 'var(--amber)') +
    statCard(s.medium||0, 'Medium', 'var(--cyan)') +
    statCard(s.low||0, 'Low', 'var(--txt2)');
  var grade = r.grade || 'N/A'; var score = r.score || 0;
  var gradeColor = grade==='A'?'var(--mint)':grade==='B'?'var(--cyan)':grade==='C'?'var(--amber)':'var(--red)';
  var html = '<div class="card mb12"><div class="ch"><div class="ct">Security Grade</div></div><div class="cb" style="text-align:center">' +
    '<div style="font-size:64px;font-weight:800;color:' + gradeColor + '">' + grade + '</div>' +
    '<div style="font-size:14px;color:var(--txt2)">Score: ' + score + '/100 · ' + (r.findings||[]).length + ' findings</div></div></div>';
  html += (r.findings||[]).map(function(f) {
    var sev = f.severity||'low';
    var bc = sevColor[sev]||'var(--txt3)';
    return '<div style="background:var(--ink2);border:1px solid var(--rim);border-left:4px solid ' + bc + ';border-radius:8px;padding:12px 14px;margin-bottom:8px">' +
      '<div style="display:flex;align-items:center;gap:8px;margin-bottom:4px">' +
      '<span class="tag t-' + (sev==='critical'?'critical':sev==='high'?'high':sev==='medium'?'medium2':'low') + '">' + sev + '</span>' +
      '<span style="font-weight:700;font-size:13px">' + esc(f.type||'') + '</span></div>' +
      '<div style="font-size:11px;color:var(--txt3);font-family:var(--mono)">' + esc(f.location||'') + '</div>' +
      '<div style="font-size:12px;color:var(--txt2);margin-top:3px">' + esc(f.detail||'') + '</div>' +
      ((f.evidence||[]).length ? '<div style="font-family:var(--mono);font-size:10px;background:#050810;color:var(--lime);padding:5px 8px;border-radius:4px;margin-top:5px;word-break:break-all">' + esc((f.evidence[0]||'').substring(0,120)) + '</div>' : '') +
      '</div>';
  }).join('');
  if (!r.findings || !r.findings.length) html += '<div class="empty"><div class="empty-ic">✅</div><div class="empty-tt" style="color:var(--mint)">No vulnerabilities detected</div></div>';
  document.getElementById('scan-findings').innerHTML = html;
}

function statCard(num, label, color) {
  return '<div class="sc"><div class="sc-acc" style="background:' + color + '"></div>' +
    '<div class="sc-num" style="color:' + color + '">' + num + '</div>' +
    '<div class="sc-lbl">' + label + '</div></div>';
}

function resetScan() {
  SCAN_RESULT = null;
  document.getElementById('scan-result').style.display = 'none';
}

function generateReportFromScan() {
  if (!SCAN_RESULT) { toast('No scan data', 'warn'); return; }
  var app_name = prompt('App name for report:', SCAN_RESULT.file || 'Scanned App');
  if (!app_name) return;
  api('/api/report/generate', 'POST', {
    appName: app_name, platform: SCAN_RESULT.platform || 'android',
    vulnFindings: SCAN_RESULT.findings || [], analysis: SCAN_RESULT
  }).then(function(d) {
    if (d && d.ok) { toast('Report generated!', 'ok'); go('reports'); loadReports(); }
    else toast('Report failed', 'err');
  });
}

// ── Intent Fuzzer ──────────────────────────────────────────────
var FZ = { fuzzId: null, pollTimer: null };

function enumComponents() {
  var serial = document.getElementById('fz-dev').value;
  var pkg = document.getElementById('fz-pkg').value.trim();
  if (!serial || !pkg) { toast('Select device and enter package', 'warn'); return; }
  toast('Enumerating components...', 'ok');
  api('/api/intent/components?serial=' + encodeURIComponent(serial) + '&package=' + encodeURIComponent(pkg))
    .then(function(data) {
      if (!data) { toast('Failed to enumerate', 'err'); return; }
      var sel = document.getElementById('fz-comp');
      var opts = [];
      (data.activities||[]).forEach(function(a){ opts.push({v:a,t:'[Activity] '+a}); });
      (data.services||[]).forEach(function(s){ opts.push({v:s,t:'[Service] '+s}); });
      (data.receivers||[]).forEach(function(r){ opts.push({v:r,t:'[Receiver] '+r}); });
      if (!opts.length) { toast('No exported components found', 'warn'); return; }
      sel.innerHTML = opts.map(function(o){ return '<option value="'+esc(o.v)+'">'+esc(o.t)+'</option>'; }).join('');
      document.getElementById('fz-comp-list').style.display = 'block';
      toast(opts.length + ' components found', 'ok');
    });
}

function startFuzz() {
  var serial = document.getElementById('fz-dev').value;
  var pkg = document.getElementById('fz-pkg').value.trim();
  var comp = document.getElementById('fz-comp').value;
  var type = document.getElementById('fz-type').value;
  if (!serial || !pkg || !comp) { toast('Configure all fields first', 'warn'); return; }
  var cats = [];
  if (document.getElementById('fz-sqli').checked) cats.push('sqli');
  if (document.getElementById('fz-trav').checked) cats.push('traversal');
  if (document.getElementById('fz-uri').checked) cats.push('uri_schemes');
  if (document.getElementById('fz-overflow').checked) cats.push('overflow');
  if (document.getElementById('fz-xss').checked) cats.push('xss');
  document.getElementById('fz-results').innerHTML = '<div style="padding:14px;font-size:12px;color:var(--txt3)"><span class="spin"></span> Fuzzing in progress...</div>';
  api('/api/intent/fuzz', 'POST', {serial:serial, package:pkg, component:comp, type:type, categories:cats}).then(function(d) {
    if (!d || !d.fuzzId) { toast('Fuzz failed', 'err'); return; }
    FZ.fuzzId = d.fuzzId;
    toast('Fuzzing started!', 'ok');
    FZ.pollTimer = setInterval(function() { pollFuzzResults(d.fuzzId); }, 2000);
    setTimeout(function() { if (FZ.pollTimer) { clearInterval(FZ.pollTimer); FZ.pollTimer = null; } }, 60000);
  });
}

function pollFuzzResults(fuzzId) {
  api('/api/intent/results/' + fuzzId).then(function(results) {
    if (!results || !results.length) return;
    clearInterval(FZ.pollTimer); FZ.pollTimer = null;
    renderFuzzResults(results);
  });
}

function renderFuzzResults(results) {
  var interesting = results.filter(function(r){ return r.interesting; });
  var html = '<div style="font-size:12px;color:var(--txt3);margin-bottom:10px">' +
    results.length + ' attempts · <span style="color:var(--amber)">' + interesting.length + ' interesting</span></div>';
  html += results.map(function(r) {
    var bc = r.interesting ? 'var(--amber)' : 'var(--rim)';
    return '<div style="background:var(--ink2);border:1px solid '+bc+';border-radius:6px;padding:8px 12px;margin-bottom:6px;font-size:11px">' +
      (r.interesting ? '<span style="color:var(--amber);font-weight:700">⚠ INTERESTING</span> ' : '') +
      '<code>' + esc((r.cmd||'').substring(0,80)) + '</code>' +
      (r.stdout ? '<div style="color:var(--txt3);margin-top:3px">' + esc(r.stdout.substring(0,100)) + '</div>' : '') +
      '</div>';
  }).join('');
  document.getElementById('fz-results').innerHTML = html;
  if (interesting.length > 0) toast(interesting.length + ' interesting responses!', 'warn');
}

// ── Class Tracer ───────────────────────────────────────────────
var TR = { sessionId: null, sse: null, count: 0 };

function updateTracerMode() {
  var mode = document.getElementById('tr-trace-mode').value;
  var lbl = document.querySelector('#tr-filter').previousElementSibling;
  var inp = document.getElementById('tr-filter');
  if (mode === 'dump') { lbl.textContent = 'Class Filter (substring match)'; inp.placeholder = 'ssl, pin, trust, auth'; }
  else { lbl.textContent = 'Target Class (full name)'; inp.placeholder = 'okhttp3.CertificatePinner'; }
}

function startTrace() {
  var serial = document.getElementById('tr-dev').value;
  var target = document.getElementById('tr-target').value.trim();
  var mode = document.getElementById('tr-trace-mode').value;
  var filter = document.getElementById('tr-filter').value.trim();
  var platform = document.getElementById('tr-platform').value;
  var spawnMode = document.getElementById('tr-mode').value === 'spawn';
  if (!serial || !target) { toast('Select device and enter target', 'warn'); return; }
  document.getElementById('tr-log').innerHTML = '';
  TR.count = 0; document.getElementById('tr-count').textContent = '0 entries';
  var payload = {serial:serial, target:target, spawnMode:spawnMode, platform:platform};
  if (mode === 'dump') payload.classFilter = filter;
  else payload.traceClass = filter;
  api('/api/trace/start', 'POST', payload).then(function(d) {
    if (!d || !d.sessionId) { toast('Failed to start tracer', 'err'); return; }
    TR.sessionId = d.sessionId;
    toast('Class tracer started!', 'ok');
    if (TR.sse) TR.sse.close();
    var sse = new EventSource('/api/trace/stream/' + d.sessionId);
    TR.sse = sse;
    sse.onmessage = function(e) {
      try {
        var entry = JSON.parse(e.data);
        var el = document.getElementById('tr-log');
        var div = document.createElement('div');
        div.className = 'll';
        div.innerHTML = '<span class="lts">'+new Date().toTimeString().slice(0,8)+'</span>' +
          '<span class="lm" style="color:' + (entry.msg.includes('CLASS:')?'var(--lime)':'var(--txt2)') + '">' + esc(entry.msg) + '</span>';
        el.appendChild(div); el.scrollTop = el.scrollHeight;
        TR.count++; document.getElementById('tr-count').textContent = TR.count + ' entries';
        if (el.children.length > 3000) el.removeChild(el.firstChild);
      } catch(err) {}
    };
  });
}

function clearTraceLog() {
  document.getElementById('tr-log').innerHTML = '';
  TR.count = 0; document.getElementById('tr-count').textContent = '0 entries';
}

// ── MDM Profiler ───────────────────────────────────────────────
function runMdmProfile() {
  var serial = document.getElementById('mdm-dev').value;
  if (!serial) { toast('Select a device', 'warn'); return; }
  toast('Profiling MDM...', 'ok');
  api('/api/mdm/profile?serial=' + encodeURIComponent(serial)).then(function(d) {
    if (!d) { toast('MDM profile failed', 'err'); return; }
    var riskColor = d.risk_level==='high'?'var(--red)':d.risk_level==='medium'?'var(--amber)':'var(--mint)';
    var html = '<div class="div" style="margin:10px 0"></div>' +
      kv('MDM Detected', d.mdm_detected ? '<span style="color:var(--red)">⚠ YES</span>' : '<span style="color:var(--mint)">✓ None</span>') +
      kv('Risk Level', '<span style="color:'+riskColor+';font-weight:700">' + (d.risk_level||'none').toUpperCase() + '</span>') +
      kv('Work Profile', d.work_profile ? '⚠ Yes (Android Enterprise)' : '✓ No') +
      kv('Knox', d.knox_enabled ? '⚠ Samsung Knox active' : '✓ Not detected') +
      kv('MDM Vendors', (d.vendors||[]).join(', ') || 'None detected') +
      kv('Device Admins', (d.device_admins||[]).join(', ') || 'None') +
      (d.notes||[]).map(function(n){ return '<div style="font-size:11px;color:var(--txt3);margin-top:4px">• '+esc(n)+'</div>'; }).join('');
    if (d.mdm_detected) {
      html += '<div style="margin-top:12px"><button class="btn btn-lime btn-sm" onclick="injectMdmBypass()">🛡 Inject MDM Bypass Script</button></div>';
    }
    document.getElementById('mdm-result').innerHTML = html;
    document.getElementById('mdm-result').style.display = 'block';
    toast(d.mdm_detected ? 'MDM detected!' : 'No MDM found', d.mdm_detected ? 'warn' : 'ok');
  });
}

function injectMdmBypass() {
  document.getElementById('custom-script').value = '// MDM Policy Bypass hooks — auto-injected from MDM Profiler\\nsend("[GhostPin:MDM] Policy hooks active");';
  go('bypass');
  toast('MDM bypass script loaded into Bypass', 'ok');
}

// ── Reports ────────────────────────────────────────────────────
function loadReports() {
  api('/api/report/list').then(function(data) {
    var el = document.getElementById('rep-list');
    if (!data || !data.length) {
      el.innerHTML = '<div class="empty" style="padding:30px"><div class="empty-ic">📊</div><div class="empty-tt">No reports yet</div></div>';
      return;
    }
    el.innerHTML = data.map(function(r) {
      return '<div class="ssi">' +
        '<div class="ssi-ic">📊</div>' +
        '<div style="flex:1;min-width:0"><div class="ssi-nm">' + esc(r.name) + '</div>' +
        '<div class="ssi-mt">' + new Date(r.created).toLocaleString() + ' · ' + (r.size/1024).toFixed(1) + ' KB</div></div>' +
        '<div class="ssi-acts">' +
        '<a class="btn btn-lime btn-xs" href="/api/report/' + esc(r.id) + '" target="_blank">👁 View</a>' +
        '<a class="btn btn-ghost btn-xs" href="/api/report/' + esc(r.id) + '" download>⬇ Save</a>' +
        '</div></div>';
    }).join('');
  });
}

function generateReport() {
  var app = document.getElementById('rep-app').value.trim();
  var plat = document.getElementById('rep-plat').value;
  var tester = document.getElementById('rep-tester').value.trim();
  var sessId = document.getElementById('rep-sess').value.trim();
  if (!app) { toast('Enter app name', 'warn'); return; }
  document.getElementById('rep-status').textContent = 'Generating...';
  api('/api/report/generate', 'POST', {
    appName: app, platform: plat, tester: tester || 'GhostPin',
    sessionId: sessId, vulnFindings: SCAN_RESULT ? SCAN_RESULT.findings||[] : [],
    analysis: SCAN_RESULT || {}
  }).then(function(d) {
    if (d && d.ok) {
      document.getElementById('rep-status').innerHTML = '<span style="color:var(--mint)">✓ Report generated!</span>';
      toast('Report ready!', 'ok'); loadReports();
    } else {
      document.getElementById('rep-status').innerHTML = '<span style="color:var(--red)">✗ Failed</span>';
      toast('Report generation failed', 'err');
    }
  });
}

// Populate new device selects when devices refresh
var _origRenderDeviceUI = renderDeviceUI;
renderDeviceUI = function(devs) {
  _origRenderDeviceUI(devs);
  var selHtml = devs.length === 0
    ? '<option value="">-- No devices --</option>'
    : devs.map(function(d){ return '<option value="'+esc(d.serial)+'">'+esc((d.manufacturer||'')+' '+(d.model||d.serial)+'('+d.serial+')')+'</option>'; }).join('');
  ['mon-dev','fz-dev','tr-dev','mdm-dev'].forEach(function(id){
    var el = document.getElementById(id);
    if (el) el.innerHTML = selHtml;
  });
};

// Extend go() to handle new pages
var _origGo = go;
go = function(id) {
  _origGo(id);
  if (id === 'reports') loadReports();
};


// ── Phase 2: PAGE TITLES ─────────────────────────────────────
PAGE_TITLES['cve']        = 'CVE Checker';
PAGE_TITLES['diff']       = 'APK Diff';
PAGE_TITLES['traffic']    = 'Traffic Replay';
PAGE_TITLES['checklist']  = 'Guided Checklist';
PAGE_TITLES['workspaces'] = 'Workspaces';

// ── Phase 2: CVE Checker ──────────────────────────────────────
function handleCveDrop(e) {
  e.preventDefault();
  document.getElementById('cve-drop-zone').style.borderColor='var(--rim2)';
  runCveCheck(e.dataTransfer.files[0]);
}
function runCveCheck(f) {
  if (!f) return;
  document.getElementById('cve-loading').style.display='block';
  document.getElementById('cve-result').style.display='none';
  var fd = new FormData(); fd.append('file', f);
  fetch('/api/cve/check', {method:'POST',body:fd})
    .then(function(r){ return r.json(); })
    .then(function(d) {
      document.getElementById('cve-loading').style.display='none';
      renderCveResult(d);
    }).catch(function(e){ document.getElementById('cve-loading').style.display='none'; toast('CVE check failed','err'); });
}
function renderCveResult(d) {
  var el = document.getElementById('cve-result');
  el.style.display='block';
  var html = '<div class="card mb12"><div class="ch"><div class="ct">Detected Libraries (' + (d.scanned||0) + ')</div></div><div class="cb">';
  (d.libraries||[]).forEach(function(lib) {
    html += '<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;font-size:12px">' +
      '<span style="color:var(--lime);font-weight:700">'+esc(lib.library)+'</span>' +
      '<span style="color:var(--txt3)">'+esc(lib.version)+'</span>' +
      '<span style="color:var(--txt4);font-size:10px">'+esc(lib.package)+'</span></div>';
  });
  html += '</div></div>';
  if (d.vulnerabilities && d.vulnerabilities.length) {
    html += '<div class="card"><div class="ch"><div class="ct">⚠ Vulnerabilities Found (' + d.vulnerabilities.length + ')</div></div><div class="cb0">';
    d.vulnerabilities.forEach(function(v) {
      var sev = v.severity||'UNKNOWN';
      var col = sev==='CRITICAL'?'var(--red)':sev==='HIGH'?'var(--amber)':sev==='MEDIUM'?'var(--cyan)':'var(--txt3)';
      html += '<div style="border-left:4px solid '+col+';background:var(--ink2);padding:10px 14px;margin-bottom:6px">' +
        '<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap">' +
        '<span style="color:'+col+';font-weight:800;font-size:12px">'+esc(sev)+'</span>' +
        '<span style="font-weight:700;font-size:12px">'+esc(v.cve||'')+'</span>' +
        '<span style="font-size:11px;color:var(--lime)">'+esc(v.library+' '+v.version)+'</span></div>' +
        '<div style="font-size:11px;color:var(--txt2);margin-top:3px">'+esc(v.summary||'')+'</div>' +
        (v.fix_version?'<div style="font-size:10px;color:var(--mint);margin-top:2px">Fix: '+esc(v.fix_version)+'</div>':'') +
        '</div>';
    });
    html += '</div></div>';
  } else {
    html += '<div class="empty" style="padding:30px"><div class="empty-ic">✅</div><div class="empty-tt" style="color:var(--mint)">No known CVEs detected</div></div>';
  }
  el.innerHTML = html;
}

// ── Phase 2: APK Diff ──────────────────────────────────────────
var DIFF_FILES = {a:null, b:null};
function setDiffFile(side, f) {
  DIFF_FILES[side] = f;
  var lbl = document.getElementById('diff-label-'+side);
  var zone = document.getElementById('diff-drop-'+side);
  lbl.textContent = f.name;
  zone.style.borderColor = 'var(--lime)';
}
function runApkDiff() {
  if (!DIFF_FILES.a || !DIFF_FILES.b) { toast('Select both APK files', 'warn'); return; }
  document.getElementById('diff-loading').style.display='block';
  document.getElementById('diff-result').style.display='none';
  var fd = new FormData(); fd.append('file_a', DIFF_FILES.a); fd.append('file_b', DIFF_FILES.b);
  fetch('/api/diff/apk',{method:'POST',body:fd})
    .then(function(r){ return r.json(); })
    .then(function(d) {
      document.getElementById('diff-loading').style.display='none';
      renderDiffResult(d);
    }).catch(function(e){ document.getElementById('diff-loading').style.display='none'; toast('Diff failed','err'); });
}
function renderDiffResult(d) {
  var el = document.getElementById('diff-result'); el.style.display='block';
  var flags = d.security_flags||[];
  var html = '<div class="card mb12"><div class="ch"><div class="ct">Security Changes: '+flags.length+'</div></div><div class="cb">';
  if (!flags.length) html += '<div style="color:var(--mint);font-size:13px">✓ No security regressions detected</div>';
  flags.forEach(function(f) {
    var col = f.severity==='critical'?'var(--red)':f.severity==='high'?'var(--amber)':'var(--cyan)';
    html += '<div style="border-left:4px solid '+col+';background:var(--ink2);padding:8px 12px;margin-bottom:6px;font-size:12px">' +
      '<span style="color:'+col+';font-weight:800;text-transform:uppercase">'+esc(f.severity)+'</span> ' +
      esc(f.change) + '</div>';
  });
  html += '</div></div>';
  function diffSection(title, diff) {
    if (!diff.added.length && !diff.removed.length) return '';
    var h = '<div class="card mb8"><div class="ch"><div class="ct">'+title+'</div></div><div class="cb" style="font-size:11px;font-family:var(--mono)">';
    diff.added.forEach(function(p){ h+='<div style="color:var(--mint)">+ '+esc(p)+'</div>'; });
    diff.removed.forEach(function(p){ h+='<div style="color:var(--red)">- '+esc(p)+'</div>'; });
    return h + '</div></div>';
  }
  html += diffSection('Permission Changes', d.permissions||{added:[],removed:[]});
  html += diffSection('NSC Pin Changes', d.nsc_pins||{added:[],removed:[]});
  html += diffSection('Native Library Changes', d.native_libs||{added:[],removed:[]});
  html += diffSection('Framework Changes', d.frameworks||{added:[],removed:[]});
  el.innerHTML = html;
}

// ── Phase 2: Traffic Replay ────────────────────────────────────
var TR_SESSION = null; var TR_CURRENT_FLOW = null;
function startTrafficCapture() {
  var port = parseInt(document.getElementById('tr-port').value)||8877;
  api('/api/traffic/start', 'POST', {port:port}).then(function(d) {
    if (!d || !d.ok) { toast(d.error||'Failed to start mitmproxy','err'); return; }
    TR_SESSION = d.session_id;
    document.getElementById('tr-start-btn').style.display='none';
    document.getElementById('tr-stop-btn').style.display='inline-flex';
    document.getElementById('tr-status').innerHTML='<span style="color:var(--mint)">Listening on port '+port+'</span>';
    toast('Traffic capture started!','ok');
  });
}
function stopTrafficCapture() {
  if (!TR_SESSION) return;
  api('/api/traffic/stop','POST',{sessionId:TR_SESSION}).then(function(){
    document.getElementById('tr-start-btn').style.display='inline-flex';
    document.getElementById('tr-stop-btn').style.display='none';
    document.getElementById('tr-status').textContent='Stopped';
    toast('Capture stopped','warn');
  });
}
function loadTrafficFlows() {
  if (!TR_SESSION) { toast('Start a capture session first','warn'); return; }
  api('/api/traffic/flows/'+TR_SESSION).then(function(flows) {
    var el = document.getElementById('tr-flow-list');
    if (!flows || !flows.length) { el.innerHTML='<div class="empty" style="padding:20px"><div class="empty-ic">🌐</div><div class="empty-tt">No flows yet</div></div>'; return; }
    document.getElementById('tr-flow-cnt').textContent = flows.length;
    document.getElementById('tr-err-cnt').textContent = flows.filter(function(f){ return f.status>=400; }).length;
    document.getElementById('tr-https-cnt').textContent = flows.filter(function(f){ return (f.host||'').includes('https')||f.port===443; }).length;
    el.innerHTML = flows.map(function(f,i) {
      var scol = f.status<300?'var(--mint)':f.status<400?'var(--amber)':'var(--red)';
      return '<div class="ssi" style="cursor:pointer" onclick="showFlowDetail('+i+')">' +
        '<span style="font-weight:700;color:var(--cyan);min-width:48px;font-size:11px">'+esc(f.method||'')+'</span>' +
        '<span style="flex:1;font-size:11px;color:var(--txt2);overflow:hidden;text-overflow:ellipsis;white-space:nowrap">'+esc((f.host||'')+(f.path||''))+'</span>' +
        '<span style="color:'+scol+';font-size:11px;font-weight:700">'+(f.status||'-')+'</span>' +
        '</div>';
    }).join('');
  });
}
function showFlowDetail(flowId) {
  if (!TR_SESSION) return;
  TR_CURRENT_FLOW = flowId;
  api('/api/traffic/flow/'+TR_SESSION+'/'+flowId).then(function(d) {
    document.getElementById('tr-detail-panel').style.display='block';
    document.getElementById('tr-detail-title').textContent='Flow #'+flowId+' — '+(d.request&&d.request.method||'')+' '+(d.request&&d.request.url||'');
    document.getElementById('tr-req-body').textContent = d.request ? JSON.stringify(d.request,null,2) : 'N/A';
    document.getElementById('tr-resp-body').textContent = d.response ? JSON.stringify(d.response,null,2) : 'N/A';
    document.getElementById('tr-replay-body').value = '';
  });
}
function replayCurrentFlow() {
  if (!TR_SESSION || TR_CURRENT_FLOW===null) return;
  var body = document.getElementById('tr-replay-body').value.trim();
  var mods = body ? {body:body} : {};
  api('/api/traffic/replay','POST',{sessionId:TR_SESSION,flowId:TR_CURRENT_FLOW,modifications:mods}).then(function(d) {
    if (d && d.ok) {
      document.getElementById('tr-resp-body').textContent = `REPLAY RESPONSE:
Status: ${d.status}

${JSON.stringify(d.headers,null,2)}

${d.body}`;
      toast('Replayed! Status: '+d.status, d.status<400?'ok':'warn');
    } else toast('Replay failed: '+(d&&d.error||'unknown'),'err');
  });
}

// ── Phase 2: Guided Checklist ──────────────────────────────────
var CL_DONE = {};
function loadChecklistTypes() {
  api('/api/checklist/all').then(function(d) {
    var el = document.getElementById('checklist-types');
    if (!d) return;
    el.innerHTML = Object.keys(d).map(function(k) {
      var cl = d[k];
      var riskCol = cl.risk==='CRITICAL'?'var(--red)':cl.risk==='HIGH'?'var(--amber)':'var(--cyan)';
      var clJson = JSON.stringify(cl).replace(/"/g, '&quot;');
      return `
        <div class="sc" style="cursor:pointer;text-align:center" onclick="openChecklist('${k}', ${clJson})">
          <div style="font-size:28px;margin-bottom:8px">${esc(cl.icon||'📱')}</div>
          <div class="sc-lbl" style="font-weight:700;color:var(--txt2)">${esc(cl.name)}</div>
          <div style="font-size:10px;margin-top:4px;color:${riskCol}">${esc(cl.risk||'')}</div>
        </div>
      `;
    }).join('');
  });
}
function openChecklist(type, cl) {
  CL_DONE = {};
  document.getElementById('checklist-active').style.display='block';
  document.getElementById('checklist-name').textContent = cl.icon + ' ' + cl.name;
  var steps = cl.steps||[];
  document.getElementById('checklist-steps').innerHTML = steps.map(function(s,i) {
    return `
      <div id="cls-${s.id}" style="display:flex;align-items:flex-start;gap:12px;padding:12px 14px;border-bottom:1px solid var(--rim)">
        <div style="width:24px;height:24px;border-radius:50%;border:2px solid var(--rim2);display:flex;align-items:center;justify-content:center;font-size:11px;cursor:pointer;flex-shrink:0" id="clc-${s.id}" onclick="toggleCLStep('${s.id}')">
          <span id="clx-${s.id}"> </span>
        </div>
        <div style="flex:1">
          <div style="font-size:13px;font-weight:700;color:var(--txt)">${esc(s.title)}</div>
          <div style="font-size:11px;color:var(--txt3);margin-top:2px">${esc(s.why||'')}</div>
          ${s.page ? `<button class="btn btn-ghost btn-xs" style="margin-top:6px" onclick="go('${s.page}')">→ Open Page</button>` : ''}
        </div>
      </div>
    `;
  }).join('');
}
function toggleCLStep(id) {
  CL_DONE[id] = !CL_DONE[id];
  var done = CL_DONE[id];
  document.getElementById('clc-'+id).style.borderColor = done?'var(--mint)':'var(--rim2)';
  document.getElementById('clx-'+id).textContent = done ? '✓' : ' ';
  document.getElementById('clx-'+id).style.color = 'var(--mint)';
}
function closeChecklist() { document.getElementById('checklist-active').style.display='none'; }

// ── Phase 2: Workspaces ────────────────────────────────────────
var WS_CURRENT = null;
function loadWorkspaces() {
  api('/api/workspace/list').then(function(d) {
    var el = document.getElementById('ws-list');
    if (!d || !d.length) { el.innerHTML='<div class="empty" style="padding:20px"><div class="empty-ic">💼</div><div class="empty-tt">No workspaces</div></div>'; return; }
    el.innerHTML = d.map(function(w) {
      return `
        <div class="ssi" style="cursor:pointer" onclick="openWorkspaceByPkg('${esc(w.package)}')">
          <div class="ssi-ic">💼</div>
          <div style="flex:1;min-width:0">
            <div class="ssi-nm">${esc(w.package)}</div>
            <div class="ssi-mt">
              ${w.last_used ? new Date(w.last_used).toLocaleDateString() : ''}
              ${w.has_scan ? ' · scan ✓' : ''}
              ${w.has_cve ? ' · CVE ✓' : ''}
            </div>
          </div>
        </div>
      `;
    }).join('');
  });
}
function openWorkspace() {
  var pkg = document.getElementById('ws-pkg').value.trim();
  if (!pkg) return;
  openWorkspaceByPkg(pkg);
}
function openWorkspaceByPkg(pkg) {
  WS_CURRENT = pkg;
  api('/api/workspace/'+encodeURIComponent(pkg)).then(function(ws) {
    document.getElementById('ws-detail').style.display='block';
    document.getElementById('ws-title').textContent='💼 '+pkg;
    var html = '<div class="fg"><label class="fl">Notes</label><textarea class="fi" id="ws-notes" rows="3" style="resize:vertical">'+esc(ws.notes||'')+'</textarea></div>' +
      '<div class="fg"><label class="fl">Preferred Bypass Scripts</label><input class="fi" id="ws-scripts" value="'+esc((ws.preferred_scripts||[]).join(', '))+'"></div>' +
      '<div class="fg"><label class="fl">Device Serial</label><input class="fi" id="ws-serial" value="'+esc(ws.serial||'')+'"></div>' +
      '<div class="fg"><label class="fl">Proxy Host:Port</label><input class="fi" id="ws-proxy" value="'+esc((ws.proxy||{host:'127.0.0.1',port:8080}).host+':'+((ws.proxy||{}).port||8080))+'"></div>' +
      '<div class="cf mt8"><button class="btn btn-lime btn-sm" onclick="saveWorkspace()">💾 Save</button>' +
      '<button class="btn btn-ghost btn-sm" onclick="applyWorkspace()">⚡ Apply to Bypass</button></div>' +
      '<div style="font-size:11px;color:var(--txt4);margin-top:12px">Sessions: '+(ws.session_ids||[]).length+' · Last: '+(ws.last_used?new Date(ws.last_used).toLocaleString():'never')+'</div>';
    document.getElementById('ws-body').innerHTML = html;
    loadWorkspaces();
  });
}
function saveWorkspace() {
  if (!WS_CURRENT) return;
  var scripts = document.getElementById('ws-scripts').value.split(',').map(function(s){ return s.trim(); }).filter(Boolean);
  var proxyStr = document.getElementById('ws-proxy').value.split(':');
  api('/api/workspace/'+encodeURIComponent(WS_CURRENT),'POST',{
    notes: document.getElementById('ws-notes').value,
    preferred_scripts: scripts,
    serial: document.getElementById('ws-serial').value,
    proxy: {host: proxyStr[0]||'127.0.0.1', port: parseInt(proxyStr[1])||8080},
  }).then(function(){ toast('Workspace saved','ok'); loadWorkspaces(); });
}
function applyWorkspace() {
  if (!WS_CURRENT) return;
  api('/api/workspace/'+encodeURIComponent(WS_CURRENT)).then(function(ws) {
    // Navigate to bypass and pre-fill
    go('bypass');
    setTimeout(function() {
      if (ws.serial && document.getElementById('device-select')) document.getElementById('device-select').value = ws.serial;
    }, 300);
    toast('Workspace applied to Bypass','ok');
  });
}
function deleteWorkspace() {
  if (!WS_CURRENT || !confirm('Delete workspace for '+WS_CURRENT+'?')) return;
  fetch('/api/workspace/'+encodeURIComponent(WS_CURRENT),{method:'DELETE'})
    .then(function(){ WS_CURRENT=null; document.getElementById('ws-detail').style.display='none'; loadWorkspaces(); toast('Workspace deleted','warn'); });
}

// ── Extend go() for Phase 2 pages and auto-init ───────────────
var _go2 = go;
go = function(id) {
  _go2(id);
  if (id === 'checklist') loadChecklistTypes();
  if (id === 'workspaces') loadWorkspaces();
};


function resetScript() {
  if (!ED_CURRENT || !confirm('Reset ' + ED_CURRENT + ' to built-in default? All custom changes will be lost.')) return;
  api('/api/scripts/'+ED_CURRENT+'/reset', 'POST').then(function(d) {
    if(d.ok) { toast('Script reset', 'ok'); loadScripts(); loadScriptToEditor(ED_CURRENT); }
    else toast('Reset failed', 'err');
  });
}

function startObjection() {
  var target = document.getElementById('bp-target').value.trim();
  var sel = document.getElementById('device-select');
  var serial = sel && sel.selectedOptions.length ? sel.selectedOptions[0].value : null;
  if (!target) { toast('Target package name required for Objection','warn'); return; }
  api('/api/objection/start', 'POST', {target:target, serial:serial}).then(function(d) {
    if(d.ok) toast('Objection terminal launched! Check your desktop.', 'ok');
    else toast('Objection failed: '+d.error, 'err');
  });
}

// Phase 4: AI Analysis
function askAI(title, details, context, btnElement) {
  if(btnElement) { btnElement.textContent = "🤖 Thinking..."; btnElement.disabled = true; }
  api('/api/ai/analyze', 'POST', {title:title, details:details, context:context}).then(function(d) {
    if(btnElement) { btnElement.textContent = "Ask AI 🤖"; btnElement.disabled = false; }
    if(d.ok) {
      let html = '<div style="font-size:12px;margin-bottom:8px"><b>Explanation:</b><br/>'+esc(d.analysis.explanation)+'</div>';
      html += '<div style="font-size:12px;margin-bottom:8px"><b>Impact:</b><br/>'+esc(d.analysis.impact)+'</div>';
      html += '<div style="font-size:12px;margin-bottom:8px"><b>Remediation:</b><br/>'+esc(d.analysis.remediation)+'</div>';
      if(d.analysis.code_snippet) {
        html += '<div style="font-size:11px;font-family:var(--mono);background:#1a1a1a;padding:8px;border-radius:4px;white-space:pre-wrap;color:#a6e22e">';
        html += esc(d.analysis.code_snippet) + '</div>';
      }
      
      let modal = document.createElement('div');
      modal.style.cssText = 'position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);width:500px;background:var(--card);border:1px solid var(--rim);box-shadow:0 10px 30px rgba(0,0,0,0.5);border-radius:8px;padding:20px;z-index:9999;';
      modal.innerHTML = '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:15px;border-bottom:1px solid var(--rim);padding-bottom:10px;"><h3 style="margin:0;color:var(--lime)">AI Pentester Analysis</h3><button onclick="this.parentElement.parentElement.remove()" style="background:none;border:none;color:var(--txt3);cursor:pointer;font-size:16px;">&times;</button></div>' + html;
      document.body.appendChild(modal);
    } else {
      toast('AI Error: '+d.error, 'err');
    }
  });
}

// Phase 4: API Auto-Discovery
function refreshApiMap() {
  api('/api/discovery/map').then(function(d) {
    if(!d.ok) return;
    let map = d.map;
    document.getElementById('map-stats').innerText = map.hosts.length + ' hosts • ' + map.endpoints.length + ' endpoints';
    
    let wrap = document.getElementById('api-map-results');
    if(!map.endpoints.length) {
      wrap.innerHTML = '<div style="padding:40px;text-align:center;color:var(--txt3);border:1px dashed var(--rim);border-radius:6px;">No endpoints discovered yet.</div>';
      return;
    }
    
    let html = '';
    // Group by host visually
    map.hosts.forEach(function(host) {
      let eps = map.endpoints.filter(e => e.host === host);
      if(!eps.length) return;
      
      html += '<div class="card mb16"><div class="ch"><div class="ct">🌐 ' + esc(host) + ' <span class="badge" style="margin-left:8px">'+eps.length+'</span></div></div><div class="cb" style="padding:0">';
      html += '<table class="table"><thead><tr><th width="60">Method</th><th>Path</th><th>Sources</th><th>Parameters</th></tr></thead><tbody>';
      
      eps.forEach(function(e) {
        let mColor = e.method==='POST'||e.method==='PUT'?'var(--amber)':(e.method==='DELETE'?'var(--red)':'var(--cyan)');
        let srcs = e.sources.map(s => '<span class="badge">'+s+'</span>').join(' ');
        let params = e.params.length ? esc(e.params.join(', ')) : '<span style="color:var(--txt3)">none</span>';
        
        html += '<tr>';
        html += '<td style="color:'+mColor+';font-weight:600">'+esc(e.method)+'</td>';
        html += '<td style="font-family:var(--mono);">'+esc(e.path||'/')+'</td>';
        html += '<td>'+srcs+'</td>';
        html += '<td style="font-family:var(--mono);font-size:10px">'+params+'</td>';
        html += '</tr>';
      });
      html += '</tbody></table></div></div>';
    });
    wrap.innerHTML = html;
  });
}

function extractStaticApis() {
  if(!window.LAST_SCAN_FINDINGS || !window.LAST_SCAN_STRINGS) {
    toast('Run a Vulnerability Scan first to extract static AST strings', 'warn');
    return;
  }
  api('/api/discovery/extract/static', 'POST', {strings: window.LAST_SCAN_STRINGS}).then(function(d){
    if(d.ok) { toast('Extracted '+d.endpoint_count+' endpoints from AST strings', 'ok'); refreshApiMap(); }
    else toast('Extraction failed', 'err');
  });
}

function exportPostman() {
  let appName = document.getElementById('rp-app') ? document.getElementById('rp-app').value : 'GhostPin_App';
  api('/api/export/postman', 'POST', {appName: appName}).then(function(d){
    if(d.ok) toast('Postman Collection saved to: '+d.path, 'ok');
    else toast('Export failed', 'err');
  });
}


// Phase 5: Auto-Patcher
function runAutoPatcher() {
  let f = document.getElementById('patch-file').files[0];
  if(!f) return toast('Select an APK or IPA first', 'err');
  
  let status = document.getElementById('patcher-status');
  status.style.display = 'block';
  status.style.color = 'var(--amber)';
  status.innerText = '⚙️ Patching... this may take 1-2 minutes. Please wait...';
  
  let fd = new FormData();
  fd.append('file', f);
  
  fetch('/api/apk/patch', { method: 'POST', body: fd })
    .then(async res => {
      if(!res.ok) {
        let err = await res.json();
        throw new Error(err.error || 'Patching failed');
      }
      return res.blob();
    })
    .then(blob => {
      status.style.color = 'var(--lime)';
      status.innerText = '✅ Patching complete! Downloading file...';
      
      let url = window.URL.createObjectURL(blob);
      let a = document.createElement('a');
      a.href = url;
      a.download = f.name.replace(/\\.[^/.]+$/, "") + "-patched" + f.name.substring(f.name.lastIndexOf('.'));
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    })
    .catch(err => {
      status.style.color = 'var(--red)';
      status.innerText = '❌ Error: ' + err.message;
      toast(err.message, 'err');
    });
}


// Phase 6: APK Extractor
function runAPKExtractor() {
  let pkg = document.getElementById('extract-package').value.trim();
  if(!pkg) return toast('Enter a package name (e.g. com.example.app)', 'err');
  
  if(!window.ACTIVE_SERIAL) return toast('Connect to a device on the Bypass page first', 'err');
  
  let status = document.getElementById('extractor-status');
  status.style.display = 'block';
  status.style.color = 'var(--amber)';
  status.innerText = '⚙️ Pulling APK from device via ADB... please wait...';
  
  fetch('/api/apk/extract', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ serial: window.ACTIVE_SERIAL, package: pkg })
  })
    .then(async res => {
      if(!res.ok) {
        let err = await res.json();
        throw new Error(err.error || 'Failed to extract APK');
      }
      return res.blob();
    })
    .then(blob => {
      status.style.color = 'var(--lime)';
      status.innerText = '✅ APK Extracted Successfully! Downloading...';
      
      let url = window.URL.createObjectURL(blob);
      let a = document.createElement('a');
      a.href = url;
      a.download = pkg + ".apk";
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    })
    .catch(err => {
      status.style.color = 'var(--red)';
      status.innerText = '❌ Error: ' + err.message;
      toast(err.message, 'err');
    });
}


// Phase 7: Native Decompiler
window.ACTIVE_DECOMPILE_WID = null;

function startDecompile() {
  let f = document.getElementById('dc-file').files[0];
  if(!f) return toast('Select an APK first', 'err');
  
  let status = document.getElementById('dc-status');
  status.style.display = 'block';
  status.style.color = 'var(--amber)';
  status.innerText = '⚙️ JADX is decompiling the app... This may take up to 3 minutes for large apps...';
  
  let fd = new FormData();
  fd.append('file', f);
  
  fetch('/api/decompile', { method: 'POST', body: fd })
    .then(async res => {
      let data = await res.json();
      if(!res.ok) throw new Error(data.error || 'Decompilation failed');
      return data;
    })
    .then(data => {
      status.style.color = 'var(--lime)';
      status.innerText = '✅ Decompilation complete! Workspace ready.';
      window.ACTIVE_DECOMPILE_WID = data.workspace_id;
      
      // Hide upload, show workspace
      document.getElementById('dc-upload-card').style.display = 'none';
      document.getElementById('dc-workspace').style.display = 'flex';
      
      // Attempt to load manifest by default
      loadSourceFile();
    })
    .catch(err => {
      status.style.color = 'var(--red)';
      status.innerText = '❌ Error: ' + err.message;
      toast(err.message, 'err');
    });
}

function loadSourceFile() {
  if(!window.ACTIVE_DECOMPILE_WID) return;
  let path = document.getElementById('dc-filepath').value.trim();
  if(!path) return;
  
  let status = document.getElementById('dc-file-status');
  status.innerText = 'Loading...';
  status.style.color = 'var(--amber)';
  
  fetch(`/api/decompile/file?workspace_id=${window.ACTIVE_DECOMPILE_WID}&file_path=${encodeURIComponent(path)}`)
    .then(r => r.json())
    .then(data => {
       if(!data.ok) {
           status.innerText = 'File not found.';
           status.style.color = 'var(--red)';
       } else {
           status.innerText = 'Loaded file successfully.';
           status.style.color = 'var(--lime)';
           document.getElementById('dc-code-viewer').value = data.content;
       }
    })
    .catch(e => {
       status.innerText = String(e);
       status.style.color = 'var(--red)';
    });
}


function deployStealthFrida() {
    if(!window.ACTIVE_SERIAL) return toast('No device selected', 'err');
    
    let logs = document.getElementById('frida-logs');
    logs.style.display = 'block';
    logs.innerHTML = `🛡️ Requesting Stealth hluda-server deployment...
`;
    
    fetch('/api/frida/stealth', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({serial: window.ACTIVE_SERIAL})
    }).then(r => r.json()).then(res => {
        if(res.ok) {
            logs.innerHTML += `
✅ STEALTH DEPLOYED: ${res.binary_name}
`;
        } else {
            logs.innerHTML += `
❌ ERROR: ${res.error}
`;
        }
    });
}


function showCGFuzzerCard() {
    let card = document.getElementById('cg-fuzzer-card');
    if(card) card.style.display = 'block';
}
// Show CG card whenever the fuzzer page is activated
document.addEventListener('DOMContentLoaded', () => {
  let origNav = window.nav;
  window.nav = function(page, el) {
    origNav && origNav(page, el);
    if(page === 'pg-fuzzer') showCGFuzzerCard();
  };
});

function runCoverageFuzzer() {
    if(!window.ACTIVE_SERIAL) return toast('Connect a device first', 'err');
    if(!window.ACTIVE_PACKAGE) return toast('Select a package first', 'err');
    
    let component = document.getElementById('cg-component').value.trim();
    if(!component) return toast('Enter a component name', 'err');
    let maxIter = parseInt(document.getElementById('cg-max-iter').value || '30');
    
    let status    = document.getElementById('cg-status');
    let statusTxt = document.getElementById('cg-status-text');
    let results   = document.getElementById('cg-results');
    
    status.style.display = 'block';
    results.style.display = 'none';
    statusTxt.innerHTML = '⚙️ Coverage-Guided Fuzzer running... (this may take a few minutes)';
    
    let fullComponent = component.startsWith('.')
        ? window.ACTIVE_PACKAGE + component
        : component;
    
    fetch('/api/fuzzer/coverage', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({
            serial: window.ACTIVE_SERIAL,
            package: window.ACTIVE_PACKAGE,
            component: fullComponent,
            max_iter: maxIter
        })
    }).then(r=>r.json()).then(res => {
        if(!res.ok) return toast(res.error, 'err');
        statusTxt.innerHTML = '⏳ Fuzzer running in background (scan_id: ' + res.scan_id + ')...';
        pollCGResults(res.scan_id);
    });
}

function pollCGResults(scanId) {
    let statusTxt = document.getElementById('cg-status-text');
    let results   = document.getElementById('cg-results');
    
    let iv = setInterval(() => {
        fetch('/api/fuzzer/coverage/results/' + scanId)
            .then(r => r.json())
            .then(data => {
                if(data.status !== 'done') return;
                clearInterval(iv);
                
                statusTxt.innerHTML = '✅ Fuzzing complete!';
                results.style.display = 'block';
                
                let crashHtml = data.crashes && data.crashes.length > 0
                    ? data.crashes.map(c => `<li><code>${c.payload ? c.payload.slice(0,60) : 'N/A'}</code> — <span style="color:var(--red)">CRASH</span></li>`).join('')
                    : '<li style="color:var(--txt3)">No crashes detected.</li>';
                    
                let interestHtml = data.interesting && data.interesting.length > 0
                    ? data.interesting.map(i => `<li><code>${i.payload ? i.payload.slice(0,60) : 'N/A'}</code> — <span style="color:var(--lime)">+${i.new_blocks} new blocks</span></li>`).join('')
                    : '<li style="color:var(--txt3)">No new code paths triggered.</li>';
                
                results.innerHTML = `
                  <div style="font-size:12px;">
                    <div class="card mb8">
                      <div class="ch"><div class="ct">Results Summary</div></div>
                      <div class="cb">
                        <table style="width:100%;border-collapse:collapse;font-size:12px;">
                          <tr><td style="padding:4px;">Iterations run</td><td style="color:var(--lime)">${data.iterations}</td></tr>
                          <tr><td style="padding:4px;">Unique basic blocks covered</td><td style="color:var(--lime)">${data.total_blocks}</td></tr>
                          <tr><td style="padding:4px;">Interesting payloads</td><td style="color:var(--amber)">${data.interesting ? data.interesting.length : 0}</td></tr>
                          <tr><td style="padding:4px;">Crashes detected</td><td style="color:var(--red)">${data.crashes ? data.crashes.length : 0}</td></tr>
                        </table>
                      </div>
                    </div>
                    <div class="card mb8">
                      <div class="ch"><div class="ct">🔴 Crashes &amp; Hangs</div></div>
                      <div class="cb"><ul style="margin:0;padding-left:16px;">${crashHtml}</ul></div>
                    </div>
                    <div class="card">
                      <div class="ch"><div class="ct">🟡 Interesting Payloads (New Code Paths)</div></div>
                      <div class="cb"><ul style="margin:0;padding-left:16px;">${interestHtml}</ul></div>
                    </div>
                  </div>
                `;
            });
    }, 4000);
}

</script>
</body>
</html>"""

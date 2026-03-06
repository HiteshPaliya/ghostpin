"""
GhostPin v5.0 — Feature: Smart Report Generator
Generates professional HTML penetration test reports from session data.
"""

import json
from datetime import datetime
from pathlib import Path

REPORT_CSS = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
  :root{--bg:#0d1018;--c1:#111520;--c2:#1d2333;--lime:#b8ff47;--red:#ff4d6a;--amber:#ffaa33;--mint:#2effa0;--cyan:#3de8ff;--violet:#b47aff;--txt:#d8e0f4;--txt2:#8892bc;--txt3:#4a5278;}
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:var(--bg);color:var(--txt);font-family:'Inter',sans-serif;font-size:14px;line-height:1.6;padding:40px;}
  .cover{background:linear-gradient(135deg,#111520,#1d2333);border:1px solid #252d42;border-radius:16px;padding:60px;margin-bottom:40px;text-align:center;}
  .cover-logo{font-size:64px;margin-bottom:20px}
  .cover-title{font-size:36px;font-weight:800;color:var(--lime);letter-spacing:-1px}
  .cover-sub{font-size:18px;color:var(--txt2);margin-top:8px}
  .cover-meta{display:flex;justify-content:center;gap:30px;margin-top:30px;font-size:12px;color:var(--txt3)}
  .cover-meta-item{background:var(--bg);padding:10px 20px;border-radius:8px;border:1px solid #252d42}
  .cover-meta-item strong{display:block;color:var(--txt);font-size:14px;margin-top:4px}
  h1{font-size:24px;font-weight:800;color:var(--txt);margin:40px 0 16px;padding-bottom:8px;border-bottom:1px solid #252d42}
  h2{font-size:18px;font-weight:700;color:var(--lime);margin:24px 0 12px}
  .section{background:var(--c1);border:1px solid #252d42;border-radius:12px;padding:24px;margin-bottom:24px}
  .stats-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:32px}
  .stat{background:var(--c1);border:1px solid #252d42;border-radius:10px;padding:20px;text-align:center;position:relative;overflow:hidden}
  .stat::before{content:'';position:absolute;left:0;top:0;bottom:0;width:3px}
  .stat.critical::before{background:var(--red)}.stat.high::before{background:var(--amber)}
  .stat.medium::before{background:var(--cyan)}.stat.ok::before{background:var(--mint)}
  .stat-num{font-size:40px;font-weight:800;line-height:1}
  .stat.critical .stat-num{color:var(--red)}.stat.high .stat-num{color:var(--amber)}
  .stat.medium .stat-num{color:var(--cyan)}.stat.ok .stat-num{color:var(--mint)}
  .stat-lbl{font-size:11px;text-transform:uppercase;letter-spacing:1.5px;color:var(--txt2);margin-top:6px}
  .finding{background:var(--c2);border-radius:8px;padding:14px 16px;margin-bottom:10px;border-left:4px solid}
  .finding.critical{border-color:var(--red)}.finding.high{border-color:var(--amber)}
  .finding.medium{border-color:var(--cyan)}.finding.low{border-color:var(--txt3)}
  .finding-header{display:flex;align-items:center;gap:10px;margin-bottom:6px}
  .badge{font-size:10px;font-weight:700;padding:2px 8px;border-radius:4px;text-transform:uppercase}
  .badge.critical{background:rgba(255,77,106,.2);color:var(--red)}
  .badge.high{background:rgba(255,170,51,.2);color:var(--amber)}
  .badge.medium{background:rgba(61,232,255,.2);color:var(--cyan)}
  .badge.low{background:#252d42;color:var(--txt3)}
  .finding-type{font-weight:700;font-size:13px}
  .finding-loc{font-size:11px;color:var(--txt3);font-family:'JetBrains Mono',monospace}
  .finding-detail{font-size:12px;color:var(--txt2);margin-top:4px}
  .evidence{font-family:'JetBrains Mono',monospace;font-size:10px;background:#080b12;color:var(--lime);padding:6px 10px;border-radius:4px;margin-top:6px;word-break:break-all}
  .score-circle{width:120px;height:120px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-direction:column;margin:0 auto 16px;font-size:36px;font-weight:800;border:4px solid}
  .score-A{border-color:var(--mint);color:var(--mint);background:rgba(46,255,160,.08)}
  .score-B{border-color:var(--cyan);color:var(--cyan);background:rgba(61,232,255,.08)}
  .score-C{border-color:var(--amber);color:var(--amber);background:rgba(255,170,51,.08)}
  .score-D,.score-F{border-color:var(--red);color:var(--red);background:rgba(255,77,106,.08)}
  .log-entry{font-family:'JetBrains Mono',monospace;font-size:11px;padding:2px 0;border-bottom:1px solid #111520;color:var(--txt2)}
  .log-entry.frida{color:var(--lime)}.log-entry.error{color:var(--red)}.log-entry.success{color:var(--mint)}
  .kv{display:flex;gap:8px;padding:6px 0;border-bottom:1px solid #252d42;font-size:12px}
  .kv:last-child{border-bottom:none}.kv-k{width:160px;color:var(--txt3);flex-shrink:0}
  .kv-v{color:var(--txt)}
  code{font-family:'JetBrains Mono',monospace;font-size:11px;background:rgba(184,255,71,.08);color:var(--lime);padding:2px 6px;border-radius:4px}
  .tbl{width:100%;border-collapse:collapse;font-size:12px}
  .tbl th{text-align:left;padding:8px 12px;font-size:10px;text-transform:uppercase;letter-spacing:1px;color:var(--txt3);border-bottom:1px solid #252d42;background:#111520}
  .tbl td{padding:8px 12px;border-bottom:1px solid #1d2333;color:var(--txt2)}
  .tbl tr:last-child td{border-bottom:none}
  .footer{text-align:center;padding:30px;color:var(--txt3);font-size:11px;margin-top:40px;border-top:1px solid #252d42}
  @media print{body{background:#fff;color:#000}.section{border-color:#ccc}code{color:#2563eb}.cover{background:#f8fafc}}
</style>
"""

def generate_report(report_data: dict, output_path: Path) -> str:
    """Generate a professional HTML penetration testing report."""
    now = datetime.now()
    app_name = report_data.get('app_name', 'Unknown Target')
    platform = report_data.get('platform', 'android')
    tester = report_data.get('tester', 'GhostPin')
    session_logs = report_data.get('logs', [])
    vuln_findings = report_data.get('vuln_findings', [])
    analysis = report_data.get('analysis', {})
    mdm = report_data.get('mdm', {})
    monitor_calls = report_data.get('monitor_calls', [])

    # Summary stats
    crit = sum(1 for f in vuln_findings if f.get('severity') == 'critical')
    high = sum(1 for f in vuln_findings if f.get('severity') == 'high')
    med  = sum(1 for f in vuln_findings if f.get('severity') == 'medium')
    low  = sum(1 for f in vuln_findings if f.get('severity') == 'low')
    grade = analysis.get('grade', 'N/A')
    score = analysis.get('score', 'N/A')

    def kv_row(k, v):
        return f'<div class="kv"><div class="kv-k">{k}</div><div class="kv-v">{v}</div></div>'

    def finding_html(f):
        sev = f.get('severity', 'low')
        evidence_html = ''
        if f.get('evidence'):
            evidence_html = ''.join(f'<div class="evidence">{e}</div>' for e in f['evidence'][:2])
        return f'''
        <div class="finding {sev}">
          <div class="finding-header">
            <span class="badge {sev}">{sev}</span>
            <span class="finding-type">{f.get("type", "")}</span>
          </div>
          <div class="finding-loc">{f.get("location", "")}</div>
          <div class="finding-detail">{f.get("detail", "")}</div>
          {evidence_html}
        </div>'''

    findings_html = ''.join(finding_html(f) for f in vuln_findings) if vuln_findings else \
        '<div style="color:var(--mint);padding:20px;text-align:center">✓ No static vulnerabilities detected</div>'

    log_html = ''
    for entry in session_logs[:200]:
        lvl = entry.get('level', 'info')
        log_html += f'<div class="log-entry {lvl}">{entry.get("msg", "")}</div>'

    monitor_html = ''
    for call in monitor_calls[:100]:
        monitor_html += f'<div class="log-entry">{call}</div>'

    mdm_html = ''
    if mdm:
        vendors = ', '.join(mdm.get('vendors', [])) or 'None detected'
        mdm_html = f'''
        <div class="section">
          <h2>🏢 MDM / Enterprise Profile</h2>
          {kv_row("MDM Detected", "⚠ Yes — " + vendors if mdm.get("mdm_detected") else "✓ No MDM detected")}
          {kv_row("Work Profile", "Yes" if mdm.get("work_profile") else "No")}
          {kv_row("Knox", "Yes" if mdm.get("knox_enabled") else "No")}
          {kv_row("Risk Level", mdm.get("risk_level", "none").upper())}
          {"".join(f'<div style="margin-top:6px;font-size:12px;color:var(--txt2)">• {n}</div>' for n in mdm.get("notes", []))}
        </div>'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>GhostPin Report — {app_name}</title>
{REPORT_CSS}
</head>
<body>

<div class="cover">
  <div class="cover-logo">🔐</div>
  <div class="cover-title">Penetration Test Report</div>
  <div class="cover-sub">{app_name} · Mobile Security Assessment</div>
  <div class="cover-meta">
    <div class="cover-meta-item">Platform<strong>{platform.upper()}</strong></div>
    <div class="cover-meta-item">Date<strong>{now.strftime("%B %d, %Y")}</strong></div>
    <div class="cover-meta-item">Tester<strong>{tester}</strong></div>
    <div class="cover-meta-item">Tool<strong>GhostPin v5.0</strong></div>
  </div>
</div>

<h1>Executive Summary</h1>
<div class="stats-grid">
  <div class="stat critical"><div class="stat-num">{crit}</div><div class="stat-lbl">Critical</div></div>
  <div class="stat high"><div class="stat-num">{high}</div><div class="stat-lbl">High</div></div>
  <div class="stat medium"><div class="stat-num">{med}</div><div class="stat-lbl">Medium</div></div>
  <div class="stat ok"><div class="stat-num">{low}</div><div class="stat-lbl">Low</div></div>
</div>

<div class="section" style="text-align:center">
  <div class="score-circle score-{grade}">{grade}<div style="font-size:14px">{score}/100</div></div>
  <div style="font-size:16px;font-weight:700">Security Score: {score}/100</div>
  <div style="font-size:12px;color:var(--txt3);margin-top:4px">Based on static analysis findings — lower is worse</div>
</div>

<div class="section">
  <h2>📱 Application Details</h2>
  {kv_row("Application", app_name)}
  {kv_row("Platform", platform.upper())}
  {kv_row("File", analysis.get("file", "N/A"))}
  {kv_row("Frameworks", ", ".join(analysis.get("frameworks", [])) or "None detected")}
  {kv_row("NSC Pinning", "⚠ Detected" if analysis.get("hasNSC") else "✓ None")}
  {kv_row("mTLS", "⚠ Client cert found in APK" if analysis.get("mTLS") else "✓ None")}
  {kv_row("Obfuscated", "Yes (ProGuard/R8)" if analysis.get("obfuscated") else "No")}
</div>

<h1>Vulnerability Findings ({len(vuln_findings)} total)</h1>
{findings_html}

{mdm_html}

''' + (f'''
<h1>Bypass Session Log</h1>
<div class="section">
  <div style="max-height:400px;overflow-y:auto">
    {log_html if log_html else '<div style="color:var(--txt3)">No session logs captured</div>'}
  </div>
</div>
''' if session_logs else '') + (f'''
<h1>Runtime API Monitor</h1>
<div class="section">
  <div style="max-height:400px;overflow-y:auto">
    {monitor_html if monitor_html else '<div style="color:var(--txt3)">No API calls monitored</div>'}
  </div>
</div>
''' if monitor_calls else '') + f'''

<div class="footer">
  Generated by GhostPin v5.0 · {now.strftime("%Y-%m-%d %H:%M:%S")} ·
  For authorized penetration testing only. Unauthorized use is illegal under CFAA, CMA, and equivalent statutes.
</div>

</body>
</html>'''

    output_path.write_text(html, encoding='utf-8')
    return str(output_path)

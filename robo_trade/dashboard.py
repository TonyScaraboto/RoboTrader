from __future__ import annotations
import os
from pathlib import Path
from flask import Flask, render_template_string, request, jsonify
import csv
import threading
import time
from typing import List, Dict, Any
from .config import settings

try:
  import ccxt  # type: ignore
except Exception:
  ccxt = None

TEMPLATE = """
<!doctype html>
<html lang="pt-br">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Robo Trade - Painel</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/chartjs-chart-financial@4.3.0/dist/chartjs-chart-financial.min.js"></script>
  <script>function fmt(n){try{return Number(n).toFixed(2)}catch(e){return n}}</script>
  <style>
    :root{--bg:#0f172a;--panel:#0b1220;--card:#111827;--text:#e5e7eb;--muted:#9ca3af;--border:#1f2937;--accent:#16a34a;--accent-600:#22c55e;--accent-light:rgba(22,163,74,0.1);--danger:#ef4444;--space-2:8px;--space-3:12px;--space-4:16px;--space-5:20px;--space-6:24px;--radius:12px;--radius-sm:8px;--radius-xs:6px;--shadow:0 4px 12px rgba(0,0,0,0.3);--shadow-lg:0 12px 32px rgba(0,0,0,0.4)}
    *{box-sizing:border-box}html,body{height:100%}body{margin:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Inter,Arial,sans-serif;background:var(--bg);color:var(--text);-webkit-font-smoothing:antialiased;color-scheme:light dark;line-height:1.5}
    .layout{display:grid;grid-template-columns:260px 1fr;height:100vh;gap:0}
    aside{background:var(--panel);border-right:1px solid var(--border);padding:var(--space-6) var(--space-4);display:flex;flex-direction:column;overflow-y:auto}
    .brand{font-weight:700;font-size:20px;letter-spacing:-0.5px;margin-bottom:var(--space-6);color:var(--text)}.brand::before{content:'⚡';display:inline-block;margin-right:8px}
    .nav{flex:1}.nav a{display:flex;align-items:center;color:var(--muted);text-decoration:none;padding:10px var(--space-3);border-radius:var(--radius-xs);transition:all .2s ease;font-size:14px;gap:8px}.nav a.active{background:var(--accent-light);color:var(--accent);font-weight:600}.nav a:hover{background:rgba(22,163,74,0.2);color:var(--text)}
    header{display:flex;align-items:center;justify-content:space-between;padding:16px 24px;border-bottom:1px solid var(--border);background:var(--panel);position:sticky;top:0;z-index:10;box-shadow:var(--shadow)}
    .header-title{font-size:18px;font-weight:700;letter-spacing:-0.3px}
    .header-controls{display:flex;align-items:center;gap:16px}
    .status-badge{display:inline-flex;align-items:center;gap:6px;padding:6px 12px;border-radius:var(--radius-xs);background:var(--accent-light);color:var(--accent);font-size:12px;font-weight:600;text-transform:uppercase}#botStatus{font-weight:700}
    main{padding:var(--space-6);overflow:auto;background:linear-gradient(135deg,var(--bg) 0%,#1a2340 100%)}
    .container{max-width:1400px;margin:0 auto}
    .grid{display:grid;grid-template-columns:1fr 1fr;gap:var(--space-6);margin-bottom:var(--space-6)}
    .grid-3{grid-template-columns:repeat(3,1fr)}
    .grid-full{grid-template-columns:1fr}
    .card{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:var(--space-6);box-shadow:var(--shadow);transition:all .3s ease;position:relative;overflow:hidden}
    .card::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,var(--accent),transparent);opacity:0}
    .card:hover{border-color:var(--accent);box-shadow:var(--shadow-lg),0 0 24px rgba(22,163,74,0.2)}.card:hover::before{opacity:1}
    h2{margin:0 0 var(--space-4) 0;font-size:16px;font-weight:700;letter-spacing:-0.3px;color:var(--text)}
    .controls{display:grid;grid-template-columns:1fr 1fr 1fr;gap:var(--space-3);margin-bottom:var(--space-4)}
    .control-group{display:flex;flex-direction:column}
    .control-label{font-size:12px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px}
    label{font-size:13px;font-weight:500;color:var(--text);display:block;margin-bottom:4px}
    input,select{background:#0b1220;border:1px solid var(--border);color:var(--text);padding:12px 14px;border-radius:var(--radius-xs);outline:none;transition:all .2s ease;font-size:14px;width:100%}
    input:focus,select:focus{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-light);background:#131a2f}
    .button-group{display:flex;gap:var(--space-2)}
    .btn{padding:10px 16px;border-radius:var(--radius-xs);border:none;font-weight:600;font-size:13px;cursor:pointer;transition:all .2s ease;display:inline-flex;align-items:center;gap:6px;white-space:nowrap}
    .btn-primary{background:var(--accent);color:#0b141e}
    .btn-primary:hover{background:var(--accent-600);transform:translateY(-2px);box-shadow:0 8px 16px rgba(22,163,74,0.3)}
    .btn-primary:active{transform:translateY(0)}
    .btn-danger{background:var(--danger);color:#fff}
    .btn-danger:hover{transform:translateY(-2px);box-shadow:0 8px 16px rgba(239,68,68,0.3)}
    .btn-danger:active{transform:translateY(0)}
    .stat-card{background:linear-gradient(135deg,rgba(22,163,74,0.1) 0%,rgba(22,163,74,0.05) 100%);border:1px solid rgba(22,163,74,0.2);border-radius:var(--radius-sm);padding:var(--space-4);text-align:center;border-left:4px solid var(--accent)}
    .stat-label{font-size:12px;text-transform:uppercase;letter-spacing:0.5px;color:var(--muted);margin-bottom:8px;font-weight:600}
    .stat-value{font-size:28px;font-weight:700;color:var(--text)}
    table{width:100%;border-collapse:separate;border-spacing:0;font-size:13px}
    th{background:linear-gradient(180deg,#0f1a2e 0%,#0b1220 100%);padding:12px;text-align:left;vertical-align:middle;font-weight:700;text-transform:uppercase;font-size:11px;letter-spacing:0.5px;border-bottom:2px solid var(--border);position:sticky;top:0;z-index:1}
    td{padding:12px;border-bottom:1px solid var(--border);color:var(--text)}
    tbody tr:hover{background:rgba(22,163,74,0.08)}
    tbody tr:nth-child(even){background:rgba(14,22,40,0.5)}
    .small{font-size:12px;color:var(--muted)}
    canvas{max-width:100%;display:block}
    p{margin:8px 0}
    strong{font-weight:700}
    @keyframes shimmer{0%{background-position:-400px 0}100%{background-position:400px 0}}
    .skeleton{position:relative;overflow:hidden;border-radius:var(--radius-sm);background:linear-gradient(90deg,rgba(255,255,255,0.06) 0px,rgba(255,255,255,0.12) 40px,rgba(255,255,255,0.06) 80px);background-size:600px 100%;animation:shimmer 1.2s infinite linear}
    .skeleton-chart{height:320px;width:100%;border:1px dashed var(--border)}
    .skeleton-line{display:inline-block;height:1em;min-width:80px;border-radius:6px;vertical-align:middle;background:linear-gradient(90deg,rgba(255,255,255,0.06) 0px,rgba(255,255,255,0.16) 40px,rgba(255,255,255,0.06) 80px);background-size:600px 100%;animation:shimmer 1.2s infinite linear}
    @media(max-width:1024px){.layout{grid-template-columns:1fr}aside{display:none}.grid,.grid-3{grid-template-columns:1fr}.controls{grid-template-columns:1fr}}
    *::-webkit-scrollbar{height:10px;width:10px}
    *::-webkit-scrollbar-track{background:#0a0f1a}
    *::-webkit-scrollbar-thumb{background:#1f2937;border-radius:8px}
    *::-webkit-scrollbar-thumb:hover{background:#273244}
    @media(prefers-color-scheme:light){:root{--bg:#f5f7fa;--panel:#ffffff;--card:#ffffff;--text:#0f172a;--muted:#64748b;--border:#e2e8f0;--accent:#16a34a;--accent-600:#15803d;--accent-light:rgba(22,163,74,0.12);--danger:#dc2626;--shadow:0 4px 12px rgba(0,0,0,0.08);--shadow-lg:0 12px 32px rgba(0,0,0,0.12)}aside{border-right:1px solid var(--border)}header{border-bottom:1px solid var(--border);box-shadow:var(--shadow)}.nav a.active{background:var(--accent-light);color:var(--accent)}.nav a:hover{background:#f0fdf4}.card{border-color:var(--border)}.stat-card{background:linear-gradient(135deg,rgba(22,163,74,0.08) 0%,rgba(22,163,74,0.03) 100%);border:1px solid rgba(22,163,74,0.15)}.btn-primary{color:#fff}.btn-primary:hover{box-shadow:0 8px 16px rgba(22,163,74,0.25)}.btn-danger:hover{box-shadow:0 8px 16px rgba(220,38,38,0.25)}th{background:linear-gradient(180deg,#f3f4f6 0%,#eff2f5 100%)}.stat-label{color:var(--muted)}main{background:linear-gradient(135deg,#f5f7fa 0%,#eef2f7 100%)}}
    :root[data-theme="dark"]{color-scheme:dark}
    :root[data-theme="light"]{--bg:#f5f7fa;--panel:#ffffff;--card:#ffffff;--text:#0f172a;--muted:#64748b;--border:#e2e8f0;--accent:#16a34a;--accent-600:#15803d;--accent-light:rgba(22,163,74,0.12);--danger:#dc2626;--shadow:0 4px 12px rgba(0,0,0,0.08);--shadow-lg:0 12px 32px rgba(0,0,0,0.12);color-scheme:light}
    a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
  </style>
</head>
<body>
  <div class="layout">
    <aside>
      <div class="brand">Robo Trade</div>
      <nav class="nav">
        <a class="active" href="/" onclick="return navigateTo('dashboard')">📊 Dashboard</a>
        <a href="/operacoes" onclick="return navigateTo('operacoes')">📈 Operações</a>
        <a href="/configuracoes" onclick="return navigateTo('configuracoes')">⚙️ Configurações</a>
      </nav>
    </aside>
    <div style="display:flex;flex-direction:column;height:100vh">
      <header>
        <div class="header-title">📈 Visão Geral</div>
        <div class="header-controls">
          <label class="small" style="margin:0;display:flex;align-items:center;gap:6px">Quotex:
            <select id="quotexEnvironment" style="margin:0;min-width:130px" onchange="changeQuotexEnvironment(this.value)">
              <option value="demo">🏦 Demo (Sem Risco)</option>
              <option value="live">💰 Real (COM RISCO)</option>
            </select>
          </label>
          <label class="small" style="margin:0;display:flex;align-items:center;gap:6px">Conta:
            <select id="accountSelect" style="margin:0;min-width:150px" onchange="switchAccount(this.value)">
              <option value="all">📊 Todas as Contas</option>
              <option value="account1">👤 Conta 1 (Paper)</option>
              <option value="account2">👤 Conta 2 (Paper)</option>
              <option value="account3">👤 Conta 3 (Live)</option>
            </select>
          </label>
          <label class="small" style="margin:0;display:flex;align-items:center;gap:6px">Tema:
            <select id="themeSelect" style="margin:0;min-width:100px">
              <option value="auto">Auto</option>
              <option value="light">Claro</option>
              <option value="dark">Escuro</option>
            </select>
          </label>
          <label class="small" style="margin:0;display:flex;align-items:center;gap:6px">Modo:
            <select id="modeSelect" style="margin:0;min-width:120px">
              <option value="paper" selected>Simulação (Paper)</option>
              <option value="live">Real (Live)</option>
            </select>
          </label>
          <div class="status-badge">Status: <span id="botStatus">parado</span></div>
        </div>
      </header>
      <main style="flex:1;overflow-y:auto">
        <div class="container">
          <!-- RESUMO DE TODAS AS CONTAS -->
          <div id="allAccountsSummary" class="card grid-full" style="margin-bottom:var(--space-6);display:none">
            <h2>📊 Resumo de Todas as Contas</h2>
            <div class="grid grid-3" style="margin-top:var(--space-4)">
              <div class="stat-card">
                <div class="stat-label">Conta 1 (Paper)</div>
                <div class="stat-value" style="color:var(--accent)" id="account1Balance">R$ 0,00</div>
                <div class="small" id="account1Stats">0 ops | 0% acerto</div>
              </div>
              <div class="stat-card">
                <div class="stat-label">Conta 2 (Paper)</div>
                <div class="stat-value" style="color:var(--accent)" id="account2Balance">R$ 0,00</div>
                <div class="small" id="account2Stats">0 ops | 0% acerto</div>
              </div>
              <div class="stat-card">
                <div class="stat-label">Conta 3 (Live)</div>
                <div class="stat-value" style="color:var(--danger)" id="account3Balance">R$ 0,00</div>
                <div class="small" id="account3Stats">0 ops | 0% acerto</div>
              </div>
            </div>
            <div style="margin-top:var(--space-4);padding-top:var(--space-4);border-top:1px solid var(--border)">
              <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:var(--space-4)">
                <div>
                  <div class="stat-label">Total Investido</div>
                  <div class="stat-value" id="totalInvested">R$ 0,00</div>
                </div>
                <div>
                  <div class="stat-label">Lucro Total</div>
                  <div class="stat-value" style="color:var(--accent)" id="totalAllProfit">R$ 0,00</div>
                </div>
                <div>
                  <div class="stat-label">Retorno Total</div>
                  <div class="stat-value" id="totalReturn">0.00%</div>
                </div>
              </div>
            </div>
          </div>

          <div class="grid">
            <div class="card">
              <h2>Controle do Robô</h2>
              <div class="controls">
                <div class="control-group">
                  <label class="control-label">Par</label>
                  <input id="symbol" value="ADA/USDT" pattern="[A-Z]{2,}/[A-Z]{2,}" title="Use formato XXX/YYY" required maxlength="20" />
                  <small style="color:var(--muted);font-size:11px;margin-top:4px">Ex: BTC/USDT, ADA/USDT</small>
                </div>
                <div class="control-group">
                  <label class="control-label">Timeframe</label>
                  <select id="timeframe" required>
                    <option value="1m">1m</option>
                    <option value="5m" selected>5m</option>
                    <option value="15m">15m</option>
                    <option value="1h">1h</option>
                    <option value="4h">4h</option>
                    <option value="1d">1d</option>
                  </select>
                </div>
                <div class="control-group">
                  <label class="control-label">Payout (%)</label>
                  <input id="payout" type="number" min="1" max="100" step="0.1" value="{{ payout_ratio }}" required />
                  <small style="color:var(--muted);font-size:11px;margin-top:4px">Entre 1 e 100%</small>
                </div>
              </div>
              <div class="button-group">
                <button class="btn btn-primary" onclick="startBot()">▶ Iniciar</button>
                <button class="btn btn-danger" onclick="stopBot()">⏹ Parar</button>
              </div>
            </div>
            <div class="card">
              <h2>Conta</h2>
              <div class="stat-card" style="margin-bottom:var(--space-3)">
                <div class="stat-label">Saldo Inicial</div>
                <div class="stat-value" id="initialBalance">{{ initial_balance }}</div>
                <div class="small">BRL</div>
              </div>
              <div class="stat-card">
                <div class="stat-label">Saldo Atual</div>
                <div class="stat-value" id="currentBalance">{{ current_balance }}</div>
                <div class="small">BRL</div>
              </div>
            </div>
          </div>
          <div class="grid grid-3">
            <div class="stat-card">
              <div class="stat-label">Total de Operações</div>
              <div class="stat-value"><span id="opsCount" class="skeleton-line">{{ ops_count }}</span></div>
            </div>
            <div class="stat-card">
              <div class="stat-label">Ganhos</div>
              <div class="stat-value" style="color:var(--accent)"><span id="winsCount" class="skeleton-line">{{ wins }}</span></div>
            </div>
            <div class="stat-card">
              <div class="stat-label">Perdas</div>
              <div class="stat-value" style="color:var(--danger)"><span id="lossesCount" class="skeleton-line">{{ losses }}</span></div>
            </div>
          </div>
          <div class="card" style="margin-bottom:var(--space-6)">
            <h2>Lucro Total</h2>
            <div style="font-size:32px;font-weight:700;color:var(--accent)"><span id="totalProfit" class="skeleton-line">{{ total_profit }}</span> BRL</div>
          </div>
          <div class="card grid-full" style="margin-bottom:var(--space-6)">
            <h2 id="accountTitle">📊 Equity - Conta Selecionada</h2>
            <div style="margin-bottom:var(--space-3);padding:var(--space-4);background:rgba(22,163,74,0.1);border-radius:var(--radius-sm);display:none" id="accountInfo">
              <div style="font-size:13px;color:var(--muted)">
                <strong>Conta:</strong> <span id="accountName">-</span> | 
                <strong>Modo:</strong> <span id="accountMode">-</span> | 
                <strong>Saldo:</strong> <span id="accountBalance" style="color:var(--accent)">R$ 0,00</span>
              </div>
            </div>
            <div id="profitSkeleton" class="skeleton skeleton-chart" style="height:320px"></div>
            <canvas id="profitChart" height="320" style="display:none"></canvas>
          </div>
          <div class="card grid-full">
            <h2 id="candleTitle">💹 Candlestick - Conta Selecionada</h2>
            <div id="candleSkeleton" class="skeleton skeleton-chart" style="height:360px"></div>
            <canvas id="candleChart" height="360" style="display:none"></canvas>
          </div>
        </div>
      </main>
    </div>
  </div>

  <script>
  function navigateTo(page) {
    if (page === 'dashboard') {
      window.location.href = '/';
    } else if (page === 'operacoes') {
      window.location.href = '/operacoes';
    }
    return false;
  }
  
  function applyTheme(mode){
    const root = document.documentElement;
    if(mode === 'light'){
      root.setAttribute('data-theme','light');
    }else if(mode === 'dark'){
      root.setAttribute('data-theme','dark');
    }else{
      root.removeAttribute('data-theme');
    }
  }
  (function initTheme(){
    const select = document.getElementById('themeSelect');
    const saved = localStorage.getItem('theme') || 'auto';
    select.value = saved;
    applyTheme(saved);
    select.addEventListener('change', ()=>{
      const v = select.value;
      localStorage.setItem('theme', v);
      applyTheme(v);
    });
  })();
  
  // Inicializar seletor de ambiente Quotex
  (function initQuotexEnvironment(){
    const select = document.getElementById('quotexEnvironment');
    const saved = localStorage.getItem('quotexEnvironment') || 'demo';
    select.value = saved;
    currentQuotexEnvironment = saved;
    updateQuotexEnvironmentUI();
  })();

  async function startBot(){
    const symbolInput = document.getElementById('symbol');
    const timeframeInput = document.getElementById('timeframe');
    const payoutInput = document.getElementById('payout');
    const modeSelect = document.getElementById('modeSelect');
    
    const symbol = symbolInput.value.trim().toUpperCase();
    const timeframe = timeframeInput.value;
    const payout = parseFloat(payoutInput.value);
    
    // Validação de symbol
    if(!symbol || symbol.length < 6) {
      alert('❌ Par inválido! Digite um par válido (mínimo 6 caracteres)');
      symbolInput.focus();
      return;
    }
    if(!symbol.includes('/')) {
      alert('❌ Par inválido! Use o formato: XXX/YYY (ex: BTC/USDT, ADA/USDT)');
      symbolInput.focus();
      return;
    }
    const parts = symbol.split('/');
    if(parts.length !== 2 || parts[0].length < 2 || parts[1].length < 2) {
      alert('❌ Par inválido! Ambas as moedas devem ter pelo menos 2 caracteres');
      symbolInput.focus();
      return;
    }
    const symbolPattern = /^[A-Z]+\\/[A-Z]+$/;
    if(!symbolPattern.test(symbol)) {
      alert('❌ Par inválido! Use apenas letras maiúsculas separadas por /');
      symbolInput.focus();
      return;
    }
    
    // Validação de timeframe
    const validTF = ['1m','5m','15m','1h','4h','1d'];
    if(!timeframe || !validTF.includes(timeframe)) {
      alert('❌ Timeframe inválido! Escolha: 1m, 5m, 15m, 1h, 4h ou 1d');
      timeframeInput.focus();
      return;
    }
    
    // Validação de payout
    if(!payoutInput.value || payoutInput.value.trim() === '') {
      alert('❌ Payout não pode estar vazio!');
      payoutInput.focus();
      return;
    }
    if(isNaN(payout)) {
      alert('❌ Payout inválido! Digite um número válido');
      payoutInput.focus();
      return;
    }
    if(payout < 1) {
      alert('❌ Payout muito baixo! Deve ser no mínimo 1%');
      payoutInput.focus();
      return;
    }
    if(payout > 100) {
      alert('❌ Payout muito alto! Deve ser no máximo 100%');
      payoutInput.focus();
      return;
    }
    if(payout % 0.1 !== 0 && payout.toString().split('.')[1]?.length > 1) {
      alert('❌ Payout com muitas casas decimais! Use no máximo 1 casa decimal');
      payoutInput.focus();
      return;
    }
    
    try {
      const res = await fetch('/start', {
        method:'POST', 
        headers:{'Content-Type':'application/json'}, 
        body: JSON.stringify({symbol, timeframe, payout, mode: modeSelect ? modeSelect.value : 'paper'})
      });
      
      if(!res.ok) {
        throw new Error('Erro ao iniciar o bot');
      }
      
      const data = await res.json();
      document.getElementById('botStatus').textContent = data.status;
      if (data.mode) {
        document.getElementById('botStatus').textContent += ` (${data.mode})`;
      }
      
      if(data.status === 'rodando') {
        alert('✅ Bot iniciado com sucesso!');
      }
    } catch(error) {
      alert('❌ Erro ao iniciar o bot: ' + error.message);
      console.error('Erro:', error);
    }
  }
  async function stopBot(){
    try {
      const res = await fetch('/stop', {method:'POST'});
      
      if(!res.ok) {
        throw new Error('Erro ao parar o bot');
      }
      
      const data = await res.json();
      document.getElementById('botStatus').textContent = data.status;
      
      if(data.status === 'parado') {
        alert('✅ Bot parado com sucesso!');
      }
    } catch(error) {
      alert('❌ Erro ao parar o bot: ' + error.message);
      console.error('Erro:', error);
    }
  }
  // ===== GERENCIAMENTO DE MÚLTIPLAS CONTAS =====
  const accountsData = {
    all: { name: 'Todas as Contas', mode: 'mixed', initial: 3000, data: [] },
    account1: { name: 'Conta 1 (Paper)', mode: 'paper', initial: 1000, balance: 1000, profit: 0, ops: 0, wins: 0, losses: 0, data: [] },
    account2: { name: 'Conta 2 (Paper)', mode: 'paper', initial: 1000, balance: 1000, profit: 0, ops: 0, wins: 0, losses: 0, data: [] },
    account3: { name: 'Conta 3 (Live)', mode: 'live', initial: 1000, balance: 1000, profit: 0, ops: 0, wins: 0, losses: 0, data: [] }
  };
  
  let currentAccount = 'all';
  let currentQuotexEnvironment = 'demo'; // demo ou live
  
  // ===== GERENCIAMENTO DE AMBIENTE QUOTEX =====
  async function changeQuotexEnvironment(env) {
    const oldEnv = currentQuotexEnvironment;
    currentQuotexEnvironment = env;
    
    const select = document.getElementById('quotexEnvironment');
    
    // Mostrar aviso se mudar para LIVE
    if (env === 'live') {
      const confirmChange = confirm(
        '⚠️ AVISO IMPORTANTE!\n\n' +
        'Você está prestes a trocar para a conta REAL da Quotex.\n\n' +
        '❌ Isso significa que você operará COM DINHEIRO REAL\n' +
        '❌ Operações perdidas resultarão em perda REAL de dinheiro\n' +
        '❌ Você é totalmente responsável pelas operações\n\n' +
        '✅ Tem certeza que deseja continuar?\n\n' +
        '(Recomendamos usar DEMO até validar sua estratégia)'
      );
      
      if (!confirmChange) {
        currentQuotexEnvironment = oldEnv;
        select.value = oldEnv;
        alert('❌ Mudança cancelada. Continuando com: ' + oldEnv.toUpperCase());
        return;
      }
    }
    
    try {
      const res = await fetch('/set-quotex-environment', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ environment: env })
      });
      
      if (!res.ok) {
        throw new Error('Erro ao mudar ambiente Quotex');
      }
      
      const data = await res.json();
      
      if (data.status === 'success') {
        if (env === 'live') {
          alert('✅ Ambiente alterado para REAL (Conta Quotex Real)\n\n' +
                '⚠️ LEMBRE-SE: Operações agora afetam sua conta real!\n' +
                '📊 Monitore constantemente!');
        } else {
          alert('✅ Ambiente alterado para DEMO (Conta Demo Quotex Segura)');
        }
        
        // Atualizar estilo do seletor
        updateQuotexEnvironmentUI();
      } else {
        throw new Error(data.message || 'Erro desconhecido');
      }
    } catch (error) {
      alert('❌ Erro ao mudar ambiente: ' + error.message);
      currentQuotexEnvironment = oldEnv;
      select.value = oldEnv;
      updateQuotexEnvironmentUI();
    }
  }
  
  function updateQuotexEnvironmentUI() {
    const select = document.getElementById('quotexEnvironment');
    if (currentQuotexEnvironment === 'live') {
      select.style.borderColor = '#ef4444';
      select.style.background = 'rgba(239,68,68,0.1)';
      select.style.color = '#ef4444';
    } else {
      select.style.borderColor = 'var(--border)';
      select.style.background = '#0b1220';
      select.style.color = 'var(--text)';
    }
  }
  
  function switchAccount(accountId) {
    currentAccount = accountId;
    const summaryDiv = document.getElementById('allAccountsSummary');
    const infoDiv = document.getElementById('accountInfo');
    
    if (accountId === 'all') {
      summaryDiv.style.display = 'block';
      infoDiv.style.display = 'none';
      document.getElementById('accountTitle').textContent = '📊 Equity - Todas as Contas';
      document.getElementById('candleTitle').textContent = '💹 Candlestick - Consolidado';
      updateAllAccountsSummary();
    } else {
      summaryDiv.style.display = 'none';
      infoDiv.style.display = 'block';
      const account = accountsData[accountId];
      document.getElementById('accountTitle').textContent = `📊 Equity - ${account.name}`;
      document.getElementById('candleTitle').textContent = `💹 Candlestick - ${account.name}`;
      document.getElementById('accountName').textContent = account.name;
      document.getElementById('accountMode').textContent = account.mode.toUpperCase();
      document.getElementById('accountBalance').textContent = `R$ ${account.balance.toFixed(2)}`;
    }
    
    updateCharts();
  }
  
  function updateAllAccountsSummary() {
    // Atualizar dados de cada conta individualmente
    Object.keys(accountsData).forEach(key => {
      if (key === 'all') return;
      const account = accountsData[key];
      const returnPct = ((account.balance - account.initial) / account.initial * 100).toFixed(2);
      const winRate = account.ops > 0 ? ((account.wins / account.ops) * 100).toFixed(1) : 0;
      
      document.getElementById(`${key}Balance`).textContent = `R$ ${account.balance.toFixed(2)}`;
      document.getElementById(`${key}Stats`).textContent = `${account.ops} ops | ${winRate}% acerto`;
    });
    
    // Totais
    const totalInvested = Object.keys(accountsData)
      .filter(k => k !== 'all')
      .reduce((sum, k) => sum + accountsData[k].initial, 0);
    const totalBalance = Object.keys(accountsData)
      .filter(k => k !== 'all')
      .reduce((sum, k) => sum + accountsData[k].balance, 0);
    const totalProfit = totalBalance - totalInvested;
    const totalReturn = ((totalProfit / totalInvested) * 100).toFixed(2);
    
    document.getElementById('totalInvested').textContent = `R$ ${totalInvested.toFixed(2)}`;
    document.getElementById('totalAllProfit').textContent = `R$ ${totalProfit.toFixed(2)}`;
    document.getElementById('totalReturn').textContent = `${totalReturn}%`;
  }
  
  let profitChart;
  function renderCharts(equity){
    const pc = document.getElementById('profitChart');
    if(!pc) return;
    
    if(!equity || equity.length === 0) {
      equity = [0];
    }
    
    const labels = equity.map((_,i)=>i+1);
    const profits = equity;
    
    if(!profitChart){
      profitChart = new Chart(pc, {
        type:'line', 
        data:{
          labels, 
          datasets:[{
            label:'Equity (BRL)', 
            data:profits, 
            borderColor:'#16a34a', 
            backgroundColor:'rgba(22,163,74,0.1)', 
            fill:true, 
            tension:0.3, 
            pointRadius:0,
            pointHoverRadius:6,
            pointHoverBackgroundColor:'#16a34a',
            pointHoverBorderColor:'#fff',
            pointHoverBorderWidth:2,
            borderWidth:3,
            segment: {
              borderColor: ctx => {
                const prev = ctx.p0.parsed.y;
                const curr = ctx.p1.parsed.y;
                return curr >= prev ? '#16a34a' : '#ef4444';
              }
            }
          }]
        }, 
        options:{
          responsive:true, 
          maintainAspectRatio:false, 
          animation: {
            duration: 750
          },
          plugins:{
            legend:{
              display:true, 
              position:'top', 
              labels:{
                font:{size:14, weight:'600'}, 
                padding:20,
                usePointStyle:true,
                boxWidth:8,
                boxHeight:8
              }
            },
            tooltip:{
              enabled:true,
              mode:'index',
              intersect:false,
              backgroundColor:'rgba(17,24,39,0.98)',
              titleColor:'#e5e7eb',
              titleFont:{size:13, weight:'600'},
              bodyColor:'#e5e7eb',
              bodyFont:{size:13},
              borderColor:'#16a34a',
              borderWidth:2,
              padding:16,
              displayColors:true,
              boxWidth:10,
              boxHeight:10,
              boxPadding:6,
              callbacks:{
                title: function(items){
                  return 'Operação #' + items[0].label;
                },
                label: function(context){
                  const value = context.parsed.y;
                  const color = value >= 0 ? '🟢' : '🔴';
                  return color + ' Equity: R$ ' + value.toFixed(2);
                }
              }
            }
          }, 
          scales:{
            y:{
              type:'linear',
              beginAtZero:true,
              ticks:{
                font:{size:12, weight:'500'}, 
                padding:8,
                callback: function(value){
                  return 'R$ ' + value.toFixed(0);
                }
              }, 
              grid:{
                color:'rgba(31,41,55,0.4)', 
                drawBorder:false,
                lineWidth:1
              },
              border:{
                display:false
              }
            }, 
            x:{
              ticks:{
                font:{size:12, weight:'500'},
                padding:8,
                maxTicksLimit:12,
                autoSkip:true
              }, 
              grid:{
                display:false, 
                drawBorder:false
              },
              border:{
                display:false
              }
            }
          }, 
          interaction:{
            mode:'nearest', 
            intersect:false,
            axis:'x'
          }
        }
      });
    } else {
      profitChart.data.labels = labels;
      profitChart.data.datasets[0].data = profits;
      profitChart.update('none');
    }
  }
  let candleChart;
  function renderCandle(candles){
    const el = document.getElementById('candleChart');
    if(!el) return;
    
    const data = candles && candles.length > 0 ? candles : [];
    
    const ds = [{
      label: 'Preço (OHLC)', 
      data, 
      upColor: 'rgba(22,163,74,0.8)', 
      downColor: 'rgba(239,68,68,0.8)', 
      borderColor: '#6b7280', 
      borderWidth:1,
      upBorderColor: '#16a34a',
      downBorderColor: '#ef4444'
    }];
    
    const options = { 
      parsing: false, 
      responsive:true, 
      maintainAspectRatio:false,
      animation: {
        duration: 500
      },
      plugins: {
        legend: {
          display:true, 
          position:'top', 
          labels:{
            font:{size:14, weight:'600'}, 
            padding:20,
            usePointStyle:true,
            boxWidth:12,
            boxHeight:12
          }
        },
        tooltip:{
          enabled:true,
          mode:'index',
          intersect:false,
          backgroundColor:'rgba(17,24,39,0.98)',
          titleColor:'#e5e7eb',
          titleFont:{size:13, weight:'600'},
          bodyColor:'#e5e7eb',
          bodyFont:{size:12},
          borderColor:'#16a34a',
          borderWidth:2,
          padding:16,
          displayColors:false,
          callbacks:{
            title: function(items){
              return 'Candle #' + items[0].dataIndex;
            },
            label: function(context){
              const d = context.raw;
              if(!d || !d.o) return '';
              const diff = d.c - d.o;
              const percent = ((diff / d.o) * 100).toFixed(2);
              const arrow = diff >= 0 ? '📈' : '📉';
              return [
                arrow + ' Variação: ' + percent + '%',
                '',
                '🟢 Abertura: R$ ' + d.o.toFixed(2),
                '🔴 Fechamento: R$ ' + d.c.toFixed(2),
                '⬆️  Máxima: R$ ' + d.h.toFixed(2),
                '⬇️  Mínima: R$ ' + d.l.toFixed(2)
              ];
            }
          }
        }
      }, 
      scales: { 
        x: { 
          type: 'linear',
          offset: true,
          ticks:{
            font:{size:12, weight:'500'},
            padding:8,
            maxTicksLimit:10,
            autoSkip:true
          }, 
          grid:{
            display:false, 
            drawBorder:false
          },
          border:{
            display:false
          }
        }, 
        y:{
          position:'right',
          ticks:{
            font:{size:12, weight:'500'},
            padding:8,
            callback: function(value){
              return 'R$ ' + value.toFixed(2);
            }
          }, 
          grid:{
            color:'rgba(31,41,55,0.4)', 
            drawBorder:false,
            lineWidth:1
          },
          border:{
            display:false
          }
        } 
      }, 
      interaction:{
        mode:'nearest', 
        intersect:false,
        axis:'x'
      } 
    };
    
    if(!candleChart){
      candleChart = new Chart(el.getContext('2d'), { 
        type: 'candlestick', 
        data:{ datasets: ds }, 
        options 
      });
    } else {
      candleChart.data.datasets[0].data = data;
      candleChart.update('none');
    }
  }
  function setLoading(loading){
    const profitSkeleton = document.getElementById('profitSkeleton');
    const candleSkeleton = document.getElementById('candleSkeleton');
    const profitCanvas = document.getElementById('profitChart');
    const candleCanvas = document.getElementById('candleChart');
    if(profitSkeleton) profitSkeleton.style.display = loading ? 'block' : 'none';
    if(candleSkeleton) candleSkeleton.style.display = loading ? 'block' : 'none';
    if(profitCanvas) profitCanvas.style.display = loading ? 'none' : 'block';
    if(candleCanvas) candleCanvas.style.display = loading ? 'none' : 'block';
    ['opsCount','winsCount','lossesCount','totalProfit','currentBalance'].forEach(id=>{
      const el = document.getElementById(id);
      if(el){ el.classList.toggle('skeleton-line', loading); }
    });
  }
  
  function updateCharts() {
    // Atualizar gráficos com base na conta selecionada
    const account = accountsData[currentAccount];
    if (currentAccount === 'all') {
      // Consolidar dados de todas as contas
      let allEquity = [];
      Object.keys(accountsData).forEach(key => {
        if (key !== 'all' && accountsData[key].data && accountsData[key].data.length > 0) {
          allEquity = allEquity.concat(accountsData[key].data);
        }
      });
      renderCharts(allEquity.length > 0 ? allEquity : []);
    } else {
      // Mostrar dados da conta individual
      renderCharts(account.data && account.data.length > 0 ? account.data : []);
    }
  }
  
  setLoading(true);
  async function loadSummary(){
    const res = await fetch('/summary');
    const s = await res.json();
    document.getElementById('botStatus').textContent = s.bot.status;
    
    // Atualizar dados da conta atual
    const account = accountsData[currentAccount];
    if (currentAccount !== 'all' && account) {
      account.balance = s.account.balance_brl || account.initial;
      account.profit = account.balance - account.initial;
      account.ops = s.ops_count || 0;
      account.wins = s.wins || 0;
      account.losses = s.losses || 0;
      account.data = s.equity_curve || [];
    }
    
    // Atualizar elementos da UI
    if(currentAccount !== 'all') {
      document.getElementById('currentBalance').textContent = fmt(account.balance);
    }
    
    const oc = document.getElementById('opsCount'); if(oc) oc.textContent = s.ops_count;
    const wc = document.getElementById('winsCount'); if(wc) wc.textContent = s.wins;
    const lc = document.getElementById('lossesCount'); if(lc) lc.textContent = s.losses;
    const tp = document.getElementById('totalProfit'); if(tp) tp.textContent = fmt(s.total_profit);
    
    // Se seleção for "todas as contas", atualizar resumo
    if(currentAccount === 'all') {
      updateAllAccountsSummary();
    }
    
    updateCharts();
    renderCandle(s.candles || []);
    setLoading(false);
  }
  setInterval(loadSummary, 2000);
  loadSummary();
  </script>
</body>
</html>
"""

app = Flask(
  __name__,
  static_folder=str(Path(__file__).resolve().parent / 'static'),
  static_url_path='/static'
)

DATA_FILE = Path("data/martingale_operations.csv")

class BotRunner:
  def __init__(self):
    self.thread: threading.Thread | None = None
    self.stop_event = threading.Event()
    self.status = 'parado'
    self.symbol = 'ADA/USDT'
    self.timeframe = '1h'
    self.equity_curve: List[float] = []
    self.win_loss_series: List[int] = []
    self.balance_brl = settings.initial_balance_brl
    self.candles: List[List[float]] = []
    self.candle_progress: int = 0

  def start(self, symbol: str, timeframe: str, mode: str = 'paper'):
    if self.thread and self.thread.is_alive():
      return
    self.stop_event.clear()
    self.status = 'rodando'
    self.symbol = symbol
    self.timeframe = timeframe
    self.mode = mode
    try:
      from .broker import create_broker_from_settings
      self.broker = create_broker_from_settings(settings) if mode in ('paper','live') else None
      
      # Tentar buscar saldo inicial da conta Quotex
      if self.broker and mode == 'live':
        try:
          balance_info = self.broker.get_balance()
          if balance_info and 'balance' in balance_info:
            self.balance_brl = balance_info['balance']
        except Exception:
          self.balance_brl = settings.initial_balance_brl
      else:
        self.balance_brl = settings.initial_balance_brl
    except Exception:
      self.broker = None
      self.balance_brl = settings.initial_balance_brl
    self.thread = threading.Thread(target=self.run_loop, daemon=True)
    self.thread.start()

  def stop(self):
    self.stop_event.set()
    self.status = 'parado'

  def run_loop(self):
    headers, rows = load_csv(DATA_FILE)
    total_profit = sum(float(r.get('profit_brl', 0) or 0) for r in rows)
    self.equity_curve = [sum(float(rows[i].get('profit_brl',0) or 0) for i in range(j+1)) for j in range(len(rows))]
    self.win_loss_series = [1 if str(r.get('win')).lower() in ('true','1') else -1 for r in rows]

    candles: List[List[float]] = []
    if ccxt:
      try:
        ex = ccxt.binance({'enableRateLimit': True})
        candles = ex.fetch_ohlcv(self.symbol, timeframe=self.timeframe, limit=300)
      except Exception:
        candles = []
    if not candles:
      candles = [[0,10,11,9,11],[0,10,11,9,9]] * 300

    self.candles = candles
    self.candle_progress = 0

    stake_seq = [2,4,10,20,50,100,200,400]
    stake_index = 0
    current_dir = None
    def candle_dir(open_, close_):
      return 'green' if close_ >= open_ else 'red'

    for i in range(1, len(candles)):
      if self.stop_event.is_set():
        break
      prev = candles[i-1]
      cur = candles[i]
      prev_dir = candle_dir(prev[1], prev[4])
      this_dir = candle_dir(cur[1], cur[4])
      if current_dir is None:
        current_dir = prev_dir
        stake_index = 0
      stake = stake_seq[stake_index]
      win = (this_dir == current_dir)
      profit = stake if win else -stake
      total_profit += profit
      # Try place order via broker in paper/live
      try:
        if getattr(self, 'broker', None) and getattr(self, 'mode', 'paper') in ('paper','live'):
          side = 'CALL' if current_dir == 'green' else 'PUT'
          exp = int(os.getenv('EXPIRATION_TIME', '60'))
          self.broker.place_order(self.symbol, side, float(stake), expiration_time=exp)
      except Exception:
        pass
      append_row({
        'index': i,
        'entry_direction': current_dir,
        'candle_direction': this_dir,
        'stake_brl': stake,
        'win': win,
        'profit_brl': profit,
      })
      self.equity_curve.append(total_profit)
      self.win_loss_series.append(1 if win else -1)
      if win:
        current_dir = None
        stake_index = 0
      else:
        stake_index += 1
        if stake_index >= len(stake_seq):
          current_dir = None
          stake_index = 0
      self.candle_progress = i + 1
      time.sleep(1.0)

    self.status = 'parado'


def load_csv(path: Path):
  if not path.exists():
    return [], []
  with path.open("r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    headers = reader.fieldnames or []
    return headers, rows

def append_row(row: Dict[str, Any]):
  exists = DATA_FILE.exists()
  with DATA_FILE.open('a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(row.keys()))
    if not exists:
      writer.writeheader()
    writer.writerow(row)

runner = BotRunner()

@app.route("/")
def index():
    headers, rows = load_csv(DATA_FILE)
    wins = sum(1 for r in rows if str(r.get("win")).lower() in ("true", "1"))
    losses = len(rows) - wins
    total_profit = sum(float(r.get("profit_brl", 0) or 0) for r in rows)
    rows_tail = rows[-200:] if len(rows) > 200 else rows
    return render_template_string(
        TEMPLATE,
        headers=headers or ["index","entry_direction","candle_direction","stake_brl","win","profit_brl"],
        rows=rows_tail,
        ops_count=len(rows),
        wins=wins,
        losses=losses,
        total_profit=f"{total_profit:.2f}",
        initial_balance=f"{settings.initial_balance_brl:.2f}",
        current_balance=f"{runner.balance_brl:.2f}",
        payout_ratio=f"{settings.payout_ratio:.2f}",
    )

@app.route('/start', methods=['POST'])
def start():
    data = request.get_json(force=True)
    symbol = data.get('symbol', 'ADA/USDT')
    timeframe = data.get('timeframe', '5m')
    payout = data.get('payout', None)
    mode = data.get('mode', 'paper')
    if isinstance(payout, (int, float)):
        try:
            from .config import settings as _settings
            _settings.payout_ratio = float(payout)
        except Exception:
            pass
    runner.start(symbol, timeframe, mode)
    return jsonify({'status': runner.status, 'symbol': runner.symbol, 'timeframe': runner.timeframe, 'mode': mode, 'payout': float(payout) if payout is not None else settings.payout_ratio})

@app.route('/stop', methods=['POST'])
def stop():
    runner.stop()
    return jsonify({'status': runner.status})

@app.route('/configuracoes')
def configuracoes():
    # Carregar configurações atuais do .env
    env_path = Path(__file__).parent.parent / '.env'
    env_vars = {}
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    
    quotex_email = env_vars.get('QUOTEX_EMAIL', '')
    quotex_password = env_vars.get('QUOTEX_PASSWORD', '')
    quotex_lang = env_vars.get('QUOTEX_LANG', 'pt')
    initial_balance = env_vars.get('INITIAL_BALANCE_BRL', '5')
    
    return render_template_string(f"""
<!doctype html>
<html lang="pt-br">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Configurações - Robo Trade</title>
  <style>
    :root{{--bg:#0f172a;--panel:#0b1220;--card:#111827;--text:#e5e7eb;--muted:#9ca3af;--border:#1f2937;--accent:#16a34a;--accent-600:#22c55e;--accent-light:rgba(22,163,74,0.1);--danger:#ef4444;--space-2:8px;--space-3:12px;--space-4:16px;--space-5:20px;--space-6:24px;--radius:12px;--radius-sm:8px;--radius-xs:6px;--shadow:0 4px 12px rgba(0,0,0,0.3);--shadow-lg:0 12px 32px rgba(0,0,0,0.4)}}
    *{{box-sizing:border-box}}html,body{{height:100%}}body{{margin:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Inter,Arial,sans-serif;background:var(--bg);color:var(--text);-webkit-font-smoothing:antialiased;color-scheme:light dark;line-height:1.5}}
    .layout{{display:grid;grid-template-columns:260px 1fr;height:100vh;gap:0}}
    aside{{background:var(--panel);border-right:1px solid var(--border);padding:var(--space-6) var(--space-4);display:flex;flex-direction:column;overflow-y:auto}}
    .brand{{font-weight:700;font-size:20px;letter-spacing:-0.5px;margin-bottom:var(--space-6);color:var(--text)}}.brand::before{{content:'⚡';display:inline-block;margin-right:8px}}
    .nav{{flex:1}}.nav a{{display:flex;align-items:center;color:var(--muted);text-decoration:none;padding:10px var(--space-3);border-radius:var(--radius-xs);transition:all .2s ease;font-size:14px;gap:8px}}.nav a.active{{background:var(--accent-light);color:var(--accent);font-weight:600}}.nav a:hover{{background:rgba(22,163,74,0.2);color:var(--text)}}
    header{{display:flex;align-items:center;justify-content:space-between;padding:16px 24px;border-bottom:1px solid var(--border);background:var(--panel);position:sticky;top:0;z-index:10;box-shadow:var(--shadow)}}
    .header-title{{font-size:18px;font-weight:700;letter-spacing:-0.3px}}
    main{{padding:var(--space-6);overflow:auto;background:linear-gradient(135deg,var(--bg) 0%,#1a2340 100%)}}
    .container{{max-width:900px;margin:0 auto}}
    .card{{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:var(--space-6);box-shadow:var(--shadow)}}
    h2{{margin:0 0 var(--space-4) 0;font-size:16px;font-weight:700;letter-spacing:-0.3px;color:var(--text)}}
    .form-group{{margin-bottom:var(--space-5)}}
    label{{font-size:13px;font-weight:600;color:var(--text);display:block;margin-bottom:8px}}
    .label-hint{{font-size:12px;color:var(--muted);font-weight:400;margin-left:4px}}
    input,select{{background:#0b1220;border:1px solid var(--border);color:var(--text);padding:12px 14px;border-radius:var(--radius-xs);outline:none;transition:all .2s ease;font-size:14px;width:100%}}
    input:focus,select:focus{{border-color:var(--accent);box-shadow:0 0 0 3px rgba(22,163,74,0.1)}}
    .btn{{padding:12px 24px;border:none;border-radius:var(--radius-xs);font-weight:600;cursor:pointer;transition:all .2s ease;font-size:14px}}
    .btn-primary{{background:var(--accent);color:#0b141e}}.btn-primary:hover{{background:var(--accent-600);transform:translateY(-2px)}}
    .btn-secondary{{background:var(--border);color:var(--text)}}.btn-secondary:hover{{background:#273244}}
    .back-btn{{display:inline-block;margin-bottom:var(--space-6);padding:10px 16px;background:var(--accent);color:#0b141e;border-radius:var(--radius-xs);font-weight:600;text-decoration:none;transition:all .2s ease}}.back-btn:hover{{background:var(--accent-600);transform:translateY(-2px)}}
    .alert{{padding:var(--space-4);border-radius:var(--radius-sm);margin-bottom:var(--space-5);border-left:4px solid}}
    .alert-info{{background:rgba(59,130,246,0.1);border-color:#3b82f6;color:#93c5fd}}
    .alert-success{{background:var(--accent-light);border-color:var(--accent);color:var(--accent-600)}}
    .alert-error{{background:rgba(239,68,68,0.1);border-color:var(--danger);color:#fca5a5}}
    .btn-group{{display:flex;gap:var(--space-3);margin-top:var(--space-6)}}
    @media(max-width:1024px){{.layout{{grid-template-columns:1fr}}aside{{display:none}}}}
  </style>
</head>
<body>
  <div class="layout">
    <aside>
      <div class="brand">Robo Trade</div>
      <nav class="nav">
        <a href="/" onclick="return navigateTo('dashboard')">📊 Dashboard</a>
        <a href="/operacoes" onclick="return navigateTo('operacoes')">📈 Operações</a>
        <a class="active" href="/configuracoes" onclick="return navigateTo('configuracoes')">⚙️ Configurações</a>
      </nav>
    </aside>
    <div style="display:flex;flex-direction:column;height:100vh">
      <header>
        <div class="header-title">⚙️ Configurações</div>
      </header>
      <main style="flex:1;overflow-y:auto">
        <div class="container">
          <a href="/" class="back-btn">← Voltar para Dashboard</a>
          
          <div class="card">
            <h2>🔑 Credenciais Quotex</h2>
            <div class="alert alert-info">
              <strong>📌 Importante:</strong> Use o email e senha da sua conta Quotex para conectar o bot.
              O bot utiliza a biblioteca PyQuotex oficial para se conectar à plataforma.
            </div>
            
            <form id="configForm" onsubmit="return saveConfig(event)">
              <div class="form-group">
                <label>Email <span class="label-hint">(Email da sua conta Quotex)</span></label>
                <input type="email" id="email" name="email" value="{quotex_email}" placeholder="seu@email.com" required>
              </div>
              
              <div class="form-group">
                <label>Senha <span class="label-hint">(Senha da sua conta Quotex)</span></label>
                <input type="password" id="password" name="password" value="{quotex_password}" placeholder="Sua senha" required>
              </div>
              
              <div class="form-group">
                <label>Idioma <span class="label-hint">(Idioma da interface Quotex)</span></label>
                <select id="lang" name="lang" required>
                  <option value="pt" {'selected' if quotex_lang == 'pt' else ''}>Português (pt)</option>
                  <option value="en" {'selected' if quotex_lang == 'en' else ''}>English (en)</option>
                  <option value="es" {'selected' if quotex_lang == 'es' else ''}>Español (es)</option>
                </select>
              </div>
              
              <div class="form-group">
                <label>Saldo Inicial (R$) <span class="label-hint">(Usado em modo demo/paper)</span></label>
                <input type="number" id="initialBalance" name="initialBalance" value="{initial_balance}" placeholder="100" step="0.01" min="0" required>
              </div>
              
              <div class="btn-group">
                <button type="submit" class="btn btn-primary">💾 Salvar Configurações</button>
                <button type="button" class="btn btn-secondary" onclick="testConnection()">🔌 Testar Conexão</button>
              </div>
            </form>
            
            <div id="message" style="margin-top:var(--space-5);display:none"></div>
          </div>
        </div>
      </main>
    </div>
  </div>

  <script>
  function navigateTo(page) {{
    if (page === 'dashboard') {{
      window.location.href = '/';
    }} else if (page === 'operacoes') {{
      window.location.href = '/operacoes';
    }} else if (page === 'configuracoes') {{
      window.location.href = '/configuracoes';
    }}
    return false;
  }}
  
  async function saveConfig(e) {{
    e.preventDefault();
    const formData = {{
      email: document.getElementById('email').value,
      password: document.getElementById('password').value,
      lang: document.getElementById('lang').value,
      initialBalance: document.getElementById('initialBalance').value
    }};
    
    try {{
      const response = await fetch('/save-config', {{
        method: 'POST',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify(formData)
      }});
      
      const result = await response.json();
      const msgDiv = document.getElementById('message');
      msgDiv.style.display = 'block';
      
      if (result.status === 'success') {{
        msgDiv.className = 'alert alert-success';
        msgDiv.innerHTML = '<strong>✅ Sucesso!</strong> ' + result.message;
        setTimeout(() => {{ msgDiv.style.display = 'none'; }}, 5000);
      }} else {{
        msgDiv.className = 'alert alert-error';
        msgDiv.innerHTML = '<strong>❌ Erro!</strong> ' + result.message;
      }}
    }} catch (error) {{
      const msgDiv = document.getElementById('message');
      msgDiv.style.display = 'block';
      msgDiv.className = 'alert alert-error';
      msgDiv.innerHTML = '<strong>❌ Erro!</strong> ' + error.message;
    }}
    
    return false;
  }}
  
  async function testConnection() {{
    const msgDiv = document.getElementById('message');
    msgDiv.style.display = 'block';
    msgDiv.className = 'alert alert-info';
    msgDiv.innerHTML = '🔄 Testando conexão com Quotex...';
    
    try {{
      const response = await fetch('/test-quotex-connection');
      const result = await response.json();
      
      if (result.status === 'success') {{
        msgDiv.className = 'alert alert-success';
        msgDiv.innerHTML = '<strong>✅ Conexão OK!</strong> Saldo: R$ ' + (result.balance || '0.00');
      }} else {{
        msgDiv.className = 'alert alert-error';
        msgDiv.innerHTML = '<strong>❌ Falha na Conexão!</strong> ' + (result.message || 'Erro desconhecido');
      }}
    }} catch (error) {{
      msgDiv.className = 'alert alert-error';
      msgDiv.innerHTML = '<strong>❌ Erro!</strong> ' + error.message;
    }}
  }}
  </script>
</body>
</html>
    """)

@app.route('/save-config', methods=['POST'])
def save_config():
    try:
        data = request.get_json()
        email = data.get('email', '')
        password = data.get('password', '')
        lang = data.get('lang', 'pt')
        initial_balance = data.get('initialBalance', '5')
        
        # Validações
        if not email or not password:
            return jsonify({{
                'status': 'error',
                'message': 'Email e senha são obrigatórios'
            }}), 400
        
        # Atualizar arquivo .env
        env_path = Path(__file__).parent.parent / '.env'
        env_lines = []
        
        # Ler linhas existentes
        if env_path.exists():
            with open(env_path, 'r', encoding='utf-8') as f:
                env_lines = f.readlines()
        
        # Atualizar ou adicionar variáveis
        updated_vars = {{
            'QUOTEX_EMAIL': email,
            'QUOTEX_PASSWORD': password,
            'QUOTEX_LANG': lang,
            'INITIAL_BALANCE_BRL': initial_balance
        }}
        
        new_lines = []
        updated_keys = set()
        
        for line in env_lines:
            line_stripped = line.strip()
            if line_stripped and not line_stripped.startswith('#') and '=' in line_stripped:
                key = line_stripped.split('=', 1)[0].strip()
                if key in updated_vars:
                    new_lines.append(f"{{key}}={{updated_vars[key]}}\n")
                    updated_keys.add(key)
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        
        # Adicionar variáveis que não existiam
        for key, value in updated_vars.items():
            if key not in updated_keys:
                new_lines.append(f"{{key}}={{value}}\n")
        
        # Escrever arquivo
        with open(env_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        # Recarregar configurações
        settings.reload()
        
        return jsonify({{
            'status': 'success',
            'message': 'Configurações salvas com sucesso! Reinicie o bot para aplicar as mudanças.'
        }})
    except Exception as e:
        return jsonify({{
            'status': 'error',
            'message': f'Erro ao salvar configurações: {{str(e)}}'
        }}), 500

@app.route('/test-quotex-connection')
def test_quotex_connection():
    try:
        from .broker import create_broker_from_settings
        broker = create_broker_from_settings(settings)
        balance_info = broker.get_balance()
        
        if balance_info and 'balance' in balance_info:
            return jsonify({{
                'status': 'success',
                'balance': balance_info['balance'],
                'message': 'Conexão estabelecida com sucesso'
            }})
        else:
            return jsonify({{
                'status': 'error',
                'message': 'Não foi possível obter o saldo da conta'
            }}), 400
    except Exception as e:
        return jsonify({{
            'status': 'error',
            'message': f'Erro na conexão: {{str(e)}}'
        }}), 500

@app.route('/set-quotex-environment', methods=['POST'])
def set_quotex_environment():
    data = request.get_json(force=True)
    env = data.get('environment', 'demo')
    
    if env not in ('demo', 'live'):
        return jsonify({'status': 'error', 'message': 'Ambiente inválido. Use "demo" ou "live"'}), 400
    
    try:
        # Atualizar as configurações
        settings.quotex_environment = env
        
        # Também atualizar a variável de ambiente para próximas sessões
        import os
        os.environ['QUOTEX_ENVIRONMENT'] = env
        
        # Se há um broker já inicializado, recriar com o novo ambiente
        if hasattr(runner, 'broker') and runner.broker:
            from .broker import create_broker_from_settings
            runner.broker = create_broker_from_settings(settings)
        
        import logging
        logging.info(f"Ambiente Quotex alterado para: {env}")
        
        return jsonify({
            'status': 'success',
            'environment': env,
            'message': f'Ambiente alterado para {env.upper()}'
        })
    except Exception as e:
        import logging
        logging.error(f"Erro ao mudar ambiente Quotex: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Erro ao mudar ambiente: {str(e)}'
        }), 500

@app.route('/operacoes')
def operacoes():
    return render_template_string("""
<!doctype html>
<html lang="pt-br">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Operações - Robo Trade</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/chartjs-chart-financial@4.3.0/dist/chartjs-chart-financial.min.js"></script>
  <style>
    :root{--bg:#0f172a;--panel:#0b1220;--card:#111827;--text:#e5e7eb;--muted:#9ca3af;--border:#1f2937;--accent:#16a34a;--accent-600:#22c55e;--accent-light:rgba(22,163,74,0.1);--danger:#ef4444;--space-2:8px;--space-3:12px;--space-4:16px;--space-5:20px;--space-6:24px;--radius:12px;--radius-sm:8px;--radius-xs:6px;--shadow:0 4px 12px rgba(0,0,0,0.3);--shadow-lg:0 12px 32px rgba(0,0,0,0.4)}
    *{box-sizing:border-box}html,body{height:100%}body{margin:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Inter,Arial,sans-serif;background:var(--bg);color:var(--text);-webkit-font-smoothing:antialiased;color-scheme:light dark;line-height:1.5}
    .layout{display:grid;grid-template-columns:260px 1fr;height:100vh;gap:0}
    aside{background:var(--panel);border-right:1px solid var(--border);padding:var(--space-6) var(--space-4);display:flex;flex-direction:column;overflow-y:auto}
    .brand{font-weight:700;font-size:20px;letter-spacing:-0.5px;margin-bottom:var(--space-6);color:var(--text)}.brand::before{content:'⚡';display:inline-block;margin-right:8px}
    .nav{flex:1}.nav a{display:flex;align-items:center;color:var(--muted);text-decoration:none;padding:10px var(--space-3);border-radius:var(--radius-xs);transition:all .2s ease;font-size:14px;gap:8px}.nav a.active{background:var(--accent-light);color:var(--accent);font-weight:600}.nav a:hover{background:rgba(22,163,74,0.2);color:var(--text)}
    header{display:flex;align-items:center;justify-content:space-between;padding:16px 24px;border-bottom:1px solid var(--border);background:var(--panel);position:sticky;top:0;z-index:10;box-shadow:var(--shadow)}
    .header-title{font-size:18px;font-weight:700;letter-spacing:-0.3px}
    main{padding:var(--space-6);overflow:auto;background:linear-gradient(135deg,var(--bg) 0%,#1a2340 100%)}
    .container{max-width:1400px;margin:0 auto}
    .card{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:var(--space-6);box-shadow:var(--shadow);margin-bottom:var(--space-6)}
    h2{margin:0 0 var(--space-4) 0;font-size:16px;font-weight:700;letter-spacing:-0.3px;color:var(--text)}
    table{width:100%;border-collapse:separate;border-spacing:0;font-size:13px}
    th{background:linear-gradient(180deg,#0f1a2e 0%,#0b1220 100%);padding:12px;text-align:left;vertical-align:middle;font-weight:700;text-transform:uppercase;font-size:11px;letter-spacing:0.5px;border-bottom:2px solid var(--border);position:sticky;top:0;z-index:1}
    td{padding:12px;border-bottom:1px solid var(--border);color:var(--text)}
    tbody tr:hover{background:rgba(22,163,74,0.08)}
    tbody tr:nth-child(even){background:rgba(14,22,40,0.5)}
    .stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:var(--space-4)}
    .stat-card{background:linear-gradient(135deg,rgba(22,163,74,0.1) 0%,rgba(22,163,74,0.05) 100%);border:1px solid rgba(22,163,74,0.2);border-radius:var(--radius-sm);padding:var(--space-4);text-align:center;border-left:4px solid var(--accent)}
    .stat-label{font-size:12px;text-transform:uppercase;letter-spacing:0.5px;color:var(--muted);margin-bottom:8px;font-weight:600}
    .stat-value{font-size:28px;font-weight:700;color:var(--text)}
    a{color:var(--accent);text-decoration:none}.back-btn{display:inline-block;margin-bottom:var(--space-6);padding:10px 16px;background:var(--accent);color:#0b141e;border-radius:var(--radius-xs);font-weight:600;transition:all .2s ease}.back-btn:hover{background:var(--accent-600);transform:translateY(-2px)}
    .charts-grid{display:grid;grid-template-columns:1fr 1fr;gap:var(--space-4)}
    @media(max-width:1024px){.layout{grid-template-columns:1fr}aside{display:none}.charts-grid{grid-template-columns:1fr}}
    *::-webkit-scrollbar{height:10px;width:10px}
    *::-webkit-scrollbar-track{background:#0a0f1a}
    *::-webkit-scrollbar-thumb{background:#1f2937;border-radius:8px}
    *::-webkit-scrollbar-thumb:hover{background:#273244}
  </style>
</head>
<body>
  <div class="layout">
    <aside>
      <div class="brand">Robo Trade</div>
      <nav class="nav">
        <a href="/" onclick="return navigateTo('dashboard')">📊 Dashboard</a>
        <a class="active" href="/operacoes" onclick="return navigateTo('operacoes')">📈 Operações</a>
        <a href="/configuracoes" onclick="return navigateTo('configuracoes')">⚙️ Configurações</a>
      </nav>
    </aside>
    <div style="display:flex;flex-direction:column;height:100vh">
      <header>
        <div class="header-title">📋 Histórico e Gráficos em Tempo Real</div>
        <div class="header-title" style="font-size:13px;color:var(--muted)">Atualiza a cada 3s</div>
      </header>
      <main style="flex:1;overflow-y:auto">
        <div class="container">
          <a href="/" class="back-btn">← Voltar para Dashboard</a>

          <div class="card">
            <h2>📊 Resumo de Operações</h2>
            <div class="stats" id="stats"></div>
          </div>

          <div class="card">
            <h2>📈 Gráficos em Tempo Real</h2>
            <div class="charts-grid">
              <div>
                <canvas id="chartEquity"></canvas>
              </div>
              <div>
                <canvas id="chartCandles"></canvas>
              </div>
            </div>
          </div>

          <div class="card">
            <h2>📋 Todas as Operações</h2>
            <table>
              <thead id="tableHead"></thead>
              <tbody id="tableBody"></tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  </div>

  <script>
  const statsEl = document.getElementById('stats');
  const tableHead = document.getElementById('tableHead');
  const tableBody = document.getElementById('tableBody');

  const equityCtx = document.getElementById('chartEquity').getContext('2d');
  const candlesCtx = document.getElementById('chartCandles').getContext('2d');

  let equityChart = new Chart(equityCtx, {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Equity (BRL)', data: [], borderColor: '#16a34a', backgroundColor: 'rgba(22,163,74,0.2)', tension: 0.15, fill: true }] },
    options: { scales: { x: { display: false }, y: { ticks: { color: '#e5e7eb' } } }, plugins: { legend: { labels: { color: '#e5e7eb' } } } }
  });

  let candleChart = new Chart(candlesCtx, {
    type: 'candlestick',
    data: { datasets: [{ label: 'Preço', data: [], borderColor: '#e5e7eb' }] },
    options: { plugins: { legend: { labels: { color: '#e5e7eb' } } }, scales: { x: { ticks: { color: '#e5e7eb' } }, y: { ticks: { color: '#e5e7eb' } } } }
  });

  async function fetchData() {
    const [summaryRes, opsRes] = await Promise.all([
      fetch('/summary'),
      fetch('/operations_data')
    ]);

    const summary = await summaryRes.json();
    const ops = await opsRes.json();

    // Stats
    const cards = [
      { label: 'Total de Operações', value: summary.ops_count },
      { label: 'Ganhas', value: summary.wins, color: 'var(--accent)' },
      { label: 'Perdidas', value: summary.losses, color: 'var(--danger)' },
      { label: 'Taxa de Acerto', value: `${((summary.wins/(summary.ops_count||1))*100).toFixed(1)}%` },
      { label: 'Lucro Total', value: `R$ ${Number(summary.total_profit||0).toFixed(2)}`, color: 'var(--accent)' },
      { label: 'Saldo Simulado', value: `R$ ${Number(summary.account?.balance_brl||0).toFixed(2)}` }
    ];
    statsEl.innerHTML = cards.map(c => `<div class="stat-card"><div class="stat-label">${c.label}</div><div class="stat-value" style="${c.color ? `color:${c.color}`:''}">${c.value}</div></div>`).join('');

    // Equity chart
    const eq = summary.equity_curve || [];
    equityChart.data.labels = eq.map((_, i) => i+1);
    equityChart.data.datasets[0].data = eq;
    equityChart.update();

    // Candles chart
    const candles = summary.candles || [];
    candleChart.data.datasets[0].data = candles.map(c => ({x: c.x, o: c.o, h: c.h, l: c.l, c: c.c}));
    candleChart.update();

    // Table
    if (ops.headers) {
      tableHead.innerHTML = `<tr>${ops.headers.map(h => `<th>${h}</th>`).join('')}</tr>`;
    }
    if (ops.rows) {
      tableBody.innerHTML = ops.rows.map(r => `<tr>${ops.headers.map(h => `<td>${r[h] ?? ''}</td>`).join('')}</tr>`).join('');
    }
  }

  function navigateTo(page) {
    if (page === 'dashboard') {
      window.location.href = '/';
    } else if (page === 'operacoes') {
      window.location.href = '/operacoes';
    }
    return false;
  }

  fetchData();
  setInterval(fetchData, 3000);
  </script>
</body>
</html>
    """)

@app.route('/operations_data')
def operations_data():
    headers, rows = load_csv(DATA_FILE)
    return jsonify({
        'headers': headers,
        'rows': rows
    })

@app.route('/summary')
def summary():
  headers, rows = load_csv(DATA_FILE)
  wins = sum(1 for r in rows if str(r.get("win")).lower() in ("true", "1"))
  losses = len(rows) - wins
  total_profit = sum(float(r.get("profit_brl", 0) or 0) for r in rows)
  prog = getattr(runner, 'candle_progress', 0) or 0
  raw = getattr(runner, 'candles', [])
  start = max(0, prog - 100)
  sliced = raw[start:prog] if prog else raw[-100:]
  candles_js = []
  idx_base = 0 if not prog else start
  for i, c in enumerate(sliced):
    try:
      t = int(c[0]) if int(c[0]) > 0 else (idx_base + i)
      o, h, l, cl = float(c[1]), float(c[2]), float(c[3]), float(c[4])
      candles_js.append({'x': t, 'o': o, 'h': h, 'l': l, 'c': cl})
    except Exception:
      continue

  # Fallback: fetch candles from exchange if none available
  try:
    if (not candles_js) and ccxt is not None:
      ex_name = getattr(settings, 'exchange', 'binance')
      symbol = getattr(runner, 'symbol', None) or getattr(settings, 'symbol', 'ADA/USDT')
      timeframe = getattr(runner, 'timeframe', None) or '5m'
      exchange = getattr(ccxt, ex_name)()
      # limit recent candles
      ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=100)
      candles_js = [
        {'x': c[0], 'o': float(c[1]), 'h': float(c[2]), 'l': float(c[3]), 'c': float(c[4])}
        for c in ohlcv
      ]
  except Exception:
    pass
  
  # Get Quotex balance if broker is connected
  quotex_balance = None
  quotex_status = "disconnected"
  if hasattr(runner, 'broker') and runner.broker:
    try:
      balance_info = runner.broker.get_balance()
      quotex_balance = balance_info.get('balance', 0.0)
      quotex_status = balance_info.get('status', 'error')
    except Exception as e:
      import logging
      logging.warning(f"Failed to get Quotex balance: {str(e)}")
      quotex_status = "error"
  
  return jsonify({
    'ops_count': len(rows),
    'wins': wins,
    'losses': losses,
    'total_profit': total_profit,
    'equity_curve': runner.equity_curve,
    'win_loss_series': runner.win_loss_series,
    'bot': {'status': runner.status, 'symbol': runner.symbol, 'timeframe': runner.timeframe},
    'account': {'balance_brl': runner.balance_brl},
    'quotex': {'balance': quotex_balance, 'status': quotex_status},
    'candles': candles_js
  })

if __name__ == "__main__":
  host = os.getenv("HOST", "0.0.0.0")
  port = int(os.getenv("PORT", "5000"))
  debug = os.getenv("DEBUG", "false").lower() in ("1","true","yes")
  app.run(host=host, port=port, debug=debug)

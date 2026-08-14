from __future__ import annotations

from html import escape
from pathlib import Path
from textwrap import dedent
from typing import Iterable

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUTS_DIR = BASE_DIR / "outputs"
FIGURES_DIR = BASE_DIR / "figures"
ASSET_DIRS = [DATA_DIR, OUTPUTS_DIR, FIGURES_DIR]

SCENARIOS = {
    "S1 Household": {
        "scenario_id": "S1",
        "scenario_name": "Household baseline",
        "health_mode": "Household baseline context",
        "risk_mode": "Baseline interpretation",
        "intervention_mode": "Demand-shift advisory",
    },
    "S2 Community": {
        "scenario_id": "S2",
        "scenario_name": "Community monitoring",
        "health_mode": "Community demand and exposure monitoring",
        "risk_mode": "Community monitoring area",
        "intervention_mode": "Community response advisory",
    },
    "S3 Multi-Stressor": {
        "scenario_id": "S3",
        "scenario_name": "Multi-stressor episode",
        "health_mode": "Compound PM2.5 + heat exposure",
        "risk_mode": "Compound exposure hotspot",
        "intervention_mode": "High-stress advisory orchestration",
    },
    "S4 Weather-AQ": {
        "scenario_id": "S4",
        "scenario_name": "Weather-AQ sensitivity",
        "health_mode": "Sensitivity and tradeoff exploration",
        "risk_mode": "Sensitivity / scenario comparison",
        "intervention_mode": "Scenario-based intervention advisory",
    },
}

NAV_ITEMS = [
    "🏠 Command Center",
    "🔄 CDE / Digital Thread",
    "📊 Analysis",
    "🌿 Intervention Layer",
    "🖥 Smart Healing Interface",
    "🎯 Decision Support",
]

ANALYSIS_ITEMS = ["S1 Household", "S2 Community", "S3 Multi-Stressor", "S4 Weather-AQ"]


st.set_page_config(
    page_title="Urban CPS DT Command Center",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    :root {
        --ink: #1f2933;
        --muted: #607080;
        --line: #d7dee6;
        --panel: #f7f9fb;
        --blue: #415a77;
        --green: #6f9385;
        --warm: #a7897f;
    }
    .stApp {
        background: #fbfcfd;
        color: var(--ink);
    }
    section[data-testid="stSidebar"] {
        background: #eef2f6;
        border-right: 1px solid var(--line);
    }
    h1, h2, h3 {
        color: var(--ink);
        letter-spacing: 0;
    }
    div[data-testid="stMetricValue"], .stMarkdown strong {
        color: var(--blue);
    }
    .badge-strip {
        display: grid;
        grid-template-columns: repeat(5, minmax(0, 1fr));
        gap: 0.55rem;
        margin: 0.75rem 0 1rem 0;
    }
    .badge {
        border: 1px solid var(--line);
        background: #f4f7fa;
        border-radius: 999px;
        padding: 0.45rem 0.65rem;
        display: flex;
        gap: 0.45rem;
        align-items: center;
        min-height: 42px;
    }
    .badge-icon {
        color: var(--blue);
        font-size: 1rem;
    }
    .badge-label {
        color: var(--muted);
        font-size: 0.68rem;
        line-height: 1.05;
    }
    .badge-value {
        color: var(--blue);
        font-weight: 750;
        font-size: 0.82rem;
        line-height: 1.15;
        overflow-wrap: anywhere;
    }
    .cc-grid {
        display: grid;
        grid-template-columns: minmax(0, .88fr) minmax(0, 1.08fr) minmax(0, 1fr);
        gap: 0.85rem;
        align-items: start;
        margin-top: 0.3rem;
    }
    .section-card {
        border: 1px solid var(--line);
        border-radius: 10px;
        background: #f8fafc;
        padding: 0.9rem;
    }
    .section-title {
        color: var(--ink);
        font-weight: 800;
        font-size: 1.02rem;
        margin-bottom: 0.2rem;
    }
    .section-subtitle {
        color: var(--muted);
        font-size: 0.82rem;
        line-height: 1.3;
        margin-bottom: 0.7rem;
    }
    .source-card,
    .state-card,
    .intervention-card,
    .trace-step,
    .loop-step,
    .hotspot-card {
        border: 1px solid var(--line);
        border-radius: 9px;
        background: #ffffff;
        padding: 0.78rem;
        margin-bottom: 0.58rem;
    }
    .source-head,
    .state-head,
    .intervention-head {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.45rem;
    }
    .icon-box {
        width: 36px;
        height: 36px;
        border-radius: 11px;
        background: #eaf0f5;
        color: var(--blue);
        display: flex;
        align-items: center;
        justify-content: center;
        flex: 0 0 36px;
        font-size: 1.05rem;
    }
    .card-title {
        color: var(--ink);
        font-weight: 780;
        line-height: 1.2;
    }
    .card-kv,
    .card-text,
    .trace-text,
    .loop-text {
        color: var(--muted);
        font-size: 0.84rem;
        line-height: 1.35;
    }
    .status-value {
        color: var(--blue);
        font-size: 1.22rem;
        font-weight: 800;
        line-height: 1.12;
        margin-bottom: 0.25rem;
    }
    .priority {
        margin-left: auto;
        border: 1px solid var(--line);
        border-radius: 999px;
        background: #eef3f7;
        color: var(--blue);
        font-size: 0.72rem;
        font-weight: 750;
        padding: 0.16rem 0.45rem;
        white-space: nowrap;
    }
    .pipeline {
        display: grid;
        gap: 0.38rem;
    }
    .pipeline-node {
        border: 1px solid var(--line);
        border-radius: 8px;
        background: #ffffff;
        color: var(--blue);
        font-weight: 760;
        text-align: center;
        padding: 0.62rem;
    }
    .pipeline-arrow {
        color: var(--muted);
        text-align: center;
        font-weight: 800;
    }
    .hotspot-grid {
        display: grid;
        grid-template-columns: repeat(5, minmax(0, 1fr));
        gap: 0.55rem;
    }
    .hotspot-card {
        border-top: 4px solid #8fa1b3;
        min-height: 118px;
    }
    .hotspot-card.active {
        border-top-color: var(--green);
        background: #f7fbf8;
    }
    .health-status-card {
        border: 1px solid var(--line);
        border-radius: 12px;
        background: #ffffff;
        padding: 1rem;
        margin: 0.4rem 0 0.95rem 0;
        border-left: 8px solid var(--green);
        display: grid;
        grid-template-columns: auto 1fr;
        gap: 0.85rem;
        align-items: center;
    }
    .health-status-card.moderate {
        border-left-color: #c5ad55;
    }
    .health-status-card.elevated {
        border-left-color: #b86f4c;
    }
    .health-status-card.high {
        border-left-color: #a15f5f;
    }
    .health-status-icon {
        width: 58px;
        height: 58px;
        border-radius: 18px;
        background: #edf4f0;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.55rem;
    }
    .health-status-label {
        color: var(--muted);
        font-size: 0.8rem;
        line-height: 1.2;
    }
    .health-status-value {
        color: var(--ink);
        font-size: 1.55rem;
        font-weight: 850;
        line-height: 1.15;
        margin: 0.1rem 0 0.2rem 0;
    }
    .health-status-detail {
        color: var(--muted);
        font-size: 0.9rem;
        line-height: 1.35;
    }
    .urban-map {
        border: 1px solid var(--line);
        border-radius: 12px;
        background: linear-gradient(135deg, #f7f9fb 0%, #eef3f7 100%);
        padding: 0.85rem;
        margin: 0.35rem 0 0.9rem 0;
    }
    .urban-map-grid {
        display: grid;
        grid-template-columns: 1fr 1.25fr 1fr;
        grid-template-rows: 120px 130px 120px;
        gap: 0.55rem;
        grid-template-areas:
            "north north industrial"
            "residential central industrial"
            "south south central2";
    }
    .urban-zone {
        border: 1px solid var(--line);
        border-radius: 10px;
        background: rgba(255,255,255,.82);
        padding: 0.7rem;
        position: relative;
        overflow: hidden;
    }
    .urban-zone.active {
        background: #f7fbf8;
        border-color: #9bb9aa;
        box-shadow: inset 0 0 0 2px rgba(111,147,133,.22);
    }
    .zone-north { grid-area: north; }
    .zone-central { grid-area: central; }
    .zone-central2 { grid-area: central2; }
    .zone-residential { grid-area: residential; }
    .zone-industrial { grid-area: industrial; }
    .zone-south { grid-area: south; }
    .zone-title {
        color: var(--ink);
        font-weight: 800;
        line-height: 1.2;
    }
    .zone-label {
        color: var(--muted);
        font-size: 0.82rem;
        line-height: 1.3;
        margin-top: 0.25rem;
        max-width: 18rem;
    }
    .hotspot-marker {
        position: absolute;
        right: 0.65rem;
        bottom: 0.65rem;
        min-width: 36px;
        height: 36px;
        border-radius: 999px;
        border: 2px solid #ffffff;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 850;
        box-shadow: 0 2px 8px rgba(31,41,51,.12);
    }
    .marker-low { background: #8ab89b; color: #173b27; }
    .marker-moderate { background: #d8c46c; color: #433814; }
    .marker-elevated { background: #d99a68; color: #4a2615; }
    .marker-high { background: #bd6969; color: #ffffff; }
    .map-legend {
        display: flex;
        flex-wrap: wrap;
        gap: 0.55rem;
        margin-top: 0.65rem;
        color: var(--muted);
        font-size: 0.82rem;
    }
    .map-legend span {
        border: 1px solid var(--line);
        border-radius: 999px;
        padding: 0.22rem 0.5rem;
        background: #ffffff;
    }
    .priority-list {
        margin-top: 0.35rem;
    }
    .priority-row {
        margin-bottom: 0.55rem;
    }
    .priority-topline {
        display: flex;
        justify-content: space-between;
        gap: 0.75rem;
        color: var(--ink);
        font-size: 0.84rem;
        font-weight: 750;
        margin-bottom: 0.18rem;
    }
    .priority-track {
        height: 8px;
        border-radius: 999px;
        background: #e5ebf0;
        overflow: hidden;
    }
    .priority-fill {
        height: 8px;
        border-radius: 999px;
        background: linear-gradient(90deg, var(--green), var(--blue));
    }
    .impact-flow {
        display: grid;
        grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr) auto minmax(0, 1fr);
        gap: 0.65rem;
        align-items: stretch;
        margin: 0.45rem 0 0.75rem 0;
    }
    .impact-card {
        border: 1px solid var(--line);
        border-radius: 12px;
        background: #ffffff;
        padding: 1rem;
        min-height: 150px;
        border-top: 5px solid #8fa1b3;
    }
    .impact-card.outcome {
        border-top-color: var(--green);
    }
    .impact-arrow {
        color: var(--muted);
        font-size: 1.8rem;
        font-weight: 850;
        align-self: center;
    }
    .impact-label {
        color: var(--muted);
        font-size: 0.78rem;
        line-height: 1.2;
        margin-bottom: 0.35rem;
    }
    .impact-title {
        color: var(--blue);
        font-weight: 850;
        font-size: 1.2rem;
        line-height: 1.18;
        margin-bottom: 0.45rem;
    }
    .impact-detail {
        color: var(--muted);
        font-size: 0.9rem;
        line-height: 1.38;
    }
    .healing-intro {
        border: 1px solid var(--line);
        border-radius: 12px;
        background: #f7fbf8;
        padding: 0.95rem 1rem;
        margin: 0.45rem 0 1rem 0;
        color: var(--muted);
        line-height: 1.42;
    }
    .reaction-flow {
        display: grid;
        grid-template-columns: repeat(6, minmax(0, 1fr));
        gap: 0.55rem;
        margin: 0.45rem 0 1rem 0;
    }
    .reaction-step {
        border: 1px solid var(--line);
        border-radius: 12px;
        background: #ffffff;
        padding: 0.78rem;
        min-height: 132px;
        border-top: 4px solid #8fa1b3;
    }
    .reaction-icon {
        width: 34px;
        height: 34px;
        border-radius: 11px;
        background: #eaf0f5;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 0.45rem;
    }
    .reaction-title {
        color: var(--blue);
        font-weight: 800;
        line-height: 1.18;
        margin-bottom: 0.28rem;
    }
    .reaction-detail {
        color: var(--muted);
        font-size: 0.8rem;
        line-height: 1.32;
    }
    .process-strip {
        display: grid;
        grid-template-columns: repeat(5, minmax(0, 1fr));
        gap: 0.45rem;
        margin: 0.35rem 0 0.85rem 0;
    }
    .process-pill {
        border: 1px solid var(--line);
        border-radius: 999px;
        background: #f7f9fb;
        padding: 0.48rem 0.62rem;
        display: flex;
        align-items: center;
        gap: 0.42rem;
        min-height: 46px;
        position: relative;
    }
    .process-pill:not(:last-child)::after {
        content: "→";
        position: absolute;
        right: -0.55rem;
        color: var(--muted);
        font-weight: 800;
    }
    .process-pill.active {
        border-color: #8db29f;
        background: #f1f7f4;
        box-shadow: 0 0 0 3px rgba(111,147,133,.12);
    }
    .process-icon {
        color: var(--blue);
        font-weight: 850;
        flex: 0 0 auto;
    }
    .process-title {
        color: var(--ink);
        font-size: 0.78rem;
        font-weight: 820;
        line-height: 1.15;
    }
    .process-detail {
        color: var(--muted);
        font-size: 0.68rem;
        line-height: 1.15;
    }
    .spatial-scene {
        border: 1px solid var(--line);
        border-radius: 16px;
        background: linear-gradient(135deg, #f7f9fb 0%, #edf3f1 100%);
        padding: 0.9rem;
        margin: 0.45rem 0 1rem 0;
        position: relative;
        overflow: hidden;
    }
    .spatial-scene-stage {
        position: relative;
        min-height: 460px;
        border: 1px solid var(--line);
        border-radius: 14px;
        background: #f8fafc;
        overflow: hidden;
    }
    .indoor-scene,
    .outdoor-scene {
        position: absolute;
        top: 0;
        bottom: 0;
        width: 50%;
    }
    .indoor-scene {
        left: 0;
        background:
            linear-gradient(155deg, rgba(229,219,204,.92) 0%, rgba(245,240,232,.92) 52%, rgba(236,229,219,.92) 52%, rgba(220,207,190,.92) 100%);
    }
    .outdoor-scene {
        right: 0;
        background:
            linear-gradient(180deg, rgba(226,236,244,.95) 0%, rgba(238,245,240,.95) 62%, rgba(213,229,214,.95) 62%, rgba(202,222,205,.95) 100%);
    }
    .window-boundary {
        position: absolute;
        left: 46%;
        top: 9%;
        width: 12%;
        height: 73%;
        border: 3px solid rgba(65,90,119,.42);
        border-radius: 10px;
        background: rgba(232,243,249,.56);
        box-shadow: inset 0 0 0 1px rgba(255,255,255,.72), 0 8px 26px rgba(31,41,51,.08);
        z-index: 4;
    }
    .window-boundary::before,
    .window-boundary::after {
        content: "";
        position: absolute;
        background: rgba(65,90,119,.32);
    }
    .window-boundary::before {
        left: 50%;
        top: 0;
        bottom: 0;
        width: 2px;
    }
    .window-boundary::after {
        left: 0;
        right: 0;
        top: 48%;
        height: 2px;
    }
    .scene-label {
        position: absolute;
        top: 0.75rem;
        border: 1px solid var(--line);
        border-radius: 999px;
        background: rgba(255,255,255,.82);
        color: var(--blue);
        padding: 0.25rem 0.6rem;
        font-size: 0.78rem;
        font-weight: 800;
        z-index: 6;
    }
    .scene-label.indoor { left: 0.8rem; }
    .scene-label.outdoor { right: 0.8rem; }
    .scene-object,
    .endpoint-object,
    .stressor-object {
        position: absolute;
        border: 1px solid var(--line);
        border-radius: 12px;
        background: rgba(255,255,255,.9);
        padding: 0.38rem 0.5rem;
        color: var(--ink);
        font-size: 0.78rem;
        font-weight: 760;
        line-height: 1.15;
        box-shadow: 0 5px 15px rgba(31,41,51,.07);
        z-index: 5;
    }
    .endpoint-object.active,
    .stressor-object.active,
    .scene-object.active {
        border-color: #8db29f;
        background: #f7fbf8;
        box-shadow: 0 0 0 3px rgba(111,147,133,.18), 0 5px 15px rgba(31,41,51,.08);
    }
    .stressor-object.alert {
        border-color: #bd7a72;
        background: #fff7f5;
        box-shadow: 0 0 0 3px rgba(189,122,114,.16), 0 5px 15px rgba(31,41,51,.08);
    }
    .room-floor {
        position: absolute;
        left: 0;
        right: 50%;
        bottom: 0;
        height: 28%;
        background: linear-gradient(145deg, rgba(214,197,177,.82), rgba(232,220,205,.82));
        clip-path: polygon(0 28%, 100% 0, 100% 100%, 0 100%);
        z-index: 1;
    }
    .greenery {
        position: absolute;
        right: 3%;
        bottom: 5%;
        width: 24%;
        height: 22%;
        border-radius: 50% 50% 0 0;
        background: rgba(128,166,139,.38);
        z-index: 2;
    }
    .flow-line {
        position: absolute;
        height: 2px;
        background: rgba(65,90,119,.38);
        z-index: 7;
    }
    .flow-line::after {
        content: "";
        position: absolute;
        right: -1px;
        top: -4px;
        border-left: 8px solid rgba(65,90,119,.55);
        border-top: 5px solid transparent;
        border-bottom: 5px solid transparent;
    }
    .flow-sensing {
        left: 25%;
        top: 48%;
        width: 12%;
    }
    .flow-intervention {
        left: 64%;
        top: 48%;
        width: 13%;
    }
    .flow-feedback {
        left: 54%;
        top: 77%;
        width: 22%;
        transform: rotate(180deg);
        opacity: .68;
    }
    .scene-note {
        margin-top: 0.7rem;
        color: var(--muted);
        font-size: 0.86rem;
        line-height: 1.38;
    }
    .healing-grid {
        display: grid;
        grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
        gap: 0.85rem;
        align-items: start;
    }
    .healing-panel {
        border: 1px solid var(--line);
        border-radius: 12px;
        background: #f8fafc;
        padding: 0.9rem;
        margin-bottom: 0.85rem;
    }
    .healing-card-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.62rem;
    }
    .exposure-card,
    .interpretation-card,
    .healing-intervention,
    .updated-card,
    .before-after-card {
        border: 1px solid var(--line);
        border-radius: 11px;
        background: #ffffff;
        padding: 0.82rem;
    }
    .exposure-card {
        min-height: 132px;
        border-left: 5px solid #8fa1b3;
    }
    .exposure-card.low,
    .status-chip.low,
    .updated-card.low {
        border-color: #7da08b;
    }
    .exposure-card.watch,
    .status-chip.watch,
    .updated-card.watch {
        border-color: #c5ad55;
    }
    .exposure-card.alert,
    .status-chip.alert,
    .updated-card.alert {
        border-color: #a15f5f;
    }
    .card-row {
        display: flex;
        gap: 0.55rem;
        align-items: center;
        margin-bottom: 0.45rem;
    }
    .status-chip {
        display: inline-block;
        border: 1px solid var(--line);
        border-radius: 999px;
        background: #eef3f7;
        color: var(--blue);
        padding: 0.18rem 0.48rem;
        font-size: 0.72rem;
        font-weight: 800;
    }
    .exposure-value {
        color: var(--ink);
        font-size: 1.15rem;
        font-weight: 850;
        line-height: 1.15;
        margin-bottom: 0.25rem;
    }
    .healing-intervention-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.65rem;
    }
    .healing-intervention {
        min-height: 176px;
        border-top: 5px solid #8fa1b3;
    }
    .healing-intervention.primary {
        border-top-color: var(--green);
        background: #f7fbf8;
    }
    .intervention-name {
        color: var(--ink);
        font-weight: 850;
        line-height: 1.18;
        margin-bottom: 0.45rem;
    }
    .intervention-line {
        color: var(--muted);
        font-size: 0.84rem;
        line-height: 1.34;
        margin-bottom: 0.35rem;
    }
    .feedback-strip {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 0.62rem;
        margin: 0.45rem 0 0.85rem 0;
    }
    .before-after-card {
        min-height: 142px;
    }
    .before-after-title {
        color: var(--muted);
        font-size: 0.78rem;
        font-weight: 750;
        margin-bottom: 0.38rem;
    }
    .before-after-flow {
        color: var(--blue);
        font-weight: 850;
        font-size: 1.08rem;
        line-height: 1.25;
        margin-bottom: 0.38rem;
    }
    .updated-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 0.62rem;
    }
    .updated-card {
        min-height: 120px;
        border-top: 4px solid #8fa1b3;
    }
    .logic-list {
        margin: 0;
        padding-left: 1.1rem;
        color: var(--muted);
        line-height: 1.45;
        font-size: 0.92rem;
    }
    .logic-flow-grid {
        display: grid;
        grid-template-columns: repeat(7, minmax(0, 1fr));
        gap: 0.5rem;
        margin: 0.45rem 0 0.95rem 0;
    }
    .logic-flow-step,
    .hardware-card,
    .closure-card,
    .compact-action-card,
    .feedback-input-card,
    .operator-review-card {
        border: 1px solid var(--line);
        border-radius: 12px;
        background: #ffffff;
        padding: 0.8rem;
    }
    .logic-flow-step {
        min-height: 132px;
        border-top: 4px solid #8fa1b3;
        position: relative;
    }
    .logic-flow-step:not(:last-child)::after {
        content: "→";
        position: absolute;
        right: -0.48rem;
        top: 42%;
        color: var(--muted);
        font-weight: 850;
    }
    .logic-step-index {
        color: var(--green);
        font-weight: 850;
        font-size: 0.78rem;
        margin-bottom: 0.25rem;
    }
    .endpoint-response-grid,
    .hardware-grid,
    .closure-grid,
    .compact-action-grid {
        display: grid;
        gap: 0.65rem;
        margin: 0.45rem 0 0.9rem 0;
    }
    .endpoint-response-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
    .hardware-grid {
        grid-template-columns: repeat(4, minmax(0, 1fr));
    }
    .closure-grid {
        grid-template-columns: repeat(3, minmax(0, 1fr));
    }
    .compact-action-grid {
        grid-template-columns: repeat(3, minmax(0, 1fr));
    }
    .hardware-card {
        min-height: 118px;
        background: #f8fafc;
    }
    .closure-card {
        min-height: 120px;
        border-left: 5px solid #8fa1b3;
    }
    .compact-action-card {
        min-height: 142px;
        border-top: 5px solid #8fa1b3;
    }
    .compact-action-card.primary {
        border-top-color: var(--green);
        background: #f7fbf8;
    }
    .feedback-input-grid,
    .operator-review-grid {
        display: grid;
        gap: 0.65rem;
        margin: 0.45rem 0 0.9rem 0;
    }
    .feedback-input-grid {
        grid-template-columns: repeat(4, minmax(0, 1fr));
    }
    .operator-review-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
    .feedback-input-card {
        min-height: 118px;
        border-left: 5px solid #8fa1b3;
        background: #f8fafc;
    }
    .operator-review-card {
        min-height: 150px;
        border-top: 5px solid #8fa1b3;
    }
    .scope-panel,
    .scenario-purpose-card,
    .decision-trace-panel {
        border: 1px solid var(--line);
        border-radius: 12px;
        background: #f8fafc;
        padding: 0.95rem;
        margin: 0.65rem 0 0.95rem 0;
    }
    .scope-grid,
    .scenario-purpose-grid,
    .decision-trace-grid {
        display: grid;
        gap: 0.62rem;
        margin-top: 0.7rem;
    }
    .scope-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
    .scenario-purpose-grid {
        grid-template-columns: repeat(4, minmax(0, 1fr));
    }
    .decision-trace-grid {
        grid-template-columns: repeat(6, minmax(0, 1fr));
    }
    .scope-card,
    .purpose-mini-card,
    .decision-trace-step {
        border: 1px solid var(--line);
        border-radius: 10px;
        background: #ffffff;
        padding: 0.75rem;
    }
    .scope-card ul {
        margin: 0.45rem 0 0 1.05rem;
        padding: 0;
        color: var(--muted);
        font-size: 0.86rem;
        line-height: 1.45;
    }
    .purpose-label,
    .control-label,
    .trace-label {
        color: var(--muted);
        font-size: 0.74rem;
        font-weight: 760;
        margin-bottom: 0.2rem;
    }
    .control-level-badge {
        display: inline-block;
        border: 1px solid #b7c5d2;
        border-radius: 999px;
        background: #eef3f7;
        color: var(--blue);
        font-size: 0.72rem;
        font-weight: 820;
        padding: 0.16rem 0.48rem;
        margin: 0.15rem 0 0.35rem 0;
    }
    .decision-trace-step {
        min-height: 110px;
        position: relative;
        border-top: 4px solid #8fa1b3;
    }
    .decision-trace-step:not(:last-child)::after {
        content: "→";
        position: absolute;
        right: -0.55rem;
        top: 42%;
        color: var(--muted);
        font-weight: 850;
    }
    .trace-row,
    .loop-row {
        display: grid;
        grid-template-columns: repeat(5, minmax(0, 1fr));
        gap: 0.55rem;
        margin: 0.4rem 0 0.75rem 0;
    }
    .trace-step,
    .loop-step {
        min-height: 94px;
        text-align: center;
    }
    .trace-index {
        color: var(--green);
        font-weight: 800;
        margin-bottom: 0.25rem;
    }
    @media (max-width: 1150px) {
        .badge-strip,
        .cc-grid,
        .hotspot-grid,
        .trace-row,
        .loop-row,
        .urban-map-grid,
        .impact-flow,
        .reaction-flow,
        .logic-flow-grid,
        .endpoint-response-grid,
        .hardware-grid,
        .closure-grid,
        .compact-action-grid,
        .feedback-input-grid,
        .operator-review-grid,
        .scope-grid,
        .scenario-purpose-grid,
        .decision-trace-grid,
        .process-strip,
        .healing-grid,
        .healing-intervention-grid,
        .feedback-strip,
        .updated-grid {
            grid-template-columns: 1fr;
        }
        .spatial-scene-stage {
            min-height: 760px;
        }
        .indoor-scene,
        .outdoor-scene {
            position: absolute;
            left: 0;
            right: 0;
            width: 100%;
            height: 50%;
        }
        .indoor-scene {
            top: 0;
            bottom: auto;
        }
        .outdoor-scene {
            top: 50%;
            bottom: 0;
        }
        .room-floor {
            right: 0;
            bottom: 50%;
            height: 14%;
        }
        .window-boundary {
            left: 10%;
            top: 43%;
            width: 80%;
            height: 13%;
        }
        .flow-line {
            display: none;
        }
        .healing-card-grid {
            grid-template-columns: 1fr;
        }
        .process-pill:not(:last-child)::after {
            display: none;
        }
        .decision-trace-step:not(:last-child)::after {
            display: none;
        }
        .urban-map-grid {
            grid-template-rows: none;
            grid-template-areas: none;
        }
        .zone-north,
        .zone-central,
        .zone-central2,
        .zone-residential,
        .zone-industrial,
        .zone-south {
            grid-area: auto;
        }
        .impact-arrow {
            text-align: center;
            transform: rotate(90deg);
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def find_asset(relative_path: str | Path) -> Path | None:
    relative_path = Path(relative_path)
    if relative_path.is_absolute() or ".." in relative_path.parts:
        return None
    for directory in ASSET_DIRS:
        candidate = directory / relative_path
        if candidate.exists():
            return candidate
    return None


def normalize_datetime(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    unnamed = [col for col in df.columns if str(col).startswith("Unnamed")]
    candidates = unnamed + [c for c in df.columns if str(c).lower() in {"timestamp", "time", "datetime", "date"}]
    for col in candidates:
        parsed = pd.to_datetime(df[col], errors="coerce")
        if parsed.notna().sum() >= max(1, len(df) // 3):
            df = df.rename(columns={col: "timestamp"})
            df["timestamp"] = parsed
            return df
    return df


@st.cache_data(show_spinner=False)
def load_csv(relative_path: str) -> tuple[pd.DataFrame | None, str | None]:
    path = find_asset(relative_path)
    if path is None:
        return None, f"Missing dashboard asset: {relative_path}"
    try:
        return normalize_datetime(pd.read_csv(path)), None
    except Exception as exc:
        return None, f"Could not load {relative_path}: {exc}"


def warn_missing(relative_path: str) -> None:
    st.warning(f"{relative_path} is unavailable in the dashboard asset layer. A non-crashing placeholder is shown.")


def show_image(relative_path: str, caption: str | None = None) -> None:
    path = find_asset(relative_path)
    if path:
        st.image(str(path), caption=caption or relative_path, use_container_width=True)
    else:
        warn_missing(relative_path)


def show_table(relative_path: str, label: str) -> pd.DataFrame | None:
    st.subheader(label)
    df, error = load_csv(relative_path)
    if error:
        warn_missing(relative_path)
        return None
    if "placeholder" in df.columns and df["placeholder"].astype(str).str.lower().eq("true").any():
        st.info(f"{relative_path} is a documented placeholder output.")
    st.dataframe(df, use_container_width=True, hide_index=True)
    return df


def first_existing_column(df: pd.DataFrame | None, names: Iterable[str]) -> str | None:
    if df is None:
        return None
    lower = {str(col).lower(): col for col in df.columns}
    for name in names:
        if name.lower() in lower:
            return lower[name.lower()]
    return None


def missing_ratio(df: pd.DataFrame) -> str:
    if df.empty:
        return "Unavailable"
    total = df.shape[0] * df.shape[1]
    if total == 0:
        return "Unavailable"
    return f"{df.isna().sum().sum() / total * 100:.2f}%"


def valid_coverage(df: pd.DataFrame) -> str:
    if df.empty:
        return "Unavailable"
    total = df.shape[0] * df.shape[1]
    if total == 0:
        return "Unavailable"
    return f"{(1 - df.isna().sum().sum() / total) * 100:.2f}%"


def get_runtime_state(selected_scenario: str) -> dict[str, str]:
    base = SCENARIOS[selected_scenario].copy()
    base.update(
        {
            "cde_status": "Harmonised",
            "sync_status": "ACTIVE",
            "feedback_status": "Simulated feedback",
            "data_mode": "Secondary-data simulation",
        }
    )
    return base


def badge(label: str, value: str, icon: str) -> str:
    return dedent(
        f"""
        <div class="badge">
            <div class="badge-icon">{escape(icon)}</div>
            <div>
                <div class="badge-label">{escape(label)}</div>
                <div class="badge-value">{escape(value)}</div>
            </div>
        </div>
        """
    ).strip()


def render_badge_strip(runtime_state: dict[str, str]) -> None:
    st.markdown(
        f"""
        <div class="badge-strip">
            {badge("Scenario", f"{runtime_state['scenario_id']} · {runtime_state['scenario_name']}", "●")}
            {badge("CDE sync", runtime_state["cde_status"], "↔")}
            {badge("Health mode", runtime_state["health_mode"], "+")}
            {badge("Intervention", runtime_state["intervention_mode"], "→")}
            {badge("Feedback", runtime_state["feedback_status"], "↻")}
        </div>
        """,
        unsafe_allow_html=True,
    )


def source_card(icon: str, title: str, rows: dict[str, str]) -> str:
    details = "".join(f"<div class='card-kv'>{escape(k)}: {escape(v)}</div>" for k, v in rows.items())
    return dedent(
        f"""
        <div class="source-card">
            <div class="source-head">
                <div class="icon-box">{escape(icon)}</div>
                <div class="card-title">{escape(title)}</div>
            </div>
            {details}
        </div>
        """
    ).strip()


def intervention_rows(runtime_state: dict[str, str]) -> list[dict[str, str]]:
    sid = runtime_state["scenario_id"]
    feedback = runtime_state["feedback_status"]
    if sid == "S1":
        return [
            {"icon": "⚡", "endpoint": "Demand-response scheduling", "priority": "Low", "trigger": "Flexible household demand window", "action": "Identify non-critical end-use periods for advisory demand shifting.", "status": feedback},
            {"icon": "👥", "endpoint": "Occupancy exposure advisory", "priority": "Low", "trigger": "Household baseline context", "action": "Keep indoor exposure context visible beside end-use behaviour.", "status": "Monitoring"},
            {"icon": "⚡", "endpoint": "Indoor baseline monitoring", "priority": "Low", "trigger": "End-use behaviour pattern", "action": "Track baseline demand and exposure indicators for interpretation.", "status": feedback},
        ]
    if sid == "S2":
        return [
            {"icon": "⚡", "endpoint": "Community demand-response scheduling", "priority": "Moderate", "trigger": "Aggregated load pressure", "action": "Coordinate advisory scheduling for flexible community demand.", "status": feedback},
            {"icon": "⚡", "endpoint": "Peak-load monitoring", "priority": "Moderate", "trigger": "Community peak tendency", "action": "Maintain peak-load watch and compare surrogate response.", "status": "Monitoring"},
            {"icon": "👥", "endpoint": "Aggregated exposure monitoring", "priority": "Moderate", "trigger": "Community environmental context", "action": "Interpret exposure pressure at community scale.", "status": feedback},
        ]
    if sid == "S3":
        return [
            {"icon": "🌬", "endpoint": "Smart ventilation / filtration", "priority": "High", "trigger": "PM2.5 exposure watch", "action": "Filter indoor air and reduce outdoor intake during elevated PM2.5.", "status": feedback},
            {"icon": "🌞", "endpoint": "Adaptive shading", "priority": "High", "trigger": "Heat stress detected", "action": "Reduce solar heat gain during elevated temperature periods.", "status": feedback},
            {"icon": "❄", "endpoint": "Passive cooling", "priority": "Moderate", "trigger": "Thermal stress watch", "action": "Use passive cooling and low-energy cooling guidance.", "status": feedback},
            {"icon": "👥", "endpoint": "Occupancy exposure advisory", "priority": "High", "trigger": "Compound PM2.5 + heat exposure", "action": "Reduce time in high-exposure environmental conditions.", "status": feedback},
            {"icon": "⚡", "endpoint": "Demand-response scheduling", "priority": "Moderate", "trigger": "Load pressure during event", "action": "Shift flexible demand away from high-stress periods.", "status": "Monitoring"},
        ]
    return [
        {"icon": "🌬", "endpoint": "Smart ventilation strategy", "priority": "Moderate", "trigger": "Weather-AQ sensitivity result", "action": "Compare ventilation options under air-quality and weather assumptions.", "status": feedback},
        {"icon": "❄", "endpoint": "Cooling-air-quality tradeoff", "priority": "Moderate", "trigger": "Cooling and air-quality contrast", "action": "Balance cooling guidance with outdoor exposure conditions.", "status": feedback},
        {"icon": "👥", "endpoint": "Scenario comparison advisory", "priority": "Low", "trigger": "Sensitivity exploration", "action": "Compare scenario pathways before selecting an advisory response.", "status": "Monitoring"},
    ]


def intervention_card(row: dict[str, str]) -> str:
    return dedent(
        f"""
        <div class="intervention-card">
            <div class="intervention-head">
                <div class="icon-box">{escape(row["icon"])}</div>
                <div class="card-title">{escape(row["endpoint"])}</div>
                <div class="priority">{escape(row["priority"])}</div>
            </div>
            <div class="card-text"><strong>Trigger:</strong> {escape(row["trigger"])}</div>
            <div class="card-text">{escape(row["action"])}</div>
            <div class="card-text"><strong>Status:</strong> {escape(row["status"])}</div>
        </div>
        """
    ).strip()


def pipeline_html() -> str:
    nodes = [
        "Energy + Air Quality + Weather",
        "Common Data Environment",
        "Health Exposure Interpretation",
        "Scenario Engine",
        "Intervention Engine",
        "Simulated Feedback",
    ]
    parts = []
    for idx, node in enumerate(nodes):
        parts.append(f"<div class='pipeline-node'>{escape(node)}</div>")
        if idx < len(nodes) - 1:
            parts.append("<div class='pipeline-arrow'>↓</div>")
    return "<div class='pipeline'>" + "".join(parts) + "</div>"


def environmental_snapshot(runtime_state: dict[str, str]) -> tuple[float | None, float | None, float | None]:
    df, _ = load_csv("community_pm25_weather_merged.csv")
    if df is None or df.empty:
        return None, None, None
    pm25_col = first_existing_column(df, ["pm25"])
    temp_col = first_existing_column(df, ["temp", "temperature"])
    load_col = first_existing_column(df, ["community_kw", "actual_load", "load"])

    def q75(col: str | None) -> float | None:
        if not col:
            return None
        values = pd.to_numeric(df[col], errors="coerce")
        if not values.notna().any():
            return None
        return float(values.quantile(0.75))

    if runtime_state["scenario_id"] == "S3" and pm25_col and temp_col:
        pm = pd.to_numeric(df[pm25_col], errors="coerce")
        tp = pd.to_numeric(df[temp_col], errors="coerce")
        score = pm.rank(pct=True).fillna(0) + tp.rank(pct=True).fillna(0)
        idx = int(score.idxmax()) if not score.empty else 0
        load = pd.to_numeric(df[load_col], errors="coerce").iloc[idx] if load_col else None
        return float(pm.iloc[idx]), float(tp.iloc[idx]), float(load) if load is not None and pd.notna(load) else q75(load_col)

    return q75(pm25_col), q75(temp_col), q75(load_col)


def classify_health(pm25: float | None, temp: float | None, load: float | None, runtime_state: dict[str, str]) -> dict[str, str]:
    sid = runtime_state["scenario_id"]
    air = "Unavailable" if pm25 is None else "Low" if pm25 < 12 else "Moderate" if pm25 < 20 else "Elevated" if pm25 < 35 else "High"
    heat = "Unavailable" if temp is None else "Normal" if temp < 24 else "Warm" if temp < 28 else "Heat stress" if temp < 32 else "Extreme heat"
    energy = "Unavailable" if load is None else "Baseline" if sid == "S1" else "Monitoring"
    if sid == "S3":
        compound = "Compound exposure watch"
    elif air in {"Elevated", "High"} and heat in {"Heat stress", "Extreme heat"}:
        compound = "Compound exposure watch"
    else:
        compound = runtime_state["health_mode"]
    return {"air": air, "heat": heat, "energy": energy, "compound": compound}


def state_card(icon: str, title: str, value: str, detail: str) -> str:
    return dedent(
        f"""
        <div class="state-card">
            <div class="state-head">
                <div class="icon-box">{escape(icon)}</div>
                <div class="card-title">{escape(title)}</div>
            </div>
            <div class="status-value">{escape(value)}</div>
            <div class="card-text">{escape(detail)}</div>
        </div>
        """
    ).strip()


def healing_tone(value: str) -> str:
    upper = value.upper()
    if any(token in upper for token in ["HIGH", "ALERT", "COMPOUND", "ELEVATED"]):
        return "alert"
    if any(token in upper for token in ["MODERATE", "WATCH", "WARM", "PRESSURE", "SENSITIVITY"]):
        return "watch"
    return "low"


def load_pressure_label(load: float | None, runtime_state: dict[str, str]) -> str:
    if load is None:
        return "Watch" if runtime_state["scenario_id"] in {"S2", "S3"} else "Baseline"
    if runtime_state["scenario_id"] == "S1":
        return "Moderate"
    if runtime_state["scenario_id"] == "S3":
        return "Elevated"
    return "Moderate"


def health_state_summary(state: dict[str, str], runtime_state: dict[str, str]) -> str:
    sid = runtime_state["scenario_id"]
    if sid == "S3":
        return "Health-aware state: Alert"
    if sid == "S4":
        return "Health-aware state: Watch"
    if state["air"] in {"Elevated", "High"} or state["heat"] in {"Heat stress", "Extreme heat"}:
        return "Health-aware state: Watch"
    return "Health-aware state: Stable"


def get_scene_visual_state(runtime_state: dict[str, str]) -> dict[str, str | int]:
    sid = runtime_state["scenario_id"]
    states: dict[str, dict[str, str | int]] = {
        "S1": {
            "theme_name": "Household baseline",
            "health_status": "Stable / Baseline / Monitoring",
            "dominant_zone": "indoor",
            "accent_colour": "#6f9385",
            "background_emphasis": "calm",
            "scene": "scenario-s1",
            "scenario_banner": "Household baseline mode active",
            "feedback_summary": "Baseline retained; demand scheduling may reduce peak load.",
            "active_step": 3,
            "mode": "Stable / Baseline / Monitoring",
            "warning": "Indoor baseline + demand scheduling",
            "indoor": "active calm",
            "pm25": "deemphasised",
            "heat": "deemphasised",
            "weather": "deemphasised",
            "vent": "active calm",
            "filter": "deemphasised",
            "cool": "deemphasised",
            "demand": "active calm",
            "occupancy": "active calm",
            "green": "calm",
            "hotspot": "deemphasised",
        },
        "S2": {
            "theme_name": "Community monitoring",
            "health_status": "Moderate Demand Pressure / Community Monitoring",
            "dominant_zone": "community-load",
            "accent_colour": "#58728f",
            "background_emphasis": "monitoring",
            "scene": "scenario-s2",
            "scenario_banner": "Community monitoring mode active",
            "feedback_summary": "Community coordination improves load distribution.",
            "active_step": 3,
            "mode": "Community monitoring / Demand pressure",
            "warning": "Aggregated demand pressure",
            "indoor": "",
            "pm25": "deemphasised",
            "heat": "deemphasised",
            "weather": "active",
            "vent": "deemphasised",
            "filter": "deemphasised",
            "cool": "deemphasised",
            "demand": "active load-focus",
            "occupancy": "",
            "green": "deemphasised",
            "hotspot": "active load-focus",
        },
        "S3": {
            "theme_name": "Multi-stressor episode",
            "health_status": "Alert / Multi-stressor / Compound Exposure",
            "dominant_zone": "outdoor-exposure",
            "accent_colour": "#b86f4c",
            "background_emphasis": "alert",
            "scene": "scenario-s3",
            "scenario_banner": "PM2.5 + heat multi-stressor episode active",
            "feedback_summary": "Mitigation pathway active: filtration + cooling + advisory.",
            "active_step": 4,
            "mode": "Alert / Multi-stressor / Exposure mitigation",
            "warning": "Compound exposure episode",
            "indoor": "active",
            "pm25": "alert",
            "heat": "alert",
            "weather": "active",
            "vent": "active",
            "filter": "active",
            "cool": "active",
            "demand": "active",
            "occupancy": "active",
            "green": "active",
            "hotspot": "alert",
        },
        "S4": {
            "theme_name": "Weather-AQ sensitivity",
            "health_status": "Environmental Sensitivity / Scenario Exploration",
            "dominant_zone": "tradeoff",
            "accent_colour": "#6f6f96",
            "background_emphasis": "exploratory",
            "scene": "scenario-s4",
            "scenario_banner": "Weather-air-quality sensitivity mode active",
            "feedback_summary": "Scenario comparison supports adaptive planning.",
            "active_step": 2,
            "mode": "Sensitivity / Tradeoff planning",
            "warning": "Weather-AQ interaction zone",
            "indoor": "",
            "pm25": "active sensitivity",
            "heat": "active sensitivity",
            "weather": "active sensitivity",
            "vent": "active sensitivity",
            "filter": "deemphasised",
            "cool": "active sensitivity",
            "demand": "deemphasised",
            "occupancy": "",
            "green": "active sensitivity",
            "hotspot": "active sensitivity",
        },
    }
    return states[sid]


def get_scene_layout(scenario_id: str) -> dict[str, str]:
    base = {
        "occupancy": "left:7%; top:25%;",
        "indoor_sensing": "left:24%; top:23%;",
        "ventilation": "left:8%; top:50%;",
        "filtration": "left:28%; top:50%;",
        "cooling": "left:8%; top:67%;",
        "lighting": "left:30%; top:67%;",
        "demand": "left:7%; top:84%;",
        "occupancy_advisory": "left:29%; top:84%;",
        "pm25": "right:32%; top:16%;",
        "heat": "right:9%; top:19%;",
        "weather": "right:34%; top:39%;",
        "greenery": "right:8%; bottom:24%;",
        "hotspot": "right:23%; bottom:39%;",
        "vent_advisory": "right:5%; top:53%;",
        "cool_advisory": "right:5%; top:64%;",
        "green_zone": "right:5%; top:75%;",
        "feedback": "left:42%; bottom:7%; max-width:34%;",
    }
    overrides = {
        "S1": {
            "demand": "left:6%; top:82%;",
            "occupancy_advisory": "left:27%; top:86%;",
            "pm25": "right:34%; top:18%;",
            "heat": "right:8%; top:21%;",
            "weather": "right:35%; top:43%;",
            "hotspot": "right:24%; bottom:42%;",
            "vent_advisory": "right:6%; top:58%;",
            "cool_advisory": "right:6%; top:70%;",
            "green_zone": "right:6%; top:81%;",
            "feedback": "left:39%; bottom:6%; max-width:31%;",
        },
        "S2": {
            "demand": "left:8%; top:83%;",
            "occupancy_advisory": "left:29%; top:84%;",
            "weather": "right:35%; top:36%;",
            "hotspot": "right:19%; bottom:43%;",
            "vent_advisory": "right:6%; top:58%;",
            "cool_advisory": "right:6%; top:70%;",
            "green_zone": "right:6%; top:81%;",
            "feedback": "left:41%; bottom:6%; max-width:33%;",
        },
        "S3": {
            "pm25": "right:34%; top:14%;",
            "heat": "right:7%; top:19%;",
            "weather": "right:35%; top:37%;",
            "hotspot": "right:22%; bottom:43%;",
            "vent_advisory": "right:5%; top:53%;",
            "cool_advisory": "right:7%; top:65%;",
            "green_zone": "right:6%; top:77%;",
            "feedback": "left:39%; bottom:5%; max-width:37%;",
        },
        "S4": {
            "pm25": "right:34%; top:16%;",
            "heat": "right:8%; top:22%;",
            "weather": "right:30%; top:39%;",
            "hotspot": "right:18%; bottom:43%;",
            "vent_advisory": "right:5%; top:55%;",
            "cool_advisory": "right:7%; top:68%;",
            "green_zone": "right:5%; top:80%;",
            "feedback": "left:42%; bottom:6%; max-width:34%;",
        },
    }
    layout = base.copy()
    layout.update(overrides.get(scenario_id, {}))
    return layout


def scene_visibility_classes(scenario_id: str) -> dict[str, str]:
    keys = [
        "occupancy",
        "indoor_sensing",
        "ventilation",
        "filtration",
        "cooling",
        "lighting",
        "demand",
        "occupancy_advisory",
        "pm25",
        "heat",
        "weather",
        "greenery",
        "hotspot",
        "vent_advisory",
        "cool_advisory",
        "green_zone",
    ]
    visible = {
        "S1": {"occupancy", "indoor_sensing", "ventilation", "demand", "occupancy_advisory"},
        "S2": {"indoor_sensing", "demand", "weather", "hotspot"},
        "S3": {
            "occupancy",
            "indoor_sensing",
            "ventilation",
            "filtration",
            "cooling",
            "demand",
            "pm25",
            "heat",
            "weather",
            "hotspot",
            "vent_advisory",
            "cool_advisory",
            "green_zone",
        },
        "S4": {"indoor_sensing", "ventilation", "cooling", "pm25", "heat", "weather", "greenery", "hotspot", "vent_advisory", "cool_advisory", "green_zone"},
    }[scenario_id]
    return {key: "" if key in visible else "scene-hidden" for key in keys}


def scene_feedback_label(runtime_state: dict[str, str]) -> str:
    return {
        "S1": "Stable baseline",
        "S2": "Load watch",
        "S3": "Exposure watch",
        "S4": "Tradeoff explored",
    }[runtime_state["scenario_id"]]


def health_interpretation_cards(state: dict[str, str], runtime_state: dict[str, str]) -> list[dict[str, str]]:
    air_text = {
        "Low": "Low respiratory exposure pressure",
        "Moderate": "Moderate respiratory exposure pressure",
        "Elevated": "Elevated respiratory exposure pressure",
        "High": "High respiratory exposure pressure",
        "Unavailable": "Respiratory exposure pressure unavailable",
    }.get(state["air"], "Respiratory exposure pressure under monitoring")
    heat_text = {
        "Normal": "Thermal discomfort pressure remains low",
        "Warm": "Thermal discomfort pressure is emerging",
        "Heat stress": "Thermal discomfort pressure is elevated",
        "Extreme heat": "Thermal discomfort pressure is high",
        "Unavailable": "Thermal discomfort pressure unavailable",
    }.get(state["heat"], "Thermal discomfort pressure under monitoring")
    burden = "Elevated compound environmental burden" if runtime_state["scenario_id"] == "S3" else state["compound"]
    if runtime_state["scenario_id"] == "S1":
        note = "Indoor exposure context remains acceptable but should be monitored."
    elif runtime_state["scenario_id"] == "S2":
        note = "Community-scale exposure and demand pressure require monitoring."
    elif runtime_state["scenario_id"] == "S3":
        note = "Coupled PM2.5 and heat conditions trigger a multi-stressor advisory."
    else:
        note = "Weather-air-quality sensitivity is interpreted through scenario comparison."
    return [
        {"icon": "🌫", "title": "Respiratory exposure pressure", "value": air_text, "tone": healing_tone(state["air"])},
        {"icon": "🌡", "title": "Thermal discomfort pressure", "value": heat_text, "tone": healing_tone(state["heat"])},
        {"icon": "⚠", "title": "Combined urban exposure burden", "value": burden, "tone": healing_tone(burden)},
        {"icon": "👥", "title": "Health-aware state summary", "value": note, "tone": healing_tone(health_state_summary(state, runtime_state))},
    ]


def healing_interventions(state: dict[str, str], runtime_state: dict[str, str]) -> list[dict[str, str]]:
    sid = runtime_state["scenario_id"]
    if sid == "S3":
        return [
            {"icon": "🌬", "name": "Prioritise air filtration", "trigger": "PM2.5 elevated", "effect": "May reduce indoor particle exposure pressure.", "status": "Advisory / simulated", "primary": "primary"},
            {"icon": "🌬", "name": "Smart ventilation advisory", "trigger": "Outdoor exposure and indoor protection tradeoff", "effect": "Supports reduced outdoor air intake or filtered ventilation when PM2.5 is elevated.", "status": "Advisory / simulated", "primary": "primary"},
            {"icon": "🌞", "name": "Shading / cooling advisory", "trigger": "Heat marker active", "effect": "May reduce solar heat gain and thermal discomfort pressure.", "status": "Advisory / simulated", "primary": "primary"},
            {"icon": "❄", "name": "Passive cooling", "trigger": "Heat stress elevated", "effect": "Supports lower-energy cooling response during multi-stressor periods.", "status": "Advisory / simulated"},
            {"icon": "👥", "name": "Occupancy guidance", "trigger": "Compound exposure burden", "effect": "Supports reduced time in high-exposure conditions.", "status": "Advisory"},
            {"icon": "⚡", "name": "Reschedule flexible demand", "trigger": "Event-period load pressure", "effect": "May lower peak pressure during high-stress periods.", "status": "Monitoring"},
        ]
    if sid == "S4":
        return [
            {"icon": "🌬", "name": "Ventilation-cooling tradeoff", "trigger": "Weather-AQ sensitivity", "effect": "Supports comparison of ventilation and cooling response pathways.", "status": "Simulated"},
            {"icon": "🔎", "name": "Weather-AQ scenario comparison", "trigger": "Sensitivity exploration", "effect": "Clarifies how air quality and weather assumptions change advisory choices.", "status": "Simulated"},
            {"icon": "🌿", "name": "Adaptive intervention planning", "trigger": "Tradeoff interpretation", "effect": "Supports scenario-resilient intervention planning.", "status": "Advisory"},
        ]
    if sid == "S2":
        return [
            {"icon": "⚡", "name": "Community demand coordination", "trigger": "Community load pressure", "effect": "Supports improved load distribution.", "status": "Advisory"},
            {"icon": "📈", "name": "Peak-load monitoring", "trigger": "Aggregated peak tendency", "effect": "Keeps community demand peaks visible for advisory planning.", "status": "Monitoring"},
            {"icon": "👥", "name": "Aggregated exposure monitoring", "trigger": "Community environmental context", "effect": "Keeps exposure pressure visible at community scale.", "status": "Monitoring"},
            {"icon": "⚡", "name": "Flexible demand coordination", "trigger": "Surrogate demand interpretation", "effect": "Supports coordinated advisory scheduling of flexible load.", "status": "Advisory"},
        ]
    return [
        {"icon": "⚡", "name": "Reschedule flexible demand", "trigger": "Household baseline demand", "effect": "May reduce short peak demand without direct control.", "status": "Advisory"},
        {"icon": "👥", "name": "Maintain baseline monitoring", "trigger": "Stable household context", "effect": "Keeps indoor exposure and energy patterns traceable.", "status": "Monitoring"},
        {"icon": "👁", "name": "Occupancy exposure advisory", "trigger": "Indoor baseline context", "effect": "Maintains advisory awareness without alert escalation.", "status": "Monitoring"},
    ]


OCCUPANT_FEEDBACK_OPTIONS = [
    "Comfortable",
    "Too warm",
    "Air feels poor",
    "Prefer low-energy mode",
    "Reduce exposure",
    "Accept recommendation",
    "Dismiss recommendation",
]


def occupant_feedback_key(runtime_state: dict[str, str]) -> str:
    return f"occupant_feedback_{runtime_state['scenario_id']}"


def occupant_feedback_update(feedback: str, state: dict[str, str], runtime_state: dict[str, str]) -> dict[str, str]:
    pm25_state = state.get("air", "Unavailable")
    filtration_or_vent = "filtered ventilation advisory" if pm25_state in {"Elevated", "High"} else "ventilation / filtration advisory"
    updates = {
        "Comfortable": {
            "received": "Comfortable",
            "interpretation": "Comfort and exposure perception are stable; baseline advisory interpretation is retained.",
            "response": "Maintain current advisory pathway and continued monitoring.",
            "status": "occupant feedback received; no advisory escalation",
            "twin": "Occupant feedback supports stable interpretation.",
        },
        "Too warm": {
            "received": "Too warm",
            "interpretation": "Thermal discomfort priority increased within the advisory prototype.",
            "response": "Prioritise shading / passive cooling advisory.",
            "status": "occupant-informed advisory update",
            "twin": "Thermal discomfort priority increased by occupant feedback.",
        },
        "Air feels poor": {
            "received": "Air feels poor",
            "interpretation": "Air-quality perception priority increased within the advisory prototype.",
            "response": f"Prioritise {filtration_or_vent} depending on PM2.5 interpretation.",
            "status": "occupant-informed air-quality advisory update",
            "twin": "Air-quality priority increased by occupant feedback.",
        },
        "Prefer low-energy mode": {
            "received": "Prefer low-energy mode",
            "interpretation": "Energy-intensive response priority reduced for advisory comparison.",
            "response": "Prefer passive strategies such as shading, demand shifting, and lower-exposure guidance.",
            "status": "low-energy preference applied to advisory interpretation",
            "twin": "Low-energy preference favours passive advisory pathways.",
        },
        "Reduce exposure": {
            "received": "Reduce exposure",
            "interpretation": "Exposure-avoidance priority increased within the advisory prototype.",
            "response": "Prioritise lower-exposure zone / occupancy advisory.",
            "status": "occupant-informed exposure-reduction update",
            "twin": "Exposure reduction priority increased by occupant feedback.",
        },
        "Accept recommendation": {
            "received": "Accept recommendation",
            "interpretation": "Advisory pathway marked as accepted by occupant feedback.",
            "response": "Continue simulated response pathway and monitoring.",
            "status": "advisory pathway accepted by occupant",
            "twin": "Occupant accepted the recommended advisory pathway.",
        },
        "Dismiss recommendation": {
            "received": "Dismiss recommendation",
            "interpretation": "Advisory pathway marked as deferred by occupant feedback.",
            "response": "Maintain monitoring and keep advisory available for later review.",
            "status": "advisory pathway deferred by occupant",
            "twin": "Occupant deferred the recommended advisory pathway.",
        },
    }
    return updates[feedback]


def apply_occupant_feedback_to_actions(
    actions: list[dict[str, str]],
    feedback_update: dict[str, str],
    feedback: str,
) -> list[dict[str, str]]:
    if feedback == "Comfortable":
        return actions
    return [
        {
            "icon": "👤",
            "name": "Occupant-informed advisory",
            "trigger": feedback_update["received"],
            "effect": feedback_update["response"],
            "status": "Simulated feedback",
            "primary": "primary",
        },
        *actions,
    ]


def apply_occupant_feedback_to_feedback_rows(
    rows: list[dict[str, str]],
    feedback_update: dict[str, str],
    feedback: str,
) -> list[dict[str, str]]:
    if feedback == "Comfortable":
        return rows
    return [
        {
            "title": "Occupant feedback",
            "before": feedback_update["received"],
            "intervention": "Advisory interpretation update",
            "after": feedback_update["status"],
        },
        *rows,
    ]


def apply_occupant_feedback_to_updated_state(
    rows: list[dict[str, str]],
    feedback_update: dict[str, str],
    feedback: str,
) -> list[dict[str, str]]:
    tone = "low" if feedback == "Comfortable" else "watch"
    return [
        {
            "title": "Occupant-informed update",
            "value": feedback_update["twin"],
            "tone": tone,
        },
        *rows[:3],
    ]


def simulated_feedback_rows(state: dict[str, str], runtime_state: dict[str, str]) -> list[dict[str, str]]:
    sid = runtime_state["scenario_id"]
    if sid == "S3":
        return [
            {"title": "PM2.5 exposure", "before": "Elevated / High", "intervention": "Filtration + ventilation advisory", "after": "Moderate"},
            {"title": "Thermal stress", "before": "Elevated", "intervention": "Cooling + shading", "after": "Reduced"},
            {"title": "Compound exposure", "before": "Alert", "intervention": "Occupancy guidance", "after": "Watch"},
            {"title": "Health-aware state", "before": "Alert", "intervention": "Compound advisory", "after": "Watch"},
        ]
    if sid == "S4":
        return [
            {"title": "Sensitivity interpretation", "before": "Uncertain", "intervention": "Scenario comparison", "after": "Clarified"},
            {"title": "Ventilation-cooling tradeoff", "before": "Exploratory", "intervention": "Tradeoff analysis", "after": "Explored"},
            {"title": "Scenario resilience", "before": "Baseline", "intervention": "Adaptive planning", "after": "Improved"},
        ]
    if sid == "S2":
        return [
            {"title": "Community load pressure", "before": "Moderate", "intervention": "Demand coordination", "after": "More balanced"},
            {"title": "Demand coordination", "before": "Baseline", "intervention": "Flexible scheduling", "after": "Improved distribution"},
            {"title": "Health-aware state", "before": "Monitoring", "intervention": "Community advisory", "after": "Monitoring"},
        ]
    return [
        {"title": "Household demand", "before": "Moderate", "intervention": "Demand scheduling", "after": "Lower peak"},
        {"title": "Indoor exposure context", "before": "Stable", "intervention": "Baseline monitoring", "after": "Stable"},
        {"title": "Health-aware state", "before": "Stable", "intervention": "Advisory", "after": "Stable"},
    ]


def updated_twin_state(state: dict[str, str], runtime_state: dict[str, str]) -> list[dict[str, str]]:
    sid = runtime_state["scenario_id"]
    if sid == "S3":
        return [
            {"title": "Updated exposure interpretation", "value": "Compound burden reduced to Watch", "tone": "watch"},
            {"title": "Updated intervention priority", "value": "Ventilation and cooling remain primary", "tone": "watch"},
            {"title": "Updated monitoring requirement", "value": "Continue PM2.5 + heat watch", "tone": "watch"},
            {"title": "Updated advisory note", "value": "Maintain occupancy guidance until stressors decline", "tone": "alert"},
        ]
    if sid == "S4":
        return [
            {"title": "Updated exposure interpretation", "value": "Sensitivity remains scenario-dependent", "tone": "watch"},
            {"title": "Updated intervention priority", "value": "Adaptive planning remains primary", "tone": "watch"},
            {"title": "Updated monitoring requirement", "value": "Compare weather-AQ response paths", "tone": "low"},
            {"title": "Updated advisory note", "value": "Use tradeoff interpretation before action", "tone": "watch"},
        ]
    if sid == "S2":
        return [
            {"title": "Updated exposure interpretation", "value": "Community pressure monitored", "tone": "watch"},
            {"title": "Updated intervention priority", "value": "Demand coordination first", "tone": "watch"},
            {"title": "Updated monitoring requirement", "value": "Track load and exposure together", "tone": "low"},
            {"title": "Updated advisory note", "value": "Community response advisory remains active", "tone": "watch"},
        ]
    return [
        {"title": "Updated exposure interpretation", "value": "Baseline state retained", "tone": "low"},
        {"title": "Updated intervention priority", "value": "Flexible demand scheduling optional", "tone": "low"},
        {"title": "Updated monitoring requirement", "value": "Continue baseline observation", "tone": "low"},
        {"title": "Updated advisory note", "value": "No direct actuation; advisory loop only", "tone": "low"},
    ]


def render_reaction_mechanism(state: dict[str, str], runtime_state: dict[str, str]) -> None:
    sid = runtime_state["scenario_id"]
    scenario_rows = {
        "S1": [
            ("1", "Sensing", "Household energy and indoor-context signals enter the CDE."),
            ("2", "Baseline interpretation", "Stable household baseline context is retained."),
            ("3", "Demand-shift advisory", "Flexible demand windows are identified without alert escalation."),
            ("4", "Simulated monitoring", "Baseline and occupancy monitoring remain active."),
            ("5", "Updated state", "Baseline retained with mild peak-reduction potential."),
        ],
        "S2": [
            ("1", "Sensing", "Community load and environmental context enter the CDE."),
            ("2", "Community aggregation", "Signals are interpreted at aggregated community scale."),
            ("3", "Demand monitoring", "Surrogate outputs support demand pressure interpretation."),
            ("4", "Community advisory", "Demand coordination and peak-load monitoring are prioritised."),
            ("5", "Updated state", "Load interpretation is updated for advisory planning."),
        ],
        "S3": [
            ("1", "Sensing", "PM2.5, heat, and load stressors enter the CDE."),
            ("2", "Compound exposure detection", "PM2.5 + heat is classified as a multi-stressor episode."),
            ("3", "Intervention escalation", "Filtration, ventilation, cooling, and occupancy advisory are prioritised."),
            ("4", "Simulated exposure mitigation", "Expected PM2.5 and thermal stress are reduced illustratively."),
            ("5", "Updated watch state", "Health-aware state shifts from Alert toward Watch."),
        ],
        "S4": [
            ("1", "Sensing", "Weather and air-quality variables enter the CDE."),
            ("2", "Sensitivity exploration", "The twin compares weather-AQ response assumptions."),
            ("3", "Tradeoff interpretation", "Ventilation and cooling tradeoffs are interpreted."),
            ("4", "Adaptive planning", "Scenario-based intervention planning is recommended."),
            ("5", "Updated state", "Scenario interpretation is clarified for future advisory use."),
        ],
    }
    rows = scenario_rows[sid]
    html = "".join(
        dedent(
            f"""
            <div class="reaction-step">
                <div class="reaction-icon">{escape(icon)}</div>
                <div class="reaction-title">{escape(title)}</div>
                <div class="reaction-detail">{escape(detail)}</div>
            </div>
            """
        ).strip()
        for icon, title, detail in rows
    )
    st.subheader("Reaction Mechanism")
    st.markdown(f"<div class='reaction-flow'>{html}</div>", unsafe_allow_html=True)


def render_digital_twin_process_strip(state: dict[str, str], runtime_state: dict[str, str]) -> None:
    interventions = healing_interventions(state, runtime_state)
    sid = runtime_state["scenario_id"]
    visual_state = get_scene_visual_state(runtime_state)
    scenario_mode = {
        "S1": "Stable / Baseline / Monitoring",
        "S2": "Community monitoring / Demand pressure",
        "S3": "Alert / Multi-stressor / Exposure mitigation",
        "S4": "Sensitivity / Tradeoff planning",
    }[sid]
    steps = [
        ("↔", "CDE / data fusion", runtime_state["data_mode"]),
        ("+", "Health-aware exposure interpretation", state.get("summary", runtime_state["health_mode"])),
        ("S", "Scenario engine", scenario_mode),
        ("→", "Intervention engine", interventions[0]["name"]),
        ("↻", "Simulated feedback", simulated_feedback_rows(state, runtime_state)[0]["after"]),
    ]
    html = "".join(
        dedent(
            f"""
            <div class="process-pill {'active' if idx == int(visual_state['active_step']) else ''}">
                <div class="process-icon">{escape(icon)}</div>
                <div>
                    <div class="process-title">{escape(title)}</div>
                    <div class="process-detail">{escape(detail)}</div>
                </div>
            </div>
            """
        ).strip()
        for idx, (icon, title, detail) in enumerate(steps, start=1)
    )
    st.subheader("Digital Twin Runtime Pipeline")
    st.markdown(f"<div class='process-strip'>{html}</div>", unsafe_allow_html=True)


def render_spatial_twin_scene(
    runtime_state: dict[str, str],
    exposure_state: dict[str, str] | None = None,
    intervention_state: list[dict[str, str]] | None = None,
) -> None:
    exposure_state = exposure_state or {}
    interventions = intervention_state or healing_interventions(exposure_state, runtime_state)
    sid = runtime_state["scenario_id"]
    scenario_highlights = get_scene_visual_state(runtime_state)
    layout = get_scene_layout(sid)
    visibility = scene_visibility_classes(sid)
    feedback_label = scene_feedback_label(runtime_state)
    st.subheader("Urban Healing Twin View")
    scene_html = f"""
    <style>
    :root {{
        --ink: #1f2933;
        --muted: #607080;
        --line: #d7dee6;
        --blue: #415a77;
        --green: #6f9385;
    }}
    * {{
        box-sizing: border-box;
    }}
    body {{
        margin: 0;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        color: var(--ink);
        background: transparent;
    }}
    .spatial-scene {{
        border: 1px solid var(--line);
        border-radius: 16px;
        background: linear-gradient(135deg, #f7f9fb 0%, #edf3f1 100%);
        padding: 12px;
        width: 100%;
        overflow: hidden;
    }}
    .spatial-scene-stage {{
        position: relative;
        height: 540px;
        border: 1px solid var(--line);
        border-radius: 14px;
        background: #f8fafc;
        overflow: hidden;
    }}
    .spatial-scene-stage.scenario-s1 {{
        background: #f8fbfb;
    }}
    .spatial-scene-stage.scenario-s2 {{
        background: linear-gradient(135deg, #f7f9fb 0%, #eef3f7 100%);
    }}
    .spatial-scene-stage.scenario-s3 {{
        background: linear-gradient(135deg, #fbf8f4 0%, #f5f8fb 100%);
    }}
    .spatial-scene-stage.scenario-s4 {{
        background: linear-gradient(135deg, #f8f8fc 0%, #eef3f7 100%);
    }}
    .indoor-scene,
    .outdoor-scene {{
        position: absolute;
        top: 0;
        bottom: 0;
        width: 50%;
    }}
    .indoor-scene {{
        left: 0;
        background:
            linear-gradient(155deg, rgba(229,219,204,.94) 0%, rgba(245,240,232,.94) 52%, rgba(236,229,219,.94) 52%, rgba(220,207,190,.94) 100%);
    }}
    .outdoor-scene {{
        right: 0;
        background:
            linear-gradient(180deg, rgba(226,236,244,.96) 0%, rgba(238,245,240,.96) 62%, rgba(213,229,214,.96) 62%, rgba(202,222,205,.96) 100%);
    }}
    .room-floor {{
        position: absolute;
        left: 0;
        right: 50%;
        bottom: 0;
        height: 28%;
        background: linear-gradient(145deg, rgba(214,197,177,.82), rgba(232,220,205,.82));
        clip-path: polygon(0 28%, 100% 0, 100% 100%, 0 100%);
        z-index: 1;
    }}
    .ceiling-edge {{
        position: absolute;
        left: 0;
        top: 13%;
        width: 45.5%;
        height: 10px;
        background: rgba(177,164,150,.45);
        border-bottom: 1px solid rgba(120,109,98,.22);
        z-index: 2;
    }}
    .wall-panel {{
        position: absolute;
        left: 5%;
        top: 19%;
        width: 34%;
        height: 44%;
        border: 1px solid rgba(151,139,126,.28);
        border-radius: 10px;
        background: rgba(255,255,255,.18);
        z-index: 2;
    }}
    .door-opening {{
        position: absolute;
        left: 39%;
        top: 46%;
        width: 6%;
        height: 32%;
        border: 2px solid rgba(99,116,132,.32);
        border-bottom: 0;
        border-radius: 8px 8px 0 0;
        background: rgba(232,243,249,.24);
        z-index: 3;
    }}
    .desk-silhouette {{
        position: absolute;
        left: 16%;
        bottom: 18%;
        width: 18%;
        height: 8%;
        border-radius: 8px 8px 2px 2px;
        background: rgba(126,111,92,.24);
        border: 1px solid rgba(126,111,92,.22);
        z-index: 3;
    }}
    .desk-silhouette::before,
    .desk-silhouette::after {{
        content: "";
        position: absolute;
        bottom: -24px;
        width: 6px;
        height: 24px;
        background: rgba(126,111,92,.22);
    }}
    .desk-silhouette::before {{ left: 18%; }}
    .desk-silhouette::after {{ right: 18%; }}
    .indoor-planter {{
        position: absolute;
        left: 4%;
        bottom: 12%;
        width: 7%;
        height: 12%;
        border-radius: 50% 50% 10% 10%;
        background: rgba(116,151,125,.32);
        border-bottom: 12px solid rgba(126,101,80,.32);
        z-index: 3;
    }}
    .hvac-grille {{
        position: absolute;
        left: 30%;
        top: 16%;
        width: 11%;
        height: 5%;
        border: 1px solid rgba(65,90,119,.26);
        border-radius: 7px;
        background: repeating-linear-gradient(90deg, rgba(65,90,119,.18), rgba(65,90,119,.18) 2px, rgba(255,255,255,.45) 2px, rgba(255,255,255,.45) 7px);
        z-index: 4;
    }}
    .light-fixture {{
        position: absolute;
        left: 15%;
        top: 15%;
        width: 13%;
        height: 4%;
        border-radius: 999px;
        background: rgba(255,248,218,.75);
        border: 1px solid rgba(209,194,139,.35);
        box-shadow: 0 10px 28px rgba(222,203,126,.22);
        z-index: 4;
    }}
    .greenery {{
        position: absolute;
        right: 3%;
        bottom: 5%;
        width: 24%;
        height: 22%;
        border-radius: 50% 50% 0 0;
        background: rgba(128,166,139,.38);
        z-index: 2;
    }}
    .lawn-patch {{
        position: absolute;
        right: 1%;
        bottom: 0;
        width: 49%;
        height: 22%;
        background: linear-gradient(180deg, rgba(181,211,184,.45), rgba(141,181,150,.44));
        z-index: 1;
    }}
    .pathway {{
        position: absolute;
        right: 12%;
        bottom: 1%;
        width: 28%;
        height: 34%;
        background: rgba(210,205,190,.55);
        clip-path: polygon(37% 0, 58% 0, 100% 100%, 0 100%);
        z-index: 2;
    }}
    .tree {{
        position: absolute;
        right: 34%;
        bottom: 19%;
        width: 7%;
        height: 22%;
        z-index: 3;
    }}
    .tree::before {{
        content: "";
        position: absolute;
        left: 42%;
        bottom: 0;
        width: 14%;
        height: 44%;
        background: rgba(112,90,65,.28);
        border-radius: 999px;
    }}
    .tree::after {{
        content: "";
        position: absolute;
        left: 0;
        top: 0;
        width: 100%;
        height: 68%;
        border-radius: 50%;
        background: rgba(102,151,115,.46);
        box-shadow: 18px 8px 0 rgba(121,166,132,.35), -12px 12px 0 rgba(112,158,124,.32);
    }}
    .bench {{
        position: absolute;
        right: 20%;
        bottom: 19%;
        width: 13%;
        height: 5%;
        border-radius: 5px;
        background: rgba(112,94,76,.36);
        z-index: 3;
    }}
    .bench::before,
    .bench::after {{
        content: "";
        position: absolute;
        bottom: -13px;
        width: 5px;
        height: 13px;
        background: rgba(112,94,76,.32);
    }}
    .bench::before {{ left: 18%; }}
    .bench::after {{ right: 18%; }}
    .canopy {{
        position: absolute;
        right: 7%;
        top: 47%;
        width: 19%;
        height: 7%;
        border-radius: 999px 999px 4px 4px;
        background: rgba(176,161,118,.34);
        border: 1px solid rgba(146,129,86,.25);
        z-index: 3;
    }}
    .cooling-mist {{
        position: absolute;
        right: 8%;
        top: 56%;
        width: 17%;
        height: 13%;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(206,230,235,.52), rgba(206,230,235,0) 68%);
        z-index: 2;
    }}
    .window-boundary {{
        position: absolute;
        left: 45%;
        top: 8%;
        width: 13%;
        height: 76%;
        border: 4px solid rgba(65,90,119,.46);
        border-radius: 10px;
        background: rgba(232,243,249,.56);
        box-shadow: inset 0 0 0 1px rgba(255,255,255,.72), 0 8px 26px rgba(31,41,51,.08);
        z-index: 4;
    }}
    .window-boundary::before,
    .window-boundary::after {{
        content: "";
        position: absolute;
        background: rgba(65,90,119,.32);
    }}
    .window-boundary::before {{
        left: 50%;
        top: 0;
        bottom: 0;
        width: 2px;
    }}
    .window-boundary::after {{
        left: 0;
        right: 0;
        top: 48%;
        height: 2px;
    }}
    .scene-label {{
        position: absolute;
        top: 12px;
        border: 1px solid var(--line);
        border-radius: 999px;
        background: rgba(255,255,255,.86);
        color: var(--blue);
        padding: 4px 10px;
        font-size: 12px;
        font-weight: 800;
        z-index: 6;
    }}
    .scene-label.indoor {{ left: 12px; }}
    .scene-label.outdoor {{ right: 12px; }}
    .scene-object,
    .endpoint-object,
    .stressor-object {{
        position: absolute;
        border: 1px solid var(--line);
        border-radius: 12px;
        background: rgba(255,255,255,.92);
        padding: 6px 8px;
        color: var(--ink);
        font-size: 12px;
        font-weight: 760;
        line-height: 1.18;
        box-shadow: 0 5px 15px rgba(31,41,51,.07);
        z-index: 5;
    }}
    .scene-object.active,
    .endpoint-object.active,
    .stressor-object.active {{
        border-color: #8db29f;
        background: #f7fbf8;
        box-shadow: 0 0 0 3px rgba(111,147,133,.18), 0 5px 15px rgba(31,41,51,.08);
    }}
    .stressor-object.alert {{
        border-color: #bd7a72;
        background: #fff7f5;
        box-shadow: 0 0 0 3px rgba(189,122,114,.16), 0 5px 15px rgba(31,41,51,.08);
    }}
    .scene-object.calm,
    .endpoint-object.calm {{
        border-color: #9db9af;
        background: #f7fbf8;
        box-shadow: 0 0 0 2px rgba(111,147,133,.12), 0 5px 15px rgba(31,41,51,.06);
    }}
    .scene-object.subtle,
    .scene-object.deemphasised,
    .endpoint-object.subtle,
    .endpoint-object.deemphasised,
    .stressor-object.subtle,
    .stressor-object.deemphasised {{
        opacity: .24;
        filter: saturate(.65);
        box-shadow: none;
    }}
    .scene-hidden {{
        display: none !important;
    }}
    .endpoint-object.load-focus,
    .stressor-object.load-focus {{
        border-color: #7f96b0;
        background: #f5f8fb;
        box-shadow: 0 0 0 3px rgba(88,114,143,.14), 0 5px 15px rgba(31,41,51,.08);
    }}
    .endpoint-object.sensitivity,
    .stressor-object.sensitivity {{
        border-color: #8e86b4;
        background: #f8f7fc;
        box-shadow: 0 0 0 3px rgba(111,111,150,.13), 0 5px 15px rgba(31,41,51,.08);
    }}
    .scenario-s2 .flow-line {{
        background: rgba(88,114,143,.48);
    }}
    .scenario-s3 .outdoor-scene {{
        background:
            radial-gradient(circle at 72% 20%, rgba(189,122,114,.18), transparent 28%),
            radial-gradient(circle at 82% 30%, rgba(213,151,91,.20), transparent 24%),
            linear-gradient(180deg, rgba(229,235,240,.96) 0%, rgba(239,241,235,.96) 62%, rgba(215,224,203,.96) 62%, rgba(202,222,205,.96) 100%);
    }}
    .scenario-s3 .window-boundary {{
        box-shadow: inset 0 0 0 1px rgba(255,255,255,.72), 0 0 0 4px rgba(189,122,114,.12), 0 8px 26px rgba(31,41,51,.08);
    }}
    .episode-banner {{
        position: absolute;
        left: 50%;
        top: 10px;
        transform: translateX(-50%);
        border: 1px solid rgba(65,90,119,.24);
        border-radius: 999px;
        background: rgba(255,255,255,.86);
        color: var(--blue);
        padding: 5px 12px;
        font-size: 12px;
        font-weight: 850;
        z-index: 8;
        box-shadow: 0 5px 16px rgba(31,41,51,.08);
    }}
    .scenario-s3 .episode-banner {{
        color: #8f4f47;
        border-color: rgba(189,122,114,.38);
        background: rgba(255,247,245,.92);
    }}
    .scenario-s4 .outdoor-scene {{
        background:
            radial-gradient(circle at 78% 25%, rgba(111,111,150,.15), transparent 27%),
            linear-gradient(180deg, rgba(231,235,246,.96) 0%, rgba(240,243,242,.96) 62%, rgba(218,226,216,.96) 62%, rgba(205,222,209,.96) 100%);
    }}
    .scenario-s4 .episode-banner {{
        color: #565684;
        border-color: rgba(111,111,150,.36);
        background: rgba(248,247,252,.92);
    }}
    .card-text {{
        color: var(--muted);
        font-size: 11px;
        font-weight: 600;
    }}
    .status-chip {{
        display: inline-block;
        border: 1px solid var(--line);
        border-radius: 999px;
        background: #eef3f7;
        color: var(--blue);
        padding: 3px 8px;
        font-size: 11px;
        font-weight: 800;
    }}
    .feedback-pill {{
        position: absolute;
        border: 1px solid rgba(65,90,119,.24);
        border-radius: 999px;
        background: rgba(255,255,255,.9);
        color: var(--blue);
        padding: 7px 12px;
        font-size: 12px;
        font-weight: 820;
        line-height: 1.2;
        text-align: center;
        box-shadow: 0 5px 16px rgba(31,41,51,.08);
        z-index: 7;
    }}
    .flow-line {{
        position: absolute;
        height: 2px;
        background: rgba(65,90,119,.38);
        z-index: 7;
    }}
    .flow-line::after {{
        content: "";
        position: absolute;
        right: -1px;
        top: -4px;
        border-left: 8px solid rgba(65,90,119,.55);
        border-top: 5px solid transparent;
        border-bottom: 5px solid transparent;
    }}
    .flow-sensing {{ left: 24%; top: 40%; width: 22%; }}
    .flow-intervention {{ left: 58%; top: 40%; width: 28%; }}
    .flow-feedback {{
        left: 55%;
        top: 84%;
        width: 30%;
        transform: rotate(180deg);
        opacity: .68;
    }}
    .scene-note {{
        margin-top: 10px;
        color: var(--muted);
        font-size: 13px;
        line-height: 1.38;
    }}
    @media (max-width: 760px) {{
        .spatial-scene-stage {{ height: 780px; }}
        .indoor-scene,
        .outdoor-scene {{
            left: 0;
            right: 0;
            width: 100%;
            height: 50%;
        }}
        .indoor-scene {{ top: 0; bottom: auto; }}
        .outdoor-scene {{ top: 50%; bottom: 0; }}
        .room-floor {{ right: 0; bottom: 50%; height: 14%; }}
        .window-boundary {{ left: 10%; top: 43%; width: 80%; height: 13%; }}
        .flow-line {{ display: none; }}
    }}
    </style>

    <div class="spatial-scene">
        <div class="spatial-scene-stage {escape(scenario_highlights["scene"])}">
            <div class="indoor-scene"></div>
            <div class="outdoor-scene"></div>
            <div class="room-floor"></div>
            <div class="ceiling-edge"></div>
            <div class="wall-panel"></div>
            <div class="door-opening"></div>
            <div class="desk-silhouette"></div>
            <div class="indoor-planter"></div>
            <div class="hvac-grille"></div>
            <div class="light-fixture"></div>
            <div class="lawn-patch"></div>
            <div class="pathway"></div>
            <div class="tree"></div>
            <div class="bench"></div>
            <div class="canopy"></div>
            <div class="cooling-mist"></div>
            <div class="greenery"></div>
            <div class="window-boundary" title="Window / façade boundary"></div>
            <div class="episode-banner">{escape(scenario_highlights["scenario_banner"])}</div>
            <div class="scene-label indoor">Indoor environment</div>
            <div class="scene-label outdoor">Outdoor exposure context</div>

            <div class="scene-object {escape(scenario_highlights["indoor"])} {escape(visibility["occupancy"])}" style="{escape(layout["occupancy"])}">👥 Occupancy<br><span class="card-text">human presence</span></div>
            <div class="scene-object {escape(scenario_highlights["indoor"])} {escape(visibility["indoor_sensing"])}" style="{escape(layout["indoor_sensing"])}">📡 Indoor sensing</div>
            <div class="endpoint-object {escape(scenario_highlights["vent"])} {escape(visibility["ventilation"])}" style="{escape(layout["ventilation"])}">🌬 Ventilation inlet/outlet</div>
            <div class="endpoint-object {escape(scenario_highlights["filter"])} {escape(visibility["filtration"])}" style="{escape(layout["filtration"])}">🧰 Air filtration</div>
            <div class="endpoint-object {escape(scenario_highlights["cool"])} {escape(visibility["cooling"])}" style="{escape(layout["cooling"])}">❄ Passive cooling</div>
            <div class="endpoint-object {escape(visibility["lighting"])}" style="{escape(layout["lighting"])}">💡 Lighting</div>
            <div class="endpoint-object {escape(scenario_highlights["demand"])} {escape(visibility["demand"])}" style="{escape(layout["demand"])}">⚡ Demand-response scheduling</div>
            <div class="endpoint-object {escape(scenario_highlights["occupancy"])} {escape(visibility["occupancy_advisory"])}" style="{escape(layout["occupancy_advisory"])}">👁 Occupancy advisory</div>

            <div class="stressor-object {escape(scenario_highlights["pm25"])} {escape(visibility["pm25"])}" style="{escape(layout["pm25"])}">🌫 PM2.5 cloud</div>
            <div class="stressor-object {escape(scenario_highlights["heat"])} {escape(visibility["heat"])}" style="{escape(layout["heat"])}">🌡 Heat marker</div>
            <div class="stressor-object {escape(scenario_highlights["weather"])} {escape(visibility["weather"])}" style="{escape(layout["weather"])}">🍃 Wind / airflow</div>
            <div class="stressor-object {escape(scenario_highlights["green"])} {escape(visibility["greenery"])}" style="{escape(layout["greenery"])}">🌿 Green refuge</div>
            <div class="stressor-object {escape(scenario_highlights["hotspot"])} {escape(visibility["hotspot"])}" style="{escape(layout["hotspot"])}">📍 {escape(scenario_highlights["warning"])}</div>

            <div class="endpoint-object {escape(scenario_highlights["vent"])} {escape(visibility["vent_advisory"])}" style="{escape(layout["vent_advisory"])}">🌬 Ventilation advisory</div>
            <div class="endpoint-object {escape(scenario_highlights["cool"])} {escape(visibility["cool_advisory"])}" style="{escape(layout["cool_advisory"])}">🌞 Cooling advisory</div>
            <div class="endpoint-object {escape(scenario_highlights["green"])} {escape(visibility["green_zone"])}" style="{escape(layout["green_zone"])}">🌿 Lower-exposure zone</div>
            <div class="feedback-pill" style="{escape(layout["feedback"])}">↻ {escape(feedback_label)}</div>

            <div class="flow-line flow-sensing"></div>
            <div class="flow-line flow-intervention"></div>
            <div class="flow-line flow-feedback"></div>
        </div>
        <div class="scene-note">
            This spatial twin scene situates the digital twin between monitored indoor space and outdoor exposure context, showing how harmonised environmental conditions are translated into advisory-level intervention pathways.
        </div>
    </div>
    """
    components.html(scene_html, height=630, scrolling=False)


def render_twin_context_view(state: dict[str, str], runtime_state: dict[str, str]) -> None:
    render_spatial_twin_scene(runtime_state, state, healing_interventions(state, runtime_state))


def trace_steps(runtime_state: dict[str, str]) -> list[str]:
    sid = runtime_state["scenario_id"]
    if sid == "S1":
        return ["UK-DALE", "CDE", "Household surrogate", "End-use baseline", "Demand-shift advisory"]
    if sid == "S2":
        return ["Community load", "CDE", "Community surrogate", "Demand monitoring", "Community response advisory"]
    if sid == "S3":
        return ["PM2.5 + weather + load", "CDE", "Multi-stressor episode", "Compound exposure", "Ventilation / cooling advisory"]
    return ["Weather-AQ variables", "CDE", "Sensitivity analysis", "Tradeoff interpretation", "Scenario-based advisory"]


def render_traceability(runtime_state: dict[str, str], title: str = "Digital Thread / Traceability") -> None:
    st.subheader(title)
    html = "".join(
        dedent(
            f"""
        <div class="trace-step">
            <div class="trace-index">{idx}</div>
            <div class="card-title">{escape(step)}</div>
        </div>
        """
        ).strip()
        for idx, step in enumerate(trace_steps(runtime_state), start=1)
    )
    st.markdown(f"<div class='trace-row'>{html}</div>", unsafe_allow_html=True)


def scenario_purpose(runtime_state: dict[str, str]) -> dict[str, str]:
    purposes = {
        "S1": {
            "scenario": "S1 Household",
            "purpose": "Demonstrates household baseline interpretation and end-use advisory logic.",
            "data": "UK-DALE energy + indoor-context proxy",
            "response": "Demand-shift advisory / baseline monitoring",
        },
        "S2": {
            "scenario": "S2 Community",
            "purpose": "Demonstrates community-scale surrogate monitoring and demand coordination.",
            "data": "Community load + environmental context",
            "response": "Community demand-response advisory",
        },
        "S3": {
            "scenario": "S3 Multi-Stressor",
            "purpose": "Demonstrates compound PM2.5 + heat episode interpretation and intervention escalation.",
            "data": "PM2.5 + temperature + load",
            "response": "Filtration / cooling / occupancy advisory",
        },
        "S4": {
            "scenario": "S4 Weather-AQ",
            "purpose": "Demonstrates weather-air-quality sensitivity exploration and adaptive intervention planning.",
            "data": "Weather + air-quality variables",
            "response": "Ventilation-cooling tradeoff / adaptive planning",
        },
    }
    return purposes[runtime_state["scenario_id"]]


def render_scenario_purpose(runtime_state: dict[str, str]) -> None:
    purpose = scenario_purpose(runtime_state)
    cards = [
        ("Scenario", purpose["scenario"]),
        ("Purpose", purpose["purpose"]),
        ("Primary data layer", purpose["data"]),
        ("Primary intervention logic", purpose["response"]),
    ]
    html = "".join(
        dedent(
            f"""
            <div class="purpose-mini-card">
                <div class="purpose-label">{escape(label)}</div>
                <div class="card-text">{escape(value)}</div>
            </div>
            """
        ).strip()
        for label, value in cards
    )
    st.markdown(
        dedent(
            f"""
            <div class="scenario-purpose-card">
                <div class="section-title">Scenario Purpose</div>
                <div class="scenario-purpose-grid">{html}</div>
            </div>
            """
        ).strip(),
        unsafe_allow_html=True,
    )


def data_to_decision_steps(runtime_state: dict[str, str]) -> list[str]:
    traces = {
        "S1": [
            "UK-DALE energy data",
            "CDE harmonisation",
            "Household surrogate",
            "End-use baseline interpretation",
            "Demand-shift advisory",
            "Simulated baseline retained / lower peak",
        ],
        "S2": [
            "Community load data",
            "CDE harmonisation",
            "Community surrogate",
            "Demand monitoring",
            "Community demand-response advisory",
            "Improved load distribution",
        ],
        "S3": [
            "PM2.5 + weather + load",
            "CDE harmonisation",
            "Multi-stressor episode interpretation",
            "Compound exposure state",
            "Filtration / cooling / occupancy advisory",
            "Simulated risk reduction",
        ],
        "S4": [
            "Weather + air-quality variables",
            "CDE harmonisation",
            "Sensitivity exploration",
            "Ventilation-cooling tradeoff interpretation",
            "Adaptive intervention planning",
            "Updated scenario interpretation",
        ],
    }
    return traces[runtime_state["scenario_id"]]


def render_data_to_decision_trace(runtime_state: dict[str, str]) -> None:
    html = "".join(
        dedent(
            f"""
            <div class="decision-trace-step">
                <div class="trace-label">Step {idx}</div>
                <div class="card-title">{escape(step)}</div>
            </div>
            """
        ).strip()
        for idx, step in enumerate(data_to_decision_steps(runtime_state), start=1)
    )
    st.markdown(
        dedent(
            f"""
            <div class="decision-trace-panel">
                <div class="section-title">Why this recommendation?</div>
                <div class="section-subtitle">This trace illustrates the data-to-decision pathway used by the advisory digital twin.</div>
                <div class="decision-trace-grid">{html}</div>
            </div>
            """
        ).strip(),
        unsafe_allow_html=True,
    )


def render_prototype_scope_panel() -> None:
    included = [
        "CDE harmonisation of secondary datasets",
        "Scenario-aware exposure interpretation",
        "Advisory intervention logic",
        "Human-in-the-loop feedback",
        "Operator review",
        "Simulated feedback closure",
    ]
    excluded = [
        "Real-time IoT deployment",
        "Direct HVAC/device control",
        "Clinical diagnosis or medical treatment",
        "Measured post-intervention validation",
        "Personal health profiling",
        "Automated actuation",
    ]

    def list_items(items: list[str]) -> str:
        return "".join(f"<li>{escape(item)}</li>" for item in items)

    st.markdown(
        dedent(
            f"""
            <div class="scope-panel">
                <div class="section-title">Prototype Scope / System Boundary</div>
                <div class="section-subtitle">
                    This demonstrator uses harmonised secondary datasets and precomputed surrogate outputs to emulate a health-aware Urban CPS Digital Twin workflow.
                    It does not perform live sensing, direct actuation, or clinical health diagnosis.
                </div>
                <div class="scope-grid">
                    <div class="scope-card">
                        <div class="card-title">Included</div>
                        <ul>{list_items(included)}</ul>
                    </div>
                    <div class="scope-card">
                        <div class="card-title">Not included</div>
                        <ul>{list_items(excluded)}</ul>
                    </div>
                </div>
            </div>
            """
        ).strip(),
        unsafe_allow_html=True,
    )


def control_level_for_endpoint(endpoint: str) -> str:
    name = endpoint.lower()
    if "demand-response" in name or "scheduling" in name:
        return "Operator scheduling"
    if "monitoring" in name or "peak-load" in name or "baseline" in name:
        return "Monitoring only"
    if "bems" in name or "iot" in name:
        return "Future BEMS/IoT-ready"
    if "shading" in name or "cooling" in name or "passive" in name:
        return "Simulated response"
    return "Advisory signal"


def urban_health_status(runtime_state: dict[str, str]) -> dict[str, str]:
    status = {
        "S1": ("🟢", "Stable", "Household baseline context with moderate energy demand.", "low"),
        "S2": ("🟡", "Moderate Demand Pressure", "Community monitoring indicates aggregated demand pressure.", "moderate"),
        "S3": ("🔴", "Elevated Compound Exposure", "PM2.5 and heat stress are interpreted as coupled exposure pressure.", "high"),
        "S4": ("🟠", "Environmental Sensitivity", "Weather-air-quality interactions are under scenario exploration.", "elevated"),
    }
    icon, value, detail, tone = status[runtime_state["scenario_id"]]
    return {"icon": icon, "value": value, "detail": detail, "tone": tone}


def render_urban_health_status(runtime_state: dict[str, str]) -> None:
    status = urban_health_status(runtime_state)
    st.markdown(
        dedent(
            f"""
            <div class="health-status-card {escape(status["tone"])}">
                <div class="health-status-icon">{escape(status["icon"])}</div>
                <div>
                    <div class="health-status-label">Urban Health Status</div>
                    <div class="health-status-value">{escape(status["value"])}</div>
                    <div class="health-status-detail">{escape(status["detail"])}</div>
                </div>
            </div>
            """
        ).strip(),
        unsafe_allow_html=True,
    )


def exposure_map_zones(runtime_state: dict[str, str]) -> list[dict[str, str]]:
    sid = runtime_state["scenario_id"]
    zones = [
        {"key": "north", "name": "North District", "label": "Low exposure watch", "level": "low", "marker": "🟢"},
        {"key": "central", "name": "Central Business Area", "label": "Moderate monitoring", "level": "moderate", "marker": "🟡"},
        {"key": "residential", "name": "Residential Zone", "label": "Residential baseline", "level": "low", "marker": "🟢"},
        {"key": "industrial", "name": "Industrial Zone", "label": "Elevated emissions context", "level": "elevated", "marker": "🟠"},
        {"key": "south", "name": "South District", "label": "Community monitoring", "level": "moderate", "marker": "🟡"},
    ]
    scenario_updates = {
        "S1": ("residential", "Household baseline context", "low", "🟢"),
        "S2": ("south", "Community demand hotspot", "moderate", "🟡"),
        "S3": ("central", "Compound exposure hotspot", "high", "🔴"),
        "S4": ("industrial", "Weather–AQ interaction zone", "elevated", "🟠"),
    }
    active_key, label, level, marker = scenario_updates[sid]
    for zone in zones:
        zone["active"] = "active" if zone["key"] == active_key else ""
        if zone["key"] == active_key:
            zone["label"] = label
            zone["level"] = level
            zone["marker"] = marker
    return zones


def render_urban_exposure_map(runtime_state: dict[str, str]) -> None:
    st.subheader("Urban Exposure Map")
    zone_html = "".join(
        dedent(
            f"""
            <div class="urban-zone zone-{escape(zone["key"])} {escape(zone["active"])}">
                <div class="zone-title">{escape(zone["name"])}</div>
                <div class="zone-label">{escape(zone["label"])}</div>
                <div class="hotspot-marker marker-{escape(zone["level"])}">{escape(zone["marker"])}</div>
            </div>
            """
        ).strip()
        for zone in exposure_map_zones(runtime_state)
    )
    st.markdown(
        f"""
        <div class="urban-map">
            <div class="urban-map-grid">{zone_html}</div>
            <div class="map-legend">
                <span>🟢 Low</span>
                <span>🟡 Moderate</span>
                <span>🟠 Elevated</span>
                <span>🔴 High</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("The spatial layer provides an interpretable representation of environmental exposure and intervention priority areas.")


def cuboid_mesh_trace(x: float, y: float, width: float, depth: float, height: float, color: str, name: str, opacity: float = 0.82) -> go.Mesh3d:
    vertices = [(x, y, 0), (x + width, y, 0), (x + width, y + depth, 0), (x, y + depth, 0), (x, y, height), (x + width, y, height), (x + width, y + depth, height), (x, y + depth, height)]
    vx, vy, vz = zip(*vertices)
    return go.Mesh3d(
        x=vx,
        y=vy,
        z=vz,
        i=[0, 0, 0, 4, 4, 1, 2, 3, 0, 1, 2, 3],
        j=[1, 2, 3, 5, 6, 5, 6, 7, 4, 5, 6, 7],
        k=[2, 3, 0, 6, 7, 6, 7, 4, 5, 6, 7, 4],
        color=color,
        opacity=opacity,
        flatshading=True,
        name=name,
        hovertemplate=f"{name}<br>synthetic building mass<extra></extra>",
        showscale=False,
    )


def synthetic_london_context_buildings() -> list[dict[str, float | str]]:
    return [
        {"x": 0, "y": 0, "w": 0.9, "d": 1.8, "h": 0.8, "zone": "Residential"}, {"x": 1.2, "y": 0.2, "w": 0.7, "d": 1.4, "h": 1.1, "zone": "Residential"}, {"x": 2.2, "y": 0.1, "w": 1.0, "d": 1.6, "h": 1.0, "zone": "Residential"},
        {"x": 3.8, "y": 0.2, "w": 1.0, "d": 1.5, "h": 2.4, "zone": "Central"}, {"x": 5.0, "y": 0.0, "w": 0.8, "d": 1.7, "h": 3.0, "zone": "Central"}, {"x": 6.1, "y": 0.4, "w": 1.2, "d": 1.3, "h": 2.1, "zone": "Central"},
        {"x": 7.8, "y": 0.1, "w": 1.4, "d": 1.8, "h": 1.3, "zone": "Industrial"}, {"x": 9.5, "y": 0.3, "w": 1.1, "d": 1.5, "h": 1.5, "zone": "Industrial"},
        {"x": 0.4, "y": 2.5, "w": 1.2, "d": 1.2, "h": 0.9, "zone": "North District"}, {"x": 2.1, "y": 2.3, "w": 0.9, "d": 1.4, "h": 1.2, "zone": "North District"},
        {"x": 3.5, "y": 2.4, "w": 1.0, "d": 1.2, "h": 2.2, "zone": "Central"}, {"x": 4.8, "y": 2.2, "w": 1.1, "d": 1.4, "h": 2.8, "zone": "Central"}, {"x": 6.3, "y": 2.6, "w": 0.9, "d": 1.1, "h": 1.9, "zone": "Central"},
        {"x": 8.0, "y": 2.4, "w": 1.3, "d": 1.3, "h": 1.5, "zone": "Industrial"}, {"x": 9.7, "y": 2.2, "w": 0.9, "d": 1.4, "h": 1.1, "zone": "South District"},
        {"x": 0.1, "y": 4.5, "w": 1.1, "d": 1.5, "h": 0.7, "zone": "Residential"}, {"x": 1.7, "y": 4.6, "w": 1.0, "d": 1.2, "h": 1.0, "zone": "Residential"},
        {"x": 3.2, "y": 4.3, "w": 1.1, "d": 1.5, "h": 1.7, "zone": "Central"}, {"x": 4.7, "y": 4.5, "w": 1.0, "d": 1.2, "h": 2.5, "zone": "Central"}, {"x": 6.2, "y": 4.4, "w": 1.3, "d": 1.5, "h": 1.6, "zone": "Community"},
        {"x": 8.0, "y": 4.6, "w": 1.1, "d": 1.2, "h": 1.0, "zone": "South District"}, {"x": 9.5, "y": 4.4, "w": 1.2, "d": 1.5, "h": 0.9, "zone": "South District"},
    ]


def map_nodes(runtime_state: dict[str, str]) -> list[dict[str, float | str]]:
    focus = {
        "S1": (1.1, 5.0, "Household baseline focus", "#6f9385"),
        "S2": (6.8, 5.1, "Community demand hotspot", "#c5ad55"),
        "S3": (8.8, 2.9, "Compound PM2.5 + heat hotspot", "#a15f5f"),
        "S4": (4.8, 1.2, "Weather-AQ sensitivity region", "#b86f4c"),
    }[runtime_state["scenario_id"]]
    return [
        {"x": 0.6, "y": 0.6, "z": 1.0, "label": "Streetlight - NB-IoT", "color": "#c69a42"},
        {"x": 2.6, "y": 1.8, "z": 1.3, "label": "Air quality - LoRaWAN", "color": "#3f8f8b"},
        {"x": 4.5, "y": 2.2, "z": 3.2, "label": "CCTV - Wi-Fi / Cellular", "color": "#b35b7e"},
        {"x": 6.8, "y": 3.6, "z": 2.0, "label": "Gateway - Cellular", "color": "#5a5fa8"},
        {"x": 9.0, "y": 1.8, "z": 1.7, "label": "Air quality - LoRaWAN", "color": "#3f8f8b"},
        {"x": focus[0], "y": focus[1], "z": 2.8, "label": focus[2], "color": focus[3]},
    ]


def render_3d_urban_twin_map(runtime_state: dict[str, str]) -> None:
    scenario_focus = {
        "S1": {
            "label": "Household baseline focus",
            "x": -4.2,
            "z": 2.4,
            "color": "#6f9385",
            "note": "Residential exposure and end-use baseline context",
        },
        "S2": {
            "label": "Community demand hotspot",
            "x": 2.3,
            "z": 2.2,
            "color": "#c5ad55",
            "note": "Aggregated demand-monitoring area",
        },
        "S3": {
            "label": "Compound PM2.5 + heat hotspot",
            "x": 4.5,
            "z": -1.6,
            "color": "#a15f5f",
            "note": "High PM2.5 and high temperature watch",
        },
        "S4": {
            "label": "Weather-AQ sensitivity region",
            "x": -0.6,
            "z": -2.1,
            "color": "#b86f4c",
            "note": "Weather-air-quality interaction sensitivity",
        },
    }[runtime_state["scenario_id"]]

    st.subheader("3D Urban Twin Map")
    st.caption(
        "Schematic London-context 3D city layer for exposure interpretation and advisory intervention priority. "
        "Weather and air-quality context use London secondary environmental data; buildings and node locations are synthetic for demonstration."
    )

    safe_label = escape(scenario_focus["label"])
    safe_note = escape(scenario_focus["note"])
    scene_html = r'''
<div class="three-map-shell">
  <div id="three-map-canvas"></div>
  <div class="three-map-title">
    <strong>London-context Urban Exposure Twin</strong>
    <span>synthetic 3D spatial demonstrator</span>
  </div>
  <div class="three-map-scenario">
    <div class="scenario-dot"></div>
    <div>
      <strong>__FOCUS_LABEL__</strong>
      <span>__FOCUS_NOTE__</span>
    </div>
  </div>
  <div class="three-map-legend">
    <div><span class="node street"></span>Streetlight / NB-IoT</div>
    <div><span class="node aq"></span>Air quality / LoRaWAN</div>
    <div><span class="node cctv"></span>CCTV / Wi-Fi / Cellular</div>
    <div><span class="node gateway"></span>Gateway / Cellular</div>
  </div>
  <div class="three-map-caption">Schematic 3D layer only. The environmental data context is London-based; geometry and device locations are synthetic.</div>
</div>

<style>
  .three-map-shell {
    position: relative;
    width: 100%;
    height: 640px;
    overflow: hidden;
    border: 1px solid #d7dee6;
    border-radius: 18px;
    background: linear-gradient(180deg, #f7f9fb 0%, #eef3f6 100%);
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  }
  #three-map-canvas { position: absolute; inset: 0; }
  .three-map-title, .three-map-scenario, .three-map-legend, .three-map-caption {
    position: absolute;
    z-index: 5;
    background: rgba(255, 255, 255, 0.78);
    border: 1px solid rgba(190, 202, 214, 0.76);
    box-shadow: 0 14px 34px rgba(80, 96, 112, 0.13);
    backdrop-filter: blur(10px);
    color: #1f2933;
  }
  .three-map-title {
    top: 22px;
    left: 24px;
    padding: 16px 18px;
    border-radius: 12px;
    min-width: 280px;
  }
  .three-map-title strong { display: block; font-size: 20px; letter-spacing: 0; }
  .three-map-title span { display: block; margin-top: 4px; color: #667789; font-size: 14px; }
  .three-map-scenario {
    top: 22px;
    right: 24px;
    display: flex;
    gap: 12px;
    align-items: center;
    max-width: 360px;
    padding: 14px 16px;
    border-radius: 999px;
  }
  .three-map-scenario strong { display: block; font-size: 15px; }
  .three-map-scenario span { display: block; color: #667789; font-size: 12px; margin-top: 2px; }
  .scenario-dot {
    width: 18px;
    height: 18px;
    border-radius: 999px;
    background: __FOCUS_COLOR__;
    box-shadow: 0 0 0 8px color-mix(in srgb, __FOCUS_COLOR__ 22%, transparent);
    flex: 0 0 auto;
  }
  .three-map-legend {
    left: 24px;
    bottom: 56px;
    padding: 14px 16px;
    border-radius: 12px;
    display: grid;
    gap: 9px;
    color: #405367;
    font-size: 13px;
  }
  .three-map-legend div { display: flex; align-items: center; gap: 10px; }
  .node { width: 11px; height: 11px; border-radius: 50%; display: inline-block; box-shadow: 0 0 0 3px rgba(255,255,255,.85); }
  .street { background: #c69a42; }
  .aq { background: #3f8f8b; }
  .cctv { background: #b35b7e; }
  .gateway { background: #5a5fa8; }
  .three-map-caption {
    right: 24px;
    bottom: 24px;
    max-width: 520px;
    padding: 11px 14px;
    border-radius: 999px;
    color: #607080;
    font-size: 12px;
  }
  @media (max-width: 900px) {
    .three-map-shell { height: 700px; }
    .three-map-scenario { left: 24px; right: 24px; top: 96px; border-radius: 14px; }
    .three-map-caption { left: 24px; right: 24px; border-radius: 14px; }
  }
</style>

<script type="importmap">
  {"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","OrbitControls":"https://unpkg.com/three@0.160.0/examples/jsm/controls/OrbitControls.js"}}
</script>
<script type="module">
  import * as THREE from 'three';
  import { OrbitControls } from 'OrbitControls';

  const container = document.getElementById('three-map-canvas');
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0xf7f9fb);
  scene.fog = new THREE.Fog(0xf7f9fb, 11, 26);

  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  container.appendChild(renderer.domElement);

  const camera = new THREE.PerspectiveCamera(42, 1, 0.1, 100);
  camera.position.set(7.5, 8.5, 9.5);
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.target.set(0, 0.6, 0);
  controls.enableDamping = true;
  controls.autoRotate = true;
  controls.autoRotateSpeed = 0.22;
  controls.maxPolarAngle = Math.PI * 0.46;
  controls.minDistance = 7;
  controls.maxDistance = 18;

  scene.add(new THREE.HemisphereLight(0xffffff, 0xd9e2e8, 2.2));
  const sun = new THREE.DirectionalLight(0xffffff, 2.6);
  sun.position.set(7, 12, 6);
  sun.castShadow = true;
  sun.shadow.mapSize.set(2048, 2048);
  scene.add(sun);

  const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(14, 9),
    new THREE.MeshStandardMaterial({ color: 0xf0f4f6, roughness: 0.95, metalness: 0.0 })
  );
  ground.rotation.x = -Math.PI / 2;
  ground.receiveShadow = true;
  scene.add(ground);

  function mat(color, opacity = 1) {
    return new THREE.MeshStandardMaterial({ color, roughness: 0.82, metalness: 0.02, transparent: opacity < 1, opacity });
  }
  const buildingMats = [mat(0xd7e1e6, 0.94), mat(0xcbd6df, 0.94), mat(0xe0e8ea, 0.94), mat(0xc5d0d8, 0.94)];
  const edgeMat = new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.42 });

  const buildings = [
    [-5.4,-2.8,.8,1.4,.75],[-4.2,-2.6,.7,1.1,1.0],[-3.0,-2.7,.9,1.3,.95],[-1.2,-2.5,.85,1.2,2.4],[0.0,-2.8,.75,1.4,3.0],[1.2,-2.4,1.0,1.1,2.1],[3.2,-2.6,1.2,1.5,1.3],[4.8,-2.5,1.0,1.3,1.55],
    [-5.0,-.7,1.1,1.0,.85],[-3.5,-.8,.8,1.1,1.2],[-1.8,-.7,.9,1.0,2.1],[-.3,-.8,1.0,1.2,2.7],[1.2,-.5,.8,.95,1.85],[3.4,-.7,1.1,1.1,1.45],[4.9,-.8,.8,1.1,1.05],
    [-5.2,1.6,1.1,1.2,.7],[-3.8,1.7,.9,1.0,1.0],[-2.2,1.5,1.0,1.2,1.65],[-.6,1.7,.9,1.0,2.45],[1.0,1.5,1.2,1.2,1.55],[2.8,1.7,1.0,1.0,.95],[4.4,1.5,1.1,1.2,.85],[-.2,3.25,.9,1.0,1.4],[1.4,3.15,1.0,1.1,1.2]
  ];
  buildings.forEach((b, i) => {
    const [x,z,w,d,h] = b;
    const mesh = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), buildingMats[i % buildingMats.length]);
    mesh.position.set(x, h / 2, z);
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    scene.add(mesh);
    const edges = new THREE.LineSegments(new THREE.EdgesGeometry(mesh.geometry), edgeMat);
    edges.position.copy(mesh.position);
    scene.add(edges);
  });

  function addRoad(x, z, w, d, rot = 0) {
    const road = new THREE.Mesh(new THREE.PlaneGeometry(w, d), mat(0xe8eef2));
    road.rotation.x = -Math.PI / 2;
    road.rotation.z = rot;
    road.position.set(x, 0.012, z);
    scene.add(road);
  }
  addRoad(0, -1.55, 12.5, .26); addRoad(0, .78, 12.5, .26); addRoad(-2.55, 0, .25, 7.3); addRoad(2.45, 0, .25, 7.3); addRoad(.1, 3.05, 8.5, .22, .14);

  function addPark(x, z, w, d) {
    const park = new THREE.Mesh(new THREE.PlaneGeometry(w, d), mat(0xcfe2d8));
    park.rotation.x = -Math.PI / 2;
    park.position.set(x, 0.02, z);
    scene.add(park);
    for (let i=0; i<7; i++) {
      const tree = new THREE.Group();
      const trunk = new THREE.Mesh(new THREE.CylinderGeometry(.035,.045,.28,8), mat(0x9b8a77));
      trunk.position.y=.14;
      const crown = new THREE.Mesh(new THREE.SphereGeometry(.16,14,10), mat(0x7fa893));
      crown.position.y=.36;
      tree.add(trunk,crown);
      tree.position.set(x - w/2 + .35 + (i%4)*.55, 0.02, z - d/2 + .35 + Math.floor(i/4)*.55);
      scene.add(tree);
    }
  }
  addPark(-5.0, 3.2, 1.5, 1.1); addPark(5.2, .85, 1.2, 1.0);

  function makeLabel(text, color) {
    const canvas = document.createElement('canvas');
    canvas.width = 512; canvas.height = 96;
    const ctx = canvas.getContext('2d');
    ctx.font = '600 30px system-ui, -apple-system, Segoe UI, sans-serif';
    ctx.fillStyle = 'rgba(255,255,255,0.88)';
    ctx.strokeStyle = 'rgba(190,202,214,0.72)';
    ctx.lineWidth = 3;
    ctx.roundRect(10, 16, 492, 58, 18); ctx.fill(); ctx.stroke();
    ctx.fillStyle = color; ctx.fillText(text, 34, 54);
    const texture = new THREE.CanvasTexture(canvas);
    const sprite = new THREE.Sprite(new THREE.SpriteMaterial({ map: texture, transparent: true }));
    sprite.scale.set(2.7, .5, 1);
    return sprite;
  }

  function addNode(x, z, color, label, size=.13) {
    const sphere = new THREE.Mesh(new THREE.SphereGeometry(size, 24, 16), mat(color));
    sphere.position.set(x, .45, z);
    sphere.castShadow = true;
    scene.add(sphere);
    const pole = new THREE.Mesh(new THREE.CylinderGeometry(.015,.015,.45,10), mat(0x8b9aaa));
    pole.position.set(x, .225, z);
    scene.add(pole);
    const tag = makeLabel(label, '#' + new THREE.Color(color).getHexString());
    tag.position.set(x, .95, z);
    scene.add(tag);
  }
  addNode(-5.1,-2.1,0xc69a42,'Streetlight',.12);
  addNode(-3.2,-1.0,0x3f8f8b,'Air quality',.13);
  addNode(-.7,-3.0,0xb35b7e,'CCTV',.12);
  addNode(1.9,-.4,0x5a5fa8,'Gateway',.15);
  addNode(4.5,1.2,0x3f8f8b,'Air quality',.13);

  const focusColor = new THREE.Color('__FOCUS_COLOR__');
  const focusX = __FOCUS_X__;
  const focusZ = __FOCUS_Z__;
  const focus = new THREE.Group();
  const halo = new THREE.Mesh(new THREE.TorusGeometry(.62, .035, 16, 96), mat(focusColor.getHex(), .82));
  halo.rotation.x = -Math.PI / 2;
  halo.position.y = .08;
  const hotspot = new THREE.Mesh(new THREE.SphereGeometry(.23, 32, 18), mat(focusColor.getHex()));
  hotspot.position.y = .58;
  const pulse = new THREE.Mesh(new THREE.RingGeometry(.78, .83, 96), new THREE.MeshBasicMaterial({ color: focusColor, transparent: true, opacity: .22, side: THREE.DoubleSide }));
  pulse.rotation.x = -Math.PI / 2;
  pulse.position.y = .035;
  focus.add(halo, hotspot, pulse);
  focus.position.set(focusX, 0, focusZ);
  scene.add(focus);
  const focusLabel = makeLabel('__FOCUS_LABEL__', '__FOCUS_COLOR__');
  focusLabel.position.set(focusX, 1.35, focusZ);
  scene.add(focusLabel);

  const airflowMat = new THREE.LineBasicMaterial({ color: 0x82a7b5, transparent: true, opacity: .45 });
  [[-5.6,3.8,-2.3,3.2],[-3.2,3.6,.4,3.0],[1.7,3.4,4.8,2.6]].forEach(line => {
    const curve = new THREE.CatmullRomCurve3([new THREE.Vector3(line[0],.25,line[1]), new THREE.Vector3((line[0]+line[2])/2,.55,(line[1]+line[3])/2), new THREE.Vector3(line[2],.25,line[3])]);
    scene.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(curve.getPoints(40)), airflowMat));
  });

  function resize() {
    const width = container.clientWidth;
    const height = container.clientHeight;
    renderer.setSize(width, height);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
  }
  window.addEventListener('resize', resize);
  resize();

  function animate() {
    requestAnimationFrame(animate);
    controls.update();
    halo.rotation.z += 0.006;
    pulse.scale.setScalar(1 + Math.sin(Date.now() * 0.002) * 0.08);
    renderer.render(scene, camera);
  }
  animate();
</script>
'''
    scene_html = (
        scene_html.replace("__FOCUS_LABEL__", safe_label)
        .replace("__FOCUS_NOTE__", safe_note)
        .replace("__FOCUS_COLOR__", scenario_focus["color"])
        .replace("__FOCUS_X__", str(scenario_focus["x"]))
        .replace("__FOCUS_Z__", str(scenario_focus["z"]))
    )
    components.html(scene_html, height=660, scrolling=False)
    st.info(
        "The 3D map is a schematic spatial layer. It does not use real London GIS geometry, real device coordinates, or live sensing feeds."
    )

def priority_ranking(runtime_state: dict[str, str]) -> list[tuple[str, int]]:
    rankings = {
        "S1": [("Demand Response", 78), ("Occupancy Advisory", 58), ("Baseline Monitoring", 46)],
        "S2": [("Community Demand Coordination", 82), ("Peak-load Monitoring", 68), ("Exposure Monitoring", 55)],
        "S3": [("Ventilation", 94), ("Passive Cooling", 84), ("Occupancy Advisory", 78), ("Demand Response", 62)],
        "S4": [("Ventilation Strategy", 76), ("Cooling-AQ Tradeoff", 70), ("Scenario Comparison", 58)],
    }
    return rankings[runtime_state["scenario_id"]]


def render_priority_ranking(runtime_state: dict[str, str]) -> str:
    rows = "".join(
        dedent(
            f"""
            <div class="priority-row">
                <div class="priority-topline"><span>{idx}. {escape(label)}</span><span>{score}%</span></div>
                <div class="priority-track"><div class="priority-fill" style="width:{score}%"></div></div>
            </div>
            """
        ).strip()
        for idx, (label, score) in enumerate(priority_ranking(runtime_state), start=1)
    )
    return f"<div class='priority-list'>{rows}</div>"


def impact_simulation(runtime_state: dict[str, str]) -> dict[str, str]:
    impacts = {
        "S1": {
            "current": "Household baseline<br>Moderate energy demand",
            "action": "Demand-response scheduling",
            "outcome": "Expected peak demand reduction:<br><strong>8–12%</strong>",
        },
        "S2": {
            "current": "Community load pressure",
            "action": "Community demand coordination",
            "outcome": "Improved load distribution",
        },
        "S3": {
            "current": "PM2.5 elevated<br>Heat stress elevated",
            "action": "Ventilation<br>Cooling<br>Occupancy guidance",
            "outcome": "Predicted exposure reduction<br>PM2.5 ↓<br>Thermal stress ↓<br>Overall risk: <strong>High → Moderate</strong>",
        },
        "S4": {
            "current": "Weather-AQ sensitivity",
            "action": "Adaptive intervention planning",
            "outcome": "Improved scenario resilience",
        },
    }
    return impacts[runtime_state["scenario_id"]]


def render_impact_simulation(runtime_state: dict[str, str]) -> None:
    impact = impact_simulation(runtime_state)
    st.subheader("Intervention Impact Simulation")
    st.markdown(
        f"""
        <div class="impact-flow">
            <div class="impact-card">
                <div class="impact-label">Current Condition</div>
                <div class="impact-title">{impact["current"]}</div>
                <div class="impact-detail">{escape(runtime_state["health_mode"])}</div>
            </div>
            <div class="impact-arrow">↓</div>
            <div class="impact-card">
                <div class="impact-label">Recommended Action</div>
                <div class="impact-title">{impact["action"]}</div>
                <div class="impact-detail">Scenario-specific advisory intervention.</div>
            </div>
            <div class="impact-arrow">↓</div>
            <div class="impact-card outcome">
                <div class="impact-label">Expected Outcome</div>
                <div class="impact-title">{impact["outcome"]}</div>
                <div class="impact-detail">Simulated impact signal for feedback interpretation.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("These outcomes represent simulated advisory-level intervention effects and are not measured real-world responses.")


def render_command_center(runtime_state: dict[str, str]) -> None:
    st.title("Urban CPS Digital Twin Command Center")
    st.caption("Health-aware environmental intervention demonstrator using harmonised secondary datasets.")
    render_badge_strip(runtime_state)
    render_scenario_purpose(runtime_state)
    render_urban_health_status(runtime_state)
    render_urban_exposure_map(runtime_state)
    render_3d_urban_twin_map(runtime_state)

    interventions = intervention_rows(runtime_state)
    st.markdown(
        f"""
        <div class="cc-grid">
            <section class="section-card">
                <div class="section-title">Data Layer</div>
                <div class="section-subtitle">Traceable secondary sources feeding the CDE.</div>
                {source_card("⚡", "Energy Data", {"Source": "UK-DALE", "Resolution": "15 min", "Status": "Harmonised"})}
                {source_card("🌫", "Air Quality Data", {"Source": "PM2.5 monitoring", "Status": "Available"})}
                {source_card("🌦", "Weather Data", {"Source": "Meteorological observations", "Variables": "temperature, humidity, wind, pressure, precipitation"})}
            </section>
            <section class="section-card">
                <div class="section-title">Urban CPS Core</div>
                <div class="section-subtitle">Digital-twin pathway from harmonised data to advisory feedback.</div>
                {pipeline_html()}
            </section>
            <section class="section-card">
                <div class="section-title">Active Intervention State</div>
                <div class="section-subtitle">Scenario-relevant advisory endpoints.</div>
                {''.join(intervention_card(row) for row in interventions)}
                <div class="section-title">Priority Ranking</div>
                {render_priority_ranking(runtime_state)}
            </section>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_impact_simulation(runtime_state)
    render_traceability(runtime_state)
    render_prototype_scope_panel()


def render_cde_page(runtime_state: dict[str, str]) -> None:
    st.header("CDE / Digital Thread")
    st.write("The Common Data Environment synchronises energy, PM2.5, and weather observations into a shared secondary-data workflow.")
    render_badge_strip(runtime_state)

    cols = st.columns(3)
    with cols[0]:
        st.markdown(source_card("⚡", "Energy", {"Source": "UK-DALE", "Role": "Demand baseline"}), unsafe_allow_html=True)
    with cols[1]:
        st.markdown(source_card("🌫", "PM2.5", {"Source": "Air-quality monitoring", "Role": "Exposure stressor"}), unsafe_allow_html=True)
    with cols[2]:
        st.markdown(source_card("🌦", "Weather", {"Source": "Meteorological observations", "Role": "Thermal context"}), unsafe_allow_html=True)

    sankey = go.Figure(
        go.Sankey(
            node=dict(
                pad=18,
                thickness=15,
                color=["#8fa1b3", "#8fa1b3", "#8fa1b3", "#6f9385", "#415a77", "#a7897f"],
                label=["Energy", "PM2.5", "Weather", "CDE harmonisation", "Scenario engine", "Advisory feedback"],
            ),
            link=dict(source=[0, 1, 2, 3, 4], target=[3, 3, 3, 4, 5], value=[1, 1, 1, 3, 2]),
        )
    )
    sankey.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="#fbfcfd", font=dict(color="#1f2933"))
    st.plotly_chart(sankey, use_container_width=True)

    df, error = load_csv("community_pm25_weather_merged.csv")
    if error:
        warn_missing("community_pm25_weather_merged.csv")
        render_traceability(runtime_state)
        return

    time_range = "Unavailable"
    if "timestamp" in df.columns:
        time_range = f"{df['timestamp'].min()} to {df['timestamp'].max()}"
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Merged samples", f"{len(df):,}")
    m2.metric("Columns", f"{len(df.columns):,}")
    m3.metric("Valid coverage", valid_coverage(df))
    m4.metric("Time range", time_range)
    st.info(f"Scenario-aware interpretation: {runtime_state['scenario_id']} · {runtime_state['risk_mode']}")
    render_traceability(runtime_state)


def render_analysis_page() -> None:
    st.header("Analysis")
    selected = st.radio("Analysis module", ANALYSIS_ITEMS, horizontal=True)
    if selected == "S1 Household":
        show_table("s1/house1_enduse_energy_kwh.csv", "S1 House 1 End-use Energy")
        a, b = st.columns(2)
        with a:
            show_image("s1/fig4a_house1_daily_profiles.png", "S1 daily profiles")
        with b:
            show_image("s1/fig4b_house1_enduse_shares.png", "S1 end-use shares")
        show_table("s1/metrics.csv", "S1 Metrics")
        c, d = st.columns(2)
        with c:
            show_image("s1/fig5a_pred_vs_actual.png", "S1 prediction")
        with d:
            show_image("s1/fig5b_shap_summary.png", "S1 SHAP")
    elif selected == "S2 Community":
        show_table("s2/metrics.csv", "S2 Community Metrics")
        a, b, c = st.columns(3)
        with a:
            show_image("s2/fig6a_daily_profiles.png", "S2 daily profiles")
        with b:
            show_image("s2/fig6b_pred_vs_actual.png", "S2 prediction")
        with c:
            show_image("s2/fig6c_shap.png", "S2 SHAP")
    elif selected == "S3 Multi-Stressor":
        show_table("s3/episode_results.csv", "S3 Episode Results")
        show_table("s3/event_summary.csv", "S3 Event Summary")
        show_table("s3/metrics.csv", "S3 Metrics")
        a, b = st.columns(2)
        with a:
            show_image("s3/fig10_s3a_highstress_load_pred.png", "S3 load prediction")
        with b:
            show_image("s3/fig10_s3b_highstress_env.png", "S3 environmental stressors")
    else:
        show_table("s4/metrics_placeholder.csv", "S4 Metrics")
        show_table("s4/prediction_grid_placeholder.csv", "S4 Prediction Grid")
        a, b, c = st.columns(3)
        with a:
            show_image("s4/fig10_s4_pm25_temp_heatmap.png", "S4 PM2.5-temperature heatmap")
        with b:
            show_image("s4/fig10a_shap_no_weather.png", "S4 SHAP without weather")
        with c:
            show_image("s4/fig10b_shap_weather.png", "S4 SHAP with weather")


def response_logic_steps(runtime_state: dict[str, str]) -> list[dict[str, str]]:
    rows = intervention_rows(runtime_state)
    first = rows[0]
    scenario = runtime_state["scenario_id"]
    trigger = {
        "S1": "Household demand and indoor baseline context",
        "S2": "Aggregated community load pressure",
        "S3": "Coupled PM2.5, heat, and load stressor watch",
        "S4": "Weather-air-quality sensitivity contrast",
    }[scenario]
    interpretation = {
        "S1": "Stable baseline; interpret flexible demand windows.",
        "S2": "Community-scale monitoring; check demand distribution.",
        "S3": "Compound exposure interpretation; escalate advisory priority.",
        "S4": "Tradeoff interpretation; compare response pathways.",
    }[scenario]
    return [
        {"index": "01", "title": "Environmental trigger", "detail": trigger},
        {"index": "02", "title": "Health-aware interpretation", "detail": interpretation},
        {"index": "03", "title": "Scenario engine", "detail": f"{runtime_state['scenario_id']} · {runtime_state['scenario_name']}"},
        {"index": "04", "title": "Response selection", "detail": first["action"]},
        {"index": "05", "title": "Endpoint abstraction", "detail": first["endpoint"]},
        {"index": "06", "title": "Simulated feedback", "detail": runtime_state["feedback_status"]},
        {"index": "07", "title": "Updated state", "detail": runtime_state["risk_mode"]},
    ]


def render_response_logic_flow(runtime_state: dict[str, str]) -> None:
    html = "".join(
        dedent(
            f"""
            <div class="logic-flow-step">
                <div class="logic-step-index">{escape(row["index"])}</div>
                <div class="card-title">{escape(row["title"])}</div>
                <div class="card-text">{escape(row["detail"])}</div>
            </div>
            """
        ).strip()
        for row in response_logic_steps(runtime_state)
    )
    st.subheader("Trigger-to-Response Logic")
    st.markdown(f"<div class='logic-flow-grid'>{html}</div>", unsafe_allow_html=True)


def endpoint_response_card(row: dict[str, str]) -> str:
    control_level = control_level_for_endpoint(row["endpoint"])
    return dedent(
        f"""
        <div class="intervention-card">
            <div class="intervention-head">
                <div class="icon-box">{escape(row["icon"])}</div>
                <div class="card-title">{escape(row["endpoint"])}</div>
                <div class="priority">{escape(row["priority"])}</div>
            </div>
            <div class="control-label">Control level</div>
            <div class="control-level-badge">{escape(control_level)}</div>
            <div class="card-text"><strong>Trigger condition:</strong> {escape(row["trigger"])}</div>
            <div class="card-text"><strong>Intended effect:</strong> {escape(row["action"])}</div>
            <div class="card-text"><strong>Feedback status:</strong> {escape(row["status"])}</div>
        </div>
        """
    ).strip()


def hardware_components(runtime_state: dict[str, str]) -> list[dict[str, str]]:
    scenario_note = {
        "S1": "supports household baseline monitoring",
        "S2": "supports community demand and exposure aggregation",
        "S3": "supports compound exposure response selection",
        "S4": "supports sensitivity-based response comparison",
    }[runtime_state["scenario_id"]]
    return [
        {"icon": "📡", "title": "Sensor nodes", "detail": "Secondary PM2.5, weather, and load signals are treated as the sensing layer."},
        {"icon": "🏠", "title": "Indoor sensing", "detail": "Represents indoor environmental context and occupancy-aware interpretation."},
        {"icon": "🌬", "title": "Ventilation unit / airflow control", "detail": "Abstract endpoint for filtered ventilation advisory signals."},
        {"icon": "🧰", "title": "Air filtration unit", "detail": "Abstract endpoint for particle exposure reduction advisories."},
        {"icon": "🌞", "title": "Shading / cooling system", "detail": "Abstract endpoint for heat and solar-gain response advisories."},
        {"icon": "👥", "title": "Occupancy advisory channel", "detail": "Could be signage or app notification in future integration."},
        {"icon": "🌿", "title": "Lower-exposure route / greenery", "detail": "Supports advisory guidance toward lower-exposure zones."},
        {"icon": "↔", "title": "BEMS / IoT pathway", "detail": f"Future integration pathway; {scenario_note}."},
    ]


def render_hardware_abstraction(runtime_state: dict[str, str]) -> None:
    html = "".join(
        dedent(
            f"""
            <div class="hardware-card">
                <div class="card-row">
                    <div class="icon-box">{escape(row["icon"])}</div>
                    <div class="card-title">{escape(row["title"])}</div>
                </div>
                <div class="card-text">{escape(row["detail"])}</div>
            </div>
            """
        ).strip()
        for row in hardware_components(runtime_state)
    )
    st.subheader("Hardware / Implementation Abstraction")
    st.markdown(f"<div class='hardware-grid'>{html}</div>", unsafe_allow_html=True)


def render_feedback_closure(runtime_state: dict[str, str]) -> None:
    pm25, temp, load = environmental_snapshot(runtime_state)
    state = classify_health(pm25, temp, load, runtime_state)
    state["energy"] = load_pressure_label(load, runtime_state)
    state["summary"] = health_state_summary(state, runtime_state)
    closure_rows = [
        {"title": "Simulated response", "detail": simulated_feedback_rows(state, runtime_state)[0]["after"]},
        {"title": "Operator review status", "detail": operator_review_summary(runtime_state)},
        {"title": "Updated exposure interpretation", "detail": health_state_summary(state, runtime_state)},
        {"title": "Continued monitoring", "detail": "CDE synchronisation remains harmonised; advisory outputs are re-evaluated as scenario inputs change."},
    ]
    html = "".join(
        dedent(
            f"""
            <div class="closure-card">
                <div class="card-title">{escape(row["title"])}</div>
                <div class="card-text">{escape(row["detail"])}</div>
            </div>
            """
        ).strip()
        for row in closure_rows
    )
    st.subheader("Feedback Closure")
    st.markdown(f"<div class='closure-grid'>{html}</div>", unsafe_allow_html=True)
    st.caption("Feedback closure is simulated: outputs update interpretation inside the demonstrator but do not operate real devices.")


def operator_action_key(runtime_state: dict[str, str], index: int) -> str:
    return f"operator_action_{runtime_state['scenario_id']}_{index}"


def operator_action_status(action: str) -> str:
    return {
        "Accept advisory": "Advisory accepted",
        "Defer": "Advisory deferred",
        "Override": "Operator override simulated",
        "Monitor only": "Monitoring continued",
    }[action]


def operator_review_summary(runtime_state: dict[str, str]) -> str:
    rows = intervention_rows(runtime_state)
    actions = [st.session_state.get(operator_action_key(runtime_state, idx), "Monitor only") for idx, _ in enumerate(rows)]
    if any(action == "Override" for action in actions):
        return "Operator override simulated"
    if any(action == "Accept advisory" for action in actions):
        return "Advisory accepted for simulated response pathway"
    if any(action == "Defer" for action in actions):
        return "Advisory deferred for operator review"
    return "Monitoring continued"


def render_operator_review_panel(runtime_state: dict[str, str], rows: list[dict[str, str]]) -> None:
    st.subheader("Operator Review / Advisory Override")
    st.caption("This page represents the operator-facing response layer for reviewing environmental intervention recommendations and simulated feedback.")
    cols = st.columns(2)
    for idx, row in enumerate(rows):
        with cols[idx % 2]:
            action = st.selectbox(
                f"Operator action · {row['endpoint']}",
                ["Accept advisory", "Defer", "Override", "Monitor only"],
                index=3,
                key=operator_action_key(runtime_state, idx),
            )
            st.markdown(
                dedent(
                    f"""
                    <div class="operator-review-card">
                        <div class="card-row">
                            <div class="icon-box">{escape(row["icon"])}</div>
                            <div>
                                <div class="card-title">{escape(row["endpoint"])}</div>
                                <span class="status-chip watch">{escape(operator_action_status(action))}</span>
                            </div>
                        </div>
                        <div class="card-text"><strong>System recommendation:</strong> {escape(row["action"])}</div>
                        <div class="card-text"><strong>Priority:</strong> {escape(row["priority"])}</div>
                        <div class="card-text"><strong>Operator action:</strong> {escape(action)}</div>
                    </div>
                    """
                ).strip(),
                unsafe_allow_html=True,
            )
    st.info("This layer supports asset-manager review of advisory endpoints. No direct actuation is performed in this prototype.")


def render_occupant_feedback_panel(state: dict[str, str], runtime_state: dict[str, str]) -> dict[str, str]:
    st.subheader("Occupant Feedback / Preference Input")
    st.caption("This page represents the occupant-facing advisory layer. It allows lightweight feedback on comfort and exposure perception.")
    feedback = st.selectbox(
        "Select occupant feedback",
        OCCUPANT_FEEDBACK_OPTIONS,
        key=occupant_feedback_key(runtime_state),
    )
    update = occupant_feedback_update(feedback, state, runtime_state)
    cards = [
        ("Feedback received", update["received"]),
        ("Updated advisory interpretation", update["interpretation"]),
        ("Updated recommended response", update["response"]),
        ("Simulated feedback status", update["status"]),
    ]
    html = "".join(
        dedent(
            f"""
            <div class="feedback-input-card">
                <div class="card-title">{escape(title)}</div>
                <div class="card-text">{escape(value)}</div>
            </div>
            """
        ).strip()
        for title, value in cards
    )
    st.markdown(f"<div class='feedback-input-grid'>{html}</div>", unsafe_allow_html=True)
    st.info("This feedback modifies the advisory interpretation within the prototype. It does not trigger direct device control.")
    return update


def render_intervention_page(runtime_state: dict[str, str]) -> None:
    st.header("Intervention Logic & Response Layer")
    st.caption("This page represents the operator-facing response layer for reviewing environmental intervention recommendations and simulated feedback.")
    render_response_logic_flow(runtime_state)

    st.subheader("Response Endpoint Cards")
    rows = intervention_rows(runtime_state)
    endpoint_html = "".join(endpoint_response_card(row) for row in rows)
    st.markdown(f"<div class='endpoint-response-grid'>{endpoint_html}</div>", unsafe_allow_html=True)
    st.caption("Control level describes how the prototype represents each intervention endpoint. No real devices are actuated.")

    st.dataframe(
        pd.DataFrame(
            [
                {
                    "Scenario": runtime_state["scenario_id"],
                    "Trigger condition": row["trigger"],
                    "Endpoint": row["endpoint"],
                    "Advisory action": row["action"],
                    "Priority": row["priority"],
                    "Feedback status": row["status"],
                }
                for row in rows
            ]
        ),
        use_container_width=True,
        hide_index=True,
    )
    render_hardware_abstraction(runtime_state)
    render_operator_review_panel(runtime_state, rows)
    render_feedback_closure(runtime_state)
    st.info("No direct control is claimed. Recommendations may support decision-making and simulated feedback for future BEMS/IoT integration.")


def render_smart_healing_page(runtime_state: dict[str, str]) -> None:
    st.header("Smart Healing Interface")
    st.caption("Human-centred advisory layer for the health-aware Urban CPS Digital Twin.")
    render_scenario_purpose(runtime_state)
    st.markdown(
        """
        <div class="healing-intro">
            This human-facing view translates backend MBSE-CPS outputs into a spatial, health-aware advisory experience.
            It focuses on current state, interpretation, top advisory actions, and expected outcome.
            Detailed trigger-response logic is handled in the Intervention Logic & Response Layer.
        </div>
        """,
        unsafe_allow_html=True,
    )
    pm25, temp, load = environmental_snapshot(runtime_state)
    state = classify_health(pm25, temp, load, runtime_state)
    state["energy"] = load_pressure_label(load, runtime_state)
    state["summary"] = health_state_summary(state, runtime_state)

    render_digital_twin_process_strip(state, runtime_state)
    render_twin_context_view(state, runtime_state)

    st.subheader("Current Environment / Exposure State")
    pm25_detail = f"PM2.5 proxy: {pm25:.2f}" if pm25 is not None else "PM2.5 proxy unavailable"
    temp_detail = f"Temperature proxy: {temp:.2f}" if temp is not None else "Temperature proxy unavailable"
    load_detail = f"Load proxy: {load:.2f}" if load is not None else "Community load proxy unavailable"
    exposure_cards = [
        ("🌫", "PM2.5 exposure state", state["air"], pm25_detail),
        ("🌡", "Thermal stress state", state["heat"], temp_detail),
        ("⚡", "Community load pressure", state["energy"], load_detail),
        ("⚠", "Compound exposure state", state["compound"], state["summary"]),
        ("●", "Scenario state", runtime_state["scenario_name"], runtime_state["risk_mode"]),
    ]
    exposure_html = "".join(
        dedent(
            f"""
            <div class="exposure-card {escape(healing_tone(value))}">
                <div class="card-row">
                    <div class="icon-box">{escape(icon)}</div>
                    <div class="card-title">{escape(title)}</div>
                </div>
                <div class="exposure-value">{escape(value)}</div>
                <div class="card-text">{escape(detail)}</div>
            </div>
            """
        ).strip()
        for icon, title, value, detail in exposure_cards
    )
    st.markdown(f"<div class='healing-card-grid'>{exposure_html}</div>", unsafe_allow_html=True)

    st.subheader("Human / Health-Aware Interpretation")
    interpretation_html = "".join(
        dedent(
            f"""
            <div class="interpretation-card">
                <div class="card-row">
                    <div class="icon-box">{escape(card["icon"])}</div>
                    <div>
                        <div class="card-title">{escape(card["title"])}</div>
                        <span class="status-chip {escape(card["tone"])}">{escape(card["tone"].title())}</span>
                    </div>
                </div>
                <div class="card-text">{escape(card["value"])}</div>
            </div>
            """
        ).strip()
        for card in health_interpretation_cards(state, runtime_state)
    )
    st.markdown(f"<div class='healing-card-grid'>{interpretation_html}</div>", unsafe_allow_html=True)
    occupant_update = render_occupant_feedback_panel(state, runtime_state)
    selected_feedback = st.session_state.get(occupant_feedback_key(runtime_state), "Comfortable")

    st.subheader("Recommended Actions")
    interventions = apply_occupant_feedback_to_actions(healing_interventions(state, runtime_state), occupant_update, selected_feedback)[:3]
    intervention_html = "".join(
        dedent(
            f"""
            <div class="compact-action-card {escape(row.get("primary", ""))}">
                <div class="card-row">
                    <div class="icon-box">{escape(row["icon"])}</div>
                    <div>
                        <div class="intervention-name">{escape(row["name"])}</div>
                        <span class="status-chip watch">{escape(row["status"])}</span>
                    </div>
                </div>
                <div class="intervention-line">{escape(row["effect"])}</div>
            </div>
            """
        ).strip()
        for row in interventions
    )
    st.markdown(f"<div class='compact-action-grid'>{intervention_html}</div>", unsafe_allow_html=True)

    st.subheader("Simulated Feedback / Expected Outcome")
    feedback_rows = apply_occupant_feedback_to_feedback_rows(simulated_feedback_rows(state, runtime_state), occupant_update, selected_feedback)
    feedback_html = "".join(
        dedent(
            f"""
            <div class="before-after-card">
                <div class="before-after-title">{escape(row["title"])}</div>
                <div class="before-after-flow">{escape(row["before"])} → {escape(row["after"])}</div>
                <div class="card-text">Intervention: {escape(row["intervention"])}</div>
            </div>
            """
        ).strip()
        for row in feedback_rows[:3]
    )
    st.markdown(f"<div class='feedback-strip'>{feedback_html}</div>", unsafe_allow_html=True)
    st.caption("The updated state reflects simulated post-intervention interpretation within the digital twin.")
    st.subheader("Updated Twin Interpretation")
    updated_html = "".join(
        dedent(
            f"""
            <div class="updated-card {escape(row["tone"])}">
                <div class="card-title">{escape(row["title"])}</div>
                <div class="card-text">{escape(row["value"])}</div>
            </div>
            """
        ).strip()
        for row in apply_occupant_feedback_to_updated_state(updated_twin_state(state, runtime_state), occupant_update, selected_feedback)
    )
    st.markdown(f"<div class='updated-grid'>{updated_html}</div>", unsafe_allow_html=True)
    render_data_to_decision_trace(runtime_state)
    st.info("This page is advisory and human-facing. It does not perform direct actuation; system response logic is documented in the Intervention Logic & Response Layer.")


def render_decision_support_page(runtime_state: dict[str, str]) -> None:
    st.header("Decision Support")
    st.info(f"Selected scenario: {runtime_state['scenario_id']} · {runtime_state['scenario_name']}")
    pm25, temp, load = environmental_snapshot(runtime_state)
    state = classify_health(pm25, temp, load, runtime_state)

    c1, c2, c3 = st.columns(3)
    c1.metric("Health-aware interpretation", state["compound"])
    c2.metric("Priority mode", intervention_rows(runtime_state)[0]["priority"])
    c3.metric("Review status", operator_review_summary(runtime_state))

    occupant_feedback = st.session_state.get(occupant_feedback_key(runtime_state), "Comfortable")
    occupant_update = occupant_feedback_update(occupant_feedback, state, runtime_state)
    st.info(
        "Human-in-the-loop status: "
        f"occupant feedback = {occupant_update['status']}; "
        f"operator review = {operator_review_summary(runtime_state)}. "
        "Both are advisory signals for simulated decision support, not direct device control."
    )

    st.subheader("Recommended Interventions")
    for row in intervention_rows(runtime_state):
        with st.container(border=True):
            st.markdown(f"**{row['icon']} {row['endpoint']}**")
            st.write(row["action"])
            st.caption(f"Trigger: {row['trigger']} | Priority: {row['priority']} | Status: {row['status']}")

    render_traceability(runtime_state, "Decision Traceability Path")
    render_data_to_decision_trace(runtime_state)
    render_impact_simulation(runtime_state)
    render_prototype_scope_panel()


def main() -> None:
    st.sidebar.title("Urban CPS DT")
    st.sidebar.caption("Command Center V2")
    selected_scenario = st.sidebar.selectbox("Global Scenario", list(SCENARIOS.keys()), key="cc_scenario")
    runtime_state = get_runtime_state(selected_scenario)

    st.sidebar.divider()
    selected_page = st.sidebar.radio("Navigation", NAV_ITEMS, key="cc_page")
    st.sidebar.divider()
    st.sidebar.markdown("**Runtime State**")
    st.sidebar.success(f"CPS Synchronization: {runtime_state['sync_status']}")
    st.sidebar.info(f"Data Mode: {runtime_state['data_mode']}")
    st.sidebar.info(f"CDE Status: {runtime_state['cde_status']}")
    st.sidebar.info(f"Feedback: {runtime_state['feedback_status']}")

    if selected_page == "🏠 Command Center":
        render_command_center(runtime_state)
    elif selected_page == "🔄 CDE / Digital Thread":
        render_cde_page(runtime_state)
    elif selected_page == "📊 Analysis":
        render_analysis_page()
    elif selected_page == "🌿 Intervention Layer":
        render_intervention_page(runtime_state)
    elif selected_page == "🖥 Smart Healing Interface":
        render_smart_healing_page(runtime_state)
    else:
        render_decision_support_page(runtime_state)


if __name__ == "__main__":
    main()


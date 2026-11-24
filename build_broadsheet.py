#!/usr/bin/env python3
"""
Deterministic editorial broadsheet builder (V2.1 Atlas Master) for make.fun news-image-20261124.
Upgrades from V1 -> V2.1:
  - High-contrast navy/gold masthead + vivid crimson date block (TUESDAY · 24 NOVEMBER 2026)
  - 6 bespoke textless editorial gouache-and-ink hero illustrations (with tight-cropped Gaza/Aden diptych)
  - Per-panel focal framing (object-position) + balanced 2-line 19.5px condensed headlines (zero orphans)
  - Unified cartographic World-Map Hotspot Dispatch Ribbon + 4 High-Contrast Global Flash Cards (zero clipping)
  - Balanced 3-column pure single-topic Global Wire across all 6 inhabited continents and every major beat
"""

from __future__ import annotations

import base64
import io
import sys
from pathlib import Path
from PIL import Image


CLEAN_ART_DIR = Path("/tmp/art_clean")


# ---------------------------------------------------------------------------
# Crisp Cartographic World Map SVG with 16 Verified 24 Nov 2026 Hotspot Pins
# ---------------------------------------------------------------------------

WORLD_MAP_SVG = """
<svg viewBox="0 0 516 128" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="oceanGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0a1626"/>
      <stop offset="100%" stop-color="#132944"/>
    </linearGradient>
    <filter id="pinGlow" x="-45%" y="-45%" width="190%" height="190%">
      <feGaussianBlur stdDeviation="1.5" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <rect width="516" height="128" fill="url(#oceanGrad)"/>
  <g stroke="#60a5fa" stroke-opacity="0.11" stroke-width="0.6" stroke-dasharray="2,3">
    <line x1="0" y1="32" x2="516" y2="32"/><line x1="0" y1="64" x2="516" y2="64"/><line x1="0" y1="96" x2="516" y2="96"/>
    <line x1="86" y1="0" x2="86" y2="128"/><line x1="172" y1="0" x2="172" y2="128"/><line x1="258" y1="0" x2="258" y2="128"/>
    <line x1="344" y1="0" x2="344" y2="128"/><line x1="430" y1="0" x2="430" y2="128"/>
  </g>
  <!-- Clean cartographic continents -->
  <g fill="#2e4866" stroke="#5f84ab" stroke-width="0.7" stroke-linejoin="round">
    <!-- North America -->
    <path d="M20,20 L46,16 L80,14 L114,16 L130,24 L124,33 L108,38 L106,47 L92,54 L80,55 L74,62 L64,59 L56,50 L46,46 L34,36 L20,28 Z"/>
    <!-- Greenland -->
    <path d="M136,8 L164,7 L172,17 L158,25 L142,22 Z"/>
    <!-- South America -->
    <path d="M86,65 L104,63 L120,71 L132,81 L126,97 L114,113 L102,120 L96,113 L96,96 L86,82 L82,71 Z"/>
    <!-- Europe + Scandinavia + UK -->
    <path d="M214,36 L226,28 L236,16 L252,14 L264,20 L272,30 L274,40 L258,45 L244,46 L234,49 L224,47 L214,45 Z"/>
    <path d="M204,31 L211,29 L213,37 L206,38 Z"/>
    <!-- Africa + Madagascar -->
    <path d="M212,53 L236,51 L262,53 L278,61 L288,71 L280,86 L272,102 L258,113 L246,110 L240,94 L234,80 L216,75 L206,65 Z"/>
    <path d="M291,93 L295,91 L296,101 L292,103 Z"/>
    <!-- Middle East & Asia -->
    <path d="M272,24 L310,16 L362,16 L414,20 L450,26 L442,36 L422,40 L412,51 L398,59 L384,65 L372,59 L362,69 L352,71 L340,59 L326,58 L310,65 L292,65 L282,57 L276,48 L274,40 Z"/>
    <!-- Japan -->
    <path d="M430,39 L437,37 L439,47 L432,51 Z"/>
    <!-- SE Asia Archipelago -->
    <path d="M382,72 L396,74 L412,76 L426,78 L422,82 L402,80 L384,78 Z"/>
    <!-- Australia + NZ -->
    <path d="M410,87 L432,84 L454,90 L460,104 L446,112 L422,110 L408,100 Z"/>
    <path d="M472,109 L479,107 L480,115 L473,117 Z"/>
  </g>

  <!-- Hotspot Pins across all 6 inhabited continents -->
  <g filter="url(#pinGlow)">
    <!-- Americas -->
    <circle cx="94" cy="38" r="3.4" fill="#f59e0b" stroke="#ffffff" stroke-width="0.9"/>
    <circle cx="96" cy="67" r="3.8" fill="#ef4444" stroke="#ffffff" stroke-width="1"/>
    <!-- Europe -->
    <circle cx="209" cy="34" r="3.5" fill="#60a5fa" stroke="#ffffff" stroke-width="0.9"/>
    <circle cx="255" cy="25" r="3.8" fill="#3b82f6" stroke="#ffffff" stroke-width="1"/>
    <circle cx="268" cy="38" r="3.2" fill="#93c5fd" stroke="#ffffff" stroke-width="0.8"/>
    <!-- Middle East -->
    <circle cx="282" cy="52" r="3.7" fill="#f97316" stroke="#ffffff" stroke-width="1"/>
    <circle cx="308" cy="57" r="4.2" fill="#ef4444" stroke="#ffffff" stroke-width="1.1"/>
    <circle cx="294" cy="66" r="3.4" fill="#fb923c" stroke="#ffffff" stroke-width="0.9"/>
    <!-- Africa -->
    <circle cx="232" cy="70" r="3.2" fill="#fbbf24" stroke="#ffffff" stroke-width="0.8"/>
    <circle cx="268" cy="68" r="3.6" fill="#f59e0b" stroke="#ffffff" stroke-width="0.9"/>
    <circle cx="261" cy="83" r="3.4" fill="#fbbf24" stroke="#ffffff" stroke-width="0.9"/>
    <circle cx="255" cy="107" r="3.0" fill="#fde68a" stroke="#ffffff" stroke-width="0.8"/>
    <!-- Asia-Pacific & South Asia -->
    <circle cx="356" cy="51" r="3.7" fill="#14b8a6" stroke="#ffffff" stroke-width="1"/>
    <circle cx="415" cy="50" r="4.0" fill="#22c55e" stroke="#ffffff" stroke-width="1"/>
    <circle cx="435" cy="44" r="3.2" fill="#4ade80" stroke="#ffffff" stroke-width="0.8"/>
    <circle cx="446" cy="104" r="3.5" fill="#2dd4bf" stroke="#ffffff" stroke-width="0.9"/>
  </g>

  <!-- Crisp non-overlapping cartographic callouts -->
  <g font-family="Liberation Sans, sans-serif" font-size="7.5" font-weight="700" letter-spacing="0.35">
    <text x="10" y="13" fill="#fcd34d" font-size="8.2" letter-spacing="0.6">GLOBAL HOTSPOT MAP · 24 NOV 2026</text>
    <text x="102" y="40" fill="#fde68a">U.S. / CAN</text>
    <text x="104" y="70" fill="#fecaca">COLOMBIA</text>
    <text x="184" y="36" fill="#bfdbfe">UK</text>
    <text x="263" y="25" fill="#bfdbfe">ESTONIA</text>
    <text x="315" y="59" fill="#fecaca">HORMUZ</text>
    <text x="352" y="43" fill="#99f6e4">NEPAL</text>
    <text x="442" y="47" fill="#bbf7d0">ASIA CHIPS</text>
    <text x="282" y="81" fill="#fde68a">SUDAN</text>
    <text x="218" y="92" fill="#fde68a">DRC</text>
    <text x="411" y="122" fill="#99f6e4">AUSTRALIA</text>
  </g>
</svg>
"""


# ---------------------------------------------------------------------------
# Master Verified Story Dataset (V2.1 — Balanced Display Lines, Zero Orphans)
# ---------------------------------------------------------------------------

HERO_STORIES = [
    {
        "region": "MIDDLE EAST · ENERGY",
        "accent": "#b82025",
        "badge": "BRENT $90.52",
        "headline": "Iran Blacklists 26 Hormuz Tugs;<br/>Brent Crude Rebounds Above $90",
        "fact": "Iran's maritime agency blacklists tugs aiding southern bypass after vessel strikes; Brent bounces from $88.10.",
        "art": CLEAN_ART_DIR / "hero1_hormuz.png",
        "obj_pos": "center 46%",
        "diptych_labels": None,
    },
    {
        "region": "GLOBAL M&A · PHARMA",
        "accent": "#0f6e6e",
        "badge": "$41.0B CASH",
        "headline": "Sanofi Agrees $41B Cash Buyout<br/>of U.S. Biotech Firm Insmed",
        "fact": "$175/share all-cash deal (€37.6B) adds Brinsupri, Arikayce & new respiratory disease pipeline drugs.",
        "art": CLEAN_ART_DIR / "hero2_sanofi.png",
        "obj_pos": "center 50%",
        "diptych_labels": None,
    },
    {
        "region": "ASIA & WALL ST · TECH",
        "accent": "#156f3d",
        "badge": "TAIEX +9.0%",
        "headline": "Asia Chip Stocks Surge;<br/>Anthropic Sinks Below $83 IPO",
        "fact": "Taiex jumps 9.0% (40,122), Kospi tops 5,000 (+6.3%), Nikkei +4.0%; Anthropic hits $75.61 (<$1T value).",
        "art": CLEAN_ART_DIR / "hero3_markets.png",
        "obj_pos": "center 28%",
        "diptych_labels": None,
    },
    {
        "region": "EUROPE · SECURITY",
        "accent": "#1b3b6f",
        "badge": "DEC 1 CLOSURE",
        "headline": "Russia Warns Estonia Border<br/>Shutdown Risks 'Open War'",
        "fact": "Moscow summons Estonian envoy over Dec 1 road closures after foiled arson plot; UK MI5 warns defense firms.",
        "art": CLEAN_ART_DIR / "hero4_estonia.png",
        "obj_pos": "center 60%",
        "diptych_labels": None,
    },
    {
        "region": "MIDDLE EAST · CONFLICT",
        "accent": "#9a3412",
        "badge": "GAZA · ADEN",
        "headline": "Gaza Strike Kills Hamas Chief;<br/>Houthis Advance Near Aden",
        "fact": "Israeli strike kills Hamas security chief Naeem Abu Nahel (7+ dead in Gaza); Yemen fortifies Aden 60 km from front.",
        "art": CLEAN_ART_DIR / "hero5_diptych.png",
        "obj_pos": "center 52%",
        "diptych_labels": ("GAZA CITY", "ADEN · 60 KM"),
    },
    {
        "region": "SPACE · GLOBAL",
        "accent": "#1e3a8a",
        "badge": "3 LAUNCHES",
        "headline": "Three Orbital Launches; China<br/>Taps 1st Pakistani Astronaut",
        "fact": "Progress 97 (ISS), Ariane 6 (36 Amazon Leo) & Falcon 9 (USSF-266) lift off; M. Zeeshan Ali joins Shenzhou-24.",
        "art": CLEAN_ART_DIR / "hero6_space.png",
        "obj_pos": "center 48%",
        "diptych_labels": None,
    },
]

# 4 High-Contrast Global Flash Anchors paired with World Map (tightly fitted, zero clipping)
MAP_FLASH_STORIES = [
    {
        "tag": "UK CLIMATE",
        "color": "#60a5fa",
        "title": "5,258 Summer Heat Deaths",
        "detail": "England record across 41 heat days (prior high 2,985).",
    },
    {
        "tag": "COLOMBIA",
        "color": "#f87171",
        "title": "25 Cartagena Hostages",
        "detail": "Gunmen seize Éxito store; airport halts landings 45 min.",
    },
    {
        "tag": "NEPAL QUAKE",
        "color": "#2dd4bf",
        "title": "M5.6 Himalayan Tremor",
        "detail": "Taplejung quake (M5.3 USGS) felt in E. India & Bhutan.",
    },
    {
        "tag": "SUDAN",
        "color": "#fbbf24",
        "title": "$55M+ Port Sudan Water",
        "detail": "AfDB & UNICEF launch project; 7,000+ families displaced.",
    },
]

# Variant A (atlas18): 18 Pure Single-Topic Wire Briefs (3+3 per col) -> 28 total unique verified stories
WIRE_18 = [
    [
        {
            "title": "EUROPE & UKRAINE",
            "color": "#1b3b6f",
            "items": [
                ("UKRAINE", "Overnight Russian strike hits Zaporizhzhia apartments (2 dead); Zelenskyy sends reinforcements."),
                ("BRITAIN", "Prince William makes first official No. 10 visit for talks with UK PM Andy Burnham."),
                ("EUROPE MKTS", "Pan-European STOXX 600 eases to 632.69, DAX to 25,005 and FTSE 100 to 10,468."),
            ],
        },
        {
            "title": "MIDDLE EAST",
            "color": "#b82025",
            "items": [
                ("US–QATAR", "Qatari PM Al Thani meets VP Vance & Sec. Rubio on Iran mediation & Gulf security."),
                ("S. LEBANON", "Israeli strikes hit buffer-zone towns (Qabrikha, Touline) as displaced civilians march."),
                ("GULF TANKERS", "U.S. investigates suspected cyberattacks on regional tankers as bypass flows continue."),
            ],
        },
    ],
    [
        {
            "title": "AMERICAS",
            "color": "#7c2d12",
            "items": [
                ("WASHINGTON", "Trump touts Nvidia lobbying ahead of Dec 3 Senate Banking AI export-control hearing."),
                ("MEXICO", "Prosecutors reject immediate U.S. extradition of 'El Chapo Isidro,' opting for local trial."),
                ("CANADA", "Alberta Premier Danielle Smith moves to invoke Sovereignty Act against Bill C-9."),
            ],
        },
        {
            "title": "ASIA-PACIFIC & SOUTH ASIA",
            "color": "#0f6e6e",
            "items": [
                ("JAPAN & ICC", "PM Sanae Takaichi pledges early 2027 ICC payment by Dec in talks with ICC Pres. Akane."),
                ("AUSTRALIA", "FM Penny Wong warns Senate of U.S.–China strain and flags AI/deepfakes as security threat."),
                ("BANGLADESH", "Dhaka rejects exiled ex-PM Sheikh Hasina's Dec 16 return request, citing arrest warrant."),
            ],
        },
    ],
    [
        {
            "title": "AFRICA",
            "color": "#b45309",
            "items": [
                ("EASTERN DRC", "WHO evacuates Ebola responders trapped 3+ days by fighting inside an Ituri clinic."),
                ("NIGERIA", "Central Bank retains benchmark rate at 23.0% citing festive demand and energy risks."),
                ("SOUTH AFRICA", "State memorial held in Johannesburg for former Deputy Pres. Phumzile Mlambo-Ngcuka."),
            ],
        },
        {
            "title": "HEALTH, MARKETS & SPORT",
            "color": "#3730a3",
            "items": [
                ("U.S. FDA", "FDA approves Cogent's Ekitna (bezuclastinib) + sunitinib combo for advanced GI cancer (GIST)."),
                ("GOLD & CRYPTO", "Gold futures drop 2.3% to $3,568/oz amid volatility; Bitcoin pulls back to ~$60.3k."),
                ("WORLD SPORT", "World Chess G1: Gukesh ½–½ Sindarov · UCL: Galatasaray 1–0 Villa · Davis Cup: Czechia 2–0 Canada · T20I: Eng beat Aus."),
            ],
        },
    ],
]

# Variant B (atlas15): 15 Pure Single-Topic Wire Briefs (5 per col, larger 12.6px type) -> 25 total unique verified stories
WIRE_15 = [
    [
        {
            "title": "EUROPE & MIDDLE EAST",
            "color": "#1b3b6f",
            "items": [
                ("UKRAINE", "Overnight Russian airstrike hits Zaporizhzhia apartments (2 dead); Zelenskyy sends reinforcements."),
                ("BRITAIN", "Prince William makes first official 10 Downing Street visit for talks with UK PM Andy Burnham."),
                ("US–QATAR", "Qatari PM Al Thani meets VP Vance & Sec. Rubio on Iran mediation & Gulf maritime security."),
                ("S. LEBANON", "Israeli strikes hit buffer-zone towns (Qabrikha, Touline) as displaced civilians march home."),
                ("MARKETS", "STOXX 600 eases to 632.69, DAX 25,005; gold drops 2.3% to $3,568/oz; Bitcoin slips ~$60.3k."),
            ],
        },
    ],
    [
        {
            "title": "AMERICAS & ASIA-PACIFIC",
            "color": "#0f6e6e",
            "items": [
                ("WASHINGTON", "Trump touts Nvidia lobbying ahead of Dec 3 Senate Banking AI export-control hearing."),
                ("MEXICO", "Prosecutors reject immediate U.S. extradition of 'El Chapo Isidro,' opting for local trial."),
                ("CANADA", "Alberta Premier Danielle Smith moves to invoke Sovereignty Act against anti-hate Bill C-9."),
                ("JAPAN & ICC", "PM Sanae Takaichi pledges early 2027 ICC payment by Dec in talks with ICC Pres. Akane."),
                ("AUSTRALIA", "FM Penny Wong warns Senate of U.S.–China strain and flags AI/deepfakes as security threat."),
            ],
        },
    ],
    [
        {
            "title": "SOUTH ASIA, AFRICA, HEALTH & SPORT",
            "color": "#9a3412",
            "items": [
                ("BANGLADESH", "Dhaka rejects exiled ex-PM Sheikh Hasina's Dec 16 return request, citing arrest warrant."),
                ("EASTERN DRC", "WHO evacuates Ebola responders trapped 3+ days by fighting inside an Ituri clinic."),
                ("NIGERIA", "Central Bank holds policy rate at 23.0% amid inflation risks; Bayelsa buries 32 boat victims."),
                ("U.S. FDA", "FDA approves Cogent's Ekitna (bezuclastinib) + sunitinib combo for advanced GI cancer (GIST)."),
                ("WORLD SPORT", "World Chess G1: Gukesh ½–½ Sindarov · UCL: Galatasaray 1–0 Villa · Davis Cup: Czechia 2–0 Canada · T20I: Eng beat Aus."),
            ],
        },
    ],
]


def data_uri_for_image(path: Path) -> str:
    raw = path.read_bytes()
    ext = path.suffix.lower().lstrip(".")
    mime = "image/png" if ext == "png" else "image/jpeg"
    b64 = base64.b64encode(raw).decode("ascii")
    return f"data:{mime};base64,{b64}"


def build_html(mode: str = "atlas18") -> str:
    is_18 = mode == "atlas18"
    wire_data = WIRE_18 if is_18 else WIRE_15

    hero_cards_html = []
    for story in HERO_STORIES:
        uri = data_uri_for_image(Path(story["art"]))
        if story["diptych_labels"]:
            l_lbl, r_lbl = story["diptych_labels"]
            badge_overlay = (
                f'<div class="diptych-tag left-tag">{l_lbl}</div>'
                f'<div class="diptych-tag right-tag">{r_lbl}</div>'
            )
        else:
            badge_overlay = f'<div class="corner-badge">{story["badge"]}</div>'

        hero_cards_html.append(
            f"""
            <article class="hero-card" style="border-top-color:{story['accent']}">
              <div class="card-meta">
                <span class="region-tag" style="background:{story['accent']}">{story['region']}</span>
              </div>
              <div class="visual-box">
                <img src="{uri}" style="object-position:{story['obj_pos']}" alt="" />
                {badge_overlay}
              </div>
              <h2 class="hero-headline">{story['headline']}</h2>
              <p class="hero-fact">{story['fact']}</p>
            </article>
            """
        )

    flash_cards_html = "".join(
        f"""
        <div class="flash-item" style="border-left-color:{f['color']}">
          <div class="flash-tag" style="color:{f['color']}">{f['tag']}</div>
          <div class="flash-title">{f['title']}</div>
          <div class="flash-detail">{f['detail']}</div>
        </div>
        """
        for f in MAP_FLASH_STORIES
    )

    wire_cols_html = []
    for col_sections in wire_data:
        sec_blocks = []
        for sec in col_sections:
            items_html = "".join(
                f'<li><span class="wire-loc" style="color:{sec["color"]}">{loc}:</span> {txt}</li>'
                for loc, txt in sec["items"]
            )
            sec_blocks.append(
                f"""
                <section class="wire-section">
                  <div class="wire-hdr" style="border-bottom-color:{sec['color']};color:{sec['color']}">
                    <span class="wire-dot" style="background:{sec['color']}"></span>{sec['title']}
                  </div>
                  <ul class="wire-list">{items_html}</ul>
                </section>
                """
            )
        wire_cols_html.append(f'<div class="wire-col">{"".join(sec_blocks)}</div>')

    wire_font = "12.0px" if is_18 else "12.6px"
    wire_loc_font = "11.3px" if is_18 else "11.9px"
    wire_li_gap = "3.4px" if is_18 else "5.5px"
    wire_li_pad = "2.8px" if is_18 else "5.0px"
    wire_col_gap = "5px" if is_18 else "4px"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    width: 1024px;
    height: 1024px;
    overflow: hidden;
    background: #f6f3ec;
    color: #0e1726;
    font-family: "Liberation Sans", "DejaVu Sans", sans-serif;
    -webkit-font-smoothing: antialiased;
  }}
  .page {{
    width: 1024px;
    height: 1024px;
    padding: 9px 14px 7px 14px;
    display: flex;
    flex-direction: column;
  }}

  /* BAND 1: HIGH-CONTRAST NAVY MASTHEAD */
  .masthead {{
    background: #0d1c30;
    color: #ffffff;
    border-radius: 4px;
    border-bottom: 3px solid #d97706;
    padding: 6px 14px;
    margin-bottom: 7px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 66px;
    flex-shrink: 0;
  }}
  .mast-left {{
    display: flex;
    flex-direction: column;
    justify-content: center;
  }}
  .mast-title {{
    font-family: "C059", "P052", "Liberation Serif", serif;
    font-size: 36px;
    font-weight: 700;
    line-height: 1.0;
    letter-spacing: -0.3px;
  }}
  .title-accent {{ color: #fbbf24; }}
  .sub-line {{
    font-size: 10.6px;
    font-weight: 700;
    letter-spacing: 1.0px;
    text-transform: uppercase;
    color: #cbd5e1;
    margin-top: 3px;
  }}
  .date-block {{
    background: #c8232c;
    color: #ffffff;
    padding: 5px 14px;
    border-radius: 4px;
    text-align: right;
    box-shadow: 0 2px 4px rgba(0,0,0,0.28);
  }}
  .date-day {{
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 1.6px;
    text-transform: uppercase;
    opacity: 0.94;
  }}
  .date-main {{
    font-family: "Nimbus Sans Narrow", "Liberation Sans", sans-serif;
    font-size: 29px;
    font-weight: 700;
    line-height: 1.02;
    letter-spacing: 0.3px;
  }}

  /* BAND 2: 6 ILLUSTRATED HERO CARDS (BALANCED 2-LINE 19.2px HEADLINES) */
  .hero-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(2, 232px);
    gap: 7px 9px;
    flex-shrink: 0;
    margin-bottom: 7px;
  }}
  .hero-card {{
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-top-width: 3.5px;
    border-radius: 3px;
    padding: 5px 8px 4px 8px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.06);
  }}
  .card-meta {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 4px;
    height: 16px;
    flex-shrink: 0;
  }}
  .region-tag {{
    color: #ffffff;
    font-size: 9.2px;
    font-weight: 700;
    letter-spacing: 0.5px;
    padding: 2px 6px;
    border-radius: 2px;
    text-transform: uppercase;
  }}
  .visual-box {{
    width: 100%;
    height: 110px;
    border-radius: 2px;
    overflow: hidden;
    flex-shrink: 0;
    position: relative;
    border: 1px solid rgba(15, 23, 42, 0.18);
    background: #0d1c30;
  }}
  .visual-box img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }}
  .corner-badge {{
    position: absolute;
    bottom: 5px;
    right: 5px;
    background: rgba(11, 23, 40, 0.92);
    color: #fef3c7;
    border: 1px solid rgba(254, 243, 199, 0.55);
    font-family: "Liberation Mono", monospace;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 2px;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.55);
    letter-spacing: 0.25px;
  }}
  .diptych-tag {{
    position: absolute;
    bottom: 4px;
    background: rgba(11, 23, 40, 0.90);
    color: #fef3c7;
    border: 1px solid rgba(254, 243, 199, 0.48);
    font-family: "Liberation Mono", monospace;
    font-size: 9.5px;
    font-weight: 700;
    padding: 1.5px 5px;
    border-radius: 2px;
  }}
  .left-tag {{ left: 5px; }}
  .right-tag {{ right: 5px; }}

  .hero-headline {{
    font-family: "Nimbus Sans Narrow", "Liberation Sans", sans-serif;
    font-size: 19.2px;
    font-weight: 700;
    line-height: 1.07;
    color: #09121e;
    margin-top: 5px;
    margin-bottom: 3px;
    flex-shrink: 0;
    letter-spacing: -0.15px;
  }}
  .hero-fact {{
    font-size: 11.3px;
    line-height: 1.22;
    color: #334155;
    flex-grow: 1;
    overflow: hidden;
  }}

  /* BAND 3: WORLD-MAP HOTSPOT DISPATCH RIBBON (130px -> ZERO FLASH CLIPPING) */
  .atlas-band {{
    height: 130px;
    background: #0f2035;
    border-radius: 4px;
    border: 1px solid #1e3a5f;
    display: grid;
    grid-template-columns: 516px 1fr;
    overflow: hidden;
    flex-shrink: 0;
    margin-bottom: 7px;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.14);
  }}
  .map-panel {{
    width: 516px;
    height: 130px;
    border-right: 1px solid #294566;
    overflow: hidden;
  }}
  .map-panel svg {{
    width: 100%;
    height: 100%;
    display: block;
  }}
  .flash-panel {{
    padding: 5px 8px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    gap: 5px 7px;
  }}
  .flash-item {{
    background: rgba(255, 255, 255, 0.065);
    border-left: 3px solid;
    border-radius: 2px;
    padding: 3.5px 6px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    overflow: hidden;
  }}
  .flash-tag {{
    font-size: 8.4px;
    font-weight: 700;
    letter-spacing: 0.65px;
    text-transform: uppercase;
    line-height: 1.05;
  }}
  .flash-title {{
    font-family: "Nimbus Sans Narrow", "Liberation Sans", sans-serif;
    font-size: 14.3px;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.08;
    margin-top: 1px;
  }}
  .flash-detail {{
    font-size: 10.1px;
    line-height: 1.15;
    color: #cbd5e1;
    margin-top: 2px;
  }}

  /* BAND 4: 3-COLUMN GLOBAL WIRE */
  .wire-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0 11px;
    flex-grow: 1;
    min-height: 0;
    overflow: hidden;
  }}
  .wire-col {{
    display: flex;
    flex-direction: column;
    gap: {wire_col_gap};
    border-right: 1px solid #cbd5e1;
    padding-right: 10px;
    overflow: hidden;
  }}
  .wire-col:last-child {{
    border-right: none;
    padding-right: 0;
  }}
  .wire-section {{
    display: flex;
    flex-direction: column;
  }}
  .wire-hdr {{
    font-size: 10.2px;
    font-weight: 700;
    letter-spacing: 0.65px;
    text-transform: uppercase;
    border-bottom: 1.8px solid;
    padding-bottom: 2px;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 5px;
  }}
  .wire-dot {{
    width: 7px;
    height: 7px;
    border-radius: 1px;
    display: inline-block;
  }}
  .wire-list {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: {wire_li_gap};
  }}
  .wire-list li {{
    font-size: {wire_font};
    line-height: 1.22;
    color: #1e293b;
    padding-bottom: {wire_li_pad};
    border-bottom: 1px dotted #cbd5e1;
  }}
  .wire-list li:last-child {{
    border-bottom: none;
    padding-bottom: 0;
  }}
  .wire-loc {{
    font-weight: 700;
    font-size: {wire_loc_font};
    letter-spacing: 0.2px;
  }}

  /* BAND 5: CLEAN AUTHENTIC PUBLICATION FOOTER */
  .footer {{
    margin-top: 5px;
    padding-top: 4px;
    border-top: 1.5px solid #0d1c30;
    display: flex;
    justify-content: space-between;
    font-size: 9.6px;
    font-weight: 700;
    color: #475569;
    letter-spacing: 0.45px;
    flex-shrink: 0;
  }}
</style>
</head>
<body>
  <main class="page">
    <header class="masthead">
      <div class="mast-left">
        <div class="mast-title">WORLD NEWS <span class="title-accent">IN ONE DAY</span></div>
        <div class="sub-line">INTERNATIONAL EDITION · MAJOR DEVELOPMENTS WORLDWIDE · UTC</div>
      </div>
      <div class="date-block">
        <div class="date-day">TUESDAY</div>
        <div class="date-main">24 NOVEMBER 2026</div>
      </div>
    </header>

    <section class="hero-grid">
      {''.join(hero_cards_html)}
    </section>

    <section class="atlas-band">
      <div class="map-panel">{WORLD_MAP_SVG}</div>
      <div class="flash-panel">{flash_cards_html}</div>
    </section>

    <section class="wire-grid">
      {''.join(wire_cols_html)}
    </section>

    <footer class="footer">
      <span>TUESDAY, 24 NOVEMBER 2026 · GLOBAL BROADSHEET · UTC EDITION</span>
      <span>EUROPE · MIDDLE EAST · AMERICAS · ASIA-PACIFIC · AFRICA · SCIENCE &amp; MARKETS</span>
    </footer>
  </main>
</body>
</html>
"""


def render_mode(mode: str, out_png: Path, out_thumb: Path) -> dict:
    html_path = out_png.with_suffix(".html")
    html_path.write_text(build_html(mode), encoding="utf-8")

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox", "--disable-gpu", "--font-render-hinting=none"])
        page = browser.new_page(viewport={"width": 1024, "height": 1024}, device_scale_factor=1)
        page.goto(f"file://{html_path.resolve()}", wait_until="load")
        page.wait_for_timeout(150)

        overflow_report = page.evaluate("""() => {
          const issues = [];
          const checks = document.querySelectorAll('.hero-card, .hero-headline, .hero-fact, .flash-item, .flash-panel, .wire-col, .wire-grid, .page');
          for (const el of checks) {
            if (el.scrollHeight > el.clientHeight + 1 || el.scrollWidth > el.clientWidth + 1) {
              issues.push({
                cls: el.className,
                scrollH: el.scrollHeight,
                clientH: el.clientHeight,
                scrollW: el.scrollWidth,
                clientW: el.clientWidth,
                text: (el.innerText || '').slice(0, 55)
              });
            }
          }
          return issues;
        }""")

        page.screenshot(path=str(out_png), type="png", clip={"x": 0, "y": 0, "width": 1024, "height": 1024})
        browser.close()

    img = Image.open(out_png).convert("RGB")
    assert img.size == (1024, 1024), f"Unexpected size {img.size}"

    img.save(out_png, format="PNG", optimize=True, compress_level=9)
    png_bytes = out_png.stat().st_size

    jpg88_buf = io.BytesIO()
    img.save(jpg88_buf, format="JPEG", quality=88, optimize=True, subsampling=0)
    jpg88_bytes = len(jpg88_buf.getvalue())

    jpg92_buf = io.BytesIO()
    img.save(jpg92_buf, format="JPEG", quality=92, optimize=True, subsampling=0)
    jpg92_bytes = len(jpg92_buf.getvalue())

    thumb = img.resize((300, 300), Image.Resampling.LANCZOS)
    thumb.save(out_thumb, format="PNG", optimize=True)

    return {
        "mode": mode,
        "png_path": str(out_png),
        "thumb_path": str(out_thumb),
        "png_bytes": png_bytes,
        "jpg88_444_bytes": jpg88_bytes,
        "jpg92_444_bytes": jpg92_bytes,
        "overflow_issues": overflow_report,
    }


def main() -> None:
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/news_v21")
    out_dir.mkdir(parents=True, exist_ok=True)
    modes = sys.argv[2:] if len(sys.argv) > 2 else ["atlas18", "atlas15"]
    for m in modes:
        res = render_mode(m, out_dir / f"v21_{m}.png", out_dir / f"v21_{m}_300.png")
        print(res)


if __name__ == "__main__":
    main()

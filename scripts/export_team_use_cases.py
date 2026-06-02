#!/usr/bin/env python3
"""Export public-safe Agentlas team use cases.

This publishes marketplace samples derived from the public benchmark where safe.
Non-public Agentlas system-generation technology is not exported. When a benchmark
case would expose non-public capability, this script substitutes a
public-safe operational team and labels it as an unscored replacement.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_APP_DIR = ROOT.parents[2] / "agentlas" / "AgentsAtlas" / "app"
PUBLIC_TEAM_DIR = ROOT / "marketplace" / "agent-teams"
PUBLIC_DOC = ROOT / "docs" / "marketplace-use-cases.md"


def agent(role: str, job: str, skills: list[str], tier: str, apis: list[str] | None = None, deliverables: list[str] | None = None) -> dict[str, Any]:
    return {
        "role": role,
        "job": job,
        "skills": skills,
        "modelTier": tier,
        "externalApis": apis or [],
        "deliverables": deliverables or [],
    }


def edge(from_: str, to: str, handoff: str) -> dict[str, str]:
    return {"from": from_, "to": to, "handoff": handoff}


def team(
    *,
    slug: str,
    prompt_id: str,
    prompt_name: str,
    selected_runtime: str,
    selected_model: str,
    score: float | None,
    wall_time_seconds: float | None,
    ko: dict[str, Any],
    en: dict[str, Any],
    metadata_source: str = "agentlas-model-benchmark-long-timeout",
    selection_rule: str = "highest score, shortest wall time as tie-breaker",
) -> dict[str, Any]:
    metadata = {
        "source": metadata_source,
        "promptId": prompt_id,
        "promptName": prompt_name,
        "selectionRule": selection_rule,
        "selectedRuntime": selected_runtime,
        "selectedModel": selected_model,
        "score100": score,
        "wallTimeSeconds": wall_time_seconds,
    }
    return {
        "slug": slug,
        "ko": {**ko, "slug": slug, "benchmark": metadata},
        "en": {**en, "slug": slug, "benchmark": metadata},
    }


TEAMS = [
    team(
        slug="benchmark-small-fund-research-os",
        prompt_id="P01",
        prompt_name="P01_INVESTMENT_FUND_AGENT",
        selected_runtime="agentlas_codex",
        selected_model="gpt-5.5",
        score=96.0,
        wall_time_seconds=68.048,
        ko={
            "name": "소형 펀드 리서치 OS",
            "tagline": "시장 데이터, 공시, 뉴스, 포트폴리오 한도, 애널리스트 메모를 한 팀으로 묶어 승인 가능한 투자 리서치 패킷을 만듭니다.",
            "category": "finance",
            "orchestrator": {
                "role": "투자위원회 HQ",
                "job": "리서치 요청을 데이터 수집, 기업/매크로 분석, 리스크 검증, 포트폴리오 제안, 컴플라이언스 리뷰로 라우팅한다. 주문 실행은 항상 사용자 승인 전까지 차단한다.",
            },
            "agents": [
                agent("시장·공시 수집관", "가격, 공시, 뉴스, 매크로 지표, 실적 캘린더를 수집하고 오래된 근거를 표시한다.", ["market-data-ingest", "filing-normalizer", "stale-evidence-check"], "cheap", ["Market data API", "SEC/EDGAR or DART", "News API"], ["근거 스냅샷", "누락 데이터 목록"]),
                agent("기업 리서치 애널리스트", "기업별 실적, 밸류에이션, 촉매, 리스크를 정리하고 투자 논리를 작성한다.", ["fundamental-analysis", "thesis-writing", "source-citation"], "premium", ["Filings API", "Financial data API"], ["종목별 투자 논리", "근거 표"]),
                agent("매크로·섹터 애널리스트", "거시 지표와 섹터 흐름이 포트폴리오에 주는 영향을 평가한다.", ["macro-briefing", "sector-map", "scenario-analysis"], "standard", ["Economic calendar", "Rates/Fx data"], ["매크로 브리프", "섹터 위험 신호"]),
                agent("리스크·반론 검증관", "투자 논리를 반대로 검증하고 집중도, 유동성, 손실 한도를 점검한다.", ["bear-case-review", "risk-budget-check", "contradiction-check"], "premium", ["Portfolio holdings API"], ["반론 리포트", "위험 한도 판정"]),
                agent("포트폴리오 제안 매니저", "승인 가능한 리밸런싱 제안을 만들되 주문 실행은 하지 않는다.", ["rebalance-planning", "approval-packaging", "backtest-summary"], "standard", ["Portfolio holdings API"], ["승인 대기 리밸런싱안", "백테스트 메모"]),
            ],
            "edges": [
                edge("투자위원회 HQ", "시장·공시 수집관", "리서치 대상과 필요한 데이터 범위"),
                edge("시장·공시 수집관", "기업 리서치 애널리스트", "출처가 붙은 기업 데이터"),
                edge("시장·공시 수집관", "매크로·섹터 애널리스트", "거시·섹터 이벤트 큐"),
                edge("기업 리서치 애널리스트", "리스크·반론 검증관", "투자 논리와 반대 근거"),
                edge("리스크·반론 검증관", "포트폴리오 제안 매니저", "통과한 후보와 제한 조건"),
            ],
            "reviewGates": ["주문 실행 전 사용자 승인 필수", "출처 없는 수치 사용 금지", "데이터 지연·결측 시 실행안 차단", "리스크 한도 위반 시 자동 반려"],
            "costGuardrails": ["수집·요약은 cheap 티어", "투자 논리와 반론 검증만 premium 티어", "동일 종목 신규 근거 없는 재분석 차단", "일일 분석 종목 수 상한"],
            "selfImprovement": "성과와 논리의 적중 여부를 메모리 레저에 남기고, 실패한 thesis 유형을 다음 리서치 체크리스트에 반영한다.",
            "creditBand": "high",
            "userSetup": ["시장 데이터 키 연결", "포트폴리오 보유/한도 입력", "승인권자와 주문 금지 정책 설정", "리포트 주기 선택"],
        },
        en={
            "name": "Small Fund Research OS",
            "tagline": "Coordinates market data, filings, news, portfolio limits, and analyst notes into approval-ready investment research packets.",
            "category": "finance",
            "orchestrator": {
                "role": "Investment Committee HQ",
                "job": "Routes research requests through data intake, company and macro analysis, risk review, portfolio proposal, and compliance review. Blocks trade execution until explicit user approval.",
            },
            "agents": [
                agent("Market & Filing Intake", "Collects prices, filings, news, macro indicators, and earnings calendars while flagging stale evidence.", ["market-data-ingest", "filing-normalizer", "stale-evidence-check"], "cheap", ["Market data API", "SEC/EDGAR or DART", "News API"], ["Evidence snapshot", "Missing data list"]),
                agent("Company Research Analyst", "Summarizes company performance, valuation, catalysts, and risk into investment theses.", ["fundamental-analysis", "thesis-writing", "source-citation"], "premium", ["Filings API", "Financial data API"], ["Per-company thesis", "Cited evidence table"]),
                agent("Macro & Sector Analyst", "Assesses how macro indicators and sector flows affect the portfolio.", ["macro-briefing", "sector-map", "scenario-analysis"], "standard", ["Economic calendar", "Rates/Fx data"], ["Macro brief", "Sector risk signals"]),
                agent("Risk & Skeptic Reviewer", "Challenges the thesis and checks concentration, liquidity, and loss limits.", ["bear-case-review", "risk-budget-check", "contradiction-check"], "premium", ["Portfolio holdings API"], ["Bear-case report", "Risk-limit verdict"]),
                agent("Portfolio Proposal Manager", "Builds approval-ready rebalance proposals but never submits trades.", ["rebalance-planning", "approval-packaging", "backtest-summary"], "standard", ["Portfolio holdings API"], ["Pending rebalance proposal", "Backtest memo"]),
            ],
            "edges": [
                edge("Investment Committee HQ", "Market & Filing Intake", "Research target and required data scope"),
                edge("Market & Filing Intake", "Company Research Analyst", "Cited company data"),
                edge("Market & Filing Intake", "Macro & Sector Analyst", "Macro and sector event queue"),
                edge("Company Research Analyst", "Risk & Skeptic Reviewer", "Thesis and bear case"),
                edge("Risk & Skeptic Reviewer", "Portfolio Proposal Manager", "Approved candidates and constraints"),
            ],
            "reviewGates": ["Explicit user approval before any trade execution", "No uncited financial claims", "Block proposals when data is stale or missing", "Reject risk-limit violations"],
            "costGuardrails": ["Cheap tier for intake and summaries", "Premium only for thesis and adversarial review", "No repeated stock analysis without new evidence", "Daily cap on analyzed names"],
            "selfImprovement": "Logs outcome quality and failed thesis patterns into a memory ledger, then updates the next research checklist.",
            "creditBand": "high",
            "userSetup": ["Connect market data keys", "Enter holdings and risk limits", "Set approvers and no-trade policy", "Choose report cadence"],
        },
    ),
    team(
        slug="benchmark-aml-fraud-investigation-team",
        prompt_id="P02",
        prompt_name="P02_AML_FRAUD_INVESTIGATION_AGENT",
        selected_runtime="agentlas_gemini",
        selected_model="gemini-3.1-pro-preview",
        score=96.0,
        wall_time_seconds=38.574,
        ko={
            "name": "AML·사기 조사 팀",
            "tagline": "경보 triage부터 증거 체인, 제재·PEP 확인, 감사 제출 리포트까지 한 번에 정리하는 조사 운영팀입니다.",
            "category": "compliance",
            "orchestrator": {"role": "조사 지휘 HQ", "job": "경보 우선순위를 정하고 KYC, 거래 패턴, 제재 리스트, 증거 보존, 리포트 작성 단계를 라우팅한다. 고객 조치나 신고는 승인 게이트를 통과해야 한다."},
            "agents": [
                agent("경보 트리아지", "거래 경보를 위험도와 긴급도별로 분류한다.", ["alert-triage", "case-priority", "false-positive-filter"], "cheap", ["Transaction monitoring system"], ["경보 우선순위", "초기 사건 요약"]),
                agent("KYC·계정 분석관", "고객 프로필, beneficial owner, 과거 검증 기록을 확인한다.", ["kyc-review", "entity-resolution", "profile-drift"], "standard", ["KYC provider", "CRM"], ["KYC 차이점", "위험 프로필"]),
                agent("거래 패턴 분석관", "거래 네트워크, 분할 송금, 이상 패턴을 탐지한다.", ["graph-analysis", "velocity-check", "pattern-mining"], "premium", ["Transaction graph DB"], ["패턴 분석", "연결 계정 지도"]),
                agent("제재·PEP 검증관", "제재, PEP, adverse media 결과를 증거와 함께 검증한다.", ["sanctions-screen", "pep-check", "adverse-media-review"], "premium", ["Sanctions API", "Web search"], ["제재 검증 표", "근거 링크"]),
                agent("감사 리포트 작성관", "증거 체인과 의사결정 로그를 감사 가능한 문서로 만든다.", ["chain-of-custody", "sar-draft", "audit-reporting"], "standard", [], ["조사 리포트", "승인 대기 조치안"]),
            ],
            "edges": [edge("조사 지휘 HQ", "경보 트리아지", "신규 경보와 정책 범위"), edge("경보 트리아지", "KYC·계정 분석관", "우선 사건과 관련 고객"), edge("KYC·계정 분석관", "거래 패턴 분석관", "계정·관계자 컨텍스트"), edge("거래 패턴 분석관", "제재·PEP 검증관", "고위험 엔티티"), edge("제재·PEP 검증관", "감사 리포트 작성관", "검증 결과와 증거")],
            "reviewGates": ["고객 계정 동결·신고 전 준법 승인", "증거 출처와 조회 시각 기록 필수", "PII 최소 공개", "모델 추정만으로 혐의 확정 금지"],
            "costGuardrails": ["대량 경보 분류는 cheap 티어", "그래프·제재 검증만 premium", "중복 사건 병합", "낮은 위험 경보는 배치 처리"],
            "selfImprovement": "오탐/정탐 결과를 사건 유형별로 기록해 경보 우선순위와 false-positive 필터를 조정한다.",
            "creditBand": "high",
            "userSetup": ["거래 모니터링 시스템 연결", "KYC/제재 API 키 입력", "승인권자와 신고 기준 설정", "PII 보존 정책 확인"],
        },
        en={
            "name": "AML & Fraud Investigation Team",
            "tagline": "Runs alert triage, evidence custody, sanctions and PEP checks, and audit-ready investigation reporting.",
            "category": "compliance",
            "orchestrator": {"role": "Investigation Command HQ", "job": "Prioritizes alerts and routes work across KYC, transaction patterns, sanctions lists, evidence custody, and reporting. Customer actions or filings require approval gates."},
            "agents": [
                agent("Alert Triage", "Classifies transaction alerts by risk and urgency.", ["alert-triage", "case-priority", "false-positive-filter"], "cheap", ["Transaction monitoring system"], ["Priority queue", "Initial case brief"]),
                agent("KYC & Account Analyst", "Checks profiles, beneficial owners, and historical verification records.", ["kyc-review", "entity-resolution", "profile-drift"], "standard", ["KYC provider", "CRM"], ["KYC deltas", "Risk profile"]),
                agent("Transaction Pattern Analyst", "Detects transaction networks, structuring, and anomalous patterns.", ["graph-analysis", "velocity-check", "pattern-mining"], "premium", ["Transaction graph DB"], ["Pattern analysis", "Connected-account map"]),
                agent("Sanctions & PEP Reviewer", "Verifies sanctions, PEP, and adverse media hits with evidence.", ["sanctions-screen", "pep-check", "adverse-media-review"], "premium", ["Sanctions API", "Web search"], ["Sanctions evidence table", "Source links"]),
                agent("Audit Report Writer", "Turns evidence custody and decision logs into reviewable reports.", ["chain-of-custody", "sar-draft", "audit-reporting"], "standard", [], ["Investigation report", "Pending action package"]),
            ],
            "edges": [edge("Investigation Command HQ", "Alert Triage", "New alert and policy scope"), edge("Alert Triage", "KYC & Account Analyst", "Priority cases and related customers"), edge("KYC & Account Analyst", "Transaction Pattern Analyst", "Account and party context"), edge("Transaction Pattern Analyst", "Sanctions & PEP Reviewer", "High-risk entities"), edge("Sanctions & PEP Reviewer", "Audit Report Writer", "Verified findings and evidence")],
            "reviewGates": ["Compliance approval before account freezes or filings", "Record source and lookup time for every evidence item", "Minimize exposed PII", "Never confirm wrongdoing from model inference alone"],
            "costGuardrails": ["Cheap tier for bulk alert sorting", "Premium only for graph and sanctions review", "Merge duplicate cases", "Batch low-risk alerts"],
            "selfImprovement": "Stores true/false positive outcomes by typology to tune alert priority and false-positive filters.",
            "creditBand": "high",
            "userSetup": ["Connect transaction monitoring", "Add KYC/sanctions API keys", "Set approvers and filing rules", "Confirm PII retention policy"],
        },
    ),
    team(
        slug="benchmark-disaster-drone-swarm-command",
        prompt_id="P03",
        prompt_name="P03_DISASTER_DRONE_SWARM_AGENT",
        selected_runtime="agentlas_upstage",
        selected_model="solar-pro2",
        score=98.0,
        wall_time_seconds=10.381,
        ko={
            "name": "재난 드론 군집 지휘팀",
            "tagline": "지도, 날씨, 배터리, 통신 상태를 보며 수색·정찰 드론 임무를 안전 게이트 안에서 조율합니다.",
            "category": "emergency",
            "orchestrator": {"role": "현장 임무 HQ", "job": "사람 구조와 안전을 최우선으로 임무 구역, 드론 역할, 비행 제한, 승인 게이트를 관리한다. 자동 비행 명령은 승인 전 차단한다."},
            "agents": [
                agent("상황 지도 분석관", "재난 구역, 장애물, 금지 구역, 우선 수색 영역을 지도화한다.", ["gis-mapping", "hazard-zoning", "priority-grid"], "standard", ["GIS map API"], ["작전 지도", "위험 구역"]),
                agent("군집 임무 플래너", "드론별 탐색 경로, 고도, 임무 순서를 계획한다.", ["swarm-routing", "coverage-planning", "battery-aware-scheduling"], "premium", ["Drone fleet API"], ["비행 계획", "배터리별 임무표"]),
                agent("텔레메트리 모니터", "배터리, 위치, 링크 품질, 충돌 위험을 실시간으로 감시한다.", ["telemetry-watch", "collision-risk", "fallback-trigger"], "standard", ["Drone telemetry"], ["상태 대시보드", "비상 알림"]),
                agent("영상·센서 판독관", "영상, 열화상, 센서 값을 구조 신호와 위험 신호로 분류한다.", ["vision-review", "thermal-detection", "confidence-labeling"], "premium", ["Video stream", "Thermal sensor"], ["후보 구조 지점", "신뢰도 표"]),
                agent("안전 승인관", "비행 금지, 사람 밀집, 날씨 악화, 배터리 위험을 최종 차단한다.", ["safety-gate", "airspace-check", "human-approval"], "standard", ["Weather API", "Airspace data"], ["승인/중지 판정", "안전 로그"]),
            ],
            "edges": [edge("현장 임무 HQ", "상황 지도 분석관", "구역과 목표"), edge("상황 지도 분석관", "군집 임무 플래너", "지도 격자와 위험 구역"), edge("군집 임무 플래너", "안전 승인관", "비행 계획"), edge("안전 승인관", "텔레메트리 모니터", "승인된 임무"), edge("텔레메트리 모니터", "영상·센서 판독관", "실시간 영상·센서 패킷")],
            "reviewGates": ["비행 명령 전 현장 책임자 승인", "비행 금지구역·날씨 위험 차단", "충돌·배터리 임계치 시 즉시 귀환", "사람 위치 정보 최소화"],
            "costGuardrails": ["지도·상태 감시는 standard", "영상 판독과 군집 최적화만 premium", "중복 영상 프레임 샘플링", "임무 변경은 이벤트 기반"],
            "selfImprovement": "임무 후 실제 커버리지, 오탐 구조 지점, 배터리 예측 오류를 기록해 다음 경로 계획을 보정한다.",
            "creditBand": "high",
            "userSetup": ["드론 fleet API 연결", "지도/날씨/공역 데이터 연결", "승인 책임자 지정", "비행 금지 정책 입력"],
        },
        en={
            "name": "Disaster Drone Swarm Command",
            "tagline": "Coordinates search and reconnaissance drones using maps, weather, batteries, and telemetry inside strict safety gates.",
            "category": "emergency",
            "orchestrator": {"role": "Field Mission HQ", "job": "Prioritizes human safety while managing mission areas, drone roles, flight restrictions, and approval gates. Blocks automated flight commands until approval."},
            "agents": [
                agent("Situation Map Analyst", "Maps disaster zones, obstacles, no-fly areas, and priority search regions.", ["gis-mapping", "hazard-zoning", "priority-grid"], "standard", ["GIS map API"], ["Operations map", "Hazard zones"]),
                agent("Swarm Mission Planner", "Plans route, altitude, and sequence for each drone.", ["swarm-routing", "coverage-planning", "battery-aware-scheduling"], "premium", ["Drone fleet API"], ["Flight plan", "Battery-aware mission sheet"]),
                agent("Telemetry Monitor", "Watches battery, position, link quality, and collision risk in real time.", ["telemetry-watch", "collision-risk", "fallback-trigger"], "standard", ["Drone telemetry"], ["Status dashboard", "Emergency alerts"]),
                agent("Video & Sensor Interpreter", "Classifies video, thermal, and sensor signals into rescue leads and hazards.", ["vision-review", "thermal-detection", "confidence-labeling"], "premium", ["Video stream", "Thermal sensor"], ["Candidate rescue points", "Confidence table"]),
                agent("Safety Approval Officer", "Blocks no-fly, crowd, weather, and battery hazards.", ["safety-gate", "airspace-check", "human-approval"], "standard", ["Weather API", "Airspace data"], ["Approve/stop verdict", "Safety log"]),
            ],
            "edges": [edge("Field Mission HQ", "Situation Map Analyst", "Area and mission objective"), edge("Situation Map Analyst", "Swarm Mission Planner", "Grid and hazard map"), edge("Swarm Mission Planner", "Safety Approval Officer", "Flight plan"), edge("Safety Approval Officer", "Telemetry Monitor", "Approved mission"), edge("Telemetry Monitor", "Video & Sensor Interpreter", "Live sensor packets")],
            "reviewGates": ["Field commander approval before flight commands", "Block no-fly and weather hazards", "Immediate return on collision or battery thresholds", "Minimize person-location data"],
            "costGuardrails": ["Standard tier for maps and state monitoring", "Premium only for vision and swarm optimization", "Sample duplicate video frames", "Event-based mission replanning"],
            "selfImprovement": "After each mission, logs coverage, false rescue leads, and battery forecast errors to improve future routing.",
            "creditBand": "high",
            "userSetup": ["Connect drone fleet API", "Connect map/weather/airspace feeds", "Assign approval owner", "Enter no-fly policy"],
        },
    ),
]


EXTRA_TEAMS = [
    {
        "slug": "benchmark-film-studio-production-os",
        "prompt_id": "P04",
        "prompt_name": "P04_FILM_STUDIO_AGENT",
        "runtime": "agentlas_upstage",
        "model": "solar-pro2",
        "score": 96.0,
        "wall": 8.204,
        "category": "creative",
        "ko_name": "영화 제작 스튜디오 OS",
        "en_name": "Film Studio Production OS",
        "ko_tag": "스토리 브리프를 대본, 콘티, 예산, 촬영 일정, 후반 작업 패키지로 나누어 제작 가능한 계획으로 바꿉니다.",
        "en_tag": "Turns a story brief into script, storyboard, budget, schedule, and post-production packages.",
        "ko_lead": "프로듀서 HQ",
        "en_lead": "Producer HQ",
        "ko_job": "창작, 제작관리, 예산, 법무, 후반 작업을 순서대로 라우팅하고, 촬영·계약·송출 전 승인 게이트를 둔다.",
        "en_job": "Routes creative, production, budget, legal, and post work while gating shoot, contract, and release decisions.",
        "roles": [
            ("Story Developer", "스토리 개발자", "Expands premise into beat sheet, character arcs, and script risks.", "시놉시스를 비트시트, 캐릭터 아크, 대본 리스크로 확장합니다."),
            ("Storyboard Director", "콘티 디렉터", "Converts scenes into shot lists and visual boards.", "장면을 샷 리스트와 시각 콘티로 변환합니다."),
            ("Production Scheduler", "제작 스케줄러", "Builds location, cast, crew, and shoot schedules.", "장소, 배우, 스태프, 촬영 일정을 구성합니다."),
            ("Budget & Legal Reviewer", "예산·법무 리뷰어", "Checks budget, rights, music, talent, and release constraints.", "예산, 권리, 음악, 출연, 공개 제한을 검토합니다."),
            ("Post Pipeline Manager", "후반 파이프라인 매니저", "Plans edit, VFX, sound, color, and delivery milestones.", "편집, VFX, 사운드, 색보정, 납품 일정을 설계합니다."),
        ],
        "setup_ko": ["스토리 브리프 입력", "예산 상한과 촬영 기간 설정", "권리·음악·출연 승인자 지정", "납품 포맷 선택"],
        "setup_en": ["Enter story brief", "Set budget cap and shooting window", "Assign rights/music/talent approvers", "Choose delivery format"],
    },
    {
        "slug": "benchmark-ai-marketing-agency-hq",
        "prompt_id": "P05",
        "prompt_name": "P05_MARKETING_AGENCY_AGENT",
        "runtime": "agentlas_upstage",
        "model": "solar-pro2",
        "score": 96.0,
        "wall": 9.467,
        "category": "marketing",
        "ko_name": "AI 마케팅 에이전시 HQ",
        "en_name": "AI Marketing Agency HQ",
        "ko_tag": "경쟁사 리서치, 캠페인 전략, 카피·디자인 생산, Playwright 검수, 성과 분석을 한 팀으로 운영합니다.",
        "en_tag": "Runs competitor research, campaign strategy, creative production, Playwright QA, and performance analysis as one agency team.",
        "ko_lead": "캠페인 디렉터 HQ",
        "en_lead": "Campaign Director HQ",
        "ko_job": "브랜드 목표와 채널별 제약을 받아 리서치, 크리에이티브, 랜딩 점검, 성과 측정으로 일을 나눈다.",
        "en_job": "Routes brand goals and channel constraints into research, creative, landing-page QA, and measurement work.",
        "roles": [
            ("Market Researcher", "시장 리서처", "Finds competitors, positioning gaps, and current examples.", "경쟁사, 포지셔닝 빈틈, 현재 사례를 찾습니다."),
            ("Strategy Planner", "전략 플래너", "Builds campaign angle, audience, channel, and offer plan.", "캠페인 각도, 타깃, 채널, 오퍼 전략을 설계합니다."),
            ("Copy & Creative Producer", "카피·크리에이티브 제작자", "Creates hooks, captions, cards, and ad variants.", "훅, 캡션, 카드, 광고 변형을 만듭니다."),
            ("Landing QA Analyst", "랜딩 QA 분석가", "Uses browser checks to review landing pages and funnels.", "브라우저 점검으로 랜딩과 퍼널을 검수합니다."),
            ("Performance Analyst", "성과 분석가", "Reads campaign data and proposes the next experiment.", "성과 데이터를 읽고 다음 실험을 제안합니다."),
        ],
        "setup_ko": ["브랜드 톤과 금지어 입력", "경쟁사/채널 선택", "광고 계정 읽기 권한 연결", "공개 전 승인자 지정"],
        "setup_en": ["Enter brand voice and banned terms", "Choose competitors/channels", "Connect read-only ad accounts", "Assign publish approver"],
    },
    {
        "slug": "benchmark-enterprise-software-delivery-hq",
        "prompt_id": "P06",
        "prompt_name": "P06_ENTERPRISE_SOFTWARE_HQ_AGENT",
        "runtime": "agentlas_upstage",
        "model": "solar-pro2",
        "score": 96.0,
        "wall": 8.403,
        "category": "software",
        "ko_name": "엔터프라이즈 소프트웨어 딜리버리 HQ",
        "en_name": "Enterprise Software Delivery HQ",
        "ko_tag": "PRD, 아키텍처, 구현, 테스트, 보안, 릴리즈 게이트를 갖춘 소프트웨어 제작 본부입니다.",
        "en_tag": "A software delivery HQ with PRD, architecture, implementation, tests, security, and release gates.",
        "ko_lead": "제품·기술 HQ",
        "en_lead": "Product & Engineering HQ",
        "ko_job": "요구사항을 PRD-first 계획, 아키텍처, 구현, QA, 보안 리뷰, 릴리즈 의사결정으로 라우팅한다.",
        "en_job": "Routes requirements into PRD-first planning, architecture, implementation, QA, security review, and release decisions.",
        "roles": [
            ("Product Planner", "제품 플래너", "Turns user goals into PRD, acceptance criteria, and scope boundaries.", "사용자 목표를 PRD, 인수 기준, 범위 경계로 바꿉니다."),
            ("System Architect", "시스템 아키텍트", "Designs data model, API contracts, and integration plan.", "데이터 모델, API 계약, 통합 계획을 설계합니다."),
            ("Implementation Engineer", "구현 엔지니어", "Produces scoped code changes and migration notes.", "범위가 잡힌 코드 변경과 마이그레이션 메모를 만듭니다."),
            ("QA & Eval Engineer", "QA·평가 엔지니어", "Builds smoke tests, regression tests, and eval prompts.", "스모크, 회귀 테스트, 평가 프롬프트를 만듭니다."),
            ("Security & Release Gate", "보안·릴리즈 게이트", "Reviews auth, secrets, permissions, and deployment risk.", "인증, 비밀, 권한, 배포 리스크를 검토합니다."),
        ],
        "setup_ko": ["레포와 배포 환경 연결", "승인자와 릴리즈 기준 설정", "테스트 명령 입력", "보안 금지 패턴 설정"],
        "setup_en": ["Connect repo and deployment target", "Set approvers and release criteria", "Enter test commands", "Set security block patterns"],
    },
    {
        "slug": "benchmark-hospital-operations-command-center",
        "prompt_id": "P07",
        "prompt_name": "P07_HOSPITAL_OPERATIONS_AGENT",
        "runtime": "agentlas_upstage",
        "model": "solar-pro2",
        "score": 96.0,
        "wall": 9.877,
        "category": "healthcare",
        "ko_name": "병원 운영 커맨드 센터",
        "en_name": "Hospital Operations Command Center",
        "ko_tag": "예약, 병상·인력 배정, 환자 흐름, 청구 지원, 임상 행정 문서를 개인정보 보호 안에서 조율합니다.",
        "en_tag": "Coordinates scheduling, beds, staffing, patient flow, claims support, and clinical admin documents with privacy controls.",
        "ko_lead": "병원 운영 HQ",
        "en_lead": "Hospital Operations HQ",
        "ko_job": "운영 병목을 감지하고 예약, 자원, 환자 흐름, 청구, 문서화 팀에 일을 나누며 PHI 접근을 최소화한다.",
        "en_job": "Detects operational bottlenecks and routes work across scheduling, resources, patient flow, claims, and documentation while minimizing PHI access.",
        "roles": [
            ("Scheduling Coordinator", "예약 코디네이터", "Balances appointment slots, no-shows, and physician calendars.", "예약 슬롯, 노쇼, 의료진 캘린더를 조율합니다."),
            ("Resource Planner", "자원 플래너", "Tracks beds, rooms, staff, and equipment constraints.", "병상, 방, 인력, 장비 제약을 추적합니다."),
            ("Patient Flow Analyst", "환자 흐름 분석가", "Finds bottlenecks from intake to discharge.", "접수부터 퇴원까지 병목을 찾습니다."),
            ("Claims Support Analyst", "청구 지원 분석가", "Prepares coding and claim-support evidence for review.", "코딩과 청구 근거를 검토용으로 준비합니다."),
            ("Privacy & Clinical Admin Gate", "개인정보·임상 행정 게이트", "Checks PHI minimization, consent, and clinical note safety.", "PHI 최소화, 동의, 임상 기록 안전성을 점검합니다."),
        ],
        "setup_ko": ["예약/EMR 읽기 권한 연결", "PHI 접근 정책 입력", "운영 KPI 선택", "임상 승인자 지정"],
        "setup_en": ["Connect scheduling/EMR read access", "Enter PHI access policy", "Choose operations KPIs", "Assign clinical approver"],
    },
    {
        "slug": "benchmark-supply-chain-control-tower",
        "prompt_id": "P08",
        "prompt_name": "P08_SUPPLY_CHAIN_CONTROL_TOWER_AGENT",
        "runtime": "agentlas_upstage",
        "model": "solar-pro2",
        "score": 96.0,
        "wall": 9.774,
        "category": "supply_chain",
        "ko_name": "공급망 컨트롤 타워",
        "en_name": "Supply Chain Control Tower",
        "ko_tag": "수요 예측, 재고, 공급업체 리스크, 물류 지연, 사고 대응을 하나의 운영 타워에서 조율합니다.",
        "en_tag": "Coordinates demand forecasting, inventory, supplier risk, logistics delays, and incident response in one operating tower.",
        "ko_lead": "운영 타워 HQ",
        "en_lead": "Operations Tower HQ",
        "ko_job": "재고와 수요 변동, 공급업체 이슈, 물류 지연을 감지해 계획·위험·대응 팀에 라우팅한다.",
        "en_job": "Detects inventory, demand, supplier, and logistics changes, then routes planning, risk, and response work.",
        "roles": [
            ("Demand Forecaster", "수요 예측관", "Builds forecasts from sales, seasonality, and promotion signals.", "판매, 계절성, 프로모션 신호로 수요를 예측합니다."),
            ("Inventory Planner", "재고 플래너", "Checks stockouts, overstock, reorder points, and allocation.", "품절, 과잉재고, 재주문점, 배분을 점검합니다."),
            ("Supplier Risk Analyst", "공급업체 리스크 분석가", "Monitors vendor performance, geopolitical risk, and capacity.", "업체 성과, 지정학 리스크, 생산 여력을 감시합니다."),
            ("Logistics Monitor", "물류 모니터", "Tracks shipments, ETAs, customs, and carrier exceptions.", "배송, ETA, 통관, 운송 예외를 추적합니다."),
            ("Incident Response Planner", "사고 대응 플래너", "Builds mitigation options and approval-ready response plans.", "완화 옵션과 승인 가능한 대응 계획을 만듭니다."),
        ],
        "setup_ko": ["ERP/재고 데이터 연결", "물류 추적 API 연결", "위험 임계치 입력", "승인 가능한 대응 범위 설정"],
        "setup_en": ["Connect ERP/inventory data", "Connect logistics tracking API", "Enter risk thresholds", "Set approved response boundaries"],
    },
    {
        "slug": "benchmark-soc-threat-response-hq",
        "prompt_id": "P09",
        "prompt_name": "P09_SOC_THREAT_RESPONSE_AGENT",
        "runtime": "agentlas_upstage",
        "model": "solar-pro2",
        "score": 95.0,
        "wall": 9.999,
        "category": "security",
        "ko_name": "SOC 위협 대응 HQ",
        "en_name": "SOC Threat Response HQ",
        "ko_tag": "SIEM 경보, 로그, 위협 인텔, MITRE 매핑, 격리 승인, 사후 보고를 조율하는 보안 운영팀입니다.",
        "en_tag": "Coordinates SIEM alerts, logs, threat intel, MITRE mapping, containment approval, and post-incident reporting.",
        "ko_lead": "인시던트 커맨더 HQ",
        "en_lead": "Incident Commander HQ",
        "ko_job": "경보를 분류하고 로그 조사, 위협 인텔, 탐지 규칙, 격리 계획, 보고서를 라우팅한다. 차단·격리는 승인 전 금지한다.",
        "en_job": "Triage alerts and routes log investigation, threat intel, detection rules, containment plans, and reports. Blocks containment actions before approval.",
        "roles": [
            ("Alert Triage Analyst", "경보 트리아지 분석가", "Ranks alerts by severity, asset criticality, and confidence.", "심각도, 자산 중요도, 신뢰도로 경보를 정렬합니다."),
            ("Log Investigator", "로그 조사관", "Queries logs and reconstructs timeline and scope.", "로그를 조회해 타임라인과 범위를 재구성합니다."),
            ("Threat Intel Mapper", "위협 인텔 매퍼", "Maps indicators to MITRE techniques and known campaigns.", "IOC를 MITRE 기술과 알려진 캠페인에 매핑합니다."),
            ("Containment Planner", "격리 계획관", "Drafts block, isolate, and rollback plans for approval.", "차단, 격리, 롤백 계획을 승인용으로 작성합니다."),
            ("Detection Engineer", "탐지 엔지니어", "Writes detection/rule updates and regression checks.", "탐지 규칙 업데이트와 회귀 점검을 작성합니다."),
        ],
        "setup_ko": ["SIEM/로그 읽기 권한 연결", "승인 가능한 격리 액션 정의", "위협 인텔 소스 선택", "사후 보고 템플릿 설정"],
        "setup_en": ["Connect SIEM/log read access", "Define allowed containment actions", "Choose threat intel sources", "Set postmortem template"],
    },
    {
        "slug": "benchmark-vendor-risk-procurement-desk",
        "prompt_id": "S10",
        "prompt_name": "S10_VENDOR_RISK_PROCUREMENT_DESK",
        "runtime": "public_curated",
        "model": "public-safe-template",
        "score": None,
        "wall": None,
        "category": "compliance",
        "ko_name": "벤더 리스크·조달 검토 데스크",
        "en_name": "Vendor Risk & Procurement Review Desk",
        "ko_tag": "신규 SaaS·외주·공급업체를 보안, 비용, 계약, 운영 리스크 관점에서 검토해 승인 가능한 구매 패킷을 만듭니다.",
        "en_tag": "Reviews new SaaS, contractor, and supplier requests across security, cost, contract, and operational risk before purchase approval.",
        "ko_lead": "조달 심사 HQ",
        "en_lead": "Procurement Review HQ",
        "ko_job": "구매 요청을 벤더 조사, 보안 설문, 계약 리스크, 비용 비교, 승인 패킷 작성으로 라우팅한다. 결제와 계약 체결은 승인 전까지 차단한다.",
        "en_job": "Routes purchase requests through vendor research, security questionnaire review, contract risk, cost comparison, and approval packaging. Blocks payment and contract execution before approval.",
        "roles": [
            ("Request Intake Analyst", "구매 요청 접수 분석가", "Captures business need, owner, budget, and required approval path.", "업무 목적, 담당자, 예산, 필요한 승인 경로를 정리합니다."),
            ("Vendor Evidence Researcher", "벤더 근거 조사관", "Collects pricing, security docs, status pages, public incidents, and references.", "가격, 보안 문서, 상태 페이지, 공개 사고, 레퍼런스를 수집합니다."),
            ("Security Questionnaire Reviewer", "보안 설문 검토관", "Checks SOC2/ISO claims, data access, SSO, logging, retention, and subprocessors.", "SOC2/ISO 주장, 데이터 접근, SSO, 로그, 보존, 하위처리자를 확인합니다."),
            ("Contract & Cost Analyst", "계약·비용 분석가", "Compares renewal terms, lock-in, cancellation, hidden usage fees, and alternatives.", "갱신 조건, 락인, 해지, 숨은 사용료, 대안을 비교합니다."),
            ("Approval Packet Manager", "승인 패킷 매니저", "Builds a go/no-go packet with residual risks, required mitigations, and approvers.", "잔여 리스크, 필요 완화책, 승인권자가 포함된 go/no-go 패킷을 작성합니다."),
        ],
        "setup_ko": ["구매 요청 양식 연결", "승인권자와 금액 한도 설정", "보안 설문 템플릿 업로드", "허용/금지 데이터 범위 지정"],
        "setup_en": ["Connect purchase request form", "Set approvers and spend limits", "Upload security questionnaire template", "Define allowed and forbidden data scope"],
    },
]


def generic_from_extra(item: dict[str, Any]) -> dict[str, Any]:
    roles_ko = []
    roles_en = []
    for en_role, ko_role, en_job, ko_job in item["roles"]:
        skills = [en_role.lower().replace(" ", "-"), "handoff-contract", "quality-check"]
        roles_en.append(agent(en_role, en_job, skills, "premium" if len(roles_en) in (1, 3) else "standard", [], [en_job.split(".")[0]]))
        roles_ko.append(agent(ko_role, ko_job, skills, "premium" if len(roles_ko) in (1, 3) else "standard", [], [ko_job.split(".")[0]]))
    ko_edges = [edge(item["ko_lead"], roles_ko[0]["role"], "목표와 입력 범위"), edge(roles_ko[0]["role"], roles_ko[1]["role"], "1차 분석 결과"), edge(roles_ko[1]["role"], roles_ko[2]["role"], "설계/제작 초안"), edge(roles_ko[2]["role"], roles_ko[3]["role"], "검토 대상"), edge(roles_ko[3]["role"], roles_ko[4]["role"], "승인된 패키지")]
    en_edges = [edge(item["en_lead"], roles_en[0]["role"], "Goal and input scope"), edge(roles_en[0]["role"], roles_en[1]["role"], "First-pass analysis"), edge(roles_en[1]["role"], roles_en[2]["role"], "Draft plan or asset"), edge(roles_en[2]["role"], roles_en[3]["role"], "Review target"), edge(roles_en[3]["role"], roles_en[4]["role"], "Approved package")]
    metadata_source = "curated-public-replacement" if item["runtime"] == "public_curated" else "agentlas-model-benchmark-long-timeout"
    selection_rule = "public-safe replacement for a non-public case" if item["runtime"] == "public_curated" else "highest score, shortest wall time as tie-breaker"
    return team(
        slug=item["slug"],
        prompt_id=item["prompt_id"],
        prompt_name=item["prompt_name"],
        selected_runtime=item["runtime"],
        selected_model=item["model"],
        score=item["score"],
        wall_time_seconds=item["wall"],
        ko={
            "name": item["ko_name"],
            "tagline": item["ko_tag"],
            "category": item["category"],
            "orchestrator": {"role": item["ko_lead"], "job": item["ko_job"]},
            "agents": roles_ko,
            "edges": ko_edges,
            "reviewGates": ["외부 전송·삭제·결제·실행 전 사용자 승인", "출처와 판단 근거 기록", "개인정보·비밀값 출력 금지", "실패 시 안전한 로컬 초안으로 대체"],
            "costGuardrails": ["수집·정리는 standard 이하", "고난도 판단만 premium", "동일 입력 반복 실행 차단", "실패 재시도 횟수 제한"],
            "selfImprovement": "실행 결과, 실패 원인, 사용자 수정 사항을 메모리 레저에 기록해 다음 체크리스트와 평가 기준을 갱신한다.",
            "creditBand": "high" if item["category"] in {"emergency", "healthcare", "security", "finance"} else "medium",
            "userSetup": item["setup_ko"],
        },
        en={
            "name": item["en_name"],
            "tagline": item["en_tag"],
            "category": item["category"],
            "orchestrator": {"role": item["en_lead"], "job": item["en_job"]},
            "agents": roles_en,
            "edges": en_edges,
            "reviewGates": ["User approval before external send/delete/payment/execution", "Record sources and rationale", "Never print private data or secrets", "Fall back to safe local drafts on failure"],
            "costGuardrails": ["Use standard or lower for collection and cleanup", "Premium only for difficult judgment", "Block repeated runs on same input", "Cap retry count"],
            "selfImprovement": "Logs run outcomes, failure causes, and user edits into a memory ledger, then updates checklists and eval criteria.",
            "creditBand": "high" if item["category"] in {"emergency", "healthcare", "security", "finance"} else "medium",
            "userSetup": item["setup_en"],
        },
        metadata_source=metadata_source,
        selection_rule=selection_rule,
    )


ALL_TEAMS = TEAMS + [generic_from_extra(item) for item in EXTRA_TEAMS]


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def render_doc() -> str:
    lines = [
        "# Agent Team Marketplace Use Cases",
        "",
        "Date: 2026-06-02",
        "",
        "These 10 team use cases are public-safe marketplace specs. Nine come from the long-timeout Agentlas model benchmark. One non-public case is intentionally replaced by an unscored public procurement workflow.",
        "",
        "| Prompt | Marketplace team | Selected model | Score | Avg wall-time evidence |",
        "|--------|------------------|----------------|------:|------------------------|",
    ]
    for item in ALL_TEAMS:
        b = item["en"]["benchmark"]
        score = f"{b['score100']:.1f}" if isinstance(b.get("score100"), (int, float)) else "unscored"
        wall = f"{b['wallTimeSeconds']:.3f}s" if isinstance(b.get("wallTimeSeconds"), (int, float)) else "n/a"
        lines.append(
            f"| {b['promptId']} | [{item['en']['name']}](../marketplace/agent-teams/{item['slug']}.en.json) | {b['selectedModel']} | {score} | {wall} |"
        )
    lines.extend([
        "",
        "## Web Marketplace Path",
        "",
        "The same JSON specs are exported into the Agentlas web app at `src/lib/teams/samples/` and wired into `src/lib/teams/catalog.ts`, so they appear on `/marketplace` under ready-made agent teams and at `/marketplace/team/<slug>`.",
        "",
        "## Public Files",
        "",
        "- `marketplace/agent-teams/manifest.json`: index for all 10 use cases.",
        "- `marketplace/agent-teams/*.json`: Korean marketplace specs.",
        "- `marketplace/agent-teams/*.en.json`: English marketplace specs.",
    ])
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Export benchmark team use cases to public repo and Agentlas web samples.")
    parser.add_argument("--app-dir", type=Path, default=DEFAULT_APP_DIR)
    parser.add_argument("--skip-app", action="store_true")
    args = parser.parse_args()

    manifest = {
        "schema": "agentlas.marketplace.team-use-cases.v1",
        "generatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "selectionRule": "highest score, shortest wall time as tie-breaker",
        "totalTeams": len(ALL_TEAMS),
        "teams": [
            {
                "slug": item["slug"],
                "nameEn": item["en"]["name"],
                "nameKo": item["ko"]["name"],
                "category": item["en"]["category"],
                "benchmark": item["en"]["benchmark"],
                "publicFiles": {
                    "ko": f"marketplace/agent-teams/{item['slug']}.json",
                    "en": f"marketplace/agent-teams/{item['slug']}.en.json",
                },
            }
            for item in ALL_TEAMS
        ],
    }

    for item in ALL_TEAMS:
        write_json(PUBLIC_TEAM_DIR / f"{item['slug']}.json", item["ko"])
        write_json(PUBLIC_TEAM_DIR / f"{item['slug']}.en.json", item["en"])

    write_json(PUBLIC_TEAM_DIR / "manifest.json", manifest)
    PUBLIC_DOC.parent.mkdir(parents=True, exist_ok=True)
    PUBLIC_DOC.write_text(render_doc(), encoding="utf-8")

    if not args.skip_app:
        samples_dir = args.app_dir / "src" / "lib" / "teams" / "samples"
        for item in ALL_TEAMS:
            write_json(samples_dir / f"{item['slug']}.json", item["ko"])
            write_json(samples_dir / f"{item['slug']}.en.json", item["en"])

    print(json.dumps({"teams": len(ALL_TEAMS), "publicDir": str(PUBLIC_TEAM_DIR), "appDir": None if args.skip_app else str(args.app_dir)}, indent=2))


if __name__ == "__main__":
    main()

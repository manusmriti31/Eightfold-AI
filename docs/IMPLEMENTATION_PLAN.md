# Multi-Agent Company Research System - Implementation Plan

## ✅ Current Status: Phase 3 Complete (Days 1-9)

### Completed Features
- ✅ **All 5 Research Agents** - Profile, Leadership, Financial, Market, Signals
- ✅ **Base Agent Framework** - Reusable architecture for all agents
- ✅ **State Management** - Complete Pydantic models
- ✅ **LangGraph Integration** - Multi-agent orchestration
- ✅ **Parallel Execution** - 2.5x speed improvement
- ✅ **Data Aggregation** - Automatic result merging
- ✅ **Report Synthesis** - Comprehensive report generation
- ✅ **Tools Infrastructure** - 10 tools across 3 categories
- ✅ **Testing Suite** - Individual and integrated tests
- ✅ **Documentation** - Complete guides and API docs

### Performance Metrics
- **Average Confidence**: 85%+
- **Sources per Company**: 45+
- **Processing Time**: ~3-4 minutes (rate limited)
- **Speed Improvement**: 2.5x vs sequential

---

## 🎯 Original Vision
Transform the single-agent research system into a sophisticated multi-agent architecture where 5 specialized agents work in parallel, followed by verification, critique, user interaction, and synthesis layers.

## 🏗️ Architecture

### Agent Hierarchy

```
┌─────────────────────────────────────────────────────────┐
│              COORDINATOR AGENT                          │
│  (Orchestrates workflow, manages state)                 │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│           PARALLEL RESEARCH LAYER (5 Agents)            │
├─────────────┬─────────────┬─────────────┬──────────────┤
│  Profile    │ Leadership  │ Financial   │   Market     │
│  Agent      │ Agent       │ Agent       │   Agent      │
│             │             │             │              │
│ • Business  │ • Founders  │ • Revenue   │ • TAM/SAM    │
│   Model     │ • C-Suite   │ • Margins   │ • Competitors│
│ • Products  │ • LinkedIn  │ • Funding   │ • SWOT       │
│ • Revenue   │ • Past Cos  │ • Ratios    │ • Porter's 5 │
└─────────────┴─────────────┴─────────────┴──────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│              SIGNALS & RISK AGENT                       │
│  • Latest News  • Social Sentiment  • Glassdoor         │
│  • Legal Issues • ESG Metrics       • Hiring Trends     │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│              DATA AGGREGATOR                            │
│  (Merges outputs, resolves duplicates)                  │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│              VERIFICATION AGENT                         │
│  • Cross-checks facts across sources                    │
│  • Flags contradictions                                 │
│  • Assigns confidence scores                            │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│              CRITIC AGENT                               │
│  • Identifies gaps in required fields                   │
│  • Spots vague/generic statements                       │
│  • Generates follow-up research queries                 │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│              USER INTERACTION AGENT                     │
│  • Asks clarifying questions                            │
│  • Handles conversational Q&A                           │
│  • Refines research based on user feedback              │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│              SYNTHESIS AGENT                            │
│  • Combines all data into coherent narrative            │
│  • Formats according to user template                   │
│  • Generates executive summary                          │
└─────────────────────────────────────────────────────────┘
                         ↓
                  FINAL REPORT
```

## 📁 New File Structure

```
company-researcher/
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py              # Abstract base class
│   │   ├── coordinator.py             # Main orchestrator
│   │   │
│   │   ├── research/                  # Research Layer
│   │   │   ├── __init__.py
│   │   │   ├── profile_agent.py       # Agent 1
│   │   │   ├── leadership_agent.py    # Agent 2
│   │   │   ├── financial_agent.py     # Agent 3
│   │   │   ├── market_agent.py        # Agent 4
│   │   │   └── signals_agent.py       # Agent 5
│   │   │
│   │   ├── intelligence/              # Intelligence Layer
│   │   │   ├── __init__.py
│   │   │   ├── verification_agent.py
│   │   │   ├── critic_agent.py
│   │   │   ├── interaction_agent.py
│   │   │   └── synthesis_agent.py
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── prompts.py             # Agent-specific prompts
│   │       └── schemas.py             # Output schemas
│   │
│   ├── graph/
│   │   ├── __init__.py
│   │   ├── multi_agent_graph.py       # LangGraph workflow
│   │   └── state.py                   # State management
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── search/
│   │   │   ├── tavily_search.py
│   │   │   ├── serper_search.py
│   │   │   └── news_api.py
│   │   ├── data/
│   │   │   ├── crunchbase_api.py
│   │   │   ├── linkedin_scraper.py
│   │   │   ├── financial_api.py       # Yahoo Finance, Alpha Vantage
│   │   │   └── glassdoor_scraper.py
│   │   └── analysis/
│   │       ├── sentiment_analyzer.py
│   │       └── fact_checker.py
│   │
│   └── ui/
│       ├── streamlit_app.py           # Enhanced UI
│       └── components/
│           ├── __init__.py
│           ├── agent_monitor.py       # Real-time tracking
│           ├── interactive_qa.py      # Q&A module
│           └── report_viewer.py       # Report display
│
├── config/
│   ├── agent_config.yaml              # Agent configurations
│   └── report_templates.yaml          # Output templates
│
└── tests/
    ├── test_agents.py
    └── test_graph.py
```

## 🔧 Implementation Phases

### Phase 1: Foundation (Days 1-3)

#### 1.1 State Management
**File**: `src/graph/state.py`

Define comprehensive state that flows through all agents:
- Input state (company, requirements)
- Research outputs (5 agent results)
- Intelligence outputs (verification, critique, Q&A)
- Final output (report, metadata)

#### 1.2 Base Agent Class
**File**: `src/agents/base_agent.py`

Abstract class with:
- `async research()` method
- Query generation
- Tool execution
- Structured output
- Confidence scoring

#### 1.3 Tool Infrastructure
**Files**: `src/tools/*`

Set up:
- Tavily search wrapper
- API clients (Crunchbase, Yahoo Finance, etc.)
- Rate limiting
- Error handling

### Phase 2: Research Agents (Days 4-8)

#### 2.1 Profile Agent
**Focus**: Business model, products, revenue streams
**Queries**: 
- "[Company] business model canvas"
- "[Company] revenue streams breakdown"
- "[Company] subsidiaries and parent company"
**Output Schema**:
```python
{
    "company_name": str,
    "founded": int,
    "ownership_type": str,
    "business_model": {
        "value_proposition": str,
        "customer_segments": list,
        "revenue_streams": list,
        "key_partnerships": list
    },
    "products_services": list,
    "confidence_score": float
}
```

#### 2.2 Leadership Agent
**Focus**: Founders, executives, management philosophy
**Queries**:
- "[Founder name] biography career history"
- "[Company] CEO CTO CFO profiles"
- "[Company] management team LinkedIn"
**Output Schema**:
```python
{
    "founders": [
        {
            "name": str,
            "role": str,
            "background": str,
            "previous_companies": list,
            "education": str,
            "linkedin_url": str
        }
    ],
    "executives": [...],
    "leadership_style": str,
    "key_risks": list,
    "confidence_score": float
}
```

#### 2.3 Financial Agent
**Focus**: Revenue, profitability, funding, ratios
**Queries**:
- "[Company] annual revenue 2024"
- "[Company] EBITDA margins profitability"
- "[Company] funding rounds investors"
**Output Schema**:
```python
{
    "revenue": {
        "current": float,
        "yoy_growth": float,
        "currency": str
    },
    "profitability": {
        "ebitda_margin": float,
        "net_margin": float,
        "is_profitable": bool
    },
    "funding": {
        "total_raised": float,
        "last_round": str,
        "investors": list
    },
    "financial_health_score": float,
    "confidence_score": float
}
```

#### 2.4 Market Agent
**Focus**: Industry, competitors, market size, SWOT
**Queries**:
- "[Industry] market size TAM SAM 2024"
- "[Company] competitors comparison"
- "[Company] SWOT analysis competitive advantage"
**Output Schema**:
```python
{
    "market": {
        "tam": float,
        "sam": float,
        "growth_rate": float,
        "industry": str
    },
    "competitors": [
        {
            "name": str,
            "market_share": float,
            "differentiation": str
        }
    ],
    "swot": {
        "strengths": list,
        "weaknesses": list,
        "opportunities": list,
        "threats": list
    },
    "confidence_score": float
}
```

#### 2.5 Signals Agent
**Focus**: News, sentiment, risks, hiring trends
**Queries**:
- "[Company] latest news 2024"
- "[Company] Glassdoor reviews employee sentiment"
- "[Company] legal issues controversies"
**Output Schema**:
```python
{
    "recent_news": [
        {
            "title": str,
            "date": str,
            "summary": str,
            "sentiment": str,
            "source": str
        }
    ],
    "employee_sentiment": {
        "glassdoor_rating": float,
        "review_summary": str
    },
    "risks": [
        {
            "type": str,  # legal, financial, reputational
            "description": str,
            "severity": str
        }
    ],
    "hiring_trends": {
        "open_positions": int,
        "growth_areas": list
    },
    "confidence_score": float
}
```

### Phase 3: Intelligence Layer (Days 9-12)

#### 3.1 Verification Agent
**Purpose**: Cross-check facts, flag contradictions
**Logic**:
- Compare revenue figures across agents
- Verify founder names consistency
- Check date accuracy
- Assign confidence scores

#### 3.2 Critic Agent
**Purpose**: Identify gaps and generate follow-ups
**Logic**:
- Check for missing required fields
- Identify vague statements ("growing rapidly" → need %)
- Generate targeted follow-up queries
- Decide if re-research is needed

#### 3.3 Interaction Agent
**Purpose**: Ask user clarifying questions
**Logic**:
- Detect ambiguities (multiple companies with same name)
- Ask about priorities (focus on financials vs market?)
- Handle user feedback loop
- Refine research direction

#### 3.4 Synthesis Agent
**Purpose**: Create final formatted report
**Logic**:
- Combine all agent outputs
- Apply user-selected template
- Generate executive summary
- Add citations and sources

### Phase 4: LangGraph Integration (Days 13-15)

#### 4.1 Multi-Agent Graph
**File**: `src/graph/multi_agent_graph.py`

```python
# Parallel research layer
builder.add_node("profile_research", profile_agent.research)
builder.add_node("leadership_research", leadership_agent.research)
builder.add_node("financial_research", financial_agent.research)
builder.add_node("market_research", market_agent.research)
builder.add_node("signals_research", signals_agent.research)

# Intelligence layer
builder.add_node("aggregate", aggregate_data)
builder.add_node("verify", verification_agent.verify)
builder.add_node("critique", critic_agent.critique)
builder.add_node("interact", interaction_agent.ask_questions)
builder.add_node("synthesize", synthesis_agent.create_report)

# Edges
builder.add_edge(START, "profile_research")
builder.add_edge(START, "leadership_research")
builder.add_edge(START, "financial_research")
builder.add_edge(START, "market_research")
builder.add_edge(START, "signals_research")

# All research agents → aggregator
builder.add_edge(["profile_research", "leadership_research", 
                  "financial_research", "market_research", 
                  "signals_research"], "aggregate")

builder.add_edge("aggregate", "verify")
builder.add_edge("verify", "critique")

# Conditional: if gaps exist, ask user or re-research
builder.add_conditional_edges("critique", should_interact)
builder.add_edge("interact", "synthesize")
builder.add_edge("synthesize", END)
```

### Phase 5: UI Enhancement (Days 16-20)

#### 5.1 Agent Monitor Component
**Features**:
- 5 parallel progress bars for research agents
- Real-time status updates
- Tool call logs per agent
- Completion indicators

#### 5.2 Interactive Q&A Module
**Features**:
- Chat interface for clarifying questions
- "Dig deeper" buttons on report sections
- Conflict resolution UI
- Feedback loop

#### 5.3 Report Customization
**Features**:
- Template selector:
  - Investment Memo
  - Sales Account Plan
  - Due Diligence Report
  - Competitive Intelligence Brief
- Section reordering drag-and-drop
- Export formats (PDF, DOCX, Markdown, Notion)

## 🎨 UI Mockup Flow

### Step 1: Input
```
┌─────────────────────────────────────────┐
│  🔍 Company Research                    │
│                                         │
│  Company Name: [_____________]          │
│                                         │
│  Report Type:                           │
│  ○ Investment Memo                      │
│  ○ Sales Account Plan                   │
│  ○ Due Diligence                        │
│  ○ Competitive Intelligence             │
│                                         │
│  Focus Areas (select all that apply):   │
│  ☑ Business Model                       │
│  ☑ Leadership                           │
│  ☑ Financials                           │
│  ☑ Market & Competitors                 │
│  ☑ News & Risks                         │
│                                         │
│         [Start Research]                │
└─────────────────────────────────────────┘
```

### Step 2: Research Progress
```
┌─────────────────────────────────────────┐
│  Researching: Tesla Inc.                │
├─────────────────────────────────────────┤
│  Profile Agent        ████████░░ 80%    │
│  Leadership Agent     ██████████ 100%   │
│  Financial Agent      ██████░░░░ 60%    │
│  Market Agent         ████░░░░░░ 40%    │
│  Signals Agent        ██████████ 100%   │
├─────────────────────────────────────────┤
│  Recent Activity:                       │
│  🌐 Searched: "Tesla revenue 2024"      │
│  📊 Extracted: Financial data           │
│  👤 Found: Elon Musk profile            │
│  ⚠️  Detected: Controversy about...     │
└─────────────────────────────────────────┘
```

### Step 3: Verification & Questions
```
┌─────────────────────────────────────────┐
│  ⚠️  I found some conflicting info:     │
│                                         │
│  Revenue figures vary:                  │
│  • Source A: $96.8B (2023)              │
│  • Source B: $81.5B (2023)              │
│                                         │
│  Which source should I prioritize?      │
│  ○ Official SEC filings                 │
│  ○ Latest analyst reports               │
│  ○ Let AI decide                        │
│                                         │
│  Also, I noticed:                       │
│  • Missing data on European market      │
│    share. Should I dig deeper? [Yes/No] │
│                                         │
│         [Continue]                      │
└─────────────────────────────────────────┘
```

### Step 4: Final Report
```
┌─────────────────────────────────────────┐
│  📄 Tesla Inc. - Investment Memo        │
├─────────────────────────────────────────┤
│  [Executive Summary] [Full Report]      │
│  [Sources] [Ask Questions]              │
├─────────────────────────────────────────┤
│  Executive Summary                      │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  Tesla is a $800B market cap...         │
│                                         │
│  💼 Business Model                      │
│  [Expand] [Dig Deeper]                  │
│                                         │
│  👥 Leadership                          │
│  [Expand] [Dig Deeper]                  │
│                                         │
│  💰 Financials                          │
│  [Expand] [Dig Deeper]                  │
│                                         │
│  [Download PDF] [Export to Notion]      │
└─────────────────────────────────────────┘
```

## 🔑 Key Technical Decisions

### 1. Parallel Execution
Use `asyncio.gather()` for 5 research agents to run simultaneously.

### 2. State Management
Use Pydantic models for type safety and validation.

### 3. LLM Strategy
- Research agents: Gemini 2.0 Flash (fast, cheap)
- Synthesis agent: Gemini 2.5 Pro (high quality)

### 4. Tool Selection
- **Search**: Tavily (primary), Serper (backup)
- **Financial**: Yahoo Finance API, Alpha Vantage
- **Social**: Custom scrapers (Glassdoor, G2)
- **News**: NewsAPI, Google News RSS

### 5. Confidence Scoring
Each agent returns confidence score (0-1) based on:
- Source reliability
- Data freshness
- Cross-validation success

## 📊 Success Metrics

1. **Speed**: Complete research in < 2 minutes
2. **Accuracy**: 90%+ fact verification rate
3. **Completeness**: 95%+ required fields populated
4. **User Satisfaction**: < 2 clarifying questions needed

## 🚀 Next Steps

1. Review and approve this plan
2. Set up development environment
3. Begin Phase 1 implementation
4. Iterate based on testing

---

**Estimated Timeline**: 20 working days
**Team Size**: 1-2 developers
**Budget Considerations**: API costs for Tavily, financial data, LLM calls

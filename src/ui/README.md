# Streamlit UI - Multi-Agent Company Research

Professional Streamlit interface for the multi-agent research system.

## 🏗️ Architecture

### Component-Based Design

```
src/ui/
├── app.py                    # Main application logic
├── components/               # Reusable UI components
│   ├── __init__.py
│   ├── agent_monitor.py     # Real-time agent monitoring
│   ├── input_form.py        # Research input form
│   └── report_viewer.py     # Report display and export
├── styles.py                # Custom CSS styles
└── utils.py                 # Utility functions
```

## 🚀 Running the UI

### Quick Start

```bash
streamlit run ui.py
```

### With Custom Port

```bash
streamlit run ui.py --server.port 8501
```

### With Auto-Reload

```bash
streamlit run ui.py --server.runOnSave true
```

## 📦 Components

### 1. AgentMonitor

**Purpose**: Real-time monitoring of agent execution

**Features**:
- Progress bars for all 5 agents
- Activity log with timestamps
- Research summary with metrics
- Status updates

**Usage**:
```python
from src.ui.components import AgentMonitor

monitor = AgentMonitor()
monitor.update_status("profile", "Researching...", 50)
monitor.add_log("profile", "Found 10 sources", "success")
monitor.render_progress_bars()
```

### 2. InputForm

**Purpose**: Company research input form

**Features**:
- Company name input
- Report type selection
- Advanced options (queries, results)
- Example companies

**Usage**:
```python
from src.ui.components import InputForm

form = InputForm()
form_data = form.render()

if form_data:
    company = form_data["company"]
    report_type = form_data["report_type"]
```

### 3. ReportViewer

**Purpose**: Display and export research reports

**Features**:
- Executive summary tab
- Full report tab
- Sources tab
- Export to Markdown, Text, JSON

**Usage**:
```python
from src.ui.components import ReportViewer

viewer = ReportViewer()
viewer.render(research_results)
```

## 🎨 Styling

Custom styles are defined in `styles.py` and applied globally.

**Features**:
- Professional color scheme
- Responsive design
- Smooth animations
- Consistent spacing

**Customization**:
```python
# Edit src/ui/styles.py
def apply_custom_styles():
    st.markdown("""
    <style>
    /* Your custom CSS here */
    </style>
    """, unsafe_allow_html=True)
```

## 🔧 Configuration

### Session State Variables

| Variable | Type | Purpose |
|----------|------|---------|
| `research_results` | Dict | Stores research results |
| `research_in_progress` | Bool | Tracks research status |
| `current_company` | Str | Current company being researched |
| `company_name` | Str | Input company name |
| `report_type` | Str | Selected report type |
| `agent_status` | Dict | Agent status tracking |
| `agent_logs` | List | Activity logs |

### Report Types

- `investment_memo` - Investment analysis
- `due_diligence` - Due diligence report
- `sales_account_plan` - Sales planning
- `competitive_intelligence` - Competitive analysis

## 📊 Features

### Real-Time Monitoring

- Live progress bars for each agent
- Activity log with timestamps
- Status updates during research
- Error handling and display

### Report Display

- Tabbed interface (Summary, Report, Sources)
- Markdown rendering
- Syntax highlighting
- Responsive layout

### Export Options

- Markdown (.md)
- Plain text (.txt)
- JSON (.json)
- Custom filename based on company

## 🧪 Testing

### Manual Testing

1. Start the UI: `streamlit run ui.py`
2. Enter a company name
3. Select report type
4. Click "Start Research"
5. Monitor progress
6. View and export report

### Component Testing

```python
# Test individual components
from src.ui.components import AgentMonitor

monitor = AgentMonitor()
monitor.update_status("profile", "Testing", 100)
assert "profile" in monitor.agent_status
```

## 🎯 Best Practices

### Component Design

1. **Single Responsibility** - Each component has one clear purpose
2. **Reusability** - Components can be used in different contexts
3. **State Management** - Use session state for persistence
4. **Error Handling** - Graceful error display

### Code Organization

1. **Separation of Concerns** - UI logic separate from business logic
2. **Type Hints** - All functions have type annotations
3. **Documentation** - Docstrings for all classes and methods
4. **Clean Code** - No redundancy, readable, maintainable

## 🔄 Workflow

```
User Input → Form Submission → Research Start → 
Agent Monitoring → Results Display → Export Options
```

### State Flow

```
1. Initial State (No Results)
   ↓
2. Form Input
   ↓
3. Research In Progress
   ↓
4. Results Available
   ↓
5. New Research (Reset)
```

## 📝 Customization

### Adding New Report Types

```python
# In input_form.py
REPORT_TYPES = {
    "investment_memo": "📈 Investment Memo",
    "your_new_type": "🆕 Your New Type"  # Add here
}
```

### Adding New Metrics

```python
# In agent_monitor.py
def render_summary(self, results):
    # Add new metric
    with col5:
        st.metric("Your Metric", value)
```

### Custom Styling

```python
# In styles.py
def apply_custom_styles():
    st.markdown("""
    <style>
    /* Add your custom CSS */
    .custom-class {
        /* Your styles */
    }
    </style>
    """, unsafe_allow_html=True)
```

## 🐛 Troubleshooting

### UI Not Loading

```bash
# Check Streamlit installation
pip install streamlit

# Verify imports
python -c "from src.ui.app import main"
```

### Components Not Rendering

```bash
# Check component imports
python -c "from src.ui.components import AgentMonitor"
```

### Async Issues

The UI uses `run_async()` utility to handle async operations in Streamlit.

## 📚 Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Component API](components/)
- [Main README](../../README.md)

## ✅ Checklist

- [x] Component-based architecture
- [x] Real-time monitoring
- [x] Professional styling
- [x] Export functionality
- [x] Error handling
- [x] Documentation
- [x] Type hints
- [x] Clean code

---

**UI is production-ready!** 🎉

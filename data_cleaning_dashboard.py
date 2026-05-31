"""
Data Cleaning & Preparation Dashboard
DecodeLabs Industrial Training Kit - Project 1
A professional Streamlit dashboard for end-to-end data cleaning workflows.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import re
from datetime import datetime
from typing import Optional

# ─────────────────────────────────────────────
#  PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Data Cleaning Dashboard | DecodeLabs",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS  – dark-theme, professional look
# ─────────────────────────────────────────────
CUSTOM_CSS = """
<style>
/* ── Global ── */
[data-testid="stAppViewContainer"] { background: #0d1117; color: #e6edf3; }
[data-testid="stSidebar"]          { background: #161b22; border-right: 1px solid #30363d; }
[data-testid="stHeader"]           { background: transparent; }

/* ── Metric cards ── */
div[data-testid="metric-container"] {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 16px 20px;
}
div[data-testid="metric-container"] label { color: #8b949e !important; font-size: .75rem; }
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #58a6ff !important; font-size: 1.9rem; font-weight: 700;
}

/* ── DataFrames ── */
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }
.stDataFrame thead tr th { background: #21262d !important; color: #58a6ff !important; }
.stDataFrame tbody tr:nth-child(even) td { background: #161b22 !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #238636, #2ea043);
    color: white; border: none; border-radius: 8px;
    padding: 8px 20px; font-weight: 600; transition: all .2s;
}
.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(46,160,67,.4); }

/* ── Sidebar nav buttons ── */
.nav-item {
    display: block; width: 100%; padding: 10px 16px; margin: 4px 0;
    background: transparent; border: 1px solid transparent;
    border-radius: 8px; color: #8b949e; cursor: pointer;
    text-align: left; font-size: .9rem; transition: all .2s;
}
.nav-item:hover, .nav-item.active {
    background: #21262d; border-color: #30363d; color: #e6edf3;
}

/* ── Section headers ── */
.section-header {
    font-size: 1.4rem; font-weight: 700; color: #e6edf3;
    border-bottom: 2px solid #238636; padding-bottom: 8px; margin-bottom: 20px;
}
.sub-header { font-size: 1.1rem; font-weight: 600; color: #58a6ff; margin: 12px 0 6px; }

/* ── Status badges ── */
.badge-success {
    background: #0f5132; color: #75b798; border: 1px solid #198754;
    border-radius: 20px; padding: 3px 12px; font-size: .8rem; font-weight: 600;
}
.badge-warning {
    background: #5c3a00; color: #f0c97a; border: 1px solid #d29922;
    border-radius: 20px; padding: 3px 12px; font-size: .8rem; font-weight: 600;
}
.badge-danger {
    background: #5c1a1a; color: #f47068; border: 1px solid #d1242f;
    border-radius: 20px; padding: 3px 12px; font-size: .8rem; font-weight: 600;
}

/* ── Info/tip boxes ── */
.tip-box {
    background: #0d2137; border-left: 4px solid #1f6feb;
    border-radius: 0 8px 8px 0; padding: 12px 16px; margin: 8px 0;
    color: #79c0ff; font-size: .88rem;
}
.warn-box {
    background: #1f1500; border-left: 4px solid #d29922;
    border-radius: 0 8px 8px 0; padding: 12px 16px; margin: 8px 0;
    color: #f0c97a; font-size: .88rem;
}
.success-box {
    background: #0a1f0a; border-left: 4px solid #238636;
    border-radius: 0 8px 8px 0; padding: 12px 16px; margin: 8px 0;
    color: #3fb950; font-size: .88rem;
}

/* ── Divider ── */
.custom-divider { border: none; border-top: 1px solid #30363d; margin: 20px 0; }

/* ── Change-log table ── */
.change-log {
    border-collapse: collapse; width: 100%; font-size: .85rem;
}
.change-log th {
    background: #21262d; color: #58a6ff; padding: 10px 14px;
    text-align: left; border-bottom: 2px solid #30363d;
}
.change-log td { padding: 8px 14px; border-bottom: 1px solid #21262d; color: #e6edf3; }
.change-log tr:nth-child(even) td { background: #0d1117; }

/* ── Upload area ── */
[data-testid="stFileUploader"] { border-radius: 12px; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SESSION STATE INITIALISATION
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "df_raw": None,        # original uploaded dataframe
        "df_clean": None,      # working copy
        "change_log": [],      # list of dicts: {id, description, impact, status}
        "change_counter": 0,   # auto-incrementing CR id
        "page": "📊 Overview",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─────────────────────────────────────────────
#  HELPER UTILITIES
# ─────────────────────────────────────────────

def next_cr_id() -> str:
    st.session_state["change_counter"] += 1
    return f"CR{st.session_state['change_counter']:03d}"

def log_change(description: str, impact: str, status: str = "Resolved"):
    """Append an entry to the audit change-log."""
    st.session_state["change_log"].append({
        "Change ID": next_cr_id(),
        "Description": description,
        "Impact": impact,
        "Status": status,
    })

def get_df() -> Optional[pd.DataFrame]:
    return st.session_state["df_clean"]

def set_df(df: pd.DataFrame):
    st.session_state["df_clean"] = df.copy()

def plotly_defaults(fig):
    """Apply consistent dark-theme styling to any Plotly figure."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#161b22",
        font=dict(color="#e6edf3", family="Inter, sans-serif"),
        margin=dict(t=40, b=30, l=40, r=20),
        xaxis=dict(gridcolor="#21262d", linecolor="#30363d"),
        yaxis=dict(gridcolor="#21262d", linecolor="#30363d"),
        hoverlabel=dict(bgcolor="#21262d", font_color="#e6edf3"),
    )
    return fig

def detect_date_columns(df: pd.DataFrame) -> list[str]:
    """Heuristically identify columns that look like dates."""
    date_cols = []
    date_patterns = [
        r"\d{4}-\d{2}-\d{2}",
        r"\d{2}/\d{2}/\d{4}",
        r"\d{2}-\d{2}-\d{4}",
        r"\d{4}/\d{2}/\d{2}",
        r"\d{1,2} \w+ \d{4}",
    ]
    for col in df.select_dtypes(include="object").columns:
        sample = df[col].dropna().astype(str).head(20)
        for pattern in date_patterns:
            if sample.str.match(pattern).sum() >= min(3, len(sample)):
                date_cols.append(col)
                break
    return date_cols

def to_excel_bytes(df: pd.DataFrame) -> bytes:
    """Serialise dataframe to .xlsx bytes for download."""
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Cleaned_Data")
    return buf.getvalue()

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style='text-align:center; padding: 20px 0 10px;'>
            <div style='font-size:2.5rem'>🧹</div>
            <div style='font-size:1.1rem; font-weight:700; color:#e6edf3'>Data Cleaning</div>
            <div style='font-size:.75rem; color:#8b949e; margin-top:2px'>DecodeLabs • Project 1</div>
        </div>
        <hr style='border-color:#30363d; margin:10px 0 16px;'>
        """, unsafe_allow_html=True)

        pages = [
            ("📊", "Overview"),
            ("❓", "Missing Values"),
            ("🔁", "Duplicates"),
            ("✏️", "Clean Data"),
            ("✅", "Validation"),
            ("📋", "Change Log"),
        ]

        for icon, label in pages:
            key = f"{icon} {label}"
            active = "background:#21262d; border-color:#30363d; color:#e6edf3;" if st.session_state["page"] == key else ""
            if st.button(f"{icon}  {label}", key=f"nav_{label}", use_container_width=True):
                st.session_state["page"] = key
                st.rerun()

        st.markdown("<hr style='border-color:#30363d; margin:16px 0;'>", unsafe_allow_html=True)

        # ── File uploader in sidebar ──
        st.markdown("<div style='color:#8b949e; font-size:.8rem; font-weight:600; text-transform:uppercase; letter-spacing:.05em'>Upload Dataset</div>", unsafe_allow_html=True)
        uploaded = st.file_uploader("", type=["xlsx", "xls", "csv"], label_visibility="collapsed")

        if uploaded:
            try:
                if uploaded.name.endswith(".csv"):
                    df = pd.read_csv(uploaded)
                else:
                    df = pd.read_excel(uploaded, engine="openpyxl")

                st.session_state["df_raw"] = df.copy()
                st.session_state["df_clean"] = df.copy()
                st.session_state["change_log"] = []
                st.session_state["change_counter"] = 0
                st.success(f"✓ Loaded {len(df):,} rows × {len(df.columns)} cols")
            except Exception as e:
                st.error(f"Error reading file: {e}")

        # ── Download button ──
        if get_df() is not None:
            st.markdown("<hr style='border-color:#30363d; margin:12px 0;'>", unsafe_allow_html=True)
            st.download_button(
                label="⬇️  Download Cleaned Data",
                data=to_excel_bytes(get_df()),
                file_name=f"cleaned_dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

# ─────────────────────────────────────────────
#  PAGES
# ─────────────────────────────────────────────

# ── 1. OVERVIEW ──────────────────────────────
def page_overview():
    st.markdown('<div class="section-header">📊 Dataset Overview</div>', unsafe_allow_html=True)
    df = get_df()
    df_raw = st.session_state["df_raw"]

    if df is None:
        st.markdown("""
        <div style='text-align:center; padding:60px 20px; color:#8b949e;'>
            <div style='font-size:4rem'>📂</div>
            <div style='font-size:1.2rem; margin-top:12px'>Upload a dataset from the sidebar to begin</div>
            <div style='font-size:.85rem; margin-top:6px'>Supports .xlsx, .xls, .csv</div>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── KPI Metrics ──
    total_missing = int(df.isnull().sum().sum())
    dup_count = int(df.duplicated().sum())

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Rows", f"{len(df):,}")
    c2.metric("Total Columns", f"{len(df.columns):,}")
    c3.metric("Missing Values", f"{total_missing:,}",
              delta=f"{total_missing/df.size*100:.1f}% of data",
              delta_color="inverse")
    c4.metric("Duplicate Rows", f"{dup_count:,}",
              delta=f"{dup_count/len(df)*100:.1f}% of rows",
              delta_color="inverse")

    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)

    # ── Data Types summary ──
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown('<div class="sub-header">Column Summary</div>', unsafe_allow_html=True)
        col_info = pd.DataFrame({
            "Column": df.columns,
            "Dtype": [str(df[c].dtype) for c in df.columns],
            "Non-Null": [int(df[c].notna().sum()) for c in df.columns],
            "Null": [int(df[c].isnull().sum()) for c in df.columns],
            "Unique": [int(df[c].nunique()) for c in df.columns],
        })
        st.dataframe(col_info, use_container_width=True, height=300)

    with col_right:
        st.markdown('<div class="sub-header">Data Type Distribution</div>', unsafe_allow_html=True)
        dtype_counts = df.dtypes.astype(str).value_counts().reset_index()
        dtype_counts.columns = ["dtype", "count"]
        fig = px.pie(
            dtype_counts, values="count", names="dtype",
            color_discrete_sequence=["#58a6ff", "#3fb950", "#f0c97a", "#ff7b72"],
            hole=0.45,
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        fig = plotly_defaults(fig)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="sub-header">Data Preview (first 50 rows)</div>', unsafe_allow_html=True)
    st.dataframe(df.head(50), use_container_width=True, height=350)


# ── 2. MISSING VALUES ────────────────────────
def page_missing():
    st.markdown('<div class="section-header">❓ Missing Value Analysis</div>', unsafe_allow_html=True)
    df = get_df()
    if df is None:
        st.warning("Please upload a dataset first.")
        return

    missing_series = df.isnull().sum()
    missing_df = pd.DataFrame({
        "Column": missing_series.index,
        "Missing Count": missing_series.values,
        "Missing %": (missing_series.values / len(df) * 100).round(2),
        "Dtype": [str(df[c].dtype) for c in missing_series.index],
    }).sort_values("Missing Count", ascending=False)

    total_missing = int(missing_df["Missing Count"].sum())

    # ── Summary metrics ──
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Missing Cells", f"{total_missing:,}")
    c2.metric("Columns with Missing", f"{int((missing_df['Missing Count'] > 0).sum())}")
    c3.metric("Overall Missing Rate", f"{total_missing / df.size * 100:.2f}%")

    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)

    col_l, col_r = st.columns([1.2, 1])

    with col_l:
        st.markdown('<div class="sub-header">Missing Values by Column</div>', unsafe_allow_html=True)
        df_show = missing_df[missing_df["Missing Count"] > 0]
        if df_show.empty:
            st.markdown('<div class="success-box">✅ No missing values detected in this dataset!</div>', unsafe_allow_html=True)
        else:
            st.dataframe(df_show.reset_index(drop=True), use_container_width=True)

    with col_r:
        st.markdown('<div class="sub-header">Completeness Rate (%)</div>', unsafe_allow_html=True)
        completeness = ((1 - missing_series / len(df)) * 100).sort_values()
        fig = px.bar(
            x=completeness.values, y=completeness.index,
            orientation="h",
            color=completeness.values,
            color_continuous_scale=[[0, "#d1242f"], [0.5, "#d29922"], [1, "#3fb950"]],
            labels={"x": "Completeness (%)", "y": ""},
            range_x=[0, 105],
        )
        fig.update_coloraxes(showscale=False)
        fig = plotly_defaults(fig)
        st.plotly_chart(fig, use_container_width=True)

    # ── Heatmap ──
    st.markdown('<div class="sub-header">Missing Value Heatmap</div>', unsafe_allow_html=True)
    sample_size = min(200, len(df))
    df_sample = df.head(sample_size).isnull().astype(int)

    fig2 = go.Figure(data=go.Heatmap(
        z=df_sample.T.values,
        x=[f"Row {i}" for i in range(sample_size)],
        y=df_sample.columns.tolist(),
        colorscale=[[0, "#161b22"], [1, "#d1242f"]],
        showscale=False,
        hoverongaps=False,
    ))
    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#161b22",
        font=dict(color="#e6edf3"), height=max(200, len(df.columns) * 25),
        margin=dict(t=20, b=40, l=100, r=20),
        xaxis=dict(visible=False), yaxis=dict(tickfont=dict(size=10)),
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("🔴 Red = missing value  |  Dark = present  |  Showing first 200 rows")


# ── 3. DUPLICATES ────────────────────────────
def page_duplicates():
    st.markdown('<div class="section-header">🔁 Duplicate Analysis</div>', unsafe_allow_html=True)
    df = get_df()
    if df is None:
        st.warning("Please upload a dataset first.")
        return

    dup_mask = df.duplicated(keep="first")
    dup_count = int(dup_mask.sum())
    unique_count = len(df) - dup_count

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Rows", f"{len(df):,}")
    c2.metric("Duplicate Rows", f"{dup_count:,}", delta=f"{dup_count/len(df)*100:.2f}%", delta_color="inverse")
    c3.metric("Unique Rows", f"{unique_count:,}")

    # ── Before / After donut ──
    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown('<div class="sub-header">Composition Before Cleaning</div>', unsafe_allow_html=True)
        fig = px.pie(
            values=[unique_count, dup_count],
            names=["Unique", "Duplicate"],
            color_discrete_sequence=["#3fb950", "#d1242f"],
            hole=0.5,
        )
        fig.update_traces(textinfo="percent+label")
        fig = plotly_defaults(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        if dup_count > 0:
            st.markdown('<div class="sub-header">Duplicate Rows Preview</div>', unsafe_allow_html=True)
            st.dataframe(df[dup_mask].head(20), use_container_width=True, height=250)
        else:
            st.markdown('<div class="success-box" style="margin-top:60px">✅ No duplicate rows found.</div>', unsafe_allow_html=True)

    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)

    if dup_count > 0:
        st.markdown('<div class="tip-box">💡 <b>Tip:</b> Removing duplicates eliminates inflated counts and skewed statistics. Only the first occurrence of each duplicate is kept.</div>', unsafe_allow_html=True)
        if st.button("🗑️  Remove All Duplicate Rows", type="primary"):
            df_dedup = df.drop_duplicates(keep="first").reset_index(drop=True)
            removed = len(df) - len(df_dedup)
            set_df(df_dedup)
            log_change(
                "Removed duplicate rows (keep='first')",
                f"Removed {removed:,} duplicate rows → {len(df_dedup):,} unique rows remain"
            )
            st.success(f"✅ Removed {removed:,} duplicate rows. Dataset now has {len(df_dedup):,} rows.")
            st.rerun()
    else:
        st.markdown('<div class="success-box">✅ Dataset is free of duplicates.</div>', unsafe_allow_html=True)


# ── 4. CLEAN DATA ────────────────────────────
def page_clean():
    st.markdown('<div class="section-header">✏️ Data Cleaning Operations</div>', unsafe_allow_html=True)
    df = get_df()
    if df is None:
        st.warning("Please upload a dataset first.")
        return

    # ═══════════════════════════════
    # SECTION A: Fill Missing Values
    # ═══════════════════════════════
    st.markdown('<div class="sub-header">A. Handle Missing Values</div>', unsafe_allow_html=True)
    st.markdown('<div class="tip-box">💡 Strategic imputation preserves your sample size. Listwise deletion reduces statistical power.</div>', unsafe_allow_html=True)

    missing_cols = [c for c in df.columns if df[c].isnull().any()]
    if not missing_cols:
        st.markdown('<div class="success-box">✅ No missing values to fill.</div>', unsafe_allow_html=True)
    else:
        c1, c2, c3 = st.columns([2, 1.5, 1])
        with c1:
            selected_col = st.selectbox("Select column", missing_cols, key="fill_col")
        with c2:
            fill_strategy = st.selectbox(
                "Fill strategy",
                ["Mean", "Median", "Mode", "Forward Fill", "Backward Fill", "Custom Value"],
                key="fill_strat",
            )
        with c3:
            custom_val = st.text_input("Custom value", key="fill_custom",
                                       disabled=(fill_strategy != "Custom Value"))

        col_dtype = df[selected_col].dtype
        null_count = int(df[selected_col].isnull().sum())
        st.caption(f"Column **{selected_col}** → dtype: `{col_dtype}` | missing: **{null_count}** cells")

        if st.button("✔  Apply Fill", key="btn_fill"):
            df_new = get_df().copy()
            col = selected_col
            strat = fill_strategy
            try:
                if strat == "Mean":
                    val = df_new[col].mean()
                    df_new[col] = df_new[col].fillna(val)
                    desc = f"Filled '{col}' missing values using Mean ({val:.4g})"
                elif strat == "Median":
                    val = df_new[col].median()
                    df_new[col] = df_new[col].fillna(val)
                    desc = f"Filled '{col}' missing values using Median ({val:.4g})"
                elif strat == "Mode":
                    val = df_new[col].mode()[0]
                    df_new[col] = df_new[col].fillna(val)
                    desc = f"Filled '{col}' missing values using Mode ('{val}')"
                elif strat == "Forward Fill":
                    df_new[col] = df_new[col].ffill()
                    desc = f"Filled '{col}' using Forward Fill"
                elif strat == "Backward Fill":
                    df_new[col] = df_new[col].bfill()
                    desc = f"Filled '{col}' using Backward Fill"
                else:
                    cast_val = pd.to_numeric(custom_val, errors="ignore") if col_dtype != object else custom_val
                    df_new[col] = df_new[col].fillna(cast_val)
                    desc = f"Filled '{col}' with custom value '{custom_val}'"
                set_df(df_new)
                log_change(desc, f"Filled {null_count} null cells in '{col}'")
                st.success(f"✅ {desc}")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)

    # ═══════════════════════════════════
    # SECTION B: Text Standardisation
    # ═══════════════════════════════════
    st.markdown('<div class="sub-header">B. Standardise Text Formatting</div>', unsafe_allow_html=True)
    text_cols = df.select_dtypes(include="object").columns.tolist()
    if not text_cols:
        st.markdown('<div class="warn-box">No text columns found.</div>', unsafe_allow_html=True)
    else:
        c1, c2 = st.columns([2, 2])
        with c1:
            txt_col = st.selectbox("Select text column", text_cols, key="txt_col")
        with c2:
            txt_ops = st.multiselect(
                "Operations",
                ["Strip whitespace", "Title Case", "UPPER CASE", "lower case",
                 "Remove special characters", "Remove extra spaces"],
                default=["Strip whitespace"],
                key="txt_ops",
            )
        if st.button("✔  Apply Text Cleaning", key="btn_text"):
            df_new = get_df().copy()
            col = txt_col
            applied = []
            for op in txt_ops:
                if op == "Strip whitespace":
                    df_new[col] = df_new[col].astype(str).str.strip()
                    applied.append("strip")
                elif op == "Title Case":
                    df_new[col] = df_new[col].astype(str).str.title()
                    applied.append("title case")
                elif op == "UPPER CASE":
                    df_new[col] = df_new[col].astype(str).str.upper()
                    applied.append("upper case")
                elif op == "lower case":
                    df_new[col] = df_new[col].astype(str).str.lower()
                    applied.append("lower case")
                elif op == "Remove special characters":
                    df_new[col] = df_new[col].astype(str).str.replace(r"[^a-zA-Z0-9 _\-]", "", regex=True)
                    applied.append("removed special chars")
                elif op == "Remove extra spaces":
                    df_new[col] = df_new[col].astype(str).str.replace(r"\s+", " ", regex=True).str.strip()
                    applied.append("removed extra spaces")
            set_df(df_new)
            desc = f"Text cleaning on '{col}': {', '.join(applied)}"
            log_change(desc, f"Standardised text in column '{col}'")
            st.success(f"✅ {desc}")
            st.rerun()

    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)

    # ═══════════════════════════════════
    # SECTION C: Date Standardisation
    # ═══════════════════════════════════
    st.markdown('<div class="sub-header">C. Standardise Date Formats → YYYY-MM-DD</div>', unsafe_allow_html=True)
    st.markdown('<div class="tip-box">💡 ISO 8601 standard (YYYY-MM-DD) ensures consistent parsing across all analytics tools.</div>', unsafe_allow_html=True)

    auto_date_cols = detect_date_columns(df)
    all_str_cols = df.select_dtypes(include=["object", "datetime"]).columns.tolist()
    date_col_options = list(set(auto_date_cols + all_str_cols))

    if not date_col_options:
        st.markdown('<div class="warn-box">No candidate date columns detected.</div>', unsafe_allow_html=True)
    else:
        c1, c2 = st.columns([2, 2])
        with c1:
            date_col = st.selectbox("Select date column", date_col_options, key="date_col",
                                    index=0 if auto_date_cols else 0)
        with c2:
            st.markdown("<br>", unsafe_allow_html=True)
            if auto_date_cols:
                st.markdown(f'<div class="badge-success">🔍 Auto-detected: {", ".join(auto_date_cols[:3])}</div>', unsafe_allow_html=True)

        if st.button("✔  Convert Dates to YYYY-MM-DD", key="btn_date"):
            df_new = get_df().copy()
            col = date_col
            before_bad = 0
            try:
                parsed = pd.to_datetime(df_new[col], infer_datetime_format=True, errors="coerce")
                before_bad = int(parsed.isnull().sum()) - int(df_new[col].isnull().sum())
                df_new[col] = parsed.dt.strftime("%Y-%m-%d")
                set_df(df_new)
                log_change(
                    f"Converted '{col}' to ISO 8601 date format (YYYY-MM-DD)",
                    f"Standardised date format; {before_bad} unparseable values set to NaT"
                )
                st.success(f"✅ '{col}' converted to YYYY-MM-DD format.")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)

    # ═══════════════════════════════════
    # SECTION D: Datatype Conversion
    # ═══════════════════════════════════
    st.markdown('<div class="sub-header">D. Fix Incorrect Data Types</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        dtype_col = st.selectbox("Select column", df.columns.tolist(), key="dtype_col")
    with c2:
        target_type = st.selectbox(
            "Convert to",
            ["int64", "float64", "str / object", "datetime64", "bool"],
            key="dtype_target",
        )
    with c3:
        st.markdown("<br>", unsafe_allow_html=True)
        current_badge = f'<span class="badge-warning">Current: {df[dtype_col].dtype}</span>'
        st.markdown(current_badge, unsafe_allow_html=True)

    if st.button("✔  Apply Type Conversion", key="btn_dtype"):
        df_new = get_df().copy()
        col = dtype_col
        try:
            before_type = str(df_new[col].dtype)
            if target_type == "int64":
                df_new[col] = pd.to_numeric(df_new[col], errors="coerce").astype("Int64")
            elif target_type == "float64":
                df_new[col] = pd.to_numeric(df_new[col], errors="coerce")
            elif target_type == "str / object":
                df_new[col] = df_new[col].astype(str)
            elif target_type == "datetime64":
                df_new[col] = pd.to_datetime(df_new[col], errors="coerce")
            elif target_type == "bool":
                df_new[col] = df_new[col].astype(bool)
            set_df(df_new)
            log_change(
                f"Type conversion: '{col}' {before_type} → {target_type}",
                f"Column '{col}' dtype changed successfully"
            )
            st.success(f"✅ '{col}' converted from `{before_type}` to `{target_type}`.")
            st.rerun()
        except Exception as e:
            st.error(f"Conversion error: {e}")

    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)

    # ═══════════════════════════════════
    # SECTION E: Remove Rows by Condition
    # ═══════════════════════════════════
    st.markdown('<div class="sub-header">E. Drop Rows with Remaining Nulls</div>', unsafe_allow_html=True)
    remaining_null_cols = [c for c in df.columns if df[c].isnull().any()]
    if remaining_null_cols:
        c1, c2 = st.columns([3, 1])
        with c1:
            drop_col = st.selectbox("Drop rows where this column is null", remaining_null_cols, key="drop_col")
        with c2:
            st.markdown("<br>", unsafe_allow_html=True)
            affected = int(df[drop_col].isnull().sum())
            st.markdown(f'<span class="badge-danger">Affects {affected} rows</span>', unsafe_allow_html=True)
        if st.button("🗑️  Drop Null Rows", key="btn_dropnull"):
            df_new = get_df().copy()
            before_len = len(df_new)
            df_new = df_new.dropna(subset=[drop_col]).reset_index(drop=True)
            removed = before_len - len(df_new)
            set_df(df_new)
            log_change(
                f"Dropped rows where '{drop_col}' is null",
                f"Removed {removed} rows → {len(df_new)} rows remain"
            )
            st.success(f"✅ Dropped {removed} rows. {len(df_new)} rows remain.")
            st.rerun()
    else:
        st.markdown('<div class="success-box">✅ No null values remain in the dataset.</div>', unsafe_allow_html=True)


# ── 5. VALIDATION ────────────────────────────
def page_validation():
    st.markdown('<div class="section-header">✅ Validation & Quality Report</div>', unsafe_allow_html=True)
    df = get_df()
    df_raw = st.session_state["df_raw"]
    if df is None:
        st.warning("Please upload a dataset first.")
        return

    # ─ Compute all validation checks ─
    dup_ids = 0
    id_col_found = None
    for col in df.columns:
        name_lc = col.lower()
        if any(x in name_lc for x in ["id", "_id", "order", "invoice", "transaction"]):
            if df[col].nunique() == len(df[col].dropna()):
                id_col_found = col
                break
            else:
                id_col_found = col
                dup_ids = int(df[col].duplicated().sum())
                break

    # Date format check
    date_issues = 0
    date_col_checked = None
    for col in df.select_dtypes(include="object").columns:
        sample = df[col].dropna().astype(str).head(50)
        iso_pattern = r"^\d{4}-\d{2}-\d{2}$"
        non_iso = sample[~sample.str.match(iso_pattern)]
        date_pattern_any = r"\d{1,4}[-/]\d{1,2}[-/]\d{1,4}"
        if sample.str.match(date_pattern_any).sum() > 3:
            date_col_checked = col
            date_issues = int(non_iso.str.match(date_pattern_any).sum())
            break

    missing_total = int(df.isnull().sum().sum())
    dup_rows = int(df.duplicated().sum())
    rows_removed = len(df_raw) - len(df)
    missing_raw = int(df_raw.isnull().sum().sum())
    missing_fixed = missing_raw - missing_total

    # ─ Gate checks ─
    gate_dup_id = dup_ids == 0
    gate_date_fmt = date_issues == 0

    st.markdown('<div class="sub-header">🏁 Verification Gate – Project 2 Threshold</div>', unsafe_allow_html=True)

    gcol1, gcol2 = st.columns(2)
    with gcol1:
        status = "✅ PASSED" if gate_dup_id else "❌ FAILED"
        color = "#3fb950" if gate_dup_id else "#d1242f"
        bg = "#0a1f0a" if gate_dup_id else "#1a0000"
        id_label = id_col_found if id_col_found else "No ID col detected"
        st.markdown(f"""
        <div style='background:{bg}; border:2px solid {color}; border-radius:12px; padding:20px; text-align:center;'>
            <div style='font-size:2rem'>{status}</div>
            <div style='color:{color}; font-weight:700; margin-top:6px'>Unique Identifiers</div>
            <div style='color:#8b949e; font-size:.85rem; margin-top:4px'>Duplicate IDs: <b style='color:{color}'>{dup_ids}</b> ({id_label})</div>
            <div style='color:#8b949e; font-size:.8rem; margin-top:2px'>Threshold: 0% Error Rate</div>
        </div>
        """, unsafe_allow_html=True)

    with gcol2:
        status2 = "✅ PASSED" if gate_date_fmt else "⚠️ REVIEW"
        color2 = "#3fb950" if gate_date_fmt else "#d29922"
        bg2 = "#0a1f0a" if gate_date_fmt else "#1f1500"
        col_label = date_col_checked if date_col_checked else "No date col detected"
        st.markdown(f"""
        <div style='background:{bg2}; border:2px solid {color2}; border-radius:12px; padding:20px; text-align:center;'>
            <div style='font-size:2rem'>{status2}</div>
            <div style='color:{color2}; font-weight:700; margin-top:6px'>Date Format Compliance</div>
            <div style='color:#8b949e; font-size:.85rem; margin-top:4px'>Non-ISO dates: <b style='color:{color2}'>{date_issues}</b> ({col_label})</div>
            <div style='color:#8b949e; font-size:.8rem; margin-top:2px'>Threshold: 0% Error Rate</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)

    # ─ Before / After Comparison ─
    st.markdown('<div class="sub-header">Before vs After Comparison</div>', unsafe_allow_html=True)
    metrics = ["Total Rows", "Missing Values", "Duplicate Rows", "Missing Rate (%)"]
    raw_vals = [
        len(df_raw),
        missing_raw,
        int(df_raw.duplicated().sum()),
        round(missing_raw / df_raw.size * 100, 2),
    ]
    clean_vals = [
        len(df),
        missing_total,
        dup_rows,
        round(missing_total / df.size * 100, 2) if df.size > 0 else 0,
    ]

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Raw Dataset", x=metrics[:3], y=raw_vals[:3],
                         marker_color="#d1242f", text=raw_vals[:3], textposition="outside"))
    fig.add_trace(go.Bar(name="Cleaned Dataset", x=metrics[:3], y=clean_vals[:3],
                         marker_color="#3fb950", text=clean_vals[:3], textposition="outside"))
    fig.update_layout(barmode="group", legend=dict(orientation="h", y=1.1))
    fig = plotly_defaults(fig)
    st.plotly_chart(fig, use_container_width=True)

    # ─ Quality Score Gauge ─
    issues = missing_total + dup_rows + dup_ids
    max_possible = max(df_raw.size, 1)
    score = max(0, 100 - (issues / max_possible * 100 * 100))
    score = min(100, score)

    st.markdown('<div class="sub-header">Data Quality Score</div>', unsafe_allow_html=True)
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=round(score, 1),
        number={"suffix": "%", "font": {"color": "#e6edf3", "size": 36}},
        delta={"reference": 70, "increasing": {"color": "#3fb950"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#8b949e"},
            "bar": {"color": "#58a6ff"},
            "steps": [
                {"range": [0, 50], "color": "#2d1515"},
                {"range": [50, 75], "color": "#2d2500"},
                {"range": [75, 100], "color": "#0a1f0a"},
            ],
            "threshold": {"line": {"color": "#3fb950", "width": 4}, "value": 90},
            "bgcolor": "transparent",
        },
        title={"text": "Overall Data Quality", "font": {"color": "#8b949e", "size": 14}},
    ))
    fig_gauge.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e6edf3"),
        height=280, margin=dict(t=30, b=10),
    )
    st.plotly_chart(fig_gauge, use_container_width=True)


# ── 6. CHANGE LOG ────────────────────────────
def page_changelog():
    st.markdown('<div class="section-header">📋 Audit Change Log</div>', unsafe_allow_html=True)
    st.markdown('<div class="tip-box">💡 Professional analysts document EVERY transformation. Stakeholders need to know WHAT changed and WHY.</div>', unsafe_allow_html=True)

    log = st.session_state["change_log"]
    if not log:
        st.markdown("""
        <div style='text-align:center; padding:40px; color:#8b949e;'>
            <div style='font-size:3rem'>📝</div>
            <div style='margin-top:8px'>No changes recorded yet. Start cleaning your data!</div>
        </div>
        """, unsafe_allow_html=True)
        return

    df_log = pd.DataFrame(log)

    # Summary counts
    c1, c2 = st.columns(2)
    c1.metric("Total Changes Applied", len(log))
    c2.metric("All Resolved", "✅ Yes" if all(r["Status"] == "Resolved" for r in log) else "⚠️ Pending")

    st.markdown("<br>", unsafe_allow_html=True)
    st.dataframe(df_log, use_container_width=True, height=400)

    # ── Download change log as CSV ──
    csv_bytes = df_log.to_csv(index=False).encode()
    st.download_button(
        "⬇️  Download Change Log (CSV)",
        data=csv_bytes,
        file_name=f"change_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
    )

    # ── Reset option ──
    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)
    st.markdown('<div class="sub-header">⚠️ Reset Dataset</div>', unsafe_allow_html=True)
    st.markdown('<div class="warn-box">This will revert all cleaning operations and restore the original uploaded data.</div>', unsafe_allow_html=True)
    if st.button("🔄  Reset to Original Dataset", type="secondary"):
        st.session_state["df_clean"] = st.session_state["df_raw"].copy()
        st.session_state["change_log"] = []
        st.session_state["change_counter"] = 0
        st.success("✅ Dataset reset to original. All changes discarded.")
        st.rerun()


# ─────────────────────────────────────────────
#  MAIN ROUTER
# ─────────────────────────────────────────────
def main():
    render_sidebar()

    page = st.session_state["page"]

    if page == "📊 Overview":
        page_overview()
    elif page == "❓ Missing Values":
        page_missing()
    elif page == "🔁 Duplicates":
        page_duplicates()
    elif page == "✏️ Clean Data":
        page_clean()
    elif page == "✅ Validation":
        page_validation()
    elif page == "📋 Change Log":
        page_changelog()

    # ── Footer ──
    st.markdown("""
    <div style='text-align:center; color:#30363d; font-size:.75rem; margin-top:40px; padding-bottom:10px;'>
        DecodeLabs • Data Analytics Project 1 • Data Cleaning & Preparation Dashboard
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

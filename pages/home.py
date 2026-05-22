import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from typing import cast
import io
import os

# Page config must be first
st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== SESSION STATE INITIALIZATION ====================
# Initialize session states if they don't exist
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'guest_mode' not in st.session_state:
    st.session_state.guest_mode = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'viz_count' not in st.session_state:
    st.session_state.viz_count = 0
if 'analysis_reports' not in st.session_state:
    st.session_state.analysis_reports = []

# ==================== DEBUG: SHOW SESSION STATE ====================
# Add debug info to understand what's happening
with st.sidebar.expander("🔧 Debug Session", expanded=False):
    st.write("Session State:")
    st.write(f"- logged_in: {st.session_state.logged_in}")
    st.write(f"- username: {st.session_state.username}")
    st.write(f"- guest_mode: {st.session_state.guest_mode}")
    st.write(f"- viz_count: {st.session_state.viz_count}")
    
    if st.button("🔄 Refresh Session"):
        st.rerun()

# ==================== ACCESS CONTROL ====================
# Simple access check - only check if NOT logged in
if not st.session_state.logged_in:
    st.warning("⚠️ Please log in to access this page")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 Go to Login"):
            st.switch_page("pages/login.py")
    with col2:
        if st.button("👤 Continue as Guest"):
            st.session_state.guest_mode = True
            st.session_state.logged_in = True
            st.session_state.username = "Guest User"
            st.session_state.viz_count = 0
            st.rerun()
    st.stop()

# ==================== DETERMINE USER TYPE ====================
# SIMPLIFIED: If username is "Guest User" or guest_mode is True → Guest
if st.session_state.username == "Guest User" or st.session_state.guest_mode:
    is_guest = True
    st.session_state.guest_mode = True  # Ensure it's set
else:
    is_guest = False
    st.session_state.guest_mode = False  # Ensure it's not set

# Show user status in sidebar
st.sidebar.markdown("---")
if is_guest:
    st.sidebar.warning(f"👤 **Guest User**\n({max(0, 3 - st.session_state.viz_count)} visualizations left)")
else:
    st.sidebar.success(f"✅ **{st.session_state.username}**\n(Full Access Member)")

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    .dashboard-header {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .guest-header {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .metric-card {
        background: #1e293b;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #3b82f6;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .user-info {
        background: #0f172a;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #334155;
    }
    
    .insight-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        border-left: 5px solid #FACC15;
    }
    
    .chart-container {
        background: #1e293b;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #334155;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    if is_guest:
        st.markdown(f"""
        <div class='user-info' style='background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);'>
            <h3>👤 Guest User</h3>
            <p>⚠️ Guest Mode Active</p>
            <div style='background: rgba(0,0,0,0.2); padding: 10px; border-radius: 5px; margin: 10px 0;'>
                <small>🎁 3 Free Visualizations</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Show guest visualization counter
        viz_remaining = max(0, 3 - st.session_state.get('viz_count', 0))
        if viz_remaining > 0:
            st.info(f"""
            🎁 **Free Trial Active**
            
            Visualizations remaining: **{viz_remaining}/3**
            """)
        else:
            st.warning("""
            ⚠️ **Free Trial Expired**
            
            You've used all 3 free visualizations.
            """)
        
        st.divider()
        st.warning("""
        ⚠️ **Guest Mode Limitations:**
        • 3 free custom charts
        • Max file size: 10MB
        • Cannot save/export
        • Limited analytics
        """)
    else:
        st.markdown(f"""
        <div class='user-info'>
            <h3>👤 {st.session_state.username}</h3>
            <p>Welcome to your dashboard!</p>
            <div style='background: #10b98120; padding: 10px; border-radius: 5px; margin: 10px 0;'>
                <small>✅ Full Member Access</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Navigation
    st.markdown("### 📊 Navigation")
    if is_guest:
        page_options = ["🏠 Data Overview", "📊 Create Charts"]
    else:
        page_options = ["🏠 Data Overview", "📊 Statistical Analysis", "📈 Trend Analysis", "🔥 Advanced Analytics", "🎨 Chart Creator"]
    
    page = st.radio(
        "Select Analysis Type",
        page_options,
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # Data Upload
    st.markdown("### 📁 Upload Data")
    max_size = 10 if is_guest else 200  # MB
    uploaded_file = st.file_uploader(
        f"Upload CSV or Excel (Max: {max_size}MB)", 
        type=['csv', 'xlsx', 'xls'],
        key="file_uploader_home"
    )
    
    # File size check for guests
    if uploaded_file and is_guest:
        file_size = len(uploaded_file.getvalue()) / (1024 * 1024)  # Convert to MB
        if file_size > 10:
            st.error(f"⚠️ File size ({file_size:.1f}MB) exceeds guest limit (10MB)")
            uploaded_file = None
    
    st.divider()
    
    # Upgrade prompt for guests
    if is_guest:
        with st.expander("🔓 Upgrade to Full Version"):
            st.info("Get unlimited access to all features!")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Sign Up", key="sidebar_signup", use_container_width=True):
                    st.switch_page("pages/signup.py")
            with col2:
                if st.button("Log In", key="sidebar_login", use_container_width=True):
                    st.switch_page("pages/login.py")
    
    if st.button("🚪 Logout", key="sidebar_logout", use_container_width=True):
        for key in ['logged_in', 'username', 'guest_mode']:
            if key in st.session_state:
                if key == 'logged_in' or key == 'guest_mode':
                    st.session_state[key] = False
                else:
                    st.session_state[key] = ""
        st.session_state.viz_count = 0
        st.switch_page("app.py")
    
    st.divider()
    
    # Developer info at bottom
    st.markdown("""
    <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border-radius: 10px;'>
        <div style='color: #FACC15; font-weight: bold; font-size: 1rem; margin-bottom: 8px;'>
            Developed by
        </div>
        <div style='color: #3b82f6; font-weight: bold; font-size: 1.3rem; margin: 8px 0;'>
            Muhammad Zarq Ali
        </div>
        <div style='color: #64748b; font-size: 0.85rem; margin-bottom: 12px;'>
            Data Scientist & Developer
        </div>
        <div>
    </div>
    """, unsafe_allow_html=True)

# ==================== MAIN DASHBOARD CONTENT ====================
# MAIN HEADER
if is_guest:
    viz_remaining = max(0, 3 - st.session_state.get('viz_count', 0))
    st.markdown(f"""
    <div class='guest-header'>
        <h1>📊 Data Analytics Dashboard</h1>
        <p>Welcome, <strong>Guest User</strong>! You have {viz_remaining} free chart visualization(s).</p>
        <div style='background: rgba(255,255,255,0.2); padding: 10px; border-radius: 5px; display: inline-block; margin-top: 10px;'>
            <small>🎁 Guest Mode | <a href='/signup' style='color: white; text-decoration: underline; font-weight: bold;'>Sign up</a> for unlimited access!</small>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class='dashboard-header'>
        <h1>📊 Advanced Data Analytics Dashboard</h1>
        <p>Welcome, <strong>{st.session_state.username}</strong>! Comprehensive analysis powered by AI.</p>
        <div style='background: rgba(255,255,255,0.2); padding: 10px; border-radius: 5px; display: inline-block; margin-top: 10px;'>
            <small>✅ Full Member Access Enabled | 🤖 AI-Powered Insights</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==================== MAIN CONTENT AREA ====================
st.markdown(f"### 📋 Currently viewing: **{page}**")

# Helper function for chart creation
def create_chart_interface(df, is_guest=False):
    """Create chart creation interface based on user type"""
    
    if is_guest:
        # Guest chart interface
        viz_count = st.session_state.get('viz_count', 0)
        
        if viz_count < 3:
            st.info(f"🎁 You have {3 - viz_count} free visualization(s) remaining")
            
            # CHART TYPE SELECTION
            chart_types = {
                "📈 Line Chart": "line",
                "📊 Bar Chart": "bar",
                "📉 Scatter Plot": "scatter",
                "🍩 Pie Chart": "pie",
                "📋 Histogram": "histogram",
                "📦 Box Plot": "box",
                "🎻 Violin Plot": "violin",
                "🔥 Heatmap": "heatmap"
            }
            
            selected_chart_name = st.selectbox(
                "Choose a visualization type:",
                list(chart_types.keys()),
                help="Select the type of chart you want to create"
            )
            
            selected_chart = chart_types[selected_chart_name]
            
            # Get column information
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            all_cols = df.columns.tolist()
            
            # Dynamic configuration based on chart type
            if selected_chart == "line":
                col1, col2 = st.columns(2)
                with col1:
                    x_col = st.selectbox("X-axis", all_cols, key="line_x")
                with col2:
                    y_col = st.selectbox("Y-axis", numeric_cols, key="line_y")
                
                if st.button("📈 Create Line Chart", use_container_width=True):
                    fig = px.line(df, x=x_col, y=y_col, title=f'{y_col} Trend')
                    st.plotly_chart(fig, use_container_width=True)
                    st.session_state.viz_count += 1
                    st.success(f"✅ Chart created! {3 - st.session_state.viz_count} remaining")
            
            elif selected_chart == "bar":
                col1, col2 = st.columns(2)
                with col1:
                    x_col = st.selectbox("Category", categorical_cols if categorical_cols else all_cols, key="bar_x")
                with col2:
                    y_col = st.selectbox("Value", numeric_cols, key="bar_y")
                
                if st.button("📊 Create Bar Chart", use_container_width=True):
                    bar_data = df.groupby(x_col)[y_col].mean().sort_values(ascending=False).head(10)
                    fig = px.bar(x=bar_data.index, y=bar_data.values, 
                               title=f'Average {y_col} by {x_col}')
                    st.plotly_chart(fig, use_container_width=True)
                    st.session_state.viz_count += 1
                    st.success(f"✅ Chart created! {3 - st.session_state.viz_count} remaining")
            
            elif selected_chart == "scatter":
                col1, col2 = st.columns(2)
                with col1:
                    x_col = st.selectbox("X-axis", numeric_cols, key="scatter_x")
                with col2:
                    y_col = st.selectbox("Y-axis", numeric_cols, key="scatter_y")
                
                if st.button("📉 Create Scatter Plot", use_container_width=True):
                    fig = px.scatter(df, x=x_col, y=y_col, title=f'{y_col} vs {x_col}')
                    st.plotly_chart(fig, use_container_width=True)
                    st.session_state.viz_count += 1
                    st.success(f"✅ Chart created! {3 - st.session_state.viz_count} remaining")
            
            elif selected_chart == "pie":
                if categorical_cols:
                    pie_col = st.selectbox("Select Category", categorical_cols, key="pie_col")
                    if st.button("🍩 Create Pie Chart", use_container_width=True):
                        value_counts = df[pie_col].value_counts().head(8)
                        fig = px.pie(values=value_counts.values, names=value_counts.index,
                                   title=f'Distribution of {pie_col}')
                        st.plotly_chart(fig, use_container_width=True)
                        st.session_state.viz_count += 1
                        st.success(f"✅ Chart created! {3 - st.session_state.viz_count} remaining")
                else:
                    st.warning("No categorical columns found for pie chart")
            
            elif selected_chart == "histogram":
                if numeric_cols:
                    hist_col = st.selectbox("Select Column", numeric_cols, key="hist_col")
                    if st.button("📋 Create Histogram", use_container_width=True):
                        fig = px.histogram(df, x=hist_col, title=f'Distribution of {hist_col}')
                        st.plotly_chart(fig, use_container_width=True)
                        st.session_state.viz_count += 1
                        st.success(f"✅ Chart created! {3 - st.session_state.viz_count} remaining")
                else:
                    st.warning("No numeric columns found for histogram")
            
            elif selected_chart == "box":
                if numeric_cols:
                    box_col = st.selectbox("Select Value Column", numeric_cols, key="box_value")
                    if st.button("📦 Create Box Plot", use_container_width=True):
                        fig = px.box(df, y=box_col, title=f'Distribution of {box_col}')
                        st.plotly_chart(fig, use_container_width=True)
                        st.session_state.viz_count += 1
                        st.success(f"✅ Chart created! {3 - st.session_state.viz_count} remaining")
                else:
                    st.warning("No numeric columns found for box plot")
            
            elif selected_chart == "heatmap":
                if len(numeric_cols) >= 2:
                    if st.button("🔥 Create Heatmap", use_container_width=True):
                        corr_matrix = df[numeric_cols].corr()
                        fig = px.imshow(corr_matrix, title='Correlation Heatmap',
                                      color_continuous_scale='RdBu_r', aspect="auto")
                        st.plotly_chart(fig, use_container_width=True)
                        st.session_state.viz_count += 1
                        st.success(f"✅ Chart created! {3 - st.session_state.viz_count} remaining")
                else:
                    st.warning("Need at least 2 numeric columns for heatmap")
            
            # Visualization counter reminder
            st.markdown("---")
            st.info(f"📊 **Remaining Visualizations:** {3 - st.session_state.viz_count}/3")
        
        else:
            # Guest limit reached
            st.warning("⚠️ You've used all 3 free visualizations!")
            st.info("Sign up for unlimited access to all features!")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📝 Sign Up Now", use_container_width=True):
                    st.switch_page("pages/signup.py")
            with col2:
                if st.button("🔐 Log In", use_container_width=True):
                    st.switch_page("pages/login.py")
            
            st.markdown("---")
            st.markdown("""
            ### ✨ Member Benefits:
            • ✅ **Unlimited** visualizations
            • 📊 15+ chart types
            • 📈 Advanced customization
            • 🔥 Real-time updates
            • 💾 Save & export charts
            • 📁 200MB file uploads
            """)
    
    else:
        # Registered user chart interface
        st.markdown("### 🎨 Advanced Chart Creator")
        
        # Advanced chart types for registered users
        advanced_chart_types = {
            "📈 Line Chart": "Advanced line charts with multiple series",
            "📊 Bar Chart": "Stacked, grouped, and horizontal bars",
            "📉 Scatter Plot": "With regression lines and confidence intervals",
            "🍩 Pie & Donut": "Pie, donut, and sunburst charts",
            "📋 Histogram": "With distribution fitting",
            "📦 Box & Violin": "Box plots and violin plots",
            "🔥 Heatmap": "Correlation and matrix heatmaps",
            "📊 Area Chart": "Stacked and percentage area charts",
            "🎯 Bubble Chart": "Size and color encoded bubbles"
        }
        
        selected_chart = st.selectbox(
            "Select chart type:",
            list(advanced_chart_types.keys()),
            help="Choose from advanced visualization types"
        )
        
        # Show description
        st.info(f"**{selected_chart}**: {advanced_chart_types[selected_chart]}")
        
        # Get data info
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        # Common settings for all charts
        with st.expander("⚙️ Chart Settings", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                chart_title = st.text_input("Chart Title", value=f"{selected_chart}")
                color_scale = st.selectbox("Color Scale", ["Viridis", "Plasma", "Inferno", "Magma", "Rainbow"])
            with col2:
                show_grid = st.checkbox("Show Grid", value=True)
                show_legend = st.checkbox("Show Legend", value=True)
        
                # Generate chart based on selection
        if selected_chart == "📈 Line Chart":
            col1, col2 = st.columns(2)
            with col1:
                x_col = st.selectbox("X-axis", df.columns.tolist(), key="adv_line_x")
            with col2:
                y_col = st.selectbox("Y-axis", numeric_cols, key="adv_line_y")
            
            if st.button("🚀 Generate Line Chart", type="primary", use_container_width=True, key="gen_line"):
                fig = px.line(df, x=x_col, y=y_col, title=chart_title)
                st.plotly_chart(fig, use_container_width=True)
                st.success("✅ Advanced line chart generated!")
        
        elif selected_chart == "📊 Bar Chart":
            col1, col2 = st.columns(2)
            with col1:
                x_col = st.selectbox("Category", categorical_cols if categorical_cols else df.columns.tolist(), key="adv_bar_x")
            with col2:
                y_col = st.selectbox("Value", numeric_cols, key="adv_bar_y")
            
            bar_type = st.selectbox("Bar Type", ["Vertical", "Horizontal", "Stacked", "Grouped"], key="bar_type")
            
            if st.button("🚀 Generate Bar Chart", type="primary", use_container_width=True, key="gen_bar"):
                fig = px.bar(df, x=x_col, y=y_col, title=chart_title, 
                           orientation='h' if bar_type == "Horizontal" else 'v')
                st.plotly_chart(fig, use_container_width=True)
                st.success("✅ Advanced bar chart generated!")
        
        elif selected_chart == "📉 Scatter Plot":
            col1, col2, col3 = st.columns(3)
            with col1:
                x_col = st.selectbox("X-axis", numeric_cols, key="adv_scatter_x")
            with col2:
                y_col = st.selectbox("Y-axis", numeric_cols, key="adv_scatter_y")
            with col3:
                if categorical_cols:
                    color_col = st.selectbox("Color by", ["None"] + categorical_cols, key="adv_scatter_color")
                else:
                    color_col = "None"
            
            show_trendline = st.checkbox("Show Trendline", value=True, key="scatter_trend")
            
            if st.button("🚀 Generate Scatter Plot", type="primary", use_container_width=True, key="gen_scatter"):
                if color_col != "None":
                    fig = px.scatter(df, x=x_col, y=y_col, color=color_col, 
                                   title=chart_title, trendline="ols" if show_trendline else None)
                else:
                    fig = px.scatter(df, x=x_col, y=y_col, title=chart_title, 
                                   trendline="ols" if show_trendline else None)
                st.plotly_chart(fig, use_container_width=True)
                st.success("✅ Advanced scatter plot generated!")
        
        elif selected_chart == "🍩 Pie & Donut":
            if categorical_cols:
                col1, col2 = st.columns(2)
                with col1:
                    pie_col = st.selectbox("Select Category", categorical_cols, key="adv_pie_col")
                with col2:
                    chart_type = st.selectbox("Chart Type", ["Pie", "Donut"], key="pie_type")
                
                if st.button("🚀 Generate Pie Chart", type="primary", use_container_width=True, key="gen_pie"):
                    value_counts = df[pie_col].value_counts().head(10)
                    if chart_type == "Donut":
                        fig = px.pie(values=value_counts.values, names=value_counts.index,
                                   title=chart_title, hole=0.4)
                    else:
                        fig = px.pie(values=value_counts.values, names=value_counts.index,
                                   title=chart_title)
                    st.plotly_chart(fig, use_container_width=True)
                    st.success("✅ Pie chart generated!")
            else:
                st.warning("No categorical columns found for pie chart")
        
        elif selected_chart == "📋 Histogram":
            if numeric_cols:
                col1, col2 = st.columns(2)
                with col1:
                    hist_col = st.selectbox("Select Column", numeric_cols, key="adv_hist_col")
                with col2:
                    bins = st.slider("Number of bins", 5, 100, 30, key="adv_hist_bins")
                
                show_distribution = st.checkbox("Show Distribution Curve", value=True, key="hist_dist")
                
                if st.button("🚀 Generate Histogram", type="primary", use_container_width=True, key="gen_hist"):
                    fig = px.histogram(df, x=hist_col, nbins=bins, title=chart_title,
                                     marginal="violin" if show_distribution else None)
                    st.plotly_chart(fig, use_container_width=True)
                    st.success("✅ Histogram generated!")
            else:
                st.warning("No numeric columns found for histogram")
        
        elif selected_chart == "📦 Box & Violin":
            if numeric_cols:
                col1, col2 = st.columns(2)
                with col1:
                    value_col = st.selectbox("Value Column", numeric_cols, key="adv_box_value")
                with col2:
                    if categorical_cols:
                        group_col = st.selectbox("Group by", ["None"] + categorical_cols, key="adv_box_group")
                    else:
                        group_col = "None"
                
                plot_type = st.selectbox("Plot Type", ["Box Plot", "Violin Plot", "Box + Violin"], key="plot_type")
                
                if st.button("🚀 Generate Plot", type="primary", use_container_width=True, key="gen_box"):
                    if plot_type == "Box Plot":
                        if group_col != "None":
                            fig = px.box(df, x=group_col, y=value_col, title=chart_title)
                        else:
                            fig = px.box(df, y=value_col, title=chart_title)
                    elif plot_type == "Violin Plot":
                        if group_col != "None":
                            fig = px.violin(df, x=group_col, y=value_col, title=chart_title, box=True)
                        else:
                            fig = px.violin(df, y=value_col, title=chart_title, box=True)
                    else:  # Box + Violin
                        if group_col != "None":
                            fig = make_subplots(rows=1, cols=2, subplot_titles=('Box Plot', 'Violin Plot'))
                            fig.add_trace(go.Box(x=df[group_col], y=df[value_col], name='Box'), row=1, col=1)
                            fig.add_trace(go.Violin(x=df[group_col], y=df[value_col], name='Violin', box_visible=True), row=1, col=2)
                            fig.update_layout(title=chart_title, showlegend=False)
                        else:
                            fig = make_subplots(rows=1, cols=2, subplot_titles=('Box Plot', 'Violin Plot'))
                            fig.add_trace(go.Box(y=df[value_col], name='Box'), row=1, col=1)
                            fig.add_trace(go.Violin(y=df[value_col], name='Violin', box_visible=True), row=1, col=2)
                            fig.update_layout(title=chart_title, showlegend=False)
                    
                    st.plotly_chart(fig, use_container_width=True)
                    st.success("✅ Plot generated!")
            else:
                st.warning("No numeric columns found for box/violin plot")
        
        elif selected_chart == "🔥 Heatmap":
            if len(numeric_cols) >= 2:
                selected_numeric = st.multiselect(
                    "Select columns for heatmap", 
                    numeric_cols, 
                    default=numeric_cols[:min(8, len(numeric_cols))],
                    key="heatmap_cols"
                )
                
                if len(selected_numeric) >= 2:
                    if st.button("🚀 Generate Heatmap", type="primary", use_container_width=True, key="gen_heatmap"):
                        corr_matrix = df[selected_numeric].corr()
                        fig = px.imshow(corr_matrix, title=chart_title,
                                      color_continuous_scale=color_scale.lower(),
                                      aspect="auto", text_auto=True)
                        st.plotly_chart(fig, use_container_width=True)
                        st.success("✅ Heatmap generated!")
                else:
                    st.warning("Please select at least 2 numeric columns")
            else:
                st.warning("Need at least 2 numeric columns for heatmap")
        
        elif selected_chart == "📊 Area Chart":
            if numeric_cols:
                col1, col2 = st.columns(2)
                with col1:
                    x_col = st.selectbox("X-axis", df.columns.tolist(), key="adv_area_x")
                with col2:
                    y_col = st.selectbox("Y-axis", numeric_cols, key="adv_area_y")
                
                if categorical_cols:
                    stack_col = st.selectbox("Stack by (optional)", ["None"] + categorical_cols, key="area_stack")
                else:
                    stack_col = "None"
                
                if st.button("🚀 Generate Area Chart", type="primary", use_container_width=True, key="gen_area"):
                    if stack_col != "None":
                        fig = px.area(df, x=x_col, y=y_col, color=stack_col, 
                                    title=chart_title, groupnorm='percent' if 'percent' in chart_title.lower() else None)
                    else:
                        fig = px.area(df, x=x_col, y=y_col, title=chart_title)
                    st.plotly_chart(fig, use_container_width=True)
                    st.success("✅ Area chart generated!")
            else:
                st.warning("No numeric columns found for area chart")
        
        elif selected_chart == "🎯 Bubble Chart":
            if len(numeric_cols) >= 3:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    x_col = st.selectbox("X-axis", numeric_cols, key="bubble_x")
                with col2:
                    y_col = st.selectbox("Y-axis", numeric_cols, key="bubble_y")
                with col3:
                    size_col = st.selectbox("Bubble Size", numeric_cols, key="bubble_size")
                with col4:
                    if categorical_cols:
                        color_col = st.selectbox("Bubble Color", ["None"] + categorical_cols, key="bubble_color")
                    else:
                        color_col = "None"
                
                if st.button("🚀 Generate Bubble Chart", type="primary", use_container_width=True, key="gen_bubble"):
                    if color_col != "None":
                        fig = px.scatter(df, x=x_col, y=y_col, size=size_col, color=color_col,
                                       title=chart_title, hover_name=df.index if len(df) < 100 else None)
                    else:
                        fig = px.scatter(df, x=x_col, y=y_col, size=size_col,
                                       title=chart_title, hover_name=df.index if len(df) < 100 else None)
                    st.plotly_chart(fig, use_container_width=True)
                    st.success("✅ Bubble chart generated!")
            else:
                st.warning("Need at least 3 numeric columns for bubble chart")
        # Add more chart types for registered users...

# Check if we have uploaded file or show demo
if uploaded_file:
    try:
        # Load data
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.success(f"✅ File uploaded successfully! Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
        
        # Show data preview
        with st.expander("📊 Data Preview"):
            st.dataframe(df.head(20), use_container_width=True)
        
        # Handle different pages
        if page == "🏠 Data Overview":
            st.subheader("📈 Quick Statistics")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Rows", f"{len(df):,}")
            with col2:
                st.metric("Total Columns", len(df.columns))
            with col3:
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                st.metric("Numeric Columns", len(numeric_cols))
            with col4:
                missing = df.isnull().sum().sum()
                st.metric("Missing Values", f"{missing:,}")
            
            # Show data types
            st.subheader("📊 Data Types Overview")
            type_counts = df.dtypes.value_counts()
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(pd.DataFrame({
                    'Data Type': type_counts.index.astype(str),
                    'Count': type_counts.values
                }), use_container_width=True)
            with col2:
                fig = px.pie(values=type_counts.values, names=type_counts.index.astype(str),
                           title='Data Types Distribution')
                st.plotly_chart(fig, use_container_width=True)
        
        elif page == "📊 Create Charts" and is_guest:
            create_chart_interface(df, is_guest=True)
        
        elif page == "🎨 Chart Creator" and not is_guest:
            create_chart_interface(df, is_guest=False)
        
        elif page == "📊 Statistical Analysis" and not is_guest:
            st.subheader("📊 Statistical Analysis")
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if numeric_cols:
                selected_col = st.selectbox("Select column for analysis", numeric_cols)
                
                # Show statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Mean", f"{df[selected_col].mean():.2f}")
                    st.metric("Median", f"{df[selected_col].median():.2f}")
                with col2:
                    st.metric("Std Dev", f"{df[selected_col].std():.2f}")
                    st.metric("Variance", f"{df[selected_col].var():.2f}")
                with col3:
                    st.metric("Min", f"{df[selected_col].min():.2f}")
                    st.metric("Max", f"{df[selected_col].max():.2f}")
                
                # Distribution plot
                st.subheader("📊 Distribution Analysis")
                fig = px.histogram(df, x=selected_col, title=f'Distribution of {selected_col}',
                                 marginal="box", nbins=30)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No numeric columns found for statistical analysis")
        
        elif page == "📈 Trend Analysis" and not is_guest:
            st.subheader("📈 Trend Analysis")
            # Check for date columns
            date_cols = []
            for col in df.columns:
                try:
                    pd.to_datetime(df[col])
                    date_cols.append(col)
                except:
                    continue
            
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if date_cols and numeric_cols:
                col1, col2 = st.columns(2)
                with col1:
                    date_col = st.selectbox("Select Date Column", date_cols)
                with col2:
                    value_col = st.selectbox("Select Value Column", numeric_cols)
                
                # Convert to datetime
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                # Guard against unexpected None/invalid selection for static type checkers
                if date_col is None:
                    st.warning("Invalid date column selected")
                    df_sorted = df
                else:
                    df_sorted = df.sort_values(by=cast(str, date_col))
                
                # Create time series plot
                fig = px.line(df_sorted, x=date_col, y=value_col, 
                            title=f'{value_col} Trend Over Time')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Need date and numeric columns for trend analysis")
        
        elif page == "🔥 Advanced Analytics" and not is_guest:
            st.subheader("🔥 Advanced Analytics")
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(numeric_cols) >= 2:
                # Correlation heatmap
                st.markdown("#### 🔥 Correlation Analysis")
                corr_matrix = df[numeric_cols].corr()
                fig = px.imshow(corr_matrix, title='Correlation Heatmap',
                              color_continuous_scale='RdBu_r', aspect="auto")
                st.plotly_chart(fig, use_container_width=True)
                
                # Scatter matrix
                st.markdown("#### 📊 Scatter Matrix")
                if len(numeric_cols) <= 6:  # Limit to avoid performance issues
                    fig = px.scatter_matrix(df[numeric_cols[:6]])
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info(f"Showing first 6 of {len(numeric_cols)} numeric columns")
                    fig = px.scatter_matrix(df[numeric_cols[:6]])
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Need at least 2 numeric columns for advanced analytics")
    
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")

else:
    # Show demo content when no file uploaded
    st.info("📝 Upload a CSV or Excel file to start analysis, or explore demo content below.")
    
    # Generate sample data
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
    sample_df = pd.DataFrame({
        'Date': dates,
        'Sales': np.random.randint(1000, 5000, 100),
        'Customers': np.random.randint(50, 200, 100),
        'Revenue': np.random.uniform(10000, 50000, 100),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], 100),
        'Product_Category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Books'], 100)
    })
    
    with st.expander("📋 Demo Data Preview"):
        st.dataframe(sample_df.head(20), use_container_width=True)
    
    # Demo content based on page
    if page == "🏠 Data Overview":
        st.subheader("📊 Demo Dashboard")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Revenue", f"${sample_df['Revenue'].sum():,.0f}")
        with col2:
            st.metric("Avg Daily Sales", f"${sample_df['Sales'].mean():,.0f}")
        with col3:
            st.metric("Total Customers", f"{sample_df['Customers'].sum():,}")
        with col4:
            st.metric("Unique Regions", sample_df['Region'].nunique())
        
        # Sample charts
        st.subheader("📈 Sample Visualizations")
        
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.line(sample_df, x='Date', y='Sales', title='Sales Trend')
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            region_counts = sample_df['Region'].value_counts()
            fig2 = px.pie(values=region_counts.values, names=region_counts.index,
                         title='Region Distribution')
            st.plotly_chart(fig2, use_container_width=True)
    
    elif page == "📊 Create Charts" and is_guest:
        st.warning("📤 Please upload your data file to create charts")
        st.info("Demo mode only shows sample visualizations in Data Overview")
    
    elif page == "🎨 Chart Creator" and not is_guest:
        st.warning("📤 Please upload your data file to use the advanced chart creator")
        st.info("Try uploading your own CSV or Excel file to access all features!")

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; padding: 1rem; background: #0f172a; border-radius: 10px; margin-top: 2rem;">
    <p style="margin-bottom: 10px;">
        <strong style="color: #FACC15;">Developed by Muhammad Zarq Ali</strong> • 
        <span style="color: #94a3b8;">v3.0</span> • 
        <a href="https://linkedin.com/in/engeenior" target="_blank" style="color: #64748b; text-decoration: none;">LinkedIn</a> • 
        <a href="https://github.com/engeenior" target="_blank" style="color: #64748b; text-decoration: none;">GitHub</a> • 
        <a href="tel:+923313267202" style="color: #64748b; text-decoration: none;">Contact</a>
    </p>
    <p style="font-size: 0.9rem; color: #475569;">
        © 2026 Data Analytics Dashboard. All rights reserved.
    </p>
</div>
""", unsafe_allow_html=True)
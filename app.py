import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Bug Life Cycle Analytics",
    page_icon="🐞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main-title {
    font-size: 36px;
    font-weight: bold;
    text-align: center;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: gray;
}

.metric-box {
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    file_path = "Bug_Life_Cycle_Managementreport.csv"

    data = pd.read_csv(file_path)

    # Remove extra spaces from column names
    data.columns = data.columns.str.strip()

    # Convert date columns safely
    date_columns = [
        "Date_Reported",
        "Date_Assigned",
        "Date_Fixed",
        "Date_Retested",
        "Date_Closed"
    ]

    for column in date_columns:

        if column in data.columns:

            data[column] = pd.to_datetime(
                data[column],
                dayfirst=True,
                errors="coerce"
            )

    # Numeric columns
    if "Resolution_Time_Hours" in data.columns:
        data["Resolution_Time_Hours"] = pd.to_numeric(
            data["Resolution_Time_Hours"],
            errors="coerce"
        )

    if "Similarity_Score" in data.columns:
        data["Similarity_Score"] = pd.to_numeric(
            data["Similarity_Score"],
            errors="coerce"
        )

    return data


try:

    df = load_data()

except FileNotFoundError:

    st.error(
        "CSV file not found. Make sure Bug_Life_Cycle_Managementreport.csv "
        "is in the same folder as app.py."
    )

    st.stop()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🐞 Bug Life Cycle Management Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Interactive Bug Analysis | Quality Monitoring | Team Performance'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🔎 Dashboard Filters")

# Status filter
status_options = sorted(
    df["Status"].dropna().unique().tolist()
)

selected_status = st.sidebar.multiselect(
    "Bug Status",
    status_options,
    default=status_options
)

# Priority filter
priority_options = sorted(
    df["Priority"].dropna().unique().tolist()
)

selected_priority = st.sidebar.multiselect(
    "Priority",
    priority_options,
    default=priority_options
)

# Severity filter
severity_options = sorted(
    df["Severity"].dropna().unique().tolist()
)

selected_severity = st.sidebar.multiselect(
    "Severity",
    severity_options,
    default=severity_options
)

# Module filter
module_options = sorted(
    df["Module"].dropna().unique().tolist()
)

selected_modules = st.sidebar.multiselect(
    "Module",
    module_options,
    default=module_options
)

# Sprint filter
sprint_options = sorted(
    df["Sprint"].dropna().unique().tolist()
)

selected_sprints = st.sidebar.multiselect(
    "Sprint",
    sprint_options,
    default=sprint_options
)

# Team filter
team_options = sorted(
    df["Team"].dropna().unique().tolist()
)

selected_teams = st.sidebar.multiselect(
    "Team",
    team_options,
    default=team_options
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df[
    df["Status"].isin(selected_status)
    & df["Priority"].isin(selected_priority)
    & df["Severity"].isin(selected_severity)
    & df["Module"].isin(selected_modules)
    & df["Sprint"].isin(selected_sprints)
    & df["Team"].isin(selected_teams)
].copy()


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_bugs = len(filtered_df)

open_bugs = len(
    filtered_df[
        filtered_df["Status"].str.contains(
            "Open",
            case=False,
            na=False
        )
    ]
)

closed_bugs = len(
    filtered_df[
        filtered_df["Status"].str.contains(
            "Closed",
            case=False,
            na=False
        )
    ]
)

in_progress = len(
    filtered_df[
        filtered_df["Status"].str.contains(
            "Progress",
            case=False,
            na=False
        )
    ]
)

critical_bugs = len(
    filtered_df[
        filtered_df["Severity"].str.contains(
            "Critical",
            case=False,
            na=False
        )
    ]
)

if len(filtered_df) > 0:

    average_resolution = filtered_df[
        "Resolution_Time_Hours"
    ].mean()

else:

    average_resolution = 0


# =========================================================
# KPI CARDS
# =========================================================

st.subheader("📊 Key Performance Indicators")

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric(
    "🐞 Total Bugs",
    total_bugs
)

k2.metric(
    "🔓 Open Bugs",
    open_bugs
)

k3.metric(
    "✅ Closed Bugs",
    closed_bugs
)

k4.metric(
    "🚨 Critical Bugs",
    critical_bugs
)

k5.metric(
    "⏱ Avg Resolution",
    f"{average_resolution:.1f} hrs"
)

st.divider()


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📊 Overview",
        "🔍 Bug Analysis",
        "👥 Team Performance",
        "📈 Trends",
        "📋 Bug Records"
    ]
)


# =========================================================
# TAB 1 - OVERVIEW
# =========================================================

with tab1:

    st.subheader("Bug Overview")

    col1, col2 = st.columns(2)

    # STATUS
    with col1:

        status_data = (
            filtered_df["Status"]
            .value_counts()
            .reset_index()
        )

        status_data.columns = [
            "Status",
            "Count"
        ]

        fig = px.pie(
            status_data,
            names="Status",
            values="Count",
            hole=0.45,
            title="Bug Status Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # PRIORITY
    with col2:

        priority_data = (
            filtered_df["Priority"]
            .value_counts()
            .reset_index()
        )

        priority_data.columns = [
            "Priority",
            "Count"
        ]

        fig = px.bar(
            priority_data,
            x="Priority",
            y="Count",
            text="Count",
            title="Priority-wise Bug Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # SEVERITY
    severity_data = (
        filtered_df["Severity"]
        .value_counts()
        .reset_index()
    )

    severity_data.columns = [
        "Severity",
        "Count"
    ]

    fig = px.bar(
        severity_data,
        x="Severity",
        y="Count",
        color="Severity",
        text="Count",
        title="Severity-wise Bug Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# TAB 2 - BUG ANALYSIS
# =========================================================

with tab2:

    st.subheader("🔍 Detailed Bug Analysis")

    col1, col2 = st.columns(2)

    # MODULE
    with col1:

        module_data = (
            filtered_df["Module"]
            .value_counts()
            .reset_index()
        )

        module_data.columns = [
            "Module",
            "Count"
        ]

        fig = px.bar(
            module_data,
            x="Module",
            y="Count",
            color="Count",
            text="Count",
            title="Module-wise Bug Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # SPRINT
    with col2:

        sprint_data = (
            filtered_df["Sprint"]
            .value_counts()
            .reset_index()
        )

        sprint_data.columns = [
            "Sprint",
            "Count"
        ]

        fig = px.bar(
            sprint_data,
            x="Sprint",
            y="Count",
            color="Count",
            text="Count",
            title="Sprint-wise Bug Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ROOT CAUSE

    st.subheader("🌳 Root Cause Analysis")

    root_data = (
        filtered_df["Root_Cause"]
        .fillna("Unknown")
        .value_counts()
        .reset_index()
    )

    root_data.columns = [
        "Root Cause",
        "Count"
    ]

    fig = px.bar(
        root_data,
        x="Count",
        y="Root Cause",
        orientation="h",
        text="Count",
        title="Bugs by Root Cause"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # RESOLUTION

    st.subheader("🔧 Resolution Analysis")

    resolution_data = (
        filtered_df["Resolution"]
        .fillna("Not Resolved")
        .value_counts()
        .reset_index()
    )

    resolution_data.columns = [
        "Resolution",
        "Count"
    ]

    fig = px.pie(
        resolution_data,
        names="Resolution",
        values="Count",
        title="Resolution Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# TAB 3 - TEAM PERFORMANCE
# =========================================================

with tab3:

    st.subheader("👥 Team Performance")

    team_data = (
        filtered_df
        .groupby("Team")
        .agg(
            Total_Bugs=("Bug_ID", "count"),
            Average_Resolution_Hours=(
                "Resolution_Time_Hours",
                "mean"
            )
        )
        .reset_index()
    )

    team_data["Average_Resolution_Hours"] = (
        team_data["Average_Resolution_Hours"]
        .round(2)
    )

    st.dataframe(
        team_data,
        use_container_width=True
    )

    # Team bugs

    fig = px.bar(
        team_data,
        x="Team",
        y="Total_Bugs",
        color="Average_Resolution_Hours",
        text="Total_Bugs",
        title="Team-wise Bug Count"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Assigned To

    st.subheader("👨‍💻 Bugs by Assigned Engineer")

    assigned_data = (
        filtered_df["Assigned_To"]
        .fillna("Unassigned")
        .value_counts()
        .reset_index()
    )

    assigned_data.columns = [
        "Assigned To",
        "Bug Count"
    ]

    fig = px.bar(
        assigned_data,
        x="Assigned To",
        y="Bug Count",
        color="Bug Count",
        text="Bug Count",
        title="Engineer-wise Bug Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# TAB 4 - TRENDS
# =========================================================

with tab4:

    st.subheader("📈 Bug Trends")

    # Reported bugs over time

    reported = (
        filtered_df
        .dropna(subset=["Date_Reported"])
        .groupby(
            filtered_df.dropna(
                subset=["Date_Reported"]
            )["Date_Reported"].dt.date
        )
        .size()
        .reset_index(name="Bug Count")
    )

    reported.columns = [
        "Date",
        "Bug Count"
    ]

    fig = px.line(
        reported,
        x="Date",
        y="Bug Count",
        markers=True,
        title="Bugs Reported Over Time"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Closed bugs trend

    closed = (
        filtered_df
        .dropna(subset=["Date_Closed"])
        .groupby(
            filtered_df.dropna(
                subset=["Date_Closed"]
            )["Date_Closed"].dt.date
        )
        .size()
        .reset_index(name="Closed Bugs")
    )

    closed.columns = [
        "Date",
        "Closed Bugs"
    ]

    fig = px.line(
        closed,
        x="Date",
        y="Closed Bugs",
        markers=True,
        title="Bugs Closed Over Time"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Resolution time

    st.subheader("⏱ Resolution Time Distribution")

    fig = px.histogram(
        filtered_df,
        x="Resolution_Time_Hours",
        nbins=20,
        title="Resolution Time in Hours"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# TAB 5 - BUG RECORDS
# =========================================================

with tab5:

    st.subheader("📋 Bug Records")

    search = st.text_input(
        "🔎 Search by Bug ID or Bug Title"
    )

    display_df = filtered_df.copy()

    if search:

        search = search.lower()

        display_df = display_df[
            display_df["Bug_ID"]
            .astype(str)
            .str.lower()
            .str.contains(search, na=False)
            |
            display_df["Bug_Title"]
            .astype(str)
            .str.lower()
            .str.contains(search, na=False)
        ]

    columns_to_show = [
        "Bug_ID",
        "Sprint",
        "Release_Version",
        "Module",
        "Feature",
        "Severity",
        "Priority",
        "Status",
        "Lifecycle_Stage",
        "Assigned_To",
        "Team",
        "Resolution",
        "Root_Cause",
        "Resolution_Time_Hours",
        "Date_Reported",
        "Date_Closed"
    ]

    columns_to_show = [
        column
        for column in columns_to_show
        if column in display_df.columns
    ]

    st.dataframe(
        display_df[columns_to_show],
        use_container_width=True,
        height=500
    )

    # Download

    download_data = display_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📥 Download Filtered Bug Report",
        data=download_data,
        file_name="Filtered_Bug_Report.csv",
        mime="text/csv"
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Bug Life Cycle Management Dashboard | "
    "Developed using Python, Pandas, Streamlit and Plotly"
)
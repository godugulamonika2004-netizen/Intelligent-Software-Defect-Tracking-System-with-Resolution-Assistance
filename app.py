import streamlit as st
import pandas as pd
import plotly.express as px
from google import genai

api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)
# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Intelligent Software Defect Tracking System with Resolution Assistance",
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
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    file_path = "Intelligent Software Defect Tracking System with Resolution Assistance.csv"

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

    # Convert numeric columns safely
    numeric_columns = [
        "Resolution_Time_Hours",
        "Similarity_Score"
    ]

    for column in numeric_columns:
        if column in data.columns:
            data[column] = pd.to_numeric(
                data[column],
                errors="coerce"
            )

    return data


# =========================================================
# LOAD CSV
# =========================================================

try:
    df = load_data()

except FileNotFoundError:

    st.error(
        "CSV file not found. Make sure "
        "'Intelligent Software Defect Tracking System with Resolution Assistance.csv' "
        "is in the same folder as app.py."
    )

    st.stop()


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def get_options(data, column):

    if column in data.columns:
        return sorted(
            data[column]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

    return []


def safe_value_counts(data, column):

    if column not in data.columns:
        return pd.DataFrame(
            columns=[column, "Count"]
        )

    result = (
        data[column]
        .fillna("Unknown")
        .value_counts()
        .reset_index()
    )

    result.columns = [
        column,
        "Count"
    ]

    return result


def get_top_item(data, column):

    if column not in data.columns:
        return None

    counts = (
        data[column]
        .fillna("Unknown")
        .value_counts()
    )

    if counts.empty:
        return None

    return counts.index[0], counts.iloc[0]


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="main-title">
    🐞 Intelligent Software Defect Tracking System
    with Resolution Assistance
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    Interactive Bug Analysis | Quality Monitoring | Team Performance | AI Assistance
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.title("🔎 Dashboard Filters")

if st.sidebar.button(
    "🔄 Reset Filters",
    use_container_width=True
):
    st.rerun()


status_options = get_options(df, "Status")
priority_options = get_options(df, "Priority")
severity_options = get_options(df, "Severity")
module_options = get_options(df, "Module")
sprint_options = get_options(df, "Sprint")
team_options = get_options(df, "Team")


selected_status = st.sidebar.multiselect(
    "Bug Status",
    status_options,
    default=status_options
)

selected_priority = st.sidebar.multiselect(
    "Priority",
    priority_options,
    default=priority_options
)

selected_severity = st.sidebar.multiselect(
    "Severity",
    severity_options,
    default=severity_options
)

selected_modules = st.sidebar.multiselect(
    "Module",
    module_options,
    default=module_options
)

selected_sprints = st.sidebar.multiselect(
    "Sprint",
    sprint_options,
    default=sprint_options
)

selected_teams = st.sidebar.multiselect(
    "Team",
    team_options,
    default=team_options
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df.copy()


if "Status" in filtered_df.columns:
    filtered_df = filtered_df[
        filtered_df["Status"].isin(selected_status)
    ]


if "Priority" in filtered_df.columns:
    filtered_df = filtered_df[
        filtered_df["Priority"].isin(selected_priority)
    ]


if "Severity" in filtered_df.columns:
    filtered_df = filtered_df[
        filtered_df["Severity"].isin(selected_severity)
    ]


if "Module" in filtered_df.columns:
    filtered_df = filtered_df[
        filtered_df["Module"].isin(selected_modules)
    ]


if "Sprint" in filtered_df.columns:
    filtered_df = filtered_df[
        filtered_df["Sprint"].isin(selected_sprints)
    ]


if "Team" in filtered_df.columns:
    filtered_df = filtered_df[
        filtered_df["Team"].isin(selected_teams)
    ]


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_bugs = len(filtered_df)


open_bugs = 0

if "Status" in filtered_df.columns:
    open_bugs = len(
        filtered_df[
            filtered_df["Status"]
            .astype(str)
            .str.contains(
                "open",
                case=False,
                na=False
            )
        ]
    )


closed_bugs = 0

if "Status" in filtered_df.columns:
    closed_bugs = len(
        filtered_df[
            filtered_df["Status"]
            .astype(str)
            .str.contains(
                "closed",
                case=False,
                na=False
            )
        ]
    )


critical_bugs = 0

if "Severity" in filtered_df.columns:
    critical_bugs = len(
        filtered_df[
            filtered_df["Severity"]
            .astype(str)
            .str.contains(
                "critical",
                case=False,
                na=False
            )
        ]
    )


average_resolution = 0

if (
    not filtered_df.empty
    and "Resolution_Time_Hours" in filtered_df.columns
):
    average_resolution = (
        filtered_df["Resolution_Time_Hours"].mean()
    )

    if pd.isna(average_resolution):
        average_resolution = 0


closure_rate = 0

if total_bugs > 0:
    closure_rate = (
        closed_bugs / total_bugs
    ) * 100


# =========================================================
# DASHBOARD TABS
# =========================================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    [
        "📊 Overview",
        "🔍 Bug Analysis",
        "👥 Team Performance",
        "📈 Trends",
        "📋 Bug Records",
        "🤖 AI Resolution Assistant",
        "💬 AI Assistant"
    ]
)


# =========================================================
# TAB 1 - OVERVIEW
# =========================================================

with tab1:

    st.header("📊 Dashboard Overview")

    k1, k2, k3, k4, k5, k6 = st.columns(6)

    k1.metric("🐞 Total Bugs", total_bugs)
    k2.metric("🔓 Open Bugs", open_bugs)
    k3.metric("✅ Closed Bugs", closed_bugs)
    k4.metric("🚨 Critical Bugs", critical_bugs)
    k5.metric("⏱ Avg Resolution", f"{average_resolution:.1f} hrs")
    k6.metric("📈 Closure Rate", f"{closure_rate:.1f}%")

    st.divider()

    if filtered_df.empty:

        st.warning(
            "No records are available for the selected filters."
        )

    else:

        col1, col2 = st.columns(2)

        with col1:

            if "Status" in filtered_df.columns:

                status_data = safe_value_counts(
                    filtered_df,
                    "Status"
                )

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

        with col2:

            if "Priority" in filtered_df.columns:

                priority_data = safe_value_counts(
                    filtered_df,
                    "Priority"
                )

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

        if "Severity" in filtered_df.columns:

            severity_data = safe_value_counts(
                filtered_df,
                "Severity"
            )

            fig = px.bar(
                severity_data,
                x="Severity",
                y="Count",
                text="Count",
                title="Severity-wise Bug Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        if "Module" in filtered_df.columns:

            module_data = (
                filtered_df["Module"]
                .value_counts()
                .head(5)
                .reset_index()
            )

            module_data.columns = [
                "Module",
                "Bug Count"
            ]

            fig = px.bar(
                module_data,
                x="Module",
                y="Bug Count",
                text="Bug Count",
                title="Top 5 Modules with Most Bugs"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


# =========================================================
# TAB 2 - BUG ANALYSIS
# =========================================================

with tab2:

    st.header("🔍 Detailed Bug Analysis")

    if not filtered_df.empty:

        col1, col2 = st.columns(2)

        with col1:

            if "Module" in filtered_df.columns:

                module_data = safe_value_counts(
                    filtered_df,
                    "Module"
                )

                fig = px.bar(
                    module_data,
                    x="Module",
                    y="Count",
                    text="Count",
                    title="Module-wise Bug Distribution"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        with col2:

            if "Sprint" in filtered_df.columns:

                sprint_data = safe_value_counts(
                    filtered_df,
                    "Sprint"
                )

                fig = px.bar(
                    sprint_data,
                    x="Sprint",
                    y="Count",
                    text="Count",
                    title="Sprint-wise Bug Distribution"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        if "Root_Cause" in filtered_df.columns:

            root_data = (
                filtered_df["Root_Cause"]
                .fillna("Unknown")
                .value_counts()
                .head(10)
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
                title="Top Root Causes"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        if "Resolution" in filtered_df.columns:

            resolution_data = safe_value_counts(
                filtered_df,
                "Resolution"
            )

            fig = px.pie(
                resolution_data,
                names="Resolution",
                values="Count",
                hole=0.35,
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

    st.header("👥 Team Performance")

    if not filtered_df.empty:

        if (
            "Team" in filtered_df.columns
            and "Bug_ID" in filtered_df.columns
        ):

            aggregation = {
                "Total_Bugs": (
                    "Bug_ID",
                    "count"
                )
            }

            if "Resolution_Time_Hours" in filtered_df.columns:

                aggregation[
                    "Average_Resolution_Time_Hours"
                ] = (
                    "Resolution_Time_Hours",
                    "mean"
                )

            team_data = (
                filtered_df
                .groupby("Team")
                .agg(**aggregation)
                .reset_index()
            )

            if (
                "Average_Resolution_Time_Hours"
                in team_data.columns
            ):

                team_data[
                    "Average_Resolution_Time_Hours"
                ] = (
                    team_data[
                        "Average_Resolution_Time_Hours"
                    ].round(2)
                )

            fig = px.bar(
                team_data,
                x="Team",
                y="Total_Bugs",
                text="Total_Bugs",
                title="Team-wise Bug Count"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        if "Assigned_To" in filtered_df.columns:

            assigned_data = (
                filtered_df["Assigned_To"]
                .fillna("Unassigned")
                .value_counts()
                .head(10)
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
                text="Bug Count",
                title="Top Developers by Assigned Bugs"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


# =========================================================
# TAB 4 - TRENDS
# =========================================================

with tab4:

    st.header("📈 Bug Trends")

    if not filtered_df.empty:

        trend_col1, trend_col2 = st.columns(2)

        with trend_col1:

            if "Date_Reported" in filtered_df.columns:

                reported_df = (
                    filtered_df
                    .dropna(subset=["Date_Reported"])
                    .copy()
                )

                if not reported_df.empty:

                    reported = (
                        reported_df
                        .groupby(
                            reported_df[
                                "Date_Reported"
                            ].dt.date
                        )
                        .size()
                        .reset_index(
                            name="Reported_Bugs"
                        )
                    )

                    reported.columns = [
                        "Date",
                        "Reported_Bugs"
                    ]

                    fig = px.line(
                        reported,
                        x="Date",
                        y="Reported_Bugs",
                        markers=True,
                        title="Bugs Reported Over Time"
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

        with trend_col2:

            if "Date_Closed" in filtered_df.columns:

                closed_df = (
                    filtered_df
                    .dropna(subset=["Date_Closed"])
                    .copy()
                )

                if not closed_df.empty:

                    closed = (
                        closed_df
                        .groupby(
                            closed_df[
                                "Date_Closed"
                            ].dt.date
                        )
                        .size()
                        .reset_index(
                            name="Closed_Bugs"
                        )
                    )

                    closed.columns = [
                        "Date",
                        "Closed_Bugs"
                    ]

                    fig = px.line(
                        closed,
                        x="Date",
                        y="Closed_Bugs",
                        markers=True,
                        title="Bugs Closed Over Time"
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

        if "Resolution_Time_Hours" in filtered_df.columns:

            fig = px.histogram(
                filtered_df,
                x="Resolution_Time_Hours",
                nbins=20,
                title="Resolution Time Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


# =========================================================
# TAB 5 - BUG RECORDS
# =========================================================

with tab5:

    st.header("📋 Bug Records")

    search = st.text_input(
        "🔎 Search by Bug ID or Bug Title"
    )

    display_df = filtered_df.copy()

    if search:

        search_lower = search.lower()

        conditions = pd.Series(
            False,
            index=display_df.index
        )

        if "Bug_ID" in display_df.columns:

            conditions = (
                conditions
                |
                display_df["Bug_ID"]
                .astype(str)
                .str.lower()
                .str.contains(
                    search_lower,
                    na=False
                )
            )

        if "Bug_Title" in display_df.columns:

            conditions = (
                conditions
                |
                display_df["Bug_Title"]
                .astype(str)
                .str.lower()
                .str.contains(
                    search_lower,
                    na=False
                )
            )

        display_df = display_df[
            conditions
        ]

    columns_to_show = [
        "Bug_ID",
        "Bug_Title",
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
        display_df[
            columns_to_show
        ],
        use_container_width=True,
        height=500
    )

    download_data = (
        display_df
        .to_csv(
            index=False
        )
        .encode(
            "utf-8"
        )
    )

    st.download_button(
        label="📥 Download Filtered Bug Report",
        data=download_data,
        file_name="Filtered_Bug_Report.csv",
        mime="text/csv",
        use_container_width=True
    )


# =========================================================
# TAB 6 - AI RESOLUTION ASSISTANT
# =========================================================

with tab6:

    st.header("🤖 AI Resolution Assistant")

    st.write(
        "Enter defect information to receive a possible root cause, "
        "recommended solution, testing recommendation, and priority action."
    )


    def generate_resolution(
        title,
        description,
        module,
        severity,
        priority,
        root_cause
    ):

        combined_text = (
            str(title).lower()
            + " "
            + str(description).lower()
            + " "
            + str(module).lower()
            + " "
            + str(root_cause).lower()
        )

        defect_type = "General Software Defect"

        possible_cause = (
            "The exact root cause requires further investigation."
        )

        recommended_solution = (
            "Reproduce the defect, review relevant logs, identify the "
            "failing component, apply a tested fix, and validate the "
            "solution before deployment."
        )

        testing = (
            "Perform functional testing and regression testing "
            "after applying the fix."
        )

        action = (
            "Assign the defect to the responsible development team "
            "and investigate the issue."
        )


        # LOGIN / AUTHENTICATION
        if any(
            word in combined_text
            for word in [
                "login",
                "authentication",
                "password",
                "sign in",
                "credential",
                "session"
            ]
        ):

            defect_type = "Authentication Defect"

            possible_cause = (
                "The issue may be related to authentication logic, "
                "credential validation, session management, token handling, "
                "or database validation."
            )

            recommended_solution = (
                "Check authentication logic, validate credential handling, "
                "inspect session and token management, and verify database "
                "connectivity."
            )

            testing = (
                "Test valid login, invalid login, password reset, "
                "session timeout, and unauthorized access."
            )

            action = (
                "Review authentication logs and reproduce the failure."
            )


        # DATABASE
        elif any(
            word in combined_text
            for word in [
                "database",
                "sql",
                "query",
                "mysql",
                "postgres",
                "mongodb"
            ]
        ):

            defect_type = "Database Defect"

            possible_cause = (
                "The issue may be caused by an incorrect database query, "
                "connection failure, missing data, or transaction handling."
            )

            recommended_solution = (
                "Verify database connectivity, inspect queries, check "
                "database records, validate transactions, and review "
                "database constraints."
            )

            testing = (
                "Perform database integration testing and verify CRUD operations."
            )

            action = (
                "Check application and database logs."
            )


        # UI / FRONTEND
        elif any(
            word in combined_text
            for word in [
                "button",
                "ui",
                "interface",
                "screen",
                "frontend",
                "form",
                "layout",
                "display"
            ]
        ):

            defect_type = "User Interface Defect"

            possible_cause = (
                "The defect may be related to UI event handling, "
                "frontend validation, component configuration, "
                "CSS issues, or JavaScript errors."
            )

            recommended_solution = (
                "Inspect the affected component, validate event handlers, "
                "check frontend validation, and inspect browser console errors."
            )

            testing = (
                "Test the affected screen across different browsers "
                "and user interaction scenarios."
            )

            action = (
                "Reproduce the UI issue and inspect the browser console."
            )


        # PERFORMANCE
        elif any(
            word in combined_text
            for word in [
                "slow",
                "performance",
                "timeout",
                "delay",
                "lag",
                "response time",
                "loading"
            ]
        ):

            defect_type = "Performance Defect"

            possible_cause = (
                "The issue may be caused by inefficient processing, "
                "slow database queries, high server load, memory usage, "
                "or network latency."
            )

            recommended_solution = (
                "Profile the application, optimize slow queries, reduce "
                "unnecessary processing, and monitor server resources."
            )

            testing = (
                "Perform load testing, stress testing, and response-time testing."
            )

            action = (
                "Measure response time and identify the slowest component."
            )


        # API
        elif any(
            word in combined_text
            for word in [
                "api",
                "endpoint",
                "request",
                "response",
                "rest",
                "http",
                "json"
            ]
        ):

            defect_type = "API Defect"

            possible_cause = (
                "The issue may be related to incorrect endpoints, "
                "request validation, authentication, or response handling."
            )

            recommended_solution = (
                "Verify API endpoints, request parameters, headers, "
                "authentication, and error handling."
            )

            testing = (
                "Test successful requests, invalid requests, authentication "
                "failures, and error responses."
            )

            action = (
                "Inspect API logs and reproduce the request."
            )


        # SECURITY
        elif any(
            word in combined_text
            for word in [
                "security",
                "permission",
                "access",
                "authorization",
                "unauthorized",
                "role"
            ]
        ):

            defect_type = "Security / Access Control Defect"

            possible_cause = (
                "The issue may be caused by incorrect access-control "
                "configuration or authorization logic."
            )

            recommended_solution = (
                "Review authentication, authorization rules, role-based "
                "access control, and permission configuration."
            )

            testing = (
                "Test authorized and unauthorized users across different roles."
            )

            action = (
                "Review security logs and verify user permissions."
            )


        # VALIDATION
        elif any(
            word in combined_text
            for word in [
                "validation",
                "invalid input",
                "required field"
            ]
        ):

            defect_type = "Input Validation Defect"

            possible_cause = (
                "The defect may be caused by missing validation "
                "or incorrect validation rules."
            )

            recommended_solution = (
                "Review validation rules and implement proper client-side "
                "and server-side validation."
            )

            testing = (
                "Perform boundary-value testing and invalid input testing."
            )

            action = (
                "Reproduce the issue using valid and invalid inputs."
            )


        # SEVERITY BASED ACTION
        if severity == "Critical":

            action += (
                " This defect is Critical and requires immediate investigation."
            )

        elif severity == "High":

            action += (
                " This defect should be prioritized before lower-severity bugs."
            )

        elif severity == "Medium":

            action += (
                " Schedule the fix according to the current sprint priority."
            )

        else:

            action += (
                " This defect can be handled according to normal priority."
            )


        return {
            "defect_type": defect_type,
            "possible_cause": possible_cause,
            "recommended_solution": recommended_solution,
            "testing": testing,
            "action": action
        }


    ai_col1, ai_col2 = st.columns(2)

    with ai_col1:

        bug_title = st.text_input(
            "🐞 Bug Title",
            key="bug_title"
        )

        affected_module = st.text_input(
            "📦 Affected Module",
            key="affected_module"
        )

        severity = st.selectbox(
            "🚨 Severity",
            [
                "Low",
                "Medium",
                "High",
                "Critical"
            ],
            key="ai_severity"
        )

    with ai_col2:

        bug_description = st.text_area(
            "📝 Bug Description",
            height=150,
            key="bug_description"
        )

        priority = st.selectbox(
            "⚡ Priority",
            [
                "Low",
                "Medium",
                "High",
                "Critical"
            ],
            key="ai_priority"
        )


    root_cause = st.text_input(
        "🌳 Known Root Cause (Optional)",
        key="root_cause"
    )


    if st.button(
        "🤖 Analyze Defect",
        type="primary",
        use_container_width=True,
        key="analyze_defect"
    ):

        if not bug_title:

            st.warning("Please enter the Bug Title.")

        elif not bug_description:

            st.warning("Please enter the Bug Description.")

        elif not affected_module:

            st.warning("Please enter the Affected Module.")

        else:

            result = generate_resolution(
                bug_title,
                bug_description,
                affected_module,
                severity,
                priority,
                root_cause
            )

            st.success("Defect analysis completed successfully.")

            st.subheader("🤖 Resolution Assistance Result")

            st.markdown(
                f"### 🏷 Identified Defect Type: **{result['defect_type']}**"
            )

            result_col1, result_col2 = st.columns(2)

            with result_col1:

                st.markdown("### 🔍 Possible Root Cause")

                st.info(result["possible_cause"])

                st.markdown("### 🛠 Recommended Resolution")

                st.success(result["recommended_solution"])

            with result_col2:

                st.markdown("### 🧪 Testing Recommendation")

                st.warning(result["testing"])

                st.markdown("### 📌 Recommended Action")

                st.info(result["action"])


# =========================================================
# TAB 7 - AI ASSISTANT
# =========================================================

with tab7:

    st.subheader("🤖 AI Assistant")

    st.write(
        "Ask questions about the project or any general topic such as "
        "Artificial Intelligence, Machine Learning, Python, programming, "
        "science, technology, and more."
    )

    user_question = st.text_input(
        "Ask any question about the project or any general topic:",
        key="ai_question"
    )


    # =====================================================
    # ANSWER PROJECT QUESTIONS DIRECTLY FROM DATASET
    # =====================================================

    def answer_project_question(question, data):

        question = question.lower().strip()


        # TOTAL BUGS
        if any(
            phrase in question
            for phrase in [
                "how many bugs",
                "total bugs",
                "number of bugs",
                "bug count",
                "bugs in project"
            ]
        ):
            return (
                f"🐞 There are **{len(data)} bugs** "
                f"in the project dataset."
            )


        # MODULE WITH HIGHEST BUGS
        if any(
            phrase in question
            for phrase in [
                "which module has highest bugs",
                "which module has the highest bugs",
                "which module has most bugs",
                "module with highest bugs",
                "module with most bugs"
            ]
        ):

            if "Module" in data.columns:

                module_counts = (
                    data["Module"]
                    .fillna("Unknown")
                    .value_counts()
                )

                if not module_counts.empty:

                    module_name = module_counts.index[0]
                    bug_count = module_counts.iloc[0]

                    return (
                        f"📦 The module with the highest number of bugs is "
                        f"**{module_name}**, with **{bug_count} bugs**."
                    )


        # OPEN BUGS
        if "open bug" in question or "open bugs" in question:

            if "Status" in data.columns:

                count = len(
                    data[
                        data["Status"]
                        .astype(str)
                        .str.contains(
                            "open",
                            case=False,
                            na=False
                        )
                    ]
                )

                return f"🔓 There are **{count} open bugs**."


        # CLOSED BUGS
        if "closed bug" in question or "closed bugs" in question:

            if "Status" in data.columns:

                count = len(
                    data[
                        data["Status"]
                        .astype(str)
                        .str.contains(
                            "closed",
                            case=False,
                            na=False
                        )
                    ]
                )

                return f"✅ There are **{count} closed bugs**."


        # CRITICAL BUGS
        if "critical bug" in question or "critical bugs" in question:

            if "Severity" in data.columns:

                count = len(
                    data[
                        data["Severity"]
                        .astype(str)
                        .str.contains(
                            "critical",
                            case=False,
                            na=False
                        )
                    ]
                )

                return f"🚨 There are **{count} critical bugs**."


        # AVERAGE RESOLUTION TIME
        if any(
            phrase in question
            for phrase in [
                "average resolution time",
                "average resolution",
                "avg resolution"
            ]
        ):

            if "Resolution_Time_Hours" in data.columns:

                average = (
                    data["Resolution_Time_Hours"]
                    .mean()
                )

                if pd.notna(average):

                    return (
                        f"⏱ The average resolution time is "
                        f"**{average:.2f} hours**."
                    )


        # TEAM WITH MOST BUGS
        if any(
            phrase in question
            for phrase in [
                "team with most bugs",
                "team with highest bugs",
                "which team has most bugs"
            ]
        ):

            if "Team" in data.columns:

                team_counts = (
                    data["Team"]
                    .fillna("Unknown")
                    .value_counts()
                )

                if not team_counts.empty:

                    team_name = team_counts.index[0]
                    bug_count = team_counts.iloc[0]

                    return (
                        f"👥 The team with the most bugs is "
                        f"**{team_name}**, with **{bug_count} bugs**."
                    )


        # MOST COMMON ROOT CAUSE
        if any(
            phrase in question
            for phrase in [
                "most common root cause",
                "top root cause",
                "main root cause"
            ]
        ):

            if "Root_Cause" in data.columns:

                root_counts = (
                    data["Root_Cause"]
                    .fillna("Unknown")
                    .value_counts()
                )

                if not root_counts.empty:

                    root_cause = root_counts.index[0]
                    bug_count = root_counts.iloc[0]

                    return (
                        f"🌳 The most common root cause is "
                        f"**{root_cause}**, with **{bug_count} bugs**."
                    )


        # Not recognized as a project statistics question
        return None


    # =====================================================
    # ASK AI
    # =====================================================

    if st.button(
        "Ask AI",
        type="primary",
        use_container_width=True,
        key="ask_ai"
    ):

        if user_question.strip():

            try:

                # -----------------------------------------
                # FIRST CHECK PROJECT DATA QUESTIONS
                # -----------------------------------------

                project_answer = answer_project_question(
                    user_question,
                    df
                )


                if project_answer is not None:

                    st.success("Answer:")
                    st.markdown(project_answer)


                # -----------------------------------------
                # GENERAL QUESTIONS -> GEMINI AI
                # -----------------------------------------

                else:

                    with st.spinner("⚡ Generating answer..."):

                        project_context = f"""
You are a helpful AI Assistant.

You are part of the project:

Intelligent Software Defect Tracking System with Resolution Assistance.

The project uses:
- Python
- Pandas
- Streamlit
- Plotly

The dashboard analyzes software bugs, bug status, priority,
severity, modules, root causes, teams, trends, and resolution time.

You can answer questions about this project.

You can ALSO answer completely general questions outside the project,
including questions about:
- Artificial Intelligence
- Machine Learning
- Python
- Programming
- Data Science
- Software Testing
- Science
- Technology
- General knowledge
- Other reasonable topics

Do not restrict your answers to the project.

Answer clearly and concisely unless the user asks for
a detailed explanation.

Question:
{user_question}
"""


                # Generate Gemini response

                    result = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=project_context
                    )

                    response = result.text

                    st.success("Answer:")
                    st.markdown(response)


            except Exception as e:

                st.error(
                    "❌ An error occurred while connecting "
                    "to the AI Assistant."
                )

                st.error(f"Error: {e}")


        else:

            st.warning("Please enter a question first.")


    # =========================================================
    # CLEAR CHAT BUTTON
    # =========================================================

    if st.button(
        "🗑 Clear Chat",
        use_container_width=True,
        key="clear_ai_chat"
    ):

        st.session_state.chat_history = []

        st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🐞 Intelligent Software Defect Tracking System with Resolution Assistance | "
    "Developed using Python, Pandas, Streamlit and Plotly"
)


# AI Projects Social Dashboard
# Required packages: streamlit, pandas, plotly
# Run: streamlit run app.py

from __future__ import annotations

import os
from io import StringIO
from typing import Iterable

import pandas as pd
import plotly.express as px
import streamlit as st


REQUIRED_COLUMNS = [
    "project_id",
    "project_name",
    "platform",
    "post_url",
    "post_date",
    "likes",
    "comments",
    "impressions",
]

SUPABASE_DEFAULT_TABLE = "social_posts"


def create_mock_data() -> pd.DataFrame:
    """Create realistic built-in sample data for first-run experience."""
    records = [
        {
            "project_id": "P001",
            "project_name": "LLM Prompt Coach",
            "platform": "LinkedIn",
            "post_url": "https://linkedin.com/posts/mock-001",
            "post_date": "2026-01-05",
            "likes": 82,
            "comments": 16,
            "impressions": 4200,
        },
        {
            "project_id": "P001",
            "project_name": "LLM Prompt Coach",
            "platform": "Twitter/X",
            "post_url": "https://twitter.com/mock/status/001",
            "post_date": "2026-01-10",
            "likes": 56,
            "comments": 11,
            "impressions": 3600,
        },
        {
            "project_id": "P002",
            "project_name": "AI Resume Critic",
            "platform": "LinkedIn",
            "post_url": "https://linkedin.com/posts/mock-002",
            "post_date": "2026-01-08",
            "likes": 140,
            "comments": 31,
            "impressions": 8100,
        },
        {
            "project_id": "P002",
            "project_name": "AI Resume Critic",
            "platform": "Twitter/X",
            "post_url": "https://twitter.com/mock/status/002",
            "post_date": "2026-01-14",
            "likes": 96,
            "comments": 20,
            "impressions": 6400,
        },
        {
            "project_id": "P003",
            "project_name": "Vision QA Bot",
            "platform": "LinkedIn",
            "post_url": "https://linkedin.com/posts/mock-003",
            "post_date": "2026-01-12",
            "likes": 73,
            "comments": 14,
            "impressions": 5000,
        },
        {
            "project_id": "P003",
            "project_name": "Vision QA Bot",
            "platform": "Twitter/X",
            "post_url": "https://twitter.com/mock/status/003",
            "post_date": "2026-01-20",
            "likes": 61,
            "comments": 9,
            "impressions": 3900,
        },
        {
            "project_id": "P004",
            "project_name": "Meeting Notes Copilot",
            "platform": "LinkedIn",
            "post_url": "https://linkedin.com/posts/mock-004",
            "post_date": "2026-01-16",
            "likes": 204,
            "comments": 46,
            "impressions": 12200,
        },
        {
            "project_id": "P004",
            "project_name": "Meeting Notes Copilot",
            "platform": "Twitter/X",
            "post_url": "https://twitter.com/mock/status/004",
            "post_date": "2026-01-23",
            "likes": 132,
            "comments": 27,
            "impressions": 8800,
        },
        {
            "project_id": "P005",
            "project_name": "RAG Benchmark Lab",
            "platform": "LinkedIn",
            "post_url": "https://linkedin.com/posts/mock-005",
            "post_date": "2026-01-19",
            "likes": 111,
            "comments": 22,
            "impressions": 7300,
        },
        {
            "project_id": "P005",
            "project_name": "RAG Benchmark Lab",
            "platform": "Twitter/X",
            "post_url": "https://twitter.com/mock/status/005",
            "post_date": "2026-01-28",
            "likes": 87,
            "comments": 18,
            "impressions": 6100,
        },
        {
            "project_id": "P006",
            "project_name": "Agent Workflow Studio",
            "platform": "LinkedIn",
            "post_url": "https://linkedin.com/posts/mock-006",
            "post_date": "2026-01-22",
            "likes": 175,
            "comments": 39,
            "impressions": 10900,
        },
        {
            "project_id": "P006",
            "project_name": "Agent Workflow Studio",
            "platform": "Twitter/X",
            "post_url": "https://twitter.com/mock/status/006",
            "post_date": "2026-01-31",
            "likes": 118,
            "comments": 25,
            "impressions": 7900,
        },
        {
            "project_id": "P007",
            "project_name": "AI Interview Simulator",
            "platform": "LinkedIn",
            "post_url": "https://linkedin.com/posts/mock-007",
            "post_date": "2026-02-02",
            "likes": 154,
            "comments": 33,
            "impressions": 9400,
        },
        {
            "project_id": "P007",
            "project_name": "AI Interview Simulator",
            "platform": "Twitter/X",
            "post_url": "https://twitter.com/mock/status/007",
            "post_date": "2026-02-07",
            "likes": 101,
            "comments": 19,
            "impressions": 6800,
        },
        {
            "project_id": "P008",
            "project_name": "MLOps Health Monitor",
            "platform": "LinkedIn",
            "post_url": "https://linkedin.com/posts/mock-008",
            "post_date": "2026-02-05",
            "likes": 66,
            "comments": 12,
            "impressions": 4700,
        },
        {
            "project_id": "P008",
            "project_name": "MLOps Health Monitor",
            "platform": "Twitter/X",
            "post_url": "https://twitter.com/mock/status/008",
            "post_date": "2026-02-11",
            "likes": 49,
            "comments": 8,
            "impressions": 3300,
        },
    ]
    df = pd.DataFrame(records)
    return _prepare_dataframe(df)


def _prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize dtypes and derived columns."""
    prepared = df.copy()
    prepared["post_date"] = pd.to_datetime(prepared["post_date"], errors="coerce")
    numeric_cols = ["likes", "comments", "impressions"]
    for col in numeric_cols:
        prepared[col] = pd.to_numeric(prepared[col], errors="coerce").fillna(0)

    denom = prepared["impressions"].where(prepared["impressions"] > 0)
    prepared["engagement_rate_proxy"] = ((prepared["likes"] + prepared["comments"]) / denom).fillna(0)

    return prepared


def _validate_columns(df: pd.DataFrame, required_columns: Iterable[str]) -> tuple[bool, list[str]]:
    missing = [col for col in required_columns if col not in df.columns]
    return len(missing) == 0, missing


def get_supabase_client():
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")
    if not supabase_url or not supabase_key:
        return None

    from supabase import create_client

    return create_client(supabase_url, supabase_key)


def load_data_from_supabase() -> pd.DataFrame | None:
    client = get_supabase_client()
    if client is None:
        return None

    table_name = os.environ.get("SUPABASE_TABLE", SUPABASE_DEFAULT_TABLE)
    response = client.table(table_name).select("*").execute()
    if response.error:
        st.error(f"Supabase query failed: {response.error.message}")
        return None

    data = response.data or []
    if not data:
        return pd.DataFrame(columns=REQUIRED_COLUMNS)

    return _prepare_dataframe(pd.DataFrame(data))


def import_data_to_supabase(df: pd.DataFrame) -> tuple[bool, str]:
    client = get_supabase_client()
    if client is None:
        return False, "Supabase credentials are not set."

    table_name = os.environ.get("SUPABASE_TABLE", SUPABASE_DEFAULT_TABLE)
    upload_df = df.copy()
    upload_df["post_date"] = upload_df["post_date"].dt.strftime("%Y-%m-%d")
    rows = upload_df[REQUIRED_COLUMNS].to_dict(orient="records")

    result = client.table(table_name).insert(rows).execute()
    if result.error:
        return False, str(result.error)

    return True, f"Imported {len(rows)} rows into Supabase table '{table_name}'."


def load_data() -> pd.DataFrame:
    """Load data from Supabase, uploaded CSV, or mock data."""
    st.sidebar.header("Data Source")

    supabase_available = bool(os.environ.get("SUPABASE_URL") and os.environ.get("SUPABASE_KEY"))
    data_source_options = ["Upload CSV", "Built-in mock data"]
    if supabase_available:
        data_source_options.insert(0, "Supabase")

    data_source = st.sidebar.radio(
        "Select data source",
        options=data_source_options,
        index=0 if supabase_available else 1,
    )

    if data_source == "Supabase":
        supabase_df = load_data_from_supabase()
        if supabase_df is not None:
            return supabase_df

        st.warning("Unable to load data from Supabase. Falling back to built-in mock data.")
        return create_mock_data()

    if data_source == "Built-in mock data":
        st.info("Using built-in mock data")
        return create_mock_data()

    uploaded_file = st.sidebar.file_uploader("Upload CSV (optional)", type=["csv"])
    if uploaded_file is None:
        st.info("Using built-in mock data")
        return create_mock_data()

    try:
        content = uploaded_file.getvalue().decode("utf-8")
        raw_df = pd.read_csv(StringIO(content))
    except Exception as exc:
        st.error(f"Unable to read uploaded CSV: {exc}")
        st.warning("Falling back to built-in mock data.")
        return create_mock_data()

    prepared_df = _prepare_dataframe(raw_df)

    if supabase_available:
        if st.sidebar.button("Import uploaded CSV into Supabase"):
            success, message = import_data_to_supabase(prepared_df)
            if success:
                st.success(message)
            else:
                st.error(message)

    is_valid, missing_cols = _validate_columns(prepared_df, REQUIRED_COLUMNS)
    if not is_valid:
        st.error(
            "Uploaded CSV is missing required columns: "
            + ", ".join(missing_cols)
            + ". Falling back to mock data."
        )
        return create_mock_data()

    return prepared_df


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Apply sidebar filters for platform, project, and date range."""
    st.sidebar.header("Filters")
    platform_options = sorted(df["platform"].dropna().unique().tolist())
    project_options = sorted(df["project_name"].dropna().unique().tolist())

    selected_platforms = st.sidebar.multiselect(
        "Platform",
        options=platform_options,
        default=platform_options,
    )
    selected_projects = st.sidebar.multiselect(
        "Project Name",
        options=project_options,
        default=project_options,
    )

    min_date = df["post_date"].min()
    max_date = df["post_date"].max()
    if pd.isna(min_date) or pd.isna(max_date):
        return df.iloc[0:0].copy()

    selected_dates = st.sidebar.date_input(
        "Date Range",
        value=(min_date.date(), max_date.date()),
        min_value=min_date.date(),
        max_value=max_date.date(),
    )

    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        start_date, end_date = pd.to_datetime(selected_dates[0]), pd.to_datetime(selected_dates[1])
    else:
        # If user picks only one date, use same date for both start/end.
        single_date = pd.to_datetime(selected_dates)
        start_date, end_date = single_date, single_date

    mask = (
        df["platform"].isin(selected_platforms)
        & df["project_name"].isin(selected_projects)
        & (df["post_date"] >= start_date)
        & (df["post_date"] <= end_date)
    )
    return df.loc[mask].copy()


def compute_project_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate post-level data into project-level performance table."""
    summary = (
        df.groupby(["project_id", "project_name"], as_index=False)
        .agg(
            num_posts=("post_url", "count"),
            total_likes=("likes", "sum"),
            total_comments=("comments", "sum"),
            total_impressions=("impressions", "sum"),
        )
        .sort_values("total_impressions", ascending=False)
    )
    summary["avg_impressions_per_post"] = (
        summary["total_impressions"] / summary["num_posts"]
    ).round(2)
    summary["engagement_score"] = summary["total_likes"] + summary["total_comments"] * 2
    return summary


def get_top_projects(summary_df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Return top N projects ranked by total impressions."""
    ranked = summary_df.sort_values("total_impressions", ascending=False).head(top_n).copy()
    ranked.insert(0, "rank", range(1, len(ranked) + 1))
    return ranked


def _format_int(x: float | int) -> str:
    return f"{int(round(x)):,}"


def render_kpis(df: pd.DataFrame) -> None:
    """Render top KPI cards."""
    total_projects = int(df["project_id"].nunique())
    total_posts = int(len(df))
    total_likes = int(df["likes"].sum())
    total_comments = int(df["comments"].sum())
    total_impressions = int(df["impressions"].sum())

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Projects", _format_int(total_projects))
    c2.metric("Total Posts", _format_int(total_posts))
    c3.metric("Total Likes", _format_int(total_likes))
    c4.metric("Total Comments", _format_int(total_comments))
    c5.metric("Total Impressions", _format_int(total_impressions))


def render_charts(df: pd.DataFrame, top_projects: pd.DataFrame) -> None:
    """Render dashboard-level Plotly charts."""
    st.subheader("Performance Visuals")
    top_project_names = top_projects["project_name"].tolist()
    chart_df = df[df["project_name"].isin(top_project_names)].copy()
    project_order = top_project_names

    impressions_by_project = (
        chart_df.groupby("project_name", as_index=False)["impressions"].sum()
        .sort_values("impressions", ascending=False)
    )
    fig_impressions = px.bar(
        impressions_by_project,
        x="project_name",
        y="impressions",
        title="Top 10 Projects: Total Impressions",
        text_auto=True,
    )
    fig_impressions.update_layout(xaxis_title="", yaxis_title="Impressions", xaxis_tickangle=-30)

    likes_by_project = (
        chart_df.groupby("project_name", as_index=False)["likes"].sum().sort_values("likes", ascending=False)
    )
    fig_likes = px.bar(
        likes_by_project,
        x="project_name",
        y="likes",
        title="Top 10 Projects: Total Likes",
        text_auto=True,
    )
    fig_likes.update_layout(xaxis_title="", yaxis_title="Likes", xaxis_tickangle=-30)

    engagement_platform = (
        chart_df.assign(engagement=chart_df["likes"] + chart_df["comments"] * 2)
        .groupby(["project_name", "platform"], as_index=False)["engagement"]
        .sum()
    )
    fig_platform = px.bar(
        engagement_platform,
        x="project_name",
        y="engagement",
        color="platform",
        title="Top 10 Projects: Engagement by Platform",
        barmode="stack",
        category_orders={"project_name": project_order},
    )
    fig_platform.update_layout(xaxis_title="", yaxis_title="Engagement", xaxis_tickangle=-30)

    by_date = df.groupby("post_date", as_index=False)["impressions"].sum().sort_values("post_date")
    fig_line = px.line(
        by_date,
        x="post_date",
        y="impressions",
        markers=True,
        title="Impressions Over Time",
    )
    fig_line.update_layout(xaxis_title="Date", yaxis_title="Impressions")

    platform_dist = df.groupby("platform", as_index=False)["post_url"].count().rename(
        columns={"post_url": "posts"}
    )
    fig_donut = px.pie(
        platform_dist,
        names="platform",
        values="posts",
        title="Post Distribution by Platform",
        hole=0.55,
    )

    row1_col1, row1_col2 = st.columns(2)
    row1_col1.plotly_chart(fig_impressions, use_container_width=True)
    row1_col2.plotly_chart(fig_likes, use_container_width=True)

    row2_col1, row2_col2 = st.columns(2)
    row2_col1.plotly_chart(fig_platform, use_container_width=True)
    row2_col2.plotly_chart(fig_line, use_container_width=True)

    st.plotly_chart(fig_donut, use_container_width=True)


def render_project_drilldown(df: pd.DataFrame) -> None:
    """Render project-level post table and detailed charts."""
    st.subheader("Project Drill-Down")
    project_names = sorted(df["project_name"].dropna().unique().tolist())
    if not project_names:
        st.info("No projects available for drill-down with current filters.")
        return

    selected_project = st.selectbox("Select a project", project_names)
    project_df = (
        df.loc[df["project_name"] == selected_project]
        .sort_values("post_date")
        .copy()
    )
    project_df["post_date"] = project_df["post_date"].dt.date

    st.markdown("**Posts for selected project**")
    st.dataframe(
        project_df[
            [
                "platform",
                "post_url",
                "post_date",
                "likes",
                "comments",
                "impressions",
                "engagement_rate_proxy",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

    trend_df = project_df.copy()
    trend_df["post_date"] = pd.to_datetime(trend_df["post_date"])
    fig_project_line = px.line(
        trend_df,
        x="post_date",
        y="impressions",
        color="platform",
        markers=True,
        title=f"Impressions Over Time: {selected_project}",
    )
    fig_project_line.update_layout(xaxis_title="Date", yaxis_title="Impressions")

    interactions_long = trend_df.melt(
        id_vars=["post_url", "post_date"],
        value_vars=["likes", "comments"],
        var_name="metric",
        value_name="value",
    )
    fig_project_bars = px.bar(
        interactions_long,
        x="post_date",
        y="value",
        color="metric",
        barmode="group",
        title=f"Likes and Comments per Post: {selected_project}",
        hover_data=["post_url"],
    )
    fig_project_bars.update_layout(xaxis_title="Date", yaxis_title="Count")

    d1, d2 = st.columns(2)
    d1.plotly_chart(fig_project_line, use_container_width=True)
    d2.plotly_chart(fig_project_bars, use_container_width=True)


def _to_csv_download_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def main() -> None:
    st.set_page_config(page_title="AI Projects Social Dashboard", layout="wide")
    st.title("AI Projects – LinkedIn & Twitter Dashboard")
    st.caption("Track weekly side project traction across LinkedIn and Twitter/X.")

    df = load_data()

    is_valid, missing_cols = _validate_columns(df, REQUIRED_COLUMNS)
    if not is_valid:
        st.error(
            "Data is missing required columns: "
            + ", ".join(missing_cols)
            + ". Please upload a valid CSV."
        )
        st.stop()

    filtered_df = apply_filters(df)
    if filtered_df.empty:
        st.warning("No data matches the selected filters. Try widening your filters.")
        st.stop()

    render_kpis(filtered_df)
    st.markdown("---")

    summary_df = compute_project_summary(filtered_df)
    top_10_summary = get_top_projects(summary_df, top_n=10)
    st.subheader("Top 10 Project Summary")
    display_summary = top_10_summary.rename(
        columns={
            "rank": "Rank",
            "project_id": "Project ID",
            "project_name": "Project Name",
            "num_posts": "Number of Posts",
            "total_likes": "Total Likes",
            "total_comments": "Total Comments",
            "total_impressions": "Total Impressions",
            "avg_impressions_per_post": "Average Impressions per Post",
            "engagement_score": "Engagement Score",
        }
    )
    st.dataframe(display_summary, use_container_width=True, hide_index=True)

    dl1, dl2 = st.columns(2)
    dl1.download_button(
        "Download filtered data (CSV)",
        data=_to_csv_download_bytes(filtered_df),
        file_name="filtered_posts.csv",
        mime="text/csv",
        use_container_width=True,
    )
    dl2.download_button(
        "Download project summary (CSV)",
        data=_to_csv_download_bytes(summary_df),
        file_name="project_summary.csv",
        mime="text/csv",
        use_container_width=True,
    )

    show_raw = st.checkbox("Show raw data")
    if show_raw:
        st.subheader("Raw Data")
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    render_charts(filtered_df, top_10_summary)
    st.markdown("---")
    render_project_drilldown(filtered_df)


if __name__ == "__main__":
    main()

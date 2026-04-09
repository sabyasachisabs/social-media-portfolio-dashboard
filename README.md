# social-media-portfolio-dashboard

A Streamlit dashboard for tracking social media project performance across LinkedIn and Twitter/X.

## Setup

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Run locally

```bash
streamlit run app.py
```

or:

```bash
./run.sh
```

## Deployment

Deploy on Streamlit Cloud or another Python host. Make sure `requirements.txt` is present so the platform installs:

- `streamlit`
- `pandas`
- `plotly`
- `supabase`

## Supabase integration

If you set `SUPABASE_URL` and `SUPABASE_KEY` as environment variables or Streamlit Cloud secrets, the app can read from a Supabase table named by `SUPABASE_TABLE` (default: `social_posts`).

The table should include these columns:

- `project_id`
- `project_name`
- `platform`
- `post_url`
- `post_date`
- `likes`
- `comments`
- `impressions`

When using the app:

- select `Supabase` in the sidebar data source
- or upload a CSV and click `Import uploaded CSV into Supabase`

Use Streamlit Cloud secrets to protect your keys:

- `SUPABASE_URL`
- `SUPABASE_KEY`
- optional: `SUPABASE_TABLE`

A Streamlit dashboard for tracking social media project performance across LinkedIn and Twitter/X.

## Setup

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Run locally

```bash
streamlit run app.py
```

## Deployment

Deploy on Streamlit Cloud or another Python host. Make sure `requirements.txt` is present so the platform installs:

- `streamlit`
- `pandas`
- `plotly`

If you use the provided `run.sh`, it will also create a virtual environment and install the same dependencies.

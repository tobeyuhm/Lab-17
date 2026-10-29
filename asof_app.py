"""A FRED-style Streamlit page that prevents look-ahead bias with ALFRED vintages."""

from datetime import date
from io import StringIO
import re
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pandas as pd
import streamlit as st


SERIES = {
    "BAA": "Moody's Baa corporate bond yield",
    "FEDFUNDS": "Effective federal funds rate",
    "DGS10": "10-year Treasury yield",
    "MORTGAGE30US": "30-year fixed mortgage rate",
}
FRED_GRAPH = "https://fred.stlouisfed.org/graph/fredgraph.csv"
ALFRED_GRAPH = "https://alfred.stlouisfed.org/graph/alfredgraph.csv"


def fred_page(series_id):
    """Return the public FRED landing page for a series."""
    return f"https://fred.stlouisfed.org/series/{series_id}"


def read_fred_csv(url):
    """Download one public CSV and turn periods plus '.' missing values into a series."""
    request = Request(url, headers={"User-Agent": "Mozilla/5.0 (Lab 17 learning app)"})
    with urlopen(request, timeout=30) as response:
        text = response.read().decode("utf-8-sig")
    frame = pd.read_csv(StringIO(text))
    if "observation_date" not in frame or len(frame.columns) < 2:
        raise ValueError("FRED did not return a recognized observation CSV for this ID.")
    value_column = frame.columns[-1]
    frame["observation_date"] = pd.to_datetime(frame["observation_date"], errors="coerce")
    frame[value_column] = pd.to_numeric(frame[value_column], errors="coerce")
    return frame.dropna(subset=["observation_date"]).set_index("observation_date")[[value_column]]


@st.cache_data(ttl=3600, show_spinner=False)
def download_today(series_id):
    """Download the values FRED displays today for one series."""
    return read_fred_csv(f"{FRED_GRAPH}?{urlencode({'id': series_id})}")


@st.cache_data(ttl=3600, show_spinner=False)
def download_as_known_on(series_id, vintage_date):
    """Download ALFRED's values as they were published by one calendar date."""
    parameters = urlencode({"id": series_id, "vintage_date": vintage_date})
    return read_fred_csv(f"{ALFRED_GRAPH}?{parameters}")


def series_label(series_id):
    """Use the supplied name when known, otherwise retain the typed FRED ID."""
    return f"{series_id} — {SERIES.get(series_id, 'typed FRED series')}"


def build_comparison_row(series_id, current, vintage):
    """Summarize release lag and revisions using only dates known by the vintage."""
    known = vintage.dropna().iloc[:, 0]
    today = current.dropna().iloc[:, 0]
    if known.empty:
        raise ValueError("ALFRED has no published values for this series by the chosen date.")

    last_known_date = known.index.max()
    known_value = known.loc[last_known_date]
    today_same_date = today.get(last_known_date, float("nan"))
    today_after_known = int((today.index > last_known_date).sum())
    common_dates = known.index.intersection(today.index)
    revised = int(
        (known.loc[common_dates].sub(today.loc[common_dates]).abs() > 1e-12).sum()
    )
    return {
        "Series ID": fred_page(series_id),
        "Last date known then": last_known_date.date().isoformat(),
        "Value known then": known_value,
        "Value today (same date)": today_same_date,
        "Today's values after then": today_after_known,
        "Revised same-date values": revised,
    }


def main():
    st.set_page_config(page_title="Rates as of a Date", layout="wide")
    st.title("Rates as of a Date")
    st.caption(
        f"Data from FRED and ALFRED, Federal Reserve Bank of St. Louis, downloaded {date.today().isoformat()}; "
        "built with AI help, a learning demonstration, not investment advice."
    )

    with st.sidebar:
        selected = st.multiselect(
            "Rate series", list(SERIES), default=list(SERIES), format_func=series_label
        )
        typed_ids = st.text_input("Add FRED series ID(s), separated by commas").upper()
        start_date = st.date_input("Start date", value=date(2020, 1, 1))
        as_known_on = st.date_input("As known on", value=date.today())

    extra_ids = [item.strip() for item in typed_ids.split(",") if item.strip()]
    invalid_ids = [item for item in extra_ids if not re.fullmatch(r"[A-Z0-9_]+", item)]
    for item in invalid_ids:
        st.error(f"{item!r} is not a valid FRED series ID format.")
    chosen = list(dict.fromkeys([*selected, *(item for item in extra_ids if item not in invalid_ids)]))
    if not chosen:
        st.info("Choose a listed series or enter a FRED series ID.")
        return

    rows = []
    start_timestamp = pd.Timestamp(start_date)
    vintage_text = as_known_on.isoformat()
    for series_id in chosen:
        try:
            current = download_today(series_id)
            vintage = download_as_known_on(series_id, vintage_text)
            current = current.loc[current.index >= start_timestamp]
            vintage = vintage.loc[vintage.index >= start_timestamp]
            if current.dropna().empty:
                raise ValueError("FRED returned no current observations from the selected start date.")

            st.subheader(series_label(series_id))
            st.line_chart(current.rename(columns={current.columns[0]: series_id}), use_container_width=True)
            known = vintage.dropna().iloc[:, 0]
            if known.empty:
                st.warning(f"No values were published for {series_id} by {vintage_text}.")
            else:
                last_known = known.index.max().date().isoformat()
                st.caption(f"Last data date known on {vintage_text}: **{last_known}**")
            rows.append(build_comparison_row(series_id, current, vintage))
        except Exception as error:
            st.error(f"{series_id}: {error}")

    if rows:
        st.subheader("As-of comparison")
        table = pd.DataFrame(rows)
        st.dataframe(
            table,
            hide_index=True,
            use_container_width=True,
            column_config={
                "Series ID": st.column_config.LinkColumn("Series ID", display_text=r".*/series/(.*)$"),
                "Value known then": st.column_config.NumberColumn(format="%.2f"),
                "Value today (same date)": st.column_config.NumberColumn(format="%.2f"),
            },
        )
        st.caption(
            "A revised same-date value differs between the selected ALFRED vintage and today's FRED value. "
            "A value after the last date known then was not available for a decision on that date."
        )


if __name__ == "__main__":
    main()

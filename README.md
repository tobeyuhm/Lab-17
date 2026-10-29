# Lab 17 — Rates as of a Date

This repository contains a Streamlit app that compares today's FRED values with
the ALFRED vintage available on a selected date, plus the DGS10 Project 2 data
card.

## Live app

https://lab-17-8ngf93khrnul8pffdva2pv.streamlit.app/

## Run

```powershell
python -m pip install -r requirements.txt
streamlit run asof_app.py
```

The app defaults to BAA, FEDFUNDS, DGS10, and MORTGAGE30US. It also accepts a
typed FRED series ID, including DGS10 for the Joby Aviation Project 2 analysis.

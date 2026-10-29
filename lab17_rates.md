# Lab 17 — Rates as of a Date

## Live app

https://lab-17-8ngf93khrnul8pffdva2pv.streamlit.app/

## Project 2 data card: DGS10

| Field | Evidence |
|---|---|
| Series ID and source | [DGS10 — Market Yield on U.S. Treasury Securities at 10-Year Constant Maturity, Quoted on an Investment Basis](https://fred.stlouisfed.org/series/DGS10) |
| What it measures | The market yield on U.S. Treasury securities at a constant 10-year maturity, quoted on an investment basis. It is a broad long-term Treasury-rate benchmark relevant to discount rates and financing conditions for Joby Aviation (JOBY). |
| Source and release | Board of Governors of the Federal Reserve System (US), H.15 Selected Interest Rates, distributed through FRED and ALFRED. |
| Units | Percent, not seasonally adjusted. |
| Frequency | Daily. |
| Publication lag | In the app's 2026-09-30 ALFRED test, the last observation known then was 2026-09-29 (5.26%). The September 30 observation (5.29%) was not yet known on September 30, showing a one-business-day publication lag in this test. |
| Revisions | The same test found 0 revised same-date values through today's FRED download, although the FRED page notes that all data are subject to revision. I must keep checking the revision count for each decision vintage. |
| Download date | 2026-10-29 |

### Three-value FRED page check

Before submission, I will read these three observations on the FRED DGS10 page and mark each as checked:

| Observation date | DGS10 value (percent) | Checked by me |
|---|---:|---|
| 2026-09-28 | 5.24 | [ ] |
| 2026-09-29 | 5.26 | [ ] |
| 2026-09-30 | 5.29 | [ ] |

## As-of evidence from the app

With the app set to **as known on 2026-09-30**, it reported:

| Field | Result |
|---|---:|
| Last date known then | 2026-09-29 |
| Value known then | 5.26% |
| Value today on that same date | 5.26% |
| Today's values after the last date known then | 19 |
| Revised same-date values | 0 |

The 19 later values were not known on September 30, so a backtest using today's full DGS10 history would have leaked information that was unavailable to a decision made that day.

## Partner attack — complete during class

**Partner's name:** [enter name]

**Field my partner trusts least:** [publication date / revisions / units]

**My two-sentence response:** [write two sentences in your own words, citing the one-business-day lag, the 0 revised same-date values in the app test, or the FRED source/units above.]

## My Project 2 call

**Admit with an as-of rule:** DGS10 may be used as a Project 2 rate factor for JOBY only from the ALFRED vintage available on the decision date; I will use the latest value published by then, not today's completed historical series. The 2026-09-30 test shows a one-business-day lag and no revisions in the tested 2020–2026 overlap, so it is suitable as a lagged daily market-rate input; I will quarantine it if a future app test shows material revisions or a longer publication lag, and reconsider if the Project 2 rule requires a same-day value before it has been published.

## Estimation-risk reflection

The data card prevents a look-ahead leak by naming the source, units, frequency, publication lag, revision behavior, and download date before a model uses the series. “Cleaning” values does not answer when each value became knowable: ALFRED's vintage date and the app's last-known date do.

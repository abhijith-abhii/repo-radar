# Repo Radar — learning guide

## What it does

Understand public repository activity. The intended user is job seekers and maintainers. Browser controls → validated Flask API → project analysis/workflow → results and export.

## Run and demonstrate

Follow the README installation block, then: Run sample mode and reconcile 36 commits across contributors and dates. Switch to a public owner/repository in live mode; inspect the retrieval timestamp and bounded-coverage note.

## Important files

- `app.py` — local HTTP interface and request/error handling.
- `core.py` — project-specific logic.
- `tests/` — regression and correctness checks.
- `reports/` — recorded outputs and verification evidence.

## Three engineering decisions

1. Cap API pagination at three pages to bound response time and unauthenticated rate use.
2. Cache public snapshots for five minutes, clearly separating sample and live modes.
3. Exclude pull-request records from issue totals and avoid treating commit counts as productivity.

## Five interview questions

1. **What does the live dashboard measure?** It samples up to three pages of commits and issue/PR records from the public GitHub API. PR records are removed from issue counts; the result is a bounded snapshot, not full repository history.

2. **Why cache results?** A five-minute disk cache reduces repeated requests and rate-limit pressure. The recorded retrieval timestamp tells a reader how fresh a result is.

3. **Does commit count measure developer performance?** No. Squashes, bots, pair work and different contribution types distort commit counts. The dashboard describes activity and never ranks people by productivity.

4. **How are sample and live data distinguished?** Sample mode explicitly labels its synthetic records. Live mode records the actual repository and retrieval time. A real Flask API snapshot is saved in reports/live-api.json.

5. **How does the app handle API failure?** It uses request timeouts and distinct messages for missing repositories, rate limits and other failures. Sample mode is an explicit fallback, never silently substituted as a live result.

## Independent exercise

Add an explicit issues state selector and preserve the state in the cache key.

Write down the expected behavior before editing. Add a meaningful regression check, run the existing suite, and describe what changed in your own words.

## Contribution and resume guidance

The implementation was developed with substantial AI assistance under Abhijith Viswanathan's direction. The verified contribution is the working artifact and the learning work actually completed, not invented employment or adoption.

Suggested factual bullet after personally validating the demo:

- Built a cached GitHub activity explorer with bounded pagination and explicit sample/live modes; validated a real public API snapshot of 300 commits.

Use [VERIFICATION.md](VERIFICATION.md) to add only measured numbers. Do not claim production traffic, users, savings, upstream acceptance or cloud deployment without corresponding evidence.

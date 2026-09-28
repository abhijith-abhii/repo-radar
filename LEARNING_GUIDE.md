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

1. **What problem does this project solve, and what is its unit of work?** Explain understand public repository activity, identify job seekers and maintainers as the audience, and trace one concrete example through the files above. Use the demonstration output rather than hypothetical impact.
2. **Why did you choose the first design decision?** Cap API pagination at three pages to bound response time and unauthenticated rate use. Show the corresponding implementation and a test that would fail if that property were removed.
3. **How do you protect correctness when inputs or execution change?** Cache public snapshots for five minutes, clearly separating sample and live modes. Explain the relevant invalid-input or edge-case test and distinguish a checked property from an untested assumption.
4. **How do you make results inspectable and reproducible?** Exclude pull-request records from issue totals and avoid treating commit counts as productivity. Point to actual outputs and recorded commands. Explain why a successful example is weaker evidence than a tested boundary or independently reconciled total.
5. **What would you improve before real deployment or real-data use?** At most 300 commits and 300 default issue-endpoint records. GitHub's issues endpoint defaults to open issues, so live issue counts describe the returned open sample. Commit timestamps are author times. No private repository tokens are used. Choose one limitation, describe the missing evidence, and propose a measurable acceptance check rather than promising production readiness.

## Independent exercise

Add an explicit issues state selector and preserve the state in the cache key.

Write down the expected behavior before editing. Add a meaningful regression check, run the existing suite, and describe what changed in your own words.

## Contribution and resume guidance

The implementation was developed with substantial AI assistance under Abhijith Viswanathan's direction. The verified contribution is the working artifact and the learning work actually completed, not invented employment or adoption.

Suggested factual bullet after personally validating the demo:

- Implemented and validated understand public repository activity using Python · Flask, with github pagination and documented correctness checks and limitations.

Use [VERIFICATION.md](VERIFICATION.md) to add only measured numbers. Do not claim production traffic, users, savings, upstream acceptance or cloud deployment without corresponding evidence.

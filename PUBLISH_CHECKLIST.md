# PUBLISH_CHECKLIST.md — from here to posted, step by step

Working order. Nothing below changes frozen or party-ruled content.
Items marked **[NOAH]** need your hands (accounts, credentials, judgment);
items marked **[CLAUDE]** I can do in a session when you say go.

## Phase 0 — credential rotation (required BEFORE anything publishes)

The Anthropic and RunPod keys have appeared in session transcripts; the
parties and you set "before publication" as the rotation deadline.

1. **[NOAH] Anthropic key:** console.anthropic.com → Settings → API Keys →
   Create Key (name it e.g. `thus-therefore-post`) → copy it → Delete/
   disable the old key.
2. **[NOAH] Update the env var** (new PowerShell window):
   `[Environment]::SetEnvironmentVariable('ANTHROPIC_API_KEY','<new>','User')`
3. **[NOAH] RunPod key:** runpod.io console → Settings → API Keys →
   Create API Key (Read/Write) → Revoke the old one.
   Then: `[Environment]::SetEnvironmentVariable('RUNPOD_API_KEY','<new>','User')`
4. **[CLAUDE] Verify both:** one cheap Anthropic call (judge smoke-style,
   pennies) + one RunPod balance query; confirm old keys are dead.
5. **[CLAUDE] Repo hygiene scan:** grep the repo (not just worktree —
   `git log -p`) for `sk-ant`, `rpa_`, key-shaped strings before the repo
   gets attention. (Keys were never committed; this is belt-and-braces.)

## Phase 1 — final content pass

6. **[NOAH] Voice pass on `writeup/results_post.md`.** The header note
   marks what's editable: party-required elements may be reworded but not
   removed; verbatim-quoted scoring blocks and Fable's closing sentence
   may not be edited at all. Things to look for: tone, length, your intro
   framing, whether you want a personal preamble about being the courier.
7. **[NOAH] Read `writeup/prereg_post.md` once more.** Its design content
   is frozen (hash is in it); voice edits were always allowed. Do NOT add
   any post-hoc motivation (e.g. watermarking) — its value is being
   frozen-time text; the results post carries the timing story.
8. **[CLAUDE] Consistency check:** numbers in the results post vs the
   committed analysis JSONs; all internal repo links valid; both posts
   reference the same manifest hash.

## Phase 2 — repo made presentation-ready

9. **[CLAUDE] README top section:** add a "Results" block up top linking
   RESULTS.md (with its correction), the corrected analysis files, and —
   after posting — the two live post URLs.
10. **[CLAUDE] Tag and release:** `git tag v1.0-results && git push --tags`;
    then a GitHub Release ("Rung 1 + instruct follow-on: corrected
    results") attaching `runs-raw-dataset.tar.gz`,
    `runs-raw-dataset-followon.tar.gz`, and the corrected-dataset tarball
    with their sha256s in the release notes. (Release upload is a
    `gh release create` — I can run it.)
11. **[NOAH] Optional but recommended:** enable GitHub Issues on the repo
    so post readers have somewhere to file questions.

## Phase 3 — publish (both posts, same sitting)

Venue per the standing plan: **LessWrong** (both posts), with Alignment
Forum crossposting if offered.

12. **[NOAH] Account:** log in at lesswrong.com (or create an account —
    email + display name; if you want the posts under your real name,
    set that in profile now). New accounts may have a short karma/rate
    limit on posting; if blocked, the fallback is posting one day apart
    or contacting LW mods (intercom button, bottom right) — they're fast.
13. **[NOAH] Post 1 — the pre-registration post.** New Post → paste
    `prereg_post.md` (LW editor accepts markdown; check the two hash
    strings didn't wrap oddly). Title suggestion: the file's own title.
    Tags: AI, Chain-of-Thought, Interpretability, Forecasting & Prediction.
    Publish. **Copy the URL.**
14. **[NOAH or CLAUDE] Link it:** insert the prereg post URL into the
    results post where the manifest/pre-registration is first mentioned.
15. **[NOAH] Post 2 — the results post.** New Post → paste the final
    `results_post.md`. Consider LW's "linkpost" field pointing at the
    GitHub release. Publish. Copy URL.
16. **[NOAH] Cross-link:** edit the prereg post, add one line at top:
    "Results are now posted: [link]." (This preserves the frozen text —
    an addition above it, clearly dated, is standard practice.)
17. **[NOAH] Alignment Forum:** if your account has AF posting rights the
    editor shows a crosspost toggle — use it for both. If not, LW is
    sufficient; AF mods sometimes promote LW posts on their own.
18. **[CLAUDE] After URLs exist:** commit them into README and RESULTS.md
    header; update the memory file.

## Phase 4 — announcement & follow-through (optional, recommended)

19. **[NOAH] One tweet/X thread or short post wherever you have reach,**
    linking the results post. The watermarking timing is the hook; the
    prediction ledger is the substance. (I can draft this.)
20. **[NOAH] Watch comments for 48h;** flag anything technical to me —
    LW commenters will likely probe the repair/certification chain, and
    the diagnosis documents answer nearly everything.
21. **[CLAUDE] Archive snapshot:** submit both post URLs + the GitHub
    release to web.archive.org (timestamp insurance).

## Phase 5 — the queued follow-ups (after publication, no deadline)

22. **[BOTH] Bridge arm** (party-blessed, exploratory): fresh design
    freeze per Sol's 3-arm amendment + Fable's Δ-comparability suggestion;
    ~$50 top-up; own manifest; results appended to the repo and optionally
    a short LW follow-up post.
23. **[BOTH] arXiv paper:** structure already exists (positioning_notes,
    watermarking_context, methods-lessons). Needs: LaTeX draft, full-text
    pass on the "authors pending" citations in references.bib, and an
    arXiv account (cs.CL or cs.AI; first-time submitters sometimes need an
    endorsement — an easy ask given the repo).
24. **[NOAH] Decide on rungs 2–4** — the outcome-filtered crux is the
    scientifically live question and both parties flagged it as unrun.

Current account state for reference: RunPod $6.04 (enough for phase 0–4;
bridge arm needs ~$50 more when you get there).

## Status addendum (2026-08-27)

- **Step 5 secret scan: EXECUTED, CLEAN.** Full git history (all commits,
  all diffs) + worktree: zero matches for Anthropic/RunPod/HF/AWS key
  patterns or private-key blocks; no env/credential files ever committed.
  Keys appeared only in local ~/.claude session transcripts (not the
  repo) — rotation (steps 1-3) STILL PENDING and remains the only
  credential exposure to close.
- **Author identity note:** all commits are authored
  `Noah <noah@foreverbuilt.com>` — public on GitHub since day one,
  standard practice, and UNREMOVABLE without rewriting history (which
  would destroy the timestamp commits 79781ea/bc93833). Noah signed off
  2026-08-27. Future repos: use GitHub noreply email if unwanted.
- **Archive.org: NEVER archived** (verified via availability API
  2026-08-27: no snapshots exist, ours or crawler's). Archiving remains a
  post-publication step (21). Honest scope: a snapshot now proves
  existence-by-now only; it cannot retroactively witness the Aug-8 push.
- **Timestamp lesson for next prereg** (also in IDEAS file): anchor the
  manifest hash to an external witness AT FREEZE TIME — OpenTimestamps
  and/or an archive.org crawl — so "when" is independent of all parties.
- **Schedule:** soft publication target mid-to-late September 2026 ruled
  worth it (core contributions don't decay; news-cycle loss already
  mostly absorbed; scoop risk mitigated by git priority).

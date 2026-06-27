# pretext-fix

Materials for an upstream PreTeXt fix: teacher-guide HTML builds fail on
PreTeXt **2.42.0** with `PTX:BUG: "hN" template reached without a $heading-level
parameter` for any `<paragraphs>` inside an activity/project `<prelude>` or
`<postlude>`. Student builds are unaffected, which is why only the `*-web-prof`
targets break.

Root cause: a missed template chain from upstream PR #2851 (which turned the old
heading-level fallback into a hard error). The `prelude`/`postlude` content is
not threaded the `$heading-level` parameter.

## Contents

- `PR-description.md` — full write-up for the upstream pull request (summary,
  reproducer, heading-level verification table, scope check, testing).
- `0001-HTML-thread-heading-level-through-prelude-postlude-c.patch` — the fix as a
  `git format-patch` (4 added lines in `xsl/pretext-html.xsl`). Recreates the
  branch/commit verbatim, authorship intact.
- `minimal-repro/` — a standalone PreTeXt project that triggers the bug.
  Run `pretext build web` inside it: fails on 2.42.0, builds clean once the patch
  is applied to core.

## How to submit the PR

The fix targets the upstream repo `PreTeXtBook/pretext` (default branch
`master` — *not* `main`).

```bash
# 1. Fork PreTeXtBook/pretext on GitHub, then:
git clone https://github.com/<your-username>/pretext.git
cd pretext

# 2. Recreate the branch + commit from the patch:
git checkout -b fix-heading-level-lude-paragraphs master
git am /path/to/pretext-fix/0001-HTML-thread-heading-level-through-prelude-postlude-c.patch

# 3. Push and open a PR against PreTeXtBook/pretext:master,
#    pasting PR-description.md as the body.
git push -u origin fix-heading-level-lude-paragraphs
```

Notes from upstream `CONTRIBUTING.md`: always use a topic branch; rebase (do not
merge) `master` if it goes stale; they normally like a heads-up on the
`pretext-dev` Google Group, but accept direct PRs "when something is clearly in
error and the change is readily apparent."

## Meanwhile: unblock local teacher builds

Downgrade the CLI to a pre-2.42.0 core (e.g. one already cached locally):

```bash
pip install "pretext==2.38.3"
```

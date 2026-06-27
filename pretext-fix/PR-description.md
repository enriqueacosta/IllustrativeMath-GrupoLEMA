# HTML: thread `heading-level` through `prelude`/`postlude` content

## Summary

PR #2851 reworked `mode="hN"` so that the heading level is *threaded* down as a
`$heading-level` parameter, and made the old `count()`-based fallback a reported
bug (`PTX:BUG ... defaulting to h2`). A few template chains were missed and have
since been fixed (#2864 Reveal, #2866 Preview, #2871 WeBWorK `task`).

This patches one more missed chain: the content of a `prelude`/`interlude`/`postlude`.
A titled `paragraphs` (or any heading-bearing block) inside the prelude/postlude
of a PROJECT-LIKE block (`activity`, `exploration`, `project`, ...) reaches
`mode="hN"` with no `$heading-level`, so every HTML build of such a document emits:

```
PTX:BUG: "hN" template reached without a $heading-level parameter
on element <paragraphs> at pretext/article/section/activity/prelude/paragraphs;
defaulting to h2
```

and the CLI treats it as a build error.

Two links were dropping the parameter:

1. The block `body` template applies `prelude`/`postlude` without passing
   `heading-level`.
2. The `prelude|interlude|postlude` template itself neither accepts nor forwards
   `heading-level` to its children.

The fix threads the existing in-scope `$heading-level` through both. The level is
passed unchanged (not `+1`) because preludes/postludes are emitted as *siblings*
of the block (outside its element), so their headings belong at the block's own
level.

## Minimal reproducer

```xml
<pretext>
  <article xml:id="repro">
    <title>Minimal hN repro</title>
    <section xml:id="sec">
      <title>Section</title>
      <activity xml:id="act">
        <title>An activity</title>
        <prelude>
          <paragraphs>
            <title>Prelude paragraphs</title>
            <p>Triggers the hN bug.</p>
          </paragraphs>
        </prelude>
        <statement><p>Do it.</p></statement>
      </activity>
    </section>
  </article>
</pretext>
```

`pretext build html` on this fails with the `PTX:BUG` above before the patch, and
builds with `Success!` (0 `PTX:BUG`) after it.

## Heading level is threaded unchanged (not `+1`)

This follows the same shape as #2871 (thread the in-scope `$heading-level`
unchanged), rather than the standalone/fresh-tree variants in #2866 (`select="2"`)
or #2864 (a derived `+1` level), because prelude/postlude content flows inline in
the article and is emitted as a *sibling* of the block (before/after its element),
not nested within it.

Verified against the actual emitted HTML. For an `activity` in a `section`, with a
titled `paragraphs` directly in the section as a baseline:

| element                                   | heading |
|-------------------------------------------|---------|
| `paragraphs` directly in section (baseline) | `h3`  |
| activity title                            | `h3`    |
| **prelude `paragraphs`**                  | **`h3`**|
| `paragraphs` inside activity statement    | `h4`    |
| **postlude `paragraphs`**                 | **`h3`**|

i.e. prelude/postlude headings land at the same level as the activity title and as
sibling section-level content, while genuinely-nested content stays one level
deeper. Passing `+1` would have incorrectly produced `h4`.

## Scope check (neighbouring containers)

To confirm this is the prelude/interlude/postlude family specifically and not a
broader gap, I built the following against an unpatched core. All other
heading-bearing containers that can hold a titled `paragraphs` thread
`heading-level` correctly and build clean:

- division `introduction`/`conclusion` (chapter, section) — clean
- block-level `introduction`/`conclusion` (`activity`, `exercises`) — clean
- `prelude`/`interlude`/`postlude` — **the only family that errors**

`interlude` has no separate application site in `pretext-html.xsl`; it reaches the
same `match="prelude|interlude|postlude"` template, so the three are fixed together
by the one template change here.

## Testing

- Minimal reproducer above: errors before, clean after.
- A real teacher-guide document with many activity preludes/postludes that fully
  failed to build (dozens of `PTX:BUG`): builds cleanly with 0 `PTX:BUG` after the
  patch.

Refs #2851.

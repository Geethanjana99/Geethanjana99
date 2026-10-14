# Validation notes

- Every local README image path resolves to an included file.
- All 63 SVG files parse successfully and contain no text outside their SVG canvas in the local Chromium check.
- Both GIFs contain 40 frames and a four-second repeating animation; transparent corners are preserved.
- No emoji characters occur in the public README.
- Desktop (1280 px viewport) and mobile (390 px viewport) previews show no page-level horizontal overflow.
- All images loaded in both checked viewport layouts.
- All seven in-page navigation links resolve to their section headings in the local preview.
- Four offline statistics tests pass: filtering and deduplication; XML escaping; zero-repository output; preservation of the old card on errors.
- The light-theme preview was also rendered locally.

The profile has not been published to GitHub. These are local browser/asset checks, not a live GitHub rendering guarantee. The optional statistics workflow has not been executed against the account. Project artwork is conceptual, not a product screenshot. The supplied contact and portfolio links were preserved rather than independently verified.

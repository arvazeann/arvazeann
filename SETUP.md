# Setup — arvazeann GitHub Profile

## Files included

- `README.md` — profile layout and dynamic cards.
- `assets/profile-header.svg` — custom dark-futuristic banner.
- `.github/workflows/snake.yml` — generates the contribution snake and publishes it to the `output` branch.

## Install

1. Open your profile repository: `https://github.com/arvazeann/arvazeann`.
2. Upload/replace `README.md` in the repository root.
3. Upload `assets/profile-header.svg`, keeping the `assets` folder.
4. Upload `.github/workflows/snake.yml`, keeping the folder structure.
5. Commit the changes to your default branch (usually `main`).
6. Open the repository's **Actions** tab.
7. If prompted, enable GitHub Actions for the repository.
8. Run **Generate contribution snake** using **Run workflow**, or wait for the scheduled run.
9. After the workflow succeeds, the `output` branch should contain the two generated SVG files.

The README references the dark snake at:

`https://raw.githubusercontent.com/arvazeann/arvazeann/output/github-contribution-grid-snake-dark.svg`

## Notes

- The workflow needs repository Actions to be enabled and permission to write repository contents. The workflow declares `contents: write`.
- The first snake image may not appear until the first workflow run succeeds.
- The typing animation, GitHub stats, streak card, activity graph, skill icons, and footer wave use third-party image services. They can occasionally be rate-limited or unavailable.
- GitHub README supports Markdown and a limited subset of HTML; it does not run arbitrary JavaScript/CSS. The motion is delivered as animated SVG/image services and GitHub Actions-generated assets.
- Statistics reflect public GitHub data and may be delayed or incomplete. Top-language cards describe repository language distribution, not skill level.
- If your default branch is not `main`, edit the `push.branches` entry in `.github/workflows/snake.yml`.
- The profile README appears only when the repository is public, named exactly `arvazeann`, and contains a non-empty `README.md` in its root.

## Optional edits

- Replace the portfolio URL if your deployment domain changes.
- Add LinkedIn or other contact links only after confirming the public URLs.
- Keep the "Currently learning" section separate from technologies used in shipped projects.

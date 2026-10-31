# Profile README assets

The profile README uses small local images and one GitHub Actions workflow:

- `assets/hero-terminal.gif` — local looping terminal boot animation.
- `assets/matrix-rain.gif` — local looping matrix rain animation.
- `assets/hero-terminal.svg` and `assets/matrix-rain.svg` — static fallbacks linked below the GIFs.
- `assets/terminal-divider.svg` and `assets/neon-footer.svg` — static green terminal decoration.
- `.github/workflows/snake.yml` — generates light and dark green contribution snake SVGs and publishes them to the `output` branch.
- `scripts/generate_assets.py` — regenerates the local GIF and SVG artwork with Pillow.

## Regenerate the local art

Python 3 and Pillow are required:

```bash
python -m pip install Pillow
python scripts/generate_assets.py
```

The GIFs are generated locally and are under 250 KB each in the current build. No hosted image-generation service is needed.

## Enable the contribution snake

1. Push the repository changes to the default branch (`main`).
2. Ensure GitHub Actions are enabled for the repository.
3. Under **Settings → Actions → General → Workflow permissions**, allow the workflow to write repository contents if the organization or repository policy requires it. The workflow declares `contents: write` and uses `GITHUB_TOKEN`.
4. Open **Actions → Generate contribution snake → Run workflow**, or wait for its daily schedule.
5. After a successful run, the `output` branch contains `github-snake.svg` and `github-snake-dark.svg`, which the README loads from `raw.githubusercontent.com`.

## Rendering notes

- GitHub does not allow profile README CSS or JavaScript to set a full-page background. The dark terminal environment is built from image assets, HTML tables, Markdown, and code blocks.
- GitHub displays GIFs as images, but reduced-motion settings and client behavior can vary. Static SVG fallbacks are linked beside the hero animations.
- The contribution streak comes from `streak-stats.demolab.com`, a third-party service, so it may be temporarily unavailable. The public GitHub Readme Stats endpoint and Activity Graph endpoint returned HTTP errors during the audit and were removed.
- The README includes no live demo links because the deployments could not be verified as reachable during this pass.
- The language and framework list is based on public project source and documentation. IoT, AI, and computer vision are shown only as interests being explored.

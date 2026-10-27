# Mohammad Imran Hossain ? academic portfolio

Static research website hosted on GitHub Pages. No build step is required.

## Pages

- `index.html` and `index_beta.html`: homepage and matching preview.
- `projects.html`: research and academic projects with filters and full-resolution figures.
- `publications.html`: co-authored preprints.
- `education.html`: experience, education, and professional networks.
- `activities.html`: featured academic stories and space for future blog posts and tutorials.
- `research.html`: detailed doctoral workflow and imaging credits.
- `academic.css` and `academic.js`: shared responsive layout, navigation, themes, pagination, and interactions.

## Preview and deployment

Run `python -m http.server 8000` and visit `http://localhost:8000`.
Pushing to `main` triggers `.github/workflows/deploy-pages.yml`.

## Content and validation

Project descriptions use supplied presentations, reports, repository results, and user corrections. Distinctions between training, validation, and test metrics are retained. Featured photographs are user supplied. Published doctoral imaging examples and licenses are documented in `images/research/SOURCES.md` and on the detailed Research page.

Before publication, local page links, anchors, assets, unique IDs, JavaScript syntax, and Git whitespace checks passed. Responsive styles cover phone, tablet, and desktop layouts. Visual browser verification of the latest changes remains pending.

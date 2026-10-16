---
name: course-material-pipeline
description: How course material (DeepLearning.AI, Coursera, university slides) flows into the public roadmap — raw stays private, distilled notes go public
type: project
---

Decided 2026-10-16: `learning/roadmap.md` stays the public hub, synced daily, for which projects we build and what to
learn next. Instead of working through courses module by module, Muse downloads and distills course material
(DeepLearning.AI, Coursera, lecture slides). Agents then connect what was distilled to the roadmap and plan projects
that cover the learning goals. The aim is learning by building, not by doing labs.

- Raw downloads (slides, PDFs, transcripts) never enter this public repo. Keep them outside git or in a private repo.
- Only notes in our own words land in `learning/`. No copied slides, transcripts, or lab code, per the DeepLearning.AI
  terms (personal, non-commercial use only).
- Use only download options a site intentionally offers. Public university course slides (Stanford CS229, CS224N,
  CS336, and similar) are a freely downloadable alternative.

- **Cadence (2026-10-15):** Muse distills one new course a day into `learning/courses/<course>/` via PRs, and adds
  newsletter items worth experimenting with. Bhavya has the main agent review and merge those PRs.
- **Review check before merging Muse PRs:** Muse writes notes with private context (interview targets, prep framing,
  ex-employer platform names). Strip those lines before merging; the course content itself is fine. Merged branch
  commits stay in public history, so scrub on the branch before merge, never after.
- **Projects (2026-10-15):** each project is a new public repo built from the roadmap. Don't keep reusing QASPER or
  its Track A/B plan; pick fresh tasks that fit what was just learned.

**Why:** Watching courses live was slower than learning in live Claude sessions. Bhavya wants a bespoke, fast learning
map with projects as the unit of learning.
**How to apply:** When reviewing distilled course notes from Muse, updating the roadmap, or proposing the next project.
See [[learning-note-workflow]], [[no-employer-trade-secrets]].

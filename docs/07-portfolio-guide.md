# Portfolio and hiring-team guide

## Tell an engineering story

A strong portfolio does not claim that installing tools equals security experience. Show a decision, the constraint, what you implemented, how you tested it, what failed, and what you improved.

Use this structure for each case study:

1. **Problem:** the capability or risk you addressed.
2. **Constraints:** hardware, time, safety, and knowledge limits.
3. **Design:** architecture and tradeoffs considered.
4. **Implementation:** concise, reproducible actions.
5. **Validation:** positive, negative, and recovery tests.
6. **Evidence:** sanitized artifacts tied to claims.
7. **Result:** measurable outcome, limitation, and next step.

## Recommended front page

Keep the README scannable: one topology, five capabilities, current status, start-here path, three featured case studies, and a safety statement. Hiring teams should understand the project in two minutes.

## Evidence rubric

| Level | Evidence quality |
|---|---|
| 0 | Claim only |
| 1 | Screenshot or command with no explanation |
| 2 | Result linked to a stated test and timestamp |
| 3 | Positive and negative test, interpretation, and cleanup |
| 4 | Reproducible test, multiple-source correlation, limitation, and improvement |

Aim for level 3 on routine tasks and level 4 on the three featured case studies.

## Publish

- Sanitized topology and IP plan using lab-only ranges
- Version/date inventory without licenses or serial numbers
- Narrow configuration excerpts with explanation
- Cropped alerts with lab identities and timestamps if appropriate
- Detection logic, test procedure, false-positive notes, and result
- Incident timelines, decisions, lessons, and recovery validation
- Honest backlog and known limitations

## Keep private

- Raw configurations, packet captures, VM exports, and unredacted screenshots
- Passwords, tokens, browser content, keys, cookies, and recovery codes
- Public/home IPs, real hostnames, email addresses, MACs, and device identifiers
- Information about an employer, school, or third-party environment

## Suggested release sequence

1. Create a repository with no raw evidence in its history.
2. Add sanitized documentation and configuration examples.
3. Run repository validation and manually inspect rendered Markdown and every image.
4. Ask someone unfamiliar with the project to follow one procedure.
5. Tag a version such as `v0.1-design`, `v0.2-core-lab`, or `v1.0-90-day-complete`.
6. Link the repository from a concise professional profile post.

Use the status vocabulary consistently: **planned**, **in progress**, **validated**, and **retired**. This prevents accidental exaggeration.

---
id: 4
title: No feature description provided
stage: general
date: 2026-02-08
surface: agent
model: claude-opus-4-6
feature: none
branch: phase-iv-deployment
user: asghar
command: /sp.specify
labels: [error,no-input,specification]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- none
tests:
- none
---

## Prompt

```

```

## Response snapshot

ERROR: No feature description provided

The /sp.specify command requires a feature description to generate a specification. Please provide a description of the feature you'd like to specify, for example:

/sp.specify "Add user authentication to the todo app"
/sp.specify "Implement real-time notifications for task updates"
/sp.specify "Add bulk import/export functionality for tasks"

## Outcome

- ✅ Impact: Identified missing input requirement for specification generation
- 🧪 Tests: none
- 📁 Files: none created
- 🔁 Next prompts: User needs to provide feature description for /sp.specify command
- 🧠 Reflection: The command requires input to generate meaningful specifications

## Evaluation notes (flywheel)

- Failure modes observed: Missing required feature description input
- Graders run and results (PASS/FAIL): NA - command cannot proceed without input
- Prompt variant (if applicable): /sp.specify without arguments
- Next experiment (smallest change to try): User should provide a feature description with the command
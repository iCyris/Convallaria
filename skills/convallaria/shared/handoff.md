# Shared Delivery Protocol

Use this reference when any Convallaria workflow produces multiple files or needs to be handed to another designer, engineer, or agent.

This is not a user-routed subskill. It is a shared delivery protocol for manifests, source-of-truth notes, validation, and practical handoff writing.

## Package Shape

```text
convallaria-output/
├── BRAND.md
├── DESIGN.md
├── LOGO_SPEC.md
├── DESIGN_QA.md
├── asset-manifest.json
├── tokens/
├── logo/
├── images/
├── screenshots/
└── handoff/
    ├── developer-handoff.md
    └── ai-agent-prompt.md
```

Only include files that exist and are relevant to the task.

## Manifest

Use `shared/templates/asset-manifest.json` as the base. The manifest should record:

- project metadata
- source inputs and their role
- generated outputs
- producer subskill or script
- assumptions
- unresolved decisions
- recommended next actions

Validate a manifest from the parent `skills/convallaria/` directory with:

```bash
python3 shared/scripts/validate_outputs.py asset-manifest.json
```

## Handoff Writing

A good handoff explains:

- what was produced
- what is the source of truth
- how to use the assets
- what should not be changed casually
- what remains open
- which files another agent should read first

Keep handoff writing practical and production-facing.

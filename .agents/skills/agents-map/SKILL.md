---
name: agents-map
description: Rebuild the AGENTS.md map in .agents/map/, a generated graph of every AGENTS.md and the files its related_files header lists. Use after an AGENTS.md is added, removed or revised, and only once a human has explicitly agreed to the rebuild.
---

# AGENTS.md map

`.agents/map/` holds a generated picture of the repository: every AGENTS.md, the
AGENTS.md files it links to, and the files its `related_files` header lists.
`.github/scripts/build_agents_map.py` builds it mechanically from those headers:

- `.agents/map/MAP.md`: Mermaid diagrams (GitHub renders them), plus the paths
  that more than one AGENTS.md lists.
- `.agents/map/graph.json`: the same graph for tools.

## Ask first

Rebuilding the map is opt-in. Don't run the script on your own initiative, from
CI, or as a side effect of another task.

1. When you add, remove or revise an AGENTS.md, finish that change, then ask the
   human whether to rebuild `.agents/map/`.
2. Run the script only after an explicit yes in the current conversation.
   Silence, or approval of a different step, is not a yes.

## Rebuild

1. Check the headers: `python .github/scripts/check_agents_md.py`. Fix errors
   first, because the map shows whatever the headers say.
2. See whether the map is stale: `python .github/scripts/build_agents_map.py --check`.
3. Rebuild it: `python .github/scripts/build_agents_map.py`.
4. Read `git diff .agents/map/` and tell the human what changed: AGENTS.md files
   added or removed, paths added or removed, and paths marked missing.
5. If the human wants it committed, commit the map together with the AGENTS.md
   change that caused it.

Don't edit the files in `.agents/map/` by hand; rebuild them. The map reads only
`related_files`, so fix a wrong map by fixing that header.

"""
Exercise 4 — Answers
====================
Fill this in after running exercise4_mcp_client.py.
"""

# ── Basic results ──────────────────────────────────────────────────────────

# Tool names as shown in "Discovered N tools" output.
TOOLS_DISCOVERED = ["search_venues", "get_venue_details"]

QUERY_1_VENUE_NAME    = "The Haymarket Vaults"
QUERY_1_VENUE_ADDRESS = "1 Dalry Road, Edinburgh"
QUERY_2_FINAL_ANSWER  = "No venues in the known Edinburgh list can accommodate 300 guests with vegan options. The search returned zero matches (count: 0). The agent correctly reported the constraint cannot be satisfied rather than hallucinating a venue."

# ── The experiment ─────────────────────────────────────────────────────────
# Required: modify venue_server.py, rerun, revert.

EX4_EXPERIMENT_DONE = True   # True or False

# What changed, and which files did or didn't need updating? Min 30 words.
EX4_EXPERIMENT_RESULT = """
Changing The Albanach's status from 'available' to 'full' in mcp_venue_server.py caused it to drop out of the Query 1 search results immediately: the baseline returned count=2 (The Albanach and The Haymarket Vaults), the experiment returned count=1 (The Haymarket Vaults only). The agent's final answer changed accordingly — it reported only The Haymarket Vaults. Query 2 was unaffected (still count=0, no venue holds 300). exercise4_mcp_client.py was not touched at any point: the client discovers tools and data dynamically on every connection, so a server-side data change is reflected in the next run with zero client code changes.
"""

# ── MCP vs hardcoded ───────────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 9   # count in exercise2_langgraph.py (tool imports + names in task_d)
LINES_OF_TOOL_CODE_EX4 = 49  # count in exercise4_mcp_client.py (_make_mcp_caller + discover_tools)

# What does MCP buy you beyond "the tools are in a separate file"? Min 30 words.
MCP_VALUE_PROPOSITION = """
MCP gives you runtime tool discovery over a transport boundary: the client has no knowledge of what tools exist until it connects and calls list_tools(). This means any MCP-compatible client — the LangGraph agent, a Rasa action server, a different language entirely — can connect to the same server and get the same tools without sharing code. Adding a new tool to mcp_venue_server.py is immediately available to every client on the next connection, with no redeploy or code change on any client. That is the key difference from "tools in a separate file": a separate file is still compiled into the client; an MCP server is a live service boundary.
"""

# ── PyNanoClaw architecture — SPECULATION QUESTION ─────────────────────────
#
# (The variable below is still called WEEK_5_ARCHITECTURE because the
# grader reads that exact name. Don't rename it — but read the updated
# prompt: the question is now about PyNanoClaw, the hybrid system the
# final assignment will have you build.)
#
# This is a forward-looking, speculative question. You have NOT yet seen
# the material that covers the planner/executor split, memory, or the
# handoff bridge in detail — that is what the final assignment (releases
# 2026-04-18) is for. The point of asking it here is to check that you
# have read PROGRESS.md and can imagine how the Week 1 pieces grow into
# PyNanoClaw.
#
# Read PROGRESS.md in the repo root. Then write at least 5 bullet points
# describing PyNanoClaw as you imagine it at final-assignment scale.
#
# Each bullet should:
#   - Name a component (e.g. "Planner", "Memory store", "Handoff bridge",
#     "Rasa MCP gateway")
#   - Say in one clause what that component does and which half of
#     PyNanoClaw it lives in (the autonomous loop, the structured agent,
#     or the shared layer between them)
#
# You are not being graded on getting the "right" architecture — there
# isn't one right answer. You are being graded on whether your description
# is coherent and whether you have thought about which Week 1 file becomes
# which PyNanoClaw component.
#
# Example of the level of detail we want:
#   - The Planner is a strong-reasoning model (e.g. Nemotron-3-Super or
#     Qwen3-Next-Thinking) that takes the raw task and produces an ordered
#     list of subgoals. It lives upstream of the ReAct loop in the
#     autonomous-loop half of PyNanoClaw, so the Executor never sees an
#     ambiguous task.

WEEK_5_ARCHITECTURE = """
- The Planner (pynanoclaw/agents/planner.py) is a strong-reasoning model that decomposes Rod's raw WhatsApp message into an ordered list of subgoals before any tools are called. It sits upstream of the ReAct loop in the autonomous-loop half, so the Executor never starts with an ambiguous task.

- The Executor (sovereign_agent/agents/research_agent.py, extended) is the ReAct loop from Week 1 grown with web search and file operations. It lives in the autonomous-loop half and works through the Planner's subgoals one by one, calling MCP tools and deciding when to hand off to the structured agent.

- The Shared MCP Tool Server (sovereign_agent/tools/mcp_venue_server.py, extended) is the single tool endpoint that both halves connect to. It lives in the shared layer and grows to cover venue search, live web search, calendar access, and email — neither half embeds tool implementations, they both discover them dynamically at runtime.

- The Handoff Bridge (pynanoclaw/bridge/handoff.py) is a tool available to the Executor that routes a task to the Rasa structured agent when a human-facing conversation is needed (e.g. confirming a deposit with the pub manager). It lives in the shared layer and routes the response back to the loop once the conversation is complete.

- The Structured Confirmation Agent (exercise3_rasa/, extended) is the Rasa CALM agent from Week 1 wired to the shared MCP server and augmented with a RAG knowledge base. It lives in the structured-agent half and handles the pub manager call with explicit, auditable flows and business-rule guards that the autonomous loop must never improvise around.

- The Persistent Memory Store (pynanoclaw/memory/persistent_store.py) is a filesystem-backed store shared between both halves. It holds venue candidates found by the loop, booking state, and prior conversation turns so that if the structured agent hands back to the loop mid-task, the Executor does not start from scratch.

- The Observability Layer (pynanoclaw/observability/) wraps both halves with tracing, cost tracking, and guardrails. It lives in the shared layer and is the component that makes PyNanoClaw auditable enough to let it act autonomously on Rod's behalf.
"""

# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
The LangGraph ReAct loop belongs on the research half and Rasa CALM belongs on the confirmation call. The reason swapping feels wrong is grounded in what we actually observed in the runs.

In Exercise 2 Task A, the LangGraph agent issued both check_pub_availability calls in a single parallel turn before seeing any results — it improvised an efficient batching strategy the prompt never asked for. That flexibility is exactly what you need for research: the space of "which pub, given these constraints, right now" cannot be scripted in advance. In Task C Scenario 1, it pivoted silently from The Bow Bar to The Albanach with no explicit instruction to do so. That is emergent reasoning, and it is valuable.

But those same properties are dangerous on the confirmation call. If the LangGraph agent is talking to the pub manager about a deposit, it might improvise a price, skip a business-rule check, or commit to terms Rod never approved — just as fluidly as it batched two tool calls. There is no flow it is required to follow.

Rasa CALM in Exercise 3 is the opposite: every path through the confirmation dialogue is an explicit named flow. The LLM picks the flow, but the steps are fixed. That predictability is exactly wrong for research (you cannot pre-script every fallback venue combination) but exactly right for a high-stakes phone call where auditability and rule enforcement matter more than flexibility.
"""

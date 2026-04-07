"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.

CALM vs Old Rasa — what changed
---------------------------------
The old open-source Rasa approach used:
  - nlu.yml: intent training examples
  - rules.yml: explicit dialogue rules
  - FormValidationAction: Python class to parse slot values

Rasa Pro CALM uses:
  - flows.yml: natural language descriptions of what each flow does
  - from_llm slots: the LLM extracts values from conversation
  - ONE custom action: ActionValidateBooking for the business rules

The conversation is the same from the manager's perspective.
The machinery underneath is completely different.

CONVERSATION SCRIPTS
---------------------
Conversation 1 (happy path):
  You:    calling to confirm a booking
  Agent:  [asks guest count]
  You:    160 guests
  Agent:  [asks vegan count]
  You:    about 50 need vegan
  Agent:  [asks deposit]
  You:    £200 deposit
  Agent:  [confirms or escalates?]

Conversation 2 (deposit too high):
  Same as above but use a deposit above £300 (e.g. "£500 deposit").

Conversation 3 (out of scope):
  Start normally, then when asked for vegan count say something like
  "can you arrange parking for the speakers?" and observe what happens.
  Does CALM handle this differently than the old rules approach?
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────

CONVERSATION_1_TRACE = """
Your input ->  calling to confirm a booking
How many guests are you confirming for tonight's event?
Your input ->  160
And how many of those guests will need vegan meals?
Your input ->  50  
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  200                                                                                                                                            
Thank you — booking confirmed. 160 guests, 50 requiring vegan meals, £200 deposit accepted. I'll send written confirmation to the organiser shortly.
Is there anything else I can help you with?
"""

CONVERSATION_1_OUTCOME = "confirmed"   # "confirmed" or "escalated"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
Your input ->   calling to confirm a booking                                                                                                                  
How many guests are you confirming for tonight's event?
Your input ->  160                                                                                                                                            
And how many of those guests will need vegan meals?
Your input ->  50                                                                                                                                             
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  400                                                                                                                                            
I need to check one thing with the organiser before I can confirm. The issue is: a deposit of £400 exceeds the organiser's authorised limit of £300. Can I call you back within 15 minutes?
Is there anything else I can help you with?
"""

CONVERSATION_2_OUTCOME = "escalated"   # "confirmed" or "escalated"
CONVERSATION_2_REASON  = "a deposit of £400 exceeds the organiser's authorised limit of £300"

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
Your input ->  calling to confirm a booking
How many guests are you confirming for tonight's event?
Your input ->  160
And how many of those guests will need vegan meals?
Your input ->  do you have parking available?                                                                                                                 
I'm sorry, I'm not trained to help with that.
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Would you like to continue with confirm booking?
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
CALM triggered the handle_out_of_scope flow, replied that it cannot help with parking, and offered to return to the booking confirmation flow without losing the collected slots.
"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
Rasa CALM handled the out-of-scope request much cleaner and explicit: it triggered a dedicated handle_out_of_scope flow, gave a clear refusal with a reason, and offered to resume the booking. LangGraph in Scenario 3 responded with weak "lacking necessary details" message that did not explain it was out of scope and gave no useful guidance.
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = True   # True or False

# List every file you changed.
TASK_B_FILES_CHANGED = ["exercise3_rasa/actions/actions.py"]

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
Temporarily changed the condition to `if True:` to force the cutoff guard to always trigger, ran a booking conversation, and verified the agent escalated with the correct deadline message. Then reverted to the real time-based condition.
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

CALM_VS_OLD_RASA = """
"""

# ── The setup cost ─────────────────────────────────────────────────────────

SETUP_COST_VALUE = """
Setup provides guaranteed, auditable behavior, which is something that we expect from the prod systems.
"""
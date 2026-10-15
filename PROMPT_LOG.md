# Complete AI Prompt Log and Differentiation Design

## Prompt 1 — System instruction (used for every generation)
The **exact** full system instruction is in `prompts.py` under `SYSTEM_PROMPT`. It specifies the required JSON keys, positive integer sides, exact Pythagorean identity, difficulty criteria, hints, explanation, and repetition avoidance. The app passes it to Gemini as `system_instruction`.

## Prompt 2 — Dynamic user prompt (used for every generation)
```text
Generate ONE NEW {level} Pythagorean theorem problem.
Previous triple+unknown signatures (avoid when possible): {previous[-20:]}
Use level-appropriate language and numerical difficulty. Return only the JSON object.
```
Here `{level}` is the learner-selected level and `{previous[-20:]}` is the last 20 task signatures. The code substitutes these at runtime.

## Prompt 3 — Hint refinement (design template; NOT called separately by the app)
```text
For this verified Grade 8 Pythagorean theorem task, write one additional hint, not the final answer. Focus on the learner's selected difficulty. Be concise and age-appropriate. Return plain text, maximum 35 words.
```
The app instead obtains one hint as part of Prompt 1's JSON, avoiding an extra API call.

## Prompt 4 — Feedback refinement (design template; NOT called separately by the app)
```text
Provide constructive feedback for a Grade 8 learner solving a verified right-triangle problem. Do not claim an incorrect answer is correct. Refer to the correct formula and suggest the next step. Return plain text, maximum 45 words.
```
The deployed app uses deterministic feedback and independent numeric checking instead, to avoid AI falsely marking an answer correct.

## Level-specific guidance
| Level | Unknown | Complexity | Scaffolding |
|---|---|---|---|
| Foundation | Hypotenuse c | Small triples, direct triangle | Identify legs, add squares |
| Standard | Leg a or b | Moderate triples | Rearrange formula, subtract squares |
| Advanced | Leg a or b | Larger triples, richer context | Identify hypotenuse, multi-step arithmetic |

## Validation and iteration
1. Start with a general Pythagorean problem request.
2. Add exact JSON schema to enable reliable parsing.
3. Add level constraints so Foundation is meaningfully easier than Standard/Advanced.
4. Require integer triples to avoid rounding and ambiguous answers.
5. Add a history list to discourage repetition.
6. Validate each response in Python and retry invalid results.
7. Render the actual question and solution from verified numbers, not from unchecked AI prose.

These are **design refinements**, not a claim of a documented historical multi-run experiment. Run and record actual examples/screenshots after deployment.

## Manual QA checklist
- [ ] Foundation generates a correct missing-hypotenuse problem
- [ ] Standard generates a correct missing-leg problem
- [ ] Advanced generates a correct larger missing-leg problem
- [ ] Hint appears and does not reveal the answer
- [ ] Solution steps and numeric answer are correct
- [ ] Correct answer is accepted, incorrect answer is rejected
- [ ] New Problem requests new AI output in Gemini mode
- [ ] No API key appears in public GitHub
- [ ] Deployed URL works on another device

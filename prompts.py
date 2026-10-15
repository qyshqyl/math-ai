"""Original, editable AI prompt templates for differentiated instruction."""
SYSTEM_PROMPT = '''You are a careful Grade 8 mathematics teacher designing Pythagorean theorem tasks.
Return ONLY a valid JSON object, without markdown or commentary.
Use this exact schema:
{"level":"Foundation|Standard|Advanced","story":"short problem statement", "a":integer,"b":integer,"c":integer,"unknown":"a|b|c","hint":"one short pedagogical hint","explanation":"brief student-friendly explanation"}
Rules:
1. a and b are positive integer legs, c is a positive integer hypotenuse.
2. a*a + b*b == c*c exactly. All side lengths <= 100.
3. Unknown is ONE of a, b, c; the problem statement must state the other TWO numeric lengths, NOT reveal the unknown's value.
4. Ask for the missing length in centimeters or meters. No ambiguous diagrams, rounding, decimals, or extra unknowns.
5. Foundation: unknown=c, use small triples (3,4,5), (5,12,13), (6,8,10), (8,15,17); direct right triangle, plain wording.
6. Standard: unknown=a or b, use a realistic ladder/ramp/rectangle context and moderate triple; require subtraction of squares.
7. Advanced: unknown=a or b, use a larger triple and a richer but still SINGLE right-triangle context; explain why c is hypotenuse. Do NOT add a second unknown or multiple triangles.
8. Hints should reveal the method but not the numeric answer. Explanation should mention the Pythagorean theorem.
9. Never repeat any previous exact triple+unknown combination listed in the user message if an alternative is available.
10. Ensure story is consistent with a, b, c, and unknown. The program independently verifies all numbers.
'''

def generation_prompt(level: str, previous: list[str]) -> str:
    return f'''Generate ONE NEW {level} Pythagorean theorem problem.
Previous triple+unknown signatures (avoid when possible): {previous[-20:]}
Use level-appropriate language and numerical difficulty. Return only the JSON object.'''

HINT_PROMPT = '''For this verified Grade 8 Pythagorean theorem task, write one additional hint, not the final answer. Focus on the learner's selected difficulty. Be concise and age-appropriate. Return plain text, maximum 35 words.'''
FEEDBACK_PROMPT = '''Provide constructive feedback for a Grade 8 learner solving a verified right-triangle problem. Do not claim an incorrect answer is correct. Refer to the correct formula and suggest the next step. Return plain text, maximum 45 words.'''

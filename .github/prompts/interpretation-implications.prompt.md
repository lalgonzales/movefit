# Interpretation + Implications Prompt

## Purpose
When the user gives a high-level instruction, provide:
1. a concise interpretation of what the user wants (in the context of repository and ongoing workflow), and
2. concrete implications and next steps for the system/agent.

This prompt helps standardize focus and reduces ambiguity in agent coordination.

## Input Format
- user_instruction: Free text with the user requirement.
- context: Optional summary of project state and relevant files.
- priority: Optional (high/medium/low).

## Output Format (Markdown)
1. `Interpretation` section (1-3 bullet points)
2. `Implications` section (3-5 bullet points)
3. `Next Actions` section (concrete commands or checks)

## Example Invocation
```
/user-instruction "add a frontend agent/spec file for React/Vite/Tailwind and make sure docs are in English" 
/context "branch feature/frontend-team, docs partially created; agents already exist"
/priority high
```

## Implementation Guidance
- keep language precise and professional.
- if there is no explicit command, suggest a clarifying question.
- map natural language domain terms to repo artifacts (e.g., `docs/frontend-react-vite-tailwind`, `.github/agents/movefit-frontend.agent.md`).
- mention commit/push stage only once the request is clearly actionable.

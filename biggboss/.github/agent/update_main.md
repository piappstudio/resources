You are a software engineer updating a JSON configuration file.

File to update:
json/shows/tamil/season9/main.json

Agent to use:
biggboss_ai

Login Credential: test@test.com / Apple@2024
Task:
- Use the biggboss_ai agent to fetch participant details for showId = 4
- Update ONLY the following keys in the JSON:
  - participants
  - category

Rules:
- Replace the entire value of `participants` and `category` with the data returned by biggboss_ai
- Do NOT modify any other keys, values, structure, or formatting
- Preserve key order and indentation
- Do NOT add or remove fields
- Do NOT add comments or metadata

Constraints:
- Treat biggboss_ai as the single source of truth
- If data is unavailable, leave the existing values unchanged

Output:
- Return the updated main.json with only `participants` and `category` changed

---
name: Generate BiggBoss SQL Queries
description: Guidelines and dynamic workflows to generate valid SQL INSERT queries for tasks and notes database tables by referencing active shows.json and main.json.
---

# Generate BiggBoss SQL Queries

This skill provides standard guidelines, schemas, and a dynamic lookup workflow to generate SQL `INSERT` statements for the `tasks` and `notes` database tables. Rather than hardcoding IDs, values are dynamically resolved by inspecting [shows.json](file:///Users/apple/AndroidStudioProjects/resources/biggboss/json/shows.json) and the show's `main.json` file.

---

## 1. Dynamic Data Lookup Workflow

When generating SQL queries for any Bigg Boss event or task, follow these steps to retrieve parameter values dynamically:

### Step 1: Identify Active Show & `show_id`
1. Read [shows.json](file:///Users/apple/AndroidStudioProjects/resources/biggboss/json/shows.json) and find active shows where `"end_date": null`.
2. Extract the show's `"id"` as **`show_id`** (e.g., `"5"` for Hindi Season 20, `"6"` for Tamil Season 10, `"7"` for Telugu Season 10).
3. Locate the show's local `main.json` file path specified in `"more_info"` (e.g., `biggboss/json/shows/tamil/season10/main.json`).

### Step 2: Dynamically Resolve Participant ID (`part_id` / `participants` / `winner`)
1. Open the target show's `main.json` file.
2. Search the `"participants"` array for the contestant name (using exact or case-insensitive partial name matching).
3. Extract the contestant's `"id"`:
   - For the **`notes`** table: Use integer `part_id`.
   - For the **`tasks`** table: Use string `'participants'` and `'winner'`.

### Step 3: Dynamically Resolve Category ID (`category_id`)
1. Match the category key for the event/task (e.g. `TTFBU` for Ticket to Finale Build Up, `NOM` for Nomination, `EVI` for Eviction, `Captain` for Captaincy, `WPW` for Worst Performer, `BPW` for Best Performer).
2. Look up the corresponding `category_id` in the show's category definitions or main data schema.

### Step 4: Dynamically Resolve Week Number (`week`)
1. Calculate the week number dynamically based on the event date relative to `"start_date"` in `shows.json`:
   $$\text{week} = \left\lfloor \frac{\text{event\_date} - \text{start\_date}}{7} \right\rfloor + 1$$
2. Alternatively, verify the current week from the latest entry in `votes.json`, `timeline.json`, or history in `main.json`.

---

## 2. Table Schemas & Query Templates

### A. `tasks` Table Schema

The `tasks` table records main task titles, contestant sub-tasks, participant IDs, and performance comments.

```sql
INSERT INTO `tasks` (
    `date`, 
    `week`, 
    `show_id`, 
    `main_task`, 
    `sub_task`, 
    `participants`, 
    `winner`, 
    `comments`, 
    `created_at`, 
    `updated_at`, 
    `is_housemate_vote`
) VALUES (
    'YYYY-MM-DD',         -- date (Event date)
    <WEEK_NUM>,           -- week (Dynamically resolved week number)
    <SHOW_ID>,            -- show_id (Dynamically resolved from shows.json)
    '<MAIN_TASK_TITLE>',  -- main_task (e.g. 'TTF Build Up Week Task 2')
    '<SUB_TASK_NAME>',    -- sub_task (format: '{Contestant Name}-{Task Name}')
    '<PARTICIPANT_ID>',   -- participants (Dynamically resolved string part_id)
    '<WINNER_ID>',        -- winner (Dynamically resolved string part_id or winner ID)
    '<COMMENTS>',         -- comments (Escaped string text)
    'YYYY-MM-DD 04:00:00',-- created_at
    'YYYY-MM-DD 04:00:00',-- updated_at
    0                     -- is_housemate_vote (0 or 1)
);
```

#### Field Formatting Guidelines:
- **`sub_task`**: Format as `'{Contestant Name}-{Task Name}'` (e.g. `'Mukesh-Kadavul Paathi, Mirugam Paathi'`).
- **`comments`**: Text describing performance or breakdown. Escaping rule: replace single quotes `'` with doubled single quotes `''` (e.g., `Mukesh''s`).

---

### B. `notes` Table Schema

The `notes` table stores category-specific ratings, scores, and points for individual participants.

```sql
INSERT INTO `notes` (
    `show_id`, 
    `part_id`, 
    `category_id`, 
    `week`, 
    `date`, 
    `value`, 
    `comments`, 
    `created_at`, 
    `updated_at`
) VALUES (
    <SHOW_ID>,             -- show_id (Dynamically resolved integer)
    <PARTICIPANT_ID>,      -- part_id (Dynamically resolved integer participant id)
    <CATEGORY_ID>,         -- category_id (Dynamically resolved category id)
    <WEEK_NUM>,            -- week (Dynamically resolved integer week)
    'YYYY-MM-DD',          -- date
    <SCORE_VALUE>,         -- value (Numeric score or points)
    '<SCORE_BREAKDOWN>',   -- comments (Detailed breakdown or ratings text)
    'YYYY-MM-DD 04:00:00', -- created_at
    'YYYY-MM-DD 04:00:00'  -- updated_at
);
```

---

## 3. SQL Formatting Rules

1. **String Literals**: Always wrap string values in single quotes `'...'` (e.g. `'2026-11-18'`). Never wrap string values in backticks `` ` ``.
2. **Escaping Single Quotes**: Any single quote inside a text string (e.g., `Mukesh's`, `Shathiga's`, `Task 'Bus Rescue'`) **must** be escaped by doubling it (`''`):
   - Correct: `'As call receiver, Mukesh''s declared order failed'`
   - Incorrect: `` `As call receiver, Mukesh's declared order failed` ``
3. **Identifiers**: Table names and column names use backticks `` ` `` (e.g. ``INSERT INTO `tasks` (`date`, `week`)``).
4. **Timestamps**: `created_at` and `updated_at` use the format `'YYYY-MM-DD HH:MM:SS'`.

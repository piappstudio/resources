---
name: BiggBoss-Reporting
description: Orchestrates the generation of visual dashboards and detailed performance reports for Bigg Boss contestants using project data and MCP tools.
---

# BiggBoss-Reporting

This skill automates the creation of visual insights for Bigg Boss (Tamil, Telugu, Hindi). It leverages local JSON data, MCP tools, and HTML templates to generate shareable reports.

## 1. Show Configurations
Use these verified endpoints for vote scraping updates:

| Show          | Language | Data Path                              | Shod ID |
|:--------------|:---------|:---------------------------------------|---------|
| **Season 10** | Tamil    | `biggboss/json/shows/tamil/season10/`  | 6       |
| **Season 10** | Telugu   | `biggboss/json/shows/telugu/season10/` | 7       |
| **Season 20** | Hindi    | `biggboss/json/shows/hindi/season20/`  | 5       |

## Data identification
- Use configured json to identify the contestant id or associated with should id
- Use MCP only to pull `nominations`, `tasks`, `notes`


## 2. Core Reporting Workflows

### A. Voting Dashboard (`voting_dashboard.html`)
*   **Purpose**: Real-time leadership tracking and trend visualization.
*   **Data Inputs**: `votes.json` (weekly standings) and `main.json` (participant IDs/metadata).
*   **Requirements**:
    *   Highlight **Top 3** leaders with 130px avatars and gold borders.
    *   Display **Bottom 3** in a list with 60px avatars and danger indicators (red bars).
    *   Calculate `width` of bars based on the leader's vote share.

### B. Eviction Report (`eviction_report.html`)
*   **Purpose**: A deep-dive wrap-up of an evicted contestant's journey.
*   **Data Inputs**:
    *   **Contestant Info**: `main.json` (History, Categories).
    *   **Tasks**: Use `tasks` API/MCP to sum up participation vs. wins.
    *   **Social**: Use `nominations` API/MCP to extract who nominated them and why.
    *   **Public Impact**: `trends.json` (Promo counts/scores) and `votes.json` (Average weekly support).
*   **Visuals**: Apply the **"Modern Professional"** (Indigo/Slate) theme and add the `EVICTED` stamp over the profile picture.

## 3. Data Extraction Guide
1.  **MCP Integration**: Use `biggboss_mcp` tools (if available) to fetch aggregated stats for tasks and nominations.
2.  **Trends Analysis**: Map participant `id` from `main.json` to the `promo` array in `trends.json` to calculate visibility scores.

## 4. Generation & Export
1.  **Template Update**: Read the target HTML template and surgically replace placeholders with the gathered data.
2.  **Rendering**: Use the `render_compose_preview` or relevant IDE preview tool to verify the visual state.
3.  **Capture**: Utilize the built-in **Export** button (powered by `html2canvas`) to save the report as a high-quality PNG.

---
> [!IMPORTANT]
> Always ensure image URLs use the absolute GitHub raw path:
> `https://raw.githubusercontent.com/piappstudio/resources/main/biggboss/images/shows/<lang>/<season>/participants/<id>.png`

---
name: Update BiggBoss Voting
description: Scrapes Bigg Boss voting results from unofficial sites and updates the project's JSON data.
---

# Update BiggBoss Voting

This skill automates the process of scraping Bigg Boss unofficial voting results and updating the project's JSON database.

## 1. Show Configuration
The skill uses the following predefined configurations for the current shows:

| Show | URL | Result Button |
| :--- | :--- | :--- |
| **BiggBoss-Tamil-Season-10** | `https://tamilglitz.in/bigg-boss-tamil-vote/` | `View Results` |
| **BiggBoss-Telugu-Season-10** | `https://biggbossvotingtelugu.in/` | `Show results` |

## 2. Weekly Monitoring
1.  **Date Analysis**: The skill reads `start_date` from [shows.json](file:///Users/apple/StudioProjects/resources/biggboss/json/shows.json) to estimate the current week.
2.  **User Prompt**: It prompts the user to confirm the current week (Week 1 to Week 15).

## 3. Scraping Process
1.  **Dependency Setup**: Ensure the environment has the required packages.
    ```bash
    pip install -r requirements.txt
    ```
2.  **Script Execution**: Locate the show's `main.json` file and run the bundled Selenium script. Pass the file path to `--main_json` to automatically extract participant names for partial name matching.
    ```bash
    python3 scripts/scrape_votes.py "<URL>" "<BUTTON_TEXT>" --main_json "biggboss/json/shows/<lang>/<season>/main.json"
    ```
3.  **Smart Matching**: The script reads names from `main.json`, searches for them (case-insensitive) on the results page, and extracts the surrounding text (votes/percentages). This handles cases where the website uses full names (e.g., "Charan Mahadev") while the local data uses short names (e.g., "Charan").
4.  **Capture**: Extracts mapped contestant data from the resulting DOM.

## 4. Data Mapping & Persistence
1.  **Contestant Identification**: Matches scraped names with `id` values from the show's `main.json` file.
2.  **JSON Update**: Updates the respective `votes.json` file on a weekly basis, referencing the format from previous seasons.

---
*For technical implementation details, refer to the [implementation_plan.artifact.md](file:///Users/apple/Library/Caches/Google/AndroidStudio2026.1.4/projects/resources.d1f14231/.artifacts/6df70476-76ec-42ee-a5b5-ba9b8d4bdea6/implementation_plan.artifact.md).*


# Instruction: Update Tamil Trends Data

As an analytics engineer, follow these steps to update `json/shows/tamil/season9/trends.json`:

1. **Analyze Current Trends Data**
     - Open `json/shows/tamil/season9/trends.json`.
     - In the `"Vijay TV Promos"` section, under `items`, find the most recent "X" (Twitter) post by checking the latest `created_at` date.

2. **Prepare for Data Update**
     - Open a terminal and navigate to:  
         `/Users/apple/StudioProjects/biggboss_prod`
     - Open `scripts/biggboss_json.sh`.
     - Update the `start_date` variable in this script to be one day after the latest `created_at` date found in step 1.

3. **Run Data Collection Script**
     - Activate the Python virtual environment:
         ```
         source ~/Documents/Projects/biggboss/AI/venv/bin/activate
         ```
     - Run the data collection script:
         ```
         python scripts/biggboss_json.sh
         ```
     - If you encounter an "X" (Twitter) system error, try a different `BEARER_TOKEN`:
         - In `biggboss_json.sh`, comment out the current token and uncomment another available token.

4. **Update Trends Data**
     - If the script runs successfully, locate the output JSON file.
     - Replace the entire `items` section in `scripts/ai/promo/shows/tamil/season9/trends.json` with the new data from the output file.

5. **Run Face Recognition Analysis**
     - Deactivate the current Python environment:
         ```
         deactivate
         ```
     - Activate the new virtual environment:
         ```
         source venv/bin/activate
         ```
     - Run the face recognition analysis:
         ```
         python scripts/ai/claude_ai.py --show-path promo/shows/tamil/season9 --max-seconds 25
         ```
     - Wait for the process to finish. The output will be in `scripts/ai/promo/shows/tamil/season9/trends_updated.json`.

6. **Finalize Trends Update**
     - Copy the entire `items` section from `trends_updated.json`.
     - Update the `items` section in `json/shows/tamil/season9/trends.json` with this new data.
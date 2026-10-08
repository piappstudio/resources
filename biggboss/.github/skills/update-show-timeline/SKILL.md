---
name: Update Show Timeline
description: Scrapes and updates daily show timelines for running Bigg Boss seasons using Wikipedia, official X handles, and web sources since the last recorded date in timeline.json.
---

# Update Show Timeline

This skill automates tracking and updating daily timeline events (`timeline.json`) for active running Bigg Boss seasons (Tamil, Telugu, Hindi). It identifies events since the last recorded date in `timeline.json` using Wikipedia, official X handles, and streaming platform updates.

---

## 1. Active Show Configurations & Sources

Active shows are dynamically identified from [shows.json](file:///Users/apple/AndroidStudioProjects/resources/biggboss/json/shows.json) where `"end_date": null`.

| Show Name                     | Language / Season | Data Directory                         | Wikipedia Link                                                                                 | Official X Handles                  | Hashtags            |
|:------------------------------|:------------------|:---------------------------------------|:-----------------------------------------------------------------------------------------------|:------------------------------------|:--------------------|
| **BiggBoss Tamil Season 10**  | `tamil/season10`  | `biggboss/json/shows/tamil/season10/`  | [BB Tamil 10 Wikipedia](https://en.wikipedia.org/wiki/Bigg_Boss_(Tamil_TV_series)_season_10)   | `@VijayTelevision`, `@DisneyPlusHS` | `#BiggBossTamil10`  |
| **BiggBoss Telugu Season 10** | `telugu/season10` | `biggboss/json/shows/telugu/season10/` | [BB Telugu 10 Wikipedia](https://en.wikipedia.org/wiki/Bigg_Boss_(Telugu_TV_series)_season_10) | `@StarMaa`, `@DisneyPlusHSTel`      | `#BiggBossTelugu10` |
| **BiggBoss Hindi Season 20**  | `hindi/season20`  | `biggboss/json/shows/hindi/season20/`  | [BB Hindi 20 Wikipedia](https://en.wikipedia.org/wiki/Bigg_Boss_(Hindi_TV_series)_season_20)   | `@ColorsTV`, `@JioCinema`           | `#BiggBoss20`       |

---

## 2. Step-by-Step Update Workflow

### Step 1: Identify Active Shows & Last Recorded Date
1. Open [shows.json](file:///Users/apple/AndroidStudioProjects/resources/biggboss/json/shows.json) and locate shows where `"end_date": null`.
2. For each active show, open its `timeline.json` (e.g., `biggboss/json/shows/tamil/season10/timeline.json`).
3. Inspect the top entry in the `"timelines"` array to extract the **`last_date`** (e.g., `"2026-10-08"`).
4. Alternatively, use the helper script to query the latest date:
   ```bash
   python3 .github/skills/update-show-timeline/scripts/update_timeline.py --get-latest "biggboss/json/shows/tamil/season10/timeline.json"
   ```

---

### Step 2: Fetch Recent Status & Events (`> last_date`)

1. **Wikipedia Summary Check**:
   - Visit the configured Wikipedia page for the show.
   - Look for recent episode summaries, daily log tables, weekly nomination/eviction tables, or wildcard entry announcements occurring after `last_date`.

2. **Official X (Twitter) Handles & Promos**:
   - Check official handles (`@VijayTelevision`, `@StarMaa`, `@ColorsTV`, `@DisneyPlusHS`, `@JioCinema`) for:
     - Daily morning & afternoon promo titles/descriptions.
     - Captaincy task winners and contender announcements.
     - Eviction alerts, walkouts, or cash-box exits.
     - Weekend episode highlights with the host.

3. **Cross-Reference & Fact Check**:
   - Verify participant names against `main.json` of the respective show to ensure accurate spellings.
   - Ensure the date assigned to each event corresponds to the actual broadcast / episode date (`YYYY-MM-DD`).

---

## 3. Timeline Schema & Standard Tags

Each entry in `timeline.json` follows this structure:
```json
{
  "date": "YYYY-MM-DD",
  "title": "Short Descriptive Headline",
  "message": "Detailed description of the event, housemates involved, and consequences.",
  "tag": "StandardTag"
}
```

### Standard Tags & Color Mapping

| Tag | Color Code | Usage / Triggers |
|:---|:---|:---|
| `Task` | `#2196F3` | Daily tasks, luxury budget tasks, spotlight/performance tasks, ration battles |
| `Captain` | `#FF9800` | Captaincy tasks, captaincy contenders, new captain announcements |
| `Nomination` | `#E91E63` | Weekly open/closed nominations, direct nominations, danger zone lists |
| `Eviction` | `#F44336` | Evictions, eliminations, secret room exits, voluntary walkouts, cash box exits |
| `Twist` | `#4CAF50` | Secret room entries, eviction-free passes, major rule changes, double eviction teasers |
| `Entry` | `#9C27B0` | Wildcard entries, guest entries, re-entries of evicted contestants |
| `Conflict` | `#FF5722` | Major heated arguments, physical fights, kitchen disputes, house clashes |
| `Premiere` | `#3F51B5` | Launch night / grand premiere episode |
| `WeekendKaVaar` / `Host` | `#673AB7` | Weekend host review episodes, host interventions, eviction reveals |
| `Update` | `#2196F3` | Boss meter, milestones, general status updates |

---

## 4. Updating & Persisting Data

1. **Draft New Entries**: Format all new events strictly adhering to the JSON schema.
2. **Merge & Sort**:
   - Prepend new entries at the top of the `"timelines"` array in `timeline.json`.
   - Maintain strict descending chronological order (`YYYY-MM-DD`).
   - Use the Python helper script to safely merge entries without duplicates:
     ```bash
     python3 .github/skills/update-show-timeline/scripts/update_timeline.py \
       --file "biggboss/json/shows/tamil/season10/timeline.json" \
       --entries '[{"date":"2026-10-09","title":"Task Title","message":"Event description","tag":"Task"}]'
     ```
3. **Verify Tag Colors**:
   - Ensure every `tag` used in `"timelines"` has an entry in the `"colors"` list at the bottom of `timeline.json`.
4. **Validate JSON Syntax**: Ensure no missing commas, trailing commas, or syntax errors remain in `timeline.json`.

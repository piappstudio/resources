---
name: Update Show Detail
description: Update the show details from online server to local JSON file
---

## 1. Show Configuration
| Show                          | show Id |
|:------------------------------|:--------|
| **BiggBoss-Tamil-Season-10**  | 6       |
| **BiggBoss-Telugu-Season-10** | 7       | 
| **BiggBoss-Hindi-Season-20**  | 5       |

## Update show Details
- Use configured biggboss MCP, use `participants/{show_id}` to pul the latest participant details, and update `main.json` of each show.
- Use `update_shows.py`, with above service response for replacement 

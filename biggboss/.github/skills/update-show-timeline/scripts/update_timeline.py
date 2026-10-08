import argparse
import json
import os
import sys

DEFAULT_COLORS = {
    "Eviction": "#F44336",
    "Nomination": "#E91E63",
    "Task": "#2196F3",
    "Captain": "#FF9800",
    "Twist": "#4CAF50",
    "Entry": "#9C27B0",
    "Conflict": "#FF5722",
    "Premiere": "#3F51B5",
    "WeekendKaVaar": "#673AB7",
    "Host": "#673AB7",
    "Update": "#2196F3"
}

def get_latest_date(timeline_file_path):
    """Returns the latest date recorded in the timeline.json file."""
    if not os.path.exists(timeline_file_path):
        print(f"Error: File not found - {timeline_file_path}", file=sys.stderr)
        return None

    with open(timeline_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    timelines = data.get('timelines', [])
    if timelines:
        return timelines[0].get('date')
    return None

def merge_timeline_entries(timeline_file_path, new_entries):
    """Merges new timeline entries into timeline.json avoiding duplicates and ensuring date sorting."""
    if not os.path.exists(timeline_file_path):
        print(f"Error: File not found - {timeline_file_path}", file=sys.stderr)
        return False

    with open(timeline_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    existing_entries = data.get('timelines', [])
    existing_keys = {(e.get('date'), e.get('title')) for e in existing_entries}

    if isinstance(new_entries, str):
        new_entries = json.loads(new_entries)

    added_count = 0
    for entry in new_entries:
        key = (entry.get('date'), entry.get('title'))
        if key not in existing_keys:
            existing_entries.append(entry)
            existing_keys.add(key)
            added_count += 1

    # Sort descending by date
    existing_entries.sort(key=lambda x: x.get('date', ''), reverse=True)
    data['timelines'] = existing_entries

    # Ensure all tags are in colors array
    colors_list = data.get('colors', [])
    existing_tags = {c['tag'] for c in colors_list if isinstance(c, dict) and 'tag' in c}

    for entry in existing_entries:
        tag = entry.get('tag')
        if tag and tag not in existing_tags:
            color = DEFAULT_COLORS.get(tag, "#2196F3")
            colors_list.append({"tag": tag, "color": color})
            existing_tags.add(tag)

    data['colors'] = colors_list

    with open(timeline_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')

    print(f"Successfully updated {timeline_file_path}: Added {added_count} new entries.")
    return True

def main():
    parser = argparse.ArgumentParser(description="Update show timeline.json with new events.")
    parser.add_argument("--get-latest", help="Path to timeline.json to get the latest recorded date.")
    parser.add_argument("--file", help="Path to timeline.json to update.")
    parser.add_argument("--entries", help="JSON string or file path containing array of new timeline entries.")

    args = parser.parse_args()

    if args.get_latest:
        latest_date = get_latest_date(args.get_latest)
        if latest_date:
            print(f"Latest Date: {latest_date}")
        else:
            print("No entries found.")
        return

    if args.file and args.entries:
        entries_content = args.entries
        if os.path.exists(args.entries):
            with open(args.entries, 'r', encoding='utf-8') as f:
                entries_content = f.read()

        merge_timeline_entries(args.file, entries_content)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

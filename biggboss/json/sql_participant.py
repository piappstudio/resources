import json
from datetime import datetime

# Function to generate SQL INSERT statements for nominations
def generate_sql_insert(participants):
    # Define the base SQL template for nominations
    sql_template = (
        "INSERT INTO `nominations` "
        "(`date`, `week`, `show_id`, `nominated_by_id`, `nominate_part_id`, `comments`) "
        "VALUES ('{date}', '{week}', '{show_id}', '{nominated_by_id}', '{nominate_part_id}', 'N/A');"
    )

    # Constants
    show_start_date = "2023-10-01"  # show start date (constant)
    show_id = "1"  # constant show id

    sql_statements = []

    # Loop through each participant
    for participant in participants:
        participant_id = participant.get("id")
        history = participant.get("history", [])

        # Loop through each week's history
        for week_info in history:
            week = week_info.get("week")
            nominates = week_info.get("nominates", [])

            # For each nominated person, create an INSERT statement
            for nominate_part_id in nominates:
                sql_statement = sql_template.format(
                    date=show_start_date,
                    week=week,
                    show_id=show_id,
                    nominated_by_id=participant_id,
                    nominate_part_id=nominate_part_id
                )
                sql_statements.append(sql_statement)

    return "\n".join(sql_statements)

# Main function to read JSON and generate SQL
def main():
    input_file = 'shows/tamil_session_7.json'  # your JSON file path
    output_file = 'insert_nominations.sql'  # output SQL file

    # Read JSON data
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Generate SQL statements
    sql_inserts = generate_sql_insert(data.get("participants", []))

    # Write to output file
    with open(output_file, 'w') as f:
        f.write(sql_inserts)

    print(f"✅ SQL nomination inserts have been written to {output_file}")

# Run the main function
if __name__ == "__main__":
    main()

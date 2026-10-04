import json

def update_show_main_json(file_path, server_response_json):
    with open(file_path, 'r', encoding='utf-8') as f:
        local_data = json.load(f)

    server_data = json.loads(server_response_json)

    local_data['participants'] = server_data['participants']
    local_data['category'] = server_data['category']

    return json.dumps(local_data, indent=2, ensure_ascii=False)

print("Helper script ready")

def read_keys_from_file(filename: str):
    keys_dict = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if '=' in line:
                key_part, value_part = line.split("=", 1)

                key_part = key_part.strip()
                value_part = value_part.strip()

                value_part = value_part.strip("'").strip('"')

                keys_dict[key_part] = value_part
    return keys_dict
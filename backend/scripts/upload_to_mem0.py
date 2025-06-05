import os
from mem0 import Mem0Client

def upload_file_to_mem0(filepath, tags=None, api_key=None):
    api_key = api_key or os.getenv("MEM0_API_KEY")
    assert api_key, "Set MEM0_API_KEY as env variable or pass as argument."

    client = Mem0Client(api_key=api_key)
    with open(filepath, "r", encoding="utf-8") as f:
        data = f.read()
    client.add_memory(data, tags=tags or [])
    print(f"Uploaded {filepath} to Mem0 with tags: {tags}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath")
    parser.add_argument("--tags", nargs="*", default=[])
    parser.add_argument("--api_key", default=None)
    args = parser.parse_args()
    upload_file_to_mem0(args.filepath, tags=args.tags, api_key=args.api_key)

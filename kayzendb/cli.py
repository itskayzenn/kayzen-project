import sys
import json
import getpass
import argparse
from .core import KayzenDB

def main():
    parser = argparse.ArgumentParser(description="KayzenDB CLI")
    parser.add_argument("db_file", help="Path to database file")
    args = parser.parse_args()

    print("🔐 KayzenDB Security Check")
    password = getpass.getpass("Enter Database Password: ")

    try:
        db = KayzenDB(args.db_file, password)
        print(f"✅ Connected to {args.db_file}")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

    print("\nCommands: CREATE, READ, UPDATE, DELETE, FIND, LIST, EXIT")
    print("Example: CREATE user1 {\"age\": 25, \"role\": \"admin\"}")

    while True:
        try:
            cmd_input = input("kayzen> ").strip()
            if not cmd_input: continue
            
            parts = cmd_input.split(" ", 2)
            cmd = parts[0].upper()

            if cmd == "EXIT":
                print("Goodbye.")
                break

            elif cmd == "LIST":
                print(db.list_keys())

            elif cmd == "READ":
                if len(parts) < 2: print("Usage: READ <key>"); continue
                try:
                    print(json.dumps(db.read(parts[1]), indent=2))
                except Exception as e: print(f"Error: {e}")

            elif cmd == "DELETE":
                if len(parts) < 2: print("Usage: DELETE <key>"); continue
                try:
                    db.delete(parts[1])
                    print("Deleted.")
                except Exception as e: print(f"Error: {e}")

            elif cmd in ["CREATE", "UPDATE"]:
                if len(parts) < 3: print(f"Usage: {cmd} <key> <json_value>"); continue
                key = parts[1]
                try:
                    val = json.loads(parts[2])
                    if cmd == "CREATE": db.create(key, val)
                    else: db.update(key, val)
                    print("Success.")
                except json.JSONDecodeError:
                    print("Error: Invalid JSON format.")
                except Exception as e:
                    print(f"Error: {e}")

            elif cmd == "FIND":
                # FIND age > 20
                # parts split logic needs adjustment for FIND
                find_parts = cmd_input.split(" ")
                if len(find_parts) < 4:
                    print("Usage: FIND <field> <operator> <value>")
                    continue
                
                field = find_parts[1]
                op = find_parts[2]
                val = find_parts[3]
                
                # Try convert val to number if possible
                try:
                    if "." in val: val = float(val)
                    else: val = int(val)
                except:
                    pass
                
                results = db.find(field, op, val)
                print(f"Found {len(results)} matches:")
                print(json.dumps(results, indent=2))

            else:
                print("Unknown command.")

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Unexpected Error: {e}")

if __name__ == "__main__":
    main()

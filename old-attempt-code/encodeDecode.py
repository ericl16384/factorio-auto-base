import json
import blueprintUtil

dataFile = "data.txt"

while True:
    # Input
    #string = input("Exchange string or JSON, or read from file (leave blank):\n")

    # Faster!!!
    string = ""

    # File
    if len(string) == 0:
        with open(dataFile, "r") as f:
            string = f.read()
        print(f"[From {dataFile}]")

    # Strip
    string = string.strip()


    # JSON
    try:
        output = blueprintUtil.encode(json.loads(string))

    # Exchange string
    except json.JSONDecodeError:
        output = json.dumps(blueprintUtil.decode(string), indent=4)

    # Output
    print()
    print(f"Result (in {dataFile}): ")
    print(output)
    print()
    with open(dataFile, "w") as f:
        print(output, file=f)

    # Faster!!!
    #input()
    break
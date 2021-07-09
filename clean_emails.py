from pathlib import Path
import argparse

parser = argparse.ArgumentParser(description="Clean output extracted emails")
parser.add_argument("file", help="File to clean.")
args = parser.parse_args()

emails = []

with open(args.file, "r") as file:
    content = file.readlines()

    for line in content:
        emails.append(line)

with open(args.file + "-emails", "a") as lnkfile:
    emails = set(emails)
    for email in emails:
        lnkfile.write(email)

# Remove old file
filePath=Path(args.file)

try:
    filePath.unlink()
except OSError as e:
    print(f"Error:{ e.strerror}")
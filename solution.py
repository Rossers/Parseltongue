def print_secret_message(doc_url: str) -> None:
    import re
    import urllib.request

    # Extract the Google Doc ID and convert to a plain text export URL
    match = re.search(r"/document/d/([a-zA-Z0-9_-]+)", doc_url)
    if not match:
        raise ValueError("Invalid Google Doc URL.")

    doc_id = match.group(1)
    txt_url = f"https://docs.google.com/document/d/{doc_id}/export?format=txt"

    # Download the document as plain text
    with urllib.request.urlopen(txt_url) as response:
        doc_text = response.read().decode("utf-8")

    # Split into lines, trim whitespace, remove blank lines
    lines = [line.strip() for line in doc_text.splitlines() if line.strip()]

    # Remove the known header labels
    lines = [
        line for line in lines
        if line not in ("x-coordinate", "Character", "y-coordinate")
    ]

    # Parse remaining lines in groups of 3: x, character, y
    if len(lines) % 3 != 0:
        raise ValueError("Unexpected document format.")

    points = []
    for i in range(0, len(lines), 3):
        x = int(lines[i])
        char = lines[i + 1]
        y = int(lines[i + 2])
        points.append((x, y, char))

    if not points:
        return

    #TODO: need to display the parsed points.
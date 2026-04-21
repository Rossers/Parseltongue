def print_secret_message(doc_url: str) -> None:
    import re
    import html
    import urllib.request

    # Download the published Google Doc page directly
    with urllib.request.urlopen(doc_url) as response:
        doc_text = response.read().decode("utf-8")

    # Convert HTML into rough plain text
    doc_text = re.sub(r"<script.*?</script>", "", doc_text, flags=re.DOTALL | re.IGNORECASE)
    doc_text = re.sub(r"<style.*?</style>", "", doc_text, flags=re.DOTALL | re.IGNORECASE)
    doc_text = re.sub(r"<br\s*/?>", "\n", doc_text, flags=re.IGNORECASE)
    doc_text = re.sub(r"</p>|</div>|</tr>|</li>|</h\d>", "\n", doc_text, flags=re.IGNORECASE)
    doc_text = re.sub(r"<[^>]+>", "", doc_text)
    doc_text = html.unescape(doc_text)

    # Split into lines, trim whitespace, remove blank lines
    lines = [line.strip() for line in doc_text.splitlines() if line.strip()]

    # Keep only the useful section starting at the coordinate table
    try:
        start_index = lines.index("x-coordinate")
        lines = lines[start_index:]
    except ValueError:
        raise ValueError("Could not find expected document data.")

    # Remove known labels and page chrome text
    ignore_lines = {
        "x-coordinate",
        "Character",
        "y-coordinate",
        "Published using Google Docs",
        "Updated automatically every 5 minutes",
        "Report abuse",
        "Learn more",
    }

    lines = [line for line in lines if line not in ignore_lines]

    # Parse remaining lines in groups of 3: x, character, y
    if len(lines) % 3 != 0:
        raise ValueError(f"Unexpected document format. Parsed {len(lines)} data lines: {lines[:20]}")

    points = []
    for i in range(0, len(lines), 3):
        x = int(lines[i])
        char = lines[i + 1]
        y = int(lines[i + 2])
        points.append((x, y, char))

    if not points:
        return

    # Find grid bounds
    max_x = max(x for x, y, char in points)
    max_y = max(y for x, y, char in points)

    # Create grid filled with spaces
    grid = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    # Place characters into the grid
    for x, y, char in points:
        grid[max_y - y][x] = char

    # Print the result row by row
    for row in grid:
        print("".join(row))

if __name__ == "__main__":
    import sys

    # Enable testing with hard-coded URLs if no URL is provided.
    TEST_URLS = {
        "example": "https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub",
        "secret": "https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub",
    }

    if len(sys.argv) > 1:
        arg = sys.argv[1]

        if arg in TEST_URLS:
            print(f"Running preset: {arg}")
            print_secret_message(TEST_URLS[arg])
        else:
            print("Running custom URL")
            print_secret_message(arg)
    else:
        print("No argument provided. Running 'example'")
        print_secret_message(TEST_URLS["example"])
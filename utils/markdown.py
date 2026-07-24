
def extract_markdown_section(full_text, start_marker, end_marker=None):
    if start_marker not in full_text:
        return ""

    start_index = full_text.find(start_marker) + len(start_marker)

    if end_marker and end_marker in full_text:
        end_index = full_text.find(end_marker)
        return full_text[start_index:end_index].strip()

    return full_text[start_index:].strip()



def clean_markdown_bold(text):

    replacements = {
        "tag:211": "211 University",
        "tag:Double 1st-Class": "Double First-Class"
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text.replace("**", "")

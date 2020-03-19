# delete content of file
def delete_text(path):
    with open(path, "r+") as f:
        f.seek(0)
        f.truncate()


def form_string(*strings):
    result = ""
    for string in strings:
        result += string
        result += " "
    return result

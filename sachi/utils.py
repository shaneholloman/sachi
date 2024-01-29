import re

FAKE_SLASH = "／"

FS_SPECIAL_CHARS = re.compile(r"[/\\:*\"?<>|]")

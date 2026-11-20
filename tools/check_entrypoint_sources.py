"""Read two small pinned source texts over HTTPS and verify their identity."""
import hashlib
import re
from urllib.request import urlopen


BASE = (
    "https://raw.githubusercontent.com/CocoSgt/riemann-hypothesis-lean/"
    "0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/"
)
FILES = {
    "Main.lean": (433, "017645ca448f2fd1f6fd5c4c2cb2c6e96e472725be13f6e180ca6e1574360939"),
    "Statements.lean": (783, "79ef7ca776e42abe1f46caee13ea09bd19f1e2d0b1620d8d5d200258f33b47bf"),
}


def main():
    for filename, (size, expected) in FILES.items():
        url = BASE + filename
        with urlopen(url, timeout=20) as response:
            data = response.read(size + 1)
        digest = hashlib.sha256(data).hexdigest()
        if len(data) != size or digest != expected:
            raise SystemExit(f"Source identity mismatch for {url}")
        print(f"{digest}  {filename}  ({size} bytes)")
        if filename == "Main.lean":
            targets = re.findall(r"^theorem (\w+) : (\w+) := (\S+)$",
                                 data.decode("utf-8"), re.MULTILINE)
            if len(targets) != 5:
                raise SystemExit("Expected five single-line theorem declarations in pinned Main")
            for name, proposition, term in targets:
                print(f"  {name} : {proposition} := {term}")
    print("Pinned source text matched. No Lean code was executed.")


if __name__ == "__main__":
    main()

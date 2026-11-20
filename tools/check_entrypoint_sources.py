"""Verify pinned source identities and compare the extracted Lean declarations."""
import hashlib
import re
from pathlib import Path
from urllib.request import urlopen


EXTRACTION = Path(__file__).resolve().parents[1] / "lean" / "extraction" / "Extraction"
BASE = (
    "https://raw.githubusercontent.com/CocoSgt/riemann-hypothesis-lean/"
    "0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/"
)
FILES = {
    "Main.lean": (433, "017645ca448f2fd1f6fd5c4c2cb2c6e96e472725be13f6e180ca6e1574360939"),
    "Statements.lean": (783, "79ef7ca776e42abe1f46caee13ea09bd19f1e2d0b1620d8d5d200258f33b47bf"),
    "Development/AutomorphicArithmetic/CharacterBoxes/ClaimStrip.lean": (
        5193, "74498552f19df4bd5b3c296ed247d25d40cabd1057647dd4db1ee7ba1c57ea03"
    ),
}
MATHLIB_REVISION = "0df444a360eaa60ab8c11dca51a86af692955474"
MATHLIB_BASE = (
    f"https://raw.githubusercontent.com/leanprover-community/mathlib4/{MATHLIB_REVISION}/Mathlib/"
)
MATHLIB_FILES = {
    "NumberTheory/LSeries/DirichletContinuation.lean": (
        18979, "86d3aaad83e64cb64a24167fd4ddb2eeec5ca4a19a9298459e87a57fec151040"
    ),
    "NumberTheory/LSeries/Nonvanishing.lean": (
        21780, "945a2fd23ca9ebd2d48f101d771ef9117dd9847d48fd77ea2623d8c345f4f5a9"
    ),
    "NumberTheory/LSeries/RiemannZeta.lean": (
        12306, "db9f37f08bcce379c502549f604c0e98bf4a39b3a3440606861bbac847f2a1a9"
    ),
}


def read_pinned_source(url, size, expected):
    with urlopen(url, timeout=20) as response:
        data = response.read(size + 1)
    digest = hashlib.sha256(data).hexdigest()
    if len(data) != size or digest != expected:
        raise SystemExit(f"Source identity mismatch for {url}")
    return "\n".join(data.decode("utf-8").splitlines())


def factor_statement(source):
    match = re.search(r"^theorem factor_ne_zero\b[\s\S]+?(?= := by\n)", source, re.MULTILINE)
    if match is None:
        raise SystemExit("Missing factor_ne_zero statement")
    return match.group()


def main():
    for base, files in ((BASE, FILES), (MATHLIB_BASE, MATHLIB_FILES)):
        for filename, (size, expected) in files.items():
            source = read_pinned_source(base + filename, size, expected)
            print(f"{expected}  {filename}  ({size} bytes)")
            if filename == "Main.lean":
                targets = re.findall(r"^theorem (\w+) : (\w+) := (\S+)$", source, re.MULTILINE)
                if len(targets) != 5:
                    raise SystemExit("Expected five single-line theorem declarations in pinned Main")
                for name, proposition, term in targets:
                    print(f"  {name} : {proposition} := {term}")
            elif filename == "Statements.lean":
                declarations = source.removeprefix("import Mathlib\n").strip()
                if declarations not in (EXTRACTION / "Semantics.lean").read_text(encoding="utf-8"):
                    raise SystemExit("Extracted semantics definitions differ from pinned Statements")
            elif filename.endswith("/ClaimStrip.lean"):
                local_factor = factor_statement((EXTRACTION / "Factor.lean").read_text(encoding="utf-8"))
                if factor_statement(source) != local_factor:
                    raise SystemExit("Extracted factor_ne_zero signature differs from pinned ClaimStrip")
    print("Pinned hashes and extracted declaration text matched. No Lean code was executed.")


if __name__ == "__main__":
    main()

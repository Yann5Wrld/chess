"""Construit app/src/main/assets/openings.json à partir des fichiers TSV de lichess-org/chess-openings.
Clé : position (pièces, trait, roques) -> [code ECO, nom]."""
import json, re, sys
import chess

out = {}
for path in sys.argv[1:-1]:
    with open(path, encoding="utf-8") as f:
        next(f)  # en-tête
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 3:
                continue
            eco, name, pgn = parts[0], parts[1], parts[2]
            board = chess.Board()
            try:
                for tok in pgn.split():
                    if re.match(r"^\d+\.", tok):
                        tok = re.sub(r"^\d+\.+", "", tok)
                        if not tok:
                            continue
                    board.push_san(tok)
            except ValueError:
                continue
            key = " ".join(board.fen().split()[:3])
            out.setdefault(key, [eco, name])

with open(sys.argv[-1], "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
print(len(out), "ouvertures")

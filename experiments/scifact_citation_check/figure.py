"""Draw the chapter figure from frozen release decisions (matplotlib 3.10.7)."""
import json
from pathlib import Path

import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
result = json.loads((HERE / "results.json").read_text())
rows = [("Triage · pool evidence", "pool", "triage"),
        ("Triage · require agreement", "agreement", "triage"),
        ("Publication · either rule", "pool", "publication")]
fig, ax = plt.subplots(figsize=(8.2, 2.65), layout="constrained")
for y, (name, arm, user) in enumerate(rows):
    start = 0
    for field, color, ink, legend in [
        ("justified", "#00675e", "white", "Justified release"),
        ("unsupported", "#994323", "white", "Unsupported release"),
        ("held", "#e3e6ea", "#202933", "Held for review"),
    ]:
        count = result["outcomes"][arm][user][field]
        ax.barh(y, count, left=start, color=color, height=.63, label=legend if y == 0 else None)
        if count:
            ax.text(start+count/2, y, str(count), color=ink, ha="center", va="center", weight="bold")
        start += count
ax.set(yticks=range(len(rows)), yticklabels=[row[0] for row in rows], xlim=(0, result["n"]),
       xlabel="Held-out claims", xticks=[0, 50, 100, 150, 200, 250, 299])
ax.invert_yaxis()
ax.spines[["top", "right", "left"]].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.legend(loc="lower center", bbox_to_anchor=(.5, 1), ncol=3, frameon=False)
fig.savefig(HERE.parents[1] / "assets/images/scifact-release-decisions.png", dpi=180)

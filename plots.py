import matplotlib.pyplot as plt

points = {
    "vasishta": (0, 277),
    "AB2": (162, 504),
    "Library": (345, 541),
    "gargi": (410, 429),
    "main gate": (454, 0),
    "Mythreyi": (580, 157),
    "gen store": (627, 295),
    "ASB": (634, 572),
    "Physical Ed": (676, 288),
    "ASB canteen": (679, 616),
    "Pandal": (729, 563),
    "AB1": (748, 115),
    "Sopanam": (854, 151),
    "kashyapa": (994, 421)
}

plt.figure(figsize=(10, 6))

for name, (x, y) in points.items():
    plt.scatter(x, y, color='crimson', s=40)
    plt.text(x + 12, y + 5, name, fontsize=9)

plt.title("Amrita Campus Nodes (Meters from Origin)")
plt.xlabel("X (Meters East)")
plt.ylabel("Y (Meters North)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.axis("equal") 
plt.show()
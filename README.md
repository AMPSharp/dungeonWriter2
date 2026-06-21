#  Bookvale Mage: Grimoire & Narrative Dungeon

An immersive, gamified CLI text adventure and writing productivity tool designed to help writers conquer writer's block and track word counts through RPG mechanics. Write prose to banish monsters, cultivate ancient gardens via Pomodoro techniques, and protect local villagers through specialized writing sprints!

---

## Core Mechanics & Locations

### 1. Pencilton (The Safe Hub)
* **The Town Shop:** Trade your hard-earned writing gold for Enchanted Writing Quills, Arcane Teleport Stones, and customized armor sets.
* **Armor Progression:** Upgrade your vestments from the humble *Trousers of Brainstorming* up to the legendary *Editor's Crown* to raise your maximum Mental Energy.

### 2. Calligraphy Forests (Monster Hunting)
* **Battle with Words:** Encounter unique monsters scaled to your equipment tier.
* **Prose Casting:** Every word you type deals direct damage to the active adversary. Be careful—maintaining continuous typing circles drains your Mental Energy (`-1 HP` per paragraph/line). Falling to exhaustion drops unsaved session data and retreats you back to town!

### 3. The Biblioarchives (Timed Writing Sprints)
Engage in focused, timed writing sprints to rebuild the defenses of Bookvale. Yields scale based on total words typed during the active window:
* **Heal Villagers I (5 Mins):** Every 50 words = 1 Villager rescued + 1 Gold.
* **Repair Wards (10 Mins):** Every 100 words = 1 Wall HP + 1 Ration bag.
* **Heal Villagers II (15 Mins):** Every 200 words = 4 Villagers rescued + 5 Gold.
* **Sooth Beasts (20 Mins):** Every 500 words = 1 Monster Cleansed + 1 Teleport Stone.

### 4. Narrative Gardens (Deep Focus Pomodoros)
* **25-Minute Rituals:** A strict, uninterrupted long-form focus block designed for heavy manuscript drafts. Early stopping is penalized!
* **Dynamic ASCII Art:** Watch the ecosystem physically evolve. As you inject words into the soil, the garden shifts across 4 distinct visual tiers from a desolate *Ashen Wasteland* to a paradise in *Full Bloom* teeming with dancing fairies.
* **Daily Focus Limits:** Up to 4 deep focus sessions allowed per calendar day before the fairies must rest.

---

## Core System Commands

| Command | Action | Location Availability |
| :--- | :--- | :--- |
| `/travel` | Open the world navigation vector map | Anywhere (Except active sprint loops) |
| `/use_quill` | Anchor and append current session text straight to the ledger | Anywhere |
| `/teleport` | Consume an Arcane Stone to instantly return to town and restore full energy | Anywhere |
| `/rations` | Consume 1 food ration bag to restore `+5` Mental Energy | Anywhere |
| `/exit` | Auto-saves your project variables and safely terminates the grimoire | Anywhere |

---

## Project Structure

Dungeon Writer 2/
├── dungeonWriter2.py    # Master Engine Loop & Core Runtime Switchboard
├── config.py            # Global Setup Manager & Session Target Goals
├── story.py             # Scripted Narrative Milestones & Daily Decay Rules
├── bestiary.py          # Adversary Profiles & Creature ASCII Rendering 
├── archives.py          # Biblioarchives Activity Timers & Reward Parsers
├── gardens.py           # Narrative Gardens Tiers & Pomodoro Loops
└── tutorial.py          # Introductory Timed Goblin Trial Script

---

## Save System & Data Vaults

All game properties and manuscript ledgers are securely recorded on close or checkpoint actions within a localized `.saves/` directory:

* `[ProjectName]_stats.json`: Tracks historical stats, health allocations, gear status, and timezone metadata.
* `[ProjectName]_backlog.md`: Your unified creative writing master ledger. All prose lines processed by the combat loop, sprint wings, or gardens are cleanly stitched into this Markdown notebook under systematic subheaders—free from formatting penalties or text distortions.

---

## Installation & Quick Start

### Prerequisites

Make sure you have Python 3 installed on your machine.

### running the game

1. Clone or download this project directory onto your computer.
2. Open your system Terminal (Linux/macOS) or Command Prompt (Windows).
3. Navigate into the project directory:
```bash
cd "path/to/Dungeon Writer 2"
```
4. Launch the application:
```bash
python3 dungeonWriter2.py

```
### Running on Android (via Termux)

You can play your game on the go by running it inside Termux, a free terminal emulator for Android.

  1. Download Termux (it is highly recommended to grab it from F-Droid rather than the Google Play Store, as the Play Store version is outdated).

  2. Open Termux and update your core environment packages:
    Bash

    pkg update && pkg upgrade

  3. Install Python and Git:
    Bash

    pkg install python git

  4. Clone your repository directly into your device environment:
    Bash

    git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
    cd YOUR_REPO_NAME

  5. Launch your grimoire:
    Bash

    python dungeonWriter2.py

Tip: Since Termux uses your device’s internal flash storage, your progress will save automatically to your active directory layout just like it does on a desktop computer!

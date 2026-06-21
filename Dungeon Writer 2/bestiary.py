import random

def get_monster_ascii(name):
    artworks = {
        "Dangling Modifier Imp": "   ,_,   \n  (o,o)  <-- *whispers confusing modifiers*\n  {`'}`  \n  -\"-\"-  ",
        "Plot Hole Slime": "   (_____)   \n _(       )_  <-- *oozing through logical inconsistencies*\n(___________)",
        "Typo Swarm": "  xX  oO  vV \n   Vv  Xx  Oo <-- *bzzzt! thier, teh, recieve!*\n  oO  vV  xX ",
        "Run-on Sentence Serpent": " ~~~~_.._~~~~~~\n     (oo)____  <-- *and then it went and and and and...*\n       ||    ||",
        "Writer's Block Goblin": "  /\033[4m  \033[0m\\\n ( o.o )  <-- \"Your mind shall remain completely blank!\"\n  > ^ <  ",
        "Passive Voice Phantom": "  .-.\n (o o)  <-- \"Mistakes were made by your characters...\"\n | O |\n |   |",
        "Cliche Chimera": "  /\\_/\\  /__\\\n ( o.o )( v v ) <-- *roars predictably in a dark and stormy night*\n  > ^ <  > ^ <",
        "Exposition Dump Ogre": "  _______ \n [ -   - ] <-- \"Let me pause the plot to explain 400 years of lore!\"\n  |  O  | \n /|_____|\\",
        "Purple Prose Vampire": "  ,-___-,  \n [(-. .-)] <-- \"Ah, your verbose, twilight-glistening soliloquy feeds me!\"\n   \033[35m\\\033[0m   \033[35m/\033[0m   \n    -v-    ",
        "Imposter Syndrome Specter": " .-'''-. \n/ _   _ \\ <-- \"A real writer would have finished a chapter by now...\"\n|  0   0 |\n\\    v   /",
        "Pacing Pterodactyl": " __   _   __ \n \\ \\ (o) / / <-- *screeches while throwing off your story beats!*\n  \\_\\_V_/_/  ",
        "Redundant Redundant Echo": " (( o ))   \n  (( o ))  <-- \"I am repeating myself over and over again repetitively!\"\n   (( o )) ",
        "Burn-out Wraith": "   (X X)   \n  /[   ]\\  <-- \"The creative well is dry... step away from the keyboard...\"\n  /  |  \\  \n     v     ",
        "The Inner Critic (Elite)": "   _###_   \n  ( ಠ ಠ )  <-- \"Delete the whole draft. It's completely unsalvageable.\"\n   \\_=_/   ",
        "Scope Creep Beholder": "  ,i. ,i. ,i.\n  (o) (o) (o)\n   \\\\  ||  // \n    (  O  )   <-- \"What if we added a trilogy-spanning prequel right here?\"\n     '---'    ",
        "Dead-End Subplot Hydra": "  (o)(o)(o) \n  || || ||  \n /  \\||/  \\ <-- \"Hahaha! Cut one off, two more useless side-quests grow!\"\n |________| ",
        
        # === STORY BOSS: THE APOCALYPTIC THREAT ===
        "The Dragon of Burnout": "       _   _ \n      ( \\_/ )   _   _ \n       ) _ (   ( \\_/ )  <-- *Breaths grey ash, turning ink to dust!*\n     _/_/ \\_\\_  ) _ ( \n    (___/_\\___)(___/  "
    }
    return artworks.get(name, "  [No Image Available]  ")

def get_monster_for_tier(tier):
    pools = {
        1: [
            {"name": "Dangling Modifier Imp", "hp": 12, "gold": 12},
            {"name": "Plot Hole Slime", "hp": 25, "gold": 18},
            {"name": "Typo Swarm", "hp": 35, "gold": 22},
            {"name": "Run-on Sentence Serpent", "hp": 50, "gold": 30}
        ],
        2: [
            {"name": "Writer's Block Goblin", "hp": 60, "gold": 45},
            {"name": "Passive Voice Phantom", "hp": 75, "gold": 55},
            {"name": "Cliche Chimera", "hp": 85, "gold": 65},
            {"name": "Exposition Dump Ogre", "hp": 100, "gold": 75}
        ],
        3: [
            {"name": "Purple Prose Vampire", "hp": 125, "gold": 95},
            {"name": "Imposter Syndrome Specter", "hp": 150, "gold": 115},
            {"name": "Pacing Pterodactyl", "hp": 175, "gold": 135},
            {"name": "Redundant Redundant Echo", "hp": 200, "gold": 150}
        ],
        4: [
            {"name": "Burn-out Wraith", "hp": 250, "gold": 200},
            {"name": "The Inner Critic (Elite)", "hp": 350, "gold": 280},
            {"name": "Scope Creep Beholder", "hp": 450, "gold": 360},
            {"name": "Dead-End Subplot Hydra", "hp": 500, "gold": 420},
            
            # Integrated Final Story Encounter: Massive HP pool to match its narrative weight
            {"name": "The Dragon of Burnout", "hp": 750, "gold": 600}
        ]
    }
    selected_pool = pools.get(tier if tier <= 4 else 4)
    base_monster = random.choice(selected_pool).copy()
    base_monster["max_hp"] = base_monster["hp"]
    return base_monster
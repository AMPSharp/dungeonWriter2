import os
import json

LOCAL_CONFIG = "game_settings.json"

def first_time_setup_wizard():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 60)
    print("🔮  DUNGEON WRITER: FIRST-TIME SETUP WIZARD  🔮")
    print("=" * 60)
    print("Where shall your mage deposit their spell archives (manuscripts)?")
    print(" [1] Standard Obsidian Vault (Documents/The Writing Desk/Dungeon Writer)")
    print(" [2] Direct External Storage Path (Legacy Android)")
    print(" [3] Custom Vault Path (Type manual absolute path)")
    print("=" * 60)

    while True:
        choice = input("Select an option (1-3): ").strip()
        if choice in ("1", "2", "3"): break
        print("❌ Invalid selection.")

    if choice == "1":
        if os.path.exists("/storage/emulated/0"):
            target_path = "/storage/emulated/0/Documents/The Writing Desk/Dungeon Writer"
        else:
            target_path = os.path.expanduser("~/Documents/The Writing Desk/Dungeon Writer")
    elif choice == "2":
        target_path = "/storage/emulated/0/Documents/DungeonWriter"
    else:
        print("\nType or paste the full absolute path to your target vault folder:")
        while True:
            target_path = input("Path: ").strip()
            if target_path: break
            print("❌ Path cannot be blank.")

    try:
        os.makedirs(target_path, exist_ok=True)
        with open(LOCAL_CONFIG, "w") as f:
            json.dump({"save_directory": target_path}, f, indent=4)
        print(f"\n✅ Archives linked to: {target_path}")
        input("Press Enter to unroll the chronicle...")
        return target_path
    except Exception as e:
        print(f"\n❌ Channeling error ({e}). Defaulting to local script directory.")
        input("Press Enter to continue...")
        return "./WordDungeon"

def get_save_directory():
    if os.path.exists(LOCAL_CONFIG):
        try:
            with open(LOCAL_CONFIG, "r") as f:
                path = json.load(f).get("save_directory")
                if path: return path
        except: pass
    return first_time_setup_wizard()

SAVE_DIR = get_save_directory()
REGISTRY_FILE = os.path.join(SAVE_DIR, "project_registry.json")

def load_registry():
    try:
        with open(REGISTRY_FILE, "r") as f: 
            data = json.load(f)
            if "slots" not in data:
                return {"slots": {"1": None, "2": None, "3": None, "4": None, "5": None}}
            return data
    except:
        return {"slots": {"1": None, "2": None, "3": None, "4": None, "5": None}}

def save_registry(registry):
    try:
        os.makedirs(os.path.dirname(REGISTRY_FILE), exist_ok=True)
        with open(REGISTRY_FILE, "w") as f: json.dump(registry, f, indent=4)
    except Exception as e:
        print(f"⚠️ Error saving registry: {e}")

def select_project_session():
    registry = load_registry()
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("=" * 60)
    print("🔮 📜  CHOOSE A DRAFT CAMPAIGN TO CHANNEL YOUR MAGIC  📜 🔮")
    print("=" * 60)
    
    for slot, project_name in sorted(registry["slots"].items()):
        if project_name:
            stats_path = os.path.join(SAVE_DIR, f"{project_name}_stats.json")
            word_count = 0
            if os.path.exists(stats_path) and os.path.getsize(stats_path) > 0:
                try:
                    with open(stats_path, "r") as sf:
                        word_count = json.load(sf).get("total_words", 0)
                except: pass
            print(f" [{slot}] {project_name} ({word_count} Mana Words channeled)")
        else:
            print(f" [{slot}] --- Empty Spell Book ---")
    print("=" * 60)
    
    while True:
        choice = input("Select an ink slot (1-5): ").strip()
        if choice in registry["slots"]: break
        print("❌ Invalid book selection.")

    # If it's a loaded game, tutorial choice is None
    if registry["slots"][choice] is not None:
        return registry["slots"][choice], None
    else:
        # === THE EXPANDED STORY INTRODUCTION ===
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 60)
        print("📖 WELCOME TO BOOKVALE")
        print("=" * 60)
        print("Welcome to Bookvale, a world constructed from the materials of itsown magic: parchment hills, vellum valleys, and library-cities. Rivers of ink flow down from the Great Wells, providing the medium for all magic. You are a paper mage in this world. Your words can help or harm the denizens as well as construct wonders beyond all but the wildest imaginations.")
        print("\nThere's just one problem... Maybe two if you count the dragon burning everything down...")
        print("\nYou don't know what to write! How can you build entire worlds if you don't know what to write?")
        print("\nThe grimoire in your hands is completely empty, and the world around you is little more than ash from the dragon's rampage. How can you ever hope to fill the tome?")
        print("-" * 60)
        print("...Let's start on the first page.")
        
        while True:
            mage_name = input("\nWhat is your name? ").strip()
            clean_mage = "".join(c for c in mage_name if c.isalnum() or c in (" ", "_", "-")).strip()
            if clean_mage: break
            print("❌ Your name cannot be blank.")

        name_word_count = len(clean_mage.split())
        print(f'\n"By {clean_mage}" Okay... that\'s {name_word_count} words.')

        while True:
            new_name = input("\nNow for a title. It's okay if its a nonsense word,\nyour friend always said the name could be changed later...\nTitle: ").strip()
            clean_name = "".join(c for c in new_name if c.isalnum() or c in (" ", "_", "-")).strip()
            if clean_name: break
            print("❌ Title invalid.")
            
        print("\nOkay, not your best name but you'll figure that out later. You flip the page...and are daunted by the empty void that greets you. Lucy would know what to write, you should go see her.")
        print("\nUh-oh...there's a goblin in the way. You're going to have to figure out something to write fast before it eats your spellbook!")
        print("=" * 60)
        
        print(" [1] Fight the goblin (play the tutorial)")
        print(" [2] Go around (skip the tutorial)")
        print("=" * 60)

        while True:
            tutorial_input = input("Choose an option (1-2): ").strip()
            if tutorial_input == "1":
                tutorial_choice = "fight"
                break
            elif tutorial_input == "2":
                tutorial_choice = "skip"
                break
            print("❌ Invalid selection.")

        final_project_identity = f"{clean_mage} - {clean_name}"
        registry["slots"][choice] = final_project_identity
        save_registry(registry)
        
        return final_project_identity, tutorial_choice
# dungeonWriter2.py
import os
import json
import random
import time
import textwrap
from datetime import datetime

# === MODULAR MANAGED IMPORTS ===
import config
import bestiary  
import story  
import archives  # New archive sprint mechanics module
import gardens   # New focus pomodoro mechanics module

# Unpack the project name and tutorial setting choice from the config setup
PROJECT_NAME, TUTORIAL_MODE = config.select_project_session()
SAVE_DIR = config.SAVE_DIR
STATS_FILE = os.path.join(SAVE_DIR, f"{PROJECT_NAME}_stats.json")
BACKLOG_FILE = os.path.join(SAVE_DIR, f"{PROJECT_NAME}_backlog.md")

def load_game():
    fallback_stats = {
        "gold": 50, "xp": 0, "total_words": 0, 
        "teleport_stones": 1, "quills": 1, "rations": 0, "armor_tier": 1, 
        "hp": 10, "max_hp": 10, "story_milestone": 0,
        "current_zone": "Pencilton",
        "villagers": 50, "village_hp": 30, "garden_hp": 10,
        "last_garden_completion": 0.0, "garden_runs_today": 0,
        "last_day_reset_timestamp": ""
    }
    if not os.path.exists(STATS_FILE) or os.path.getsize(STATS_FILE) == 0:
        return fallback_stats

    try:
        with open(STATS_FILE, "r") as f:
            text = f.read().strip()
            if not text: return fallback_stats
            data = json.loads(text)
            
            # Schema backward compatibility layers
            if "quills" not in data: data["quills"] = 1
            if "teleport_stones" not in data: data["teleport_stones"] = data.pop("shields", 1)
            if "rations" not in data: data["rations"] = 0
            if "armor_tier" not in data: data["armor_tier"] = 1
            if "hp" not in data: data["hp"] = data.get("max_hp", 10)
            if "max_hp" not in data: data["max_hp"] = 10
            if "story_milestone" not in data: data["story_milestone"] = 0
            if "current_zone" not in data: data["current_zone"] = "Pencilton"
            if "villagers" not in data: data["villagers"] = 50
            if "village_hp" not in data: data["village_hp"] = 30
            if "garden_hp" not in data: data["garden_hp"] = 10
            return data
    except (json.JSONDecodeError, PermissionError):
        return fallback_stats

def save_game(stats, paragraph_list):
    try:
        os.makedirs(os.path.dirname(STATS_FILE), exist_ok=True)
        with open(STATS_FILE, "w") as f: 
            json.dump(stats, f, indent=4)
        with open(BACKLOG_FILE, "w") as f: 
            f.write("\n\n".join(paragraph_list))
    except Exception as e:
        print(f"⚠️ Spell sealing failure (Save Error): {e}")

def load_manuscript():
    try:
        with open(BACKLOG_FILE, "r") as f:
            text = f.read().strip()
            return text.split("\n\n") if text else []
    except FileNotFoundError:
        return []

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[H\033[2J", end="")

def get_armor_name(tier):
    names = {
        1: "Trousers of Brainstorming",
        2: "Scribe's Robes",
        3: "Armor of Critique",
        4: "Editor's Crown"
    }
    return names.get(tier, "Masterpiece Regalia")

def count_words(text_list):
    total = 0
    for para in text_list:
        if not para.startswith("## "): total += len(para.split())
    return total

def render_ui(stats, monster, combat_log, current_run_paragraphs):
    clear_screen()
    armor_name = get_armor_name(stats['armor_tier'])
    print("=" * 60)
    print(f"🔮 MAGE GRIMOIRE: {PROJECT_NAME}  |  📍 LOCATION: {stats['current_zone'].upper()}")
    print(f"🪙 GOLD: {stats['gold']} | ✨ MANA XP: {stats['xp']} | 🖋️ COUNTER: {stats['total_words']} words")
    print(f"🔮 STONES: {stats['teleport_stones']} | 🪶 QUILLS: {stats['quills']} | 🍖 RATIONS: {stats['rations']}")
    print(f"💖 MENTAL ENERGY: {stats['hp']}/{stats['max_hp']} [{armor_name}]")
    print(f"🏘️ VILLAGE HEALTH: {stats['village_hp']}/50 | 👥 POP: {stats['villagers']}/100 | 🌿 GARDEN: {stats['garden_hp']}/25")
    print("=" * 60)
    
    if stats["current_zone"] == "Calligraphy Forests" and monster:
        print(f"👹 ADVERSARY: {monster['name']} (HP: {monster['hp']}/{monster['max_hp']})")
        print(bestiary.get_monster_ascii(monster['name']))
        print("=" * 60)
    
    print(f"🔮 SYSTEM LOG: {combat_log}")
    print("=" * 60)
    
    if stats["current_zone"] == "Calligraphy Forests":
        print(f"\n--- UNROLLED SPELL PARCHMENT ---")
        prose_display = "\n\n".join(current_run_paragraphs)
        if not prose_display:
            print("[Inscribe your prose below to strike the beast...]")
        else:
            if len(prose_display) > 600:
                prose_display = "..." + prose_display[-600:]
            paragraphs = prose_display.split("\n\n")
            for para in paragraphs:
                print("\n".join(textwrap.wrap(para, width=60)))
        print("-" * 60)
    
    # Context-dependent commands
    if stats["current_zone"] == "Pencilton":
        next_tier = stats['armor_tier'] + 1
        prices = {2: 50, 3: 120, 4: 300}
        shop_armor = f"/buyarmor ({prices[next_tier]}g)" if next_tier <= 4 else "MAX REGALIA"
        print(f"🏪 PENCILTON SHOP: /buyquill (10g) | /teleport_stone (30g) | {shop_armor}")
    else:
        print(f"🏪 REMOTE SUPPLIES: /buyquill (10g) | /teleport_stone (30g)")
        
    print("🎮 ACTIONS: /travel (Change Maps) | /teleport (Save & Return to Town) | /use_quill (Quick Save) | /rations | /exit")

def main():
    stats = load_game()
    full_backlog = load_manuscript()
    stats["total_words"] = count_words(full_backlog)
    
    # 1. RUN TIMED GOBLIN TUTORIAL IF APPLICABLE
    if TUTORIAL_MODE == "fight":
        import tutorial
        tutorial.run_goblin_tutorial(stats, full_backlog, clear_screen, save_game)
        
    # 2. RUN CHAPTER 1 INITIALIZATION IF NEW GAME
    if stats.get("story_milestone", 0) == 0:
        story.run_chapter_1(stats, full_backlog, clear_screen, save_game)
        
    # Check Daily World Decay state on bootup
    decay_messages = story.check_and_apply_daily_decay(stats, save_game, full_backlog)
    combat_log = decay_messages[0] if decay_messages else "Focus locked. Channelling circles active."

    current_monster = None
    if stats["current_zone"] == "Calligraphy Forests":
        current_monster = bestiary.get_monster_for_tier(stats["armor_tier"])
        
    current_run_paragraphs = []
    time.sleep(1)

    while True:
        story.check_story_milestones(stats, full_backlog, clear_screen, save_game)
        
 # --- FIXED SPECIALIZED REGION ROUTERS ---
        if stats["current_zone"] == "Biblioarchives":
            archive_cmd = archives.run_archive_sprint(stats, full_backlog, clear_screen, save_game)
            if archive_cmd:
                # If you typed a command, trick the engine into processing it below
                user_input = archive_cmd
            else:
                continue # Refresh the archive hub screen normally
                
        elif stats["current_zone"] == "Narrative Gardens":
            garden_cmd = gardens.run_garden_pomodoro(stats, full_backlog, clear_screen, save_game)
            if garden_cmd:
                user_input = garden_cmd
            else:
                continue
        else:
            # If we are in a normal zone (Pencilton/Forest), render the regular UI and get input
            render_ui(stats, current_monster, combat_log, current_run_paragraphs)
            try:
                user_input = input("\n> ")
            except (KeyboardInterrupt, EOFError):
                save_game(stats, full_backlog)
                break
            
        render_ui(stats, current_monster, combat_log, current_run_paragraphs)
        
        try:
            user_input = input("\n> ")
        except (KeyboardInterrupt, EOFError):
            save_game(stats, full_backlog)
            break

        cmd = user_input.strip()
        cmd_lower = cmd.lower()
        if not cmd: continue
        
        # --- ARCANE SHOP SYSTEMS ---
        if cmd_lower == "/teleport_stone":
            if stats["gold"] >= 30:
                stats["gold"] -= 30
                stats["teleport_stones"] += 1
                combat_log = "🏪 Acquired an Arcane Teleport Stone!"
                save_game(stats, full_backlog)
            else:
                combat_log = "❌ Insufficient gold coins!"
            continue

        if cmd_lower == "/buyquill":
            if stats["gold"] >= 10:
                stats["gold"] -= 10
                stats["quills"] += 1
                combat_log = "🏪 Purchased an Enchanted Writing Quill!"
                save_game(stats, full_backlog)
            else:
                combat_log = "❌ Insufficient gold for a Quill!"
            continue

        if cmd_lower == "/buyarmor":
            if stats["current_zone"] != "Pencilton":
                combat_log = "❌ Heavy vestments can only be custom tailored inside Pencilton!"
                continue
            next_tier = stats['armor_tier'] + 1
            prices = {2: 50, 3: 120, 4: 300}
            hp_values = {2: 20, 3: 35, 4: 50}
            
            if next_tier > 4:
                combat_log = "❌ Final vestment mastery achieved!"
            elif stats["gold"] >= prices[next_tier]:
                stats["gold"] -= prices[next_tier]
                stats["armor_tier"] = next_tier
                stats["max_hp"] = hp_values[next_tier]
                stats["hp"] = stats["max_hp"]
                combat_log = f"🛡️ Donned the {get_armor_name(next_tier)}! Max Energy raised to {stats['max_hp']}!"
                save_game(stats, full_backlog)
            else:
                combat_log = f"❌ Insufficient gold! You require {prices[next_tier]}g."
            continue

        # --- CONSUMABLES ---
        if cmd_lower == "/rations":
            if stats["rations"] > 0:
                stats["rations"] -= 1
                stats["hp"] = min(stats["max_hp"], stats["hp"] + 5)
                combat_log = "🍖 Consumed 1 bag of Rations! Restored +5 Mental Energy."
                save_game(stats, full_backlog)
            else:
                combat_log = "❌ You have no ration bags left in your satchel!"
            continue

        # --- TRAVEL NAVIGATION ENGINE ---
        if cmd_lower == "/travel":
            clear_screen()
            print("=" * 60)
            print("🗺️  BOOKVALE WORLD MAP — CHOOSE DESTINATION")
            print("=" * 60)
            print(" [1] Pencilton (Safe Town Hub)")
            print(" [2] Calligraphy Forests (Active Monster Hunting Zone)")
            print(" [3] Biblioarchives (Timed Healing & Wall Maintenance Sprints)")
            print(" [4] Narrative Gardens (25-minute Deep Focus Rituals)")
            print("=" * 60)
            choice = input("Enter destination (1-4): ").strip()
            
            zones = {"1": "Pencilton", "2": "Calligraphy Forests", "3": "Biblioarchives", "4": "Narrative Gardens"}
            if choice in zones:
                stats["current_zone"] = zones[choice]
                if stats["current_zone"] == "Calligraphy Forests":
                    current_monster = bestiary.get_monster_for_tier(stats["armor_tier"])
                current_run_paragraphs = []
                combat_log = f"Travelled successfully to {stats['current_zone']}."
                save_game(stats, full_backlog)
            else:
                combat_log = "❌ Invalid navigation vector coordinates rejected."
            continue

        # --- PROGRESS COALESCENCE SYSTEMS ---
        if cmd_lower == "/use_quill":
            if stats["quills"] > 0:
                if not current_run_paragraphs:
                    combat_log = "❌ Your spell parchment is blank! Channel some words first."
                    continue
                stats["quills"] -= 1
                readable_date = datetime.now().strftime("%Y-%m-%d %H:%M")
                full_backlog.append(f"## Quill Inscription Checkpoint: {readable_date}")
                full_backlog.extend(current_run_paragraphs)
                current_run_paragraphs = []
                combat_log = "🪶 The Enchanted Quill flashes! Progress anchored to your vault safely."
                save_game(stats, full_backlog)
            else:
                combat_log = "❌ You possess no Enchanted Quills!"
            continue

        if cmd_lower in ["/teleport", "/use_shield"]:
            if stats["teleport_stones"] > 0:
                if not current_run_paragraphs and stats["current_zone"] != "Calligraphy Forests":
                    combat_log = "❌ No active spells or environmental logs to seal."
                    continue
                
                stats["teleport_stones"] -= 1
                readable_date = datetime.now().strftime("%Y-%m-%d %H:%M")
                
                if current_run_paragraphs:
                    full_backlog.append(f"## Chapter Milestone: {readable_date}")
                    full_backlog.extend(current_run_paragraphs)
                    current_run_paragraphs = []

                stats["hp"] = stats["max_hp"]
                stats["current_zone"] = "Pencilton"
                combat_log = "🔮 shattered a Teleport Stone! Teleported safely to Pencilton. Energy restored!"
                save_game(stats, full_backlog)
            else:
                combat_log = "❌ Out of Teleport Stones! Buy one at the shop for 30g."
            continue

        if cmd_lower == "/exit":
            if current_run_paragraphs:
                readable_date = datetime.now().strftime("%Y-%m-%d %H:%M")
                full_backlog.append(f"## Session: {readable_date} (Forced Meditation Close)")
                full_backlog.extend(current_run_paragraphs)
            save_game(stats, full_backlog)
            break

        if cmd_lower == "/the_end":
            if stats.get("unlocked_the_end", False):
                stats["story_milestone"] = 7
                current_words = stats["total_words"]
                
                clear_screen()
                print("=" * 60)
                print("🖋️ FINISHING THE STORY: THE END")
                print("=" * 60)
                print("With a sigh, you realize there isn't any more for you to write for this tale. You raise your hands, whispering the final words to close the spell. \n\n\"The End.\"\n")
                print("The book swirls with energy, draining the last of your mana before vanishing with a quiet WOOSH. It has gone back to your tower, where it sits on your desk to await transcribing.")
                print("\nYou begin the long trek back to your tower. Perhaps another story will come to you along the way. Perhaps not. But for now, Bookvale is overflowing with flowers and ink, and you've earned a little rest.")
                print("=" * 60)
                save_game(stats, full_backlog)
                break
            else:
                combat_log = "❌ You cannot seal the grimoire yet! Reach your word goal first."
                continue

        # --- TYPING CASTING ENGINE CONTROLLER ---
        if stats["current_zone"] == "Calligraphy Forests" and current_monster:
            current_run_paragraphs.append(cmd)
            words_in_para = len(cmd.split())
            stats["total_words"] += words_in_para
            
            stats["hp"] -= 1
            current_monster["hp"] -= words_in_para
            combat_log = f"💥 Cast Spell! {words_in_para} syllables deal massive damage! (-1 Mental Energy)"
            
            if stats["hp"] <= 0:
                combat_log = f"🥱 EXHAUSTION! You collapsed. Unsaved active runes collapsed!"
                current_run_paragraphs = []
                stats["hp"] = stats["max_hp"] // 2
                stats["current_zone"] = "Pencilton"
                save_game(stats, full_backlog)
                continue

            if current_monster["hp"] <= 0:
                gold_earned = current_monster["gold"]
                xp_earned = current_monster["max_hp"] // 2
                stats["gold"] += gold_earned
                stats["xp"] += xp_earned
                
                readable_date = datetime.now().strftime("%Y-%m-%d %H:%M")
                full_backlog.append(f"## Forest Combat Victory: {readable_date}")
                full_backlog.extend(current_run_paragraphs)
                current_run_paragraphs = []
                
                print("\n" + "=" * 60)
                print(f"🏆 Victory! Banished {current_monster['name']}! (+{gold_earned}g, +{xp_earned} Spell XP)")
                print("=" * 60)
                
                if stats["hp"] < (stats["max_hp"] // 2):
                    print(f"⚠️ DANGER: Your Mental Energy is low ({stats['hp']}/{stats['max_hp']})!")
                    choice = input("Would you like to continue hunting or return to town for free? (stay/town): ").strip().lower()
                    if choice == "town":
                        stats["current_zone"] = "Pencilton"
                        stats["hp"] = stats["max_hp"]
                        print("\n✨ You head back to Pencilton with your spoils. Mental Energy fully restored!")
                        input("Press Enter to continue...")
                
                current_monster = bestiary.get_monster_for_tier(stats["armor_tier"])
                save_game(stats, full_backlog)
        else:
            combat_log = "❌ You are standing in a peaceful zone. Type /travel to go find monsters!"

if __name__ == "__main__":
    main()
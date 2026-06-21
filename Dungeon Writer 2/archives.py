# archives.py
import time

def get_archives_ascii():
    return """
         _______  ___________________________  _______
        |       ||                           ||       |
        |=======||     THE BIBLIOARCHIVES    ||=======|
        |   _   ||                           ||   _   |
        |  | |  ||   ____     ___     ____   ||  | |  |
        |  |_|  ||  [____]   [___]   [____]  ||  |_|  |
        |_______||___________________________||_______|
        |=======||===========================||=======|
        |       ||  _ _  _  _  _ _  _  _  _  ||       |
        |       || |_|_||_||_||_||_|_||_||_| ||       |
        |       || | | || || || | || || || | ||       |
        |_______||_|_|_||_||_||_|_||_||_||_|_||_______|
        ===============================================
        [ The scent of old parchment and glowing ink fills the air. ]"""

def get_activity_success_ascii(choice):
    """Returns specialized success visual cards to break up post-sprint feedback."""
    if choice in ["1", "3"]:
        return """
              +   +   +
            + [💖] [💖] +
              +   +   +
        [ The ink forms a soothing balm. Wounds are mended! ]"""
    elif choice == "2":
        return """
           ___   ___   ___
          |___| |___| |___|
          |___| |___| |___|
        [ The reinforced stonework thrums with defensive energy! ]"""
    elif choice == "4":
        return """
            ✨  👁️   ✨
             \\\\_|_//
             ( X_X ) -> ( ^_^ )
        [ Madness recedes. A wild creature calms down into a neighbor. ]"""
    return ""

def run_archive_sprint(stats, full_backlog, clear_screen_func, save_game_func):
    clear_screen_func()
    print("=" * 60)
    print("📚 WELCOME TO THE BIBLIOARCHIVES SPRINT WING")
    print("=" * 60)
    # Render the grand library entrance
    print(get_archives_ascii())
    print("=" * 60)
    print(" [1] Heal Villagers I  (5 Mins  | Every 50 words = 1 Villager + 1 Gold)")
    print(" [2] Repair Wards      (10 Mins | Every 100 words = 1 Wall HP + 1 Ration)")
    print(" [3] Heal Villagers II (15 Mins | Every 200 words = 4 Villagers + 5 Gold)")
    print(" [4] Sooth Beasts      (20 Mins | Every 500 words = 1 Mob Cleansed + 1 Stone)")
    print("=" * 60)
    
    choice = input("Select an activity (1-4) or type a command: ").strip()
    
    # 🌟 PASSTHROUGH PLUG: Catch commands so the main loop can intercept them!
    if choice.lower() in ["/travel", "/exit", "/teleport", "/rations"]:
        return choice.lower()
    if choice not in ["1", "2", "3", "4"]: 
        return None
    
    # Set the new durations in seconds
    durations = {
        "1": 5 * 60,   # 5 Mins
        "2": 10 * 60,  # 10 Mins
        "3": 15 * 60,  # 15 Mins
        "4": 20 * 60   # 20 Mins
    }
    target_time = durations[choice]
    
    input(f"\nPress Enter to begin your {target_time // 60} minute sprint loop. Ready... Set...")
    
    start_time = time.time()
    sprint_paragraphs = []
    
    print("\n⏳ TIMER ACTIVE! Start typing prose blocks below. Type /end_heal to stop early.\n")
    
    while True:
        elapsed = time.time() - start_time
        remaining = target_time - elapsed
        
        if remaining <= 0:
            print("\n⏰ Time is up! Calculating scribing yields...")
            break
            
        print(f"⏱️ [{int(remaining // 60)}m {int(remaining % 60)}s remaining]")
        user_text = input("> ").strip()
        
        if user_text.lower() == "/end_heal":
            print("\n💾 Early collection initiated...")
            break
            
        if user_text:
            sprint_paragraphs.append(user_text)
            
    # Calculate word total
    total_sprint_words = sum(len(p.split()) for p in sprint_paragraphs)
    stats["total_words"] += total_sprint_words
    
    # Save text unconditionally to backlog path without text formatting penalties
    if sprint_paragraphs:
        full_backlog.append(f"## Archive Sprint Session ({total_sprint_words} words)")
        full_backlog.extend(sprint_paragraphs)
        
    # Clear screen to cleanly drop the success summaries and art cards
    clear_screen_func()
    print("=" * 60)
    print(f"📝 SPRINT COMPLETE: Channeled {total_sprint_words} words safely.")
    print("=" * 60)
    print(get_activity_success_ascii(choice))
    print("=" * 60)
    
    # Process payout based on the brand new rewards architecture
    if choice == "1":
        yielded = total_sprint_words // 50
        stats["villagers"] = min(100, stats["villagers"] + yielded)
        stats["gold"] += yielded
        print(f"✨ Heal Villagers I Result: Restored {yielded} villagers and earned {yielded}g!")
        
    elif choice == "2":
        yielded = total_sprint_words // 100
        stats["village_hp"] = min(50, stats["village_hp"] + yielded)
        stats["rations"] += yielded
        print(f"🧱 Ward Repair Result: Reinforced walls by {yielded} HP and baked {yielded} Rations!")
        
    elif choice == "3":
        multipliers = total_sprint_words // 200
        villagers_saved = multipliers * 4
        gold_earned = multipliers * 5
        stats["villagers"] = min(100, stats["villagers"] + villagers_saved)
        stats["gold"] += gold_earned
        print(f"✨ Heal Villagers II Result: Restored {villagers_saved} villagers and earned {gold_earned}g!")
        
    elif choice == "4":
        mobs_cleansed = total_sprint_words // 500
        stones = total_sprint_words // 500  # 1 stone per 500 words match
        stats["villagers"] = min(100, stats["villagers"] + mobs_cleansed)
        stats["teleport_stones"] += stones
        print(f"🔮 Sooth Beasts Result: Calmed {mobs_cleansed} monsters and earned {stones} Teleport Stones!")

    save_game_func(stats, full_backlog)
    input("\nPress Enter to return to the archives hub...")
    return None
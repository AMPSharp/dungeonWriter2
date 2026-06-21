# gardens.py
import time

def get_garden_ascii(hp):
    """Returns an ASCII art string based on the garden's current health level."""
    # STAGE 1: Burnt Ash (0 - 5 HP)
    if hp <= 5:
        return """
          .   -  .  * .   -  .
         (     Ashen Wasteland   )
          ` .  -   .   * .  - . '
             ___...---...___
        ____/_/_/_/_/_/_/_/_\______
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        [ The garden is covered in thick, choking dragon ash. ]
        """
    
    # STAGE 2: Sprouting Seeds (6 - 12 HP)
    elif hp <= 12:
        return """
               .  ~  🌱  ~  .
         (   Life returns slowly   )
          ` .  ~  🌱  ~  🌱  ~  . '
                 __    __
           🌱   /  \  /  \   🌱
         ______/____\/____\______
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        [ Tiny green shoots are breaking through the soil! ]
        """
    
    # STAGE 3: Growing Flowers (13 - 19 HP)
    elif hp <= 19:
        return """
              (o)       (o)   
               |  \ _ /  |    🌸
             _\|/  (_)  \|/_ /
            (_/|\_     _/|\_)
         ______\_/_____/_\_______
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        [ Colorful buds are starting to uncurl in the breeze. ]
        """
    
    # STAGE 4: Full Bloom & Fairies! (20 - 25 HP)
    else:
        return """
             ✨  O     O  ✨
                /|\\   /|\\      ✨
         🌸     /_\\   /_\\    🌸
           (o)    |     |    (o)
          _\|/_  \|/   \|/  _\|/_
         ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        [ SUCCESS! Fairies dance above a sea of radiant blossoms! ]
        """


def run_garden_pomodoro(stats, full_backlog, clear_screen_func, save_game_func):
    clear_screen_func()
    print("=" * 60)
    print(f"🧚 WELCOME TO THE NARRATIVE GARDENS (CURRENT HEALTH: {stats['garden_hp']}/25)")
    print("=" * 60)
    
    # Display the dynamic ASCII art based on current health
    print(get_garden_ascii(stats["garden_hp"]))
    print("=" * 60)
    
    import time  # Ensure time module is locally contextually active if needed
    current_time = time.time()
    time_since_last = current_time - stats.get("last_garden_completion", 0.0)
    cooldown_remaining = 300 - time_since_last  # 5 mins cooldown
    
    if cooldown_remaining > 0:
        print(f"❌ The fairies are still recuperating! Wait {int(cooldown_remaining // 60)}m {int(cooldown_remaining % 60)}s.")
        input("\nPress Enter to return...")
        return None
        
    if stats.get("garden_runs_today", 0) >= 4:
        print("❌ You have hit your maximum focus meditation limit here for today (4/4).")
        print("Rest your eyes and return tomorrow when your daily ink limits clear.")
        input("\nPress Enter to return...")
        return None

    print("Welcome! Cultivate the garden via deep long-form work. Rules:")
    print("⚠️ Write un-interrupted for 25 minutes. No early stopping allowed.")
    
    confirm = input("\nAre you ready to initiate this trial? (y/n) or type command: ").strip()
    confirm_lower = confirm.lower()
    
    # 🌟 PASSTHROUGH PLUG: Catch commands or cancellations on confirmation prompt
    if confirm_lower in ["/travel", "/exit", "/teleport", "/rations"]:
        return confirm_lower
    if confirm_lower == 'n':
        return None
    elif confirm_lower != 'y':
        # Handles accidental mistypes gracefully by dropping back to hub
        return None

    # 25 minutes in seconds (Change to something smaller like 10 for testing!)
    pomodoro_duration = 25 * 60  
    garden_paragraphs = []
    start_time = time.time()
    
    print("\n🌿 Focus block active. Inscribe your masterpiece blocks below:")
    print("-" * 60)
    
    # Catch raw typing blocks continuously until time expires
    while time.time() - start_time < pomodoro_duration:
        rem = pomodoro_duration - (time.time() - start_time)
        print(f"\n⏱️ [Garden Focus Session: {int(rem // 60)}m {int(rem % 60)}s remaining]")
        
        para_input = input("> ").strip()
        para_lower = para_input.lower()
        
# 🌟 PASSTHROUGH PLUG: Allow mid-session escapes if emergency commands are called
        if para_lower in ["/travel", "/exit", "/teleport", "/rations"]:
            # Save whatever partial progress you managed before abandoning the timer
            if garden_paragraphs:
                garden_words = sum(len(p.split()) for p in garden_paragraphs)
                stats["total_words"] += garden_words
                full_backlog.append(f"## Garden Inscription [Interrupted] ({garden_words} words)")
                full_backlog.extend(garden_paragraphs)
                save_game_func(stats, full_backlog)
            return para_lower
            
        if para_input:
            garden_paragraphs.append(para_input)

    # Calculate final word success rewards
    garden_words = sum(len(p.split()) for p in garden_paragraphs)
    stats["total_words"] += garden_words
    stats["garden_hp"] = min(25, stats["garden_hp"] + 5)
    stats["garden_runs_today"] += 1
    stats["last_garden_completion"] = time.time()
    
    full_backlog.append(f"## Garden Cultivation Inscription ({garden_words} words)")
    full_backlog.extend(garden_paragraphs)
    
    save_game_func(stats, full_backlog)
    
    # Celebration screen showing the new garden state immediately
    clear_screen_func()
    print("=" * 60)
    print(f"🎉 SUCCESS! GARDEN HEALTH INCREASED TO: {stats['garden_hp']}/25")
    print("=" * 60)
    print(get_garden_ascii(stats["garden_hp"]))
    print("=" * 60)
    print(f"You typed {garden_words} words and breathed life back into Bookvale!")
    input("\nPress Enter to conclude your garden session...")
    return None
# story.py
import os
import textwrap

def run_chapter_1(stats, full_backlog, clear_screen_func, save_game_func):
    """
    Executes the Chapter 1 opening sequence where the player defines their
    overall writing goal and logs their story summary into the backlog.
    """
    clear_screen_func()
    print("=" * 60)
    print("📖 DUNGEON WRITER: CHAPTER 1 — THE CREATIVE SPARK")
    print("=" * 60)
    print("Lucy coughs a deep, wet hack that makes you wince. Just like always, her sleeve comes back stained with ink. And... just like always... she tries to apologize for being out of sorts. You hold up a hand to stop her.")
    print("\n\"You can't help it,\" you say before pointing to the next blank page of your grimoire. \"I have an idea but I don't know what to write. Then, when I did figure something out, Sir Flame-butt interrupted me!")
    print("What do I do? I can't focus, and Bookvale is crawling with monsters now.\"")
    print("\nLucy lays her head on her desk, only succeeding in having another coughing fit. After it subsides, she leans back in her chair instead. \"Remember that workshop we went to last summer? You need to just write. Start with a few goals, and then write until you reach them.\"")
    print("\n\"But how do I write if I don't know what to write? They said to write what you know, but I don't know what I know to write it.\"")
    print("\nLucy smiles, but she seems a little sad to you. Her pointy ears are too pale, and her eyes look hazy like she has a headache from all her coughing. \"Let's start with a goal. How big do you want your story to be? Try writing down a number.\"")
    print("=" * 60)

    # 1. Capture Target Word Count Goal
    while True:
        goal_input = input("\nEnter your target word count goal (e.g., 5000): ").strip()
        if goal_input.isdigit() and int(goal_input) > 0:
            stats["target_goal"] = int(goal_input)
            break
        print("❌ Please enter a valid number greater than 0.")

    print("\n\"Good, now tell me what you want the story to be about.\"")
    print("-" * 60)
    
    # 2. Capture Story Summary
    while True:
        summary_input = input("\nInscribe your story summary/premise below:\n> ").strip()
        if summary_input:
            break
        print("❌ Your summary cannot be completely blank.")

    # 3. Calculate metrics and log to files
    summary_words = len(summary_input.split())
    stats["total_words"] += summary_words
    
    # Securely structure the summary entry into the markdown backlog
    full_backlog.append("## Chapter 1: Manifested Story Premise")
    full_backlog.append(summary_input)
    
    # Progress the milestone tracker so this scene doesn't loop
    stats["story_milestone"] = 1 
    save_game_func(stats, full_backlog)

    # 4. Outro Narrative Segment
    print("\n" + "=" * 60)
    print(f"Lucy's smile widens with pride: \"That was already {summary_words} words into your story.\"")
    print("\n\"Oh,\" you say. \"I guess that wasn't so hard.\"")
    print("\nLucy nods before slowly rising from the table. \"Go wander around, tell the monsters and people of Bookvale about your story and eventually, you will have written it all and will be ready for the final stage.\"")
    print("\n\"Sealing the grimoire,\" you say in a breathless whisper. Lucy nods,")
    print("then gently ushers you out of the house so she can rest.")
    print("\n\"Travel,\" she says again. \"There are people that need healing from your stories, and monsters that need slain. Just talk to them as you did to me, and remember to use your quill to bind your words to the grimoire.\"")
    print("\nThe door of Lucy's cottage closes behind you, and a wide open world")
    print("stands before you. Where will you go?")
    print("=" * 60)
    input("\nPress Enter to begin exploring Bookvale...")

def check_and_apply_daily_decay(stats, save_game_func, full_backlog):
    """
    Tracks time passed since last login to handle world state logic.
    Returns a status message for the main game interface.
    """
    # If it's a brand new game or first day, just initialize smoothly
    if not stats.get("last_day_reset_timestamp"):
        stats["last_day_reset_timestamp"] = "initialized"
        save_game_func(stats, full_backlog)
        return ["✨ The sun rises over Bookvale. Your journey begins!"]
        
    return ["Focus locked. Channelling circles active."]

def check_story_milestones(stats, full_backlog, clear_screen_func, save_game_func):
    """
    Checks long-term progress metrics (post-Chapter 1) to trigger narrative beats.
    Updated word count milestones to scale dynamically based on percentage thresholds
    of the player's custom target goal, complete with a choosing finale.
    """
    current_words = stats["total_words"]
    milestone_level = stats["story_milestone"]
    
    # Fallback default goal if it somehow isn't in stats (e.g., legacy saves)
    target_goal = stats.get("target_goal", 5000)
    
    # Calculate percentage increments dynamically
    m_10 = target_goal * 0.10
    m_25 = target_goal * 0.25
    m_50 = target_goal * 0.50
    m_75 = target_goal * 0.75
    m_90 = target_goal * 0.90
    m_100 = target_goal

    # --- MILESTONE 1: 10% COMPLETED ---
    if current_words >= m_10 and milestone_level < 2:
        clear_screen_func()
        print("=" * 60)
        print(f"📖 NARRATIVE MILESTONE: 10% COMPLETED ({current_words}/{target_goal} words)")
        print("=" * 60)
        print("It's hard to believe that already 10 percent of the grimoire is now filled with your words. Each monster you've fought, each person you've helped, makes it a little easier to find the next word.")
        print("=" * 60)
        input("\nPress Enter to continue your journey...")
        stats["story_milestone"] = 2
        save_game_func(stats, full_backlog)

    # --- MILESTONE 2: 25% COMPLETED ---
    elif current_words >= m_25 and milestone_level < 3:
        clear_screen_func()
        print("=" * 60)
        print(f"📖 NARRATIVE MILESTONE: 25% COMPLETED ({current_words}/{target_goal} words)")
        print("=" * 60)
        print("A quarter of the way there... There have been hiccups and changes, and you're not sure you're actually that far through the story, but that's how many pages of your grimoire you've filled.")
        print("\nThe world around you has begun to recover its magic. The grass is green again. The rivers are flowing with the Ink that sustains your magic. Burnout is still flying overhead, threatening to turn everything to ash again, but for now, he stays back.")
        print("=" * 60)
        input("\nPress Enter to continue your journey...")
        stats["story_milestone"] = 3
        save_game_func(stats, full_backlog)

    # --- MILESTONE 3: 50% COMPLETED ---
    elif current_words >= m_50 and milestone_level < 4:
        clear_screen_func()
        print("=" * 60)
        print(f"📖 NARRATIVE MILESTONE: 50% COMPLETED ({current_words}/{target_goal} words)")
        print("=" * 60)
        print("Halfway there. Fruit blossoms tremble in the air overhead. There are wheat and oats growing in the fields once more. You don't worry how many pages are left in the grimoire; there's plenty of space to finish the tale.")
        print("=" * 60)
        input("\nPress Enter to continue your journey...")
        stats["story_milestone"] = 4
        save_game_func(stats, full_backlog)

    # --- MILESTONE 4: 75% COMPLETED ---
    elif current_words >= m_75 and milestone_level < 5:
        clear_screen_func()
        print("=" * 60)
        print(f"📖 NARRATIVE MILESTONE: 75% COMPLETED ({current_words}/{target_goal} words)")
        print("=" * 60)
        print("A songbird lands on the brim of your hat. Its sweet song brings images of summer skies before it leaves again. The field before you bends before the wind in rolling emerald waves.")
        print("\nAbove you, the dragon swoops overhead, pulling away as he decides not to burn the fields today. There's only a quarter of your grimoire left to fill. You hope it can hold all of your story.")
        print("=" * 60)
        input("\nPress Enter to continue your journey...")
        stats["story_milestone"] = 5
        save_game_func(stats, full_backlog)

    # --- MILESTONE 5: 90% COMPLETED ---
    elif current_words >= m_90 and milestone_level < 6:
        clear_screen_func()
        print("=" * 60)
        print(f"📖 NARRATIVE MILESTONE: 90% COMPLETED ({current_words}/{target_goal} words)")
        print("=" * 60)
        print("The grimoire you hold in your hands is nearly filled to the brim with your words, both good and bad. You're tempted to seal it now, to finish the story in a fresh grimoire. But that wouldn't be fair to the leather binding that has carried you this far.")
        print("\nBeneath you, the world trembles. A wave of ash rises into the sky. You consider telling Burnout to knock off his antics, but instead choose to focus again on your story. Some other Paper Mage or Ink Witch will deal with the dragon.")
        print("=" * 60)
        input("\nPress Enter to continue your journey...")
        stats["story_milestone"] = 6
        save_game_func(stats, full_backlog)

# --- MILESTONE 6: 100% COMPLETED (THE FINALE CHOICE) ---
    elif current_words >= m_100 and milestone_level < 7:
        clear_screen_func()
        print("=" * 60)
        print(f"✨ GRAND FINALE MILESTONE: 100% COMPLETED ({current_words}/{target_goal} words)")
        print("=" * 60)
        print("You filled the last page...")
        print("\nYou thought there was another page left—one that you could intentionally leave blank, but you miscalculated. You were in the middle of a thought, too. The grimoire glows, lifting out of your hands to flip through the written pages. It's ready to be sealed, but you're not sure if you're ready for that yet.")
        print("=" * 60)
        
        while True:
            print("\nWHAT WILL YOU DO, Mage?")
            print(" [A] Seal the Grimoire and finish the story.")
            print(" [B] Grab the book. You're not ready for the story to end.")
            
            choice = input("\n> ").strip().upper()
            if choice == 'A':
                clear_screen_func()
                print("=" * 60)
                print("🖋️ FINISHING THE STORY: THE END")
                print("=" * 60)
                print("With a sigh, you realize there isn't any more for you to write for this tale. You raise your hands, whispering the final words to close the spell. \n\n\"The End.\"\n")
                print("The book swirls with energy, draining the last of your mana before vanishing with a quiet WOOSH. It has gone back to your tower, where it sits on your desk to await transcribing.")
                print("\nYou begin the long trek back to your tower. Perhaps another story will come to you along the way. Perhaps not. But for now, Bookvale is overflowing with flowers and ink, and you've earned a little rest.")
                print("=" * 60)
                
                stats["story_milestone"] = 7
                save_game_func(stats, full_backlog)
                input("\nPress Enter to close the grimoire session...")
                break
                
            elif choice == 'B':
                clear_screen_func()
                print("=" * 60)
                print("📚 GRAB THE BOOK: THE TALE CONTINUES")
                print("=" * 60)
                print("No. You're not done yet. Grabbing the book, you flip open to the last page only to find it blank! The grimoire has responded to your need. It now creates new blank pages so it can hold the rest of the tale.")
                print("\nYour travels in Bookvale continue. Where will you go?")
                print("=" * 60)
                print("\n✨ UNLOCKED NEW POWER: You can type /the_end anytime from your actions panel to officially seal your story when you're ready!")
                print("-" * 60)
                
                # Expand goal so the display stays clean, but unlock the toggle command
                stats["target_goal"] = int(target_goal * 1.25)
                stats["unlocked_the_end"] = True 
                stats["story_milestone"] = 6 # Keep them on milestone 6 so they can play
                
                save_game_func(stats, full_backlog)
                input("\nPress Enter to return to Bookvale...")
                break
            else:
                print("❌ Focus your intent. Choose A or B.")
# tutorial.py
import time

def run_goblin_tutorial(stats, full_backlog, clear_screen_func, save_game_func):
    """
    Executes the introductory timed tutorial sequence against the tutorial goblin
    and the healing event for Lucy.
    """
    
    # ==========================================
    # STAGE 1: THE TUTORIAL GOBLIN ENCOUNTER
    # ==========================================
    goblin_hp = 25
    
    while goblin_hp > 0:
        clear_screen_func()
        print("=" * 60)
        print(f"👹 TUTORIAL ADVERSARY: Word-Eating Goblin (HP: {goblin_hp}/25)")
        print("=" * 60)
        print("Uh-oh... there's a goblin in the way! You're going to have to figure out something to write fast before it eats your spellbook!")
        print("\n[Inscribe prose below to deal damage! 1 word = 1 damage]")
        print("-" * 60)
        
        user_input = input("\n> ").strip()
        if not user_input:
            continue
            
        word_count = len(user_input.split())
        goblin_hp -= word_count
        
        # Track word updates securely to the master logs
        stats["total_words"] += word_count
        full_backlog.append(user_input)
        
        if goblin_hp > 0:
            print("\n" + "-" * 60)
            print("Uh-oh... The goblin ate the words right off your page, leaving you with only your name and your book's title! The monster still looks hungry, though. WATCH OUT!")
            print("-" * 60)
            input("\nPress Enter to brace yourself...")

    # ==========================================
    # STAGE 2: REACHING LUCY'S COTTAGE
    # ==========================================
    clear_screen_func()
    print("=" * 60)
    print("📖 TUTORIAL: REACHING LUCY'S COTTAGE")
    print("=" * 60)
    print("Whew, you wrote that just in time! But you're pretty tired now. Who knew writing just a few words took that much out of you?")
    print("\nLucy's tower was less a tower and more a tiny stone cottage. You step through the ashen garden, sighing as you realize the dragon has burned her roses yet again.")
    print("\nAt the doorstep, you grab the heavy knocker...")
    print("BANG... BANG... BANG...")
    print("No one answers. You try again.")
    print("BANG... BANG... BANG...")
    print("\nThe door gives way with an unsettling creak. There is still no")
    print("answer, but now the door is open.")
    print("\nInside, at a table with an unfinished glass of water, Lucy sleeps with her head down. Underneath her flowing locks of brown hair, you see the blank pages of her grimoire.")
    print("\n'Lucy?' You reach out and shake her shoulder. No response. It looks like you need to help her.")
    print("=" * 60)
    input("\nPress Enter to prepare your healing spell...")

    # ==========================================
    # STAGE 3: THE TIMED HEALING MECHANIC
    # ==========================================
    while True:
        clear_screen_func()
        print("=" * 60)
        print("⚡ CRITICAL EVENT: HEAL LUCY")
        print("=" * 60)
        print("Type a healing spell paragraph of AT LEAST 10 words.")
        print("CRITICAL LIMIT: You must submit it in LESS THAN 30 seconds!")
        print("=" * 60)
        print("\nPress Enter when you are ready to start the timer...")
        input()
        
        print("\n⏳ TIMER STARTED! Inscribe your 10+ word spell now:")
        start_time = time.time()
        spell_input = input("\n> ").strip()
        end_time = time.time()
        
        elapsed_seconds = end_time - start_time
        spell_words = len(spell_input.split())
        
        # Log any text typed during the trial safely
        if spell_words > 0:
            stats["total_words"] += spell_words
            full_backlog.append(spell_input)
            
        print(f"\n⏱️ Spell complete! Time taken: {elapsed_seconds:.1f} seconds | Words: {spell_words}")
        
        # Validation checks
        if elapsed_seconds < 30 and spell_words >= 10:
            print("\n" + "=" * 60)
            print("Whew, she's awake now! Maybe she can finally help you with")
            print("that story idea... (Tutorial completed!)")
            print("=" * 60)
            
            # Grant introductory rewards for completing the tutorial safely
            stats["gold"] += 20
            stats["xp"] += 15
            save_game_func(stats, full_backlog)
            
            input("\nPress Enter to venture out into Bookvale...")
            break
        else:
            print("\n" + "-" * 60)
            if elapsed_seconds >= 30:
                print("❌ TOO SLOW! The dragon's residual ash dulled your focus.")
            if spell_words < 10:
                print(f"❌ TOO SHORT! You only wrote {spell_words}/10 required words.")
            print("\nUh-oh... She must have really exhausted herself this time.")
            print("Let's try again!")
            print("-" * 60)
            input("\nPress Enter to center your Creative Spark...")
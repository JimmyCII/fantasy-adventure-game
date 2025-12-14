"""
fantasy-Style Text Adventure Game
A text-based adventure game where players explore locations, collect items,
encounter challenges, and complete a quest to defeat the Dragon of Shadowmere.

Python Concepts Used:
- Variables: player stats, game state
- Lists: inventory, locations
- Loops: game loop, menu navigation
- Conditionals: player choices, combat outcomes
- Functions: modular game logic
"""

import random

# ============================================================================
# GAME DATA - Variables and Lists
# ============================================================================

# Player stats (variables)
player = {
    "name": "",
    "health": 100,
    "max_health": 100,
    "attack": 10,
    "defense": 5,
    "gold": 20
}

# Player inventory (list)
inventory = []

# Available locations (list of dictionaries)
locations = [
    {
        "name": "Village of Elderbrook",
        "description": "A peaceful village with cobblestone streets and friendly townsfolk. A tavern and shop stand nearby.",
        "visited": False
    },
    {
        "name": "Whispering Forest",
        "description": "A dark, mysterious forest where the trees seem to whisper ancient secrets. Danger lurks within.",
        "visited": False
    },
    {
        "name": "Crystal Cave",
        "description": "A cave filled with glowing crystals that illuminate the darkness. Strange creatures dwell here.",
        "visited": False
    },
    {
        "name": "Dragon's Lair",
        "description": "The dreaded lair of the Dragon of Shadowmere. Only the bravest adventurers dare enter.",
        "visited": False
    }
]

# Items available in the shop (list)
shop_items = [
    {"name": "Health Potion", "price": 15, "effect": "Restores 30 health"},
    {"name": "Iron Sword", "price": 25, "effect": "Increases attack by 5"},
    {"name": "Leather Shield", "price": 20, "effect": "Increases defense by 3"},
    {"name": "Magic Amulet", "price": 40, "effect": "Increases max health by 20"}
]

# Game state
game_active = True
dragon_defeated = False


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_valid_input(prompt: str, valid_options: list) -> str:
    """
    Get validated input from the player.
    
    Args:
        prompt: The message to display to the player
        valid_options: List of valid input options
        
    Returns:
        The validated user input (lowercase)
    """
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_options:
            return user_input
        print(f"Invalid choice. Please enter one of: {', '.join(valid_options)}")


def display_separator():
    """Display a visual separator line."""
    print("\n" + "=" * 60 + "\n")


def display_player_status():
    """Display current player stats and inventory."""
    print(f"\n--- {player['name']}'s Status ---")
    print(f"Health: {player['health']}/{player['max_health']}")
    print(f"Attack: {player['attack']} | Defense: {player['defense']}")
    print(f"Gold: {player['gold']}")
    print(f"Inventory: {', '.join(inventory) if inventory else 'Empty'}")


# ============================================================================
# GAME FUNCTIONS
# ============================================================================

def start_game():
    """
    Initialize the game and get player name.
    Displays welcome message and sets up initial game state.
    """
    display_separator()
    print("⚔️  WELCOME TO THE REALM OF SHADOWMERE ⚔️")
    print("A Fantasy-Style Text Adventure Game")
    display_separator()
    
    print("In the land of Shadowmere, a fearsome dragon threatens the kingdom.")
    print("You are a brave adventurer chosen to defeat this ancient evil.")
    print("Explore the land, gather items, and prepare for the ultimate battle!\n")
    
    player["name"] = input("Enter your adventurer's name: ").strip()
    if not player["name"]:
        player["name"] = "Hero"
    
    print(f"\nWelcome, {player['name']}! Your quest begins in the Village of Elderbrook.")
    inventory.append("Rusty Dagger")
    print("You start with a Rusty Dagger and 20 gold coins.\n")


def main_menu():
    """
    Display the main game menu and handle player choices.
    
    Returns:
        The player's menu choice
    """
    print("\n--- What would you like to do? ---")
    print("1. Explore a location")
    print("2. Check status")
    print("3. Visit shop")
    print("4. Use item")
    print("5. Quit game")
    
    choice = get_valid_input("Enter your choice (1-5): ", ["1", "2", "3", "4", "5"])
    return choice


def explore_location():
    """
    Allow player to choose and explore a location.
    Handles different encounters based on location.
    """
    print("\n--- Available Locations ---")
    for i, loc in enumerate(locations, 1):
        visited_marker = " (Visited)" if loc["visited"] else ""
        print(f"{i}. {loc['name']}{visited_marker}")
    print(f"{len(locations) + 1}. Go back")
    
    valid_choices = [str(i) for i in range(1, len(locations) + 2)]
    choice = get_valid_input("Where would you like to go? ", valid_choices)
    
    if choice == str(len(locations) + 1):
        return
    
    location_index = int(choice) - 1
    location = locations[location_index]
    
    display_separator()
    print(f"📍 {location['name']}")
    print(location["description"])
    location["visited"] = True
    
    # Handle location-specific encounters
    if location["name"] == "Village of Elderbrook":
        village_encounter()
    elif location["name"] == "Whispering Forest":
        forest_encounter()
    elif location["name"] == "Crystal Cave":
        cave_encounter()
    elif location["name"] == "Dragon's Lair":
        dragon_encounter()


def village_encounter():
    """
    Handle encounters in the Village of Elderbrook.
    Player can talk to villagers and receive hints.
    """
    print("\nThe villagers greet you warmly.")
    print("An old sage approaches you...")
    print('\n"Brave adventurer," he says, "to defeat the dragon, you must first')
    print('find the Crystal Sword hidden in the Crystal Cave. Without it,')
    print('the dragon\'s scales cannot be pierced!"')
    
    # Random chance to receive gold from grateful villagers
    if random.random() < 0.5:
        gold_found = random.randint(5, 15)
        player["gold"] += gold_found
        print(f"\nA grateful villager gives you {gold_found} gold coins!")


def forest_encounter():
    """
    Handle encounters in the Whispering Forest.
    Player may encounter friendly or hostile creatures.
    """
    print("\nYou venture deep into the forest...")
    
    encounters = ["goblin", "fairy", "wolf", "treasure"]
    encounter = random.choice(encounters)
    
    if encounter == "goblin":
        print("\n⚔️ A wild Goblin appears!")
        combat("Goblin", health=30, attack=8, gold_reward=10)
    elif encounter == "fairy":
        print("\n✨ A friendly forest fairy appears!")
        print("She sprinkles healing dust on you.")
        heal_amount = 20
        player["health"] = min(player["health"] + heal_amount, player["max_health"])
        print(f"You recovered {heal_amount} health!")
    elif encounter == "wolf":
        print("\n🐺 A fierce Wolf blocks your path!")
        combat("Wolf", health=25, attack=10, gold_reward=8)
    else:
        gold_found = random.randint(10, 25)
        player["gold"] += gold_found
        print(f"\n💰 You found a hidden treasure chest containing {gold_found} gold!")


def cave_encounter():
    """
    Handle encounters in the Crystal Cave.
    Player can find the Crystal Sword needed to defeat the dragon.
    """
    print("\nThe crystals illuminate your path as you explore the cave...")
    
    if "Crystal Sword" in inventory:
        print("You've already claimed the Crystal Sword from this cave.")
        print("The cave feels peaceful now.")
        return
    
    print("\n🦇 A Giant Bat swoops down to attack!")
    victory = combat("Giant Bat", health=35, attack=12, gold_reward=15)
    
    if victory:
        print("\n✨ With the bat defeated, you notice a glowing sword embedded in a crystal!")
        print("You pull it free - it's the legendary CRYSTAL SWORD!")
        inventory.append("Crystal Sword")
        player["attack"] += 15
        print("Your attack power has increased by 15!")


def dragon_encounter():
    """
    Handle the final boss encounter with the Dragon of Shadowmere.
    Requires Crystal Sword to have a chance at victory.
    """
    global dragon_defeated, game_active
    
    if dragon_defeated:
        print("\nThe dragon has been defeated. Peace has returned to the lair.")
        return
    
    print("\n🐉 THE DRAGON OF SHADOWMERE AWAKENS!")
    print("Its massive form fills the cavern, scales glittering like obsidian.")
    
    if "Crystal Sword" not in inventory:
        print("\n⚠️ You don't have the Crystal Sword!")
        print("Your attacks bounce harmlessly off the dragon's scales.")
        print("You barely escape with your life!")
        player["health"] = max(10, player["health"] - 40)
        print(f"You took 40 damage fleeing! Current health: {player['health']}")
        return
    
    print("\nYour Crystal Sword glows with ancient power!")
    print("The dragon recognizes the legendary blade and roars in fury!")
    
    victory = combat("Dragon of Shadowmere", health=100, attack=20, gold_reward=100)
    
    if victory:
        dragon_defeated = True
        print("\n🎉 VICTORY! 🎉")
        print("The Dragon of Shadowmere has been defeated!")
        print("You are hailed as the greatest hero the realm has ever known!")
        print("\n*** CONGRATULATIONS! YOU HAVE COMPLETED THE QUEST! ***")
        
        choice = get_valid_input("\nWould you like to continue exploring? (yes/no): ", ["yes", "no"])
        if choice == "no":
            game_active = False


def combat(enemy_name: str, health: int, attack: int, gold_reward: int) -> bool:
    """
    Handle combat between the player and an enemy.
    
    Args:
        enemy_name: Name of the enemy
        health: Enemy's starting health
        attack: Enemy's attack power
        gold_reward: Gold earned for defeating the enemy
        
    Returns:
        True if player wins, False if player flees or is defeated
    """
    enemy_health = health
    
    print(f"\n--- Battle with {enemy_name} ---")
    print(f"{enemy_name} Health: {enemy_health}")
    
    while enemy_health > 0 and player["health"] > 0:
        print(f"\nYour Health: {player['health']} | {enemy_name} Health: {enemy_health}")
        print("1. Attack")
        print("2. Use Health Potion")
        print("3. Flee")
        
        choice = get_valid_input("Choose your action: ", ["1", "2", "3"])
        
        if choice == "1":
            # Player attacks
            damage = random.randint(player["attack"] - 3, player["attack"] + 5)
            enemy_health -= damage
            print(f"You strike the {enemy_name} for {damage} damage!")
            
        elif choice == "2":
            if "Health Potion" in inventory:
                inventory.remove("Health Potion")
                heal = 30
                player["health"] = min(player["health"] + heal, player["max_health"])
                print(f"You drink a Health Potion and recover {heal} health!")
            else:
                print("You don't have any Health Potions!")
                continue
                
        elif choice == "3":
            escape_chance = random.random()
            if escape_chance > 0.3:
                print("You successfully flee from battle!")
                return False
            else:
                print("You failed to escape!")
        
        # Enemy attacks if still alive
        if enemy_health > 0:
            enemy_damage = random.randint(attack - 2, attack + 3)
            actual_damage = max(1, enemy_damage - player["defense"])
            player["health"] -= actual_damage
            print(f"The {enemy_name} attacks you for {actual_damage} damage!")
    
    if player["health"] <= 0:
        print("\n💀 You have been defeated!")
        print("GAME OVER")
        return False
    else:
        print(f"\n⚔️ You defeated the {enemy_name}!")
        player["gold"] += gold_reward
        print(f"You earned {gold_reward} gold!")
        return True


def visit_shop():
    """
    Allow player to buy items from the shop.
    Displays available items and handles purchase logic.
    """
    print("\n--- Welcome to the Village Shop ---")
    print(f"Your gold: {player['gold']}\n")
    
    for i, item in enumerate(shop_items, 1):
        print(f"{i}. {item['name']} - {item['price']} gold ({item['effect']})")
    print(f"{len(shop_items) + 1}. Leave shop")
    
    valid_choices = [str(i) for i in range(1, len(shop_items) + 2)]
    choice = get_valid_input("What would you like to buy? ", valid_choices)
    
    if choice == str(len(shop_items) + 1):
        print("Thanks for visiting!")
        return
    
    item_index = int(choice) - 1
    item = shop_items[item_index]
    
    if player["gold"] >= item["price"]:
        player["gold"] -= item["price"]
        
        # Apply item effects
        if item["name"] == "Health Potion":
            inventory.append("Health Potion")
        elif item["name"] == "Iron Sword":
            player["attack"] += 5
            inventory.append("Iron Sword")
        elif item["name"] == "Leather Shield":
            player["defense"] += 3
            inventory.append("Leather Shield")
        elif item["name"] == "Magic Amulet":
            player["max_health"] += 20
            player["health"] += 20
            inventory.append("Magic Amulet")
        
        print(f"You purchased {item['name']}!")
    else:
        print("You don't have enough gold!")


def use_item():
    """
    Allow player to use items from their inventory.
    """
    if not inventory:
        print("\nYour inventory is empty!")
        return
    
    print("\n--- Your Inventory ---")
    usable_items = [item for item in inventory if item == "Health Potion"]
    
    if not usable_items:
        print("You have no usable items.")
        print(f"Inventory: {', '.join(inventory)}")
        return
    
    for i, item in enumerate(usable_items, 1):
        print(f"{i}. {item}")
    print(f"{len(usable_items) + 1}. Cancel")
    
    valid_choices = [str(i) for i in range(1, len(usable_items) + 2)]
    choice = get_valid_input("Which item would you like to use? ", valid_choices)
    
    if choice == str(len(usable_items) + 1):
        return
    
    item_name = usable_items[int(choice) - 1]
    
    if item_name == "Health Potion":
        if player["health"] >= player["max_health"]:
            print("Your health is already full!")
        else:
            inventory.remove("Health Potion")
            heal = 30
            player["health"] = min(player["health"] + heal, player["max_health"])
            print(f"You drink a Health Potion and recover {heal} health!")


def end_game():
    """
    Display end game message and final stats.
    """
    display_separator()
    print("Thank you for playing THE REALM OF SHADOWMERE!")
    print("\n--- Final Stats ---")
    display_player_status()
    
    if dragon_defeated:
        print("\n🏆 Quest Status: COMPLETED - Dragon Defeated!")
    else:
        print("\n📜 Quest Status: Incomplete - The dragon still lives...")
    
    display_separator()


# ============================================================================
# MAIN GAME LOOP
# ============================================================================

def main():
    """
    Main game loop that runs the adventure.
    Demonstrates use of while loop for continuous gameplay.
    """
    global game_active
    
    start_game()
    
    while game_active and player["health"] > 0:
        choice = main_menu()
        
        if choice == "1":
            explore_location()
        elif choice == "2":
            display_player_status()
        elif choice == "3":
            visit_shop()
        elif choice == "4":
            use_item()
        elif choice == "5":
            confirm = get_valid_input("Are you sure you want to quit? (yes/no): ", ["yes", "no"])
            if confirm == "yes":
                game_active = False
    
    end_game()


# Run the game
if __name__ == "__main__":
    main()

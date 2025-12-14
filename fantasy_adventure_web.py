"""
DnD-Style Text Adventure Game - Web Version
Host locally using Flask so others can play via browser.

To run:
1. Install Flask: pip install flask
2. Run this script: python fantasy_adventure_web.py
3. Open browser to: http://localhost:5000
4. For others on your network: http://YOUR_IP:5000

To find your IP address:
- Windows: ipconfig (look for IPv4 Address)
- Mac/Linux: ifconfig or ip addr
"""

from flask import Flask, render_template_string, request, session, redirect, url_for
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# HTML Template with DnD styling
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Realm of Shadowmere - Fantasy Adventure</title>
    <style>
        * { box-sizing: border-box; }
        body {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #e8d5b7;
            font-family: 'Georgia', serif;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(0,0,0,0.6);
            border: 3px solid #c9a227;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 0 30px rgba(201, 162, 39, 0.3);
        }
        h1 {
            text-align: center;
            color: #c9a227;
            text-shadow: 2px 2px 4px #000;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        h2 {
            color: #c9a227;
            border-bottom: 2px solid #c9a227;
            padding-bottom: 10px;
        }
        .subtitle {
            text-align: center;
            font-style: italic;
            margin-bottom: 30px;
        }
        .stats-bar {
            display: flex;
            justify-content: space-around;
            background: rgba(201, 162, 39, 0.2);
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        .stat {
            text-align: center;
            padding: 5px 15px;
        }
        .stat-label { font-size: 0.9em; color: #aaa; }
        .stat-value { font-size: 1.3em; font-weight: bold; color: #c9a227; }
        .game-text {
            background: rgba(0,0,0,0.4);
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
            line-height: 1.8;
            border-left: 4px solid #c9a227;
        }
        .choices {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .choice-btn {
            background: linear-gradient(180deg, #2d2d44 0%, #1a1a2e 100%);
            color: #e8d5b7;
            border: 2px solid #c9a227;
            padding: 15px 25px;
            font-size: 1.1em;
            cursor: pointer;
            border-radius: 5px;
            transition: all 0.3s;
            font-family: 'Georgia', serif;
        }
        .choice-btn:hover {
            background: linear-gradient(180deg, #c9a227 0%, #a07d1c 100%);
            color: #1a1a2e;
            transform: translateX(10px);
        }
        input[type="text"] {
            background: rgba(0,0,0,0.5);
            border: 2px solid #c9a227;
            color: #e8d5b7;
            padding: 15px;
            font-size: 1.1em;
            width: 100%;
            border-radius: 5px;
            margin-bottom: 15px;
            font-family: 'Georgia', serif;
        }
        .inventory {
            background: rgba(201, 162, 39, 0.1);
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
        }
        .inventory h3 { margin-top: 0; color: #c9a227; }
        .message {
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 15px;
            text-align: center;
        }
        .message-success { background: rgba(39, 174, 96, 0.3); border: 1px solid #27ae60; }
        .message-danger { background: rgba(231, 76, 60, 0.3); border: 1px solid #e74c3c; }
        .message-info { background: rgba(52, 152, 219, 0.3); border: 1px solid #3498db; }
        .health-bar {
            background: #333;
            border-radius: 10px;
            overflow: hidden;
            height: 20px;
            margin: 5px 0;
        }
        .health-fill {
            background: linear-gradient(90deg, #e74c3c, #27ae60);
            height: 100%;
            transition: width 0.5s;
        }
        footer {
            text-align: center;
            margin-top: 30px;
            color: #666;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        {{ content | safe }}
    </div>
    <footer>Fantasy Adventure Game - Created with Python & Flask</footer>
</body>
</html>
"""

def get_player():
    """Get or initialize player session data."""
    if 'player' not in session:
        session['player'] = {
            'name': '',
            'health': 100,
            'max_health': 100,
            'attack': 10,
            'defense': 5,
            'gold': 20,
            'inventory': ['Rusty Dagger'],
            'locations_visited': [],
            'dragon_defeated': False,
            'game_started': False,
            'current_combat': None,
            'message': None,
            'message_type': None
        }
    return session['player']


def save_player(player):
    """Save player data to session."""
    session['player'] = player
    session.modified = True


def render_stats_bar(player):
    """Render the player stats bar HTML."""
    health_percent = (player['health'] / player['max_health']) * 100
    return f"""
    <div class="stats-bar">
        <div class="stat">
            <div class="stat-label">Adventurer</div>
            <div class="stat-value">{player['name']}</div>
        </div>
        <div class="stat">
            <div class="stat-label">Health</div>
            <div class="health-bar"><div class="health-fill" style="width: {health_percent}%"></div></div>
            <div class="stat-value">{player['health']}/{player['max_health']}</div>
        </div>
        <div class="stat">
            <div class="stat-label">Attack</div>
            <div class="stat-value">⚔️ {player['attack']}</div>
        </div>
        <div class="stat">
            <div class="stat-label">Defense</div>
            <div class="stat-value">🛡️ {player['defense']}</div>
        </div>
        <div class="stat">
            <div class="stat-label">Gold</div>
            <div class="stat-value">💰 {player['gold']}</div>
        </div>
    </div>
    """


def render_message(player):
    """Render any pending message."""
    if player.get('message'):
        msg = player['message']
        msg_type = player.get('message_type', 'info')
        player['message'] = None
        player['message_type'] = None
        save_player(player)
        return f'<div class="message message-{msg_type}">{msg}</div>'
    return ''


def render_inventory(player):
    """Render inventory section."""
    items = ', '.join(player['inventory']) if player['inventory'] else 'Empty'
    return f"""
    <div class="inventory">
        <h3>🎒 Inventory</h3>
        <p>{items}</p>
    </div>
    """


@app.route('/')
def index():
    """Main game entry point."""
    player = get_player()
    
    if not player['game_started']:
        content = """
        <h1>⚔️ REALM OF SHADOWMERE ⚔️</h1>
        <p class="subtitle">A DnD-Style Text Adventure</p>
            <p class="subtitle">A Fantasy-Style Text Adventure</p>
        
        <div class="game-text">
            <p>In the land of Shadowmere, a fearsome dragon threatens the kingdom.</p>
            <p>You are a brave adventurer chosen to defeat this ancient evil.</p>
            <p>Explore the land, gather items, and prepare for the ultimate battle!</p>
        </div>
        
        <form action="/start" method="POST">
            <input type="text" name="player_name" placeholder="Enter your adventurer's name..." required>
            <button type="submit" class="choice-btn">🗡️ Begin Your Quest</button>
        </form>
        """
    else:
        content = render_stats_bar(player)
        content += render_message(player)
        content += """
        <h2>📍 Village of Elderbrook</h2>
        <div class="game-text">
            <p>You stand in the heart of the village. The townsfolk go about their daily business.</p>
            <p>Where would you like to go?</p>
        </div>
        
        <div class="choices">
            <a href="/location/village" class="choice-btn">🏘️ Explore the Village</a>
            <a href="/location/forest" class="choice-btn">🌲 Enter the Whispering Forest</a>
            <a href="/location/cave" class="choice-btn">💎 Venture into Crystal Cave</a>
            <a href="/location/dragon" class="choice-btn">🐉 Challenge the Dragon's Lair</a>
            <a href="/shop" class="choice-btn">🛒 Visit the Shop</a>
            <a href="/status" class="choice-btn">📊 Check Status</a>
            <a href="/reset" class="choice-btn">🔄 Restart Game</a>
        </div>
        """
        content += render_inventory(player)
    
    return render_template_string(HTML_TEMPLATE, content=content)


@app.route('/start', methods=['POST'])
def start_game():
    """Start a new game."""
    player = get_player()
    player['name'] = request.form.get('player_name', 'Hero').strip() or 'Hero'
    player['game_started'] = True
    player['message'] = f"Welcome, {player['name']}! Your quest begins!"
    player['message_type'] = 'success'
    save_player(player)
    return redirect(url_for('index'))


@app.route('/location/<location>')
def explore_location(location):
    """Handle location exploration."""
    player = get_player()
    
    if not player['game_started']:
        return redirect(url_for('index'))
    
    content = render_stats_bar(player)
    content += render_message(player)
    
    if location == 'village':
        content += village_content(player)
    elif location == 'forest':
        content += forest_content(player)
    elif location == 'cave':
        content += cave_content(player)
    elif location == 'dragon':
        content += dragon_content(player)
    
    content += render_inventory(player)
    content += '<div class="choices"><a href="/" class="choice-btn">⬅️ Return to Village</a></div>'
    
    save_player(player)
    return render_template_string(HTML_TEMPLATE, content=content)


def village_content(player):
    """Generate village content."""
    if 'village' not in player['locations_visited']:
        player['locations_visited'].append('village')
        gold_bonus = random.randint(5, 15)
        player['gold'] += gold_bonus
        return f"""
        <h2>🏘️ Village of Elderbrook</h2>
        <div class="game-text">
            <p>The villagers greet you warmly as you walk through the cobblestone streets.</p>
            <p>An old sage approaches you with wisdom in his eyes...</p>
            <p><em>"Brave adventurer," he says, "to defeat the dragon, you must first
            find the Crystal Sword hidden in the Crystal Cave. Without it,
            the dragon's scales cannot be pierced!"</em></p>
            <p>A grateful villager gives you <strong>{gold_bonus} gold</strong> for your bravery!</p>
        </div>
        """
    else:
        return """
        <h2>🏘️ Village of Elderbrook</h2>
        <div class="game-text">
            <p>The peaceful village continues its daily routines.</p>
            <p>The old sage nods at you knowingly. "Remember - the Crystal Sword is your key to victory!"</p>
        </div>
        """


def forest_content(player):
    """Generate forest encounter content."""
    encounter = random.choice(['goblin', 'fairy', 'wolf', 'treasure'])
    
    content = "<h2>🌲 Whispering Forest</h2>"
    content += '<div class="game-text"><p>You venture deep into the mysterious forest. The trees seem to whisper ancient secrets...</p>'
    
    if encounter == 'goblin':
        content += """
            <p>⚔️ <strong>A wild Goblin leaps from the bushes!</strong></p>
        </div>
        <div class="choices">
            <a href="/combat/goblin" class="choice-btn">⚔️ Fight the Goblin</a>
            <a href="/flee" class="choice-btn">🏃 Attempt to Flee</a>
        </div>
        """
    elif encounter == 'fairy':
        heal = min(20, player['max_health'] - player['health'])
        player['health'] += heal
        content += f"""
            <p>✨ <strong>A friendly forest fairy appears!</strong></p>
            <p>She sprinkles healing dust on you, restoring <strong>{heal} health</strong>!</p>
        </div>
        """
    elif encounter == 'wolf':
        content += """
            <p>🐺 <strong>A fierce Wolf blocks your path!</strong></p>
        </div>
        <div class="choices">
            <a href="/combat/wolf" class="choice-btn">⚔️ Fight the Wolf</a>
            <a href="/flee" class="choice-btn">🏃 Attempt to Flee</a>
        </div>
        """
    else:
        gold = random.randint(10, 25)
        player['gold'] += gold
        content += f"""
            <p>💰 <strong>You discovered a hidden treasure chest!</strong></p>
            <p>Inside you find <strong>{gold} gold coins</strong>!</p>
        </div>
        """
    
    return content


def cave_content(player):
    """Generate cave content."""
    content = "<h2>💎 Crystal Cave</h2>"
    content += '<div class="game-text"><p>The crystals illuminate your path as you explore the cave...</p>'
    
    if 'Crystal Sword' in player['inventory']:
        content += """
            <p>The cave feels peaceful now that you've claimed the Crystal Sword.</p>
            <p>The crystals seem to hum with approval as you pass.</p>
        </div>
        """
    else:
        content += """
            <p>🦇 <strong>A Giant Bat swoops down from the darkness!</strong></p>
            <p>You must defeat it to reach the legendary Crystal Sword!</p>
        </div>
        <div class="choices">
            <a href="/combat/bat" class="choice-btn">⚔️ Fight the Giant Bat</a>
            <a href="/flee" class="choice-btn">🏃 Attempt to Flee</a>
        </div>
        """
    
    return content


def dragon_content(player):
    """Generate dragon lair content."""
    content = "<h2>🐉 Dragon's Lair</h2>"
    
    if player['dragon_defeated']:
        content += """
        <div class="game-text">
            <p>The dragon has been defeated. Peace has returned to the lair.</p>
            <p>Your legend will be told for generations to come!</p>
        </div>
        """
    elif 'Crystal Sword' not in player['inventory']:
        damage = 40
        player['health'] = max(10, player['health'] - damage)
        content += f"""
        <div class="game-text">
            <p>🐉 <strong>THE DRAGON OF SHADOWMERE AWAKENS!</strong></p>
            <p>Its massive form fills the cavern, scales glittering like obsidian.</p>
            <p>⚠️ <strong>You don't have the Crystal Sword!</strong></p>
            <p>Your attacks bounce harmlessly off the dragon's scales. You barely escape with your life!</p>
            <p class="message message-danger">You took {damage} damage fleeing!</p>
        </div>
        """
    else:
        content += """
        <div class="game-text">
            <p>🐉 <strong>THE DRAGON OF SHADOWMERE AWAKENS!</strong></p>
            <p>Its massive form fills the cavern, scales glittering like obsidian.</p>
            <p>Your Crystal Sword glows with ancient power! The dragon recognizes the legendary blade!</p>
        </div>
        <div class="choices">
            <a href="/combat/dragon" class="choice-btn">⚔️ FIGHT THE DRAGON!</a>
            <a href="/flee" class="choice-btn">🏃 Flee (Coward!)</a>
        </div>
        """
    
    return content


@app.route('/combat/<enemy>')
def combat(enemy):
    """Handle combat encounters."""
    player = get_player()
    
    enemies = {
        'goblin': {'name': 'Goblin', 'health': 30, 'attack': 8, 'gold': 10},
        'wolf': {'name': 'Wolf', 'health': 25, 'attack': 10, 'gold': 8},
        'bat': {'name': 'Giant Bat', 'health': 35, 'attack': 12, 'gold': 15},
        'dragon': {'name': 'Dragon of Shadowmere', 'health': 100, 'attack': 20, 'gold': 100}
    }
    
    if enemy not in enemies:
        return redirect(url_for('index'))
    
    enemy_data = enemies[enemy]
    
    # Initialize or get combat state
    if player.get('current_combat') is None or player['current_combat'].get('type') != enemy:
        player['current_combat'] = {
            'type': enemy,
            'enemy_health': enemy_data['health'],
            'enemy_name': enemy_data['name']
        }
    
    combat_state = player['current_combat']
    
    content = render_stats_bar(player)
    content += f"""
    <h2>⚔️ Battle: {combat_state['enemy_name']}</h2>
    <div class="game-text">
        <p><strong>{combat_state['enemy_name']} Health:</strong> {combat_state['enemy_health']}</p>
    </div>
    <div class="choices">
        <a href="/attack/{enemy}" class="choice-btn">⚔️ Attack!</a>
    """
    
    if 'Health Potion' in player['inventory']:
        content += '<a href="/use_potion_combat" class="choice-btn">🧪 Use Health Potion</a>'
    
    content += """
        <a href="/flee" class="choice-btn">🏃 Attempt to Flee</a>
    </div>
    """
    
    save_player(player)
    return render_template_string(HTML_TEMPLATE, content=content)


@app.route('/attack/<enemy>')
def attack(enemy):
    """Process an attack."""
    player = get_player()
    
    enemies = {
        'goblin': {'attack': 8, 'gold': 10},
        'wolf': {'attack': 10, 'gold': 8},
        'bat': {'attack': 12, 'gold': 15},
        'dragon': {'attack': 20, 'gold': 100}
    }
    
    if enemy not in enemies or player.get('current_combat') is None:
        return redirect(url_for('index'))
    
    combat_state = player['current_combat']
    enemy_data = enemies[enemy]
    
    # Player attacks
    damage = random.randint(player['attack'] - 3, player['attack'] + 5)
    combat_state['enemy_health'] -= damage
    
    message = f"You strike for {damage} damage! "
    
    # Check if enemy defeated
    if combat_state['enemy_health'] <= 0:
        player['gold'] += enemy_data['gold']
        player['current_combat'] = None
        
        # Special rewards
        if enemy == 'bat' and 'Crystal Sword' not in player['inventory']:
            player['inventory'].append('Crystal Sword')
            player['attack'] += 15
            player['message'] = f"Victory! You earned {enemy_data['gold']} gold and found the CRYSTAL SWORD! (+15 Attack)"
        elif enemy == 'dragon':
            player['dragon_defeated'] = True
            player['message'] = "🎉 VICTORY! You have defeated the Dragon of Shadowmere! You are the hero of the realm!"
        else:
            player['message'] = f"Victory! You earned {enemy_data['gold']} gold!"
        
        player['message_type'] = 'success'
        save_player(player)
        return redirect(url_for('index'))
    
    # Enemy attacks back
    enemy_damage = random.randint(enemy_data['attack'] - 2, enemy_data['attack'] + 3)
    actual_damage = max(1, enemy_damage - player['defense'])
    player['health'] -= actual_damage
    
    message += f"The {combat_state['enemy_name']} hits you for {actual_damage} damage!"
    
    # Check if player defeated
    if player['health'] <= 0:
        player['message'] = "💀 You have been defeated! Game Over!"
        player['message_type'] = 'danger'
        player['game_started'] = False
        player['current_combat'] = None
        save_player(player)
        return redirect(url_for('reset'))
    
    player['message'] = message
    player['message_type'] = 'info'
    save_player(player)
    return redirect(url_for('combat', enemy=enemy))


@app.route('/flee')
def flee():
    """Attempt to flee from combat."""
    player = get_player()
    
    if random.random() > 0.3:
        player['current_combat'] = None
        player['message'] = "You successfully fled from battle!"
        player['message_type'] = 'info'
    else:
        player['message'] = "You failed to escape!"
        player['message_type'] = 'danger'
    
    save_player(player)
    return redirect(url_for('index'))


@app.route('/use_potion_combat')
def use_potion_combat():
    """Use health potion during combat."""
    player = get_player()
    
    if 'Health Potion' in player['inventory']:
        player['inventory'].remove('Health Potion')
        heal = 30
        player['health'] = min(player['health'] + heal, player['max_health'])
        player['message'] = f"You drink a Health Potion and recover {heal} health!"
        player['message_type'] = 'success'
    
    save_player(player)
    
    if player.get('current_combat'):
        return redirect(url_for('combat', enemy=player['current_combat']['type']))
    return redirect(url_for('index'))


@app.route('/shop')
def shop():
    """Display shop interface."""
    player = get_player()
    
    if not player['game_started']:
        return redirect(url_for('index'))
    
    content = render_stats_bar(player)
    content += render_message(player)
    content += """
    <h2>🛒 Village Shop</h2>
    <div class="game-text">
        <p>"Welcome, adventurer! What would you like to purchase?"</p>
    </div>
    <div class="choices">
        <a href="/buy/potion" class="choice-btn">🧪 Health Potion - 15 gold (Restores 30 health)</a>
        <a href="/buy/sword" class="choice-btn">⚔️ Iron Sword - 25 gold (+5 Attack)</a>
        <a href="/buy/shield" class="choice-btn">🛡️ Leather Shield - 20 gold (+3 Defense)</a>
        <a href="/buy/amulet" class="choice-btn">📿 Magic Amulet - 40 gold (+20 Max Health)</a>
        <a href="/" class="choice-btn">⬅️ Leave Shop</a>
    </div>
    """
    content += render_inventory(player)
    
    return render_template_string(HTML_TEMPLATE, content=content)


@app.route('/buy/<item>')
def buy_item(item):
    """Process item purchase."""
    player = get_player()
    
    items = {
        'potion': {'name': 'Health Potion', 'price': 15},
        'sword': {'name': 'Iron Sword', 'price': 25, 'attack': 5},
        'shield': {'name': 'Leather Shield', 'price': 20, 'defense': 3},
        'amulet': {'name': 'Magic Amulet', 'price': 40, 'max_health': 20}
    }
    
    if item not in items:
        return redirect(url_for('shop'))
    
    item_data = items[item]
    
    if player['gold'] >= item_data['price']:
        player['gold'] -= item_data['price']
        player['inventory'].append(item_data['name'])
        
        if 'attack' in item_data:
            player['attack'] += item_data['attack']
        if 'defense' in item_data:
            player['defense'] += item_data['defense']
        if 'max_health' in item_data:
            player['max_health'] += item_data['max_health']
            player['health'] += item_data['max_health']
        
        player['message'] = f"Purchased {item_data['name']}!"
        player['message_type'] = 'success'
    else:
        player['message'] = "Not enough gold!"
        player['message_type'] = 'danger'
    
    save_player(player)
    return redirect(url_for('shop'))


@app.route('/status')
def status():
    """Display detailed player status."""
    player = get_player()
    
    if not player['game_started']:
        return redirect(url_for('index'))
    
    quest_status = "🏆 COMPLETED - Dragon Defeated!" if player['dragon_defeated'] else "📜 Incomplete - Defeat the Dragon"
    
    content = render_stats_bar(player)
    content += f"""
    <h2>📊 Adventurer Status</h2>
    <div class="game-text">
        <p><strong>Name:</strong> {player['name']}</p>
        <p><strong>Health:</strong> {player['health']}/{player['max_health']}</p>
        <p><strong>Attack Power:</strong> {player['attack']}</p>
        <p><strong>Defense:</strong> {player['defense']}</p>
        <p><strong>Gold:</strong> {player['gold']}</p>
        <p><strong>Quest Status:</strong> {quest_status}</p>
        <p><strong>Locations Visited:</strong> {', '.join(player['locations_visited']) if player['locations_visited'] else 'None yet'}</p>
    </div>
    """
    content += render_inventory(player)
    content += '<div class="choices"><a href="/" class="choice-btn">⬅️ Return to Village</a></div>'
    
    return render_template_string(HTML_TEMPLATE, content=content)


@app.route('/reset')
def reset():
    """Reset the game."""
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🐉 DnD Adventure Game - Web Server")
        print("🐉 Fantasy Adventure Game - Web Server")
    print("="*60)
    print("\nStarting server...")
    print("\n📍 Local access: http://localhost:5000")
    print("📍 Network access: http://YOUR_IP:5000")
    print("\nPress Ctrl+C to stop the server\n")
    
    # host='0.0.0.0' allows access from other devices on the network
    app.run(host='0.0.0.0', port=5000, debug=True)

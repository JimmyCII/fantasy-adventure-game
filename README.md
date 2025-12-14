# 🐉 Fantasy Adventure Game

A text-based adventure game built with Python and Flask for the Microsoft AI Engineer Program.

## 🎮 Play the Game

### Web Version (Browser)
```bash
pip install -r requirements.txt
python fantasy_adventure_web.py
```
Then open http://localhost:5000

### CLI Version (Terminal)
```bash
python dnd_adventure_game.py
```

## 🗡️ Game Features

- **4 Explorable Locations**: Village, Forest, Cave, Dragon's Lair
- **Combat System**: Turn-based battles with attack, flee, and potion options
- **Shop System**: Buy weapons, armor, and potions
- **Inventory Management**: Collect and use items
- **Quest Objective**: Find the Crystal Sword and defeat the Dragon of Shadowmere

## 💻 Tech Stack

- Python 3.11
- Flask (web framework)
- HTML/CSS (fantasy-themed UI)
- Session management for multiplayer support

## 📚 Python Concepts Demonstrated

| Concept | Implementation |
|---------|----------------|
| Variables | Player stats, game state flags |
| Lists | Inventory, locations, shop items |
| Loops | Game loop, combat loop, menus |
| Conditionals | Player choices, combat outcomes |
| Functions | 15+ modular functions |

## 🤖 Built with GitHub Copilot

This project was developed using GitHub Copilot for AI-assisted coding, demonstrating how AI tools can accelerate development while learning fundamental programming concepts.

## 📁 Project Structure

```
├── fantasy_adventure_game.py     # CLI version
├── fantasy_adventure_web.py      # Web version (Flask)
├── requirements.txt          # Python dependencies
├── Procfile                  # Deployment config
├── README.md                 # This file
└── Fantasy_Adventure_Game_Documentation.md  # Full documentation
```

## 🚀 Deploy Your Own

### PythonAnywhere (Free)
1. Create account at pythonanywhere.com
2. Upload files
3. Create Flask web app
4. Done!

### Render.com
1. Connect GitHub repo
2. Auto-deploys from Procfile

---

*Created for Microsoft AI Engineer Program - December 2025*

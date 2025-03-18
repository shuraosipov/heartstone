# 🃏 Hearthstone AI Assistant 🧙‍♂️

![Hearthstone](https://img.shields.io/badge/Hearthstone-AI%20Assistant-orange?style=for-the-badge&logo=battle.net)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge&logo=streamlit)

<p align="center">
  <img src="https://www.pngall.com/wp-content/uploads/13/Hearthstone-Logo-PNG-Image.png" alt="Hearthstone Logo" width="400"/>
</p>

## ✨ Overview

Hearthstone AI Assistant is your personal companion for dominating the Hearthstone ladder! This interactive Streamlit application uses AI-powered analytics to provide real-time game advice, deck analysis, meta insights, and personalized coaching - all wrapped in an authentic Hearthstone visual experience.

Whether you're a Rank 50 newcomer or a Legend player looking to optimize your gameplay, this assistant helps you make better decisions and climb the ranks faster.

## 🌟 Features

### 🛡️ Game Advisor
- Real-time gameplay analysis and recommendations
- Intelligent board state evaluation
- Lethal detection and optimal play suggestions
- Priority-based advice with color-coded indicators
- Visual battlefield representation
- Support for all hero classes and card types

### 📊 Deck Analysis
- Mana curve visualization and optimization
- Card type distribution analysis
- Matchup evaluation against popular decks
- Personalized mulligan advice
- Support for custom deck codes or preset decks

### 📈 Meta Report
- Current tier list of top performing decks
- Detailed breakdown of meta decks and counter strategies
- Meta trend forecasting and analysis
- Key card highlights for each archetype

### 💬 Chat Assistant
- Natural language interaction with Hearthstone AI
- Get answers to strategy questions, card interactions, and gameplay mechanics
- Context-aware responses based on your current game state
- Beginner-friendly explanations and expert tips

## 🎮 Screenshots

<p align="center">
  <img src="https://i.imgur.com/example1.png" alt="Game Advisor" width="400"/>
  <img src="https://i.imgur.com/example2.png" alt="Deck Analysis" width="400"/>
</p>

## 🔧 Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/hearthstone-ai-assistant.git
cd hearthstone-ai-assistant
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

1. Run the Streamlit app:
```bash
streamlit run hearthstone_app.py
```

2. Open your browser and navigate to the provided URL (typically http://localhost:8501)

3. Select your preferred mode from the sidebar:
   - Game Advisor: Input your current game state for personalized advice
   - Deck Analysis: Analyze deck composition and get optimization tips
   - Meta Report: Stay updated on the current Hearthstone meta
   - Chat Assistant: Ask questions and get Hearthstone wisdom

## 🧩 How It Works

The Hearthstone AI Assistant combines several advanced techniques:

1. **Game State Analysis**: Evaluates board states, hand resources, and possible plays
2. **Heuristic Engine**: Uses game-specific heuristics to determine optimal plays
3. **Visualization**: Generates Hearthstone-style card artwork and interfaces
4. **Natural Language Processing**: Powers the conversational AI assistant
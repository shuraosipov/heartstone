import streamlit as st
import random
from PIL import Image
import io
import base64
import requests
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import json
import pandas as pd
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from io import BytesIO
import re

# Set page config
st.set_page_config(
    page_title="Hearthstone AI Assistant",
    page_icon="🃏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
/* Global styling with Hearthstone background */
.main {
    background-image: url('https://wallpaperaccess.com/full/832451.jpg');
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
    background-repeat: no-repeat;
    padding: 20px;
    color: #FFD100;
    font-family: 'Belwe Bold', 'Times New Roman', serif;
}

.block-container {
    backdrop-filter: blur(5px);
    background-color: rgba(0, 0, 0, 0.75);
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
    border: 2px solid #C09A5E;
}

/* Custom font styling for Hearthstone feel */
h1, h2, h3, h4, h5, h6 {
    color: #FFD100 !important;
    font-family: 'Belwe Bold', 'Times New Roman', serif !important;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8) !important;
}

h1 {
    background: linear-gradient(to bottom, #FFD100, #FFA500);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 3em !important;
    text-align: center;
    margin-bottom: 30px !important;
}

.stButton > button {
    background-color: #C67435 !important;
    color: white !important;
    border: 3px solid #8B4513 !important;
    border-radius: 10px !important;
    font-family: 'Belwe Bold', 'Times New Roman', serif !important;
    font-weight: bold !important;
    font-size: 1.1em !important;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4) !important;
    transition: all 0.2s ease-in-out !important;
}

.stButton > button:hover {
    background-color: #8B4513 !important;
    transform: scale(1.05) !important;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.6) !important;
}

p, span, div, label {
    color: #F8E9B7 !important;
    font-family: 'Belwe Bold', 'Times New Roman', serif;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background-image: url('https://wallpaperaccess.com/full/1551162.jpg') !important;
    background-size: cover !important;
    background-position: center !important;
    color: #F8E9B7 !important;
    border-right: 2px solid #C09A5E;
}

section[data-testid="stSidebar"] .block-container {
    backdrop-filter: blur(10px) !important;
    background-color: rgba(0, 0, 0, 0.75) !important;
}

/* Card styling to match real Hearthstone cards */
.card {
    background-color: #1A0F00;
    background-image: url('https://hearthstone.judgehype.com/screenshots/deck/2019/back.jpg');
    background-size: cover;
    border-radius: 15px;
    padding: 10px;
    margin: 8px;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.7);
    position: relative;
    color: white;
    min-height: 250px;
    width: 180px;
    transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
    border: 2px solid #C09A5E;
    overflow: hidden;
}

.card:hover {
    transform: scale(1.05) translateY(-10px) rotate(2deg);
    z-index: 100;
    box-shadow: 0 16px 32px rgba(0, 0, 0, 0.8), 0 0 20px rgba(255, 215, 0, 0.4);
}

.card-minion {
    background-color: #4A2E1D;
}

.card-spell {
    background-color: #284A7E;
}

.card-weapon {
    background-color: #7E2828;
}

.mana {
    background-image: linear-gradient(135deg, #0053A6, #007BFF);
    background-size: 100% 100%;
    width: 40px;
    height: 40px;
    position: absolute;
    top: 5px;
    left: 5px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 24px;
    color: white;
    text-shadow: 2px 2px 0px #0053A6;
    border-radius: 50%;
    border: 2px solid #00B4FF;
    box-shadow: 0 0 10px #00B4FF;
    z-index: 5;
}

.attack {
    background-image: linear-gradient(135deg, #A13012, #FF5722);
    background-size: 100% 100%;
    width: 40px;
    height: 40px;
    position: absolute;
    bottom: 5px;
    left: 5px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 24px;
    color: white;
    text-shadow: 2px 2px 0px #A13012;
    border-radius: 50%;
    border: 2px solid #FF9800;
    box-shadow: 0 0 10px #FF9800;
    z-index: 5;
}

.health {
    background-image: linear-gradient(135deg, #9B0E0E, #E91E63);
    background-size: 100% 100%;
    width: 40px;
    height: 40px;
    position: absolute;
    bottom: 5px;
    right: 5px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 24px;
    color: white;
    text-shadow: 2px 2px 0px #9B0E0E;
    border-radius: 50%;
    border: 2px solid #FF4081;
    box-shadow: 0 0 10px #FF4081;
    z-index: 5;
}

.card-name {
    text-align: center;
    font-weight: bold;
    font-size: 16px;
    margin-top: 40px;
    margin-bottom: 5px;
    color: white;
    text-shadow: 2px 2px 2px black;
}

.card-text {
    text-align: center;
    font-size: 12px;
    margin: 5px 5px 50px 5px;
    color: white;
    text-shadow: 1px 1px 1px black;
}

/* Player stats styling */
.player-stats {
    background-image: linear-gradient(45deg, #4A2E1D, #2E1D0F);
    background-size: cover;
    color: white;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 15px;
    display: flex;
    justify-content: space-between;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
    border: 2px solid #C09A5E;
}

/* Recommendation styling */
.recommendation {
    background-image: linear-gradient(45deg, #4A2E1D, #2E1D0F);
    background-size: cover;
    color: white;
    padding: 15px;
    border-radius: 10px;
    margin: 15px 0;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
    border: 2px solid #C09A5E;
    position: relative;
    overflow: hidden;
}

.recommendation::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(to right, transparent, #C09A5E, transparent);
}

.high-priority {
    border-left: 8px solid #FF4500;
    animation: pulsate-high 2s infinite alternate;
}

.medium-priority {
    border-left: 8px solid #FFA500;
    animation: pulsate-medium 3s infinite alternate;
}

.low-priority {
    border-left: 8px solid #4CAF50;
}

@keyframes pulsate-high {
    0% { box-shadow: 0 0 5px rgba(255, 69, 0, 0.5); }
    100% { box-shadow: 0 0 20px rgba(255, 69, 0, 0.8); }
}

@keyframes pulsate-medium {
    0% { box-shadow: 0 0 5px rgba(255, 165, 0, 0.5); }
    100% { box-shadow: 0 0 15px rgba(255, 165, 0, 0.7); }
}

.battlefield {
    min-height: 150px;
    background-image: url('https://cdn.hearthstonetopdecks.com/wp-content/uploads/2014/06/board-stormwind.jpg');
    background-size: cover;
    border-radius: 15px;
    padding: 20px 10px;
    margin: 15px 0;
    box-shadow: inset 0 0 15px 5px rgba(0, 0, 0, 0.7);
    border: 3px solid #C09A5E;
}

/* Tab styling */
[data-testid="stHorizontalBlock"] > div[data-testid="stVerticalBlock"] > div[data-baseweb="tab-list"] {
    background-color: rgba(81, 45, 29, 0.8) !important;
    border-radius: 10px !important;
    padding: 5px !important;
    border: 2px solid #C09A5E !important;
}

[data-testid="stHorizontalBlock"] > div[data-testid="stVerticalBlock"] > div[data-baseweb="tab-list"] button[data-baseweb="tab"] {
    color: #FFD100 !important;
    font-family: 'Belwe Bold', 'Times New Roman', serif !important;
    border-radius: 5px !important;
}

[data-testid="stHorizontalBlock"] > div[data-testid="stVerticalBlock"] > div[data-baseweb="tab-list"] button[aria-selected="true"] {
    background-color: #8B4513 !important;
    color: white !important;
    font-weight: bold !important;
}

/* Multiselect, selectbox styling */
div[data-baseweb="select"] {
    background-color: rgba(50, 30, 14, 0.8) !important;
    border-radius: 5px !important;
    border: 2px solid #C09A5E !important;
}

/* Number input, slider styling */
div[data-testid="stSlider"], 
div[data-baseweb="input"] {
    background-color: rgba(50, 30, 14, 0.5) !important;
    border-radius: 10px !important;
    padding: 10px !important;
    border: 2px solid #C09A5E !important;
}

/* Radio button styling */
[data-testid="stRadio"] {
    background-color: rgba(50, 30, 14, 0.7) !important;
    border-radius: 10px !important;
    padding: 10px !important;
    border: 2px solid #C09A5E !important;
}

/* Tables styling */
div[data-testid="stTable"] {
    border: 3px solid #C09A5E !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

div[data-testid="stTable"] thead {
    background-color: #8B4513 !important;
    color: #FFD100 !important;
}

div[data-testid="stTable"] tbody tr:nth-child(odd) {
    background-color: rgba(50, 30, 14, 0.7) !important;
}

div[data-testid="stTable"] tbody tr:nth-child(even) {
    background-color: rgba(81, 45, 29, 0.7) !important;
}

/* Charts styling */
div[data-testid="stChart"] {
    background-color: rgba(50, 30, 14, 0.7) !important;
    border-radius: 10px !important;
    padding: 10px !important;
    border: 2px solid #C09A5E !important;
}

/* Expander styling */
div[data-testid="stExpander"] {
    border-radius: 10px !important;
    overflow: hidden !important;
}

div[data-testid="stExpander"] > div:first-child {
    background-color: rgba(81, 45, 29, 0.8) !important;
    border-radius: 10px 10px 0 0 !important;
    border: 2px solid #C09A5E !important;
    color: #FFD100 !important;
    font-family: 'Belwe Bold', 'Times New Roman', serif !important;
}

div[data-testid="stExpander"] > div:last-child {
    background-color: rgba(50, 30, 14, 0.7) !important;
    border-radius: 0 0 10px 10px !important;
    border: 2px solid #C09A5E !important;
    border-top: none !important;
}

/* Alert/Info message styling */
div[data-testid="stAlert"] {
    background-color: rgba(81, 45, 29, 0.8) !important;
    border-radius: 10px !important;
    border: 2px solid #C09A5E !important;
}

/* Chat container styling */
.chat-container {
    background-image: linear-gradient(45deg, #4A2E1D, #2E1D0F);
    background-size: cover;
    border-radius: 15px;
    padding: 20px;
    margin: 20px 0;
    max-height: 600px;
    overflow-y: auto;
    border: 3px solid #C09A5E;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
    position: relative;
}

.chat-container::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: url('https://wallpaperaccess.com/full/832451.jpg');
    background-size: cover;
    opacity: 0.2;
    z-index: -1;
    border-radius: 15px;
}

.chat-message {
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 15px;
    font-size: 16px;
    max-width: 80%;
    animation: fade-in 0.3s ease-in-out;
    position: relative;
}

@keyframes fade-in {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.user-message {
    background: linear-gradient(135deg, rgba(194, 149, 94, 0.8), rgba(153, 103, 53, 0.8));
    color: white;
    margin-left: auto;
    margin-right: 10px;
    text-align: right;
    border-bottom-right-radius: 0;
    border: 1px solid #8B4513;
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.2);
}

.user-message::after {
    content: "";
    position: absolute;
    right: -10px;
    bottom: 0;
    width: 0;
    height: 0;
    border: 10px solid transparent;
    border-top-color: rgba(153, 103, 53, 0.8);
    border-bottom: 0;
    border-right: 0;
}

.assistant-message {
    background: linear-gradient(135deg, rgba(73, 53, 29, 0.8), rgba(50, 36, 22, 0.8));
    color: #FFD100;
    margin-right: auto;
    margin-left: 10px;
    text-align: left;
    border-bottom-left-radius: 0;
    border: 1px solid #C09A5E;
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.2);
}

.assistant-message::after {
    content: "";
    position: absolute;
    left: -10px;
    bottom: 0;
    width: 0;
    height: 0;
    border: 10px solid transparent;
    border-top-color: rgba(50, 36, 22, 0.8);
    border-bottom: 0;
    border-left: 0;
}

input[type="text"] {
    background-color: rgba(50, 30, 14, 0.7) !important;
    border-radius: 10px !important;
    padding: 10px !important;
    border: 2px solid #C09A5E !important;
    color: white !important;
    box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.3);
}

.chat-header {
    text-align: center;
    background: linear-gradient(45deg, #4A2E1D, #2E1D0F);
    border-radius: 10px 10px 0 0;
    padding: 15px;
    margin-bottom: 0;
    border: 2px solid #C09A5E;
    border-bottom: none;
    position: relative;
    overflow: hidden;
}

.chat-header::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: url('https://wallpaperaccess.com/full/1551162.jpg');
    background-size: cover;
    background-position: center;
    opacity: 0.2;
    z-index: -1;
}

.chat-header h3 {
    margin: 0;
    color: #FFD100 !important;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5) !important;
    font-size: 1.5em !important;
}

.chat-footer {
    background: linear-gradient(45deg, #4A2E1D, #2E1D0F);
    border-radius: 0 0 10px 10px;
    padding: 10px;
    margin-top: 0;
    border: 2px solid #C09A5E;
    border-top: none;
    position: relative;
    overflow: hidden;
}

.chat-footer::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: url('https://wallpaperaccess.com/full/1551162.jpg');
    background-size: cover;
    background-position: center;
    opacity: 0.2;
    z-index: -1;
}

/* Animations */
@keyframes glow {
    0% { box-shadow: 0 0 5px rgba(192, 154, 94, 0.5); }
    100% { box-shadow: 0 0 20px rgba(192, 154, 94, 0.8); }
}

/* Apply animations to various elements */
.stButton > button:hover,
.card:hover {
    animation: glow 1.5s infinite alternate;
}

.gold-text {
    color: #FFD100 !important;
    text-shadow: 0 0 5px rgba(255, 209, 0, 0.5);
}

.parchment {
    background-color: rgba(233, 214, 178, 0.1);
    background-image: url('https://cdn.pixabay.com/photo/2015/12/03/08/50/paper-1074131_640.jpg');
    background-blend-mode: overlay;
    background-size: cover;
    border-radius: 10px;
    padding: 20px;
    color: #4A2E1D;
    border: 1px solid #C09A5E;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
}

/* Logo styling */
.logo-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-bottom: 30px;
    position: relative;
}

.logo-container::after {
    content: "";
    position: absolute;
    bottom: -15px;
    left: 25%;
    right: 25%;
    height: 2px;
    background: linear-gradient(to right, transparent, #C09A5E, transparent);
}

.logo-img {
    width: 400px;
    height: auto;
    filter: drop-shadow(0 8px 12px rgba(0, 0, 0, 0.6));
    margin-bottom: 10px;
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
}

.stTabs [role="tablist"] {
    gap: 5px;
}

</style>
""", unsafe_allow_html=True)

# Card types
@dataclass
class Card:
    id: int
    name: str
    mana_cost: int
    card_type: str
    card_class: str
    rarity: str
    text: str

@dataclass
class MinionCard(Card):
    attack: int
    health: int
    keywords: List[str] = None

@dataclass
class SpellCard(Card):
    effect: str = None

@dataclass
class WeaponCard(Card):
    attack: int
    durability: int

@dataclass
class Player:
    name: str
    hero_class: str
    health: int = 30
    armor: int = 0
    mana: int = 0
    max_mana: int = 0
    hand: List[Card] = None
    battlefield: List[MinionCard] = None
    weapon: Optional[WeaponCard] = None
    
    def __post_init__(self):
        if self.hand is None:
            self.hand = []
        if self.battlefield is None:
            self.battlefield = []

@dataclass
class GameState:
    player: Player
    opponent: Player
    turn_number: int
    current_player: str  # "player" or "opponent"
    player_deck_remaining: int
    opponent_deck_remaining: int
    player_fatigue: int = 0
    opponent_fatigue: int = 0

# Initialize session state
if 'current_deck' not in st.session_state:
    st.session_state.current_deck = None

if 'game_state' not in st.session_state:
    st.session_state.game_state = None

if 'card_database' not in st.session_state:
    st.session_state.card_database = None

if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "I'm your Hearthstone AI Assistant! Ask me anything about cards, strategies, or game mechanics."}
    ]

# Helper functions
def load_hearthstone_card_data():
    """Load a comprehensive database of real Hearthstone cards"""
    # In a real application, this would load from a real API or database
    # For this demo, we'll create a limited set of cards
    
    cards = []
    
    # Load some popular cards from various classes
    
    # Neutral minions
    cards.append(MinionCard(id=1, name="Zilliax", mana_cost=5, card_type="Minion", card_class="Neutral", 
                           rarity="Legendary", text="Magnetic, Divine Shield, Taunt, Lifesteal, Rush", 
                           attack=3, health=2, keywords=["Magnetic", "Divine Shield", "Taunt", "Lifesteal", "Rush"]))
    
    cards.append(MinionCard(id=2, name="Zephrys the Great", mana_cost=2, card_type="Minion", card_class="Neutral", 
                           rarity="Legendary", text="If your deck has no duplicates, wish for the perfect card.", 
                           attack=3, health=2))
    
    # Mage cards
    cards.append(SpellCard(id=3, name="Fireball", mana_cost=4, card_type="Spell", card_class="Mage", 
                          rarity="Free", text="Deal 6 damage.", effect="Deal 6 damage"))
    
    cards.append(SpellCard(id=4, name="Frost Nova", mana_cost=3, card_type="Spell", card_class="Mage", 
                          rarity="Free", text="Freeze all enemy minions.", effect="Freeze all enemy minions"))
    
    # Warrior cards
    cards.append(WeaponCard(id=5, name="Fiery War Axe", mana_cost=3, card_type="Weapon", card_class="Warrior", 
                           rarity="Free", text="", attack=3, durability=2))
    
    cards.append(SpellCard(id=6, name="Shield Slam", mana_cost=1, card_type="Spell", card_class="Warrior", 
                          rarity="Epic", text="Deal 1 damage to a minion for each Armor you have.", 
                          effect="Deal 1 damage to a minion for each Armor you have"))
    
    # Priest cards
    cards.append(SpellCard(id=7, name="Shadow Word: Death", mana_cost=3, card_type="Spell", card_class="Priest", 
                          rarity="Basic", text="Destroy a minion with 5 or more Attack.", 
                          effect="Destroy a minion with 5 or more Attack"))
    
    # And more cards would be added for a complete database
    return cards

def load_meta_decks():
    """Load current meta decks information"""
    # In a real app, this would be regularly updated from a meta database/API
    meta_decks = [
        {
            "name": "Tempo Demon Hunter",
            "tier": "1",
            "description": "Fast-paced aggro deck that aims to control the board early and finish with direct damage.",
            "key_cards": ["Twin Slice", "Battlefiend", "Spectral Sight", "Skull of Gul'dan"],
            "counters": ["Control Warrior", "Libram Paladin"]
        },
        {
            "name": "Control Warrior",
            "tier": "2",
            "description": "Defensive deck that gains a lot of armor and removes threats until playing late-game win conditions.",
            "key_cards": ["Shield Slam", "Brawl", "Risky Skipper", "Armorsmith"],
            "counters": ["Quest Mage", "Galakrond Rogue"]
        },
        {
            "name": "Spell Mage",
            "tier": "2",
            "description": "Spell focused deck that uses no minions to enable powerful spell synergies.",
            "key_cards": ["Font of Power", "Apexis Blast", "Deep Freeze", "Evocation"],
            "counters": ["Demon Hunter", "Face Hunter"]
        }
    ]
    return meta_decks

def analyze_game_state(game_state: GameState) -> List[dict]:
    """
    Analyze the current game state and provide recommendations
    Returns a list of recommendation objects with priority levels
    """
    recommendations = []
    
    # Get player and opponent information for easier access
    player = game_state.player
    opponent = game_state.opponent
    is_player_turn = game_state.current_player == "player"
    
    # Only provide recommendations on player's turn
    if not is_player_turn:
        recommendations.append({
            "title": "Waiting for opponent",
            "description": "It's your opponent's turn. Use this time to plan your next move.",
            "priority": "low"
        })
        return recommendations
    
    # Analyze hand for efficient plays
    if player.hand:
        playable_cards = [card for card in player.hand if card.mana_cost <= player.mana]
        if playable_cards:
            # Sort by mana efficiency (using all available mana is generally good)
            best_mana_play = max(playable_cards, key=lambda card: card.mana_cost)
            recommendations.append({
                "title": f"Consider playing {best_mana_play.name}",
                "description": f"This uses {best_mana_play.mana_cost}/{player.mana} mana efficiently.",
                "priority": "medium"
            })
    
    # Analyze board state for favorable trades
    if player.battlefield and opponent.battlefield:
        for i, minion in enumerate(player.battlefield):
            # Look for favorable trades (where our minion can kill an enemy but survive)
            favorable_trades = []
            for j, enemy in enumerate(opponent.battlefield):
                if minion.attack >= enemy.health and minion.health > enemy.attack:
                    favorable_trades.append((j, enemy))
            
            if favorable_trades:
                best_trade = max(favorable_trades, key=lambda x: x[1].attack)
                recommendations.append({
                    "title": f"Favorable trade with {minion.name}",
                    "description": f"Trade your {minion.name} into opponent's {best_trade[1].name} for a favorable exchange.",
                    "priority": "high"
                })
    
    # Check for lethal (if we can deal enough damage to kill the opponent)
    total_damage_potential = sum(minion.attack for minion in player.battlefield)
    if player.weapon:
        total_damage_potential += player.weapon.attack
    
    # Add damage from direct damage spells in hand
    damage_spells = [card for card in player.hand if card.card_type == "Spell" and "damage" in card.text.lower()]
    for spell in damage_spells:
        # This is a simplified calculation - in a real app, you'd need to parse the card text
        # to extract the actual damage value
        if "fireball" in spell.name.lower():
            total_damage_potential += 6
    
    if total_damage_potential >= opponent.health + opponent.armor:
        recommendations.append({
            "title": "Potential lethal detected!",
            "description": f"You have {total_damage_potential} potential damage, and opponent has {opponent.health} health and {opponent.armor} armor.",
            "priority": "high"
        })
    
    # Provide resource management advice
    if game_state.turn_number >= 7 and len(player.hand) <= 2:
        recommendations.append({
            "title": "Low on cards",
            "description": "You're running low on cards. Consider playing for value rather than tempo.",
            "priority": "medium"
        })
    
    # Add general advice based on match-up
    recommendations.append({
        "title": f"{player.hero_class} vs {opponent.hero_class} match-up advice",
        "description": f"In this match-up, focus on controlling the board early and saving removal for key threats.",
        "priority": "low"
    })
    
    return recommendations

class ImageGenerator:
    """Class to generate Hearthstone-style images on the fly"""
    
    @staticmethod
    def generate_card_art(card_name, card_type, card_class):
        """Generate card art based on card properties"""
        # In a real implementation, this would call an image generation model
        # Here we'll create a procedural image based on the inputs
        
        # Create a base image with a size typical for Hearthstone card art
        width, height = 300, 300
        
        # Seed the random generator with the card name for consistency
        seed = sum(ord(c) for c in card_name)
        np.random.seed(seed)
        
        # Generate a base color based on card class
        class_colors = {
            "Neutral": (200, 200, 200),
            "Mage": (64, 81, 211),
            "Warrior": (198, 45, 45),
            "Hunter": (0, 150, 0),
            "Priest": (255, 255, 255),
            "Paladin": (255, 215, 0),
            "Shaman": (0, 112, 222),
            "Druid": (102, 51, 0),
            "Warlock": (138, 43, 226),
            "Rogue": (105, 105, 105),
            "Demon Hunter": (46, 139, 87)
        }
        
        base_color = class_colors.get(card_class, (200, 200, 200))
        
        # Create the image with gradient background
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
        # Draw a gradient background
        for y in range(height):
            r = int(base_color[0] * (1 - y/height*0.5))
            g = int(base_color[1] * (1 - y/height*0.5))
            b = int(base_color[2] * (1 - y/height*0.5))
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Add some random elements based on card type
        if card_type == "Minion":
            # Add some shapes that suggest a creature
            for _ in range(5):
                x = np.random.randint(50, width-50)
                y = np.random.randint(50, height-50)
                size = np.random.randint(20, 80)
                color = tuple(np.random.randint(0, 255, 3))
                draw.ellipse((x-size/2, y-size/2, x+size/2, y+size/2), outline=color, width=3)
                
        elif card_type == "Spell":
            # Add magical-looking effects
            for _ in range(20):
                x1 = np.random.randint(0, width)
                y1 = np.random.randint(0, height)
                x2 = np.random.randint(0, width)
                y2 = np.random.randint(0, height)
                color = tuple(np.random.randint(100, 255, 3))
                draw.line([(x1, y1), (x2, y2)], fill=color, width=2)
                
        elif card_type == "Weapon":
            # Add weapon-like shapes
            center_x = width // 2
            center_y = height // 2
            # Draw handle
            draw.rectangle([center_x-10, center_y, center_x+10, center_y+100], 
                          fill=(139, 69, 19))
            # Draw blade
            points = [(center_x-30, center_y), (center_x+30, center_y), 
                     (center_x, center_y-100)]
            draw.polygon(points, fill=(192, 192, 192))
        
        # Apply some filters to make it look more artistic
        img = img.filter(ImageFilter.GaussianBlur(radius=2))
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.5)
        
        # Add a subtle vignette effect
        vignette = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw_v = ImageDraw.Draw(vignette)
        
        # Create radial gradient for vignette
        for i in range(50):
            box = (i, i, width-i, height-i)
            draw_v.rectangle(box, outline=(0, 0, 0, i*5), width=1)
        
        img = Image.alpha_composite(img.convert('RGBA'), vignette)
        
        # Convert the image to base64 for embedding in HTML
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    
    @staticmethod
    def generate_hero_portrait(hero_class):
        """Generate a hero portrait based on the class"""
        # In a real implementation, this would call an image generation model
        # Here we'll create a simplified hero portrait
        
        width, height = 200, 200
        
        # Class-specific color schemes
        class_colors = {
            "Mage": [(64, 81, 211), (180, 180, 255)],
            "Warrior": [(198, 45, 45), (255, 150, 150)],
            "Hunter": [(0, 150, 0), (200, 255, 200)],
            "Priest": [(200, 200, 200), (255, 255, 255)],
            "Paladin": [(255, 215, 0), (255, 255, 200)],
            "Shaman": [(0, 112, 222), (150, 200, 255)],
            "Druid": [(102, 51, 0), (150, 120, 90)],
            "Warlock": [(138, 43, 226), (200, 150, 255)],
            "Rogue": [(105, 105, 105), (180, 180, 180)],
            "Demon Hunter": [(46, 139, 87), (150, 255, 200)]
        }
        
        colors = class_colors.get(hero_class, [(100, 100, 100), (200, 200, 200)])
        
        # Create circular portrait
        img = Image.new('RGB', (width, height), colors[0])
        mask = Image.new('L', (width, height), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, width, height), fill=255)
        
        # Create the portrait image
        portrait = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(portrait)
        
        # Draw a gradient background
        for y in range(height):
            r = int(colors[0][0] + (colors[1][0] - colors[0][0]) * y / height)
            g = int(colors[0][1] + (colors[1][1] - colors[0][1]) * y / height)
            b = int(colors[0][2] + (colors[1][2] - colors[0][2]) * y / height)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Add some distinctive class elements
        if hero_class == "Mage":
            # Add arcane runes
            for _ in range(10):
                x = np.random.randint(20, width-20)
                y = np.random.randint(20, height-20)
                size = np.random.randint(10, 30)
                draw.ellipse((x-size, y-size, x+size, y+size), outline=(255, 255, 255), width=2)
                
        elif hero_class == "Warrior":
            # Add warrior helmet shape
            center_x = width // 2
            draw.rectangle([center_x-50, 30, center_x+50, 120], outline=(255, 200, 200), width=3)
            
        # Add random decorative elements based on class
        for _ in range(15):
            x = np.random.randint(10, width-10)
            y = np.random.randint(10, height-10)
            size = np.random.randint(5, 15)
            draw.ellipse((x-size, y-size, x+size, y+size), fill=colors[1])
        
        # Apply the circular mask
        portrait.putalpha(mask)
        
        # Add a border
        draw = ImageDraw.Draw(portrait)
        draw.ellipse((0, 0, width-1, height-1), outline=(255, 215, 0), width=5)
        
        # Convert the image to base64 for embedding in HTML
        buffered = BytesIO()
        portrait.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    
    @staticmethod
    def generate_battlefield(player_minions_count, opponent_minions_count):
        """Generate a visual representation of the battlefield"""
        # Create an image showing the battlefield state
        width, height = 600, 300
        battlefield = Image.new('RGB', (width, height), (62, 39, 20))
        draw = ImageDraw.Draw(battlefield)
        
        # Draw the battlefield table
        draw.rectangle([20, 20, width-20, height-20], fill=(101, 67, 33), outline=(145, 111, 60), width=5)
        
        # Draw a center line dividing player and opponent sides
        draw.line([(20, height//2), (width-20, height//2)], fill=(145, 111, 60), width=2)
        
        # Draw opponent minion slots
        slot_width = (width - 40) // 7
        for i in range(7):
            x = 20 + i * slot_width
            y = 30
            draw.rectangle([x+5, y, x+slot_width-5, y+100], outline=(145, 111, 60), width=1)
            if i < opponent_minions_count:
                # Fill with a red minion indicator
                draw.rectangle([x+10, y+5, x+slot_width-10, y+95], fill=(180, 60, 60))
        
        # Draw player minion slots
        for i in range(7):
            x = 20 + i * slot_width
            y = height - 130
            draw.rectangle([x+5, y, x+slot_width-5, y+100], outline=(145, 111, 60), width=1)
            if i < player_minions_count:
                # Fill with a blue minion indicator
                draw.rectangle([x+10, y+5, x+slot_width-10, y+95], fill=(60, 100, 180))
        
        # Convert the image to base64 for embedding in HTML
        buffered = BytesIO()
        battlefield.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"

# Modify the card rendering function to use generated images
def render_card_image(card):
    """Render a visual representation of a card with Hearthstone styling and generated art"""
    card_class = ""
    if card.card_type == "Minion":
        card_class = "card-minion" 
    elif card.card_type == "Spell":
        card_class = "card-spell"
    elif card.card_type == "Weapon":
        card_class = "card-weapon"
    
    # Generate card art
    card_art = ImageGenerator.generate_card_art(card.name, card.card_type, card.card_class)
    
    # Create rarity gem visualization
    rarity_color = "#FFFFFF"  # Common (white)
    if card.rarity == "Rare":
        rarity_color = "#0070DD"  # Blue
    elif card.rarity == "Epic":
        rarity_color = "#A335EE"  # Purple
    elif card.rarity == "Legendary":
        rarity_color = "#FF8000"  # Orange
        
    html = f"""
    <div class="card {card_class}">
        <div class="mana">{card.mana_cost}</div>
        <div class="card-art" style="height: 120px; width: 85%; margin: 10px auto; background-image: url('{card_art}'); background-size: cover; background-position: center; border-radius: 10px; overflow: hidden;"></div>
        <div class="card-name">{card.name}</div>
        <div style="position: absolute; top: 160px; left: 50%; transform: translateX(-50%); width: 80%; height: 1px; background: linear-gradient(to right, transparent, {rarity_color}, transparent);"></div>
        <div class="card-text">{card.text}</div>
    """
    
    if card.card_type == "Minion":
        html += f"""
        <div class="attack">{card.attack}</div>
        <div class="health">{card.health}</div>
        """
    elif card.card_type == "Weapon":
        html += f"""
        <div class="attack">{card.attack}</div>
        <div class="health">{card.durability}</div>
        """
    
    html += "</div>"
    return html

def render_recommendations(recommendations):
    """Render recommendations with appropriate styling based on priority"""
    if not recommendations:
        st.warning("No recommendations available for the current game state.")
        return
    
    for rec in recommendations:
        priority_class = f"{rec['priority']}-priority"
        icon = "🔴" if rec['priority'] == "high" else "🟠" if rec['priority'] == "medium" else "🟢"
        
        st.markdown(f"""
        <div class="recommendation {priority_class}">
            <h3>{icon} {rec['title']}</h3>
            <p>{rec['description']}</p>
        </div>
        """, unsafe_allow_html=True)

def create_sample_game_state():
    """Create a sample game state for demonstration"""
    cards = load_hearthstone_card_data()
    
    # Create player hand and board
    player_hand = [
        next(card for card in cards if card.name == "Fireball"),
        next(card for card in cards if card.name == "Zephrys the Great")
    ]
    
    player_board = [
        next(card for card in cards if card.name == "Zilliax")
    ]
    
    # Create opponent board
    opponent_board = [
        MinionCard(id=101, name="Convincing Infiltrator", mana_cost=5, card_type="Minion", 
                  card_class="Priest", rarity="Rare", text="Taunt, Deathrattle: Destroy a random enemy minion.", 
                  attack=2, health=6, keywords=["Taunt", "Deathrattle"])
    ]
    
    # Create players
    player = Player(
        name="Player",
        hero_class="Mage",
        health=25,
        armor=0,
        mana=7,
        max_mana=7,
        hand=player_hand,
        battlefield=player_board
    )
    
    opponent = Player(
        name="Opponent",
        hero_class="Priest",
        health=18,
        armor=0,
        mana=0,  # Opponent's turn will set this
        max_mana=7,
        hand=[],  # We don't know opponent's hand
        battlefield=opponent_board
    )
    
    # Create game state
    game_state = GameState(
        player=player,
        opponent=opponent,
        turn_number=7,
        current_player="player",
        player_deck_remaining=20,
        opponent_deck_remaining=18
    )
    
    return game_state

def process_chat_query(query, game_state=None):
    """Process a user's chat query and generate a response"""
    # Simple rule-based responses
    query = query.lower().strip()
    
    # Game state aware responses
    if game_state:
        # Questions about current game state
        if "lethal" in query or "win this turn" in query:
            total_damage = sum(minion.attack for minion in game_state.player.battlefield)
            if game_state.player.weapon:
                total_damage += game_state.player.weapon.attack
            
            # Add damage from damage spells in hand
            for card in game_state.player.hand:
                if card.card_type == "Spell" and "damage" in card.text.lower():
                    if "fireball" in card.name.lower():
                        total_damage += 6
            
            if total_damage >= game_state.opponent.health + game_state.opponent.armor:
                return f"Yes! You have {total_damage} potential damage and your opponent has {game_state.opponent.health} health with {game_state.opponent.armor} armor. You can win this turn if you use all your damage optimally."
            else:
                return f"Not quite. You have {total_damage} potential damage, but your opponent has {game_state.opponent.health} health with {game_state.opponent.armor} armor. You need {game_state.opponent.health + game_state.opponent.armor - total_damage} more damage for lethal."
        
        elif "best play" in query or "what should i do" in query:
            recommendations = analyze_game_state(game_state)
            if recommendations:
                high_priority = [r for r in recommendations if r["priority"] == "high"]
                if high_priority:
                    return f"Your best play right now: {high_priority[0]['title']} - {high_priority[0]['description']}"
                else:
                    return f"I recommend: {recommendations[0]['title']} - {recommendations[0]['description']}"
            else:
                return "I need more information about the current game state to recommend the best play."
    
    # Card specific questions
    card_match = re.search(r"how (do I|to) (use|play) ([a-zA-Z\s:']+)(\?)?", query)
    if card_match:
        card_name = card_match.group(3).strip()
        cards = load_hearthstone_card_data()
        matching_card = next((card for card in cards if card.name.lower() == card_name.lower()), None)
        
        if matching_card:
            if matching_card.card_type == "Minion":
                return f"{matching_card.name} is a {matching_card.mana_cost}-mana {matching_card.card_class} minion with {matching_card.attack}/{matching_card.health}. {matching_card.text} Best used to establish board presence and trade efficiently."
            elif matching_card.card_type == "Spell":
                return f"{matching_card.name} is a {matching_card.mana_cost}-mana {matching_card.card_class} spell. {matching_card.text} Use it strategically to gain tempo or value depending on the matchup."
            elif matching_card.card_type == "Weapon":
                return f"{matching_card.name} is a {matching_card.mana_cost}-mana {matching_card.card_class} weapon with {matching_card.attack} attack and {matching_card.durability} durability. {matching_card.text} Good for efficient board control or face damage."
    
    # Class specific questions
    class_match = re.search(r"how (do I|to) (play|beat|counter) ([a-zA-Z\s]+)(\?)?", query)
    if class_match:
        class_name = class_match.group(3).strip()
        action = class_match.group(2)
        
        hero_classes = ["Mage", "Warrior", "Hunter", "Druid", "Priest", "Paladin", "Shaman", "Warlock", "Rogue", "Demon Hunter"]
        matching_class = next((c for c in hero_classes if c.lower() == class_name.lower()), None)
        
        if matching_class:
            if action == "play":
                strategies = {
                    "Mage": "Focus on spell damage and efficient removal. Save your burn spells for lethal when possible.",
                    "Warrior": "Build armor and control the board with weapons and removal spells. Look for value in the late game.",
                    "Hunter": "Apply constant pressure. Remember - your hero power doesn't affect the board, so you need to push damage continuously.",
                    "Druid": "Ramp up your mana early to play big threats ahead of curve. Balance ramp with enough threats.",
                    "Priest": "Control the board and heal efficiently. Look for value generation for the late game.",
                    "Paladin": "Build and buff a board of minions. Divine Shield and Taunt provide great value.",
                    "Shaman": "Use Overload cards efficiently and plan your mana for future turns. Totems can provide incremental value.",
                    "Warlock": "Use your hero power aggressively to draw cards. Your health is a resource - don't be afraid to use it.",
                    "Rogue": "Generate tempo with Combo cards and cheap spells. Control the early game.",
                    "Demon Hunter": "Aggressive attacks with your hero and efficient minions. Focus on consistent damage output."
                }
                return f"To play {matching_class} effectively: {strategies[matching_class]}"
            elif action == "beat" or action == "counter":
                counters = {
                    "Mage": "Apply pressure to force them to use burn spells defensively. Save healing/armor for after their big burst turns.",
                    "Warrior": "Either go extremely aggressive before they build armor, or play for maximum value in the late game.",
                    "Hunter": "Focus on board control and healing. Taunts are very effective against most Hunter decks.",
                    "Druid": "Disrupt their ramp or apply pressure before they can play their big threats.",
                    "Priest": "Apply constant pressure without overcommitting to board clears. Save silence effects for their key resurrect targets.",
                    "Paladin": "Use efficient removal for their buffed minions. AOE is effective against their wide boards.",
                    "Shaman": "Play around their AOE breakpoints and overload turns. Silence effects are good against their evolved minions.",
                    "Warlock": "Apply pressure to punish their life tapping. Save removal for their big threats.",
                    "Rogue": "Taunts are effective against their weapon attacks. Healing helps against their burst damage.",
                    "Demon Hunter": "Prioritize early board control and healing/taunt to stop their aggressive gameplan."
                }
                return f"To counter {matching_class} decks: {counters[matching_class]}"
    
    # Meta and general questions
    if "best deck" in query or "meta" in query:
        meta_decks = load_meta_decks()
        top_deck = meta_decks[0]
        return f"Currently, {top_deck['name']} is considered one of the strongest decks (Tier {top_deck['tier']}). It {top_deck['description']} Key cards include {', '.join(top_deck['key_cards'][:3])}"
    
    elif "mulligan" in query or "starting hand" in query:
        return "For mulligan decisions: 1) Keep low-cost minions that contest the early board. 2) Keep specific tech cards for the matchup. 3) Generally throw back cards costing 4+ mana unless they're critical to your strategy or you have a perfect curve. 4) Always consider your matchup - against aggro you need early answers, against control you need value generators."
    
    elif "beginner" in query or "new player" in query or "start" in query:
        return "For beginners, I recommend: 1) Start with aggro decks as they're usually cheaper and more straightforward to play. 2) Focus on understanding the core mechanics like mana efficiency and board control. 3) Watch streamers or YouTubers to learn advanced tactics. 4) Use budget-friendly decks like Face Hunter or Zoo Warlock while building your collection."
    
    # Default response for unrecognized queries
    return "I'm not sure about that. Could you rephrase your question? You can ask about cards, strategies, classes, or current meta decks. If you're in a game, you can also ask for advice about your current situation."

def game_advisor_ui():
    st.markdown("""
    <div style="text-align: center;">
        <img src="https://i.imgur.com/NdXTdsZ.png" width="100">
    </div>
    """, unsafe_allow_html=True)
    
    st.header("Game Advisor")
    st.subheader("Real-time advice for your Hearthstone matches")
    
    # Tabs for different ways to input game state
    tab1, tab2 = st.tabs(["Manual Input", "Demo Mode"])
    
    with tab1:
        st.write("Enter your current game state to get personalized advice:")
        
        # Input columns for player and opponent
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Your Information")
            player_class = st.selectbox("Your Hero Class", 
                                       ["Mage", "Warrior", "Hunter", "Druid", "Priest", 
                                        "Paladin", "Shaman", "Warlock", "Rogue", "Demon Hunter"])
            
            # Show generated hero portrait
            player_portrait = ImageGenerator.generate_hero_portrait(player_class)
            st.markdown(f"""
            <div style="text-align: center; margin-bottom: 20px;">
                <img src="{player_portrait}" width="120" style="border-radius: 60px; border: 3px solid gold;">
            </div>
            """, unsafe_allow_html=True)
            
            player_health = st.slider("Your Health", 0, 30, 30)
            player_armor = st.slider("Your Armor", 0, 30, 0)
            player_mana = st.slider("Your Current Mana", 0, 10, 10)
            player_cards = st.number_input("Cards in Hand", 0, 10, 4)
            player_deck = st.number_input("Cards in Deck", 0, 30, 20)
        
        with col2:
            st.subheader("Opponent Information")
            opponent_class = st.selectbox("Opponent's Hero Class", 
                                         ["Priest", "Warrior", "Hunter", "Druid", "Mage", 
                                          "Paladin", "Shaman", "Warlock", "Rogue", "Demon Hunter"])
            
            # Show generated hero portrait for opponent
            opponent_portrait = ImageGenerator.generate_hero_portrait(opponent_class)
            st.markdown(f"""
            <div style="text-align: center; margin-bottom: 20px;">
                <img src="{opponent_portrait}" width="120" style="border-radius: 60px; border: 3px solid silver;">
            </div>
            """, unsafe_allow_html=True)
            
            opponent_health = st.slider("Opponent's Health", 0, 30, 30)
            opponent_armor = st.slider("Opponent's Armor", 0, 30, 0)
            opponent_cards = st.number_input("Opponent's Hand Size", 0, 10, 3)
            opponent_deck = st.number_input("Opponent's Deck Size (estimated)", 0, 30, 20)
        
        # Input for board state
        st.subheader("Board State")
        
        # Visualize the battlefield
        col_vis, _ = st.columns([1, 1])
        with col_vis:
            # Your minions
            your_minions_count = st.number_input("How many minions do you have?", 0, 7, 2)
            # Opponent minions
            opponent_minions_count = st.number_input("How many minions does your opponent have?", 0, 7, 1)
            
            # Generate and display battlefield visualization
            battlefield_image = ImageGenerator.generate_battlefield(your_minions_count, opponent_minions_count)
            st.markdown(f"""
            <div style="text-align: center; margin: 20px 0;">
                <img src="{battlefield_image}" width="100%" style="border-radius: 10px; border: 3px solid #C09A5E;">
            </div>
            """, unsafe_allow_html=True)
        
        # Your minions
        st.write("Your minions on board:")
        your_minions = []
        if your_minions_count > 0:
            for i in range(your_minions_count):
                cols = st.columns(4)
                with cols[0]:
                    name = st.text_input(f"Minion {i+1} Name", f"Minion {i+1}")
                with cols[1]:
                    attack = st.number_input(f"Minion {i+1} Attack", 0, 30, 3)
                with cols[2]:
                    health = st.number_input(f"Minion {i+1} Health", 1, 30, 3)
                with cols[3]:
                    keywords = st.multiselect(f"Minion {i+1} Keywords", 
                                             ["Taunt", "Divine Shield", "Rush", "Charge", "Windfury", 
                                              "Poisonous", "Lifesteal", "Reborn", "Stealth"], [])
                
                your_minions.append({
                    "name": name,
                    "attack": attack,
                    "health": health,
                    "keywords": keywords
                })
        
        # Opponent minions
        st.write("Opponent's minions on board:")
        opponent_minions = []
        if opponent_minions_count > 0:
            for i in range(opponent_minions_count):
                cols = st.columns(4)
                with cols[0]:
                    name = st.text_input(f"Opponent Minion {i+1} Name", f"Enemy Minion {i+1}")
                with cols[1]:
                    attack = st.number_input(f"Opponent Minion {i+1} Attack", 0, 30, 4)
                with cols[2]:
                    health = st.number_input(f"Opponent Minion {i+1} Health", 1, 30, 4)
                with cols[3]:
                    keywords = st.multiselect(f"Opponent Minion {i+1} Keywords", 
                                             ["Taunt", "Divine Shield", "Rush", "Charge", "Windfury", 
                                              "Poisonous", "Lifesteal", "Reborn", "Stealth"], ["Taunt"])
                
                opponent_minions.append({
                    "name": name,
                    "attack": attack,
                    "health": health,
                    "keywords": keywords
                })
        
        # Cards in hand (simplified)
        st.subheader("Your Hand")
        st.write("Select key cards in your hand:")
        
        available_cards = st.session_state.card_database
        selected_cards = st.multiselect(
            "Cards in hand",
            [card.name for card in available_cards],
            []
        )
        
        # Create hand from selected cards
        hand = []
        for card_name in selected_cards:
            card = next((card for card in available_cards if card.name == card_name), None)
            if card:
                hand.append(card)
        
        # Turn information
        st.subheader("Turn Information")
        turn_number = st.number_input("Current Turn Number", 1, 30, 7)
        current_player = st.radio("Current Player", ["You", "Opponent"], horizontal=True)
        
        # Create game state when user clicks button
        if st.button("Analyze Game State"):
            # Convert UI inputs to GameState object
            
            # Create player minion objects
            player_battlefield = []
            for minion_data in your_minions:
                player_battlefield.append(
                    MinionCard(
                        id=random.randint(1000, 9999),
                        name=minion_data["name"],
                        mana_cost=0,  # We don't know/care about the cost of minions already on board
                        card_type="Minion",
                        card_class="Neutral",  # Default
                        rarity="Common",  # Default
                        text="",
                        attack=minion_data["attack"],
                        health=minion_data["health"],
                        keywords=minion_data["keywords"]
                    )
                )
            
            # Create opponent minion objects
            opponent_battlefield = []
            for minion_data in opponent_minions:
                opponent_battlefield.append(
                    MinionCard(
                        id=random.randint(1000, 9999),
                        name=minion_data["name"],
                        mana_cost=0,  # We don't know/care about the cost of minions already on board
                        card_type="Minion",
                        card_class="Neutral",  # Default
                        rarity="Common",  # Default
                        text="",
                        attack=minion_data["attack"],
                        health=minion_data["health"],
                        keywords=minion_data["keywords"]
                    )
                )
            
            # Create player object
            player = Player(
                name="You",
                hero_class=player_class,
                health=player_health,
                armor=player_armor,
                mana=player_mana,
                max_mana=min(10, turn_number),
                hand=hand,
                battlefield=player_battlefield
            )
            
            # Create opponent object
            opponent = Player(
                name="Opponent",
                hero_class=opponent_class,
                health=opponent_health,
                armor=opponent_armor,
                mana=0 if current_player == "You" else min(10, turn_number),
                max_mana=min(10, turn_number),
                hand=[],  # We don't know opponent's hand contents
                battlefield=opponent_battlefield
            )
            
            # Create game state
            game_state = GameState(
                player=player,
                opponent=opponent,
                turn_number=turn_number,
                current_player="player" if current_player == "You" else "opponent",
                player_deck_remaining=player_deck,
                opponent_deck_remaining=opponent_deck
            )
            
            # Store in session state and analyze
            st.session_state.game_state = game_state
            recommendations = analyze_game_state(game_state)
            
            # Store analysis in history
            st.session_state.analysis_history.append({
                "timestamp": time.time(),
                "turn": turn_number,
                "recommendations": recommendations
            })
            
            # Show recommendations
            st.subheader("Recommendations")
            render_recommendations(recommendations)
            
    with tab2:
        st.write("Use a pre-configured game state to see how the advisor works:")
        
        if st.button("Load Sample Game"):
            # Create and store a sample game state
            sample_state = create_sample_game_state()
            st.session_state.game_state = sample_state
            
            # Analyze the sample state
            recommendations = analyze_game_state(sample_state)
            
            # Store in history
            st.session_state.analysis_history.append({
                "timestamp": time.time(),
                "turn": sample_state.turn_number,
                "recommendations": recommendations
            })
        
        # If a game state exists, show it and the recommendations
        if st.session_state.game_state:
            game_state = st.session_state.game_state
            player = game_state.player
            opponent = game_state.opponent
            
            # Display game state summary
            st.subheader("Current Game State")
            
            # Generate hero portraits
            player_portrait = ImageGenerator.generate_hero_portrait(player.hero_class)
            opponent_portrait = ImageGenerator.generate_hero_portrait(opponent.hero_class)
            
            # Generate battlefield visualization
            battlefield_image = ImageGenerator.generate_battlefield(
                len(player.battlefield), len(opponent.battlefield))
            
            # Display the battlefield
            st.markdown(f"""
            <div style="text-align: center; margin: 20px 0;">
                <img src="{battlefield_image}" width="100%" style="border-radius: 10px; border: 3px solid #C09A5E;">
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                # Display player hero portrait
                st.markdown(f"""
                <div style="text-align: center; margin-bottom: 20px;">
                    <img src="{player_portrait}" width="100" style="border-radius: 50px; border: 3px solid gold;">
                    <h3>{player.hero_class}</h3>
                </div>
                """, unsafe_allow_html=True)
                
                st.write(f"**You ({player.hero_class})**: {player.health} Health, {player.armor} Armor")
                st.write(f"Mana: {player.mana}/{player.max_mana}")
                st.write(f"Cards in hand: {len(player.hand)}")
                st.write(f"Cards in deck: {game_state.player_deck_remaining}")
                
                # Display player's hand
                if player.hand:
                    st.write("**Your Hand:**")
                    hand_cols = st.columns(len(player.hand))
                    for i, card in enumerate(player.hand):
                        with hand_cols[i]:
                            st.markdown(render_card_image(card), unsafe_allow_html=True)
                
                # Display player's board
                if player.battlefield:
                    st.write("**Your Board:**")
                    board_cols = st.columns(len(player.battlefield))
                    for i, minion in enumerate(player.battlefield):
                        with board_cols[i]:
                            st.markdown(render_card_image(minion), unsafe_allow_html=True)
            
            with col2:
                # Display opponent hero portrait
                st.markdown(f"""
                <div style="text-align: center; margin-bottom: 20px;">
                    <img src="{opponent_portrait}" width="100" style="border-radius: 50px; border: 3px solid silver;">
                    <h3>{opponent.hero_class}</h3>
                </div>
                """, unsafe_allow_html=True)
                
                st.write(f"**Opponent ({opponent.hero_class})**: {opponent.health} Health, {opponent.armor} Armor")
                st.write(f"Turn: {game_state.turn_number}")
                st.write(f"Current Player: {'You' if game_state.current_player == 'player' else 'Opponent'}")
                st.write(f"Opponent cards in deck: {game_state.opponent_deck_remaining}")
                
                # Display opponent's board
                if opponent.battlefield:
                    st.write("**Opponent's Board:**")
                    opp_board_cols = st.columns(len(opponent.battlefield))
                    for i, minion in enumerate(opponent.battlefield):
                        with opp_board_cols[i]:
                            st.markdown(render_card_image(minion), unsafe_allow_html=True)
            
            # Show recommendations
            st.subheader("Recommendations")
            recommendations = analyze_game_state(game_state)
            render_recommendations(recommendations)

def deck_analysis_ui():
    st.markdown("""
    <div style="text-align: center;">
        <img src="https://i.imgur.com/GfhaMvK.png" width="100">
    </div>
    """, unsafe_allow_html=True)
    
    st.header("Deck Analysis")
    st.subheader("Get insights about your deck's strengths and weaknesses")
    
    # Option to upload a deck code or select from presets
    st.write("Input your deck code or select a preset deck:")
    
    deck_input_option = st.radio("Deck Input Method", ["Deck Code", "Preset Deck"])
    
    if deck_input_option == "Deck Code":
        deck_code = st.text_input("Enter your Hearthstone deck code")
        
        if deck_code:
            st.warning("Deck code parsing would be implemented in a full version. Using a preset deck for demonstration.")
            # In a real implementation, we would parse the deck code here
            st.session_state.current_deck = {
                "name": "Custom Deck",
                "class": "Mage",
                "cards": [card for card in st.session_state.card_database if card.card_class in ["Neutral", "Mage"]][:30]
            }
    else:
        preset_decks = [
            "Tempo Demon Hunter",
            "Control Warrior",
            "Spell Mage"
        ]
        selected_deck = st.selectbox("Select a preset deck", preset_decks)
        
        if selected_deck and st.button("Analyze Deck"):
            # In a real implementation, we would load the actual deck list
            st.session_state.current_deck = {
                "name": selected_deck,
                "class": selected_deck.split()[1] if len(selected_deck.split()) > 1 else "Neutral",
                "cards": [card for card in st.session_state.card_database 
                         if card.card_class in ["Neutral", selected_deck.split()[1]]][:30]
            }
    
    # If a deck is selected, show analysis
    if st.session_state.current_deck:
        deck = st.session_state.current_deck
        
        st.subheader(f"Analysis of {deck['name']}")
        
        # Deck composition by mana cost (mana curve)
        st.write("**Mana Curve:**")
        mana_costs = [card.mana_cost for card in deck["cards"]]
        mana_curve = pd.DataFrame({
            "Mana Cost": range(0, 11),
            "Count": [mana_costs.count(i) for i in range(0, 11)]
        })
        st.bar_chart(mana_curve.set_index("Mana Cost"))
        
        # Deck composition by card type
        card_types = [card.card_type for card in deck["cards"]]
        type_counts = {card_type: card_types.count(card_type) for card_type in set(card_types)}
        st.write("**Card Types:**")
        st.write(type_counts)
        
        # Matchup analysis
        st.subheader("Matchup Analysis")
        matchups = {
            "Tempo Demon Hunter": "Unfavorable - They can pressure you early",
            "Control Warrior": "Favorable - You have more value",
            "Spell Mage": "Even - Both decks have similar power levels",
            "Face Hunter": "Unfavorable - Too aggressive for this deck",
            "Libram Paladin": "Favorable - You can outvalue them"
        }
        
        for matchup, analysis in matchups.items():
            st.write(f"**{matchup}**: {analysis}")
        
        # Mulligan advice
        st.subheader("Mulligan Advice")
        st.write("""
        **General Mulligan Strategy:**
        - Look for early game minions to establish board presence
        - Keep specific tech cards against known matchups
        - Avoid keeping high-cost cards unless they're crucial
        """)
        
        # Key cards to keep in specific matchups
        st.write("**Cards to keep against specific classes:**")
        mulligan_advice = {
            "Hunter": "Early removal and healing",
            "Warrior": "Value generation cards",
            "Mage": "Pressure cards and counterspell",
            "Priest": "Tempo plays and value generators"
        }
        for class_name, advice in mulligan_advice.items():
            st.write(f"**Against {class_name}**: {advice}")

def meta_report_ui():
    st.markdown("""
    <div style="text-align: center;">
        <img src="https://i.imgur.com/NmF5mRh.png" width="100">
    </div>
    """, unsafe_allow_html=True)
    
    st.header("Meta Report")
    st.subheader("Current Hearthstone meta overview and trends")
    
    # Load meta decks
    meta_decks = load_meta_decks()
    
    # Display tier list
    st.subheader("Current Tier List")
    
    # Create tier list dataframe
    tier_data = {
        "Deck": [deck["name"] for deck in meta_decks],
        "Tier": [deck["tier"] for deck in meta_decks],
        "Key Cards": [", ".join(deck["key_cards"][:2]) + "..." for deck in meta_decks]
    }
    tier_df = pd.DataFrame(tier_data)
    st.table(tier_df)
    
    # Display individual deck information
    st.subheader("Top Decks Analysis")
    
    for deck in meta_decks:
        with st.expander(f"{deck['name']} (Tier {deck['tier']})"):
            st.write(f"**Description:** {deck['description']}")
            st.write("**Key Cards:**")
            for card in deck["key_cards"]:
                st.write(f"- {card}")
            st.write("**Countered by:**")
            for counter in deck["counters"]:
                st.write(f"- {counter}")
    
    # Meta trends
    st.subheader("Meta Trends")
    st.write("""
    **Current Trends:**
    - Aggressive decks are becoming more popular in the current meta
    - Control decks are adapting with more early-game tools
    - Combo decks are falling out of favor due to the speed of the meta
    
    **Predicted Shifts:**
    - Expect an increase in tech cards targeting aggressive strategies
    - Mid-range decks may make a comeback as the meta adjusts
    - New cards from the upcoming expansion will likely shake up the meta
    """)

def chat_ui():
    """Display a chat interface for talking with the Hearthstone AI Assistant"""
    st.markdown("""
    <div class="logo-container">
        <img src="https://www.pngall.com/wp-content/uploads/13/Hearthstone-Logo-PNG-Image.png" class="logo-img">
    </div>
    """, unsafe_allow_html=True)
    
    st.header("Hearthstone Chat Assistant")
    
    # Get the current game state if available
    current_game_state = st.session_state.game_state if 'game_state' in st.session_state else None
    
    # Draw the chat UI
    st.markdown('<div class="chat-header"><h3>🧙‍♂️ Hearthstone AI Chat</h3></div>', unsafe_allow_html=True)
    
    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f'<div class="chat-message user-message">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message assistant-message">{message["content"]}</div>', unsafe_allow_html=True)
    
    # Chat input
    user_input = st.text_input("Ask me anything about Hearthstone", key="chat_input", 
                               placeholder="e.g., 'How do I play against Mage?' or 'What's the best play now?'",
                               label_visibility="collapsed")
    
    if user_input:
        # Add user message to chat
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Process the query and get response
        assistant_response = process_chat_query(user_input, current_game_state)
        
        # Add assistant response to chat
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
        
        # Clear the input box (need to rerun to show the updated chat)
        st.rerun()
    
    st.markdown('<div class="chat-footer"></div>', unsafe_allow_html=True)
    
    # Add some example questions
    with st.expander("✨ Example questions you can ask"):
        st.markdown("""
        - "How do I play against Mage?"
        - "What's the best deck in the current meta?"
        - "How do I use Zephrys the Great?"
        - "Do I have lethal this turn?"
        - "What's the best play right now?"
        - "How should I mulligan against aggro decks?"
        - "I'm a beginner, how should I start?"
        """)

def main():
    # Add a Hearthstone logo at the top
    st.markdown("""
    <div class="logo-container">
        <img src="https://www.pngall.com/wp-content/uploads/13/Hearthstone-Logo-PNG-Image.png" class="logo-img">
        <h1>AI Assistant</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for mode selection and meta information
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <img src="https://cdn-icons-png.flaticon.com/512/667/667029.png" width="120" style="filter: drop-shadow(0 4px 6px rgba(0,0,0,0.5));">
        </div>
        """, unsafe_allow_html=True)
        
        st.header("Options")
        app_mode = st.radio("Mode", ["Game Advisor", "Deck Analysis", "Meta Report", "Chat Assistant"])
        
        st.header("About")
        st.info("""
        This Hearthstone AI Assistant helps you make optimal plays during your Hearthstone matches.
        Choose a mode from above to get started.
        """)
    
    # Load card database if not already loaded
    if st.session_state.card_database is None:
        st.session_state.card_database = load_hearthstone_card_data()
    
    if app_mode == "Game Advisor":
        game_advisor_ui()
    elif app_mode == "Deck Analysis":
        deck_analysis_ui()
    elif app_mode == "Meta Report":
        meta_report_ui()
    elif app_mode == "Chat Assistant":
        chat_ui()

if __name__ == "__main__":
    main()
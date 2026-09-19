import os
import json
import sqlite3
import asyncio
from pathlib import Path

import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
DB_PATH = Path("data/builder.sqlite")
BACKUP_DIR = Path("backups")
DB_PATH.parent.mkdir(exist_ok=True)
BACKUP_DIR.mkdir(exist_ok=True)

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents)

db = sqlite3.connect(DB_PATH)
db.execute("""
CREATE TABLE IF NOT EXISTS guild_config (
    guild_id INTEGER PRIMARY KEY,
    template TEXT,
    welcome_channel_id INTEGER,
    member_role_id INTEGER
)
""")
db.commit()

TEMPLATES = {
    "community": {
        "name": "✨ Community",
        "roles": [
            ("👑 Owner", discord.Colour.red(), True),
            ("🛡️ Admin", discord.Colour.orange(), True),
            ("⚔️ Moderator", discord.Colour.blue(), True),
            ("💎 Helper", discord.Colour.teal(), True),
            ("🚀 Booster", discord.Colour.magenta(), False),
            ("⭐ Member", discord.Colour.green(), False),
        ],
        "categories": {
            "📌 INFORMATION": [
                ("📜・rules", "text"),
                ("📢・announcements", "text"),
                ("👋・welcome", "text"),
                ("📖・server-info", "text"),
                ("📝・guidelines", "text"),
                ("🎭・self-roles", "text"),
            ],
            "💬 COMMUNITY": [
                ("💬・general-chat", "text"),
                ("🗣️・off-topic", "text"),
                ("👋・introductions", "text"),
                ("😂・memes", "text"),
                ("📸・media-sharing", "text"),
                ("🎨・creative-corner", "text"),
                ("💡・suggestions", "text"),
                ("🤝・partnerships", "text"),
            ],
            "🎉 EVENTS & FUN": [
                ("🎉・events", "text"),
                ("🎁・giveaways", "text"),
                ("🎮・game-night", "text"),
                ("🏆・contests", "text"),
                ("📊・polls", "text"),
            ],
            "🤖 BOTS & COMMANDS": [
                ("🤖・bot-commands", "text"),
                ("📈・level-up", "text"),
                ("💰・economy", "text"),
                ("🎵・music-requests", "text"),
            ],
            "🎫 SUPPORT": [
                ("🎫・create-ticket", "text"),
                ("❓・help-desk", "text"),
                ("📋・faq", "text"),
            ],
            "🔊 VOICE HANGOUT": [
                ("💬・General Voice", "voice"),
                ("🎮・Gaming Lounge", "voice"),
                ("🎵・Music Room", "voice"),
                ("🎬・Movie Night", "voice"),
                ("😴・AFK Zone", "voice"),
            ],
            "🛡️ STAFF ONLY": [
                ("💼・staff-chat", "text"),
                ("📋・staff-logs", "text"),
                ("🔨・mod-actions", "text"),
                ("🚨・reports", "text"),
            ],
        },
    },
    "gaming": {
        "name": "🎮 Gaming",
        "roles": [
            ("👑 Owner", discord.Colour.red(), True),
            ("🛡️ Admin", discord.Colour.orange(), True),
            ("⚔️ Moderator", discord.Colour.blue(), True),
            ("🎪 Event Manager", discord.Colour.purple(), True),
            ("🎮 Pro Gamer", discord.Colour.gold(), False),
            ("⭐ Gamer", discord.Colour.green(), False),
            ("🚀 Booster", discord.Colour.magenta(), False),
        ],
        "categories": {
            "📌 SERVER INFO": [
                ("📜・rules", "text"),
                ("📢・announcements", "text"),
                ("👋・welcome", "text"),
                ("🎭・get-roles", "text"),
                ("📅・event-schedule", "text"),
            ],
            "🎮 GAMING CENTRAL": [
                ("💬・general-gaming", "text"),
                ("🎯・looking-for-squad", "text"),
                ("🏆・leaderboards", "text"),
                ("💎・pro-strats", "text"),
                ("🎥・gameplay-clips", "text"),
                ("📸・gaming-screenshots", "text"),
                ("🎬・stream-links", "text"),
                ("💡・game-suggestions", "text"),
            ],
            "🕹️ GAME ZONES": [
                ("🔫・fps-games", "text"),
                ("⚔️・rpg-adventure", "text"),
                ("🏎️・racing-sports", "text"),
                ("🧩・puzzle-casual", "text"),
                ("👾・retro-gaming", "text"),
            ],
            "🎉 EVENTS & TOURNAMENTS": [
                ("🏆・tournaments", "text"),
                ("🎁・giveaways", "text"),
                ("🎪・community-events", "text"),
                ("📊・voting-polls", "text"),
            ],
            "🤖 BOT ZONE": [
                ("🤖・bot-commands", "text"),
                ("📈・level-rankings", "text"),
                ("🎵・music-player", "text"),
            ],
            "💬 CHILL ZONE": [
                ("☕・lounge", "text"),
                ("🗣️・random-talk", "text"),
                ("😂・memes-only", "text"),
                ("📸・share-media", "text"),
                ("🎨・fan-art", "text"),
            ],
            "🎫 SUPPORT": [
                ("🎫・support-tickets", "text"),
                ("❓・questions", "text"),
                ("🤝・partner-with-us", "text"),
            ],
            "🔊 VOICE ROOMS": [
                ("🎮・Squad Up #1", "voice"),
                ("🎮・Squad Up #2", "voice"),
                ("🎮・Squad Up #3", "voice"),
                ("💬・Chill Lounge", "voice"),
                ("🎵・Music Vibes", "voice"),
                ("🎬・Watch Party", "voice"),
                ("😴・AFK Station", "voice"),
            ],
            "🛡️ STAFF HQ": [
                ("💼・staff-chat", "text"),
                ("📋・action-logs", "text"),
                ("🔨・moderation", "text"),
                ("🚨・user-reports", "text"),
            ],
        },
    },
    "minecraft": {
        "name": "⛏️ Minecraft",
        "roles": [
            ("👑 Owner", discord.Colour.red(), True),
            ("🛡️ Admin", discord.Colour.orange(), True),
            ("⚔️ Moderator", discord.Colour.blue(), True),
            ("🏗️ Builder", discord.Colour.gold(), False),
            ("📹 Content Creator", discord.Colour.red(), False),
            ("🚀 Booster", discord.Colour.magenta(), False),
            ("⭐ Player", discord.Colour.green(), False),
        ],
        "categories": {
            "📌 SERVER HUB": [
                ("📜・rules", "text"),
                ("📢・announcements", "text"),
                ("👋・welcome-spawn", "text"),
                ("📖・server-guide", "text"),
                ("🟢・server-status", "text"),
                ("🗺️・world-map", "text"),
                ("🎭・choose-roles", "text"),
            ],
            "⛏️ MINECRAFT WORLD": [
                ("💬・minecraft-chat", "text"),
                ("📊・player-stats", "text"),
                ("🏆・top-players", "text"),
                ("💰・economy-trade", "text"),
                ("🛒・marketplace", "text"),
                ("🎁・daily-rewards", "text"),
                ("📸・builds-showcase", "text"),
                ("🎥・epic-moments", "text"),
                ("🏗️・building-ideas", "text"),
                ("🐛・bug-reports", "text"),
                ("💡・server-suggestions", "text"),
            ],
            "🎉 EVENTS & MINIGAMES": [
                ("🎪・events-hub", "text"),
                ("🎁・giveaways", "text"),
                ("🏆・competitions", "text"),
                ("🎮・minigames", "text"),
            ],
            "🤖 BOT COMMANDS": [
                ("🤖・bot-zone", "text"),
                ("📈・leveling-system", "text"),
                ("🎵・music-player", "text"),
            ],
            "💬 COMMUNITY": [
                ("💬・general-chat", "text"),
                ("🗣️・off-topic", "text"),
                ("😂・memes-corner", "text"),
                ("📸・random-pics", "text"),
                ("🎨・pixel-art", "text"),
                ("🤝・find-teammates", "text"),
            ],
            "🎫 HELP & SUPPORT": [
                ("🎫・open-ticket", "text"),
                ("❓・help-desk", "text"),
                ("📋・common-questions", "text"),
            ],
            "🔊 VOICE CHANNELS": [
                ("⛏️・Mining Squad", "voice"),
                ("🏗️・Building Zone", "voice"),
                ("🎮・PvP Arena", "voice"),
                ("💬・Hangout", "voice"),
                ("🎵・Music Chill", "voice"),
                ("😴・AFK Mine", "voice"),
            ],
            "🛡️ STAFF AREA": [
                ("💼・staff-discussion", "text"),
                ("📋・server-logs", "text"),
                ("🔨・mod-actions", "text"),
                ("🚨・player-reports", "text"),
            ],
        },
    },
    "social": {
        "name": "🌸 Social / Aesthetic",
        "roles": [
            ("👑 Owner", discord.Colour.red(), True),
            ("🛡️ Admin", discord.Colour.orange(), True),
            ("⚔️ Moderator", discord.Colour.blue(), True),
            ("💎 Helper", discord.Colour.teal(), True),
            ("🚀 Booster", discord.Colour.magenta(), False),
            ("✨ VIP", discord.Colour.gold(), False),
            ("⭐ Member", discord.Colour.green(), False),
        ],
        "categories": {
            "🌸・WELCOME": [
                ("👋・welcome", "text"),
                ("📜・rules", "text"),
                ("🎭・get-roles", "text"),
                ("🚪・goodbye", "text"),
            ],
            "🌿・MAIN LOUNGE": [
                ("💬・main-chat", "text"),
                ("📷・photo-dump", "text"),
                ("🎥・video-share", "text"),
                ("📸・selfies", "text"),
                ("🤳・aesthetic-pics", "text"),
                ("💭・daily-quotes", "text"),
                ("🐾・cute-pets", "text"),
                ("✨・vibes", "text"),
            ],
            "💬・CHAT ROOMS": [
                ("🎤・vent-space", "text"),
                ("☕・casual-talk", "text"),
                ("👥・couples-zone", "text"),
                ("🌐・singles-hangout", "text"),
                ("📢・spam-allowed", "text"),
                ("🤖・bot-playground", "text"),
            ],
            "🎮・FUN & GAMES": [
                ("😂・memes-lol", "text"),
                ("🎮・word-games", "text"),
                ("🔥・truth-or-dare", "text"),
                ("🎀・counting-game", "text"),
                ("🎁・giveaways", "text"),
                ("📊・polls-votes", "text"),
                ("🎯・trivia-quiz", "text"),
            ],
            "🎵・VOICE HANGOUT": [
                ("💬・Main Lounge", "voice"),
                ("🎮・Gaming Voice", "voice"),
                ("🎵・Music Chill", "voice"),
                ("📞・Call Zone", "voice"),
                ("😴・AFK Room", "voice"),
            ],
            "🛡️・STAFF": [
                ("💼・staff-chat", "text"),
                ("📋・server-logs", "text"),
                ("🔨・mod-tools", "text"),
                ("🚨・user-reports", "text"),
            ],
        },
    },
    "shop": {
        "name": "🛒 Shop / Business",
        "roles": [
            ("👑 Owner", discord.Colour.red(), True),
            ("🛡️ Admin", discord.Colour.orange(), True),
            ("💼 Staff", discord.Colour.blue(), True),
            ("💎 Support Team", discord.Colour.teal(), True),
            ("⭐ Customer", discord.Colour.green(), False),
            ("🚀 Booster", discord.Colour.magenta(), False),
        ],
        "categories": {
            "📌 INFORMATION": [
                ("📜・rules", "text"),
                ("📢・announcements", "text"),
                ("👋・welcome", "text"),
                ("💰・pricing", "text"),
                ("📖・faq", "text"),
                ("💳・payment-methods", "text"),
            ],
            "🛒 SHOP & PRODUCTS": [
                ("🛍️・browse-products", "text"),
                ("⭐・testimonials", "text"),
                ("💳・payment-info", "text"),
                ("📦・order-tracking", "text"),
                ("🎁・discounts-deals", "text"),
                ("✨・new-arrivals", "text"),
            ],
            "🎫 SUPPORT & TICKETS": [
                ("🎫・open-ticket", "text"),
                ("❓・general-help", "text"),
                ("📋・ticket-archive", "text"),
            ],
            "📣 COMMUNITY": [
                ("💬・general-chat", "text"),
                ("📸・customer-showcase", "text"),
                ("💡・feedback-suggestions", "text"),
                ("🤝・partnerships", "text"),
            ],
            "🔊 VOICE SUPPORT": [
                ("💬・Customer Support", "voice"),
                ("🛒・Shopping Help", "voice"),
                ("😴・AFK", "voice"),
            ],
            "🛡️ STAFF ONLY": [
                ("💼・staff-discussion", "text"),
                ("📋・server-logs", "text"),
                ("💰・order-management", "text"),
                ("📊・analytics", "text"),
            ],
        },
    },
    "anime": {
        "name": "🌸 Anime & Manga",
        "roles": [
            ("👑 Sensei", discord.Colour.red(), True),
            ("🛡️ Admin", discord.Colour.orange(), True),
            ("⚔️ Moderator", discord.Colour.blue(), True),
            ("🌸 Helper", discord.Colour.teal(), True),
            ("✨ Otaku", discord.Colour.purple(), False),
            ("📚 Weeb", discord.Colour.green(), False),
            ("🚀 Booster", discord.Colour.magenta(), False),
        ],
        "categories": {
            "🌸 WELCOME ZONE": [
                ("👋・welcome-dojo", "text"),
                ("📜・server-rules", "text"),
                ("🎭・pick-roles", "text"),
                ("📢・announcements", "text"),
                ("📖・how-to-start", "text"),
            ],
            "🎌 ANIME DISCUSSION": [
                ("💬・general-anime", "text"),
                ("🔥・trending-shows", "text"),
                ("📺・currently-watching", "text"),
                ("⭐・recommendations", "text"),
                ("🎬・movie-night", "text"),
                ("💡・anime-opinions", "text"),
                ("🎭・character-talk", "text"),
            ],
            "📚 MANGA & LIGHT NOVELS": [
                ("📖・manga-discussion", "text"),
                ("✨・light-novels", "text"),
                ("🎨・webtoons", "text"),
                ("📚・reading-club", "text"),
            ],
            "🎨 CREATIVE CORNER": [
                ("🎨・fan-art", "text"),
                ("✍️・fanfiction", "text"),
                ("🖼️・wallpapers", "text"),
                ("📸・cosplay", "text"),
                ("🎵・anime-music", "text"),
            ],
            "🎮 ANIME GAMING": [
                ("🎮・anime-games", "text"),
                ("🃏・gacha-pulls", "text"),
                ("⚔️・gaming-party", "text"),
            ],
            "😂 FUN & MEMES": [
                ("😂・anime-memes", "text"),
                ("🎲・games-quizzes", "text"),
                ("💝・waifus-husbandos", "text"),
            ],
            "🤖 BOT COMMANDS": [
                ("🤖・bot-zone", "text"),
                ("📈・leveling", "text"),
                ("🎵・music-player", "text"),
            ],
            "🎫 SUPPORT": [
                ("🎫・support-tickets", "text"),
                ("❓・help", "text"),
                ("🤝・partnerships", "text"),
            ],
            "🔊 VOICE CHANNELS": [
                ("💬・Watch Party", "voice"),
                ("🎮・Gaming Voice", "voice"),
                ("🎵・Music Room", "voice"),
                ("☕・Chill Lounge", "voice"),
                ("😴・AFK Realm", "voice"),
            ],
            "🛡️ STAFF ZONE": [
                ("💼・staff-chat", "text"),
                ("📋・logs", "text"),
                ("🔨・moderation", "text"),
            ],
        },
    },
    "art": {
        "name": "🎨 Art & Creative",
        "roles": [
            ("👑 Master Artist", discord.Colour.red(), True),
            ("🛡️ Admin", discord.Colour.orange(), True),
            ("⚔️ Moderator", discord.Colour.blue(), True),
            ("🎨 Art Mentor", discord.Colour.purple(), True),
            ("✨ Professional", discord.Colour.gold(), False),
            ("🖌️ Artist", discord.Colour.green(), False),
            ("🚀 Booster", discord.Colour.magenta(), False),
        ],
        "categories": {
            "🌟 WELCOME": [
                ("👋・welcome-studio", "text"),
                ("📜・rules", "text"),
                ("🎭・roles", "text"),
                ("📢・announcements", "text"),
                ("📖・about-us", "text"),
            ],
            "🎨 ART GALLERY": [
                ("🖼️・digital-art", "text"),
                ("🖌️・traditional-art", "text"),
                ("✏️・sketches-wip", "text"),
                ("🎭・character-design", "text"),
                ("🌈・abstract-art", "text"),
                ("📸・photography", "text"),
                ("🎥・animations", "text"),
                ("✨・portfolio-showcase", "text"),
            ],
            "💬 DISCUSSION": [
                ("💬・general-chat", "text"),
                ("🗣️・art-talk", "text"),
                ("💡・feedback-critique", "text"),
                ("📚・tutorials-tips", "text"),
                ("🎯・challenges", "text"),
                ("💭・inspiration", "text"),
            ],
            "🎨 RESOURCES": [
                ("📦・asset-sharing", "text"),
                ("🖌️・brushes-tools", "text"),
                ("🎨・color-palettes", "text"),
                ("📖・learning-resources", "text"),
            ],
            "💼 COMMISSIONS": [
                ("💰・commission-info", "text"),
                ("🛒・open-commissions", "text"),
                ("📋・commission-queue", "text"),
                ("⭐・reviews", "text"),
            ],
            "🎉 EVENTS": [
                ("🎪・art-events", "text"),
                ("🏆・contests", "text"),
                ("🎁・giveaways", "text"),
            ],
            "🤖 BOT ZONE": [
                ("🤖・bot-commands", "text"),
                ("🎨・ai-art", "text"),
            ],
            "🎫 SUPPORT": [
                ("🎫・support", "text"),
                ("🤝・collaborations", "text"),
            ],
            "🔊 VOICE STUDIO": [
                ("🎨・Art Session", "voice"),
                ("💬・Creative Lounge", "voice"),
                ("🎵・Music While Drawing", "voice"),
                ("😴・AFK", "voice"),
            ],
            "🛡️ STAFF": [
                ("💼・staff-chat", "text"),
                ("📋・logs", "text"),
                ("🔨・moderation", "text"),
            ],
        },
    },
    "music": {
        "name": "🎵 Music & Audio",
        "roles": [
            ("👑 Maestro", discord.Colour.red(), True),
            ("🛡️ Admin", discord.Colour.orange(), True),
            ("⚔️ Moderator", discord.Colour.blue(), True),
            ("🎵 DJ", discord.Colour.purple(), True),
            ("🎸 Musician", discord.Colour.gold(), False),
            ("🎧 Music Lover", discord.Colour.green(), False),
            ("🚀 Booster", discord.Colour.magenta(), False),
        ],
        "categories": {
            "🎶 WELCOME": [
                ("👋・welcome-stage", "text"),
                ("📜・rules", "text"),
                ("🎭・get-roles", "text"),
                ("📢・announcements", "text"),
                ("🎵・whats-new", "text"),
            ],
            "🎵 MUSIC DISCUSSION": [
                ("💬・general-music", "text"),
                ("🎸・rock-metal", "text"),
                ("🎹・electronic-edm", "text"),
                ("🎤・hip-hop-rap", "text"),
                ("🎺・jazz-classical", "text"),
                ("🎧・indie-alternative", "text"),
                ("🌍・world-music", "text"),
                ("💡・recommendations", "text"),
            ],
            "🎤 MUSIC SHARING": [
                ("🎵・share-songs", "text"),
                ("📻・spotify-links", "text"),
                ("🎥・music-videos", "text"),
                ("🎧・playlists", "text"),
                ("🔥・new-releases", "text"),
            ],
            "🎹 CREATION ZONE": [
                ("🎼・original-music", "text"),
                ("🎛️・production-tips", "text"),
                ("🎸・covers-remixes", "text"),
                ("💡・feedback-critique", "text"),
                ("📚・tutorials", "text"),
            ],
            "🎉 EVENTS": [
                ("🎪・listening-parties", "text"),
                ("🏆・music-contests", "text"),
                ("🎁・giveaways", "text"),
            ],
            "🤖 BOT COMMANDS": [
                ("🤖・bot-zone", "text"),
                ("🎵・music-player", "text"),
            ],
            "🎫 SUPPORT": [
                ("🎫・support", "text"),
                ("🤝・collaborations", "text"),
            ],
            "🔊 VOICE STUDIOS": [
                ("🎵・Music Room #1", "voice"),
                ("🎵・Music Room #2", "voice"),
                ("🎤・Live Performance", "voice"),
                ("🎧・DJ Session", "voice"),
                ("💬・Chill Lounge", "voice"),
                ("😴・AFK", "voice"),
            ],
            "🛡️ STAFF": [
                ("💼・staff-chat", "text"),
                ("📋・logs", "text"),
                ("🔨・moderation", "text"),
            ],
        },
    },
    "study": {
        "name": "📚 Study & Learning",
        "roles": [
            ("👑 Principal", discord.Colour.red(), True),
            ("🛡️ Admin", discord.Colour.orange(), True),
            ("⚔️ Moderator", discord.Colour.blue(), True),
            ("🎓 Tutor", discord.Colour.purple(), True),
            ("📚 Scholar", discord.Colour.gold(), False),
            ("✏️ Student", discord.Colour.green(), False),
            ("🚀 Booster", discord.Colour.magenta(), False),
        ],
        "categories": {
            "📚 WELCOME": [
                ("👋・welcome-hall", "text"),
                ("📜・rules", "text"),
                ("🎭・choose-subjects", "text"),
                ("📢・announcements", "text"),
                ("📅・study-schedule", "text"),
            ],
            "💬 GENERAL": [
                ("💬・general-chat", "text"),
                ("☕・lounge", "text"),
                ("💡・motivation", "text"),
                ("🎯・study-goals", "text"),
                ("📖・resources", "text"),
            ],
            "📖 STUDY SUBJECTS": [
                ("🔢・mathematics", "text"),
                ("🧪・science", "text"),
                ("📚・literature", "text"),
                ("🌍・geography-history", "text"),
                ("💻・computer-science", "text"),
                ("🎨・arts-humanities", "text"),
                ("🗣️・languages", "text"),
            ],
            "✏️ STUDY HELP": [
                ("❓・homework-help", "text"),
                ("🎓・tutoring", "text"),
                ("📝・notes-sharing", "text"),
                ("🤝・study-partners", "text"),
            ],
            "🎯 PRODUCTIVITY": [
                ("⏰・pomodoro-timers", "text"),
                ("📊・progress-tracking", "text"),
                ("🏆・achievements", "text"),
                ("📅・deadlines", "text"),
            ],
            "🎉 BREAKS & FUN": [
                ("😂・memes", "text"),
                ("🎮・games", "text"),
                ("🎁・giveaways", "text"),
            ],
            "🤖 BOT ZONE": [
                ("🤖・bot-commands", "text"),
                ("🎵・study-music", "text"),
            ],
            "🎫 SUPPORT": [
                ("🎫・support", "text"),
                ("💡・suggestions", "text"),
            ],
            "🔊 STUDY ROOMS": [
                ("📚・Silent Study", "voice"),
                ("💬・Study Group #1", "voice"),
                ("💬・Study Group #2", "voice"),
                ("☕・Break Room", "voice"),
                ("😴・AFK", "voice"),
            ],
            "🛡️ STAFF": [
                ("💼・staff-chat", "text"),
                ("📋・logs", "text"),
                ("🔨・moderation", "text"),
            ],
        },
    },
    "tech": {
        "name": "💻 Tech & Programming",
        "roles": [
            ("👑 Tech Lead", discord.Colour.red(), True),
            ("🛡️ Admin", discord.Colour.orange(), True),
            ("⚔️ Moderator", discord.Colour.blue(), True),
            ("💎 Senior Dev", discord.Colour.purple(), True),
            ("💻 Developer", discord.Colour.gold(), False),
            ("🔧 Tech Enthusiast", discord.Colour.green(), False),
            ("🚀 Booster", discord.Colour.magenta(), False),
        ],
        "categories": {
            "💻 WELCOME": [
                ("👋・welcome", "text"),
                ("📜・rules", "text"),
                ("🎭・select-roles", "text"),
                ("📢・announcements", "text"),
                ("📖・resources", "text"),
            ],
            "💬 GENERAL": [
                ("💬・general-tech", "text"),
                ("🗣️・off-topic", "text"),
                ("💡・ideas-projects", "text"),
                ("🎯・career-advice", "text"),
                ("📰・tech-news", "text"),
            ],
            "👨‍💻 PROGRAMMING": [
                ("🐍・python", "text"),
                ("☕・javascript-typescript", "text"),
                ("⚙️・java-kotlin", "text"),
                ("🦀・rust-go", "text"),
                ("🔷・c-cpp", "text"),
                ("📱・mobile-dev", "text"),
                ("🌐・web-development", "text"),
                ("🎮・game-development", "text"),
            ],
            "🛠️ HELP & DEBUG": [
                ("❓・help-desk", "text"),
                ("🐛・debugging", "text"),
                ("📚・tutorials-guides", "text"),
                ("🔗・useful-links", "text"),
            ],
            "🚀 PROJECT SHOWCASE": [
                ("✨・show-your-projects", "text"),
                ("🤝・collaborations", "text"),
                ("💼・job-opportunities", "text"),
            ],
            "🎉 COMMUNITY": [
                ("🏆・coding-challenges", "text"),
                ("🎁・giveaways", "text"),
                ("😂・programmer-memes", "text"),
            ],
            "🤖 BOT ZONE": [
                ("🤖・bot-commands", "text"),
                ("💻・code-snippets", "text"),
            ],
            "🎫 SUPPORT": [
                ("🎫・support", "text"),
                ("💡・suggestions", "text"),
            ],
            "🔊 VOICE CODE": [
                ("💻・Code Together #1", "voice"),
                ("💻・Code Together #2", "voice"),
                ("💬・Tech Talk", "voice"),
                ("☕・Coffee Break", "voice"),
                ("😴・AFK", "voice"),
            ],
            "🛡️ STAFF": [
                ("💼・staff-chat", "text"),
                ("📋・logs", "text"),
                ("🔨・moderation", "text"),
            ],
        },
    },
    "roleplay": {
        "name": "🎭 Roleplay",
        "roles": [
            ("👑 Game Master", discord.Colour.red(), True),
            ("🛡️ Admin", discord.Colour.orange(), True),
            ("⚔️ Moderator", discord.Colour.blue(), True),
            ("🎭 Story Keeper", discord.Colour.purple(), True),
            ("⚔️ Veteran Roleplayer", discord.Colour.gold(), False),
            ("✨ Roleplayer", discord.Colour.green(), False),
            ("🚀 Booster", discord.Colour.magenta(), False),
        ],
        "categories": {
            "🌟 WELCOME": [
                ("👋・welcome-tavern", "text"),
                ("📜・rules-lore", "text"),
                ("📋・character-creation", "text"),
                ("📢・announcements", "text"),
                ("📖・how-to-roleplay", "text"),
            ],
            "💬 GENERAL": [
                ("💬・general-ooc", "text"),
                ("🗣️・casual-chat", "text"),
                ("💡・rp-ideas", "text"),
                ("🎨・character-art", "text"),
            ],
            "🎭 ROLEPLAY ZONES": [
                ("🏰・medieval-fantasy", "text"),
                ("🚀・sci-fi-space", "text"),
                ("🌆・modern-city", "text"),
                ("🧙・magic-academy", "text"),
                ("⚔️・adventure-quests", "text"),
                ("💕・romance-rp", "text"),
                ("😈・dark-rp", "text"),
                ("🎪・random-rp", "text"),
            ],
            "📚 CHARACTER PROFILES": [
                ("📝・character-sheets", "text"),
                ("🖼️・character-gallery", "text"),
                ("📖・backstories", "text"),
            ],
            "🎉 EVENTS": [
                ("🎪・rp-events", "text"),
                ("🏆・rp-contests", "text"),
                ("🎁・giveaways", "text"),
            ],
            "🤖 BOT ZONE": [
                ("🤖・bot-commands", "text"),
                ("🎲・dice-rolls", "text"),
            ],
            "🎫 SUPPORT": [
                ("🎫・support", "text"),
                ("🤝・rp-partnerships", "text"),
            ],
            "🔊 VOICE RP": [
                ("🎭・Voice RP #1", "voice"),
                ("🎭・Voice RP #2", "voice"),
                ("💬・OOC Lounge", "voice"),
                ("😴・AFK", "voice"),
            ],
            "🛡️ STAFF": [
                ("💼・staff-chat", "text"),
                ("📋・logs", "text"),
                ("🔨・moderation", "text"),
            ],
        },
    },
    "streaming": {
        "name": "📹 Streaming & Content",
        "roles": [
            ("👑 Platform Owner", discord.Colour.red(), True),
            ("🛡️ Admin", discord.Colour.orange(), True),
            ("⚔️ Moderator", discord.Colour.blue(), True),
            ("🎬 Content Manager", discord.Colour.purple(), True),
            ("⭐ Verified Streamer", discord.Colour.gold(), False),
            ("📹 Content Creator", discord.Colour.green(), False),
            ("🎥 Viewer", discord.Colour.default(), False),
            ("🚀 Booster", discord.Colour.magenta(), False),
        ],
        "categories": {
            "🌟 WELCOME": [
                ("👋・welcome-studio", "text"),
                ("📜・rules", "text"),
                ("🎭・roles", "text"),
                ("📢・announcements", "text"),
                ("📅・stream-schedule", "text"),
            ],
            "💬 COMMUNITY": [
                ("💬・general-chat", "text"),
                ("🗣️・off-topic", "text"),
                ("💡・content-ideas", "text"),
                ("🎯・goals-milestones", "text"),
            ],
            "📹 STREAMING": [
                ("🔴・live-now", "text"),
                ("📺・stream-highlights", "text"),
                ("🎥・vod-clips", "text"),
                ("📊・stream-stats", "text"),
                ("💡・stream-tips", "text"),
            ],
            "🎬 CONTENT CREATION": [
                ("🎞️・youtube-videos", "text"),
                ("📸・instagram-tiktok", "text"),
                ("🐦・twitter-updates", "text"),
                ("🎨・thumbnails-graphics", "text"),
                ("🎵・music-sounds", "text"),
            ],
            "🛠️ TECH & SETUP": [
                ("💻・tech-support", "text"),
                ("🎙️・audio-setup", "text"),
                ("📹・video-quality", "text"),
                ("🔧・troubleshooting", "text"),
            ],
            "🤝 COLLABORATION": [
                ("🤝・collab-requests", "text"),
                ("🎮・squad-up", "text"),
                ("💼・sponsorships", "text"),
            ],
            "🎉 EVENTS": [
                ("🎪・community-events", "text"),
                ("🏆・competitions", "text"),
                ("🎁・giveaways", "text"),
            ],
            "🤖 BOT ZONE": [
                ("🤖・bot-commands", "text"),
                ("🎵・music-player", "text"),
            ],
            "🎫 SUPPORT": [
                ("🎫・support-tickets", "text"),
                ("❓・help", "text"),
            ],
            "🔊 VOICE CHANNELS": [
                ("📹・Streaming Voice", "voice"),
                ("🎮・Gaming Party", "voice"),
                ("💬・Creator Lounge", "voice"),
                ("🎥・Watch Party", "voice"),
                ("😴・AFK", "voice"),
            ],
            "🛡️ STAFF": [
                ("💼・staff-chat", "text"),
                ("📋・logs", "text"),
                ("🔨・moderation", "text"),
            ],
        },
    },
}


def save_config(guild_id, template, welcome_channel_id=None, member_role_id=None):
    db.execute("""
    INSERT INTO guild_config(guild_id, template, welcome_channel_id, member_role_id)
    VALUES(?,?,?,?)
    ON CONFLICT(guild_id) DO UPDATE SET
        template=excluded.template,
        welcome_channel_id=excluded.welcome_channel_id,
        member_role_id=excluded.member_role_id
    """, (guild_id, template, welcome_channel_id, member_role_id))
    db.commit()


def get_config(guild_id):
    return db.execute(
        "SELECT template,welcome_channel_id,member_role_id FROM guild_config WHERE guild_id=?",
        (guild_id,)
    ).fetchone()


async def create_template(guild: discord.Guild, template_key: str):
    template = TEMPLATES[template_key]
    me = guild.me

    if not me.guild_permissions.manage_channels or not me.guild_permissions.manage_roles:
        raise RuntimeError("I need **Manage Channels** and **Manage Roles** permissions.")

    existing = {r.name for r in guild.roles}
    created_roles = {}

    # Create roles from lowest to highest.
    for role_name, colour, staff in reversed(template["roles"]):
        if role_name in existing:
            role = discord.utils.get(guild.roles, name=role_name)
        else:
            role = await guild.create_role(
                name=role_name,
                colour=colour,
                reason=f"Server Builder: {template['name']} template"
            )
        created_roles[role_name] = role

    created_channels = []
    for category_name, channels in template["categories"].items():
        category = discord.utils.get(guild.categories, name=category_name)
        if category is None:
            category = await guild.create_category(
                category_name,
                reason=f"Server Builder: {template['name']} template"
            )

        for channel_name, kind in channels:
            if kind == "text":
                channel = discord.utils.get(category.text_channels, name=channel_name)
                if channel is None:
                    channel = await guild.create_text_channel(
                        channel_name,
                        category=category,
                        reason="Server Builder"
                    )
            else:
                channel = discord.utils.get(category.voice_channels, name=channel_name)
                if channel is None:
                    channel = await guild.create_voice_channel(
                        channel_name,
                        category=category,
                        reason="Server Builder"
                    )
            created_channels.append(channel)

    # Find appropriate member role based on template
    member_role = (
        created_roles.get("⭐ Member") or
        created_roles.get("⭐ Player") or
        created_roles.get("⭐ Customer") or
        created_roles.get("🎥 Viewer") or
        created_roles.get("✏️ Student") or
        created_roles.get("🔧 Tech Enthusiast") or
        created_roles.get("🎧 Music Lover") or
        created_roles.get("🖌️ Artist") or
        created_roles.get("📚 Weeb") or
        created_roles.get("✨ Roleplayer") or
        created_roles.get("⭐ Gamer")
    )
    
    # Find welcome/announcement channel
    welcome = (
        discord.utils.get(guild.text_channels, name="📢・announcements") or
        discord.utils.get(guild.text_channels, name="👋・welcome")
    )

    save_config(
        guild.id,
        template_key,
        welcome.id if welcome else None,
        member_role.id if member_role else None
    )

    return len(created_roles), len(created_channels)


async def make_backup(guild: discord.Guild):
    data = {
        "guild": {"name": guild.name, "id": guild.id},
        "roles": [],
        "categories": [],
        "channels": []
    }

    for role in guild.roles:
        if role.is_default():
            continue
        data["roles"].append({
            "name": role.name,
            "colour": role.colour.value,
            "hoist": role.hoist,
            "mentionable": role.mentionable,
            "position": role.position
        })

    for category in guild.categories:
        data["categories"].append({
            "name": category.name,
            "position": category.position
        })

    for channel in guild.channels:
        if isinstance(channel, discord.CategoryChannel):
            continue
        data["channels"].append({
            "name": channel.name,
            "type": str(channel.type),
            "category": channel.category.name if channel.category else None,
            "position": channel.position,
            "topic": getattr(channel, "topic", None),
            "nsfw": getattr(channel, "nsfw", False)
        })

    path = BACKUP_DIR / f"{guild.id}.json"
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


async def restore_backup(guild: discord.Guild):
    path = BACKUP_DIR / f"{guild.id}.json"
    if not path.exists():
        return False, "No backup exists for this server."

    data = json.loads(path.read_text(encoding="utf-8"))
    existing_categories = {c.name: c for c in guild.categories}

    for item in sorted(data["categories"], key=lambda x: x["position"]):
        if item["name"] not in existing_categories:
            existing_categories[item["name"]] = await guild.create_category(
                item["name"], reason="Server Builder restore"
            )

    existing_text = {c.name for c in guild.text_channels}
    existing_voice = {c.name for c in guild.voice_channels}

    for item in sorted(data["channels"], key=lambda x: x["position"]):
        category = existing_categories.get(item["category"])
        if item["type"] == "text":
            if item["name"] not in existing_text:
                await guild.create_text_channel(
                    item["name"], category=category, topic=item.get("topic"),
                    nsfw=item.get("nsfw", False), reason="Server Builder restore"
                )
        elif item["type"] == "voice":
            if item["name"] not in existing_voice:
                await guild.create_voice_channel(
                    item["name"], category=category, reason="Server Builder restore"
                )

    return True, "Backup restored successfully!"


class TemplateSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Community", value="community", emoji="✨"),
            discord.SelectOption(label="Gaming", value="gaming", emoji="🎮"),
            discord.SelectOption(label="Minecraft", value="minecraft", emoji="⛏️"),
            discord.SelectOption(label="Social / Aesthetic", value="social", emoji="🌸"),
            discord.SelectOption(label="Shop / Business", value="shop", emoji="🛒"),
            discord.SelectOption(label="Anime & Manga", value="anime", emoji="🌸"),
            discord.SelectOption(label="Art & Creative", value="art", emoji="🎨"),
            discord.SelectOption(label="Music & Audio", value="music", emoji="🎵"),
            discord.SelectOption(label="Study & Learning", value="study", emoji="📚"),
            discord.SelectOption(label="Tech & Programming", value="tech", emoji="💻"),
            discord.SelectOption(label="Roleplay", value="roleplay", emoji="🎭"),
            discord.SelectOption(label="Streaming & Content", value="streaming", emoji="📹"),
        ]
        super().__init__(
            placeholder="✨ Choose your perfect server template...",
            options=options,
            custom_id="server_builder_template"
        )

    async def callback(self, interaction: discord.Interaction):
        if not interaction.guild:
            return await interaction.response.send_message(
                "❌ This can only be used in a server.", ephemeral=True
            )

        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send("⚙️ Building your server... This may take a moment! ✨", ephemeral=True)

        try:
            roles, channels = await create_template(interaction.guild, self.values[0])
            await interaction.edit_original_response(
                content=f"✅ **Server built successfully!** 🎉\n\n"
                        f"**Template:** {TEMPLATES[self.values[0]]['name']}\n"
                        f"**Roles created/used:** {roles} 👥\n"
                        f"**Channels created/used:** {channels} 📝\n\n"
                        f"Your server is ready to go! 🚀"
            )
        except discord.Forbidden:
            await interaction.edit_original_response(
                content="❌ I don't have enough permissions. Please give me **Manage Roles** and **Manage Channels** permissions! 🔒"
            )
        except Exception as e:
            await interaction.edit_original_response(
                content=f"❌ Builder error: `{e}`\n\nPlease contact support if this persists."
            )


class BuilderView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)
        self.add_item(TemplateSelect())


@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"✅ Logged in as {bot.user}")
        print(f"✅ Synced {len(synced)} slash commands")
        print(f"✅ Server Builder is ready! 🚀")
    except Exception as e:
        print(f"❌ Command sync error: {e}")


@bot.event
async def on_guild_join(guild):
    print(f"✅ Joined new server: {guild.name} ({guild.id})")


@bot.tree.command(name="setup", description="🛠️ Open the Discord server builder menu")
@app_commands.checks.has_permissions(manage_guild=True)
async def setup(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🛠️ Discord Server Builder",
        description=(
            "**Build a complete Discord server in seconds!** ✨\n\n"
            "Choose from 12 professional templates below:\n"
            "• Community, Gaming, Minecraft\n"
            "• Social, Shop, Anime\n"
            "• Art, Music, Study\n"
            "• Tech, Roleplay, Streaming\n\n"
            "I'll automatically create roles, categories, and channels for you! 🚀"
        ),
        colour=discord.Colour.blurple()
    )
    embed.set_footer(text="🌟 Server Builder • Made with ❤️ by NEXORA LAB")
    await interaction.response.send_message(embed=embed, view=BuilderView(), ephemeral=True)


@bot.tree.command(name="config", description="⚙️ Show the current server builder configuration")
@app_commands.checks.has_permissions(manage_guild=True)
async def config(interaction: discord.Interaction):
    row = get_config(interaction.guild.id)
    if not row:
        return await interaction.response.send_message(
            "⚠️ This server hasn't been configured yet. Use `/setup` to get started! ✨",
            ephemeral=True
        )

    template, welcome_id, role_id = row
    embed = discord.Embed(
        title="⚙️ Server Builder Configuration",
        description="Current settings for this server:",
        colour=discord.Colour.blurple()
    )
    embed.add_field(
        name="📋 Template",
        value=TEMPLATES.get(template, {}).get("name", template),
        inline=False
    )
    embed.add_field(
        name="👋 Welcome Channel",
        value=f"<#{welcome_id}>" if welcome_id else "❌ Not set",
        inline=True
    )
    embed.add_field(
        name="👥 Member Role",
        value=f"<@&{role_id}>" if role_id else "❌ Not set",
        inline=True
    )
    embed.set_footer(text="🌟 Server Builder Config")
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="backup", description="💾 Save this server's structure to a backup file")
@app_commands.checks.has_permissions(administrator=True)
async def backup(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    try:
        path = await make_backup(interaction.guild)
        await interaction.followup.send(
            f"✅ **Backup created successfully!** 💾\n\n"
            f"**Location:** `{path}`\n\n"
            f"Keep this file safe if you want to restore your server structure later! 🔒",
            ephemeral=True
        )
    except Exception as e:
        await interaction.followup.send(
            f"❌ Backup failed: `{e}`\n\nPlease try again or contact support.",
            ephemeral=True
        )


@bot.tree.command(name="restore", description="♻️ Restore the saved server structure from backup")
@app_commands.checks.has_permissions(administrator=True)
async def restore(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    try:
        ok, message = await restore_backup(interaction.guild)
        emoji = "✅" if ok else "❌"
        await interaction.followup.send(f"{emoji} {message}", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(
            f"❌ Restore failed: `{e}`\n\nPlease check if a backup file exists.",
            ephemeral=True
        )


@bot.tree.command(name="server-info", description="📊 Show detailed server information")
async def server_info(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(
        title=f"📊 {guild.name}",
        description="Server statistics and information",
        colour=discord.Colour.blurple()
    )
    embed.add_field(name="👥 Members", value=str(guild.member_count), inline=True)
    embed.add_field(name="🎭 Roles", value=str(len(guild.roles)), inline=True)
    embed.add_field(name="📝 Channels", value=str(len(guild.channels)), inline=True)
    embed.add_field(name="📁 Categories", value=str(len(guild.categories)), inline=True)
    embed.add_field(name="💬 Text Channels", value=str(len(guild.text_channels)), inline=True)
    embed.add_field(name="🔊 Voice Channels", value=str(len(guild.voice_channels)), inline=True)
    
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    
    embed.set_footer(text=f"Server ID: {guild.id}")
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="say", description="📢 Send a message as the bot")
@app_commands.describe(message="The message to send")
@app_commands.checks.has_permissions(manage_messages=True)
async def say(interaction: discord.Interaction, message: str):
    await interaction.response.send_message("✅ Message sent!", ephemeral=True)
    await interaction.channel.send(message)


@bot.tree.command(name="templates", description="📋 View all available server templates")
async def templates(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📋 Available Server Templates",
        description="Choose from these professionally designed templates:\n",
        colour=discord.Colour.blurple()
    )
    
    template_list = [
        "✨ **Community** - Perfect for general community servers",
        "🎮 **Gaming** - Optimized for gaming communities",
        "⛏️ **Minecraft** - Designed for Minecraft servers",
        "🌸 **Social / Aesthetic** - Chill and aesthetic vibes",
        "🛒 **Shop / Business** - E-commerce and business servers",
        "🌸 **Anime & Manga** - For anime and manga fans",
        "🎨 **Art & Creative** - Artists and creative communities",
        "🎵 **Music & Audio** - Music lovers and creators",
        "📚 **Study & Learning** - Educational communities",
        "💻 **Tech & Programming** - Developer communities",
        "🎭 **Roleplay** - Roleplay and storytelling servers",
        "📹 **Streaming & Content** - Content creators and streamers",
    ]
    
    embed.description += "\n".join(template_list)
    embed.set_footer(text="Use /setup to build your server! 🚀")
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.errors.MissingPermissions):
        msg = "❌ You don't have permission to use this command! 🔒"
    else:
        msg = f"❌ Error: `{error}`"
    
    if interaction.response.is_done():
        await interaction.followup.send(msg, ephemeral=True)
    else:
        await interaction.response.send_message(msg, ephemeral=True)


if not TOKEN:
    raise RuntimeError("❌ DISCORD_TOKEN is missing! Please add it to your .env file.")

print("🚀 Starting Discord Server Builder...")
bot.run(TOKEN)
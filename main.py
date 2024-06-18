from flask import Flask, render_template, url_for, redirect, request
import random
app = Flask(__name__)

wurm_unlimited = '366220'
rust = '252490'
ark = '346110'
zomboid = '108600'
daystodie = '251570'
csgo = '730'
factorio = '427520'
satisfactory = '526870'
valheim= '892970'
terraria = '105600'
server_name_bank = [
    "Avalon", "Titan", "Elysium", "Olympus", "Valhalla", "Haven", "Fortress", "Sanctuary", "Citadel", "Bastion",
    "Arcadia", "Eden", "Nirvana", "Utopia", "Shangri-La", "Asgard", "Atlantis", "Camelot", "Erebus", "El Dorado",
    "Frosthold", "Helios", "Hyperion", "Inferno", "Ironhold", "Leviathan", "Lumina", "Nebula", "Nexus", "Odyssey",
    "Orion", "Pandora", "Purgatory", "Ragnarok", "Solstice", "Starlight", "Terra", "Valiant", "Vanguard", "Vortex",
    "Zephyr", "Zenith", "Zion", "Aurora", "Blaze", "Celestial", "Chronos", "Cyclone", "Eclipse", "Equinox",
    "Evermore", "Genesis", "Horizon", "Mirage", "Nova", "Onyx", "Paragon", "Phoenix", "Radiance", "Serenity"
]
used_names = set()
server_list = []
for _ in range(20):
    while True:
        server_name = random.choice(server_name_bank)
        if server_name not in used_names:
            used_names.add(server_name)
            break
    server_status = random.choice(['online', 'offline','online'])
    player_count = random.randint(5, 100)
    game_id = random.choice([wurm_unlimited, rust, ark, zomboid, daystodie, csgo, factorio, satisfactory, valheim, terraria])

    server_list.append({
        'server_name': server_name.lower(),
        'server_status': server_status,
        'player_count': player_count,
        'game_id': game_id,
    })


@app.route('/')
def home():
    return render_template('home.html',)
    
@app.route('/servers')
def servers():
    return render_template('servers.html', server_list=server_list)

if __name__ == "__main__":
    app.run(debug=True, host='localhost',port=80)

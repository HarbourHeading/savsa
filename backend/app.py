"""Backend API server"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pymongo.mongo_client import MongoClient
from asyncio import gather
from aiohttp import ClientSession
import os

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://liamcodes.dev"}})

DATABASE_URI = f"mongodb://{os.getenv('DATABASE_ROOT_USERNAME')}:{os.getenv('DATABASE_ROOT_PASSWORD')}@database:27017/{os.getenv('DATABASE_NAME')}?authSource=admin"

client = MongoClient(DATABASE_URI)
database = client[os.getenv("DATABASE_NAME")]
profiles = database['profiles']  # Collection to store steamIDs

limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri=DATABASE_URI,
    strategy="fixed-window",
    default_limits=["1000 per day", "100 per hour"]
)


async def fetch(session, url):
    """Fetch data from given URL and return it as JSON"""
    async with session.get(url) as response:
        if response.status != 200 and response.content_type != 'application/json':  # Profile has private (inaccessible) recent games statistics
            return None

        return await response.json()


@app.route("/api/SteamProfileService/GetRandomProfile", methods=['GET'])
@limiter.limit("2 per second")
async def get_random_profile():
    """Return steam profile data in JSON format"""

    steamid = list(profiles.aggregate([{"$sample": {"size": 1}}]))[0]['steamid']  # Take 1 random steamid from database

    api_summary = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={os.getenv('STEAM_API_KEY')}&steamids={steamid}&format=json"
    api_recent_games = f"https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={os.getenv('STEAM_API_KEY')}&steamid={steamid}&format=json&count=3"
    api_badges = f"https://api.steampowered.com/IPlayerService/GetBadges/v1/?key={os.getenv('STEAM_API_KEY')}&steamid={steamid}"

    async with ClientSession() as session:
        player_summary, recently_played_games, player_badges = await gather(
            fetch(session, api_summary),
            fetch(session, api_recent_games),
            fetch(session, api_badges)
        )

    if player_summary.get('response', {}).get('players'):
        profile_data = player_summary['response']['players'][0]

        recently_played = recently_played_games.get('response', {}).get('games', [])
        profile_data['recently_played'] = recently_played

        player_level = player_badges.get('response', {}).get('player_level', None)
        profile_data['player_level'] = player_level

        return jsonify(profile_data)
    else:
        profiles.delete_one({"steamid": steamid})
        return await get_random_profile()


@app.route("/api/SteamProfileService/PostSteamID", methods=['POST'])
@limiter.limit("3 per minute")
async def post_steam_id():
    """Post user-submitted steamID or account name to database"""

    new_steamid = request.json

    api_summary = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={os.getenv('STEAM_API_KEY')}&format=json&steamids={new_steamid}"

    async with ClientSession() as session:
        async with session.get(api_summary) as response:
            if response.status != 200:  # Unsuccessful connection
                return jsonify({"error": "An error occurred. Please try again later."}), 500

            data = await response.json()

            if not data['response']['players']:  # Profile data is empty (profile does not exist, or it is private)
                return jsonify({"error": "Error occurred. Does the user not exist, or is their profile private?"}), 404

            if profiles.find_one(new_steamid):  # Supplied ID already exists in the database
                return jsonify({"error": "Profile has already been added."}), 400

            profiles.insert_one(new_steamid)  # Insert profile into database
            return jsonify({"message": "Your account has been added!"}), 200


if __name__ == "__main__":
    app.run(port=5000)

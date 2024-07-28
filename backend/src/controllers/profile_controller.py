"""API requests"""

from flask import jsonify, request
from asyncio import gather
from aiohttp import ClientSession

from ..db import *


class ProfileController:

    @staticmethod
    async def fetch(session, url):
        """Fetch data from given URL and return it as JSON"""

        async with session.get(url) as response:
            if response.status != 200 and response.content_type != 'application/json':  # Profile has private (inaccessible) recent games statistics
                return None

            return await response.json()

    @staticmethod
    async def get_random_profile():
        """Return steam profile data in JSON format"""

        steamid = list(database.profiles.aggregate([{"$sample": {"size": 1}}]))[0]['steamid']  # Take 1 random steamid from database

        api_summary = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={getenv('STEAM_API_KEY')}&steamids={steamid}&format=json"
        api_recent_games = f"https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={getenv('STEAM_API_KEY')}&steamid={steamid}&format=json&count=3"
        api_badges = f"https://api.steampowered.com/IPlayerService/GetBadges/v1/?key={getenv('STEAM_API_KEY')}&steamid={steamid}&format=json"

        async with ClientSession() as session:
            player_summary, recently_played_games, player_badges = await gather(
                ProfileController.fetch(session, api_summary),
                ProfileController.fetch(session, api_recent_games),
                ProfileController.fetch(session, api_badges)
            )

        if player_summary.get('response', {}).get('players'):
            profile_data = player_summary['response']['players'][0]

            recently_played = recently_played_games.get('response', {}).get('games', [])
            profile_data['recently_played'] = recently_played

            player_level = player_badges.get('response', {}).get('player_level', None)
            profile_data['player_level'] = player_level

            return jsonify(profile_data)
        else:
            database.profiles.delete_one({"steamid": steamid})
            return await ProfileController.get_random_profile()

    @staticmethod
    async def post_steam_id():
        """Post user-submitted steamID or account name to database"""

        new_steamid = request.json

        api_summary = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={getenv('STEAM_API_KEY')}&format=json&steamids={new_steamid}"

        async with ClientSession() as session:
            async with session.get(api_summary) as response:
                if response.status != 200:  # Unsuccessful connection
                    return jsonify({"error": "An error occurred. Please try again later."}), 500

                data = await response.json()

                if not data['response']['players']:  # Profile data is empty (profile does not exist, or it is private)
                    return jsonify(
                        {"error": "Error occurred. Does the user not exist, or is their profile private?"}), 404

                if database.profiles.find_one(new_steamid):  # Supplied ID already exists in the database
                    return jsonify({"error": "Profile has already been added."}), 400

                database.profiles.insert_one(new_steamid)  # Insert profile into database
                return jsonify({"message": "Your account has been added!"}), 200

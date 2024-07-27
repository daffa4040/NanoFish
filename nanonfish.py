#  JOIN TELEGRAM : https://t.me/apsstudiotech
#  JOIN DISCORD : https://discord.gg/N9caefVJ7F

import requests
import json
import urllib.parse
import time
import random
from collections import Counter
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Define the ASCII art banner
ascii_banner = """
 █████╗ ██████╗ ███████╗    ███████╗████████╗██╗   ██╗██████╗ ██╗ ██████╗ 
██╔══██╗██╔══██╗██╔════╝    ██╔════╝╚══██╔══╝██║   ██║██╔══██╗██║██╔═══██╗
███████║██████╔╝███████╗    ███████╗   ██║   ██║   ██║██║  ██║██║██║   ██║
██╔══██║██╔═══╝ ╚════██║    ╚════██║   ██║   ██║   ██║██║  ██║██║██║   ██║
██║  ██║██║     ███████║    ███████║   ██║   ╚██████╔╝██████╔╝██║╚██████╔╝
╚═╝  ╚═╝╚═╝     ╚══════╝    ╚══════╝   ╚═╝    ╚═════╝ ╚═════╝ ╚═╝ ╚═════╝ 
JOIN TELEGRAM : https://t.me/apsstudiotech
JOIN DISCORD  : https://discord.gg/N9caefVJ7F
"""

# Define available colors for colorama
colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]

# Function to print text with random color
def colored_print(text):
    color = random.choice(colors)
    print(color + text + Style.RESET_ALL)

# Print the banner with random color
colored_print(ascii_banner)

# Prompt the user for input at the beginning
buy_fish_enabled = None
while buy_fish_enabled not in ['y', 'n']:
    buy_fish_enabled = input("Do you want to enable buy fish actions? (y/n): ").strip().lower()
    if buy_fish_enabled not in ['y', 'n']:
        colored_print("Invalid input. Please enter 'y' or 'n'.")

buy_fish_enabled = (buy_fish_enabled == 'y')

# Define the URLs and headers for API requests
login_url = "https://fishapi.xboost.io/index/tglogin"
gamestate_url = "https://fishapi.xboost.io/zone/user/gamestate"
game_actions_url = "https://fishapi.xboost.io/zone/user/gameactions"
create_order_url = "https://fishapi.xboost.io/zone/order/createorder"
task_paction_url = "https://fishapi.xboost.io/zone/task/paction"

# Function to get login token
def get_login_token(init_data):
    try:
        login_payload = {
            "initData": init_data,
            "inviteCode": None,
            "source": None
        }
        login_headers = {
            "Accept": "*/*",
            "Content-Type": "application/json;charset=UTF-8",
            "Origin": "https://happy-aquarium.xboost.io",
            "Referer": "https://happy-aquarium.xboost.io/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
        }
        login_response = requests.post(login_url, headers=login_headers, json=login_payload)
        login_response.raise_for_status()
        login_response_json = login_response.json()
        if "data" in login_response_json:
            data = login_response_json["data"]
            return data.get("login_token")
        else:
            colored_print("Login Response does not contain 'data'.")
            return None
    except requests.RequestException as e:
        colored_print(f"Error during login request: {e}")
        return None

# Function to get game state
def get_game_state(login_token):
    try:
        gamestate_headers = {
            "Accept": "*/*",
            "Content-Type": "application/json;charset=UTF-8",
            "Authorization": login_token,
            "Origin": "https://happy-aquarium.xboost.io",
            "Referer": "https://happy-aquarium.xboost.io/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
        }
        gamestate_response = requests.post(gamestate_url, headers=gamestate_headers)
        gamestate_response.raise_for_status()
        gamestate_response_json = gamestate_response.json()
        if "data" in gamestate_response_json:
            data = gamestate_response_json["data"]
            gold = data.get("gold")
            return data.get("fishes"), gold
        else:
            colored_print("Game State Response does not contain 'data'.")
            return None, None
    except requests.RequestException as e:
        colored_print(f"Error during game state request: {e}")
        return None, None

# Function to perform game actions
def perform_game_actions(login_token, fishes):
    try:
        game_actions_headers = {
            "Accept": "*/*",
            "Content-Type": "application/json;charset=UTF-8",
            "Authorization": login_token,
            "Origin": "https://happy-aquarium.xboost.io",
            "Referer": "https://happy-aquarium.xboost.io/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
        }
        fish_counter = Counter(fishes)
        duplicate_fish_ids = [fish_id for fish_id, count in fish_counter.items() if count > 1]
        while duplicate_fish_ids:
            for fish_id in duplicate_fish_ids:
                game_actions_payload = {
                    "actions": [
                        {
                            "action": "compose",
                            "id": fish_id
                        }
                    ]
                }
                game_actions_response = requests.post(game_actions_url, headers=game_actions_headers, json=game_actions_payload)
                game_actions_response.raise_for_status()
            time.sleep(0.1)
            fishes, _ = get_game_state(login_token)
            if fishes is None:
                colored_print("Failed to get game state.")
                break
            fish_counter = Counter(fishes)
            duplicate_fish_ids = [fish_id for fish_id, count in fish_counter.items() if count > 1]
    except requests.RequestException as e:
        colored_print(f"Error during game actions request: {e}")

# Function to buy the highest fish
def buy_highest_fish(login_token):
    try:
        game_actions_headers = {
            "Accept": "*/*",
            "Content-Type": "application/json;charset=UTF-8",
            "Authorization": login_token,
            "Origin": "https://happy-aquarium.xboost.io",
            "Referer": "https://happy-aquarium.xboost.io/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
        }
        fishes, _ = get_game_state(login_token)
        if fishes is None:
            colored_print("Failed to get game state.")
            return
        max_fish_id = max(fishes, default=0)
        buy_id = max_fish_id - 4
        if buy_id <= 0:
            colored_print("No valid fish ID to buy.")
            return

        for attempt in range(10):
            buy_payload = {
                "actions": [
                    {
                        "action": "buy",
                        "id": buy_id
                    }
                ]
            }
            buy_response = requests.post(game_actions_url, headers=game_actions_headers, json=buy_payload)
            buy_response.raise_for_status()
            response_json = buy_response.json()
            results = response_json.get('data', {}).get('results', [])
            if results and results[0] == "balance not enough":
                colored_print("Balance not enough for buying more fish.")
                break
            time.sleep(0.1)
    except requests.RequestException as e:
        colored_print(f"Error during buy request: {e}")

# Function to recover fish
def recover_fish(login_token):
    try:
        game_actions_headers = {
            "Accept": "*/*",
            "Content-Type": "application/json;charset=UTF-8",
            "Authorization": login_token,
            "Origin": "https://happy-aquarium.xboost.io",
            "Referer": "https://happy-aquarium.xboost.io/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
        }
        fishes, _ = get_game_state(login_token)
        if fishes is None:
            colored_print("Failed to get game state.")
            return
        max_fish_id = max(fishes, default=0)
        recover_ids = [fish_id for fish_id in fishes if fish_id < (max_fish_id - 4)]

        for fish_id in recover_ids:
            recover_payload = {
                "actions": [
                    {
                        "action": "recover",
                        "id": fish_id
                    }
                ]
            }
            recover_response = requests.post(game_actions_url, headers=game_actions_headers, json=recover_payload)
            recover_response.raise_for_status()
            time.sleep(0.1)
    except requests.RequestException as e:
        colored_print(f"Error during recover request: {e}")

# Function to create order
def create_order(login_token):
    try:
        create_order_headers = {
            "Accept": "*/*",
            "Content-Type": "application/json;charset=UTF-8",
            "Authorization": login_token,
            "Origin": "https://happy-aquarium.xboost.io",
            "Referer": "https://happy-aquarium.xboost.io/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
        }
        create_order_payload = {"goods_id": 2}
        create_order_response = requests.post(create_order_url, headers=create_order_headers, json=create_order_payload)
        create_order_response.raise_for_status()
    except requests.RequestException as e:
        colored_print(f"Error during create order request: {e}")

# Function to perform task action
def perform_task_action(login_token):
    try:
        task_paction_headers = {
            "Accept": "*/*",
            "Content-Type": "application/json;charset=UTF-8",
            "Authorization": login_token,
            "Origin": "https://happy-aquarium.xboost.io",
            "Referer": "https://happy-aquarium.xboost.io/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
        }
        for task_id in [2, 3]:
            task_paction_payload = {"task_id": task_id}
            task_paction_response = requests.post(task_paction_url, headers=task_paction_headers, json=task_paction_payload)
            task_paction_response.raise_for_status()
    except requests.RequestException as e:
        colored_print(f"Error during task action request: {e}")

def extract_first_name(token):
    try:
        # Extract the 'user' parameter from the token
        query_params = urllib.parse.parse_qs(token)
        user_data = query_params.get('user', [None])[0]
        
        if user_data:
            # Decode and parse the 'user' parameter
            user_data = urllib.parse.unquote(user_data)
            user_info = json.loads(user_data)
            return user_info.get('first_name', 'Unknown')
        else:
            return 'Unknown'
    except Exception as e:
        print(f"Error extracting first name: {e}")
        return 'Unknown'

# Main loop
while True:
    with open("token.txt", "r") as file:
        init_data_list = file.read().splitlines()

    for init_data in init_data_list:
        parsed_init_data = urllib.parse.unquote(init_data.strip())
        login_token = get_login_token(parsed_init_data)
        
        # Extract and display the first name from the token
        first_name = extract_first_name(parsed_init_data)
        colored_print(f"Processing token for: {first_name}")

        if login_token:
            colored_print("Login successful.")
            
            # Create order and perform task action
            create_order(login_token)
            perform_task_action(login_token)

            # Get game state and perform actions
            fishes, gold = get_game_state(login_token)
            if fishes is not None:
                colored_print(f"Number of fishes: {len(fishes)}")
                colored_print(f"Gold: {gold}")
                perform_game_actions(login_token, fishes)
                if buy_fish_enabled and len(fishes) < 12:
                    buy_highest_fish(login_token)
                recover_fish(login_token)
        else:
            colored_print("Failed to get login token.")
    
    colored_print("Sleeping for 10 minutes...")
    print("")
    time.sleep(1)  # Sleep for 10 minutes before repeating

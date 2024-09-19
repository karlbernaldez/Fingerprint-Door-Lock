# Fingerprint Door Lock with Web Interface and MongoDB

This project implements a smart door lock system that uses fingerprint biometrics for authentication, integrated with a web interface for user management and MongoDB as the database. The Raspberry Pi controls the fingerprint sensor, relay, and solenoid door lock, enabling a secure and automated door lock solution. Users can register and authenticate using their fingerprints, and a log of login and logout activities is maintained.

## Features

- Fingerprint-based registration and login system
- Web interface for managing users
- MongoDB for storing user data and login logs
- Relay control for locking and unlocking the door using a solenoid lock
- Logs user activities (login, logout) including timestamps
- Secure password handling with hashed passwords
- REST API endpoints for user registration, login, and fingerprint enrollment
- Flexible user authentication methods: Fingerprint and Password-based login
- Session management with tokens for tracking active users

## System Architecture

- **Backend**: Flask-based web server running on a Raspberry Pi
- **Database**: MongoDB for user storage and login logs
- **Frontend**: A web interface for user interaction, running on Vercel (optional)
- **Hardware**: Raspberry Pi, R307 Fingerprint sensor, 12V Relay, Solenoid door lock, 12V power supply

## Hardware Requirements

- Raspberry Pi 4
- R307 Fingerprint Sensor
- 12V Solenoid Door Lock
- 5V Relay Module
- 12V Power Supply for the solenoid lock and relay
- Power adapter for Raspberry Pi (5V, 3A recommended)

## Software Requirements

- Python 3.x
- Flask
- MongoDB
- PyMongo
- Flask-Login for session management
- R307 Fingerprint sensor library (PyFingerprint)
- Vercel (for hosting the web frontend, optional)

## Connecting to Raspberry Pi via SSH

To set up your Raspberry Pi headless (without a monitor) and manage it via SSH, follow these steps:

1. **Download the SSH Keys**:
   - Download the public (`.pub`) and private key (`id_rsa`) files that are provided.
   
2. **Move Keys to `.ssh` Folder**:
   - Copy the keys to your local `.ssh` folder.
   - Use the following command to copy the keys to the `.ssh` folder:
     ```bash
     mv /path/to/downloaded/pubkey ~/.ssh/id_rsa.pub
     mv /path/to/downloaded/privkey ~/.ssh/id_rsa
     ```

3. **Set Proper Permissions for the Keys**:
   - Make sure the keys have the correct permissions:
     ```bash
     chmod 600 ~/.ssh/id_rsa
     ```

4. **Open VS Code**:
   - Install the **Remote - SSH** extension for VS Code.

5. **Add Host in VS Code**:
   - Hit `Ctrl+Shift+P` to open the Command Palette.
   - Type `Remote-SSH: Add New SSH Host...`.
   - Enter your SSH connection string: Change the Raspberry PI Ip with the current RPI IP
     ```
     ssh admin@<Raspberry-Pi-IP>
     ```
   - Save the host configuration to `~/.ssh/config`.

6. **Connect to the Host**:
   - Select the host from the SSH Targets list in VS Code and connect.
   - Enter the password when prompted.

7. **Start Working Remotely**:
   - Once connected, you can open a folder, edit code, and interact with the Raspberry Pi as if you were working on it locally.




## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/fingerprint-door-lock.git
   cd fingerprint-door-lock
   
2. **Set Up the Virtual Environment:**
   ```bash
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt

3. **Run the Application on Raspberry Pi:**
   ```bash
    python main.py

## Hardware Setup

To implement the fingerprint door lock system, you'll need to connect various components like the fingerprint sensor, relay, and solenoid door lock to the Raspberry Pi. Follow the wiring and connection guide below.

### Components Needed

- Raspberry Pi 4 (with power adapter, 5V 3A recommended)
- R307 Fingerprint Sensor
- 12V Solenoid Door Lock
- 12V Relay Module
- 12V Power Supply (for solenoid lock and relay)
- Jumper wires for connections
- Breadboard (optional, for testing connections)

### Connection Diagram

Below is an outline of how to connect the hardware components to the Raspberry Pi:


![Hardware Setup Diagram](https://storage.googleapis.com/adoveloper_dumps/Fingerprint%20Door%20Lock%20Wiring%20Diagram.png)



### Notes:

- Ensure that the relay module supports 12V switching to control the solenoid lock properly.
- Be cautious when working with a 12V power supply to avoid short circuits.
- Double-check the wiring and ensure proper insulation to prevent accidental shorting or damage.

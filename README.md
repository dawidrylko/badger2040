# 🦡 Badger 2040

[![Python Linting](https://github.com/dawidrylko/badger2040/actions/workflows/python-linting.yml/badge.svg)](https://github.com/dawidrylko/badger2040/actions/workflows/python-linting.yml)

> A programmable badge with fast updating E Ink® display and wireless connectivity, powered by Raspberry Pi Pico W.

## 📖 Overview

This repository provides several example projects that demonstrate the capabilities of the Badger 2040. These examples are intended to help users explore the potential of the Badger 2040 and implement their own projects with ease. The projects cover a range of functionalities, from basic operations to advanced applications involving WiFi and action handling.

## 🧩 Key Components

The examples in this repository are organized into different categories based on their functionality. Each category contains a set of examples that demonstrate a specific feature or use case of the Badger 2040.

### ⚙️ GitHub Actions Workflows

The Actions examples demonstrate how to display GitHub Actions workflows directly on the Badger 2040. This includes processing button presses to navigate through different workflows, viewing their statuses, and updating the E Ink display with the relevant information.

<img
    src="https://github.com/dawidrylko/badger2040/assets/11761319/65b4375b-1720-4c5e-956f-1ba6a4a488e1"
    alt="Badger2040 - GitHub Actions Workflows App - dawidrylko/badger2040"
    width="45%"
/>
<img
    src="https://github.com/dawidrylko/badger2040/assets/11761319/679f0d0d-9609-4fcc-8bae-14d54bc4af0e"
    alt="Badger2040 - GitHub Actions Workflows App - dawidrylko/dawidrylko.com"
    width="45%"
/>

```plaintext
badger_os/
├── examples/
│   ├── actions.py
│   └── icon-actions.png
└── GITHUB_CONFIG.py
```

- `actions.py`: Demonstrates how to define and handle various user actions, such as button presses, to trigger different functionalities and update the display accordingly.
- `icon-actions.png`: Icon representing actions within the system.
- `GITHUB_CONFIG.py`: Configuration file for GitHub Actions, useful for setting up automation or CI/CD processes related to the project.

### ✨ Configuration Restoration

The configuration restoration feature allows you to easily restore WiFi and GitHub settings to your Badger 2040. This is particularly useful for quickly switching between different network environments or resetting configurations to a known state, such as using the Badger at home or at work.

<img
    src="https://github.com/dawidrylko/badger2040/assets/11761319/c8c763db-4d9c-4454-a904-78409a8bb55b"
    alt="Badger2040 - Configuration Restoration App"
    width="45%"
/>
<img
    src="https://github.com/dawidrylko/badger2040/assets/11761319/25172bee-275e-4438-9bfb-f632e8bf2ffd"
    alt="Badger2040 - Configuration Restoration App"
    width="45%"
/>

```plaintext
badger_os/
├── examples/
│   ├── restore.py
│   └── icon-restore.png
└── defaults/
    ├── WIFI_HOME.py
    ├── WIFI_WORK.py
    ├── WIFI_HOTSPOT.py
    ├── GITHUB_HOME.py
    └── GITHUB_WORK.py
```

- `restore.py`: Main script to handle restoration of WiFi and GitHub configurations by pressing a button on the Badger 2040.
- `WIFI_HOME.py`, `WIFI_WORK.py`, `WIFI_HOTSPOT.py`: Default WiFi configuration files for different environments.
- `GITHUB_HOME.py`, `GITHUB_WORK.py`: Default GitHub configuration files for different environments.

Simply press the appropriate button on the Badger 2040 to restore the corresponding configuration.

### 🌐 Wireless Connectivity

The WiFi examples demonstrate how to utilize the Badger 2040's wireless capabilities. You can learn how to connect to a WiFi network, perform network operations, and interact with web content. This includes changing network configurations by setting up an access point for network configuration.

<img
    src="https://github.com/dawidrylko/badger2040/assets/11761319/0e8569a1-63d6-4ac2-b611-49a54cfef813"
    alt="Badger2040 - Wireless Connectivity - Access Point"
    width="45%"
/>
<img
    src="https://github.com/dawidrylko/badger2040/assets/11761319/583b0290-1c13-402f-81c6-210fb85e1d97"
    alt="Badger2040 - Wireless Connectivity - Connection"
    width="45%"
/>

<img
    src="https://github.com/dawidrylko/badger2040/assets/11761319/ef4aad72-e547-4537-90a5-ddda6fdd46df"
    alt="Badger2040 - Wireless Connectivity - WiFi Setup"
    width="30%"
/>
<img
    src="https://github.com/dawidrylko/badger2040/assets/11761319/39810618-dfea-415f-a76b-0f9092b5f21e"
    alt="Badger2040 - Wireless Connectivity - WiFi Setup"
    width="30%"
/>
<img
    src="https://github.com/dawidrylko/badger2040/assets/11761319/0ed97b57-a1c9-4831-95e6-ea248f959f33"
    alt="Badger2040 - Wireless Connectivity - WiFi Setup Successful"
    width="30%"
/>

<img
    src="https://github.com/dawidrylko/badger2040/assets/11761319/08c27dc0-8535-4e8a-b1a0-5e36a25744d9"
    alt="Badger2040 - Wireless Connectivity - Configured"
    width="45%"
/>

```plaintext
badger_os/
├── examples/
│   ├── wifi.py
│   └── icon-wifi.png
└── pages/
    ├── wifi-setup-successful.html
    └── wifi-setup.html
```

- `wifi.py`: Script to connect the Badger 2040 to a WiFi network and perform basic network operations like fetching data from the web.
- `wifi-setup.html`: HTML page for setting up the WiFi connection via a web interface.
- `wifi-setup-successful.html`: HTML page displayed upon a successful WiFi connection setup.

## 📋 Requirements

To use the examples in this repository, you will need the following:

- [Badger 2040](https://shop.pimoroni.com/products/badger-2040-w)
- [Thonny IDE](https://thonny.org/)

Ensure you have the latest firmware and software updates for optimal performance.

## 🚀 Getting Started

Follow these steps to get started with the Badger 2040 examples:

1. Clone the repository:

   ```sh
   git clone https://github.com/dawidrylko/badger2040.git
   ```

2. Open the example project you want to use in Thonny IDE.
3. Connect your Badger 2040 to your computer using a USB cable.
4. Copy the code to the appropriate place in the Thonny IDE.
5. Run the code to see the examples in action on your Badger 2040.

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## 👨‍💻 Author

This library was created by [Dawid Ryłko](https://dawidrylko.com).

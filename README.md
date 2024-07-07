# 🦡 Badger 2040

> A programmable badge with fast updating E Ink® display and wireless connectivity, powered by Raspberry Pi Pico W.

## 📖 Overview

This repository provides several example projects that demonstrate the capabilities of the Badger 2040. These examples are intended to help users explore the potential of the Badger 2040 and implement their own projects with ease. The projects cover a range of functionalities, from basic operations to advanced applications involving WiFi and action handling.

## 🧩 Key Components

The examples in this repository are organized into different categories based on their functionality. Each category contains a set of examples that demonstrate a specific feature or use case of the Badger 2040.

### ✨ Configuration Restoration

Easily restore WiFi and GitHub configurations with the new configuration restoration feature:

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

- `config_restore.py`: Main script to handle restoration of WiFi and GitHub configurations.
- `WIFI_HOME.py`, `WIFI_WORK.py`, `WIFI_HOTSPOT.py`: Default WiFi configuration files.
- `GITHUB_HOME.py`, `GITHUB_WORK.py`: Default GitHub configuration files.

Simply press the appropriate button on the Badger 2040 to restore the corresponding configuration.

### 🌐 WiFi

Explore the wireless connectivity capabilities of the Badger 2040 with the following examples:

```plaintext
badger_os/
├── examples/
│   ├── icon-wifi.png
│   └── wifi.py
└── pages/
    ├── wifi-setup-successful.html
    └── wifi-setup.html
```

- `wifi.py`: Demonstrates how to connect the Badger 2040 to a WiFi network and perform basic network operations.
- `wifi-setup.html`: HTML page for setting up the WiFi connection.
- `wifi-setup-successful.html`: HTML page displayed upon successful WiFi connection.

### ⚙️ Actions

Learn how to handle different actions on the Badger 2040 with these examples:

```plaintext
badger_os/
├── examples/
│   ├── actions.py
│   └── icon-actions.png
└── GITHUB_CONFIG.py
```

- `actions.py`: Shows how to define and handle various user actions, such as button presses and screen updates.
- `icon-actions.png`: Icon representing actions within the system.
- `GITHUB_CONFIG.py`: Configuration file for GitHub Actions, if any automation or CI/CD processes are set up.

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

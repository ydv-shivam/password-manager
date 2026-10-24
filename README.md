# 🔒 Secure Python Password Manager

A comprehensive, lightweight command-line password manager built in Python. It features secure master password authentication, symmetric encryption (`cryptography.fernet`) for your stored credentials, and built-in tools for generating and managing strong passwords locally.

---

## ✨ Features

* **Master Password Protection:** Secures access to your vault using SHA-256 hashing.
* **Strong Encryption:** Uses Fernet (AES-128) encryption to ensure your stored passwords remain unreadable on your disk.
* **Interactive CLI Menu:** Easily add, view, list, or delete stored credentials through an intuitive terminal interface.
* **Built-in Password Generator:** Automatically generate strong, randomized passwords with custom lengths containing letters, numbers, and symbols.
* **Local Storage:** Keeps your encrypted data safe locally without relying on third-party cloud servers.

---

## 🚀 Getting Started

### Prerequisites

Make sure you have **Python 3.x** installed on your machine.

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/ydv-shivam/password-manager.git](https://github.com/ydv-shivam/password-manager.git)
   cd password-manager

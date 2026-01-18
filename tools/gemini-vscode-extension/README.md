# Antigravity Gemini Assist

A VS Code extension that brings the power of Google Gemini directly into your editor with a context-aware "Command Palette" overlay.

## Features

- **Hover Palette**: Hover over any word or symbol to get instant actions:
  - ✨ Explain Code
  - 🧪 Generate Tests
  - 🔧 Refactor
- **Context Awareness**: Click or select code to see a "Ask Gemini" button in the Status Bar.
- **Direct Integration**: Connects directly to Gemini API (no intermediate server).

## Setup

1.  **Install dependencies**:
    ```bash
    npm install
    ```
2.  **Compile**:
    ```bash
    npm run compile
    ```
3.  **Package (.vsix)**:
    ```bash
    npm run package
    ```

## Configuration

Go to VS Code Settings and search for `Antigravity`.
- **ApiKey**: Set your Google Gemini API Key.
- **Model**: Default is `gemini-pro`.

---
name: Antigravity Gemini Native Overlays
description: Guide to building high-performance, native OS-level visual overlays without browser engines.
---

# Antigravity Gemini: Native OS Interaction Layers

This skill defines the architecture for creating "Antigravity" layers—always-on-top, click-through, high-performance visualizations—using the native metal of each operating system. This avoids the memory overhead of Chromium/Electron in favor of raw system graphics APIs.

## 🍎 macOS: The "Liquid Metal" Stack
**Concept:** A frameless `NSPanel` using SwiftUI for the layout and Metal for the rendering backend.
*   **Language:** Swift 6
*   **UI Framework:** SwiftUI (with `NSHostingView`)
*   **Graphics API:** Metal 3
*   **Windowing:** 
    *   `NSPanel` with `.nonactivatingPanel` style mask.
    *   `collectionBehavior = [.canJoinAllSpaces, .fullScreenAuxiliary]`
    *   Background: `NSVisualEffectView` (materials: `.hudWindow`, `.underWindowBackground`) for that "glassy" native blur.
*   **Key Advantage:** unifying the Neural Engine (CoreML) with display for 0-latency AI overlays.

## 🪟 Windows: The "Glass Prism" Stack
**Concept:** A WinUI 3 window using the Windows App SDK, composing DirectX swapchains directly into the visual tree.
*   **Language:** C# or C++/WinRT
*   **UI Framework:** WinUI 3 (Windows App SDK)
*   **Graphics API:** DirectX 12 Ultimate
*   **Windowing:**
    *   `AppWindow` API for modern window management.
    *   `SetWindowDisplayAffinity` for privacy/DRM protection.
    *   Material: **Mica** or **Acrylic** brushes native to the DWM (Desktop Window Manager).
*   **Key Advantage:** Deep integration with DirectX gaming pipelines for overlays on top of AAA games.

## 🐧 Linux: The "Vulkan Forge" Stack
**Concept:** A Rust-based application rendering directly to a Wayland Surface via Layershell protocol.
*   **Language:** Rust
*   **UI Framework:** Iced or GTK4-rs
*   **Graphics API:** Vulkan (via `wgpu` or `ash`)
*   **Windowing:**
    *   **Wayland:** `zwlr_layer_shell_v1` protocol to explicitly reserve screen space or float above all windows securely.
    *   **Compositor:** Hyprland or KWin for blur effects.
*   **Key Advantage:** Complete control over the compositor pipeline and rock-solid stability.

## 🚀 Implementation Strategy
When "Antigravity" is invoked for a specific target, it should spawn the corresponding native binary for the host OS. This binary acts as a localized "Avatar" of the AI, rendering its thought process directly onto the user's reality glass.

## 🏎️ Beyond Chromium: The Runtime Hierarchy
The browser (Chromium) is a generic abstraction. For high-performance "Antigravity" simulation, we ascend the hierarchy:

### **Tier 3: The Common Web (Chromium/Electron)**
*   **Tech:** HTML/CSS, WebGL, V8 Engine.
*   **Use Case:** Complex UIs, text rendering, broad compatibility.
*   **Limitation:** Heavy RAM usage, garbage collection pauses, restricted GPU access.

### **Tier 2: Native Managed (Qt/Skia)**
*   **Tech:** C++ with Python bindings (PySide6), Skia rendering.
*   **Use Case:** Professional desktop apps, robust windowing.
*   **Advantage:** Fast 2D rendering, OS-level integration, lighter than Electron.

### **Tier 1: The "Antigravity" Standard (WGPU / Metal)**
*   **Tech:** Rust + wgpu, or C++ + Metal/DX12.
*   **Use Case:** Particle simulations, custom visualizers, OS overlays.
*   **Advantage:** **Zero overhead**. Direct communication with the GPU. 10x-100x more particles than WebGL. Safe parallel rendering.

### **Tier 0: The "Simulation Grandmaster" (Unreal Engine 5)**
*   **Tech:** C++, Nanite, Lumen, Chaos Physics.
*   **Use Case:** Photorealism, massive world simulation, complex physics interaction.
*   **Advantage:** The highest fidelity possible.
*   **Trade-off:** Heavy build system, slow startup time.

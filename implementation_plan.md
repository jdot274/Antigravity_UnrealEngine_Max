# Implementation Plan - Antigravity Nexus Launch & Polish

This plan outlines the final steps to stabilize the Antigravity Nexus environment, ensuring a smooth launch, robust Python interop, and a high-fidelity "Full Game" experience.

## User Review Required

> [!IMPORTANT]
> **Shader Compilation**: The initial launch may show a black screen while shaders compile. This is normal for a fresh build.
> **Storage Warning**: The logs indicate "Insufficient Storage" for the Derived Data Cache. This might slow down load times but shouldn't prevent launch.

## Proposed Changes

### 1. Python Environment Stabilization
- [x] **Fix Path Issues**: Copy `level_generator.py` and `gemini_ultra_brain.py` to `Content/Python/utils/` to resolve `ImportError`.
- [x] **Debug Logging**: Add Python version logging to `init_unreal.py` to verify the environment.

### 2. Launch Script Robustness
- [x] **Absolute Paths**: Update `launch_full_game.sh` to use hardcoded absolute paths for the Project and UE5 Editor to prevent "Project Browser" launch issues.
- [x] **Signaling Server**: Ensure `npm install` runs if dependencies are missing and use explicit local IP.

### 3. "Full Game" Experience Polish
- [ ] **Welcome Text**: Spawn valid 3D Text in `nexus_game_manager.py` to confirm the game loop is active visually.
- [ ] **Verification**: Confirm Pixel Streaming connects and renders the scene (Golf Course, Player).

## Verification Plan

### Automated Checks
- **Log Review**: Check `NexusGlobal.log` and Unreal Output Log for `✅ Game Loop Initialized` and no `ImportError`.
- **Process Check**: Ensure `UnrealEditor` (Game Mode), `node` (Signaling Server), and `Next.js` (if applicable) are running.

### Manual Verification
1. Run `./AntigravityNexus.command`.
2. Select Option [1].
3. Wait for Shaders to compile (Black screen resolve).
4. Verify "ANTIGRAVITY NEXUS" text is visible.
5. Control the Player Ball.

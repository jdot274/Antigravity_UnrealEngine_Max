# Fix NexusRuntime Module Structure & Launch

## Context
The project successfully passed the compilation phase, but failed at runtime with "The game module 'NexusRuntime' could not be successfully initialized".
Investigation revealed that the `Source/NexusRuntime` directory contains a nested `NexusRuntime` folder (i.e., `Source/NexusRuntime/NexusRuntime/NexusRuntime.Build.cs`), which is incorrect. This likely occurred during the backup restoration process.

## Goal
Fix the directory structure, verify module dependencies, and ensure a clean build and successful launch.

## Actions

### 1. Fix Directory Structure
- [ ] Move all contents from `Source/NexusRuntime/NexusRuntime/` up to `Source/NexusRuntime/`.
- [ ] Remove the now-empty nested `NexusRuntime` directory.
- [ ] Verify `NexusRuntime.Build.cs` is at `Source/NexusRuntime/NexusRuntime.Build.cs`.

### 2. Dependency Verification
- [ ] Check `NexusRuntime.Build.cs` to ensure it includes `NexusRuntime` (self), `Engine`, `Core`, `CoreUObject`, and other required modules.
- [ ] Ensure `Public` and `Private` folders are correctly populated.

### 3. Clean Build Environment
- [ ] Remove `Binaries` and `Intermediate` folders to prevent stale linkage.
- [ ] Re-generate project files (via `build_project.sh` which typically handles this, or manual UBT command if needed).

### 4. Build & Launch
- [ ] Run `./build_project.sh`.
- [ ] Validated success output.
- [ ] Run `./launch_client_local.sh`.
- [ ] Confirm "SYSTEM ONLINE" text in the game world.

## User Actions Required
- Approve the directory structure fix.
- Run the build script when ready.

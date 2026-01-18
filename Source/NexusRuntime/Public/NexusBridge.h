#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "NexusBridge.generated.h"

class UObject;
class UWorld;

UCLASS()
class NEXUSRUNTIME_API UNexusBridge : public UBlueprintFunctionLibrary {
  GENERATED_BODY()

public:
  // Core Runtime Command Router
  UFUNCTION(BlueprintCallable, Category = "Nexus|Core")
  static FString ExecuteRuntimeCpp(FString Command, FString Payload);

  // Golf Course Spawning
  UFUNCTION(BlueprintCallable, Category = "Nexus|Spawning",
            meta = (WorldContext = "WorldContextObject"))
  static void SpawnGolfCourse(const UObject *WorldContextObject);

  // Complete Course (internal use)
  static void SpawnCompleteGolfCourse(UWorld *World);

  // Player Ball Spawning
  UFUNCTION(BlueprintCallable, Category = "Nexus|Spawning",
            meta = (WorldContext = "WorldContextObject"))
  static void SpawnPlayer(const UObject *WorldContextObject);

  // Asset Gallery
  static void SpawnAssetGallery(UWorld *World);

  // Dynamic Lighting
  static void SpawnLighting(UWorld *World);

  // HUD / UI Elements
  static void SpawnHUD(UWorld *World);

  // 3D Mechanisms
  UFUNCTION(BlueprintCallable, Category = "Nexus|UI")
  static void SpawnContentDrawer(UWorld *World);

  // === AI TERMINAL ===
  // Spawns the physical 3D interface
  static void SpawnAIConsole(UWorld *World);

  // Updates the 3D text display
  UFUNCTION(BlueprintCallable, Category = "Nexus|AI")
  static void UpdateChatLog(FString NewLog);

  // === GAME COMMANDS (Callable from Python) ===

  // Add stroke to current hole
  UFUNCTION(BlueprintCallable, Category = "Nexus|Game")
  static FString AddStroke(); // Implemented in CPP to avoid inline complexity

  // Complete current hole
  UFUNCTION(BlueprintCallable, Category = "Nexus|Game")
  static FString CompleteHole();

  // Get current score
  UFUNCTION(BlueprintCallable, Category = "Nexus|Game")
  static FString GetScore();

  // Reset game
  UFUNCTION(BlueprintCallable, Category = "Nexus|Game")
  static FString ResetGame();

  // === MATERIAL FACTORY TESTING ===

  // Test the Nanite material factory
  UFUNCTION(BlueprintCallable, Category = "Nexus|Materials")
  static FString TestMaterialFactory();

  // Spawn a procedural actor at runtime
  UFUNCTION(BlueprintCallable, Category = "Nexus|Spawning",
            meta = (WorldContext = "WorldContextObject"))
  static void SpawnProceduralActor(const UObject *WorldContextObject,
                                   FString ActorName);
};

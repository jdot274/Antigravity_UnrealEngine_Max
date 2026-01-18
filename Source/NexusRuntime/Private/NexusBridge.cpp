#include "NexusBridge.h"
#include "NexusContentDrawer.h"

// ... (existing includes)

// (At the end of file)
void UNexusBridge::SpawnContentDrawer(UWorld *World) {
  if (!World)
    return;

  // Try to find player location
  FVector SpawnLoc(100.0f, 0.0f, 100.0f);
  FRotator SpawnRot(0.0f);

  APlayerController *PC = World->GetFirstPlayerController();
  if (PC && PC->GetPawn()) {
    FVector PlayerLoc = PC->GetPawn()->GetActorLocation();
    FVector PlayerFwd = PC->GetPawn()->GetActorForwardVector();
    SpawnLoc = PlayerLoc + (PlayerFwd * 150.0f) + FVector(0, 0, 50);
    SpawnRot = PC->GetPawn()->GetActorRotation();
    // Face the player
    SpawnRot.Yaw += 180.0f;
  }

  FActorSpawnParameters Params;
  Params.SpawnCollisionHandlingOverride =
      ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

  ANexusContentDrawer *Drawer = World->SpawnActor<ANexusContentDrawer>(
      ANexusContentDrawer::StaticClass(), SpawnLoc, SpawnRot, Params);

  if (Drawer) {
    UE_LOG(LogTemp, Warning, TEXT("Spawned 3D Content Drawer!"));
    // Auto open for effect
    Drawer->SetDrawerOpen(true);
  }
}

// Core Includes
#include "Kismet/GameplayStatics.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "Modules/ModuleManager.h"
#include "Serialization/JsonReader.h"
#include "Serialization/JsonSerializer.h"

// Engine Includes
#include "Camera/CameraActor.h"
#include "Components/DirectionalLightComponent.h"
#include "Components/LightComponent.h"
#include "Components/PointLightComponent.h"
#include "Components/SkyAtmosphereComponent.h"
#include "Components/SkyLightComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Components/TextRenderComponent.h"
#include "Engine/DirectionalLight.h"
#include "Engine/PointLight.h"
// #include "Engine/SkyAtmosphere.h"
#include "Engine/SkyLight.h"
#include "Engine/StaticMesh.h"
#include "Engine/StaticMeshActor.h"
// #include "Engine/TextRenderActor.h"
#include "Engine/World.h"
#include "GameFramework/Actor.h"
#include "GameFramework/PlayerController.h"

// Project Includes
#include "NexusGameMode.h"
#include "NexusGeneratedArchetypes.h"
// #include "NexusGeneratedRegistry.h"
#include "NexusPawn.h"

// Static Game State
// static ATextRenderActor *GlobalChatLog = nullptr;
static TMap<FString, int32> Scores;
static TArray<FString> ChatHistory;
static int32 Strokes = 0;

FString UNexusBridge::ExecuteRuntimeCpp(FString Command, FString Payload) {
  if (Command == "PING")
    return TEXT("PONG");
  if (Command == "INIT_SYSTEM")
    return TEXT("BrainLink Established");

  if (Command == "ADD_STROKE") {
    Strokes++;
    return FString::Printf(TEXT("Stroke: %d"), Strokes);
  }

  if (Command == "HOLE_COMPLETE") {
    return TEXT("Hole Completed!");
  }

  if (Command == "GET_SCORE") {
    return FString::Printf(TEXT("Strokes: %d"), Strokes);
  }

  if (Command == "RESET_GAME") {
    Strokes = 0;
    return TEXT("Game Reset");
  }

  // Default response
  return FString::Printf(TEXT("Unknown Command: %s"), *Command);
}

void UNexusBridge::SpawnGolfCourse(const UObject *WorldContextObject) {
  UWorld *World = WorldContextObject->GetWorld();
  if (World) {
    SpawnCompleteGolfCourse(World);
  }
}

void UNexusBridge::SpawnPlayer(const UObject *WorldContextObject) {
  UWorld *World = WorldContextObject->GetWorld();
  if (!World)
    return;

  FActorSpawnParameters SpawnParams;
  SpawnParams.SpawnCollisionHandlingOverride =
      ESpawnActorCollisionHandlingMethod::AdjustIfPossibleButAlwaysSpawn;

  FVector Location(0.0f, 0.0f, 200.0f);
  FRotator Rotation(0.0f, 0.0f, 0.0f);

  World->SpawnActor<ANexusPawn>(ANexusPawn::StaticClass(), Location, Rotation,
                                SpawnParams);
}

void UNexusBridge::SpawnCompleteGolfCourse(UWorld *World) {
  if (!World)
    return;
  UE_LOG(LogTemp, Warning, TEXT("Spawning Golf Course..."));
  // Implementation placeholder
}

void UNexusBridge::SpawnAssetGallery(UWorld *World) {
  // Implementation placeholder
}

void UNexusBridge::SpawnLighting(UWorld *World) {
  // Implementation placeholder
}

#include "NexusInGameHUD.h"

void UNexusBridge::SpawnHUD(UWorld *World) {
  if (!World)
    return;

  APlayerController *PC = World->GetFirstPlayerController();
  if (PC) {
    // Create the widget (Base class for now, user can swap with BP subclass)
    UNexusInGameHUD *HUD =
        CreateWidget<UNexusInGameHUD>(PC, UNexusInGameHUD::StaticClass());
    if (HUD) {
      HUD->AddToViewport(9999); // Z-order high
      HUD->ShowNotification("ANTIGRAVITY", "Welcome to the Nexus");
      UE_LOG(LogTemp, Warning, TEXT("✅ HUD Spawned"));
    }
  }
}

void UNexusBridge::SpawnAIConsole(UWorld *World) {
  if (!World)
    return;
  UE_LOG(LogTemp, Warning, TEXT("SYSTEM ONLINE"));
  // TODO: Restore ATextRenderActor once engine header is fixed
}

void UNexusBridge::UpdateChatLog(FString NewLog) {
  ChatHistory.Add(NewLog);
  UE_LOG(LogTemp, Warning, TEXT("ChatLog: %s"), *NewLog);
  // TODO: Restore ATextRenderActor once engine header is fixed
}

FString UNexusBridge::AddStroke() {
  return ExecuteRuntimeCpp("ADD_STROKE", "");
}

FString UNexusBridge::CompleteHole() {
  return ExecuteRuntimeCpp("HOLE_COMPLETE", "");
}

FString UNexusBridge::GetScore() { return ExecuteRuntimeCpp("GET_SCORE", ""); }

FString UNexusBridge::ResetGame() {
  return ExecuteRuntimeCpp("RESET_GAME", "");
}

FString UNexusBridge::TestMaterialFactory() {
#if WITH_EDITOR
  FNexusMaterialStyle Style;
  Style.BaseColor = FLinearColor(0.8f, 0.2f, 0.1f, 1.0f); // Red-orange
  Style.Roughness = 0.3f;
  Style.DisplacementIntensity = 50.0f;
  Style.bIsSpiky = true;

  FString MaterialName =
      FString::Printf(TEXT("TestMaterial_%d"), FMath::RandRange(1000, 9999));
  UMaterial *NewMaterial =
      UNexusMaterialFactory::CreateNaniteMaterial(MaterialName, Style);

  if (NewMaterial) {
    FString Path =
        FString::Printf(TEXT("/Game/Nexus/Generated/%s"), *MaterialName);
    UE_LOG(LogTemp, Warning, TEXT("✅ Material created: %s"), *Path);
    return FString::Printf(TEXT("SUCCESS: %s"), *Path);
  } else {
    UE_LOG(LogTemp, Error, TEXT("❌ Material creation failed"));
    return TEXT("FAILED: Material creation failed");
  }
#else
  UE_LOG(LogTemp, Warning,
         TEXT("TestMaterialFactory is only available in Editor builds."));
  return TEXT("FAILED: Editor-only function");
#endif
}

void UNexusBridge::SpawnProceduralActor(const UObject *WorldContextObject,
                                        FString ActorName) {
  UWorld *World = WorldContextObject->GetWorld();
  if (!World)
    return;

  FActorSpawnParameters SpawnParams;
  SpawnParams.SpawnCollisionHandlingOverride =
      ESpawnActorCollisionHandlingMethod::AdjustIfPossibleButAlwaysSpawn;

  FVector Location(FMath::RandRange(-500.0f, 500.0f),
                   FMath::RandRange(-500.0f, 500.0f), 200.0f);
  FRotator Rotation(0.0f, FMath::RandRange(0.0f, 360.0f), 0.0f);

  ANexusPhysicsActor *NewActor = World->SpawnActor<ANexusPhysicsActor>(
      ANexusPhysicsActor::StaticClass(), Location, Rotation, SpawnParams);

  if (NewActor) {
    UE_LOG(LogTemp, Warning,
           TEXT("✅ Spawned Procedural Actor: %s at (%f, %f, %f)"), *ActorName,
           Location.X, Location.Y, Location.Z);
  }
}

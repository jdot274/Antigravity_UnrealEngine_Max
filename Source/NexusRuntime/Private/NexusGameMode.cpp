#include "NexusGameMode.h"
#include "Engine/World.h"
#include "NexusBridge.h"
#include "NexusButton.h"
#include "NexusGolfGenerator.h"

void ANexusGameMode::StartPlay() {
  Super::StartPlay();

  UE_LOG(LogTemp, Warning,
         TEXT("[NEXUS] GameMode StartPlay: Spawning World Content..."));

  UWorld *World = GetWorld();
  if (World) {
    // 1. Spawn PROCEDURAL Golf Generator
    World->SpawnActor<ANexusGolfGenerator>(FVector::ZeroVector,
                                           FRotator::ZeroRotator);

    // 2. Spawn Interactive Buttons
    FVector ButtonLoc(100, 100, 150);
    ANexusButton *Btn =
        World->SpawnActor<ANexusButton>(ButtonLoc, FRotator::ZeroRotator);
    if (Btn) {
      Btn->ButtonLabel = "RESET WORLD";
    }

    // Spawn another
    ANexusButton *Btn2 = World->SpawnActor<ANexusButton>(
        ButtonLoc + FVector(0, 100, 0), FRotator::ZeroRotator);
    if (Btn2) {
      Btn2->ButtonLabel = "SPAWN AI";
      Btn2->BaseColor = FLinearColor::Red;
    }

    // Spawn SIMULATE button
    ANexusButton *Btn3 = World->SpawnActor<ANexusButton>(
        ButtonLoc + FVector(0, 200, 0), FRotator::ZeroRotator);
    if (Btn3) {
      Btn3->ButtonLabel = "RUN SIMULATION";
      Btn3->BaseColor = FLinearColor::Green;
    }

    // 3. Keep other utilities
    UNexusBridge::SpawnPlayer(World);
    UNexusBridge::SpawnLighting(World);
    UNexusBridge::SpawnHUD(World);
    UNexusBridge::SpawnAIConsole(World);
  }
}

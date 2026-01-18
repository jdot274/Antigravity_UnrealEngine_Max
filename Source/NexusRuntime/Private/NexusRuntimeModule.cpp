#include "NexusRuntimeModule.h"
#include "HAL/IConsoleManager.h"
#include "NexusBridge.h"

#define LOCTEXT_NAMESPACE "FNexusRuntimeModule"

void FNexusRuntimeModule::StartupModule() {
  UE_LOG(LogTemp, Warning,
         TEXT("🚀 NexusRuntime C++ Module Loaded. Connectivity to Gemini C++ "
              "Client Ready."));

  // Register Console Commands
  IConsoleManager::Get().RegisterConsoleCommand(
      TEXT("nexus.ping"), TEXT("Ping the Nexus Bridge"),
      FConsoleCommandDelegate::CreateLambda([]() {
        FString Result = UNexusBridge::ExecuteRuntimeCpp("PING", "");
        UE_LOG(LogTemp, Log, TEXT("Nexus Ping Result: %s"), *Result);
      }),
      ECVF_Default);

  IConsoleManager::Get().RegisterConsoleCommand(
      TEXT("nexus.reset"), TEXT("Reset the Game"),
      FConsoleCommandDelegate::CreateLambda([]() {
        FString Result = UNexusBridge::ResetGame();
        UE_LOG(LogTemp, Log, TEXT("Nexus Reset Result: %s"), *Result);
      }),
      ECVF_Default);

  IConsoleManager::Get().RegisterConsoleCommand(
      TEXT("nexus.score"), TEXT("Get Current Score"),
      FConsoleCommandDelegate::CreateLambda([]() {
        FString Result = UNexusBridge::GetScore();
        UE_LOG(LogTemp, Log, TEXT("Nexus Score: %s"), *Result);
      }),
      ECVF_Default);

  IConsoleManager::Get().RegisterConsoleCommand(
      TEXT("nexus.testmaterial"), TEXT("Test the material factory"),
      FConsoleCommandDelegate::CreateLambda([]() {
        FString Result = UNexusBridge::TestMaterialFactory();
        UE_LOG(LogTemp, Log, TEXT("Nexus TestMaterial: %s"), *Result);
      }),
      ECVF_Default);

  IConsoleManager::Get().RegisterConsoleCommand(
      TEXT("nexus.spawn"), TEXT("Spawn a procedural actor"),
      FConsoleCommandWithArgsDelegate::CreateLambda(
          [](const TArray<FString> &Args) {
            FString ActorName = Args.Num() > 0 ? Args[0] : TEXT("TestActor");
            if (GWorld) {
              UNexusBridge::SpawnProceduralActor(GWorld, ActorName);
              UE_LOG(LogTemp, Log, TEXT("Nexus Spawn: %s"), *ActorName);
            } else {
              UE_LOG(LogTemp, Warning,
                     TEXT("Nexus Spawn: No world context available"));
            }
          }),
      ECVF_Default);
}

void FNexusRuntimeModule::ShutdownModule() {
  // Unregister commands if necessary, though commonly handled by module manager
  // on shutdown
}

#undef LOCTEXT_NAMESPACE

IMPLEMENT_MODULE(FNexusRuntimeModule, NexusRuntime)

#include "NexusRuntimeModule.h"

#define LOCTEXT_NAMESPACE "FNexusRuntimeModule"

void FNexusRuntimeModule::StartupModule() {
  UE_LOG(LogTemp, Warning,
         TEXT("🚀 NexusRuntime C++ Module Loaded. Connectivity to Gemini C++ "
              "Client Ready."));
}

void FNexusRuntimeModule::ShutdownModule() {}

#undef LOCTEXT_NAMESPACE

IMPLEMENT_MODULE(FNexusRuntimeModule, NexusRuntime)

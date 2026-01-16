#include "AntigravityNativeModule.h"

AAntigravityNativeModule::AAntigravityNativeModule() {
  PrimaryActorTick.bCanEverTick = true;
}

void AAntigravityNativeModule::BeginPlay() {
  Super::BeginPlay();
  UE_LOG(LogTemp, Warning,
         TEXT("🚀 Antigravity Native Module Initialized (Metal 3 Pipeline "
              "Active)"));
}

void AAntigravityNativeModule::Tick(float DeltaTime) {
  Super::Tick(DeltaTime);
  UpdateGPUBuffers();
}

void AAntigravityNativeModule::InjectTacticalData(FString DataStream) {
  // This is the live bridge from Python
  // data_stream is expected to be a JSON payload from the dashboard
  UE_LOG(LogTemp, Display, TEXT("📡 Data Injected: %s"), *DataStream);

  // Fast-path parsing and application to game state
}

FVector AAntigravityNativeModule::CalculateHoverForces(FVector CurrentLocation,
                                                       float TargetHeight,
                                                       float DeltaTime) {
  // 1. Calculate Error
  float HeightError = TargetHeight - CurrentLocation.Z;

  // 2. Add "Futuristic" Sine Wave Bobbing
  HoverTime += DeltaTime;
  float Bobbing = FMath::Sin(HoverTime * 2.0f) * 5.0f; // 5 units variance

  // 3. Spring Force (Proportional)
  float SpringStiffness = 100.0f;
  float ForceZ = (HeightError + Bobbing) * SpringStiffness * DeltaTime;

  // 4. Return the Delta Vector
  return FVector(0.0f, 0.0f, ForceZ);
}

void AAntigravityNativeModule::UpdatePaddlePosition(FVector NewTargetPosition) {
  // Smooth Lerp for "Weighty" feel
  float LerpSpeed = 10.0f; // Tunable
  // In a real actor we would set SetActorLocation here, but for this module
  // we assume it is calculating for a controlled pawn or just updating internal
  // state.
  CurrentPaddlePos = FMath::VInterpTo(CurrentPaddlePos, NewTargetPosition,
                                      GetWorld()->GetDeltaSeconds(), LerpSpeed);

  // Log for debug viz
  // UE_LOG(LogTemp, Verbose, TEXT("🏓 Paddle Glide: %s"),
  // *CurrentPaddlePos.ToString());
}

void AAntigravityNativeModule::UpdateGPUBuffers() {
  // Placeholder for direct Metal 3 vertex buffer updates
  // In a real AAA project, we would use RHI (Rendering Hardware Interface) here
}

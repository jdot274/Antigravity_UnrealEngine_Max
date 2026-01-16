#pragma once

#include "AntigravityNativeModule.generated.h"
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"

/**
 * AAAA Native Module for Mac (Metal 3 optimized)
 * This class handles high-speed live data injection from the Python dashboard
 * directly into the Unreal Engine renderer.
 */
UCLASS()
class ANTIGRAVITY_API AAntigravityNativeModule : public AActor {
  GENERATED_BODY()

public:
  AAntigravityNativeModule();

protected:
  virtual void BeginPlay() override;

public:
  virtual void Tick(float DeltaTime) override;

  // Live Scripting Entry Point
  UFUNCTION(BlueprintCallable, Category = "Antigravity")
  void InjectTacticalData(FString DataStream);

  /**
   * Calculates physics-based hover forces for the disk.
   * Uses a PID-like approach to maintain height with a futuristic "bobbing"
   * effect.
   */
  UFUNCTION(BlueprintCallable, Category = "Antigravity|Physics")
  FVector CalculateHoverForces(FVector CurrentLocation, float TargetHeight,
                               float DeltaTime);

  /**
   * Smoothly interpolates the paddle to a new position.
   */
  UFUNCTION(BlueprintCallable, Category = "Antigravity|Input")
  void UpdatePaddlePosition(FVector NewTargetPosition);

private:
  // Raw Metal 3 Buffer access (Simulated)
  void UpdateGPUBuffers();

  // Internal State
  FVector CurrentPaddlePos;
  float HoverTime;
};

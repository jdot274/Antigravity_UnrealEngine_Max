#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Pawn.h"
#include "NexusPawn.generated.h"

class UCameraComponent;
class USpringArmComponent;

UCLASS()
class NEXUSRUNTIME_API ANexusPawn : public APawn {
  GENERATED_BODY()

public:
  ANexusPawn();

protected:
  virtual void BeginPlay() override;

public:
  virtual void Tick(float DeltaTime) override;
  virtual void SetupPlayerInputComponent(
      class UInputComponent *PlayerInputComponent) override;

  // Components
  UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera")
  TObjectPtr<USpringArmComponent> SpringArmComp;

  UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera")
  TObjectPtr<UCameraComponent> CameraComp;

  // Pixel Streaming & Interaction
  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nexus|Streaming")
  bool bEnableDepthTracking;

  UFUNCTION(BlueprintCallable, Category = "Nexus|Interaction")
  void HighlightObjectUnderCursor();

private:
  void MoveForward(float Value);
  void MoveRight(float Value);
};

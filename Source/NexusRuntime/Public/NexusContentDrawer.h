#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "NexusContentDrawer.generated.h"

UCLASS()
class NEXUSRUNTIME_API ANexusContentDrawer : public AActor {
  GENERATED_BODY()

public:
  ANexusContentDrawer();

  virtual void Tick(float DeltaTime) override;

  // Toggle the drawer open/closed state
  UFUNCTION(BlueprintCallable, Category = "Nexus|Drawer")
  void ToggleDrawer();

  // Set the target state directly that we want to interp to
  UFUNCTION(BlueprintCallable, Category = "Nexus|Drawer")
  void SetDrawerOpen(bool bOpen);

protected:
  virtual void BeginPlay() override;

private:
  // Root component
  UPROPERTY(VisibleAnywhere)
  USceneComponent *RootScene;

  // The main casing/housing of the drawer system
  UPROPERTY(VisibleAnywhere)
  UStaticMeshComponent *CasingMesh;

  // The sliding part that holds content
  UPROPERTY(VisibleAnywhere)
  UStaticMeshComponent *SlidingTrayMesh;

  // State
  bool bTargetOpenState;
  float CurrentOpenAlpha; // 0.0 to 1.0

  // Animations settings
  UPROPERTY(EditAnywhere, Category = "Drawer Config")
  float OpenSpeed;

  UPROPERTY(EditAnywhere, Category = "Drawer Config")
  FVector OpenOffset; // Relative offset when fully open

  FVector ClosedPosition;
  FVector OpenPosition;
};

#pragma once

#include "Components/StaticMeshComponent.h"
#include "Components/TextRenderComponent.h"
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "NexusButton.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnNexusButtonClicked,
                                            ANexusButton *, Button);

UCLASS()
class NEXUSRUNTIME_API ANexusButton : public AActor {
  GENERATED_BODY()

public:
  ANexusButton();

protected:
  virtual void BeginPlay() override;
  virtual void Tick(float DeltaTime) override;
  virtual void
  NotifyActorOnClicked(FKey ButtonPressed = EKeys::LeftMouseButton) override;

public:
  // Visuals
  UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Nexus|UI")
  UStaticMeshComponent *SphereMesh;

  UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Nexus|UI")
  UTextRenderComponent *LabelText;

  // Config
  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nexus|UI")
  FString ButtonLabel = "NEXUS ACTION";

  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nexus|UI")
  FLinearColor BaseColor = FLinearColor(0.0f, 0.8f, 1.0f, 1.0f); // Cyan

  // Event
  UPROPERTY(BlueprintAssignable, Category = "Nexus|UI")
  FOnNexusButtonClicked OnNexusActivated;

private:
  class UMaterialInstanceDynamic *DynamicMat;
  float TimeAccumulator;
  bool bIsHovered;
};

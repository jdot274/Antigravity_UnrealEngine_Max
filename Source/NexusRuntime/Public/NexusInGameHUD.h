#pragma once

#include "Blueprint/UserWidget.h"
#include "CoreMinimal.h"
#include "NexusInGameHUD.generated.h"

UCLASS()
class NEXUSRUNTIME_API UNexusInGameHUD : public UUserWidget {
  GENERATED_BODY()

public:
  virtual void NativeConstruct() override;

  UFUNCTION(BlueprintCallable, Category = "Nexus|UI")
  void ShowNotification(FString Title, FString Message);

  UPROPERTY(EditAnywhere, BlueprintReadWrite, meta = (BindWidgetOptional))
  class UNexusCurveWidget *CurveEditor;

  UPROPERTY(EditAnywhere, BlueprintReadWrite, meta = (BindWidgetOptional))
  class UTextBlock *NotificationText;
};

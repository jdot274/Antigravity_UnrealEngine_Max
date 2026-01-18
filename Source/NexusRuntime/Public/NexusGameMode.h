#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "NexusGameMode.generated.h"

/**
 *
 */
UCLASS()
class NEXUSRUNTIME_API ANexusGameMode : public AGameModeBase {
  GENERATED_BODY()

public:
  virtual void StartPlay() override;
};

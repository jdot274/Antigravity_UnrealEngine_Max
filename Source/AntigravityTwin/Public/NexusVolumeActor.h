#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "NexusVolumeActor.generated.h"

UCLASS()
class ANTIGRAVITYTWIN_API ANexusVolumeActor : public AActor
{
	GENERATED_BODY()
	
public:	
	ANexusVolumeActor();

protected:
	virtual void BeginPlay() override;

public:	
	virtual void Tick(float DeltaTime) override;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nexus | Volumetrics")
	int32 SphereCount = 500;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nexus | Volumetrics")
	float BlurIntensity = 0.5f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nexus | Volumetrics")
	FLinearColor GlassColor = FLinearColor(0.2f, 0.5f, 1.0f, 0.3f);

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nexus | Volumetrics")
	FVector VolumeExtents = FVector(1000.0f, 1000.0f, 500.0f);

	UFUNCTION(BlueprintCallable, Category = "Nexus | Logic")
	void UpdateVolumeData(float Time);
};

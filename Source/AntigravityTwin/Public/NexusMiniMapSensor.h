#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Components/SceneCaptureComponent2D.h"
#include "NexusMiniMapSensor.generated.h"

/**
 * High-precision 4K sensor for capturing tactical map data from the environment.
 * Optimized for Metal/Vulkan compute pipelines.
 */
UCLASS()
class ANTIGRAVITYTWIN_API ANexusMiniMapSensor : public AActor
{
	GENERATED_BODY()
	
public:	
	// Sets default values for this actor's properties
	ANexusMiniMapSensor();

protected:
	// Called when the game starts or when spawned
	virtual void BeginPlay() override;

public:	
	// Called every frame
	virtual void Tick(float DeltaTime) override;

    // The main capture component
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Nexus Sensor")
    USceneCaptureComponent2D* MiniMapCapture;

    // Texture target for the 4K stream
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nexus Sensor")
    class UTextureRenderTarget2D* RenderTarget;

    // Activate the sensor stream
    UFUNCTION(BlueprintCallable, Category = "Nexus Sensor")
    void ActivateSensorStream(int32 ResolutionX = 3840, int32 ResolutionY = 2160);

    // Apply the schematic filter
    UFUNCTION(BlueprintCallable, Category = "Nexus Sensor")
    void ApplySchematicFilter();

private:
    void SetupRenderTarget(int32 ResX, int32 ResY);
};

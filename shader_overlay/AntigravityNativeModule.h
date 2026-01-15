#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "AntigravityNativeModule.generated.h"

/**
 * AAAA Native Module for Mac (Metal 3 optimized)
 * This class handles high-speed live data injection from the Python dashboard
 * directly into the Unreal Engine renderer.
 */
UCLASS()
class ANTIGRAVITY_API AAntigravityNativeModule : public AActor
{
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

private:
	// Raw Metal 3 Buffer access (Simulated)
	void UpdateGPUBuffers();
};

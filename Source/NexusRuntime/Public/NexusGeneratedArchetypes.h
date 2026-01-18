#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Materials/Material.h"
#include "Materials/MaterialInstanceConstant.h"
#include "NexusGeneratedArchetypes.generated.h"

/**
 * Base class for AI-generated Physics Actors
 */
UCLASS()
class NEXUSRUNTIME_API ANexusPhysicsActor : public AActor {
  GENERATED_BODY()

public:
  ANexusPhysicsActor();

  UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Nexus|Physics")
  class UStaticMeshComponent *MeshComponent;

  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nexus|Properties")
  float Density;

  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nexus|Properties")
  bool bUseNaniteDisplacement;

protected:
  virtual void BeginPlay() override;
};

/**
 * Data structure for AI-procedural material parameters
 */
USTRUCT(BlueprintType)
struct FNexusMaterialStyle {
  GENERATED_BODY()

  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nexus|Style")
  FLinearColor BaseColor;

  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nexus|Style")
  float Roughness;

  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nexus|Style")
  float DisplacementIntensity;

  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nexus|Style")
  bool bIsSpiky; // For spikes (grass/nanite) vs curvy (SDF)
};

/**
 * Singleton-like factory for building materials in C++
 */
UCLASS()
class NEXUSRUNTIME_API UNexusMaterialFactory : public UObject {
  GENERATED_BODY()

public:
  // Builds a material with advanced displacement logic in C++
  static UMaterial *CreateNaniteMaterial(const FString &Name,
                                         const FNexusMaterialStyle &Style);

  // Builds transmission-level material blueprints
  static UMaterial *CreateTransmissionMaterial(const FString &Name,
                                               float Transparency);
};

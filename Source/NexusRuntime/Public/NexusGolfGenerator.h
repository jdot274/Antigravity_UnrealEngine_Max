#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"

class UProceduralMeshComponent;
class UHierarchicalInstancedStaticMeshComponent;

#include "NexusGolfGenerator.generated.h"

UCLASS()
class NEXUSRUNTIME_API ANexusGolfGenerator : public AActor {
  GENERATED_BODY()

public:
  ANexusGolfGenerator();

protected:
  virtual void BeginPlay() override;
  virtual void OnConstruction(const FTransform &Transform) override;

  void GenerateTerrain();
  void PopulateInstancedAssets();

public:
  // Components
  UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Nexus|Golf")
  UProceduralMeshComponent *ProceduralMesh;

  UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Nexus|Golf")
  UHierarchicalInstancedStaticMeshComponent *TreeInstances;

  UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Nexus|Golf")
  UHierarchicalInstancedStaticMeshComponent *FlagInstances;

  // Config
  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nexus|Golf")
  FVector2D GridSize = FVector2D(5000.0f, 5000.0f);

  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nexus|Golf")
  int32 GridResolution = 64;

  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nexus|Golf")
  float HIllFactor = 200.0f;

  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nexus|Golf")
  float RippleFactor = 50.0f;

  // Assets to Load
  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nexus|Assets")
  UStaticMesh *TreeMeshAsset;

  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nexus|Assets")
  UStaticMesh *FlagMeshAsset;

  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Nexus|Assets")
  UMaterialInterface *GroundMaterial;

private:
  float GetHeightAt(float X, float Y);
};

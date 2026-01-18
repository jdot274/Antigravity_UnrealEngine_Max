#include "NexusGolfGenerator.h"
#include "Components/HierarchicalInstancedStaticMeshComponent.h"
#include "KismetProceduralMeshLibrary.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "ProceduralMeshComponent.h"
#include "UObject/ConstructorHelpers.h"

ANexusGolfGenerator::ANexusGolfGenerator() {
  PrimaryActorTick.bCanEverTick = false;

  ProceduralMesh =
      CreateDefaultSubobject<UProceduralMeshComponent>(TEXT("ProceduralMesh"));
  RootComponent = ProceduralMesh;
  ProceduralMesh->bUseAsyncCooking = true;

  TreeInstances =
      CreateDefaultSubobject<UHierarchicalInstancedStaticMeshComponent>(
          TEXT("TreeInstances"));
  TreeInstances->SetupAttachment(RootComponent);

  FlagInstances =
      CreateDefaultSubobject<UHierarchicalInstancedStaticMeshComponent>(
          TEXT("FlagInstances"));
  FlagInstances->SetupAttachment(RootComponent);

  // Load defaults if not set
  static ConstructorHelpers::FObjectFinder<UStaticMesh> DefaultTreeMesh(
      TEXT("/Engine/BasicShapes/Cylinder.Cylinder"));
  if (DefaultTreeMesh.Succeeded()) {
    TreeInstances->SetStaticMesh(DefaultTreeMesh.Object);
    TreeMeshAsset = DefaultTreeMesh.Object;
  }

  static ConstructorHelpers::FObjectFinder<UStaticMesh> DefaultFlagMesh(
      TEXT("/Engine/BasicShapes/Cone.Cone"));
  if (DefaultFlagMesh.Succeeded()) {
    FlagInstances->SetStaticMesh(DefaultFlagMesh.Object);
    FlagMeshAsset = DefaultFlagMesh.Object;
  }

  static ConstructorHelpers::FObjectFinder<UMaterialInterface> DefaultMat(
      TEXT("/Engine/BasicShapes/BasicShapeMaterial.BasicShapeMaterial"));
  if (DefaultMat.Succeeded()) {
    GroundMaterial = DefaultMat.Object;
  }
}

void ANexusGolfGenerator::BeginPlay() {
  Super::BeginPlay();
  GenerateTerrain();
  PopulateInstancedAssets();
}

void ANexusGolfGenerator::OnConstruction(const FTransform &Transform) {
  Super::OnConstruction(Transform);
  // Optional: Preview in Editor
  // GenerateTerrain();
}

float ANexusGolfGenerator::GetHeightAt(float X, float Y) {
  // Combine low freq hill and high freq ripple
  float Z1 = FMath::Sin(X * 0.002f) * FMath::Cos(Y * 0.002f) * HIllFactor;
  float Z2 = FMath::Sin(X * 0.005f + Y * 0.004f) * RippleFactor;
  return Z1 + Z2;
}

void ANexusGolfGenerator::GenerateTerrain() {
  if (!ProceduralMesh)
    return;

  ProceduralMesh->ClearAllMeshSections();

  TArray<FVector> Vertices;
  TArray<int32> Triangles;
  TArray<FVector> Normals;
  TArray<FVector2D> UVs;
  TArray<FProcMeshTangent> Tangents;
  TArray<FLinearColor> VertexColors;

  float DX = GridSize.X / GridResolution;
  float DY = GridSize.Y / GridResolution;

  // Generate Vertices
  for (int32 Y = 0; Y <= GridResolution; Y++) {
    for (int32 X = 0; X <= GridResolution; X++) {
      float PX = X * DX - (GridSize.X * 0.5f);
      float PY = Y * DY - (GridSize.Y * 0.5f);
      float PZ = GetHeightAt(PX, PY);

      Vertices.Add(FVector(PX, PY, PZ));
      UVs.Add(FVector2D(float(X) / GridResolution, float(Y) / GridResolution));

      // Color Logic (Green = Height, Red = "Sand" Noise)
      float NormZ = (PZ + HIllFactor) / (HIllFactor * 2.0f);
      float Noise =
          FMath::Frac(FMath::Sin(PX * 0.1f) * 43758.5453f); // Simple hash
      float Red = (Noise > 0.9f) ? 1.0f : 0.0f;             // Sand patch

      VertexColors.Add(FLinearColor(Red, NormZ, 0.0f, 1.0f));
    }
  }

  // Generate Triangles
  for (int32 Y = 0; Y < GridResolution; Y++) {
    for (int32 X = 0; X < GridResolution; X++) {
      int32 i0 = Y * (GridResolution + 1) + X;
      int32 i1 = i0 + 1;
      int32 i2 = i0 + (GridResolution + 1);
      int32 i3 = i2 + 1;

      // Tri 1
      Triangles.Add(i0);
      Triangles.Add(i2);
      Triangles.Add(i1);

      // Tri 2
      Triangles.Add(i2);
      Triangles.Add(i3);
      Triangles.Add(i1);
    }
  }

  // Calculate Normals/Tangents auto?
  // We can use UKismetProceduralMeshLibrary::CalculateTangentsForMesh but it
  // needs separate arrays. For now, let's just make them UP or basic. Ideally
  // use library.
  UKismetProceduralMeshLibrary::CalculateTangentsForMesh(
      Vertices, Triangles, UVs, Normals, Tangents);

  ProceduralMesh->CreateMeshSection_LinearColor(
      0, Vertices, Triangles, Normals, UVs, VertexColors, Tangents, true);

  // Material
  if (GroundMaterial) {
    UMaterialInstanceDynamic *DynMat =
        UMaterialInstanceDynamic::Create(GroundMaterial, this);
    if (DynMat) {
      DynMat->SetVectorParameterValue(
          "Color", FLinearColor(0.1, 0.6, 0.1, 1.0)); // Default Green
      ProceduralMesh->SetMaterial(0, DynMat);
    }
  }
}

void ANexusGolfGenerator::PopulateInstancedAssets() {
  if (!TreeInstances || !FlagInstances)
    return;

  TreeInstances->ClearInstances();
  FlagInstances->ClearInstances();

  // Set Meshes if configured
  if (TreeMeshAsset)
    TreeInstances->SetStaticMesh(TreeMeshAsset);
  if (FlagMeshAsset)
    FlagInstances->SetStaticMesh(FlagMeshAsset);

  // Random placement based on logic
  int32 NumItems = 50;

  // Seed
  FRandomStream Stream(12345);

  for (int32 i = 0; i < NumItems; i++) {
    float PX = Stream.FRandRange(-GridSize.X * 0.45f, GridSize.X * 0.45f);
    float PY = Stream.FRandRange(-GridSize.Y * 0.45f, GridSize.Y * 0.45f);
    float PZ = GetHeightAt(PX, PY);

    bool bIsFlag = Stream.FRand() > 0.8f;

    FTransform T(FRotator(0, Stream.FRandRange(0, 360), 0),
                 FVector(PX, PY, PZ));

    if (bIsFlag) {
      // Place Flag in 'Valleys' preferrably? Or just random for now.
      T.SetScale3D(FVector(1, 1, 3)); // Tall
      FlagInstances->AddInstance(T);
    } else {
      // Trees
      T.SetScale3D(FVector(1, 1, 1) * Stream.FRandRange(0.8f, 1.5f));
      TreeInstances->AddInstance(T);
    }
  }
}

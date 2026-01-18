#include "NexusGeneratedArchetypes.h"
#include "Components/StaticMeshComponent.h"
#include "Materials/Material.h"
#include "Materials/MaterialExpressionConstant3Vector.h"
#include "Materials/MaterialExpressionScalarParameter.h"
#include "Materials/MaterialExpressionVectorParameter.h"

#if WITH_EDITOR
#include "AssetRegistry/AssetRegistryModule.h"
#include "Factories/MaterialFactoryNew.h"
#include "UObject/SavePackage.h"
#endif

// ANexusPhysicsActor Implementation
ANexusPhysicsActor::ANexusPhysicsActor() {
  MeshComponent =
      CreateDefaultSubobject<UStaticMeshComponent>(TEXT("MeshComponent"));
  RootComponent = MeshComponent;
  Density = 1.0f;
  bUseNaniteDisplacement = false;
}

void ANexusPhysicsActor::BeginPlay() {
  Super::BeginPlay();
  // Physics actor initialization
}

// UNexusMaterialFactory Implementation
UMaterial *
UNexusMaterialFactory::CreateNaniteMaterial(const FString &Name,
                                            const FNexusMaterialStyle &Style) {
#if WITH_EDITOR
  FString PackageName = TEXT("/Game/Nexus/Generated/") + Name;
  UPackage *Package = CreatePackage(*PackageName);

  UMaterialFactoryNew *Factory = NewObject<UMaterialFactoryNew>();
  UMaterial *NewMaterial = (UMaterial *)Factory->FactoryCreateNew(
      UMaterial::StaticClass(), Package, *Name, RF_Standalone | RF_Public, NULL,
      GWarn);

  if (NewMaterial) {
    // Base Color
    UMaterialExpressionVectorParameter *BaseColorExp =
        NewObject<UMaterialExpressionVectorParameter>(NewMaterial);
    BaseColorExp->DefaultValue = Style.BaseColor;
    BaseColorExp->ParameterName = TEXT("BaseColor");
    NewMaterial->GetExpressionCollection().AddExpression(BaseColorExp);
    NewMaterial->GetEditorOnlyData()->BaseColor.Expression = BaseColorExp;

    // Roughness
    UMaterialExpressionScalarParameter *RoughnessExp =
        NewObject<UMaterialExpressionScalarParameter>(NewMaterial);
    RoughnessExp->DefaultValue = Style.Roughness;
    RoughnessExp->ParameterName = TEXT("Roughness");
    NewMaterial->GetExpressionCollection().AddExpression(RoughnessExp);
    NewMaterial->GetEditorOnlyData()->Roughness.Expression = RoughnessExp;

    // Nanite / Displacement Logic could go here (WorldPositionOffset)
    if (Style.DisplacementIntensity > 0.0f) {
      // Detailed displacement logic would involve linking
      // Multiply/VertexNormalWS etc. For now we just mark the usage.
      NewMaterial->bUsedWithNanite = true;
    }

    NewMaterial->PostEditChange();
    FAssetRegistryModule::AssetCreated(NewMaterial);
    Package->SetDirtyFlag(true);
  }

  return NewMaterial;
#else
  UE_LOG(LogTemp, Warning,
         TEXT("CreateNaniteMaterial is only available in Editor builds."));
  return nullptr;
#endif
}

UMaterial *
UNexusMaterialFactory::CreateTransmissionMaterial(const FString &Name,
                                                  float Transparency) {
#if WITH_EDITOR
  FString PackageName = TEXT("/Game/Nexus/Generated/") + Name;
  UPackage *Package = CreatePackage(*PackageName);

  UMaterialFactoryNew *Factory = NewObject<UMaterialFactoryNew>();
  UMaterial *NewMaterial = (UMaterial *)Factory->FactoryCreateNew(
      UMaterial::StaticClass(), Package, *Name, RF_Standalone | RF_Public, NULL,
      GWarn);

  if (NewMaterial) {
    NewMaterial->BlendMode = BLEND_Translucent;

    UMaterialExpressionScalarParameter *OpacityExp =
        NewObject<UMaterialExpressionScalarParameter>(NewMaterial);
    OpacityExp->DefaultValue = Transparency;
    OpacityExp->ParameterName = TEXT("Opacity");
    NewMaterial->GetExpressionCollection().AddExpression(OpacityExp);
    NewMaterial->GetEditorOnlyData()->Opacity.Expression = OpacityExp;

    NewMaterial->TwoSided = true;
    NewMaterial->bUsedWithNanite = false; // Translucency + Nanite is complex,
                                          // usually disabled for simple stuff

    NewMaterial->PostEditChange();
    FAssetRegistryModule::AssetCreated(NewMaterial);
    Package->SetDirtyFlag(true);
  }

  return NewMaterial;
#else
  UE_LOG(
      LogTemp, Warning,
      TEXT("CreateTransmissionMaterial is only available in Editor builds."));
  return nullptr;
#endif
}

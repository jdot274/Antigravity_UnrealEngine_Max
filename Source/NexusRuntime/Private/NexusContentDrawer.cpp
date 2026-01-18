#include "NexusContentDrawer.h"
#include "Components/StaticMeshComponent.h"
#include "UObject/ConstructorHelpers.h"

ANexusContentDrawer::ANexusContentDrawer() {
  PrimaryActorTick.bCanEverTick = true;

  // Create Components
  RootScene = CreateDefaultSubobject<USceneComponent>(TEXT("RootScene"));
  RootComponent = RootScene;

  CasingMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("CasingMesh"));
  CasingMesh->SetupAttachment(RootScene);

  SlidingTrayMesh =
      CreateDefaultSubobject<UStaticMeshComponent>(TEXT("SlidingTrayMesh"));
  SlidingTrayMesh->SetupAttachment(
      CasingMesh); // Attached to casing, but we will move it relatively

  // Defaults
  bTargetOpenState = false;
  CurrentOpenAlpha = 0.0f;
  OpenSpeed = 2.0f;
  OpenOffset =
      FVector(0.0f, 100.0f, 0.0f); // Slide out 100 units in Y by default

  // Attempt to finding a basic cube for visualization (Optional, but helpful)
  static ConstructorHelpers::FObjectFinder<UStaticMesh> CubeMeshAsset(
      TEXT("/Engine/BasicShapes/Cube.Cube"));
  if (CubeMeshAsset.Succeeded()) {
    CasingMesh->SetStaticMesh(CubeMeshAsset.Object);
    SlidingTrayMesh->SetStaticMesh(CubeMeshAsset.Object);

    // Scale the tray to look like a tray inside the casing
    CasingMesh->SetWorldScale3D(FVector(1.0f, 0.1f, 1.0f)); // Thin back panel
    SlidingTrayMesh->SetRelativeScale3D(FVector(0.9f, 8.0f, 0.9f));
  }
}

void ANexusContentDrawer::BeginPlay() {
  Super::BeginPlay();
  ClosedPosition = SlidingTrayMesh->GetRelativeLocation();
  OpenPosition = ClosedPosition + OpenOffset;
}

void ANexusContentDrawer::Tick(float DeltaTime) {
  Super::Tick(DeltaTime);

  float TargetAlpha = bTargetOpenState ? 1.0f : 0.0f;

  // Smooth interpolation
  if (CurrentOpenAlpha != TargetAlpha) {
    CurrentOpenAlpha =
        FMath::FInterpTo(CurrentOpenAlpha, TargetAlpha, DeltaTime, OpenSpeed);

    // Update Position
    FVector NewLocation =
        FMath::Lerp(ClosedPosition, OpenPosition, CurrentOpenAlpha);
    SlidingTrayMesh->SetRelativeLocation(NewLocation);
  }
}

void ANexusContentDrawer::ToggleDrawer() {
  bTargetOpenState = !bTargetOpenState;
}

void ANexusContentDrawer::SetDrawerOpen(bool bOpen) {
  bTargetOpenState = bOpen;
}

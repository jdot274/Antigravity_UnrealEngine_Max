#include "NexusButton.h"
#include "Kismet/GameplayStatics.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "UObject/ConstructorHelpers.h"

ANexusButton::ANexusButton() {
  PrimaryActorTick.bCanEverTick = true;

  SphereMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("SphereMesh"));
  RootComponent = SphereMesh;

  // Load Sphere Mesh
  static ConstructorHelpers::FObjectFinder<UStaticMesh> DefaultMesh(
      TEXT("/Engine/BasicShapes/Sphere.Sphere"));
  if (DefaultMesh.Succeeded()) {
    SphereMesh->SetStaticMesh(DefaultMesh.Object);
  }

  // Default Material (Basic Shape Material supports Color param?)
  // Creating a material instance in constructor is risky, usually done in
  // PostInit or BeginPlay for dynamic.
  static ConstructorHelpers::FObjectFinder<UMaterialInterface> DefaultMat(
      TEXT("/Engine/BasicShapes/BasicShapeMaterial.BasicShapeMaterial"));
  if (DefaultMat.Succeeded()) {
    SphereMesh->SetMaterial(0, DefaultMat.Object);
  }

  LabelText = CreateDefaultSubobject<UTextRenderComponent>(TEXT("LabelText"));
  LabelText->SetupAttachment(RootComponent);
  LabelText->SetRelativeLocation(FVector(0, 0, 70.0f));
  LabelText->SetWorldSize(20.0f);
  LabelText->SetHorizontalAlignment(EHorizTextAligment::EHTA_Center);
  LabelText->SetText(FText::FromString(TEXT("BUTTON")));

  TimeAccumulator = 0.0f;
  bIsHovered = false;
}

void ANexusButton::BeginPlay() {
  Super::BeginPlay();

  LabelText->SetText(FText::FromString(ButtonLabel));

  // Create Dynamic Material
  if (SphereMesh->GetMaterial(0)) {
    DynamicMat = SphereMesh->CreateAndSetMaterialInstanceDynamic(0);
    if (DynamicMat) {
      DynamicMat->SetVectorParameterValue("Color", BaseColor);
    }
  }
}

void ANexusButton::Tick(float DeltaTime) {
  Super::Tick(DeltaTime);
  TimeAccumulator += DeltaTime;

  if (DynamicMat) {
    // Pulsate logic
    float Pulse = 0.5f + 0.5f * FMath::Sin(TimeAccumulator * 3.0f);
    float GlowIntensity = bIsHovered ? 5.0f : (1.0f + Pulse * 0.5f);

    // Emissive boost hack via color brightness if material doesn't have
    // explicit Emissive Param
    FLinearColor GlowColor = BaseColor * GlowIntensity;
    DynamicMat->SetVectorParameterValue("Color", GlowColor);
  }

  // Billboard text to look at player
  if (APlayerCameraManager *Cam =
          UGameplayStatics::GetPlayerCameraManager(this, 0)) {
    FVector CamLoc = Cam->GetCameraLocation();
    FRotator LookRot = (CamLoc - GetActorLocation()).Rotation();
    LabelText->SetWorldRotation(LookRot);
  }
}

void ANexusButton::NotifyActorOnClicked(FKey ButtonPressed) {
  Super::NotifyActorOnClicked(ButtonPressed);

  UE_LOG(LogTemp, Log, TEXT("🔴 Nexus Button Clicked: %s"), *ButtonLabel);
  OnNexusActivated.Broadcast(this);

  // Visual Feedback: Jump up
  FVector Loc = GetActorLocation();
  SetActorLocation(Loc + FVector(0, 0, 10));
}

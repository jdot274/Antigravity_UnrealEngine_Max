#include "NexusPawn.h"
#include "Camera/CameraComponent.h"
#include "Components/InputComponent.h"
#include "Components/PrimitiveComponent.h"
#include "Engine/World.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/SpringArmComponent.h"

ANexusPawn::ANexusPawn() {
  PrimaryActorTick.bCanEverTick = true;
  bEnableDepthTracking = true;

  // Create Components
  RootComponent =
      CreateDefaultSubobject<USceneComponent>(TEXT("RootComponent"));

  SpringArmComp =
      CreateDefaultSubobject<USpringArmComponent>(TEXT("SpringArmComp"));
  SpringArmComp->SetupAttachment(RootComponent);
  SpringArmComp->TargetArmLength = 400.0f;
  SpringArmComp->bDoCollisionTest = true;
  SpringArmComp->bUsePawnControlRotation = true;

  CameraComp = CreateDefaultSubobject<UCameraComponent>(TEXT("CameraComp"));
  CameraComp->SetupAttachment(SpringArmComp);
}

void ANexusPawn::BeginPlay() { Super::BeginPlay(); }

void ANexusPawn::Tick(float DeltaTime) {
  Super::Tick(DeltaTime);

  if (bEnableDepthTracking) {
    HighlightObjectUnderCursor();
  }
}

void ANexusPawn::SetupPlayerInputComponent(
    UInputComponent *PlayerInputComponent) {
  Super::SetupPlayerInputComponent(PlayerInputComponent);

  PlayerInputComponent->BindAxis("MoveForward", this, &ANexusPawn::MoveForward);
  PlayerInputComponent->BindAxis("MoveRight", this, &ANexusPawn::MoveRight);

  PlayerInputComponent->BindAxis("Turn", this, &APawn::AddControllerYawInput);
  PlayerInputComponent->BindAxis("LookUp", this,
                                 &APawn::AddControllerPitchInput);
}

void ANexusPawn::MoveForward(float Value) {
  if (Value != 0.0f) {
    AddMovementInput(GetActorForwardVector(), Value);
  }
}

void ANexusPawn::MoveRight(float Value) {
  if (Value != 0.0f) {
    AddMovementInput(GetActorRightVector(), Value);
  }
}

void ANexusPawn::HighlightObjectUnderCursor() {
  APlayerController *PC = Cast<APlayerController>(GetController());
  if (!PC)
    return;

  FHitResult Hit;
  if (PC->GetHitResultUnderCursor(ECC_Visibility, false, Hit)) {
    if (AActor *HitActor = Hit.GetActor()) {
      // Logic for highlighting would go here.
      // For now, we can draw a debug sphere or just log it.
      // visual feedback will be added in Blueprints usually via PostProcess or
      // Material parameter.
    }
  }
}

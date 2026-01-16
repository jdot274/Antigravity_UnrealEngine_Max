#include "NexusMiniMapSensor.h"
#include "Components/SceneCaptureComponent2D.h"
#include "Engine/TextureRenderTarget2D.h"
#include "JsonObjectConverter.h"
#include "Kismet/KismetRenderingLibrary.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "Serialization/JsonSerializer.h"

// Sets default values
ANexusMiniMapSensor::ANexusMiniMapSensor() {
  // Set this actor to call Tick() every frame.  You can turn this off to
  // improve performance if you don't need it.
  PrimaryActorTick.bCanEverTick = true;

  // Initialize the Capture Component
  MiniMapCapture =
      CreateDefaultSubobject<USceneCaptureComponent2D>(TEXT("MiniMapCapture"));
  RootComponent = MiniMapCapture;

  // Default Orientation (Top-Down)
  MiniMapCapture->SetRelativeRotation(FRotator(-90.0f, 0.0f, 0.0f));
  MiniMapCapture->ProjectionType = ECameraProjectionMode::Orthographic;
  MiniMapCapture->OrthoWidth = 4096.0f; // Wide area coverage
}

// Called when the game starts or when spawned
void ANexusMiniMapSensor::BeginPlay() { Super::BeginPlay(); }

// Called every frame
void ANexusMiniMapSensor::Tick(float DeltaTime) {
  Super::Tick(DeltaTime);

  // Dynamic animation for the sensor "breathe" effect or scanning
  float Time = GetWorld()->GetTimeSeconds();

  // Subtle Z-movement to simulate floating sensor
  AddActorLocalOffset(FVector(0.0f, 0.0f, FMath::Sin(Time) * 0.5f));

  // --- LIVE VISUALS BRIDGE ---
  // Every 60 frames (approx 1 sec), check for external state updates
  if (GFrameCounter % 60 == 0) {
    FString StateFile = FPaths::Combine(
        FPaths::ProjectDir(), TEXT("shader_overlay/universe_state.json"));
    FString JsonContent;
    if (FFileHelper::LoadFileToString(JsonContent, *StateFile)) {
      TSharedPtr<FJsonObject> JsonObject;
      TSharedRef<TJsonReader<>> Reader =
          TJsonReaderFactory<>::Create(JsonContent);
      if (FJsonSerializer::Deserialize(Reader, JsonObject)) {
        // Update visuals based on external JSON state
        if (JsonObject->HasField("screen_distortion")) {
          float Distortion = JsonObject->GetNumberField("screen_distortion");
          MiniMapCapture->PostProcessSettings.bOverride_SceneFringeIntensity =
              true;
          MiniMapCapture->PostProcessSettings.SceneFringeIntensity = Distortion;
        }
        if (JsonObject->HasField("bloom_intensity")) {
          float Bloom = JsonObject->GetNumberField("bloom_intensity");
          MiniMapCapture->PostProcessSettings.bOverride_BloomIntensity = true;
          MiniMapCapture->PostProcessSettings.BloomIntensity = Bloom;
        }
        if (JsonObject->HasField("ortho_zoom")) {
          float Zoom = JsonObject->GetNumberField("ortho_zoom");
          MiniMapCapture->OrthoWidth = Zoom;
        }
      }
    }
  }
}

void ANexusMiniMapSensor::ActivateSensorStream(int32 ResolutionX,
                                               int32 ResolutionY) {
  SetupRenderTarget(ResolutionX, ResolutionY);
  MiniMapCapture->TextureTarget = RenderTarget;
  MiniMapCapture->CaptureSource = ESceneCaptureSource::SCS_FinalColorLDR;

  UE_LOG(LogTemp, Log, TEXT("Nexus MiniMap Sensor Active: %dx%d"), ResolutionX,
         ResolutionY);
}

void ANexusMiniMapSensor::SetupRenderTarget(int32 ResX, int32 ResY) {
  RenderTarget = NewObject<UTextureRenderTarget2D>(this);
  RenderTarget->RenderTargetFormat = ETextureRenderTargetFormat::RTF_RGBA8;
  RenderTarget->InitAutoFormat(ResX, ResY);
  RenderTarget->UpdateResourceImmediate(true);
}

void ANexusMiniMapSensor::ApplySchematicFilter() {
  // In a full C++ impl, we would load a specific Material Instance here.
  // For now, we simulate the post-processing configuration.

  FPostProcessSettings &Settings = MiniMapCapture->PostProcessSettings;

  // Enable Post-Process properties
  Settings.bOverride_SceneFringeIntensity = true;
  Settings.SceneFringeIntensity =
      2.0f; // Chromatic Aberration for "Digital" look

  Settings.bOverride_FilmGrainIntensity = true;
  Settings.FilmGrainIntensity = 0.5f; // Noise

  Settings.bOverride_BloomIntensity = true;
  Settings.BloomIntensity = 2.0f; // Glows

  // Note: The "Outline" or "Edge Detect" is typically done via a Weighted
  // Blendable Material. We assume the Python script ensures the material asset
  // exists and assigns it via Blueprint or we'd load it here with
  // FSoftObjectPath.
}

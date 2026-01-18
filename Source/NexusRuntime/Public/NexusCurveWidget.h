// NexusCurveWidget.h
// A Photoshop-style color curves editor widget for Unreal Engine
// Supports adding/removing control points and smooth bezier interpolation

#pragma once

#include "CoreMinimal.h"
#include "Components/Widget.h"
#include "Widgets/SCompoundWidget.h"
#include "NexusCurveWidget.generated.h"

// Control point on the curve
USTRUCT(BlueprintType)
struct FCurveControlPoint {
  GENERATED_BODY()

  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Curve")
  FVector2D Position; // X,Y both 0-1 range

  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Curve")
  bool bIsSelected;

  FCurveControlPoint() : Position(0.f, 0.f), bIsSelected(false) {}

  FCurveControlPoint(float X, float Y) : Position(X, Y), bIsSelected(false) {}
};

// Delegate for curve changes
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnCurveChanged);

/**
 * SNexusCurveEditor - Slate widget for drawing curves
 */
class SNexusCurveEditor : public SCompoundWidget {
public:
  SLATE_BEGIN_ARGS(SNexusCurveEditor)
      : _GridColor(FLinearColor(0.2f, 0.2f, 0.2f, 1.f)),
        _CurveColor(FLinearColor(0.f, 1.f, 0.96f, 1.f)) // Cyan
        ,
        _PointColor(FLinearColor(1.f, 1.f, 1.f, 1.f)),
        _BackgroundColor(FLinearColor(0.05f, 0.05f, 0.06f, 1.f)) {}
  SLATE_ARGUMENT(FLinearColor, GridColor)
  SLATE_ARGUMENT(FLinearColor, CurveColor)
  SLATE_ARGUMENT(FLinearColor, PointColor)
  SLATE_ARGUMENT(FLinearColor, BackgroundColor)
  SLATE_END_ARGS()

  void Construct(const FArguments &InArgs);

  // SWidget interface
  virtual int32 OnPaint(const FPaintArgs &Args,
                        const FGeometry &AllottedGeometry,
                        const FSlateRect &MyCullingRect,
                        FSlateWindowElementList &OutDrawElements, int32 LayerId,
                        const FWidgetStyle &InWidgetStyle,
                        bool bParentEnabled) const override;

  virtual FReply OnMouseButtonDown(const FGeometry &MyGeometry,
                                   const FPointerEvent &MouseEvent) override;
  virtual FReply OnMouseButtonUp(const FGeometry &MyGeometry,
                                 const FPointerEvent &MouseEvent) override;
  virtual FReply OnMouseMove(const FGeometry &MyGeometry,
                             const FPointerEvent &MouseEvent) override;
  virtual FReply
  OnMouseButtonDoubleClick(const FGeometry &MyGeometry,
                           const FPointerEvent &MouseEvent) override;

  // Control points
  TArray<FCurveControlPoint> ControlPoints;

  // Callback when curve changes
  TFunction<void()> OnCurveChangedCallback;

  // Evaluate curve at X position (0-1)
  float EvaluateCurve(float X) const;

private:
  FLinearColor GridColor;
  FLinearColor CurveColor;
  FLinearColor PointColor;
  FLinearColor BackgroundColor;

  int32 DraggedPointIndex;
  bool bIsDragging;

  // Convert screen to curve space
  FVector2D ScreenToCurve(const FGeometry &Geo,
                          const FVector2D &ScreenPos) const;
  FVector2D CurveToScreen(const FGeometry &Geo,
                          const FVector2D &CurvePos) const;

  // Find point near position
  int32 FindPointNear(const FVector2D &CurvePos, float Threshold = 0.05f) const;

  // Draw bezier curve
  void DrawCurve(const FGeometry &Geo, FSlateWindowElementList &OutDrawElements,
                 int32 LayerId) const;
};

/**
 * UNexusCurveWidget - UMG Widget wrapper
 */
UCLASS()
class NEXUSRUNTIME_API UNexusCurveWidget : public UWidget {
  GENERATED_BODY()

public:
  UNexusCurveWidget(const FObjectInitializer &ObjectInitializer);

  // Colors
  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Appearance")
  FLinearColor GridColor;

  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Appearance")
  FLinearColor CurveColor;

  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Appearance")
  FLinearColor PointColor;

  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Appearance")
  FLinearColor BackgroundColor;

  // Control points
  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Curve")
  TArray<FCurveControlPoint> ControlPoints;

  // Events
  UPROPERTY(BlueprintAssignable, Category = "Curve|Events")
  FOnCurveChanged OnCurveChanged;

  // Blueprint functions
  UFUNCTION(BlueprintCallable, Category = "Curve")
  void AddPoint(float X, float Y);

  UFUNCTION(BlueprintCallable, Category = "Curve")
  void RemovePoint(int32 Index);

  UFUNCTION(BlueprintCallable, Category = "Curve")
  void ClearPoints();

  UFUNCTION(BlueprintCallable, Category = "Curve")
  void ResetToDefault();

  UFUNCTION(BlueprintPure, Category = "Curve")
  float EvaluateCurve(float X) const;

  UFUNCTION(BlueprintPure, Category = "Curve")
  TArray<FCurveControlPoint> GetPoints() const;

protected:
  // UWidget interface
  virtual TSharedRef<SWidget> RebuildWidget() override;
  virtual void SynchronizeProperties() override;
  virtual void ReleaseSlateResources(bool bReleaseChildren) override;

#if WITH_EDITOR
  virtual const FText GetPaletteCategory() override;
#endif

private:
  TSharedPtr<SNexusCurveEditor> CurveEditor;
};

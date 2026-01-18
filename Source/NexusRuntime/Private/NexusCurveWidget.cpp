// NexusCurveWidget.cpp
// Implementation of Photoshop-style color curves editor

#include "NexusCurveWidget.h"
#include "Rendering/DrawElements.h"
#include "Widgets/SBoxPanel.h"

// ============================================================================
// SNexusCurveEditor - Slate Implementation
// ============================================================================

void SNexusCurveEditor::Construct(const FArguments &InArgs) {
  GridColor = InArgs._GridColor;
  CurveColor = InArgs._CurveColor;
  PointColor = InArgs._PointColor;
  BackgroundColor = InArgs._BackgroundColor;

  DraggedPointIndex = INDEX_NONE;
  bIsDragging = false;

  // Default diagonal line (identity curve)
  ControlPoints.Add(FCurveControlPoint(0.f, 0.f));
  ControlPoints.Add(FCurveControlPoint(1.f, 1.f));
}

FVector2D SNexusCurveEditor::ScreenToCurve(const FGeometry &Geo,
                                           const FVector2D &ScreenPos) const {
  FVector2D LocalPos = Geo.AbsoluteToLocal(ScreenPos);
  FVector2D Size = Geo.GetLocalSize();

  float X = FMath::Clamp(LocalPos.X / Size.X, 0.f, 1.f);
  float Y = FMath::Clamp(1.f - (LocalPos.Y / Size.Y), 0.f, 1.f); // Invert Y

  return FVector2D(X, Y);
}

FVector2D SNexusCurveEditor::CurveToScreen(const FGeometry &Geo,
                                           const FVector2D &CurvePos) const {
  FVector2D Size = Geo.GetLocalSize();
  return FVector2D(CurvePos.X * Size.X,
                   (1.f - CurvePos.Y) * Size.Y // Invert Y
  );
}

int32 SNexusCurveEditor::FindPointNear(const FVector2D &CurvePos,
                                       float Threshold) const {
  for (int32 i = 0; i < ControlPoints.Num(); ++i) {
    if (FVector2D::Distance(ControlPoints[i].Position, CurvePos) < Threshold) {
      return i;
    }
  }
  return INDEX_NONE;
}

float SNexusCurveEditor::EvaluateCurve(float X) const {
  if (ControlPoints.Num() == 0)
    return X;
  if (ControlPoints.Num() == 1)
    return ControlPoints[0].Position.Y;

  // Find surrounding points
  int32 LeftIdx = 0;
  int32 RightIdx = ControlPoints.Num() - 1;

  for (int32 i = 0; i < ControlPoints.Num(); ++i) {
    if (ControlPoints[i].Position.X <= X) {
      LeftIdx = i;
    }
    if (ControlPoints[i].Position.X >= X && i < RightIdx) {
      RightIdx = i;
      break;
    }
  }

  // Clamp to endpoints
  if (X <= ControlPoints[0].Position.X)
    return ControlPoints[0].Position.Y;
  if (X >= ControlPoints.Last().Position.X)
    return ControlPoints.Last().Position.Y;

  // Linear interpolation between points (could be upgraded to bezier)
  const FCurveControlPoint &Left = ControlPoints[LeftIdx];
  const FCurveControlPoint &Right = ControlPoints[RightIdx];

  float T = (X - Left.Position.X) /
            FMath::Max(Right.Position.X - Left.Position.X, 0.0001f);

  // Smooth step for nicer curves
  T = T * T * (3.f - 2.f * T);

  return FMath::Lerp(Left.Position.Y, Right.Position.Y, T);
}

int32 SNexusCurveEditor::OnPaint(const FPaintArgs &Args,
                                 const FGeometry &AllottedGeometry,
                                 const FSlateRect &MyCullingRect,
                                 FSlateWindowElementList &OutDrawElements,
                                 int32 LayerId,
                                 const FWidgetStyle &InWidgetStyle,
                                 bool bParentEnabled) const {
  const FVector2D Size = AllottedGeometry.GetLocalSize();

  // 1. Background
  FSlateDrawElement::MakeBox(OutDrawElements, LayerId,
                             AllottedGeometry.ToPaintGeometry(),
                             FCoreStyle::Get().GetBrush("WhiteBrush"),
                             ESlateDrawEffect::None, BackgroundColor);
  LayerId++;

  // 2. Grid lines
  const int32 GridDivisions = 4;
  TArray<FVector2D> GridPoints;

  for (int32 i = 0; i <= GridDivisions; ++i) {
    float Pos = (float)i / GridDivisions;

    // Vertical line
    GridPoints.Reset();
    GridPoints.Add(FVector2D(Pos * Size.X, 0.f));
    GridPoints.Add(FVector2D(Pos * Size.X, Size.Y));
    FSlateDrawElement::MakeLines(OutDrawElements, LayerId,
                                 AllottedGeometry.ToPaintGeometry(), GridPoints,
                                 ESlateDrawEffect::None, GridColor, true, 1.f);

    // Horizontal line
    GridPoints.Reset();
    GridPoints.Add(FVector2D(0.f, Pos * Size.Y));
    GridPoints.Add(FVector2D(Size.X, Pos * Size.Y));
    FSlateDrawElement::MakeLines(OutDrawElements, LayerId,
                                 AllottedGeometry.ToPaintGeometry(), GridPoints,
                                 ESlateDrawEffect::None, GridColor, true, 1.f);
  }
  LayerId++;

  // 3. Diagonal reference line
  GridPoints.Reset();
  GridPoints.Add(FVector2D(0.f, Size.Y));
  GridPoints.Add(FVector2D(Size.X, 0.f));
  FSlateDrawElement::MakeLines(
      OutDrawElements, LayerId, AllottedGeometry.ToPaintGeometry(), GridPoints,
      ESlateDrawEffect::None, FLinearColor(0.3f, 0.3f, 0.3f, 0.5f), true, 1.f);
  LayerId++;

  // 4. Draw the curve
  const int32 CurveResolution = 100;
  TArray<FVector2D> CurvePoints;

  for (int32 i = 0; i <= CurveResolution; ++i) {
    float X = (float)i / CurveResolution;
    float Y = EvaluateCurve(X);
    CurvePoints.Add(CurveToScreen(AllottedGeometry, FVector2D(X, Y)));
  }

  FSlateDrawElement::MakeLines(OutDrawElements, LayerId,
                               AllottedGeometry.ToPaintGeometry(), CurvePoints,
                               ESlateDrawEffect::None, CurveColor, true, 2.f);
  LayerId++;

  // 5. Draw control points
  const float PointRadius = 6.f;
  for (const FCurveControlPoint &Point : ControlPoints) {
    FVector2D ScreenPos = CurveToScreen(AllottedGeometry, Point.Position);

    FLinearColor Color = Point.bIsSelected ? FLinearColor::Yellow : PointColor;

    // Outer circle
    FSlateDrawElement::MakeBox(
        OutDrawElements, LayerId,
        AllottedGeometry.ToPaintGeometry(
            FVector2D(PointRadius * 2.f, PointRadius * 2.f),
            FSlateLayoutTransform(ScreenPos -
                                  FVector2D(PointRadius, PointRadius))),
        FCoreStyle::Get().GetBrush("WhiteBrush"), ESlateDrawEffect::None,
        Color);
  }
  LayerId++;

  return LayerId;
}

FReply SNexusCurveEditor::OnMouseButtonDown(const FGeometry &MyGeometry,
                                            const FPointerEvent &MouseEvent) {
  if (MouseEvent.GetEffectingButton() == EKeys::LeftMouseButton) {
    FVector2D CurvePos =
        ScreenToCurve(MyGeometry, MouseEvent.GetScreenSpacePosition());
    int32 PointIdx = FindPointNear(CurvePos);

    if (PointIdx != INDEX_NONE) {
      // Start dragging existing point
      DraggedPointIndex = PointIdx;
      bIsDragging = true;
      return FReply::Handled().CaptureMouse(SharedThis(this));
    }
  }

  return FReply::Unhandled();
}

FReply SNexusCurveEditor::OnMouseButtonUp(const FGeometry &MyGeometry,
                                          const FPointerEvent &MouseEvent) {
  if (bIsDragging) {
    bIsDragging = false;
    DraggedPointIndex = INDEX_NONE;

    // Sort points by X
    ControlPoints.Sort(
        [](const FCurveControlPoint &A, const FCurveControlPoint &B) {
          return A.Position.X < B.Position.X;
        });

    if (OnCurveChangedCallback) {
      OnCurveChangedCallback();
    }

    return FReply::Handled().ReleaseMouseCapture();
  }

  return FReply::Unhandled();
}

FReply SNexusCurveEditor::OnMouseMove(const FGeometry &MyGeometry,
                                      const FPointerEvent &MouseEvent) {
  if (bIsDragging && DraggedPointIndex != INDEX_NONE) {
    FVector2D CurvePos =
        ScreenToCurve(MyGeometry, MouseEvent.GetScreenSpacePosition());

    // Don't allow moving first/last points horizontally
    if (DraggedPointIndex == 0) {
      CurvePos.X = 0.f;
    } else if (DraggedPointIndex == ControlPoints.Num() - 1) {
      CurvePos.X = 1.f;
    }

    ControlPoints[DraggedPointIndex].Position = CurvePos;

    return FReply::Handled();
  }

  return FReply::Unhandled();
}

FReply
SNexusCurveEditor::OnMouseButtonDoubleClick(const FGeometry &MyGeometry,
                                            const FPointerEvent &MouseEvent) {
  FVector2D CurvePos =
      ScreenToCurve(MyGeometry, MouseEvent.GetScreenSpacePosition());
  int32 PointIdx = FindPointNear(CurvePos);

  if (PointIdx != INDEX_NONE && PointIdx != 0 &&
      PointIdx != ControlPoints.Num() - 1) {
    // Remove point (except endpoints)
    ControlPoints.RemoveAt(PointIdx);
  } else if (PointIdx == INDEX_NONE) {
    // Add new point
    ControlPoints.Add(FCurveControlPoint(CurvePos.X, CurvePos.Y));

    // Sort by X
    ControlPoints.Sort(
        [](const FCurveControlPoint &A, const FCurveControlPoint &B) {
          return A.Position.X < B.Position.X;
        });
  }

  if (OnCurveChangedCallback) {
    OnCurveChangedCallback();
  }

  return FReply::Handled();
}

// ============================================================================
// UNexusCurveWidget - UMG Wrapper
// ============================================================================

UNexusCurveWidget::UNexusCurveWidget(
    const FObjectInitializer &ObjectInitializer)
    : Super(ObjectInitializer) {
  GridColor = FLinearColor(0.2f, 0.2f, 0.2f, 1.f);
  CurveColor = FLinearColor(0.f, 1.f, 0.96f, 1.f); // Cyan
  PointColor = FLinearColor(1.f, 1.f, 1.f, 1.f);
  BackgroundColor = FLinearColor(0.05f, 0.05f, 0.06f, 1.f);
}

TSharedRef<SWidget> UNexusCurveWidget::RebuildWidget() {
  CurveEditor = SNew(SNexusCurveEditor)
                    .GridColor(GridColor)
                    .CurveColor(CurveColor)
                    .PointColor(PointColor)
                    .BackgroundColor(BackgroundColor);

  CurveEditor->OnCurveChangedCallback = [this]() {
    ControlPoints = CurveEditor->ControlPoints;
    OnCurveChanged.Broadcast();
  };

  return CurveEditor.ToSharedRef();
}

void UNexusCurveWidget::SynchronizeProperties() {
  Super::SynchronizeProperties();

  if (CurveEditor.IsValid()) {
    CurveEditor->ControlPoints = ControlPoints;
  }
}

void UNexusCurveWidget::ReleaseSlateResources(bool bReleaseChildren) {
  Super::ReleaseSlateResources(bReleaseChildren);
  CurveEditor.Reset();
}

#if WITH_EDITOR
const FText UNexusCurveWidget::GetPaletteCategory() {
  return FText::FromString(TEXT("Nexus"));
}
#endif

void UNexusCurveWidget::AddPoint(float X, float Y) {
  ControlPoints.Add(FCurveControlPoint(X, Y));
  ControlPoints.Sort(
      [](const FCurveControlPoint &A, const FCurveControlPoint &B) {
        return A.Position.X < B.Position.X;
      });

  if (CurveEditor.IsValid()) {
    CurveEditor->ControlPoints = ControlPoints;
  }

  OnCurveChanged.Broadcast();
}

void UNexusCurveWidget::RemovePoint(int32 Index) {
  if (Index > 0 && Index < ControlPoints.Num() - 1) {
    ControlPoints.RemoveAt(Index);

    if (CurveEditor.IsValid()) {
      CurveEditor->ControlPoints = ControlPoints;
    }

    OnCurveChanged.Broadcast();
  }
}

void UNexusCurveWidget::ClearPoints() {
  ControlPoints.Empty();
  ControlPoints.Add(FCurveControlPoint(0.f, 0.f));
  ControlPoints.Add(FCurveControlPoint(1.f, 1.f));

  if (CurveEditor.IsValid()) {
    CurveEditor->ControlPoints = ControlPoints;
  }

  OnCurveChanged.Broadcast();
}

void UNexusCurveWidget::ResetToDefault() { ClearPoints(); }

float UNexusCurveWidget::EvaluateCurve(float X) const {
  if (CurveEditor.IsValid()) {
    return CurveEditor->EvaluateCurve(X);
  }
  return X;
}

TArray<FCurveControlPoint> UNexusCurveWidget::GetPoints() const {
  return ControlPoints;
}

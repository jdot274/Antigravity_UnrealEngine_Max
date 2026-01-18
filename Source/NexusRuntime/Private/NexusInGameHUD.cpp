#include "NexusInGameHUD.h"
#include "Blueprint/WidgetTree.h"
#include "Components/CanvasPanel.h"
#include "Components/CanvasPanelSlot.h"
#include "Components/TextBlock.h"
#include "NexusCurveWidget.h"

void UNexusInGameHUD::NativeConstruct() {
  Super::NativeConstruct();

  // Optional: Auto-setup if not bound (though usually done in BP)
  if (NotificationText) {
    NotificationText->SetText(FText::FromString(TEXT("Nexus System Online")));
  }

  // Simulate Editor: Create Curve Widget directly
  if (!CurveEditor) {
    // Must check WidgetTree. If this is a BP widget, WidgetTree exists.
    // If strict C++, we might need to initialize it.
    if (WidgetTree) {
      // 1. Create a Root Canvas if none exists (simple fix for C++ only widget)
      UCanvasPanel *RootCanvas = WidgetTree->ConstructWidget<UCanvasPanel>(
          UCanvasPanel::StaticClass(), TEXT("RootCanvas"));
      WidgetTree->RootWidget = RootCanvas;

      // 2. Create Curve Editor
      CurveEditor = WidgetTree->ConstructWidget<UNexusCurveWidget>(
          UNexusCurveWidget::StaticClass(), TEXT("CurveEditor"));

      if (CurveEditor && RootCanvas) {
        UCanvasPanelSlot *Slot = RootCanvas->AddChildToCanvas(CurveEditor);
        if (Slot) {
          Slot->SetPosition(FVector2D(50, 50));
          Slot->SetSize(FVector2D(400, 300));
        }
      }
    }
  }
}

void UNexusInGameHUD::ShowNotification(FString Title, FString Message) {
  if (NotificationText) {
    FString FullMsg = FString::Printf(TEXT("%s: %s"), *Title, *Message);
    NotificationText->SetText(FText::FromString(FullMsg));

    // Simple fade animation could be done here or in BP opacity binding
    PlayAnimation(NULL); // Placeholder for an animation uobject
  }
}

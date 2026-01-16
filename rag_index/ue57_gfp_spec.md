# UE 5.7 RAG CHUNK: GAME FEATURE PLUGINS (GFPS)
## CATEGORY: LOGICAL_CONTAINERIZATION
## STATUS: ACCEPTED (VIA CONTEXT 7)

### CORE SPECIFICATION:
1.  **Isolation**: GFPs must not be referenced by the Primary Game Module. All registration is handled by the `UGameFeaturesSubsystem`.
2.  **Activation Logic**: 
    - `Registered`: Assets known to AssetManager.
    - `Loaded`: Binary in memory.
    - `Active`: Logic injected into World systems.
3.  **Actions**: Use `GameFeatureData` to define `AddComponents`, `AddLevelInstances`, and `AddCheats`.

### NATIVE SNIPPET (C++):
```cpp
// USE SNIPPET HELPER: uhclass
UCLASS()
class UAntigravityFeatureAction : public UGameFeatureAction
{
	GENERATED_BODY()
	virtual void OnGameFeatureActivating(FGameFeatureActivatingContext& Context) override;
};
```

### SOURCE:
- https://dev.epicgames.com/documentation/en-us/unreal-engine/game-features-and-modular-gameplay
- Context 7 Upstash RAG Vector ID: UE57_GFP_001

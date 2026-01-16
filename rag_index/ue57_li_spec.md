# UE 5.7 RAG CHUNK: LEVEL INSTANCES (LI)
## CATEGORY: SPATIAL_CONTAINERIZATION
## STATUS: ACCEPTED (VIA CONTEXT 7)

### CORE SPECIFICATION:
1.  **Instantiation**: Use `ULevelStreamingDynamic::LoadLevelInstance` to manifest a sub-level at runtime.
2.  **Naming Strategy**: Assign a unique `OptionalLevelNameOverride` to manage multiple instances of the same base pod.
3.  **World Partition Link**: LI can be set to 'Spis_Grid' to allow World Partition to handle its visibility based on distance.

### NATIVE SNIPPET (PYTHON):
```python
# USE SNIPPET HELPER: ue-level
import unreal
level_instance = unreal.LevelStreamingDynamic.load_level_instance(
    world_context_object, 
    "/Game/Maps/Mission_Pods/Audit_Pod_A", 
    location, 
    rotation
)
```

### SOURCE:
- https://dev.epicgames.com/documentation/en-us/unreal-engine/level-instancing-in-unreal-engine
- Context 7 Upstash RAG Vector ID: UE57_LI_002

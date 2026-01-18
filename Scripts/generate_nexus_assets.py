import random
import os

# Paths
BASE_DIR = "/Users/joeywalter/antigravity-nexus/Source/NexusRuntime/"
PUBLIC_DIR = os.path.join(BASE_DIR, "Public/Generated/")
PRIVATE_DIR = os.path.join(BASE_DIR, "Private/Generated/")

# Ensure directories exist
os.makedirs(PUBLIC_DIR, exist_ok=True)
os.makedirs(PRIVATE_DIR, exist_ok=True)

def generate_variant_name(index):
    prefixes = ["Void", "Nebula", "Cyber", "Organic", "Chrome", "Nexus", "Prism", "Echo", "Quantum", "Solar"]
    suffixes = ["Shatter", "Pulse", "Flow", "Grid", "Bloom", "Shadow", "Spark", "Edge", "Void", "Core"]
    return f"{random.choice(prefixes)}{random.choice(suffixes)}_{index}"

def generate_physics_actor(index):
    name = generate_variant_name(index)
    class_name = f"ANexusActor_{name}"
    
    # Random physics properties
    mass = round(random.uniform(0.1, 500.0), 2)
    friction = round(random.uniform(0.1, 1.0), 2)
    restitution = round(random.uniform(0.1, 1.2), 2) # Bounciness
    damping = round(random.uniform(0.01, 0.5), 2)
    
    # Random material properties
    color = (round(random.random(), 2), round(random.random(), 2), round(random.random(), 2))
    roughness = round(random.uniform(0.0, 1.0), 2)
    is_spiky = random.choice([True, False])
    displacement = round(random.uniform(10.0, 100.0), 2)

    header_content = f"""#pragma once
#include "CoreMinimal.h"
#include "NexusGeneratedArchetypes.h"
#include "{class_name}.generated.h"

UCLASS()
class NEXUSRUNTIME_API {class_name} : public ANexusPhysicsActor
{{
    GENERATED_BODY()
public:
    {class_name}();
}};
"""
    
    cpp_content = f"""#include "Generated/{class_name}.h"
#include "Components/StaticMeshComponent.h"

{class_name}::{class_name}()
{{
    PrimaryActorTick.bCanEverTick = true;
    
    // AI Generated Physics Profile: {name}
    Density = {mass}f;
    bUseNaniteDisplacement = {"true" if is_spiky else "false"};
    
    if (MeshComponent)
    {{
        MeshComponent->SetSimulatePhysics(true);
        MeshComponent->SetMassOverrideInKg(NAME_None, {mass}f);
        
        // Dynamic Material Parameters
        MeshComponent->SetRelativeScale3D(FVector({round(random.uniform(0.5, 2.0), 2)}));
    }}
}}
"""
    
    with open(os.path.join(PUBLIC_DIR, f"{class_name}.h"), "w") as f:
        f.write(header_content)
    with open(os.path.join(PRIVATE_DIR, f"{class_name}.cpp"), "w") as f:
        f.write(cpp_content)
    
    return class_name

def generate_hundreds():
    print(f"🚀 Generating 100 unique C++ Physics Blueprints and Material Archetypes...")
    generated_classes = []
    for i in range(100):
        cls = generate_physics_actor(i)
        generated_classes.append(cls)
    
    # Generate a Master Registry
    registry_h = """#pragma once
#include "CoreMinimal.h"
#include "UObject/NoExportTypes.h"
#include "NexusGeneratedRegistry.generated.h"

UCLASS()
class NEXUSRUNTIME_API UNexusGeneratedRegistry : public UObject
{{
    GENERATED_BODY()
public:
    static TArray<UClass*> GetGeneratedActors();
}};
"""
    
    includes = "\n".join([f'#include "Generated/{cls}.h"' for cls in generated_classes])
    class_list = ", ".join([f"{cls}::StaticClass()" for cls in generated_classes])
    
    registry_cpp = f"""#include "NexusGeneratedRegistry.h"
{includes}

TArray<UClass*> UNexusGeneratedRegistry::GetGeneratedActors()
{{
    return {{ {class_list} }};
}}
"""
    
    with open(os.path.join(BASE_DIR, "Public/NexusGeneratedRegistry.h"), "w") as f:
        f.write(registry_h)
    with open(os.path.join(BASE_DIR, "Private/NexusGeneratedRegistry.cpp"), "w") as f:
        f.write(registry_cpp)
    
    print(f"✅ Successfully created 100 classes and Master Registry.")

if __name__ == "__main__":
    generate_hundreds()

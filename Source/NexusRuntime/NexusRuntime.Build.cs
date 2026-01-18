using UnrealBuildTool;

public class NexusRuntime : ModuleRules
{
	public NexusRuntime(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
	
		PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine", "InputCore" });

		PrivateDependencyModuleNames.AddRange(new string[] { 
            "HTTP", 
            "Json", 
            "JsonUtilities",
            "PixelStreaming", // For predictive streaming hook
            "ProceduralMeshComponent",
            "UMG",
            "Slate",
            "SlateCore"
        });

        if (Target.bBuildEditor)
        {
            PrivateDependencyModuleNames.AddRange(new string[] {
                "UnrealEd",
                "AssetTools",
                "AssetRegistry",
                "KismetCompiler",
                "BlueprintGraph"
            });
        }
	}
}

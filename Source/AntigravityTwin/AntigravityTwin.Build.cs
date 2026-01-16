using UnrealBuildTool;

public class AntigravityTwin : ModuleRules
{
	public AntigravityTwin(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
	
		PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine", "InputCore", "UMG", "Blutility" });

		PrivateDependencyModuleNames.AddRange(new string[] {  });
	}
}

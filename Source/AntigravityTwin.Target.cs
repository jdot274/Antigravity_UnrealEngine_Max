using UnrealBuildTool;
using System.Collections.Generic;

public class AntigravityTwinTarget : TargetRules
{
	public AntigravityTwinTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Game;
		DefaultBuildSettings = BuildSettingsVersion.V6;
		IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
		ExtraModuleNames.Add("AntigravityTwin");
	}
}

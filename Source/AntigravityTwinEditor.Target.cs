using UnrealBuildTool;
using System.Collections.Generic;

public class AntigravityTwinEditorTarget : TargetRules
{
	public AntigravityTwinEditorTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Editor;
		DefaultBuildSettings = BuildSettingsVersion.V6;
		IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
		ExtraModuleNames.Add("AntigravityTwin");
	}
}


#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "MCPServerData.h"
#include "MCPMarkdownParser.generated.h"

UCLASS()
class MCPVIEWER_API UMCPMarkdownParser : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()

public:
	UFUNCTION(BlueprintCallable, Category = "MCP Parser")
	static TArray<UMCPServerData*> ParseMCPMarkdown(const FString& MarkdownText);
};

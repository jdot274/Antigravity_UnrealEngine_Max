
#pragma once

#include "CoreMinimal.h"
#include "UObject/NoExportTypes.h"
#include "MCPServerData.generated.h"

UCLASS(Blueprintable, BlueprintType)
class MCPVIEWER_API UMCPServerData : public UObject
{
	GENERATED_BODY()

public:
	UPROPERTY(BlueprintReadWrite, Category = "MCP Server")
	FString ServerName;

	UPROPERTY(BlueprintReadWrite, Category = "MCP Server")
	FString Description;

	UPROPERTY(BlueprintReadWrite, Category = "MCP Server")
	FString URL;
};


#include "MCPMarkdownParser.h"
#include "MCPServerData.h"

TArray<UMCPServerData*> UMCPMarkdownParser::ParseMCPMarkdown(const FString& MarkdownText)
{
	TArray<UMCPServerData*> ServerDataArray;
	TArray<FString> Lines;
	MarkdownText.ParseIntoArrayLines(Lines);

	for (int32 i = 0; i < Lines.Num(); ++i)
	{
		const FString& Line = Lines[i];
		if (Line.StartsWith("["))
		{
			UMCPServerData* ServerData = NewObject<UMCPServerData>();
			FString NamePart;
			FString UrlPart;
			Line.Split("](", &NamePart, &UrlPart);
			ServerData->ServerName = NamePart.RightChop(1);
			ServerData->URL = UrlPart.LeftChop(1);

			// The next line should be the description
			if (i + 1 < Lines.Num())
			{
				ServerData->Description = Lines[i + 1];
			}
			
			ServerDataArray.Add(ServerData);
		}
	}

	return ServerDataArray;
}

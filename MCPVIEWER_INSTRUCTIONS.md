
# MCP Viewer Instructions

This document provides instructions on how to create the user interface for the MCP Viewer and how to use the C++ code created to display the list of MCP servers.

## 1. Compile the C++ Code

Before you can use the C++ classes in the Unreal Editor, you need to compile them. You can do this by opening the `MCPViewer.uproject` file in the Unreal Editor. The editor will detect the new C++ files and ask you to compile them. Click "Yes" to compile the code.

Alternatively, you can try to run the `build_mcpviewer.sh` script in the root of the project.

## 2. Create the MCP Server Widget

1.  Open the Unreal Editor and open the `MCPViewer` project.
2.  In the Content Browser, create a new folder called `UI`.
3.  Right-click in the `UI` folder and select "User Interface" -> "Widget Blueprint".
4.  Name the new widget `W_MCPServerList`.
5.  Open the `W_MCPServerList` widget.
6.  In the designer tab, add a `Scroll Box` to the canvas.
7.  Add a `Vertical Box` inside the `Scroll Box`.
8.  In the Graph tab, go to the "Event Graph" and add the following logic:
    *   On the `Event Construct` node, create a new function called `PopulateServerList`.
    *   In the `PopulateServerList` function, add the following nodes:
        *   `Get All Assets of Class` with the class set to `TextAsset`. You will need to create a `TextAsset` in the editor containing the content of `Source/NexusRuntime/Public/## All MCP servers`.
        *   Get the first element from the array.
        *   From the `TextAsset`, get the `Text` property.
        *   Call the `ParseMCPMarkdown` function from the `MCPMarkdownParser` C++ class.
        *   For each `MCPServerData` object returned from the `ParseMCPMarkdown` function, create a new widget. You will need to create another widget to represent a single server entry, let's call it `W_MCPServerEntry`.
        *   The `W_MCPServerEntry` widget should have `Text` blocks for the server name, description, and a button to open the URL.
        *   Add the `W_MCPServerEntry` widget to the `Vertical Box` in the `W_MCPServerList` widget.

## 3. Create the MCP Server Entry Widget

1.  Create a new `Widget Blueprint` called `W_MCPServerEntry`.
2.  This widget should contain:
    *   A `Vertical Box`.
    *   A `Text` block for the server name.
    *   A `Text` block for the description.
    *   A `Button` to open the URL.
3.  Create variables in this widget to hold the `MCPServerData`.
4.  When the widget is constructed, set the text of the `Text` blocks from the `MCPServerData` variable.
5.  On the `Button`'s `OnClicked` event, use the `Launch URL` node to open the server's URL.

## 4. Add the Widget to the Level

1.  Open the `MCPViewerMap` level.
2.  Open the Level Blueprint.
3.  On the `Event BeginPlay` node, add the following nodes:
    *   `Create Widget` with the class set to `W_MCPServerList`.
    *   `Add to Viewport`.

After following these steps, you will have a working MCP Viewer that displays the list of MCP servers from the markdown file.

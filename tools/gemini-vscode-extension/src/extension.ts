import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    console.log('Antigravity Gemini Assist is now active!');

    // 1. Register the Hover Provider
    const hoverProvider = vscode.languages.registerHoverProvider('*', new AntigravityHoverProvider());
    context.subscriptions.push(hoverProvider);

    // 2. Register a Status Bar Item for "Click" interaction
    const statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBarItem.command = 'antigravity.askGemini';
    context.subscriptions.push(statusBarItem);

    // Update Status Bar based on selection
    vscode.window.onDidChangeTextEditorSelection((e) => {
        if (!e.selections[0].isEmpty) {
            statusBarItem.text = `$(sparkle) Ask Gemini (${e.selections[0].end.line - e.selections[0].start.line + 1} lines)`;
            statusBarItem.show();
        } else {
            statusBarItem.hide();
        }
    });

    // 3. Register Commands
    const geminiService = new GeminiService();

    context.subscriptions.push(
        vscode.commands.registerCommand('antigravity.explainCode', () => handleCommand(geminiService, 'Explain this code')),
        vscode.commands.registerCommand('antigravity.generateTests', () => handleCommand(geminiService, 'Generate unit tests for this code')),
        vscode.commands.registerCommand('antigravity.refactorCode', () => handleCommand(geminiService, 'Refactor this code for performance and readability')),
        vscode.commands.registerCommand('antigravity.askGemini', () => handleCustomQuery(geminiService))
    );
}

class AntigravityHoverProvider implements vscode.HoverProvider {
    provideHover(document: vscode.TextDocument, position: vscode.Position, token: vscode.CancellationToken): vscode.ProviderResult<vscode.Hover> {
        const range = document.getWordRangeAtPosition(position);
        if (!range) { return null; }

        const word = document.getText(range);

        // Create the "Command Palette" in Markdown
        const md = new vscode.MarkdownString();
        md.isTrusted = true;
        md.supportHtml = true; // Allow basic HTML if needed, but MD is safer for commands

        md.appendMarkdown(`### 🌌 Nexus AI\n`);
        md.appendMarkdown(`Target: \`${word}\`\n\n`);
        md.appendMarkdown(`---\n`);
        md.appendMarkdown(`[$(info) Explain](command:antigravity.explainCode) &nbsp; `);
        md.appendMarkdown(`[$(beaker) Tests](command:antigravity.generateTests) &nbsp; `);
        md.appendMarkdown(`[$(tools) Refactor](command:antigravity.refactorCode) &nbsp; `);
        md.appendMarkdown(`[$(comment-discussion) Custom...](command:antigravity.askGemini)`);

        return new vscode.Hover(md);
    }
}

async function handleCommand(service: GeminiService, promptPrefix: string) {
    const editor = vscode.window.activeTextEditor;
    if (!editor) { return; }

    const selection = editor.selection;
    const text = selection.isEmpty ? editor.document.getText(editor.document.getWordRangeAtPosition(selection.active)) : editor.document.getText(selection);

    if (!text) {
        vscode.window.showErrorMessage("No code selected or found at cursor.");
        return;
    }

    await service.streamResponse(`${promptPrefix}:\n\n${text}`);
}

async function handleCustomQuery(service: GeminiService) {
    const prompt = await vscode.window.showInputBox({ prompt: "Ask Gemini about your code..." });
    if (prompt) {
        await handleCommand(service, prompt);
    }
}

class GeminiService {
    private outputChannel: vscode.OutputChannel;

    constructor() {
        this.outputChannel = vscode.window.createOutputChannel("Antigravity Gemini");
    }

    async streamResponse(prompt: string) {
        const config = vscode.workspace.getConfiguration('antigravity.gemini');
        const apiKey = config.get<string>('apiKey');
        const model = config.get<string>('model') || 'gemini-pro';

        if (!apiKey) {
            vscode.window.showErrorMessage("Please set your Gemini API Key in Settings (antigravity.gemini.apiKey)");
            return;
        }

        this.outputChannel.show(true);
        this.outputChannel.appendLine(`\n➤ User: ${prompt.split('\n')[0]}...`);
        this.outputChannel.appendLine(`➤ Gemini: Thinking...`);

        try {
            const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`;

            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    contents: [{ parts: [{ text: prompt }] }]
                })
            });

            if (!response.ok) {
                throw new Error(`API Error: ${response.status} ${response.statusText}`);
            }

            const data = await response.json() as any;

            // Safety check for response structure
            if (data.candidates && data.candidates.length > 0 && data.candidates[0].content && data.candidates[0].content.parts) {
                const text = data.candidates[0].content.parts[0].text;
                this.outputChannel.appendLine(text);

                // Show a "success" notification
                vscode.window.setStatusBarMessage('$(check) Gemini response received', 3000);

            } else {
                this.outputChannel.appendLine("No response content from Gemini.");
            }

        } catch (error: any) {
            this.outputChannel.appendLine(`Error: ${error.message}`);
            vscode.window.showErrorMessage(`Gemini Request Failed: ${error.message}`);
        }
    }
}

export function deactivate() { }

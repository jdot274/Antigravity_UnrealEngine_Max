"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
const vscode = require("vscode");
const path = require("path");
const fs = require("fs");
const cp = require("child_process");
function activate(context) {
    const provider = new AntigravityRecorderViewProvider(context.extensionUri);
    context.subscriptions.push(vscode.window.registerWebviewViewProvider(AntigravityRecorderViewProvider.viewType, provider));
    context.subscriptions.push(vscode.commands.registerCommand('antigravity.startRecording', () => {
        provider.triggerRecording();
    }));
}
class AntigravityRecorderViewProvider {
    constructor(_extensionUri) {
        this._extensionUri = _extensionUri;
    }
    resolveWebviewView(webviewView, context, _token) {
        this._view = webviewView;
        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [
                this._extensionUri
            ]
        };
        webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);
        webviewView.webview.onDidReceiveMessage(data => {
            switch (data.type) {
                case 'startRecording':
                    {
                        vscode.window.showInformationMessage('Antigravity Recorder: Initializing Predictive Sequence...');
                        this.runPythonRecorder();
                        break;
                    }
            }
        });
    }
    triggerRecording() {
        if (this._view) {
            this._view.webview.postMessage({ type: 'triggerRecording' });
        }
    }
    runPythonRecorder() {
        // We will execute a python script that handles the ffmpeg recording
        // For now, we stub this out or call a script we are about to create.
        const pythonScriptPath = path.join(this._extensionUri.fsPath, 'resources', 'recorder.py');
        const pythonCommand = 'python3'; // Assume python3 is available
        // Check if script exists
        if (!fs.existsSync(pythonScriptPath)) {
            vscode.window.showErrorMessage(`Recorder script not found at ${pythonScriptPath}`);
            return;
        }
        const process = cp.spawn(pythonCommand, [pythonScriptPath], {
            detached: true,
            stdio: 'ignore'
        });
        process.unref();
        vscode.window.showInformationMessage('Recording Sequence Active (5m Increment).');
    }
    _getHtmlForWebview(webview) {
        return `<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Antigravity Recorder</title>
            <style>
                body {
                    margin: 0;
                    overflow: hidden;
                    background-color: #000;
                    font-family: 'Inter', sans-serif;
                }

                /* LAYER A: THE "REALITY" PASSTHROUGH (OLED BLACKS) */
                .reality-layer {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: radial-gradient(circle at 50% 50%, #1a1a1a 0%, #000 90%);
                    z-index: 0;
                    /* Abstract representation of a blurred night drive */
                    filter: blur(20px); 
                    opacity: 0.8;
                }
                
                /* Simulated street lights for the reality layer */
                .street-light {
                    position: absolute;
                    width: 100px;
                    height: 100px;
                    border-radius: 50%;
                    background: rgba(255, 200, 100, 0.1);
                    animation: drive-by 4s infinite linear;
                }

                @keyframes drive-by {
                    0% { transform: translate(-50%, -50%) scale(0.5); opacity: 0; top: 40%; left: 45%; }
                    20% { opacity: 0.5; }
                    100% { transform: translate(-200%, 100%) scale(4); opacity: 0; top: 100%; left: 0%; }
                }

                /* LAYER B: THE "LIVE SIM" OVERLAY */
                canvas {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    z-index: 10;
                }

                /* UI ELEMENTS */
                .hud-overlay {
                    position: absolute;
                    bottom: 40px;
                    left: 50%;
                    transform: translateX(-50%);
                    z-index: 20;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    pointer-events: none;
                }

                .pill-indicator {
                    background: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(10px);
                    padding: 8px 16px;
                    border-radius: 30px;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    color: rgba(255, 255, 255, 0.9);
                    font-size: 11px;
                    letter-spacing: 2px;
                    text-transform: uppercase;
                    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
                    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
                }

                .recording .pill-indicator {
                    background: rgba(255, 59, 48, 0.15);
                    border-color: rgba(255, 59, 48, 0.4);
                    color: #ff3b30;
                    box-shadow: 0 0 20px rgba(255, 59, 48, 0.2);
                }

                /* VISUAL HAPTIC ALERT */
                @keyframes haptic-shake {
                    0%, 100% { transform: translate(0, 0); }
                    10%, 30%, 50%, 70%, 90% { transform: translate(-2px, -1px); }
                    20%, 40%, 60%, 80% { transform: translate(2px, 1px); }
                }

                .alert-state {
                    animation: haptic-shake 0.4s cubic-bezier(.36,.07,.19,.97) both;
                }

            </style>
        </head>
        <body>
            <!-- Layer A: Reality Context -->
            <div class="reality-layer">
                <div class="street-light" style="animation-delay: 0s;"></div>
                <div class="street-light" style="animation-delay: 2s; right: 20%; left: auto;"></div>
            </div>

            <!-- Layer B: Sim Reconstruction -->
            <canvas id="sim-canvas"></canvas>

            <div class="hud-overlay">
                <div class="pill-indicator" id="status-pill">Safety Systems Active</div>
            </div>

            <script>
                const vscode = acquireVsCodeApi();
                const canvas = document.getElementById('sim-canvas');
                const ctx = canvas.getContext('2d');
                const pill = document.getElementById('status-pill');
                
                let width, height;
                let particles = [];
                let impulses = [];
                let isRecording = false;
                let frame = 0;

                // --- CONFIGURATION ---
                const ROAD_COLOR_SAFE = 'rgba(100, 200, 255, 0.2)';
                const ROAD_COLOR_RECORDING = 'rgba(255, 100, 100, 0.3)';
                const GLASS_GLOW = 'rgba(200, 240, 255, 0.6)';
                
                function resize() {
                    width = window.innerWidth;
                    height = window.innerHeight;
                    canvas.width = width;
                    canvas.height = height;
                }
                window.addEventListener('resize', resize);
                resize();

                // --- 1. GLASS ROAD PATHS ---
                function drawGlassRoad(yOffset, curvature, zIndex) {
                    ctx.beginPath();
                    
                    // Perspective road points
                    const startX = width * 0.5 + (curvature * 10);
                    const startY = height * 0.45; // Horizon line
                    const endX = width * 0.5 + (width * curvature); 
                    const endY = height; 

                    // Create Gradient for "Glass" effect
                    const grad = ctx.createLinearGradient(0, startY, 0, endY);
                    grad.addColorStop(0, 'rgba(255, 255, 255, 0.0)');
                    grad.addColorStop(0.2, 'rgba(255, 255, 255, 0.05)');
                    grad.addColorStop(1, 'rgba(255, 255, 255, 0.2)');

                    // Control points for smooth bezier curve
                    const cp1x = width * 0.5 + (curvature * 50);
                    const cp1y = height * 0.8;
                    const cp2x = endX;
                    const cp2y = height;

                    // Left Edge
                    ctx.moveTo(startX - 10 * zIndex, startY);
                    ctx.quadraticCurveTo(cp1x - 100 * zIndex, cp1y, endX - 300 * zIndex, endY);
                    
                    // Right Edge
                    ctx.lineTo(endX + 300 * zIndex, endY);
                    ctx.quadraticCurveTo(cp1x + 100 * zIndex, cp1y, startX + 10 * zIndex, startY);
                    
                    ctx.fillStyle = grad;
                    ctx.fill();

                    // Glass Edges (Neon/Glow)
                    ctx.strokeStyle = isRecording ? 'rgba(255, 50, 50, 0.5)' : GLASS_GLOW;
                    ctx.lineWidth = 2;
                    ctx.shadowBlur = 10;
                    ctx.shadowColor = isRecording ? '#ff3b30' : '#80d0ff';
                    ctx.stroke();
                    ctx.shadowBlur = 0;
                }

                // --- 2. LIDAR DOTS (DIGITAL RECONSTRUCTION) ---
                class LidarPoint {
                    constructor() {
                        this.init();
                    }
                    init() {
                        this.x = (Math.random() - 0.5) * width * 3;
                        this.y = height * 0.45; // Spawn at horizon
                        this.z = 0; // Perspective depth
                        this.speed = Math.random() * 0.02 + 0.005;
                    }
                    update() {
                        this.z += this.speed;
                        if(this.z > 1) this.init();
                    }
                    draw() {
                        const screenX = width/2 + (this.x / this.z) * 0.1;
                        const screenY = height/2 + ((this.y - height/2) / this.z) * 0.1;
                        
                        // Only draw if on bottom half
                        if (screenY < height * 0.45 || this.z < 0.1) return;

                        const size = 3 * this.z;
                        const alpha = this.z;

                        ctx.fillStyle = isRecording ? \`rgba(255, 50, 50, \${alpha})\` : \`rgba(200, 255, 255, \${alpha})\`;
                        ctx.beginPath();
                        ctx.arc(screenX, screenY, size, 0, Math.PI*2);
                        ctx.fill();
                    }
                }
                
                // --- 3. RAPID NEON PULSES (FAST MOVEMENTS) ---
                class NeonPulse {
                    constructor() {
                        this.progress = 0;
                        this.lane = Math.floor(Math.random() * 3) - 1; // -1, 0, 1
                    }
                    update() {
                        this.progress += 0.04; // FAST
                    }
                    draw() {
                        if (this.progress > 1) return;
                        
                        // Fake perspective calc simplified for speed
                        const startX = width/2;
                        const startY = height * 0.45;
                        const endX = width/2 + (this.lane * width * 0.4);
                        const endY = height * 1.2;

                        const curX = startX + (endX - startX) * this.progress;
                        const curY = startY + (endY - startY) * this.progress * this.progress; // Quadratic acceleration feel

                        ctx.fillStyle = '#fff';
                        ctx.shadowBlur = 20;
                        ctx.shadowColor = '#fff';
                        ctx.beginPath();
                        // Elongated streak for speed
                        ctx.ellipse(curX, curY, 40 * this.progress, 5 * this.progress, 0, 0, Math.PI*2);
                        ctx.fill();
                        ctx.shadowBlur = 0;
                    }
                }

                // Initialize Lidar
                for(let i=0; i<300; i++) particles.push(new LidarPoint());

                // Loop
                function animate() {
                    ctx.clearRect(0,0,width,height);
                    
                    // A. Reality Layer is HTML background
                    
                    // B. Draw Roads
                    drawGlassRoad(0, 0, 1.0); // Center
                    drawGlassRoad(0, -0.2, 0.3); // Left shoulder
                    drawGlassRoad(0, 0.2, 0.3); // Right shoulder

                    // C. Update & Draw Lidar
                    particles.forEach(p => { p.update(); p.draw(); });

                    // D. Impulses
                    if (Math.random() > 0.95 && isRecording) impulses.push(new NeonPulse()); // Rare normally, common on record?
                    if (Math.random() > 0.98 && !isRecording) impulses.push(new NeonPulse());

                    impulses = impulses.filter(p => p.progress <= 1);
                    impulses.forEach(p => { p.update(); p.draw(); });

                    requestAnimationFrame(animate);
                }
                animate();

                // INTERACTION
                // Mimic tapping the "Glass" to modify the sim state
                window.addEventListener('click', () => {
                    toggleRecording();
                });

                function toggleRecording() {
                    isRecording = !isRecording;
                    
                    // Haptic Visual Feedback
                    document.body.classList.remove('alert-state');
                    void document.body.offsetWidth; // trigger reflow
                    document.body.classList.add('alert-state');

                    if (isRecording) {
                        document.body.classList.add('recording');
                        pill.innerText = "CAPTURING INCIDENTS";
                        vscode.postMessage({ type: 'startRecording' });
                    } else {
                        document.body.classList.remove('recording');
                        pill.innerText = "SAFETY SYSTEMS ACTIVE";
                    }
                }

                // Listen for extension commands
                window.addEventListener('message', event => {
                    const message = event.data;
                    if (message.type === 'triggerRecording') {
                        toggleRecording();
                    }
                });
            </script>
        </body>
        </html>`;
    }
}
AntigravityRecorderViewProvider.viewType = 'antigravity.recorderView';
//# sourceMappingURL=extension.js.map
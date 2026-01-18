import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import * as cp from 'child_process';

export function activate(context: vscode.ExtensionContext) {
    const provider = new AntigravityRecorderViewProvider(context.extensionUri);

    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider(AntigravityRecorderViewProvider.viewType, provider)
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('antigravity.startRecording', () => {
            provider.triggerRecording();
        })
    );
}

class AntigravityRecorderViewProvider implements vscode.WebviewViewProvider {

    public static readonly viewType = 'antigravity.recorderView';
    private _view?: vscode.WebviewView;

    constructor(
        private readonly _extensionUri: vscode.Uri,
    ) { }

    public resolveWebviewView(
        webviewView: vscode.WebviewView,
        context: vscode.WebviewViewResolveContext,
        _token: vscode.CancellationToken,
    ) {
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

    public triggerRecording() {
        if (this._view) {
            this._view.webview.postMessage({ type: 'triggerRecording' });
        }
    }

    private runPythonRecorder() {
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

    private _getHtmlForWebview(webview: vscode.Webview) {
        // Load the Python-generated World Data
        const worldDataPath = path.join(this._extensionUri.fsPath, 'resources', 'world_data.json');
        let worldDataJson = 'null';
        try {
            if (fs.existsSync(worldDataPath)) {
                worldDataJson = fs.readFileSync(worldDataPath, 'utf8');
            }
        } catch (e) { console.error("Could not load world data", e); }

        return `<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Gravity AI</title>
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
                
                /* VIGNETTE for "FOCUSED SCENE" */
                .focus-vignette {
                    position: absolute;
                    top: 0; left: 0; right: 0; bottom: 0;
                    background: radial-gradient(circle at center, transparent 30%, rgba(0,0,0,0.8) 90%);
                    z-index: 15;
                    pointer-events: none;
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
            
            <!-- Focus Vignette -->
            <div class="focus-vignette"></div>

            <div class="hud-overlay">
                <div class="pill-indicator" id="status-pill">Safety Systems Active</div>
            </div>

            <script>
                const vscode = acquireVsCodeApi();
                const canvas = document.getElementById('sim-canvas');
                const ctx = canvas.getContext('2d');
                const pill = document.getElementById('status-pill');
                
                // Initialize World Data (from Python)
                const rawWorldData = ${worldDataJson}; 
                const worldSegments = rawWorldData ? rawWorldData.segments : [];
                const worldObjectsData = rawWorldData ? rawWorldData.objects : [];
                
                let width, height;
                let particles = [];
                let impulses = [];
                let isRecording = false;
                
                // Track Progress
                let travelDist = 0;
                let speed = 0.5;

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

                // --- 1. FOCUSED ROAD PATHS (Python Data Driven) ---
                function drawFocusedRoad(zIndex) {
                    // Find current segment index
                    const segmentIndex = Math.floor(travelDist) % (worldSegments.length || 1);
                    const curvature = worldSegments[segmentIndex] ? worldSegments[segmentIndex].curve : 0;
                    
                    ctx.beginPath();
                    
                    // Perspective: FOCUSED (Narrower FOV, Higher Horizon)
                    // The "Important Part" - Seeing the road clearly
                    const startX = width * 0.5 + (curvature * 20);
                    const startY = height * 0.45; // Horizon
                    const endX = width * 0.5 + (width * curvature * 1.5); 
                    const endY = height; 

                    // Create Gradient for "Glass" effect
                    const grad = ctx.createLinearGradient(0, startY, 0, endY);
                    grad.addColorStop(0, 'rgba(255, 255, 255, 0.0)');
                    grad.addColorStop(0.2, 'rgba(255, 255, 255, 0.1)'); // Brighter core
                    grad.addColorStop(1, 'rgba(255, 255, 255, 0.3)');

                    // Control points for smooth bezier curve
                    const cp1x = width * 0.5 + (curvature * 100);
                    const cp1y = height * 0.8;
                    const cp2x = endX;
                    const cp2y = height;
                    
                    // Road Width Scale (Non-linear perspective)
                    const wTop = 2 * zIndex;
                    const wBot = 150 * zIndex;

                    // Left Edge
                    ctx.moveTo(startX - wTop, startY);
                    ctx.quadraticCurveTo(cp1x - 50 * zIndex, cp1y, endX - wBot, endY);
                    
                    // Right Edge
                    ctx.lineTo(endX + wBot, endY);
                    ctx.quadraticCurveTo(cp1x + 50 * zIndex, cp1y, startX + wTop, startY);
                    
                    ctx.fillStyle = grad;
                    ctx.fill();

                    // Non-Mesh Wireframe Edges (Technical Look)
                    ctx.strokeStyle = isRecording ? 'rgba(255, 50, 50, 0.8)' : 'rgba(100, 240, 255, 0.8)';
                    ctx.lineWidth = 1;
                    ctx.shadowBlur = 15;
                    ctx.shadowColor = isRecording ? '#ff3b30' : '#00ffff';
                    ctx.stroke();
                    ctx.shadowBlur = 0;
                }

                // --- 2. LIDAR DOTS (DIGITAL RECONSTRUCTION) ---
                class LidarPoint {
                    constructor() {
                        this.init();
                    }
                    init() {
                        // Narrower spread for "Focused Scene"
                        this.x = (Math.random() - 0.5) * width * 1.5; 
                        this.y = height * 0.45; 
                        this.z = 0; 
                        this.speed = Math.random() * 0.02 + 0.005;
                    }
                    update() {
                        this.z += this.speed;
                        if(this.z > 1) this.init();
                    }
                    draw() {
                        const screenX = width/2 + (this.x / this.z) * 0.1;
                        const screenY = height/2 + ((this.y - height/2) / this.z) * 0.1;
                        
                        if (screenY < height * 0.45 || this.z < 0.1) return;

                        const size = 1 + (2 * this.z); // Smaller dots for precision
                        const alpha = this.z;

                        ctx.fillStyle = isRecording ? `rgba(255, 50, 50, ${ alpha })` : `rgba(200, 255, 255, ${ alpha })`;
                        ctx.beginPath();
                        ctx.arc(screenX, screenY, size, 0, Math.PI*2);
                        ctx.fill();
                    }
                }
                
                // --- 3. RAPID NEON PULSES (FAST MOVEMENTS) ---
                class NeonPulse {
                    constructor() {
                        this.progress = 0;
                        this.lane = Math.floor(Math.random() * 3) - 1; 
                    }
                    update() {
                        this.progress += 0.04; 
                    }
                    draw() {
                        if (this.progress > 1) return;
                        
                        const startX = width/2;
                        const startY = height * 0.45;
                        const endX = width/2 + (this.lane * width * 0.2); // Tighter lane spread
                        const endY = height * 1.2;

                        const curX = startX + (endX - startX) * this.progress;
                        const curY = startY + (endY - startY) * this.progress * this.progress; 

                        ctx.fillStyle = '#fff';
                        ctx.shadowBlur = 20;
                        ctx.shadowColor = '#fff';
                        ctx.beginPath();
                        ctx.ellipse(curX, curY, 40 * this.progress, 3 * this.progress, 0, 0, Math.PI*2);
                        ctx.fill();
                        ctx.shadowBlur = 0;
                    }
                }

                // --- 5. INTERACTIVE WINDOWS & FIELD HIGHLIGHTING ---
                // "User not passenger... initiates new windows and highlights needed fields"
                class DataWindow {
                    constructor(id, x, y, title) {
                        this.id = id;
                        this.x = x;
                        this.y = y;
                        this.width = 0;
                        this.targetWidth = 180;
                        this.height = 0;
                        this.targetHeight = 100;
                        this.isOpen = false;
                        this.isHighlighted = false;
                    }

                    toggle() {
                        this.isOpen = !this.isOpen;
                    }

                    highlight() {
                        this.isHighlighted = true;
                        setTimeout(() => { this.isHighlighted = false; }, 2000);
                    }

                    update() {
                        // Smooth open/close ani
                        const speed = 0.2;
                        if (this.isOpen) {
                            this.width += (this.targetWidth - this.width) * speed;
                            this.height += (this.targetHeight - this.height) * speed;
                        } else {
                            this.width += (0 - this.width) * speed;
                            this.height += (0 - this.height) * speed;
                        }
                    }

                    draw() {
                        if (this.width < 1) return;

                        ctx.save();
                        ctx.translate(this.x, this.y);

                        // Window Glass Background
                        ctx.fillStyle = 'rgba(10, 20, 30, 0.7)';
                        ctx.strokeStyle = this.isHighlighted ? '#ffcc00' : 'rgba(100, 200, 255, 0.5)';
                        ctx.lineWidth = this.isHighlighted ? 3 : 1;
                        
                        // Glow if highlighted (Attention needed)
                        if (this.isHighlighted) {
                            ctx.shadowBlur = 20;
                            ctx.shadowColor = '#ffcc00';
                        }

                        // Draw Rect
                        ctx.beginPath();
                        ctx.roundRect(-this.width/2, -this.height/2, this.width, this.height, 10);
                        ctx.fill();
                        ctx.stroke();
                        
                        // Header Line
                        ctx.beginPath();
                        ctx.moveTo(-this.width/2 + 10, -this.height/2 + 20);
                        ctx.lineTo(this.width/2 - 10, -this.height/2 + 20);
                        ctx.strokeStyle = 'rgba(255,255,255,0.2)';
                        ctx.lineWidth = 1;
                        ctx.stroke();

                        // Mock Data Lines
                        ctx.fillStyle = this.isHighlighted ? '#ffcc00' : 'rgba(200, 255, 255, 0.8)';
                        ctx.font = '10px Inter';
                        ctx.fillText(this.id, -this.width/2 + 15, -this.height/2 + 14); // Title

                        if (this.height > 60) {
                            ctx.fillStyle = 'rgba(255,255,255,0.5)';
                            ctx.fillText("STATUS: ACTIVE", -this.width/2 + 15, 0);
                            ctx.fillText("LINK: UNREAL ENGINE", -this.width/2 + 15, 15);
                            ctx.fillText("LATENCY: 4ms", -this.width/2 + 15, 30);
                        }

                        ctx.restore();
                    }
                }

                const windows = [
                    new DataWindow("TELEMETRY", width * 0.2, height * 0.5, "TELEMETRY"),
                    new DataWindow("UE5 LINK", width * 0.8, height * 0.5, "UNREAL BRIDGE")
                ];

                // --- 7. REAL WEATHER SIMULATION ---
                // "Simulates the real weather"
                class WeatherParticle {
                    constructor(type) {
                        this.type = type; // 'rain', 'snow'
                        this.init();
                    }

                    init() {
                        this.x = (Math.random() - 0.5) * width;
                        this.y = (Math.random() - 0.5) * height;
                        this.z = Math.random() * 2; // Depth
                        this.speed = 0.05 + Math.random() * 0.1;
                    }

                    update() {
                        this.z -= this.speed;
                        if (this.z <= 0) this.init();
                    }

                    draw() {
                        const x = width/2 + (this.x / this.z);
                        const y = height/2 + (this.y / this.z);
                        
                        // Don't draw if out of bounds
                        if (x < 0 || x > width || y < 0 || y > height) return;

                        ctx.beginPath();
                        ctx.strokeStyle = 'rgba(150, 200, 255, 0.4)';
                        ctx.lineWidth = 1 / this.z;
                        
                        // Rain Streak effect (radial from center)
                        const len = 20 / this.z;
                        const angle = Math.atan2(y - height/2, x - width/2);
                        
                        ctx.moveTo(x, y);
                        ctx.lineTo(x + Math.cos(angle) * len, y + Math.sin(angle) * len);
                        ctx.stroke();
                    }
                }

                class WeatherSystem {
                    constructor() {
                        this.particles = [];
                        this.condition = 'rain'; // 'clear', 'rain', 'storm'
                        for(let i=0; i<100; i++) this.particles.push(new WeatherParticle('rain'));
                    }

                    draw() {
                        // Dynamic Weather Change (Simulation)
                        if (Math.random() > 0.999) {
                            this.condition = Math.random() > 0.5 ? 'rain' : 'storm';
                        }
                        
                        // Fog Layer
                        if (this.condition === 'storm') {
                             const grad = ctx.createLinearGradient(0, 0, 0, height);
                             grad.addColorStop(0, 'rgba(20, 30, 40, 0.4)');
                             grad.addColorStop(1, 'rgba(0,0,0,0)');
                             ctx.fillStyle = grad;
                             ctx.fillRect(0,0,width,height);
                        }

                        this.particles.forEach(p => {
                            p.speed = this.condition === 'storm' ? 0.2 : 0.05;
                            p.update();
                            p.draw();
                        });
                    }
                }
                const weather = new WeatherSystem();

                // --- 6. 3D WORLD OBJECTS (FROM PYTHON DATA) ---
                // "Fake non mesh designs" - Wireframes
                class WorldObject {
                    constructor(data) {
                        this.data = data; // {z, x, width, height...}
                        this.z = data.z - travelDist; // Relative z
                    }
                    
                    update() {
                        // Recalculate z based on total travel distance
                        const relativeZ = this.data.z - travelDist;
                        this.z = relativeZ;
                        
                        // Loop around for infinite track illusion if we run out of data
                        // (Simple modulo logic)
                    }
                    
                    draw() {
                        // Only draw if in front of camera (z > 0) and close enough
                        // Scale down Z to fit 0-1 range for projection logic or adapt logic
                        // Here map world Z to screen projection Z
                        
                        let renderZ = (50 - this.z) / 50; // Inverted: As distance decreases, renderZ approaches 1?
                        // Actually let's stick to the previous simple projection: Z starts high, goes to 0
                        // Z = Relative Distance. 
                        
                        // Simplification for the "Infinite Loop" feel using the Python data as a template:
                        // We will instanciate NEW objects based on the Python Templates spawning in the distance.
                    }
                }
                
                // Procedural Spawner based on Python Data
                const activeObjects = [];
                function spawnWorldObjects() {
                     // Check if we need to spawn new objects at the horizon
                     // Simplified: Just keep a pool of objects that follow the Python data patterns randomly
                }

                // Temporary: Simple Wireframe Boxes (The "Non Mesh" Look)
                 class ProceduralObject {
                    constructor() {
                        this.init();
                    }
                    
                    init() {
                        this.x = (Math.random() - 0.5) * width * 4; 
                        if (Math.abs(this.x) < width * 0.2) this.x += (this.x > 0 ? width*0.3 : -width*0.3);
                        this.z = 0; 
                        this.y = height * 0.45; 
                        this.width = 50 + Math.random() * 50;
                        this.height = 100 + Math.random() * 200;
                        this.speed = 0.005;
                    }
                    
                    update() {
                        this.z += this.speed;
                        this.speed *= 1.02; 
                        if (this.z > 1.2) this.init();
                    }
                    
                    draw() {
                        if (this.z < 0.01) return;
                        
                        const scale = this.z;
                        const screenX = width/2 + (this.x / this.z) * 0.1;
                        const screenY = height/2 + ((this.y - height/2) / this.z) * 0.1;
                        
                        const w = this.width * scale * 2;
                        const h = this.height * scale * 2;
                        const bottomY = screenY;
                        const topY = screenY - h;
                        
                        // Fake Non Mesh = WIREFRAME ONLY
                        ctx.strokeStyle = isRecording ? 'rgba(255, 50, 50, 0.4)' : 'rgba(100, 200, 255, 0.3)';
                        ctx.lineWidth = 1;
                        ctx.fillStyle = 'rgba(0,0,0,0)'; // Transparent fill
                        
                        ctx.beginPath();
                        ctx.moveTo(screenX - w/2, bottomY);
                        ctx.lineTo(screenX + w/2, bottomY);
                        ctx.lineTo(screenX + w/2, topY);
                        ctx.lineTo(screenX - w/2, topY);
                        ctx.closePath();
                        ctx.stroke();
                        
                        // Internal diagonals for "Technical" look
                        ctx.beginPath();
                        ctx.moveTo(screenX - w/2, bottomY);
                        ctx.lineTo(screenX + w/2, topY);
                        ctx.moveTo(screenX + w/2, bottomY);
                        ctx.lineTo(screenX - w/2, topY);
                        ctx.strokeStyle = 'rgba(255,255,255,0.1)';
                        ctx.stroke();
                    }
                }
                const proceduralObjects = [];
                for(let i=0; i<30; i++) proceduralObjects.push(new ProceduralObject());


                // --- 4. SAFETY CORE (UNWAVERING + UE STATUS) ---
                class SafetyCore {
                    constructor() {
                        this.pulse = 0;
                    }
                    draw() {
                        const time = Date.now() / 1000;
                        const heartBeat = Math.abs(Math.sin(time * 2)); 
                        
                        ctx.beginPath();
                        ctx.arc(width/2, height * 0.85, 40 + (heartBeat * 4), 0, Math.PI*2);
                        
                        const color = isRecording ? 'rgba(255, 59, 48, 0.3)' : 'rgba(50, 255, 100, 0.1)';
                        const glow = isRecording ? 'rgba(255, 59, 48, 0.6)' : 'rgba(50, 255, 100, 0.3)';
                        
                        const grad = ctx.createRadialGradient(width/2, height * 0.85, 10, width/2, height * 0.85, 60);
                        grad.addColorStop(0, glow);
                        grad.addColorStop(1, 'rgba(0,0,0,0)');
                        
                        ctx.fillStyle = grad;
                        ctx.fill();
                        
                        ctx.strokeStyle = glow;
                        ctx.lineWidth = 2;
                        ctx.beginPath();
                        ctx.moveTo(width/2 - 20, height * 0.85);
                        ctx.lineTo(width/2 + 20, height * 0.85);
                        ctx.stroke();
                        
                        // Text Label below
                        ctx.fillStyle = 'rgba(255,255,255,0.4)';
                        ctx.textAlign = 'center';
                        ctx.fillText("GRAVITY CORE", width/2, height * 0.85 + 60);
                    }
                }
                const safetyCore = new SafetyCore();

                // Initialize Lidar
                for(let i=0; i<NUM_PARTICLES; i++) particles.push(new LidarPoint());

                // Loop
                function animate() {
                    ctx.clearRect(0,0,width,height);
                    
                    // Update global progress
                    travelDist += speed;

                    // A. Reality Layer (Background)
                    
                    // B. Focused Road (Safety Critical)
                    drawFocusedRoad(1.0); 
                    drawFocusedRoad(0.3); // Shoulder
                    
                    // C. Wireframe World (Background)
                    proceduralObjects.forEach(obj => { obj.update(); obj.draw(); });
                    
                    // Draw Weather
                    weather.draw();

                    // Draw Safety Core
                    safetyCore.draw();

                    // D. Lidar (Data)
                    if (Math.random() > 0.05) { 
                        particles.forEach(p => { p.update(); p.draw(); });
                    }

                    // E. Windows
                    windows.forEach(w => { w.x = w.id === "TELEMETRY" ? width*0.15 : width*0.85; w.update(); w.draw(); });

                    // F. Impulses
                    if (Math.random() > 0.95 && isRecording) impulses.push(new NeonPulse()); 
                    if (Math.random() > 0.98 && !isRecording) impulses.push(new NeonPulse());

                    impulses = impulses.filter(p => p.progress <= 1);
                    impulses.forEach(p => { p.update(); p.draw(); });

                    requestAnimationFrame(animate);
                }
                animate();

                // INTERACTION
                window.addEventListener('click', (e) => {
                    // Check if clicked windows (simplified collision)
                    // If clicked center, toggle record. If side, toggle window.
                    if (e.clientX < width * 0.3) {
                        windows[0].toggle();
                        if(windows[0].isOpen) windows[0].highlight();
                        return;
                    }
                    if (e.clientX > width * 0.7) {
                        windows[1].toggle();
                        if(windows[1].isOpen) windows[1].highlight();
                        return;
                    }

                    toggleRecording();
                });

                function toggleRecording() {
                    isRecording = !isRecording;
                    
                    // Haptic Visual Feedback - INSTANT
                    document.body.classList.remove('alert-state');
                    void document.body.offsetWidth; // trigger reflow
                    document.body.classList.add('alert-state');

                    if (isRecording) {
                        document.body.classList.add('recording');
                        pill.innerText = "RECORDING SCENE [UNREAL LINKED]";
                        vscode.postMessage({ type: 'startRecording' });
                        // Simulate "User Attention" needed
                        windows[0].isOpen = true;
                        windows[0].highlight();
                    } else {
                        document.body.classList.remove('recording');
                        pill.innerText = "SYSTEM IDLE";
                        windows[0].isOpen = false;
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

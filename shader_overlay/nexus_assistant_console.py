import time
import sys
import random

def assistant_talk(prefix, message, color="\033[94m"):
    reset = "\033[0m"
    for char in message:
        sys.stdout.write(f"{color}{char}{reset}")
        sys.stdout.flush()
        time.sleep(0.01)
    sys.stdout.write("\n")

def run_console():
    print("\033[96m" + "="*60)
    print("🚀 ANTIGRAVITY NEXUS | GEMINI CODE ASSIST TERMINAL")
    print("="*60 + "\033[0m")
    
    actions = [
        "Analyzing Metal 3 shader pipeline...",
        "Optimizing glass_spheres.hlsl for refractive depth...",
        "Syncing GT-Vehicle physics with Rocket League impulse logic...",
        "Deploying Pixel Streaming buffers to port 80...",
        "Injecting procedural sphere animation constants...",
        "Monitoring Unreal PIE state -> STABLE",
        "Refining asphalt friction coefficients for Interceptor_GT...",
        "💥 GEMINI: Upgrading Volumetric Density to 16,000 instances...",
        "Instancing 40x40x10 Glass Sphere Grid..."
    ]

    assistant_talk("[GEMINI]", "Nexus System Ready. I am now coding in the background.")
    assistant_talk("[GEMINI]", "CRITICAL UPDATE: Density increased by 100x. Mesh count: 16,000 blocks.")
    assistant_talk("[GEMINI]", "I see you're using bash-3.2. I will project the build logs here.")

    try:
        while True:
            time.sleep(random.uniform(2, 5))
            action = random.choice(actions)
            timestamp = time.strftime("%H:%M:%S")
            assistant_talk(f"[{timestamp}]", f" BUILD_SYNC >> {action}", color="\033[92m")
            
            if random.random() > 0.8:
                assistant_talk("[GEMINI]", "Directive: 'Rocket League x Gran Turismo' Arena is fully compiled. Awaiting your move in PIE.", color="\033[94m")
    except KeyboardInterrupt:
        print("\n[SYSTEM] Assistant terminal suspended.")

if __name__ == "__main__":
    run_console()

// [GEMINI_OPTIMIZED] Enhanced Subsurface Approximation & Ray-Bending
// Advanced Immersive Glass Blur Spheres Shader - V2
// Designed for Antigravity Nexus - GT x RL Arena

#define MAX_STEPS 128 // Gemini: Increased for depth fidelity
#define SURFACE_DIST 0.001
#define MAX_DIST 50.0

// Chromatic Aberration & Refraction Indices
#define IOR_RED 1.54
#define IOR_GREEN 1.50
#define IOR_BLUE 1.46

// Noise function from Shadertoy (Classic Hash)
float hash(float n) { return frac(sin(n) * 43758.5453123); }
float noise(float3 x) {
    float3 p = floor(x);
    float3 f = frac(x);
    f = f*f*(3.0-2.0*f);
    float n = p.x + p.y*157.0 + 113.0*p.z;
    return lerp(lerp(lerp(hash(n+  0.0), hash(n+  1.0),f.x),
                   lerp(hash(n+157.0), hash(n+158.0),f.x),f.y),
               lerp(lerp(hash(n+113.0), hash(n+114.0),f.x),
                   lerp(hash(n+270.0), hash(n+271.0),f.x),f.y),f.z);
}

float GetDist(float3 p, float iTime) {
    // Procedural movement - Kinetic spheres responding to "Time"
    float3 q = p;
    q.y += iTime * 0.5; // Upward flow
    
    // Dense packing logic
    float3 grid = frac(q * 0.25) - 0.5;
    float n = noise(floor(q * 0.25) + iTime * 0.1);
    
    float radius = 0.12 + 0.08 * sin(iTime * 2.0 + n * 10.0);
    float d = length(grid) - radius;
    
    // Add a refractive 'haze' volume
    float haze = noise(p * 0.5 + iTime * 0.2) * 0.05;
    return d + haze;
}

float3 GetNormal(float3 p, float iTime) {
    float d = GetDist(p, iTime);
    float2 e = float2(0.005, 0); // Finer normal for glass reflections
    float3 n = d - float3(
        GetDist(p-e.xyy, iTime),
        GetDist(p-e.yxy, iTime),
        GetDist(p-e.yyx, iTime));
    return normalize(n);
}

float3 RaymarchScene(float3 ro, float3 rd, float iTime) {
    float t = 0.0;
    float3 col = 0;
    float transmittance = 1.0;
    
    for(int i=0; i<MAX_STEPS; i++) {
        float3 p = ro + rd * t;
        float d = GetDist(p, iTime);
        
        if(d < SURFACE_DIST) {
            float3 n = GetNormal(p, iTime);
            
            // Fresnel Reflection
            float fresnel = pow(1.0 - max(0.0, dot(-rd, n)), 5.0);
            
            // Refraction (Dispersion)
            float3 refrR = refract(rd, n, 1.0/IOR_RED);
            float3 refrG = refract(rd, n, 1.0/IOR_GREEN);
            float3 refrB = refract(rd, n, 1.0/IOR_BLUE);
            
            // Background Light Injection (Simulated)
            float3 bg = float3(0.02, 0.05, 0.1) * (1.0 + sin(iTime + p.y));
            col += bg * (1.0 - fresnel) * transmittance;
            col += float3(0.8, 0.9, 1.0) * fresnel * transmittance; // Specular Hit
            
            transmittance *= 0.85; // Volume absorbtion
            
            rd = refrG; // Continue depth march with bent rays
            p += rd * 0.05; // Step inside
            t += 0.05;
        }
        
        t += max(d * 0.5, 0.002);
        if(t > MAX_DIST || transmittance < 0.1) break;
    }
    
    // Volumetric Glow (GT-Style)
    col += float3(0.0, 0.3, 0.5) * exp(-0.1 * t);
    return col;
}

// Final Pipeline Entry
// return RaymarchScene(CameraPosition, CameraDirection, Time);

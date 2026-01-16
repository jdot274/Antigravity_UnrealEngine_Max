#version 330
uniform float iTime;
uniform vec2 iResolution;
out vec4 fragColor;

void main() {
    vec2 uv = (gl_FragCoord.xy - 0.5 * iResolution.xy) / iResolution.y;
    float time = iTime * 0.15;
    
    vec3 finalColor = vec3(0.0);
    
    for (float i = 0.0; i < 4.0; i++) {
        uv = abs(uv) - 0.5;
        float angle = iTime * 0.1 + i * 0.8;
        mat2 rot = mat2(cos(angle), -sin(angle), sin(angle), cos(angle));
        uv = rot * uv;
        
        float d = length(uv) * exp(-length(uv));
        vec3 col = vec3(0.1, 0.4, 0.9) * 0.5 + 0.5 * cos(iTime + i * 2.0 + vec3(0, 2, 4));
        
        d = sin(d * 8.0 + iTime) / 8.0;
        d = abs(d);
        d = pow(0.01 / d, 1.2);
        
        finalColor += col * d;
    }
    
    fragColor = vec4(finalColor * 0.6, 1.0);
}

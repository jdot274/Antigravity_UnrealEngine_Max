// Antigravity Nexus - 3D Scene Controller
import * as THREE from 'https://cdn.skypack.dev/three@0.136.0';

class NexusScene {
    constructor(container) {
        this.container = container;
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        this.objects = [];
        this.mouse = { x: 0, y: 0 };

        this.init();
    }

    init() {
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        this.container.appendChild(this.renderer.domElement);

        this.camera.position.z = 8;

        this.createLights();
        this.createGeometry();
        this.createParticles();

        this.bindEvents();
        this.animate();
    }

    createLights() {
        const ambient = new THREE.AmbientLight(0x404040, 0.5);
        this.scene.add(ambient);

        const point1 = new THREE.PointLight(0x00f0ff, 2, 50);
        point1.position.set(10, 10, 10);
        this.scene.add(point1);

        const point2 = new THREE.PointLight(0x8b5cf6, 2, 50);
        point2.position.set(-10, -10, 5);
        this.scene.add(point2);
    }

    createGeometry() {
        // Golf ball (icosphere)
        const ballGeo = new THREE.IcosahedronGeometry(1.5, 2);
        const ballMat = new THREE.MeshPhongMaterial({
            color: 0x00f0ff,
            wireframe: true,
            transparent: true,
            opacity: 0.6
        });
        const ball = new THREE.Mesh(ballGeo, ballMat);
        ball.position.set(-4, 1, -5);
        this.scene.add(ball);
        this.objects.push({ mesh: ball, rotSpeed: { x: 0.003, y: 0.005 }, floatOffset: 0 });

        // Fairway platform
        const platformGeo = new THREE.BoxGeometry(6, 0.3, 12);
        const platformMat = new THREE.MeshPhongMaterial({
            color: 0x8b5cf6,
            wireframe: true,
            transparent: true,
            opacity: 0.4
        });
        const platform = new THREE.Mesh(platformGeo, platformMat);
        platform.position.set(4, -2, -8);
        platform.rotation.z = 0.15;
        this.scene.add(platform);
        this.objects.push({ mesh: platform, rotSpeed: { x: 0.001, y: 0.002 }, floatOffset: 1 });

        // Floating torus rings
        for (let i = 0; i < 4; i++) {
            const torusGeo = new THREE.TorusGeometry(2 + i * 1.5, 0.08, 8, 64);
            const torusMat = new THREE.MeshPhongMaterial({
                color: i % 2 === 0 ? 0x00f0ff : 0xec4899,
                wireframe: true,
                transparent: true,
                opacity: 0.3
            });
            const torus = new THREE.Mesh(torusGeo, torusMat);
            torus.position.set(0, 0, -15 - i * 4);
            torus.rotation.x = Math.PI / 2;
            this.scene.add(torus);
            this.objects.push({ mesh: torus, rotSpeed: { x: 0, y: 0.005 + i * 0.002 }, floatOffset: i * 0.5 });
        }

        // Flag cone
        const flagGeo = new THREE.ConeGeometry(0.5, 1.5, 4);
        const flagMat = new THREE.MeshPhongMaterial({
            color: 0xec4899,
            wireframe: true,
            transparent: true,
            opacity: 0.7
        });
        const flag = new THREE.Mesh(flagGeo, flagMat);
        flag.position.set(2, 3, -6);
        this.scene.add(flag);
        this.objects.push({ mesh: flag, rotSpeed: { x: 0.005, y: 0.008 }, floatOffset: 2 });
    }

    createParticles() {
        const particleCount = 200;
        const positions = new Float32Array(particleCount * 3);

        for (let i = 0; i < particleCount * 3; i += 3) {
            positions[i] = (Math.random() - 0.5) * 50;
            positions[i + 1] = (Math.random() - 0.5) * 50;
            positions[i + 2] = (Math.random() - 0.5) * 50;
        }

        const geometry = new THREE.BufferGeometry();
        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

        const material = new THREE.PointsMaterial({
            color: 0x00f0ff,
            size: 0.1,
            transparent: true,
            opacity: 0.6
        });

        this.particles = new THREE.Points(geometry, material);
        this.scene.add(this.particles);
    }

    bindEvents() {
        window.addEventListener('resize', () => this.onResize());
        window.addEventListener('mousemove', (e) => this.onMouseMove(e));
    }

    onResize() {
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
    }

    onMouseMove(event) {
        this.mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
        this.mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
    }

    animate() {
        requestAnimationFrame(() => this.animate());

        const time = Date.now() * 0.001;

        // Animate objects
        this.objects.forEach((obj, i) => {
            obj.mesh.rotation.x += obj.rotSpeed.x;
            obj.mesh.rotation.y += obj.rotSpeed.y;
            obj.mesh.position.y += Math.sin(time + obj.floatOffset) * 0.003;
        });

        // Animate particles
        if (this.particles) {
            this.particles.rotation.y += 0.0002;
        }

        // Mouse parallax
        this.camera.position.x += (this.mouse.x * 0.5 - this.camera.position.x) * 0.05;
        this.camera.position.y += (this.mouse.y * 0.5 - this.camera.position.y) * 0.05;
        this.camera.lookAt(this.scene.position);

        this.renderer.render(this.scene, this.camera);
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('canvas-container');
    if (container) {
        window.nexusScene = new NexusScene(container);
    }
});

export { NexusScene };

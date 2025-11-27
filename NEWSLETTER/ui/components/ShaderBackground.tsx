"use client";

import { useRef, useMemo } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { Mesh } from "three";
import * as THREE from "three";

/**
 * Shader de fundo reativo ao mouse
 * Cria um efeito de ondas digitais/starfield distorcido
 */
function ShaderPlane() {
  const meshRef = useRef<Mesh>(null);
  const mouseRef = useRef({ x: 0, y: 0 });

  // Shader material customizado
  const shaderMaterial = useMemo(
    () =>
      new THREE.ShaderMaterial({
        uniforms: {
          uTime: { value: 0 },
          uMouse: { value: new THREE.Vector2(0, 0) },
          uResolution: { value: new THREE.Vector2(window.innerWidth, window.innerHeight) },
        },
        vertexShader: `
          varying vec2 vUv;
          
          void main() {
            vUv = uv;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
          }
        `,
        fragmentShader: `
          uniform float uTime;
          uniform vec2 uMouse;
          uniform vec2 uResolution;
          varying vec2 vUv;
          
          // Noise function
          float random(vec2 st) {
            return fract(sin(dot(st.xy, vec2(12.9898,78.233))) * 43758.5453123);
          }
          
          float noise(vec2 st) {
            vec2 i = floor(st);
            vec2 f = fract(st);
            float a = random(i);
            float b = random(i + vec2(1.0, 0.0));
            float c = random(i + vec2(0.0, 1.0));
            float d = random(i + vec2(1.0, 1.0));
            vec2 u = f * f * (3.0 - 2.0 * f);
            return mix(a, b, u.x) + (c - a)* u.y * (1.0 - u.x) + (d - b) * u.x * u.y;
          }
          
          void main() {
            vec2 st = vUv;
            vec2 mouse = uMouse * 0.5 + 0.5;
            
            // Distância do mouse
            float dist = distance(st, mouse);
            
            // Ondas digitais
            float wave1 = sin(st.x * 10.0 + uTime * 0.5) * 0.5 + 0.5;
            float wave2 = sin(st.y * 10.0 - uTime * 0.3) * 0.5 + 0.5;
            float waves = wave1 * wave2;
            
            // Noise animado
            vec2 noiseCoord = st * 3.0 + uTime * 0.1;
            float n = noise(noiseCoord);
            
            // Starfield effect
            float stars = step(0.98, random(floor(st * 100.0)));
            stars *= sin(uTime * 2.0 + random(floor(st * 100.0)) * 6.28) * 0.5 + 0.5;
            
            // Gradiente base (void escuro)
            vec3 color1 = vec3(0.012, 0.012, 0.02); // #030305
            vec3 color2 = vec3(0.039, 0.039, 0.059); // void-light
            vec3 baseColor = mix(color1, color2, st.y);
            
            // Electric blue e purple
            vec3 electricBlue = vec3(0.231, 0.510, 0.965); // #3B82F6
            vec3 cyberPurple = vec3(0.545, 0.361, 0.965); // #8B5CF6
            
            // Efeito de mouse
            float mouseEffect = smoothstep(0.5, 0.0, dist);
            vec3 mouseGlow = mix(electricBlue, cyberPurple, sin(uTime) * 0.5 + 0.5);
            
            // Combinar tudo
            vec3 finalColor = baseColor;
            finalColor += waves * 0.02;
            finalColor += n * 0.03;
            finalColor += stars * 0.3;
            finalColor += mouseGlow * mouseEffect * 0.15;
            
            // Vinheta sutil
            float vignette = smoothstep(1.0, 0.3, dist);
            finalColor *= vignette * 0.5 + 0.5;
            
            gl_FragColor = vec4(finalColor, 1.0);
          }
        `,
      }),
    []
  );

  // Atualizar uniforms a cada frame
  useFrame((state) => {
    if (meshRef.current) {
      const material = meshRef.current.material as THREE.ShaderMaterial;
      material.uniforms.uTime.value = state.clock.elapsedTime;
      material.uniforms.uMouse.value.set(mouseRef.current.x, mouseRef.current.y);
    }
  });

  // Mouse move handler
  if (typeof window !== "undefined") {
    window.addEventListener("mousemove", (e) => {
      mouseRef.current.x = (e.clientX / window.innerWidth) * 2 - 1;
      mouseRef.current.y = -(e.clientY / window.innerHeight) * 2 + 1;
    });
  }

  return (
    <mesh ref={meshRef}>
      <planeGeometry args={[10, 10, 1, 1]} />
      <primitive object={shaderMaterial} attach="material" />
    </mesh>
  );
}

/**
 * Componente de background com shader WebGL
 */
export default function ShaderBackground() {
  return (
    <div className="fixed inset-0 -z-10">
      <Canvas
        camera={{ position: [0, 0, 5], fov: 45 }}
        dpr={[1, 2]}
        gl={{ antialias: false, alpha: false }}
      >
        <ShaderPlane />
      </Canvas>
    </div>
  );
}

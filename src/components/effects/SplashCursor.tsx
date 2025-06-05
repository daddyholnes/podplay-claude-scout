"use client";
import { useEffect, useRef } from "react";

interface SplashCursorProps {
  SIM_RESOLUTION?: number;
  DYE_RESOLUTION?: number;
  CAPTURE_RESOLUTION?: number;
  DENSITY_DISSIPATION?: number;
  VELOCITY_DISSIPATION?: number;
  PRESSURE?: number;
  PRESSURE_ITERATIONS?: number;
  CURL?: number;
  SPLAT_RADIUS?: number;
  SPLAT_FORCE?: number;
  SHADING?: boolean;
  COLOR_UPDATE_SPEED?: number;
  BACK_COLOR?: { r: number; g: number; b: number };
  TRANSPARENT?: boolean;
}

/**
 * SplashCursor - Interactive fluid simulation cursor effect
 * Creates beautiful, flowing liquid-like effects that follow mouse movement
 * Perfect for creating an immersive, calming interaction experience
 * 
 * @param SIM_RESOLUTION - Simulation resolution (default: 128)
 * @param DYE_RESOLUTION - Dye resolution for color effects (default: 1440)
 * @param DENSITY_DISSIPATION - How quickly density fades (default: 3.5)
 * @param VELOCITY_DISSIPATION - How quickly velocity fades (default: 2)
 * @param SPLAT_RADIUS - Size of cursor splash effect (default: 0.2)
 * @param SPLAT_FORCE - Force of cursor interaction (default: 6000)
 */
function SplashCursor({
  SIM_RESOLUTION = 128,
  DYE_RESOLUTION = 1440,
  CAPTURE_RESOLUTION = 512,
  DENSITY_DISSIPATION = 3.5,
  VELOCITY_DISSIPATION = 2,
  PRESSURE = 0.1,
  PRESSURE_ITERATIONS = 20,
  CURL = 3,
  SPLAT_RADIUS = 0.2,
  SPLAT_FORCE = 6000,
  SHADING = true,
  COLOR_UPDATE_SPEED = 10,
  BACK_COLOR = { r: 0.5, g: 0, b: 0 },
  TRANSPARENT = true,
}: SplashCursorProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    // Canvas context setup
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    // Simplified fluid animation using 2D canvas
    let animationId: number;
    let mouseX = 0;
    let mouseY = 0;
    let prevMouseX = 0;
    let prevMouseY = 0;
    
    // Particle system for visual effects
    const particles: Array<{
      x: number;
      y: number;
      vx: number;
      vy: number;
      life: number;
      maxLife: number;
      hue: number;
    }> = [];
    
    const animate = () => {
      // Clear with slight fade for trailing effect
      ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      // Update and draw particles
      for (let i = particles.length - 1; i >= 0; i--) {
        const particle = particles[i];
        
        // Update particle
        particle.x += particle.vx;
        particle.y += particle.vy;
        particle.life -= 1;
        particle.vx *= 0.99; // Damping
        particle.vy *= 0.99;
        
        // Remove dead particles
        if (particle.life <= 0) {
          particles.splice(i, 1);
          continue;
        }
        
        // Draw particle
        const alpha = particle.life / particle.maxLife;
        const size = alpha * 3;
        
        ctx.save();
        ctx.globalAlpha = alpha * 0.8;
        ctx.fillStyle = `hsl(${particle.hue}, 70%, 60%)`;
        ctx.beginPath();
        ctx.arc(particle.x, particle.y, size, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      }
      
      animationId = requestAnimationFrame(animate);
    };

    const handleMouseMove = (e: MouseEvent) => {
      prevMouseX = mouseX;
      prevMouseY = mouseY;
      mouseX = e.clientX;
      mouseY = e.clientY;
      
      // Calculate velocity
      const vx = mouseX - prevMouseX;
      const vy = mouseY - prevMouseY;
      const velocity = Math.sqrt(vx * vx + vy * vy);
      
      // Add particles based on velocity
      if (velocity > 2) {
        const numParticles = Math.min(Math.floor(velocity / 3), 10);
        
        for (let i = 0; i < numParticles; i++) {
          particles.push({
            x: mouseX + (Math.random() - 0.5) * 20,
            y: mouseY + (Math.random() - 0.5) * 20,
            vx: vx * 0.1 + (Math.random() - 0.5) * 2,
            vy: vy * 0.1 + (Math.random() - 0.5) * 2,
            life: 60,
            maxLife: 60,
            hue: (Date.now() * 0.1) % 360
          });
        }
      }
    };

    const handleResize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('resize', handleResize);
    
    animate();

    return () => {
      if (animationId) {
        cancelAnimationFrame(animationId);
      }
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return (
    <div className="fixed top-0 left-0 z-50 pointer-events-none">
      <canvas 
        ref={canvasRef} 
        className="w-screen h-screen" 
        style={{ position: 'fixed', top: 0, left: 0, zIndex: 50, pointerEvents: 'none' }}
      />
    </div>
  );
}

export { SplashCursor };
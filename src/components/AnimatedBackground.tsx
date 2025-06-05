import React from 'react';
import { useTheme } from '../contexts/ThemeContext';

// Cloud Animation for Light Theme
const CloudAnimation: React.FC = () => {
  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
      {[...Array(8)].map((_, i) => (
        <div
          key={i}
          className="absolute opacity-20 text-white text-6xl select-none"
          style={{
            top: `${Math.random() * 100}%`,
            left: `${-20 + i * 15}%`,
            animation: `float ${15 + i * 3}s linear infinite`,
            animationDelay: `${i * 2}s`
          }}
        >
          ☁️
        </div>
      ))}
      
      <style>{`
        @keyframes float {
          from {
            transform: translateX(-100px);
          }
          to {
            transform: translateX(calc(100vw + 100px));
          }
        }
      `}</style>
    </div>
  );
};

// Particle Animation for Purple Theme
const ParticleAnimation: React.FC = () => {
  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
      {[...Array(50)].map((_, i) => (
        <div
          key={i}
          className="absolute rounded-full"
          style={{
            width: `${2 + Math.random() * 4}px`,
            height: `${2 + Math.random() * 4}px`,
            top: `${Math.random() * 100}%`,
            left: `${Math.random() * 100}%`,
            background: `radial-gradient(circle, ${
              Math.random() > 0.5 ? '#ec4899' : '#a855f7'
            }, transparent)`,
            animation: `pulse ${2 + Math.random() * 4}s ease-in-out infinite`,
            animationDelay: `${Math.random() * 2}s`,
            boxShadow: `0 0 ${10 + Math.random() * 20}px ${
              Math.random() > 0.5 ? '#ec4899' : '#a855f7'
            }`
          }}
        />
      ))}
      
      {/* Floating particles */}
      {[...Array(20)].map((_, i) => (
        <div
          key={`float-${i}`}
          className="absolute w-1 h-1 bg-pink-400 rounded-full"
          style={{
            top: `${Math.random() * 100}%`,
            left: `${Math.random() * 100}%`,
            animation: `floatUp ${10 + Math.random() * 10}s linear infinite`,
            animationDelay: `${Math.random() * 5}s`,
            opacity: 0.6
          }}
        />
      ))}
      
      <style>{`
        @keyframes pulse {
          0%, 100% {
            opacity: 0.3;
            transform: scale(1);
          }
          50% {
            opacity: 0.8;
            transform: scale(1.2);
          }
        }
        
        @keyframes floatUp {
          from {
            transform: translateY(100vh) rotate(0deg);
            opacity: 0;
          }
          10% {
            opacity: 0.6;
          }
          90% {
            opacity: 0.6;
          }
          to {
            transform: translateY(-100px) rotate(360deg);
            opacity: 0;
          }
        }
      `}</style>
    </div>
  );
};

// Starfield Animation for Dark Theme
const StarfieldAnimation: React.FC = () => {
  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
      {[...Array(150)].map((_, i) => (
        <div
          key={i}
          className="absolute rounded-full bg-white"
          style={{
            width: `${1 + Math.random() * 3}px`,
            height: `${1 + Math.random() * 3}px`,
            top: `${Math.random() * 100}%`,
            left: `${Math.random() * 100}%`,
            animation: `twinkle ${3 + Math.random() * 6}s ease-in-out infinite`,
            animationDelay: `${Math.random() * 5}s`,
            opacity: Math.random() * 0.8 + 0.2
          }}
        />
      ))}
      
      {/* Shooting stars */}
      {[...Array(3)].map((_, i) => (
        <div
          key={`shooting-${i}`}
          className="absolute h-0.5 bg-gradient-to-r from-transparent via-purple-400 to-transparent"
          style={{
            width: '100px',
            top: `${Math.random() * 50}%`,
            left: '-100px',
            animation: `shootingStar ${8 + Math.random() * 4}s linear infinite`,
            animationDelay: `${i * 3 + Math.random() * 2}s`
          }}
        />
      ))}
      
      <style>{`
        @keyframes twinkle {
          0%, 100% {
            opacity: 0.2;
            transform: scale(1);
          }
          50% {
            opacity: 1;
            transform: scale(1.1);
          }
        }
        
        @keyframes shootingStar {
          from {
            transform: translateX(0) translateY(0) rotate(45deg);
            opacity: 0;
          }
          10% {
            opacity: 1;
          }
          90% {
            opacity: 1;
          }
          to {
            transform: translateX(calc(100vw + 200px)) translateY(200px) rotate(45deg);
            opacity: 0;
          }
        }
      `}</style>
    </div>
  );
};

export default function AnimatedBackground() {
  const { theme } = useTheme();
  
  if (theme.animations.clouds) {
    return <CloudAnimation />;
  }
  
  if (theme.animations.particles) {
    return <ParticleAnimation />;
  }
  
  if (theme.animations.stars) {
    return <StarfieldAnimation />;
  }
  
  return null;
}
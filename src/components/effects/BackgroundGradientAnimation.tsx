"use client";
import { cn } from "../../lib/utils";
import { useEffect, useRef, useState } from "react";

export const BackgroundGradientAnimation = ({
  gradientBackgroundStart = "rgb(108, 0, 162)",
  gradientBackgroundEnd = "rgb(0, 17, 82)",
  firstColor = "18, 113, 255",
  secondColor = "221, 74, 255", 
  thirdColor = "100, 220, 255",
  fourthColor = "200, 50, 50",
  fifthColor = "180, 180, 50",
  pointerColor = "140, 100, 255",
  size = "80%",
  blendingValue = "hard-light",
  children,
  className,
  interactive = true,
  containerClassName,
}: {
  gradientBackgroundStart?: string;
  gradientBackgroundEnd?: string;
  firstColor?: string;
  secondColor?: string;
  thirdColor?: string;
  fourthColor?: string;
  fifthColor?: string;
  pointerColor?: string;
  size?: string;
  blendingValue?: string;
  children?: React.ReactNode;
  className?: string;
  interactive?: boolean;
  containerClassName?: string;
}) => {
  const interactiveRef = useRef<HTMLDivElement>(null);
  const [cursorPosition, setCursorPosition] = useState({ x: 0, y: 0 });
  const [hoveringOverCard, setHoveringOverCard] = useState(false);

  useEffect(() => {
    function handleMouseMove(event: MouseEvent) {
      if (interactiveRef.current) {
        const rect = interactiveRef.current.getBoundingClientRect();
        setCursorPosition({
          x: event.clientX - rect.left,
          y: event.clientY - rect.top,
        });
      }
    }

    if (interactive) {
      document.addEventListener("mousemove", handleMouseMove);
      return () => {
        document.removeEventListener("mousemove", handleMouseMove);
      };
    }
  }, [interactive]);

  return (
    <div
      className={cn(
        "h-screen w-screen relative overflow-hidden top-0 left-0",
        containerClassName
      )}
      ref={interactiveRef}
      onMouseEnter={() => setHoveringOverCard(true)}
      onMouseLeave={() => setHoveringOverCard(false)}
    >
      <svg className="hidden">
        <defs>
          <filter id="blurMe">
            <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="blur" />
            <feColorMatrix
              in="blur"
              mode="matrix"
              values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -8"
              result="goo"
            />
            <feBlend in="SourceGraphic" in2="goo" />
          </filter>
        </defs>
      </svg>
      <div className={cn("", className)}>
        <div className="gradients-container h-full w-full blur-lg">
          <div
            className={cn(
              `absolute [background:radial-gradient(circle_at_center,_var(--color)_0,_var(--color)_50%)_no-repeat]`,
              `[mix-blend-mode:var(--blending-value)] w-[var(--size)] h-[var(--size)] top-[calc(50%-var(--size)/2)] left-[calc(50%-var(--size)/2)]`,
              `[transform-origin:center_center]`,
              `animate-first`,
              `opacity-100`
            )}
            style={{
              "--size": size,
              "--color": `rgba(${firstColor}, 0.8)`,
              "--blending-value": blendingValue,
            } as React.CSSProperties}
          ></div>
          <div
            className={cn(
              `absolute [background:radial-gradient(circle_at_center,_rgba(var(--color),_0.8)_0,_rgba(var(--color),_0)_50%)_no-repeat]`,
              `[mix-blend-mode:var(--blending-value)] w-[var(--size)] h-[var(--size)] top-[calc(50%-var(--size)/2)] left-[calc(50%-var(--size)/2)]`,
              `[transform-origin:calc(50%-400px)]`,
              `animate-second`,
              `opacity-100`
            )}
            style={{
              "--size": size,
              "--color": secondColor,
              "--blending-value": blendingValue,
            } as React.CSSProperties}
          ></div>
          <div
            className={cn(
              `absolute [background:radial-gradient(circle_at_center,_rgba(var(--color),_0.8)_0,_rgba(var(--color),_0)_50%)_no-repeat]`,
              `[mix-blend-mode:var(--blending-value)] w-[var(--size)] h-[var(--size)] top-[calc(50%-var(--size)/2)] left-[calc(50%-var(--size)/2)]`,
              `[transform-origin:calc(50%+400px)]`,
              `animate-third`,
              `opacity-100`
            )}
            style={{
              "--size": size,
              "--color": thirdColor,
              "--blending-value": blendingValue,
            } as React.CSSProperties}
          ></div>
          <div
            className={cn(
              `absolute [background:radial-gradient(circle_at_center,_rgba(var(--color),_0.8)_0,_rgba(var(--color),_0)_50%)_no-repeat]`,
              `[mix-blend-mode:var(--blending-value)] w-[var(--size)] h-[var(--size)] top-[calc(50%-var(--size)/2)] left-[calc(50%-var(--size)/2)]`,
              `[transform-origin:calc(50%-200px)]`,
              `animate-fourth`,
              `opacity-70`
            )}
            style={{
              "--size": size,
              "--color": fourthColor,
              "--blending-value": blendingValue,
            } as React.CSSProperties}
          ></div>
          <div
            className={cn(
              `absolute [background:radial-gradient(circle_at_center,_rgba(var(--color),_0.8)_0,_rgba(var(--color),_0)_50%)_no-repeat]`,
              `[mix-blend-mode:var(--blending-value)] w-[var(--size)] h-[var(--size)] top-[calc(50%-var(--size)/2)] left-[calc(50%-var(--size)/2)]`,
              `[transform-origin:calc(50%+200px)]`,
              `animate-fifth`,
              `opacity-100`
            )}
            style={{
              "--size": size,
              "--color": fifthColor,
              "--blending-value": blendingValue,
            } as React.CSSProperties}
          ></div>

          {interactive && (
            <div
              className={cn(
                `absolute [background:radial-gradient(circle_at_center,_rgba(var(--color),_0.8)_0,_rgba(var(--color),_0)_50%)_no-repeat]`,
                `[mix-blend-mode:var(--blending-value)] w-[var(--size)] h-[var(--size)] opacity-70`,
                `transition-opacity duration-300`,
                hoveringOverCard ? "opacity-100" : "opacity-0"
              )}
              style={{
                "--size": size,
                "--color": pointerColor,
                "--blending-value": blendingValue,
                transform: `translate(${cursorPosition.x - parseFloat(size) / 2}px, ${
                  cursorPosition.y - parseFloat(size) / 2
                }px)`,
              } as React.CSSProperties}
            ></div>
          )}
        </div>
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="relative z-10">{children}</div>
        </div>
      </div>
    </div>
  );
};
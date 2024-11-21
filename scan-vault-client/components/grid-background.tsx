'use client'

import React, { useEffect, useRef } from 'react'

export function GridBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const resizeCanvas = () => {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
    }

    resizeCanvas()
    window.addEventListener('resize', resizeCanvas)

    const drawGrid = () => {
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)'
      ctx.lineWidth = 0.5

      const cellSize = 50
      for (let x = 0; x <= canvas.width; x += cellSize) {
        ctx.beginPath()
        ctx.moveTo(x, 0)
        ctx.lineTo(x, canvas.height)
        ctx.stroke()
      }

      for (let y = 0; y <= canvas.height; y += cellSize) {
        ctx.beginPath()
        ctx.moveTo(0, y)
        ctx.lineTo(canvas.width, y)
        ctx.stroke()
      }
    }

    const sparkles: { x: number; y: number; size: number; alpha: number }[] = Array(5).fill(null).map(() => ({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      size: 2 + Math.random() * 2,
      alpha: 1
    }))

    const animateSparkles = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      drawGrid()

      sparkles.forEach(sparkle => {
        sparkle.x += (Math.random() - 0.5) * 2
        sparkle.y += (Math.random() - 0.5) * 2
        sparkle.alpha = Math.max(0, sparkle.alpha - 0.01)

        if (sparkle.alpha <= 0) {
          sparkle.x = Math.random() * canvas.width
          sparkle.y = Math.random() * canvas.height
          sparkle.alpha = 1
        }

        ctx.beginPath()
        ctx.arc(sparkle.x, sparkle.y, sparkle.size, 0, Math.PI * 2)
        ctx.fillStyle = `rgba(255, 255, 255, ${sparkle.alpha})`
        ctx.fill()
      })

      requestAnimationFrame(animateSparkles)
    }

    animateSparkles()

    return () => {
      window.removeEventListener('resize', resizeCanvas)
    }
  }, [])

  return <canvas ref={canvasRef} className="absolute inset-0 w-full h-full" />
}


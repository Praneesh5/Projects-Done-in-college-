import { useEffect, useRef } from 'react'

/**
 * Lightweight Matrix Rain — single canvas, minimal CPU.
 * Drops green glyphs from top to bottom in columns.
 */
export default function MatrixRain() {
    const canvasRef = useRef(null)

    useEffect(() => {
        const canvas = canvasRef.current
        if (!canvas) return
        const ctx = canvas.getContext('2d')

        const resize = () => {
            canvas.width = window.innerWidth
            canvas.height = window.innerHeight
        }
        resize()
        window.addEventListener('resize', resize)

        const fontSize = 14
        const cols = Math.floor(canvas.width / fontSize)
        const drops = Array(cols).fill(1)
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*(){}[]<>/\\|~₹?!;:アイウエオカキクケコサシスセソ'.split('')

        let animId
        const draw = () => {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.06)'
            ctx.fillRect(0, 0, canvas.width, canvas.height)

            for (let i = 0; i < drops.length; i++) {
                const char = chars[Math.floor(Math.random() * chars.length)]
                const x = i * fontSize
                const y = drops[i] * fontSize

                // Head char is brighter
                if (Math.random() > 0.5) {
                    ctx.fillStyle = '#00FF41'
                    ctx.shadowBlur = 8
                    ctx.shadowColor = '#00FF41'
                } else {
                    ctx.fillStyle = 'rgba(0, 255, 65, 0.35)'
                    ctx.shadowBlur = 0
                }

                ctx.font = `${fontSize}px 'Share Tech Mono', monospace`
                ctx.fillText(char, x, y)
                ctx.shadowBlur = 0

                if (y > canvas.height && Math.random() > 0.975) {
                    drops[i] = 0
                }
                drops[i]++
            }
            animId = requestAnimationFrame(draw)
        }

        // Slow down to ~20fps for performance
        let lastTime = 0
        const fps = 20
        const interval = 1000 / fps

        const loop = (time) => {
            animId = requestAnimationFrame(loop)
            const delta = time - lastTime
            if (delta < interval) return
            lastTime = time - (delta % interval)
            draw()
        }

        // Cancel the direct draw loop, use throttled one
        const startLoop = () => {
            cancelAnimationFrame(animId)
            lastTime = performance.now()
            animId = requestAnimationFrame(loop)
        }
        startLoop()

        return () => {
            cancelAnimationFrame(animId)
            window.removeEventListener('resize', resize)
        }
    }, [])

    return (
        <canvas
            ref={canvasRef}
            style={{
                position: 'fixed',
                top: 0,
                left: 0,
                width: '100%',
                height: '100%',
                zIndex: 0,
                opacity: 0.4,
                pointerEvents: 'none',
            }}
        />
    )
}

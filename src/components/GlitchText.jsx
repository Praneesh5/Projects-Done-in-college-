import { motion } from 'framer-motion'

/**
 * GlitchText — Cyberpunk glitch effect on hover
 * Replaces DancingText for the hacker theme
 */
export default function GlitchText({ text, className, color = 'var(--neon-green)', size }) {
    return (
        <motion.span
            className={className}
            style={{
                display: 'inline-block',
                color,
                fontFamily: 'var(--font-display)',
                fontSize: size || 'inherit',
                fontWeight: 800,
                textTransform: 'uppercase',
                letterSpacing: '0.05em',
                position: 'relative',
                cursor: 'default',
            }}
            whileHover={{
                textShadow: `2px 0 var(--neon-cyan), -2px 0 var(--neon-red), 0 0 20px ${color}`,
                transition: { duration: 0.1 },
            }}
        >
            {text}
        </motion.span>
    )
}

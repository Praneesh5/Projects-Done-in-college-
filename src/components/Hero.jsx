import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { HiArrowRight, HiCalendar, HiLocationMarker } from 'react-icons/hi'

/* ── Countdown ── */
function Countdown({ targetDate }) {
    const [time, setTime] = useState({ days: 0, hours: 0, minutes: 0, seconds: 0 })

    useEffect(() => {
        const interval = setInterval(() => {
            const diff = targetDate - new Date()
            if (diff <= 0) { clearInterval(interval); return }
            setTime({
                days: Math.floor(diff / 86400000),
                hours: Math.floor((diff / 3600000) % 24),
                minutes: Math.floor((diff / 60000) % 60),
                seconds: Math.floor((diff / 1000) % 60),
            })
        }, 1000)
        return () => clearInterval(interval)
    }, [targetDate])

    return (
        <div className="flex gap-3 sm:gap-5 justify-center flex-wrap">
            {Object.entries(time).map(([label, value], i) => (
                <motion.div
                    key={label}
                    className="flex flex-col items-center"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.8 + i * 0.1 }}
                    whileHover={{ scale: 1.1, y: -5 }}
                >
                    <div
                        className="flex items-center justify-center mb-2"
                        style={{
                            width: 'clamp(60px, 12vw, 85px)',
                            height: 'clamp(60px, 12vw, 85px)',
                            background: 'rgba(0, 255, 65, 0.03)',
                            border: '1px solid rgba(0, 255, 65, 0.2)',
                            borderRadius: '4px',
                            animation: 'pulse-neon 3s ease-in-out infinite',
                            animationDelay: `${i * 0.5}s`,
                        }}
                    >
                        <span className="neon-text" style={{
                            fontFamily: 'var(--font-display)',
                            fontSize: 'clamp(1.4rem, 4vw, 2.4rem)',
                            fontWeight: 800,
                        }}>
                            {String(value).padStart(2, '0')}
                        </span>
                    </div>
                    <span style={{
                        fontSize: '0.6rem',
                        color: 'var(--text-dim)',
                        textTransform: 'uppercase',
                        letterSpacing: '3px',
                        fontWeight: 600,
                        fontFamily: 'var(--font-mono)',
                    }}>
                        {label}
                    </span>
                </motion.div>
            ))}
        </div>
    )
}

/* ── HERO ── */
export default function Hero() {
    const eventDate = new Date('2026-04-10T09:00:00+05:30')

    return (
        <section
            id="home"
            className="relative flex items-center justify-center overflow-hidden"
            style={{ minHeight: '100vh', paddingTop: '100px', paddingBottom: '80px' }}
        >
            <div className="relative z-10 w-full max-w-5xl mx-auto px-6 sm:px-10 text-center">
                {/* Status Terminal Line */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.2 }}
                    className="inline-flex items-center gap-2 mb-8"
                >
                    <div className="flex items-center gap-2.5 px-5 py-2.5"
                        style={{
                            background: 'rgba(0, 10, 5, 0.8)',
                            border: '1px solid rgba(0, 255, 65, 0.2)',
                            borderRadius: '2px',
                        }}
                    >
                        <motion.div
                            animate={{ opacity: [1, 0.3, 1] }}
                            transition={{ duration: 1.5, repeat: Infinity }}
                            style={{
                                width: '6px', height: '6px', borderRadius: '50%',
                                background: 'var(--neon-green)',
                                boxShadow: '0 0 8px var(--neon-green)',
                            }}
                        />
                        <span style={{
                            fontFamily: 'var(--font-mono)',
                            fontSize: '0.7rem',
                            color: 'var(--text-secondary)',
                            letterSpacing: '2px',
                        }}>
                            NATIONAL LEVEL SYMPOSIUM // STATUS: ACTIVE
                        </span>
                    </div>
                </motion.div>

                {/* Title — Glitch Style */}
                <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.8, delay: 0.3 }}
                >
                    <h1 className="neon-text" style={{
                        fontFamily: 'var(--font-display)',
                        fontSize: 'clamp(3rem, 12vw, 8rem)',
                        fontWeight: 900,
                        lineHeight: 0.95,
                        letterSpacing: '0.08em',
                        marginBottom: '0.5rem',
                        animation: 'flicker 4s ease-in-out infinite',
                    }}>
                        INTELLEX
                    </h1>
                </motion.div>

                {/* Year */}
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.6, duration: 0.6 }}
                    className="flex justify-center gap-2 sm:gap-3 mb-8"
                >
                    {['2', '0', '2', '6'].map((digit, i) => (
                        <motion.span
                            key={i}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.7 + i * 0.1 }}
                            whileHover={{ scale: 1.2, textShadow: '0 0 20px var(--neon-cyan)' }}
                            style={{
                                fontFamily: 'var(--font-display)',
                                fontSize: 'clamp(1.2rem, 3vw, 2.2rem)',
                                fontWeight: 800,
                                color: 'var(--neon-cyan)',
                                background: 'rgba(0, 240, 255, 0.05)',
                                width: 'clamp(40px, 7vw, 56px)',
                                height: 'clamp(40px, 7vw, 56px)',
                                display: 'inline-flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                border: '1px solid rgba(0, 240, 255, 0.2)',
                                borderRadius: '4px',
                                cursor: 'default',
                                textShadow: '0 0 10px rgba(0, 240, 255, 0.3)',
                            }}
                        >
                            {digit}
                        </motion.span>
                    ))}
                </motion.div>

                {/* Date & Venue Badges */}
                <motion.div
                    initial={{ opacity: 0, y: 15 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.8 }}
                    className="flex flex-wrap justify-center gap-3 mb-10"
                >
                    {[
                        { icon: <HiCalendar />, text: '10 — 11 APRIL 2026', color: 'var(--neon-green)' },
                        { icon: <HiLocationMarker />, text: 'SIMATS ENGINEERING', color: 'var(--neon-cyan)' },
                    ].map((badge, i) => (
                        <motion.div
                            key={i}
                            whileHover={{ scale: 1.05, boxShadow: `0 0 20px ${badge.color === 'var(--neon-green)' ? 'rgba(0,255,65,0.15)' : 'rgba(0,240,255,0.15)'}` }}
                            className="flex items-center gap-2 px-5 py-2.5"
                            style={{
                                background: 'rgba(0, 10, 5, 0.8)',
                                border: `1px solid ${badge.color === 'var(--neon-green)' ? 'rgba(0,255,65,0.15)' : 'rgba(0,240,255,0.15)'}`,
                                borderRadius: '4px',
                            }}
                        >
                            <span style={{ color: badge.color, fontSize: '1rem' }}>{badge.icon}</span>
                            <span style={{
                                fontFamily: 'var(--font-mono)',
                                fontSize: '0.75rem',
                                fontWeight: 600,
                                color: 'var(--text-primary)',
                                letterSpacing: '1.5px',
                            }}>
                                {badge.text}
                            </span>
                        </motion.div>
                    ))}
                </motion.div>

                {/* Countdown */}
                <motion.div
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.9 }}
                    className="mb-12"
                >
                    <p className="mb-4" style={{
                        color: 'var(--text-dim)',
                        letterSpacing: '4px',
                        textTransform: 'uppercase',
                        fontSize: '0.6rem',
                        fontWeight: 600,
                        fontFamily: 'var(--font-mono)',
                    }}>
                        // COUNTDOWN_TO_EVENT
                    </p>
                    <Countdown targetDate={eventDate} />
                </motion.div>

                {/* CTA */}
                <motion.div
                    initial={{ opacity: 0, y: 15 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 1.1 }}
                    className="flex flex-wrap justify-center gap-4"
                >
                    <motion.a href="#tech-events" className="btn-solid"
                        whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                        EXPLORE_EVENTS <HiArrowRight />
                    </motion.a>
                    <motion.a href="#about" className="btn-hack"
                        whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                        ./LEARN_MORE
                    </motion.a>
                </motion.div>

                {/* Scroll Indicator */}
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 2 }} className="mt-14">
                    <motion.div animate={{ y: [0, 10, 0] }} transition={{ repeat: Infinity, duration: 2 }}
                        style={{
                            width: '20px',
                            height: '34px',
                            border: '1px solid rgba(0,255,65,0.2)',
                            borderRadius: '10px',
                            margin: '0 auto',
                            position: 'relative',
                        }}>
                        <motion.div animate={{ y: [0, 12, 0], opacity: [1, 0.3, 1] }}
                            transition={{ repeat: Infinity, duration: 2 }}
                            style={{
                                width: '2px',
                                height: '6px',
                                background: 'var(--neon-green)',
                                borderRadius: '1px',
                                position: 'absolute',
                                top: '5px',
                                left: '50%',
                                transform: 'translateX(-50%)',
                                boxShadow: '0 0 5px var(--neon-green)',
                            }} />
                    </motion.div>
                </motion.div>
            </div>
        </section>
    )
}

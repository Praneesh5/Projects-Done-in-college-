import { motion } from 'framer-motion'
import { useInView } from 'react-intersection-observer'
import { HiPhone } from 'react-icons/hi'
import GlitchText from './GlitchText'

const coordinators = [
    {
        name: 'Dr. M. Arivukarasi',
        role: 'Event Coordinator',
        phone: '9791082080',
        initial: 'MA',
        color: '#00FF41',
    },
    {
        name: 'Dr. J. Nithisha',
        role: 'Event Coordinator',
        phone: '8754419740',
        initial: 'JN',
        color: '#00F0FF',
    },
]

export default function Coordinators() {
    const [ref, inView] = useInView({ triggerOnce: true, threshold: 0.1 })

    return (
        <section
            id="coordinators"
            ref={ref}
            className="relative overflow-hidden"
            style={{
                background: 'var(--bg-void)',
                paddingTop: 'clamp(80px, 12vw, 140px)',
                paddingBottom: 'clamp(80px, 12vw, 140px)',
            }}
        >
            <div className="relative z-10 max-w-4xl mx-auto px-6 sm:px-10">
                <motion.div
                    initial={{ opacity: 0, y: 40 }}
                    animate={inView ? { opacity: 1, y: 0 } : {}}
                    transition={{ duration: 0.7 }}
                    className="text-center mb-5"
                >
                    <span className="section-tag inline-block">// ADMIN_ACCESS</span>
                    <h2 className="section-title">
                        <GlitchText text="EVENT " color="var(--text-primary)" />
                        <GlitchText text="OPERATORS" color="var(--neon-cyan)" />
                    </h2>
                </motion.div>

                <motion.p
                    initial={{ opacity: 0 }}
                    animate={inView ? { opacity: 1 } : {}}
                    transition={{ duration: 0.5, delay: 0.2 }}
                    className="section-subtitle mb-14"
                >
                    {'>'} The system administrators behind INTELLEX 2026. Reach out anytime.
                </motion.p>

                <div className="grid sm:grid-cols-2 gap-5 max-w-2xl mx-auto">
                    {coordinators.map((coord, i) => (
                        <motion.div
                            key={coord.name}
                            initial={{ opacity: 0, y: 40 }}
                            animate={inView ? { opacity: 1, y: 0 } : {}}
                            transition={{ duration: 0.6, delay: 0.1 + i * 0.12 }}
                            className="relative p-7 text-center cyber-card"
                            style={{
                                borderColor: `${coord.color}15`,
                                transition: 'all 0.4s ease',
                            }}
                            onMouseEnter={(e) => {
                                e.currentTarget.style.borderColor = `${coord.color}40`
                                e.currentTarget.style.boxShadow = `0 0 30px ${coord.color}15`
                                e.currentTarget.style.transform = 'translateY(-6px)'
                            }}
                            onMouseLeave={(e) => {
                                e.currentTarget.style.borderColor = `${coord.color}15`
                                e.currentTarget.style.boxShadow = 'none'
                                e.currentTarget.style.transform = 'translateY(0)'
                            }}
                        >
                            {/* Avatar */}
                            <div className="relative mx-auto w-20 h-20 flex items-center justify-center mb-5"
                                style={{
                                    border: `2px solid ${coord.color}40`,
                                    borderRadius: '4px',
                                    background: `${coord.color}08`,
                                }}>
                                <span style={{
                                    fontFamily: 'var(--font-display)',
                                    fontSize: '1.3rem',
                                    fontWeight: 800,
                                    color: coord.color,
                                    textShadow: `0 0 15px ${coord.color}50`,
                                }}>
                                    {coord.initial}
                                </span>
                                <motion.div
                                    animate={{ opacity: [0.3, 0, 0.3] }}
                                    transition={{ duration: 3, repeat: Infinity }}
                                    className="absolute inset-0"
                                    style={{
                                        border: `1px solid ${coord.color}30`,
                                        borderRadius: '4px',
                                    }}
                                />
                            </div>

                            <h3 className="text-base font-bold mb-1"
                                style={{
                                    fontFamily: 'var(--font-display)',
                                    color: 'var(--text-primary)',
                                    letterSpacing: '1px',
                                    fontSize: '0.9rem',
                                }}>
                                {coord.name}
                            </h3>
                            <p className="text-xs mb-5" style={{
                                color: 'var(--text-dim)',
                                fontFamily: 'var(--font-mono)',
                                letterSpacing: '1.5px',
                                textTransform: 'uppercase',
                            }}>
                                {coord.role}
                            </p>

                            <motion.a
                                href={`tel:${coord.phone}`}
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                className="inline-flex items-center gap-2 px-5 py-2.5 text-xs font-bold no-underline"
                                style={{
                                    background: 'transparent',
                                    color: coord.color,
                                    border: `1px solid ${coord.color}30`,
                                    borderRadius: '3px',
                                    fontFamily: 'var(--font-mono)',
                                    letterSpacing: '1px',
                                    transition: 'all 0.3s ease',
                                }}
                                onMouseEnter={(e) => {
                                    e.currentTarget.style.background = coord.color
                                    e.currentTarget.style.color = '#000'
                                    e.currentTarget.style.boxShadow = `0 0 20px ${coord.color}30`
                                }}
                                onMouseLeave={(e) => {
                                    e.currentTarget.style.background = 'transparent'
                                    e.currentTarget.style.color = coord.color
                                    e.currentTarget.style.boxShadow = 'none'
                                }}
                            >
                                <HiPhone size={12} /> {coord.phone}
                            </motion.a>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    )
}

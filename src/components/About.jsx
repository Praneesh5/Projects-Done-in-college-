import { motion } from 'framer-motion'
import { useInView } from 'react-intersection-observer'
import GlitchText from './GlitchText'

const highlights = [
    {
        title: 'CERTIFIED RECOGNITION',
        desc: 'Merit certificates and participation acknowledgements for all eligible students.',
        color: 'var(--neon-green)',
        icon: '🏅',
        prefix: '[cert]',
    },
    {
        title: 'EXCITING PRIZES',
        desc: 'Win medals, trophies, and amazing prizes for outstanding performances.',
        color: 'var(--neon-amber)',
        icon: '🏆',
        prefix: '[prize]',
    },
    {
        title: 'NATIONAL EXPOSURE',
        desc: 'Engage with participants across institutions from all over the country.',
        color: 'var(--neon-cyan)',
        icon: '🌐',
        prefix: '[net]',
    },
    {
        title: 'NETWORKING HUB',
        desc: 'Interact with industry experts, peers, and faculty from top institutions.',
        color: 'var(--neon-purple)',
        icon: '🤝',
        prefix: '[hub]',
    },
]

export default function About() {
    const [ref, inView] = useInView({ triggerOnce: true, threshold: 0.05 })

    return (
        <section
            id="about"
            ref={ref}
            className="relative overflow-hidden grid-overlay"
            style={{
                background: 'var(--bg-deep)',
                paddingTop: 'clamp(80px, 12vw, 140px)',
                paddingBottom: 'clamp(80px, 12vw, 140px)',
            }}
        >
            <div className="relative z-10 max-w-5xl mx-auto px-6 sm:px-10">
                {/* Header */}
                <motion.div
                    initial={{ opacity: 0, y: 40 }}
                    animate={inView ? { opacity: 1, y: 0 } : {}}
                    transition={{ duration: 0.7 }}
                    className="text-center mb-5"
                >
                    <span className="section-tag inline-block">// ABOUT_SYSTEM</span>
                    <h2 className="section-title">
                        <GlitchText text="WHY " color="var(--text-primary)" />
                        <GlitchText text="INTELLEX?" color="var(--neon-green)" />
                    </h2>
                </motion.div>

                <motion.p
                    initial={{ opacity: 0, y: 20 }}
                    animate={inView ? { opacity: 1, y: 0 } : {}}
                    transition={{ duration: 0.6, delay: 0.2 }}
                    className="section-subtitle mb-14"
                >
                    {'>'} INTELLEX 2026 is a national-level symposium uniting innovators, creators,
                    developers, and performers to showcase talent in technical and non-technical domains.
                </motion.p>

                {/* Feature Cards */}
                <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
                    {highlights.map((item, i) => (
                        <motion.div
                            key={item.title}
                            initial={{ opacity: 0, y: 40 }}
                            animate={inView ? { opacity: 1, y: 0 } : {}}
                            transition={{ duration: 0.6, delay: 0.3 + i * 0.1 }}
                            whileHover={{
                                y: -6,
                                borderColor: item.color,
                                boxShadow: `0 0 30px ${item.color === 'var(--neon-green)' ? 'rgba(0,255,65,0.15)' :
                                    item.color === 'var(--neon-amber)' ? 'rgba(255,184,0,0.15)' :
                                        item.color === 'var(--neon-cyan)' ? 'rgba(0,240,255,0.15)' :
                                            'rgba(191,0,255,0.15)'}`,
                            }}
                            className="cyber-card p-6 cursor-default"
                        >
                            <div className="flex items-center gap-3 mb-4">
                                <span className="text-2xl">{item.icon}</span>
                                <span style={{
                                    fontFamily: 'var(--font-mono)',
                                    fontSize: '0.65rem',
                                    color: item.color,
                                    letterSpacing: '1px',
                                    opacity: 0.7,
                                }}>
                                    {item.prefix}
                                </span>
                            </div>
                            <h3 style={{
                                fontFamily: 'var(--font-display)',
                                color: 'var(--text-primary)',
                                fontSize: '0.85rem',
                                fontWeight: 700,
                                letterSpacing: '1px',
                                marginBottom: '0.5rem',
                            }}>
                                {item.title}
                            </h3>
                            <p style={{
                                fontSize: '0.82rem',
                                color: 'var(--text-secondary)',
                                lineHeight: 1.7,
                                fontFamily: 'var(--font-body)',
                            }}>
                                {item.desc}
                            </p>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    )
}

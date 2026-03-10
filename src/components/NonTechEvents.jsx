import { motion } from 'framer-motion'
import { useInView } from 'react-intersection-observer'
import { HiArrowRight, HiPhone } from 'react-icons/hi'
import GlitchText from './GlitchText'

const nonTechEvents = [
    {
        title: 'Treasure Hunt',
        brief: 'Follow the clues, solve puzzles, and race to the treasure!',
        icon: '🗺️',
        color: '#FFB800',
        squad: 'Team (3-4)',
        window: '60 mins',
        fee: '',
        faculty: '',
        volunteer: '',
        volunteerPhone: '',
        rules: ['Teams of 3-4 members', 'Clues given one at a time', 'No mobile phones during hunt', 'Stay within campus', 'First team to find all clues wins', "Organizer's decision is final"],
    },
    {
        title: 'Find the BGM',
        brief: 'Identify background music from movies and shows!',
        icon: '🎵',
        color: '#FF00A0',
        squad: 'Solo / Duo',
        window: '45 mins',
        fee: '',
        faculty: 'Dr. S. Aghalya',
        volunteer: '',
        volunteerPhone: '',
        rules: ['Solo or duo participation', 'Multiple rounds of difficulty', 'Answer within time limit', 'No Shazam or music apps', 'Languages: Tamil, English, Hindi', 'Top scorers advance to finals'],
    },
    {
        title: 'Dance',
        brief: 'Set the stage on fire with your moves!',
        icon: '💃',
        color: '#FF003C',
        squad: 'Solo / Group',
        window: '3–5 mins',
        fee: '',
        faculty: 'Dr. B. Abirami',
        volunteer: 'B. Divesh Chowdary',
        volunteerPhone: '9100452238',
        rules: ['Solo or group (max 8)', 'Music submitted before deadline', 'Performance: 3-5 minutes', 'No vulgar/offensive content', 'Props OK, no fire/liquid', "Judge's decision is final"],
    },
    {
        title: 'Ramp Walk',
        brief: 'Walk the ramp with style and confidence!',
        icon: '✨',
        color: '#00F0FF',
        squad: 'Solo / Team (Max 6)',
        window: '4 mins (+1 prep)',
        fee: '',
        faculty: '',
        volunteer: 'P. Deepika',
        volunteerPhone: '6379764261',
        rules: ['Max 6 members per team', 'Theme-based dressing encouraged', '4 mins (+1 min prep)', 'Costumes must be decent', 'Judging: Style, Confidence, Coordination', 'No offensive themes'],
    },
    {
        title: 'E-Sports',
        brief: 'Battle it out in popular e-sports titles!',
        icon: '🎮',
        color: '#BF00FF',
        squad: 'Solo / Squad',
        window: 'Varies',
        fee: '',
        faculty: '',
        volunteer: '',
        volunteerPhone: '',
        rules: ['Games: BGMI / Free Fire / Valorant', 'Bring your own devices', 'Fair play — no hacks/cheats', 'Tournament bracket format', 'Stable internet provided', 'Winners by elimination rounds'],
    },
    {
        title: 'Chess',
        brief: 'Outsmart your opponents in the ultimate game of strategy!',
        icon: '♟️',
        color: '#00FF41',
        squad: 'Solo',
        window: 'Varies',
        fee: '',
        faculty: 'Dr. Nithisha',
        volunteer: 'Vaishnavi',
        volunteerPhone: '8778971695',
        rules: ['Individual participation only', 'Standard chess rules apply', 'Time control per round', 'No digital assistance allowed', 'Tournament bracket format', "Arbiter's decision is final"],
    },
]

function getGlow(hex) {
    const r = parseInt(hex.slice(1, 3), 16)
    const g = parseInt(hex.slice(3, 5), 16)
    const b = parseInt(hex.slice(5, 7), 16)
    return `rgba(${r},${g},${b},0.15)`
}

export default function NonTechEvents() {
    const [ref, inView] = useInView({ triggerOnce: true, threshold: 0.02 })

    return (
        <section
            id="nontech-events"
            ref={ref}
            className="relative overflow-hidden grid-overlay"
            style={{
                background: 'var(--bg-deep)',
                paddingTop: 'clamp(80px, 12vw, 140px)',
                paddingBottom: 'clamp(80px, 12vw, 140px)',
            }}
        >
            <div className="relative z-10 max-w-5xl mx-auto px-6 sm:px-10">
                <motion.div
                    initial={{ opacity: 0, y: 40 }}
                    animate={inView ? { opacity: 1, y: 0 } : {}}
                    transition={{ duration: 0.7 }}
                    className="text-center mb-5"
                >
                    <span className="section-tag inline-block" style={{
                        background: 'rgba(255, 0, 60, 0.05)',
                        borderColor: 'rgba(255, 0, 60, 0.2)',
                        color: 'var(--neon-red)',
                    }}>
                        {'>'} NON_TECH_EVENTS
                    </span>
                    <h2 className="section-title">
                        <GlitchText text="FUN. " color="var(--text-primary)" />
                        <GlitchText text="UNLEASHED." color="var(--neon-red)" />
                    </h2>
                </motion.div>

                <motion.p
                    initial={{ opacity: 0 }}
                    animate={inView ? { opacity: 1 } : {}}
                    transition={{ duration: 0.5, delay: 0.2 }}
                    className="section-subtitle mb-14"
                >
                    {'>'} Show off your creative side in these exciting non-technical events
                </motion.p>

                <div className="flex flex-col gap-5">
                    {nonTechEvents.map((event, i) => (
                        <motion.div
                            key={event.title}
                            initial={{ opacity: 0, y: 40 }}
                            animate={inView ? { opacity: 1, y: 0 } : {}}
                            transition={{ duration: 0.6, delay: 0.2 + i * 0.08 }}
                            className="cyber-card"
                            style={{
                                padding: 'clamp(20px, 4vw, 32px)',
                                borderColor: `${event.color}20`,
                                transition: 'all 0.4s ease',
                            }}
                            onMouseEnter={(e) => {
                                e.currentTarget.style.borderColor = `${event.color}50`
                                e.currentTarget.style.boxShadow = `0 0 40px ${getGlow(event.color)}`
                                e.currentTarget.style.transform = 'translateY(-3px)'
                            }}
                            onMouseLeave={(e) => {
                                e.currentTarget.style.borderColor = `${event.color}20`
                                e.currentTarget.style.boxShadow = 'none'
                                e.currentTarget.style.transform = 'translateY(0)'
                            }}
                        >
                            <div className="relative flex flex-col lg:flex-row gap-5 lg:gap-8">
                                <div className="lg:w-2/5 flex flex-col">
                                    <div className="flex items-center gap-3 mb-3">
                                        <span className="text-2xl">{event.icon}</span>
                                        <span style={{
                                            fontFamily: 'var(--font-mono)',
                                            fontSize: '0.6rem',
                                            color: event.color,
                                            letterSpacing: '2px',
                                            opacity: 0.6,
                                        }}>
                                            [FUN_{String(i + 1).padStart(2, '0')}]
                                        </span>
                                    </div>
                                    <h3 style={{
                                        fontFamily: 'var(--font-display)',
                                        fontSize: 'clamp(1.2rem, 2.5vw, 1.6rem)',
                                        fontWeight: 700,
                                        color: 'var(--text-primary)',
                                        letterSpacing: '1px',
                                        marginBottom: '0.6rem',
                                        textTransform: 'uppercase',
                                    }}>
                                        {event.title}
                                    </h3>
                                    <p style={{
                                        fontSize: '0.88rem',
                                        color: 'var(--text-secondary)',
                                        lineHeight: 1.7,
                                        fontFamily: 'var(--font-body)',
                                    }}>
                                        {event.brief}
                                    </p>
                                    <div className="flex flex-wrap gap-2 mt-3">
                                        {[
                                            { label: 'SQUAD', value: event.squad },
                                            { label: 'TIME', value: event.window },
                                            ...(event.fee ? [{ label: 'FEE', value: event.fee }] : []),
                                        ].map(b => (
                                            <div key={b.label} className="flex items-center gap-2 px-3 py-1.5"
                                                style={{
                                                    background: `${event.color}08`,
                                                    border: `1px solid ${event.color}15`,
                                                    borderRadius: '3px',
                                                }}>
                                                <span style={{
                                                    fontSize: '0.55rem',
                                                    color: 'var(--text-dim)',
                                                    fontFamily: 'var(--font-mono)',
                                                    letterSpacing: '1px',
                                                }}>{b.label}:</span>
                                                <span style={{
                                                    fontSize: '0.75rem',
                                                    color: 'var(--text-primary)',
                                                    fontFamily: 'var(--font-mono)',
                                                    fontWeight: 600,
                                                }}>{b.value}</span>
                                            </div>
                                        ))}
                                    </div>

                                    {/* Coordinator Info — Faculty first, then Volunteer */}
                                    {(event.faculty || event.volunteer) && (
                                        <div style={{
                                            marginTop: '14px',
                                            padding: '12px 14px',
                                            background: 'rgba(0, 10, 5, 0.6)',
                                            border: `1px solid ${event.color}12`,
                                            borderRadius: '4px',
                                        }}>
                                            <p style={{
                                                fontFamily: 'var(--font-mono)',
                                                fontSize: '0.6rem',
                                                color: event.color,
                                                letterSpacing: '2px',
                                                marginBottom: '8px',
                                                opacity: 0.7,
                                            }}>
                                                // COORDINATORS
                                            </p>
                                            <div className="flex flex-col gap-2">
                                                {/* Faculty — shown first */}
                                                {event.faculty && (
                                                    <div>
                                                        <span style={{
                                                            fontSize: '0.6rem',
                                                            color: 'var(--text-dim)',
                                                            fontFamily: 'var(--font-mono)',
                                                            letterSpacing: '1.5px',
                                                            display: 'block',
                                                            marginBottom: '2px',
                                                        }}>FACULTY:</span>
                                                        <span style={{
                                                            fontSize: '0.95rem',
                                                            color: 'var(--text-primary)',
                                                            fontFamily: 'var(--font-body)',
                                                            fontWeight: 700,
                                                        }}>
                                                            {event.faculty}
                                                        </span>
                                                    </div>
                                                )}
                                                {/* Volunteer — shown second */}
                                                {event.volunteer && (
                                                    <div>
                                                        <span style={{
                                                            fontSize: '0.6rem',
                                                            color: 'var(--text-dim)',
                                                            fontFamily: 'var(--font-mono)',
                                                            letterSpacing: '1.5px',
                                                            display: 'block',
                                                            marginBottom: '2px',
                                                        }}>VOLUNTEER:</span>
                                                        <div className="flex items-center gap-2 flex-wrap">
                                                            <span style={{
                                                                fontSize: '0.95rem',
                                                                color: 'var(--text-primary)',
                                                                fontFamily: 'var(--font-body)',
                                                                fontWeight: 700,
                                                            }}>
                                                                {event.volunteer}
                                                            </span>
                                                            {event.volunteerPhone && (
                                                                <a href={`tel:${event.volunteerPhone}`} className="flex items-center gap-1 no-underline"
                                                                    style={{ fontSize: '0.75rem', color: event.color, fontFamily: 'var(--font-mono)' }}>
                                                                    <HiPhone size={11} /> {event.volunteerPhone}
                                                                </a>
                                                            )}
                                                        </div>
                                                    </div>
                                                )}
                                            </div>
                                        </div>
                                    )}
                                </div>

                                <div className="lg:w-3/5">
                                    <p className="flex items-center gap-2 mb-3 text-xs"
                                        style={{
                                            color: event.color,
                                            fontFamily: 'var(--font-mono)',
                                            letterSpacing: '2px',
                                            fontWeight: 600,
                                        }}>
                                        {'>'} RULES_CONFIG
                                    </p>
                                    <div className="grid sm:grid-cols-2 gap-2">
                                        {event.rules.map((rule, ri) => (
                                            <motion.div
                                                key={ri}
                                                whileHover={{ x: 4, borderColor: `${event.color}30` }}
                                                className="flex items-start gap-2 p-2.5"
                                                style={{
                                                    background: 'rgba(0, 10, 5, 0.5)',
                                                    borderRadius: '3px',
                                                    border: `1px solid ${event.color}10`,
                                                }}
                                            >
                                                <span style={{
                                                    fontFamily: 'var(--font-mono)',
                                                    fontSize: '0.6rem',
                                                    color: event.color,
                                                    opacity: 0.6,
                                                    flexShrink: 0,
                                                    marginTop: '2px',
                                                }}>
                                                    [{String(ri + 1).padStart(2, '0')}]
                                                </span>
                                                <p className="text-xs leading-snug" style={{
                                                    color: 'var(--text-secondary)',
                                                    fontFamily: 'var(--font-body)',
                                                }}>
                                                    {rule}
                                                </p>
                                            </motion.div>
                                        ))}
                                    </div>
                                    <motion.a
                                        href="https://forms.google.com"
                                        target="_blank" rel="noopener noreferrer"
                                        whileHover={{ scale: 1.05 }}
                                        whileTap={{ scale: 0.95 }}
                                        className="inline-flex items-center gap-2 px-6 py-2.5 mt-5 text-xs cursor-pointer no-underline"
                                        style={{
                                            background: event.color,
                                            color: '#000',
                                            borderRadius: '3px',
                                            fontFamily: 'var(--font-mono)',
                                            fontWeight: 700,
                                            letterSpacing: '1.5px',
                                            textTransform: 'uppercase',
                                            boxShadow: `0 0 20px ${getGlow(event.color)}`,
                                        }}>
                                        REGISTER_NOW <HiArrowRight />
                                    </motion.a>
                                </div>
                            </div>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    )
}

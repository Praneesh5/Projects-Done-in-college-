import { motion } from 'framer-motion'
import { useInView } from 'react-intersection-observer'
import { HiArrowRight, HiPhone } from 'react-icons/hi'
import GlitchText from './GlitchText'

const techEvents = [
    {
        title: 'Paper Presentation',
        brief: 'Present your research papers on cutting-edge topics in technology and innovation.',
        icon: '📄',
        color: '#00FF41',
        squad: 'Solo / Team (Max 2)',
        window: '8–10 mins',
        fee: '₹200',
        prize: '₹3000',
        faculty: 'Dr. Jaithunbi A K',
        volunteer: 'M. Tharun Kumar',
        volunteerPhone: '8248471603',
        rules: ['Topics: CS or IT', 'Max 2 members', 'PPT 24hrs before event', 'No plagiarism', 'Judging: Content, Delivery, Q&A', 'Time: 8-10 mins per team'],
    },
    {
        title: 'Logo Design',
        brief: 'Unleash your creativity and design stunning logos in a time-bound challenge.',
        icon: '🎨',
        color: '#FF00A0',
        squad: 'Solo',
        window: '60 mins',
        fee: '',
        prize: '',
        faculty: 'Dr. S. Aghalya',
        volunteer: '',
        volunteerPhone: '',
        rules: ['Individual only', 'Use: Illustrator/Photoshop/Canva/Figma', 'Theme on the spot', 'No pre-made templates', 'Judging: Creativity, Typography', 'Output: PNG/SVG'],
    },
    {
        title: 'Build a Website',
        brief: 'Build a fully functional, responsive website from scratch within the given time.',
        icon: '💻',
        color: '#00F0FF',
        squad: 'Solo / Duo',
        window: '90 mins',
        fee: '₹100 per team',
        prize: '₹1000',
        faculty: 'Dr. V. Suresh Kumar',
        volunteer: 'Dhivakaran D',
        volunteerPhone: '9123526614',
        rules: ['Team: 1-2 members', 'HTML/CSS/JS (frameworks OK)', 'Topic on the spot', 'No templates or copy-paste', 'Judging: Design, Responsive, Function', 'Hosted demo preferred'],
    },
    {
        title: 'Project Expo',
        brief: 'Display your innovative hardware or software projects and get expert evaluation.',
        icon: '🚀',
        color: '#FFB800',
        squad: 'Team (Max 4)',
        window: '10 mins',
        fee: '₹300 per team',
        prize: '₹2000',
        faculty: 'Dr. Nithisha J',
        volunteer: 'Tamil Selvan R',
        volunteerPhone: '7604802220',
        rules: ['Up to 4 members', 'HW/SW projects accepted', 'Working demo required', 'Project report (abstract)', 'Judging: Innovation, Feasibility', 'Power & tables provided'],
    },
    {
        title: 'Video Editing & Photography',
        brief: 'Create captivating videos, reels, and photographs that tell a story with cinematic flair.',
        icon: '🎬',
        color: '#BF00FF',
        squad: 'Solo / Duo',
        window: '2–5 mins',
        fee: '',
        prize: '',
        faculty: '',
        volunteer: '',
        volunteerPhone: '',
        rules: ['Solo or duo', 'Topic provided on spot', '30 secs to 5 mins max', 'Any editing software', 'Royalty-free music only', 'Judging: Story, Edit, Visual'],
    },
]

function getGlow(hex) {
    const r = parseInt(hex.slice(1, 3), 16)
    const g = parseInt(hex.slice(3, 5), 16)
    const b = parseInt(hex.slice(5, 7), 16)
    return `rgba(${r},${g},${b},0.15)`
}

export default function TechEvents() {
    const [ref, inView] = useInView({ triggerOnce: true, threshold: 0.02 })

    return (
        <section
            id="tech-events"
            ref={ref}
            className="relative overflow-hidden"
            style={{
                background: 'var(--bg-void)',
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
                        background: 'rgba(0, 255, 65, 0.05)',
                        borderColor: 'rgba(0, 255, 65, 0.2)',
                    }}>
                        {'>'} TECHNICAL_EVENTS
                    </span>
                    <h2 className="section-title">
                        <GlitchText text="COMPETE. " color="var(--text-primary)" />
                        <GlitchText text="INNOVATE." color="var(--neon-green)" />
                    </h2>
                </motion.div>

                <motion.p
                    initial={{ opacity: 0 }}
                    animate={inView ? { opacity: 1 } : {}}
                    transition={{ duration: 0.5, delay: 0.2 }}
                    className="section-subtitle mb-14"
                >
                    {'>'} Showcase your technical prowess in these challenging events
                </motion.p>

                <div className="flex flex-col gap-5">
                    {techEvents.map((event, i) => (
                        <motion.div
                            key={event.title}
                            initial={{ opacity: 0, y: 40 }}
                            animate={inView ? { opacity: 1, y: 0 } : {}}
                            transition={{ duration: 0.6, delay: 0.2 + i * 0.08 }}
                            className="cyber-card group"
                            style={{
                                padding: 'clamp(20px, 4vw, 32px)',
                                borderColor: `${event.color}20`,
                            }}
                            onMouseEnter={(e) => {
                                e.currentTarget.style.borderColor = `${event.color}50`
                                e.currentTarget.style.boxShadow = `0 0 40px ${getGlow(event.color)}`
                            }}
                            onMouseLeave={(e) => {
                                e.currentTarget.style.borderColor = `${event.color}20`
                                e.currentTarget.style.boxShadow = 'none'
                            }}
                        >
                            <div className="relative flex flex-col lg:flex-row gap-5 lg:gap-8">
                                {/* Left */}
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
                                            [EVENT_{String(i + 1).padStart(2, '0')}]
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
                                            ...(event.prize ? [{ label: 'PRIZE', value: event.prize }] : []),
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

                                {/* Right — Rules */}
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

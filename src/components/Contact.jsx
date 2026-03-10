import { useState } from 'react'
import { motion } from 'framer-motion'
import { useInView } from 'react-intersection-observer'
import { HiArrowRight } from 'react-icons/hi'
import { BsInstagram, BsLinkedin, BsYoutube, BsTwitterX } from 'react-icons/bs'
import GlitchText from './GlitchText'

const socialLinks = [
    { icon: <BsInstagram size={16} />, href: '#', label: 'Instagram', color: '#e1306c' },
    { icon: <BsLinkedin size={16} />, href: '#', label: 'LinkedIn', color: '#0077b5' },
    { icon: <BsYoutube size={16} />, href: '#', label: 'YouTube', color: '#ff0000' },
    { icon: <BsTwitterX size={16} />, href: '#', label: 'Twitter', color: '#fff' },
]

export default function Contact() {
    const [ref, inView] = useInView({ triggerOnce: true, threshold: 0.05 })
    const [formData, setFormData] = useState({ name: '', email: '', message: '' })

    const handleSubmit = (e) => {
        e.preventDefault()
        const subject = encodeURIComponent(`INTELLEX 2026 Inquiry from ${formData.name}`)
        const body = encodeURIComponent(`Name: ${formData.name}\nEmail: ${formData.email}\n\n${formData.message}`)
        window.open(`mailto:intelligencesystems.simats@gmail.com?subject=${subject}&body=${body}`)
    }

    return (
        <>
            <section
                id="contact"
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
                            color: 'var(--neon-cyan)',
                            borderColor: 'rgba(0, 240, 255, 0.2)',
                            background: 'rgba(0, 240, 255, 0.05)',
                        }}>
                            // ESTABLISH_LINK
                        </span>
                        <h2 className="section-title">
                            <GlitchText text="CONTACT " color="var(--text-primary)" />
                            <GlitchText text="US" color="var(--neon-cyan)" />
                        </h2>
                    </motion.div>

                    <motion.p
                        initial={{ opacity: 0 }}
                        animate={inView ? { opacity: 1 } : {}}
                        transition={{ duration: 0.5, delay: 0.2 }}
                        className="section-subtitle mb-14"
                    >
                        {'>'} Have questions? Open a secure channel to reach us.
                    </motion.p>

                    <div className="grid lg:grid-cols-2 gap-6">
                        {/* Form */}
                        <motion.div
                            initial={{ opacity: 0, x: -30 }}
                            animate={inView ? { opacity: 1, x: 0 } : {}}
                            transition={{ duration: 0.6, delay: 0.2 }}
                        >
                            <form onSubmit={handleSubmit} className="terminal-box p-6 flex flex-col gap-4">
                                <h3 className="text-sm font-bold mb-1" style={{
                                    fontFamily: 'var(--font-display)',
                                    color: 'var(--neon-green)',
                                    letterSpacing: '2px',
                                    textTransform: 'uppercase',
                                }}>
                                    {'>'} SEND_MESSAGE
                                </h3>
                                {[
                                    { label: 'ALIAS', type: 'text', key: 'name', placeholder: 'enter_your_name' },
                                    { label: 'EMAIL', type: 'email', key: 'email', placeholder: 'you@domain.com' },
                                ].map(field => (
                                    <div key={field.key}>
                                        <label className="text-xs font-semibold mb-2 block" style={{
                                            color: 'var(--text-dim)',
                                            fontFamily: 'var(--font-mono)',
                                            fontSize: '0.7rem',
                                            letterSpacing: '2px',
                                        }}>
                                            {field.label}:
                                        </label>
                                        <input
                                            type={field.type} required
                                            value={formData[field.key]}
                                            onChange={(e) => setFormData({ ...formData, [field.key]: e.target.value })}
                                            className="w-full px-4 py-2.5 text-sm outline-none transition-all duration-300"
                                            placeholder={field.placeholder}
                                            style={{
                                                background: 'rgba(0, 255, 65, 0.03)',
                                                border: '1px solid rgba(0, 255, 65, 0.1)',
                                                borderRadius: '3px',
                                                color: 'var(--text-primary)',
                                                fontFamily: 'var(--font-mono)',
                                                fontSize: '0.8rem',
                                            }}
                                            onFocus={(e) => {
                                                e.target.style.borderColor = 'var(--neon-green)'
                                                e.target.style.boxShadow = '0 0 10px rgba(0,255,65,0.1)'
                                            }}
                                            onBlur={(e) => {
                                                e.target.style.borderColor = 'rgba(0,255,65,0.1)'
                                                e.target.style.boxShadow = 'none'
                                            }}
                                        />
                                    </div>
                                ))}
                                <div>
                                    <label className="text-xs font-semibold mb-2 block" style={{
                                        color: 'var(--text-dim)',
                                        fontFamily: 'var(--font-mono)',
                                        fontSize: '0.7rem',
                                        letterSpacing: '2px',
                                    }}>
                                        PAYLOAD:
                                    </label>
                                    <textarea
                                        required rows={3}
                                        value={formData.message}
                                        onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                                        className="w-full px-4 py-2.5 text-sm outline-none transition-all duration-300 resize-none"
                                        placeholder="type_your_message..."
                                        style={{
                                            background: 'rgba(0, 255, 65, 0.03)',
                                            border: '1px solid rgba(0, 255, 65, 0.1)',
                                            borderRadius: '3px',
                                            color: 'var(--text-primary)',
                                            fontFamily: 'var(--font-mono)',
                                            fontSize: '0.8rem',
                                        }}
                                        onFocus={(e) => {
                                            e.target.style.borderColor = 'var(--neon-green)'
                                            e.target.style.boxShadow = '0 0 10px rgba(0,255,65,0.1)'
                                        }}
                                        onBlur={(e) => {
                                            e.target.style.borderColor = 'rgba(0,255,65,0.1)'
                                            e.target.style.boxShadow = 'none'
                                        }}
                                    />
                                </div>
                                <button type="submit" className="btn-solid justify-center w-full" style={{ marginTop: '8px' }}>
                                    TRANSMIT <HiArrowRight />
                                </button>
                            </form>
                        </motion.div>

                        {/* Info + Map */}
                        <motion.div
                            initial={{ opacity: 0, x: 30 }}
                            animate={inView ? { opacity: 1, x: 0 } : {}}
                            transition={{ duration: 0.6, delay: 0.3 }}
                            className="flex flex-col gap-3"
                        >
                            {[
                                { label: 'EMAIL_ADDR', value: 'intelligencesystems.simats@gmail.com', color: 'var(--neon-green)', icon: '📧' },
                                { label: 'PHONE_LINE', value: '+91 9791082080 / +91 8754419740', color: 'var(--neon-cyan)', icon: '📱' },
                                { label: 'COORDINATES', value: 'SIMATS Engineering, Chennai, TN', color: 'var(--neon-amber)', icon: '📍' },
                            ].map((item) => (
                                <motion.div key={item.label}
                                    whileHover={{ x: 4 }}
                                    className="flex items-center gap-3 p-4 cyber-card"
                                    style={{ borderColor: `${item.color === 'var(--neon-green)' ? 'rgba(0,255,65,0.1)' : item.color === 'var(--neon-cyan)' ? 'rgba(0,240,255,0.1)' : 'rgba(255,184,0,0.1)'}` }}
                                >
                                    <div className="w-10 h-10 flex items-center justify-center flex-shrink-0 text-lg"
                                        style={{
                                            border: '1px solid rgba(0,255,65,0.15)',
                                            borderRadius: '3px',
                                            background: 'rgba(0,255,65,0.03)',
                                        }}>
                                        {item.icon}
                                    </div>
                                    <div>
                                        <p className="text-xs mb-0.5" style={{
                                            color: 'var(--text-dim)',
                                            fontFamily: 'var(--font-mono)',
                                            letterSpacing: '2px',
                                            fontSize: '0.6rem',
                                        }}>
                                            {item.label}:
                                        </p>
                                        <p className="font-semibold text-xs" style={{
                                            color: 'var(--text-primary)',
                                            fontFamily: 'var(--font-mono)',
                                        }}>
                                            {item.value}
                                        </p>
                                    </div>
                                </motion.div>
                            ))}

                            <div className="overflow-hidden flex-grow cyber-card" style={{
                                minHeight: '180px',
                                borderColor: 'rgba(0,255,65,0.1)',
                            }}>
                                <iframe
                                    src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3888.853!2d80.1644!3d12.9279!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3a525fdb4a20b0a1%3A0x5db5e0b7c3bfc14a!2sSaveetha%20Institute%20of%20Medical%20and%20Technical%20Sciences!5e0!3m2!1sen!2sin!4v1700000000000!5m2!1sen!2sin"
                                    width="100%" height="100%"
                                    style={{
                                        border: 0,
                                        minHeight: '180px',
                                        borderRadius: '8px',
                                        filter: 'invert(90%) hue-rotate(180deg) brightness(0.8) contrast(1.2)',
                                    }}
                                    allowFullScreen="" loading="lazy"
                                    referrerPolicy="no-referrer-when-downgrade"
                                    title="SIMATS Engineering Location"
                                />
                            </div>
                        </motion.div>
                    </div>

                    {/* Social */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={inView ? { opacity: 1, y: 0 } : {}}
                        transition={{ duration: 0.5, delay: 0.5 }}
                        className="flex justify-center gap-3 mt-10"
                    >
                        {socialLinks.map((social) => (
                            <motion.a key={social.label} href={social.href} target="_blank" rel="noopener noreferrer"
                                whileHover={{ scale: 1.15, y: -3 }}
                                whileTap={{ scale: 0.95 }}
                                className="w-9 h-9 flex items-center justify-center no-underline"
                                style={{
                                    background: 'transparent',
                                    border: '1px solid rgba(0,255,65,0.15)',
                                    borderRadius: '3px',
                                    color: 'var(--text-dim)',
                                    transition: 'all 0.3s',
                                }}
                                onMouseEnter={(e) => {
                                    e.currentTarget.style.color = social.color
                                    e.currentTarget.style.borderColor = social.color
                                    e.currentTarget.style.boxShadow = `0 0 15px ${social.color}30`
                                }}
                                onMouseLeave={(e) => {
                                    e.currentTarget.style.color = 'var(--text-dim)'
                                    e.currentTarget.style.borderColor = 'rgba(0,255,65,0.15)'
                                    e.currentTarget.style.boxShadow = 'none'
                                }}
                                title={social.label}>
                                {social.icon}
                            </motion.a>
                        ))}
                    </motion.div>
                </div>
            </section>

            {/* Footer */}
            <footer className="relative py-6 text-center"
                style={{
                    background: 'var(--bg-void)',
                    borderTop: '1px solid rgba(0,255,65,0.06)',
                }}>
                <div className="max-w-6xl mx-auto px-6">
                    <p className="text-xs" style={{
                        color: 'var(--text-dim)',
                        fontFamily: 'var(--font-mono)',
                        letterSpacing: '1px',
                    }}>
                        © 2026 INTELLEX_SYS · SIMATS ENGINEERING · ALL_RIGHTS_RESERVED
                    </p>
                    <p className="text-xs mt-1" style={{
                        color: 'var(--text-dim)',
                        opacity: 0.4,
                        fontFamily: 'var(--font-mono)',
                        fontSize: '0.6rem',
                    }}>
                        {'>'} SYSTEM DESIGNED FOR THE HACKERS OF TOMORROW
                    </p>
                </div>
            </footer>
        </>
    )
}

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { HiMenu, HiX } from 'react-icons/hi'

const navItems = [
    { name: 'Home', href: '#home' },
    { name: 'About', href: '#about' },
    { name: 'Technical', href: '#tech-events' },
    { name: 'Non-Tech', href: '#nontech-events' },
    { name: 'Team', href: '#coordinators' },
    { name: 'Contact', href: '#contact' },
]

export default function Navbar() {
    const [scrolled, setScrolled] = useState(false)
    const [mobileOpen, setMobileOpen] = useState(false)
    const [activeSection, setActiveSection] = useState('home')

    useEffect(() => {
        const handleScroll = () => {
            setScrolled(window.scrollY > 50)
            const sections = navItems.map(item => item.href.slice(1))
            for (let i = sections.length - 1; i >= 0; i--) {
                const el = document.getElementById(sections[i])
                if (el && el.getBoundingClientRect().top <= 150) {
                    setActiveSection(sections[i])
                    break
                }
            }
        }
        window.addEventListener('scroll', handleScroll)
        return () => window.removeEventListener('scroll', handleScroll)
    }, [])

    return (
        <motion.nav
            initial={{ y: -100 }}
            animate={{ y: 0 }}
            transition={{ duration: 0.6, ease: 'easeOut' }}
            className={`fixed top-0 left-0 w-full z-50 transition-all duration-500 ${scrolled ? 'py-2' : 'py-3'}`}
            style={{
                background: scrolled ? 'rgba(0, 0, 0, 0.85)' : 'transparent',
                backdropFilter: scrolled ? 'blur(20px)' : 'none',
                borderBottom: scrolled ? '1px solid rgba(0, 255, 65, 0.1)' : 'none',
            }}
        >
            <div className="max-w-7xl mx-auto px-5 sm:px-8 flex items-center justify-between">
                {/* Logo */}
                <motion.a href="#home" className="flex items-center gap-3 no-underline" whileHover={{ scale: 1.05 }}>
                    <div className="w-9 h-9 flex items-center justify-center font-black text-xs"
                        style={{
                            border: '1px solid var(--neon-green)',
                            borderRadius: '4px',
                            color: 'var(--neon-green)',
                            fontFamily: 'var(--font-display)',
                            fontSize: '0.7rem',
                            letterSpacing: '1px',
                            boxShadow: '0 0 10px rgba(0,255,65,0.2)',
                        }}>
                        IX
                    </div>
                    <div className="hidden sm:flex flex-col">
                        <span style={{
                            fontFamily: 'var(--font-display)',
                            color: 'var(--neon-green)',
                            fontWeight: 700,
                            fontSize: '0.85rem',
                            lineHeight: 1.2,
                            letterSpacing: '2px',
                            textShadow: '0 0 10px rgba(0,255,65,0.3)',
                        }}>
                            INTELLEX
                        </span>
                        <span style={{
                            fontFamily: 'var(--font-mono)',
                            fontSize: '0.55rem',
                            letterSpacing: '3px',
                            color: 'var(--text-dim)',
                        }}>
                            SYS_2026
                        </span>
                    </div>
                </motion.a>

                {/* Desktop Nav */}
                <div className="hidden lg:flex items-center gap-1 p-1"
                    style={{
                        background: 'rgba(0, 10, 5, 0.6)',
                        border: '1px solid rgba(0, 255, 65, 0.08)',
                        borderRadius: '4px',
                        backdropFilter: 'blur(10px)',
                    }}>
                    {navItems.map((item) => (
                        <a key={item.name} href={item.href}
                            className="relative px-4 py-2 text-xs no-underline transition-all duration-300"
                            style={{
                                fontFamily: 'var(--font-mono)',
                                fontWeight: 600,
                                letterSpacing: '1.5px',
                                textTransform: 'uppercase',
                                borderRadius: '2px',
                                color: activeSection === item.href.slice(1) ? '#000' : 'var(--text-secondary)',
                                background: activeSection === item.href.slice(1) ? 'var(--neon-green)' : 'transparent',
                                boxShadow: activeSection === item.href.slice(1) ? '0 0 15px rgba(0,255,65,0.3)' : 'none',
                            }}>
                            {item.name}
                        </a>
                    ))}
                </div>

                {/* Right Controls */}
                <div className="flex items-center gap-3">
                    <a href="#contact"
                        className="hidden lg:inline-flex items-center gap-2 px-5 py-2 text-xs font-bold no-underline transition-all duration-300"
                        style={{
                            fontFamily: 'var(--font-mono)',
                            background: 'transparent',
                            color: 'var(--neon-red)',
                            border: '1px solid var(--neon-red)',
                            borderRadius: '2px',
                            letterSpacing: '1.5px',
                            textTransform: 'uppercase',
                        }}
                        onMouseEnter={(e) => {
                            e.currentTarget.style.background = 'rgba(255,0,60,0.1)'
                            e.currentTarget.style.boxShadow = '0 0 20px rgba(255,0,60,0.2)'
                        }}
                        onMouseLeave={(e) => {
                            e.currentTarget.style.background = 'transparent'
                            e.currentTarget.style.boxShadow = 'none'
                        }}>
                        [CONNECT]
                    </a>

                    <motion.button
                        whileTap={{ scale: 0.9 }}
                        onClick={() => setMobileOpen(!mobileOpen)}
                        className="lg:hidden w-9 h-9 flex items-center justify-center cursor-pointer"
                        style={{
                            background: 'transparent',
                            border: '1px solid rgba(0,255,65,0.3)',
                            borderRadius: '2px',
                            color: 'var(--neon-green)',
                        }}>
                        {mobileOpen ? <HiX size={18} /> : <HiMenu size={18} />}
                    </motion.button>
                </div>
            </div>

            {/* Mobile Menu */}
            <AnimatePresence>
                {mobileOpen && (
                    <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        transition={{ duration: 0.3 }}
                        className="lg:hidden overflow-hidden"
                        style={{
                            background: 'rgba(0, 0, 0, 0.95)',
                            backdropFilter: 'blur(20px)',
                            borderTop: '1px solid rgba(0,255,65,0.1)',
                        }}>
                        <div className="px-5 py-3 flex flex-col gap-1">
                            {navItems.map((item, index) => (
                                <motion.a key={item.name} href={item.href}
                                    initial={{ opacity: 0, x: -20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: index * 0.04 }}
                                    onClick={() => setMobileOpen(false)}
                                    className="px-4 py-2.5 text-xs font-semibold no-underline"
                                    style={{
                                        fontFamily: 'var(--font-mono)',
                                        letterSpacing: '2px',
                                        textTransform: 'uppercase',
                                        borderRadius: '2px',
                                        color: activeSection === item.href.slice(1) ? 'var(--neon-green)' : 'var(--text-dim)',
                                        background: activeSection === item.href.slice(1) ? 'rgba(0,255,65,0.05)' : 'transparent',
                                    }}>
                                    {'> '}{item.name}
                                </motion.a>
                            ))}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </motion.nav>
    )
}

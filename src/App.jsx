import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import Navbar from './components/Navbar'
import Hero from './components/Hero'
import About from './components/About'
import TechEvents from './components/TechEvents'
import NonTechEvents from './components/NonTechEvents'
import Coordinators from './components/Coordinators'
import Contact from './components/Contact'
import WhatsAppButton from './components/WhatsAppButton'
import MatrixRain from './components/MatrixRain'

/* ── Hacker Loading Screen ── */
function LoadingScreen() {
    const [lines, setLines] = useState([])
    const bootSequence = [
        '> INITIALIZING SYSTEM...',
        '> LOADING KERNEL MODULES...',
        '> ESTABLISHING SECURE CONNECTION...',
        '> DECRYPTING PAYLOAD...',
        '> BYPASSING FIREWALL...',
        '> ACCESS GRANTED ██████████ 100%',
        '> WELCOME TO INTELLEX_2026',
    ]

    useEffect(() => {
        let i = 0
        const interval = setInterval(() => {
            if (i < bootSequence.length) {
                setLines((prev) => [...prev, bootSequence[i]])
                i++
            }
        }, 250)
        return () => clearInterval(interval)
    }, [])

    return (
        <div
            style={{
                position: 'fixed',
                inset: 0,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                background: '#000',
                zIndex: 9999,
            }}
        >
            <div style={{
                maxWidth: '500px',
                width: '90%',
                padding: '30px',
                border: '1px solid rgba(0,255,65,0.2)',
                borderRadius: '4px',
                background: 'rgba(0,10,5,0.95)',
            }}>
                <div style={{
                    fontFamily: "'Share Tech Mono', monospace",
                    fontSize: '0.8rem',
                    color: '#00FF41',
                    marginBottom: '20px',
                    textShadow: '0 0 10px rgba(0,255,65,0.5)',
                }}>
                    INTELLEX_SYSTEM v2.026
                </div>
                {lines.map((line, idx) => (
                    <motion.div
                        key={idx}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.2 }}
                        style={{
                            fontFamily: "'Share Tech Mono', monospace",
                            fontSize: '0.72rem',
                            color: idx === lines.length - 1 ? '#00FF41' : 'rgba(0,255,65,0.5)',
                            marginBottom: '6px',
                            textShadow: idx === lines.length - 1 ? '0 0 10px rgba(0,255,65,0.5)' : 'none',
                        }}
                    >
                        {line}
                    </motion.div>
                ))}
                <motion.div
                    animate={{ opacity: [1, 0, 1] }}
                    transition={{ duration: 0.8, repeat: Infinity }}
                    style={{
                        width: '8px',
                        height: '14px',
                        background: '#00FF41',
                        marginTop: '8px',
                        boxShadow: '0 0 8px #00FF41',
                    }}
                />
            </div>
        </div>
    )
}

/* ── Section Divider ── */
function SectionDivider() {
    return (
        <div style={{ maxWidth: '800px', margin: '0 auto', padding: '0 24px' }}>
            <div style={{
                width: '100%',
                height: '1px',
                background: 'linear-gradient(90deg, transparent, rgba(0,255,65,0.2), transparent)',
            }} />
        </div>
    )
}

export default function App() {
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const timer = setTimeout(() => setLoading(false), 2200)
        return () => clearTimeout(timer)
    }, [])

    return (
        <div className="scanlines">
            <AnimatePresence>
                {loading && (
                    <motion.div key="loader" exit={{ opacity: 0 }} transition={{ duration: 0.5 }}>
                        <LoadingScreen />
                    </motion.div>
                )}
            </AnimatePresence>

            {!loading && (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.6 }}>
                    {/* Single lightweight background */}
                    <MatrixRain />

                    <Navbar />

                    <main style={{ position: 'relative', zIndex: 2 }}>
                        <Hero />
                        <SectionDivider />
                        <About />
                        <SectionDivider />
                        <TechEvents />
                        <SectionDivider />
                        <NonTechEvents />
                        <SectionDivider />
                        <Coordinators />
                        <SectionDivider />
                        <Contact />
                    </main>

                    <WhatsAppButton />
                </motion.div>
            )}
        </div>
    )
}

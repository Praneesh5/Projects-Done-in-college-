import { motion } from 'framer-motion'
import { BsWhatsapp } from 'react-icons/bs'

export default function WhatsAppButton() {
    return (
        <motion.a
            href="https://wa.me/919791082080?text=Hi!%20I'm%20interested%20in%20INTELLEX%202026.%20Can%20you%20share%20more%20details?"
            target="_blank"
            rel="noopener noreferrer"
            className="whatsapp-float"
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 2.5, type: 'spring', stiffness: 200 }}
            whileHover={{ scale: 1.15 }}
            whileTap={{ scale: 0.9 }}
            title="Chat on WhatsApp"
        >
            <BsWhatsapp size={26} />
        </motion.a>
    )
}

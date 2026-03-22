import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { Zap } from "lucide-react";
import { Button } from "@/components/ui/button";

const Navbar = () => {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <motion.nav
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.5 }}
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled ? "glass-strong shadow-lg" : "bg-transparent"
      }`}
    >
      <div className="container mx-auto flex items-center justify-between h-16 px-6">
        <Link to="/" className="flex items-center gap-2 group">
          <div className="w-8 h-8 rounded-lg gradient-primary flex items-center justify-center glow-primary">
            <Zap className="w-4 h-4 text-foreground" />
          </div>
          <span className="text-lg font-bold text-foreground tracking-tight">
            TrustScore <span className="gradient-text">AI</span>
          </span>
        </Link>

        <div className="hidden md:flex items-center gap-8">
          <a href="#features" className="text-sm text-muted-foreground hover:text-foreground transition-colors">Features</a>
          <a href="#wow" className="text-sm text-muted-foreground hover:text-foreground transition-colors">Highlights</a>
          <a href="#about" className="text-sm text-muted-foreground hover:text-foreground transition-colors">About</a>
        </div>

        <div className="flex items-center gap-3">
          <Button variant="hero-outline" size="sm" asChild>
            <Link to="/dashboard">Dashboard</Link>
          </Button>
        </div>
      </div>
    </motion.nav>
  );
};

export default Navbar;

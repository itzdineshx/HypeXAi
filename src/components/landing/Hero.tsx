import { motion } from "framer-motion";
import { ArrowRight, Play } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";

const ParticleGrid = () => (
  <div className="absolute inset-0 overflow-hidden pointer-events-none">
    {/* Gradient orbs */}
    <div className="absolute top-1/4 left-1/4 w-[500px] h-[500px] rounded-full bg-primary/5 blur-[120px] animate-pulse-glow" />
    <div className="absolute bottom-1/4 right-1/4 w-[400px] h-[400px] rounded-full bg-secondary/5 blur-[120px] animate-pulse-glow" style={{ animationDelay: "1.5s" }} />
    {/* Grid lines */}
    <div className="absolute inset-0 opacity-[0.03]" style={{
      backgroundImage: `linear-gradient(hsl(var(--primary)) 1px, transparent 1px), linear-gradient(90deg, hsl(var(--primary)) 1px, transparent 1px)`,
      backgroundSize: "60px 60px",
    }} />
  </div>
);

const Hero = () => (
  <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
    <ParticleGrid />
    <div className="container mx-auto px-6 pt-20 relative z-10">
      <div className="max-w-4xl mx-auto text-center">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <div className="inline-flex items-center gap-2 glass rounded-full px-4 py-1.5 mb-8 text-xs font-medium text-muted-foreground">
            <span className="w-2 h-2 rounded-full bg-success animate-pulse" />
            Live • Analyzing 12,847 tokens in real-time
          </div>
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.1 }}
          className="text-5xl md:text-7xl font-black tracking-tight leading-[1.05] mb-6"
        >
          Don't Follow Crypto Hype.{" "}
          <span className="gradient-text text-glow">Understand It.</span>
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto mb-10 leading-relaxed"
        >
          AI-powered platform to detect trends, identify manipulation, and analyze meme coin markets in real time.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.3 }}
          className="flex flex-col sm:flex-row items-center justify-center gap-4"
        >
          <Button variant="hero" size="lg" asChild className="text-base px-8 py-6">
            <Link to="/dashboard">
              Explore Dashboard
              <ArrowRight className="w-4 h-4 ml-1" />
            </Link>
          </Button>
          <Button variant="hero-outline" size="lg" asChild className="text-base px-8 py-6">
            <Link to="/dashboard">
              <Play className="w-4 h-4 mr-1" />
              View Live Trends
            </Link>
          </Button>
        </motion.div>

        {/* Floating metric preview */}
        <motion.div
          initial={{ opacity: 0, y: 60 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1, delay: 0.6 }}
          className="mt-20 grid grid-cols-3 gap-4 max-w-xl mx-auto"
        >
          {[
            { label: "Trust Score", value: "87%", color: "text-success" },
            { label: "Tokens Tracked", value: "12.8K", color: "text-primary" },
            { label: "Alerts Today", value: "24", color: "text-warning" },
          ].map((m) => (
            <div key={m.label} className="glass rounded-xl p-4 text-center glow-border">
              <div className={`text-2xl font-bold font-mono ${m.color}`}>{m.value}</div>
              <div className="text-xs text-muted-foreground mt-1">{m.label}</div>
            </div>
          ))}
        </motion.div>
      </div>
    </div>
  </section>
);

export default Hero;

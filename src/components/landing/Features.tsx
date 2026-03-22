import { motion } from "framer-motion";
import { TrendingUp, ShieldCheck, AlertTriangle } from "lucide-react";

const features = [
  {
    icon: TrendingUp,
    title: "Trend Detection",
    description: "Identify emerging meme coin trends from social signals before the crowd catches on.",
  },
  {
    icon: ShieldCheck,
    title: "Trust Score",
    description: "Evaluate the reliability of hype using AI-driven scoring across multiple data sources.",
  },
  {
    icon: AlertTriangle,
    title: "Risk Alerts",
    description: "Detect pump-and-dump patterns and market manipulation in real time.",
  },
];

const Features = () => (
  <section id="features" className="py-32 relative">
    <div className="container mx-auto px-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="text-center mb-16"
      >
        <h2 className="text-3xl md:text-4xl font-bold mb-4">
          Intelligence at <span className="gradient-text">Every Layer</span>
        </h2>
        <p className="text-muted-foreground max-w-lg mx-auto">
          Three pillars of crypto intelligence, powered by cutting-edge AI.
        </p>
      </motion.div>

      <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto">
        {features.map((f, i) => (
          <motion.div
            key={f.title}
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.15 }}
            className="glass rounded-2xl p-8 group hover:glow-border transition-all duration-500"
          >
            <div className="w-12 h-12 rounded-xl gradient-primary flex items-center justify-center mb-5 group-hover:scale-110 transition-transform duration-300">
              <f.icon className="w-6 h-6 text-foreground" />
            </div>
            <h3 className="text-lg font-semibold mb-3 text-foreground">{f.title}</h3>
            <p className="text-sm text-muted-foreground leading-relaxed">{f.description}</p>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

export default Features;

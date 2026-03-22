import { motion } from "framer-motion";
import { Play, Pause, SkipBack } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";

const HypeReplayPreview = () => {
  const [playing, setPlaying] = useState(false);
  const [progress, setProgress] = useState(35);
  
  const dataPoints = [20, 25, 22, 30, 45, 80, 95, 72, 55, 40, 35, 50, 68, 85, 60];

  return (
    <div className="glass rounded-2xl p-6 glow-border">
      <div className="flex items-center justify-between mb-4">
        <h4 className="text-sm font-semibold text-foreground">$PEPE Hype Timeline</h4>
        <span className="text-xs font-mono text-muted-foreground">Jan 15 – Feb 12, 2026</span>
      </div>
      {/* Chart area */}
      <div className="h-32 flex items-end gap-1 mb-4">
        {dataPoints.map((h, i) => (
          <motion.div
            key={i}
            className="flex-1 rounded-t-sm"
            style={{
              background: i <= Math.floor((progress / 100) * dataPoints.length)
                ? `linear-gradient(to top, hsl(var(--primary)), hsl(var(--secondary)))`
                : "hsl(var(--muted))",
              opacity: i <= Math.floor((progress / 100) * dataPoints.length) ? 1 : 0.3,
            }}
            initial={{ height: 0 }}
            whileInView={{ height: `${h}%` }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.05, duration: 0.4 }}
          />
        ))}
      </div>
      {/* Controls */}
      <div className="flex items-center gap-3">
        <Button
          variant="ghost"
          size="icon"
          className="w-8 h-8"
          onClick={() => { setProgress(0); setPlaying(false); }}
        >
          <SkipBack className="w-3.5 h-3.5" />
        </Button>
        <Button
          variant="ghost"
          size="icon"
          className="w-8 h-8"
          onClick={() => setPlaying(!playing)}
        >
          {playing ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
        </Button>
        <div className="flex-1 h-1.5 bg-muted rounded-full overflow-hidden">
          <motion.div
            className="h-full gradient-primary rounded-full"
            style={{ width: `${progress}%` }}
          />
        </div>
        <span className="text-xs font-mono text-muted-foreground">{progress}%</span>
      </div>
    </div>
  );
};

const InfluenceRadarPreview = () => {
  const nodes = [
    { x: 50, y: 50, size: 28, label: "CryptoKing", score: 94 },
    { x: 25, y: 30, size: 18, label: "DegenTrader", score: 72 },
    { x: 75, y: 25, size: 22, label: "WhaleAlert", score: 88 },
    { x: 30, y: 75, size: 15, label: "MemeHunter", score: 65 },
    { x: 78, y: 70, size: 20, label: "AlphaLeaks", score: 81 },
    { x: 55, y: 20, size: 12, label: "ShibArmy", score: 45 },
    { x: 20, y: 55, size: 14, label: "NFTGuru", score: 58 },
  ];

  return (
    <div className="glass rounded-2xl p-6 glow-border-secondary relative overflow-hidden">
      <h4 className="text-sm font-semibold text-foreground mb-4">Influence Network</h4>
      <div className="relative h-64">
        {/* Connection lines */}
        <svg className="absolute inset-0 w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="none">
          {nodes.slice(1).map((n, i) => (
            <line
              key={i}
              x1={nodes[0].x} y1={nodes[0].y}
              x2={n.x} y2={n.y}
              stroke="hsl(var(--secondary))"
              strokeWidth="0.3"
              strokeOpacity="0.4"
            />
          ))}
        </svg>
        {/* Nodes */}
        {nodes.map((n, i) => (
          <motion.div
            key={n.label}
            className="absolute group cursor-pointer"
            style={{ left: `${n.x}%`, top: `${n.y}%`, transform: "translate(-50%, -50%)" }}
            initial={{ scale: 0, opacity: 0 }}
            whileInView={{ scale: 1, opacity: 1 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.1, type: "spring" }}
          >
            <div
              className="rounded-full flex items-center justify-center gradient-primary text-[8px] font-bold text-foreground transition-transform duration-300 group-hover:scale-125"
              style={{ width: n.size, height: n.size }}
            >
              {n.score}
            </div>
            <div className="absolute top-full mt-1 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 transition-opacity glass rounded-md px-2 py-1 whitespace-nowrap z-10">
              <div className="text-[10px] font-medium text-foreground">@{n.label}</div>
              <div className="text-[9px] text-muted-foreground">Impact: {n.score}/100</div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

const WowFeatures = () => (
  <section id="wow" className="py-32 relative gradient-bg-subtle">
    <div className="container mx-auto px-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="text-center mb-16"
      >
        <h2 className="text-3xl md:text-4xl font-bold mb-4">
          <span className="gradient-text">Wow</span> Features
        </h2>
        <p className="text-muted-foreground max-w-lg mx-auto">
          Groundbreaking tools that redefine crypto intelligence.
        </p>
      </motion.div>

      <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
        <motion.div
          initial={{ opacity: 0, x: -30 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
        >
          <div className="mb-4">
            <h3 className="text-xl font-bold text-foreground mb-2">⏳ Hype Replay</h3>
            <p className="text-sm text-muted-foreground">Travel back in time and replay how hype evolved around any token.</p>
          </div>
          <HypeReplayPreview />
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 30 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
        >
          <div className="mb-4">
            <h3 className="text-xl font-bold text-foreground mb-2">📡 Influence Radar</h3>
            <p className="text-sm text-muted-foreground">Map the network of influencers driving meme coin hype.</p>
          </div>
          <InfluenceRadarPreview />
        </motion.div>
      </div>
    </div>
  </section>
);

export default WowFeatures;

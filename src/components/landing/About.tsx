import { motion } from "framer-motion";

const About = () => (
  <section id="about" className="py-32">
    <div className="container mx-auto px-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="max-w-2xl mx-auto text-center"
      >
        <h2 className="text-3xl md:text-4xl font-bold mb-6">
          About <span className="gradient-text">TrustScore AI</span>
        </h2>
        <p className="text-lg text-muted-foreground leading-relaxed mb-8">
          We transform social media noise into actionable crypto intelligence. Our AI analyzes millions of posts, tracks influencer networks, and delivers trust scores — so you can invest with clarity, not chaos.
        </p>
        <div className="flex items-center justify-center gap-8 text-sm text-muted-foreground">
          {[
            { val: "50M+", label: "Posts analyzed" },
            { val: "12K+", label: "Tokens tracked" },
            { val: "99.2%", label: "Uptime" },
          ].map((s) => (
            <div key={s.label}>
              <div className="text-2xl font-bold gradient-text font-mono">{s.val}</div>
              <div className="mt-1">{s.label}</div>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  </section>
);

export default About;

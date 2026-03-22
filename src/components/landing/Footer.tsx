import { Zap } from "lucide-react";

const Footer = () => (
  <footer className="border-t border-border py-10">
    <div className="container mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-4">
      <div className="flex items-center gap-2">
        <div className="w-6 h-6 rounded-md gradient-primary flex items-center justify-center">
          <Zap className="w-3 h-3 text-foreground" />
        </div>
        <span className="text-sm font-semibold text-foreground">TrustScore AI</span>
      </div>
      <p className="text-xs text-muted-foreground">© 2026 TrustScore AI. All rights reserved.</p>
    </div>
  </footer>
);

export default Footer;

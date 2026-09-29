import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import { motion, useScroll, useSpring, useTransform } from "framer-motion";
import {
  ArrowDownRight,
  ArrowRight,
  Check,
  ChevronRight,
  CircleAlert,
  Fingerprint,
  LockKeyhole,
  Orbit,
  Play,
  ScanLine,
  ShieldCheck,
  Sparkles,
  Terminal,
  X,
  Zap,
} from "lucide-react";
import "./styles.css";

const demoAuthorized = {
  tool: "customer_api",
  operation: "update",
  resource: "customer:1042",
  parameters: { plan: "pro" },
  context: { environment: "production", purpose: "support" },
  actor: "agent:support",
};

const demoExecuted = {
  ...demoAuthorized,
  resource: "customer:9001",
};

function Pill({ children, accent = false }) {
  return <span className={`pill ${accent ? "pill-accent" : ""}`}>{children}</span>;
}

function ActionVisual({ compact = false }) {
  return (
    <div className={`action-visual ${compact ? "compact" : ""}`}>
      <div className="visual-noise" />
      <motion.div
        className="orb orb-a"
        animate={{ rotate: 360, scale: [1, 1.04, 1] }}
        transition={{ rotate: { duration: 18, repeat: Infinity, ease: "linear" }, scale: { duration: 4, repeat: Infinity } }}
      />
      <motion.div
        className="orb orb-b"
        animate={{ rotate: -360, y: [0, -18, 0] }}
        transition={{ rotate: { duration: 24, repeat: Infinity, ease: "linear" }, y: { duration: 5, repeat: Infinity, ease: "easeInOut" } }}
      />
      <div className="wire wire-1" />
      <div className="wire wire-2" />
      <div className="wire wire-3" />
      <motion.div
        className="core-card"
        animate={{ rotateX: [0, 4, 0], rotateY: [-4, 4, -4] }}
        transition={{ duration: 7, repeat: Infinity, ease: "easeInOut" }}
      >
        <div className="core-top">
          <span>AUTHORIZATION OBJECT</span>
          <span className="live-dot" />
        </div>
        <div className="core-code">
          <span className="code-key">tool</span><span>customer_api</span>
          <span className="code-key">op</span><span>update</span>
          <span className="code-key">resource</span><span>customer:1042</span>
          <span className="code-key">actor</span><span>agent:support</span>
        </div>
        <div className="core-bottom">
          <span>SHA-256</span>
          <span>PROVENANCE LOCKED</span>
        </div>
      </motion.div>
    </div>
  );
}

function Hero() {
  const { scrollYProgress } = useScroll();
  const y = useTransform(scrollYProgress, [0, 0.25], [0, -100]);
  const opacity = useTransform(scrollYProgress, [0, 0.2], [1, 0]);

  return (
    <section className="hero">
      <div className="hero-glow" />
      <nav className="nav">
        <div className="brand">
          <span className="brand-mark"><span /></span>
          <span>A2E</span>
        </div>
        <div className="nav-center">
          <a href="#verify">VERIFY</a>
          <a href="#how">HOW IT WORKS</a>
          <a href="#research">RESEARCH</a>
        </div>
        <a className="nav-cta" href="#verify">OPEN VERIFIER <ArrowDownRight size={15} /></a>
      </nav>

      <motion.div className="hero-content" style={{ y, opacity }}>
        <div className="eyebrow"><span className="eyebrow-line" /> AUTHORIZATION → EXECUTION INTEGRITY</div>
        <h1>
          <span>KEEP THE</span>
          <span className="outline">ACTION</span>
          <span>AUTHORIZED.</span>
        </h1>
        <p className="hero-copy">
          A deterministic verification layer for AI agents.
          Track what was authorized, what changed, and what actually executed.
        </p>
        <div className="hero-actions">
          <a className="button button-solid" href="#verify">TRY A2E <ArrowRight size={16} /></a>
          <a className="button button-ghost" href="#how"><Play size={14} fill="currentColor" /> SEE THE FLOW</a>
        </div>
      </motion.div>

      <motion.div className="hero-object" style={{ y: useTransform(scrollYProgress, [0, 0.25], [0, 90]) }}>
        <ActionVisual />
      </motion.div>

      <div className="hero-bottom">
        <span>OPEN SOURCE SECURITY RESEARCH</span>
        <span>01 / 05</span>
      </div>
    </section>
  );
}

function Flow() {
  const items = [
    { n: "01", title: "AUTHORIZE", desc: "The original action becomes the reference state.", icon: LockKeyhole },
    { n: "02", title: "TRANSFORM", desc: "Track delegation, reconstruction, parameter and context changes.", icon: Orbit },
    { n: "03", title: "VERIFY", desc: "Compare the eventual action against the authorization.", icon: ScanLine },
    { n: "04", title: "EXECUTE", desc: "Only a preserved authorization reaches the effect layer.", icon: ShieldCheck },
  ];

  return (
    <section className="flow-section" id="how">
      <div className="section-intro">
        <Pill>THE PROBLEM</Pill>
        <h2>Authorization can<br /><em>drift.</em></h2>
        <p>
          An agent can start with a valid instruction and still arrive at a different
          tool, resource, parameter set, actor or context.
        </p>
      </div>

      <div className="flow-stack">
        {items.map((item, i) => {
          const Icon = item.icon;
          return (
            <motion.div
              className="flow-row"
              key={item.n}
              initial={{ opacity: 0, x: 60 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true, amount: 0.35 }}
              transition={{ duration: 0.7, delay: i * 0.08 }}
            >
              <span className="flow-number">{item.n}</span>
              <div className="flow-icon"><Icon size={20} /></div>
              <h3>{item.title}</h3>
              <p>{item.desc}</p>
              <ArrowDownRight className="flow-arrow" size={22} />
            </motion.div>
          );
        })}
      </div>
    </section>
  );
}

function Verify() {
  const [authorized, setAuthorized] = useState(demoAuthorized);
  const [executed, setExecuted] = useState(demoExecuted);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const verifyNow = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/verify", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ authorized, executed }),
      });
      if (!res.ok) throw new Error("API unavailable");
      setResult(await res.json());
    } catch {
      const mismatch =
        authorized.tool !== executed.tool ? "TOOL_MISMATCH" :
        authorized.operation !== executed.operation ? "OPERATION_MISMATCH" :
        authorized.resource !== executed.resource ? "RESOURCE_MISMATCH" :
        JSON.stringify(authorized.parameters) !== JSON.stringify(executed.parameters) ? "PARAMETER_MISMATCH" :
        JSON.stringify(authorized.context) !== JSON.stringify(executed.context) ? "CONTEXT_MISMATCH" :
        authorized.actor !== executed.actor ? "ACTOR_MISMATCH" : "MATCH";
      setResult({
        allowed: mismatch === "MATCH",
        verdict: mismatch,
        investigation: {
          summary: mismatch === "MATCH"
            ? "The executed action matches the authorization."
            : "The executed action does not preserve the original authorization.",
          category: mismatch === "MATCH" ? "NO_DRIFT" : mismatch.replace("_MISMATCH", "_DRIFT"),
          evidence: [`Deterministic comparison returned ${mismatch}.`],
          remediation: ["Re-validate the action immediately before execution.", "Preserve provenance across transformations."],
        },
      });
    } finally {
      setLoading(false);
    }
  };

  const loadAttack = () => setExecuted(demoExecuted);
  const loadSafe = () => setExecuted(demoAuthorized);

  return (
    <section className="verify-section" id="verify">
      <div className="verify-heading">
        <div>
          <Pill accent>LIVE VERIFIER</Pill>
          <h2>SHOW ME<br /><span>THE DRIFT.</span></h2>
        </div>
        <p>Real deterministic verification. No AI decision-maker.</p>
      </div>

      <div className="verify-stage">
        <div className="stage-topline">
          <span>AUTHORIZATION INPUT</span>
          <span>EXECUTION INPUT</span>
          <span>VERDICT</span>
        </div>

        <div className="compare-grid">
          <ActionEditor label="AUTHORIZED" value={authorized} onChange={setAuthorized} />
          <div className="compare-arrow">
            <motion.div
              animate={{ x: [0, 8, 0] }}
              transition={{ duration: 1.6, repeat: Infinity }}
            >
              <ArrowRight size={28} />
            </motion.div>
            <span>VERIFY</span>
          </div>
          <ActionEditor label="EXECUTED" value={executed} onChange={setExecuted} />
        </div>

        <div className="preset-row">
          <button onClick={loadAttack}>LOAD DRIFT CASE</button>
          <button onClick={loadSafe}>LOAD MATCH CASE</button>
          <button className="run-button" onClick={verifyNow}>
            {loading ? "CHECKING…" : "RUN VERIFICATION"} <Zap size={15} fill="currentColor" />
          </button>
        </div>

        {result && (
          <motion.div
            className={`verdict ${result.allowed ? "verdict-safe" : "verdict-danger"}`}
            initial={{ opacity: 0, y: 25, scale: 0.98 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
          >
            <div className="verdict-symbol">
              {result.allowed ? <Check size={28} /> : <CircleAlert size={28} />}
            </div>
            <div>
              <span className="verdict-label">{result.allowed ? "AUTHORIZATION PRESERVED" : "AUTHORIZATION DRIFT DETECTED"}</span>
              <strong>{result.verdict}</strong>
              <p>{result.investigation?.summary}</p>
            </div>
            <div className="verdict-meta">
              <span>{result.investigation?.category}</span>
              <span>{result.allowed ? "EXECUTION ELIGIBLE" : "EXECUTION BLOCKED"}</span>
            </div>
          </motion.div>
        )}
      </div>
    </section>
  );
}

function ActionEditor({ label, value, onChange }) {
  const set = (key, val) => onChange({ ...value, [key]: val });
  return (
    <div className="editor">
      <div className="editor-header"><span>{label}</span><Fingerprint size={16} /></div>
      <div className="editor-body">
        <label>TOOL<input value={value.tool} onChange={e => set("tool", e.target.value)} /></label>
        <label>OPERATION<input value={value.operation} onChange={e => set("operation", e.target.value)} /></label>
        <label>RESOURCE<input value={value.resource || ""} onChange={e => set("resource", e.target.value)} /></label>
        <label>ACTOR<input value={value.actor || ""} onChange={e => set("actor", e.target.value)} /></label>
        <label>PARAMETERS<textarea value={JSON.stringify(value.parameters, null, 2)} onChange={e => {
          try { set("parameters", JSON.parse(e.target.value)); } catch {}
        }} /></label>
      </div>
    </div>
  );
}

function Research() {
  return (
    <section className="research-section" id="research">
      <div className="research-number">A2E<span>/</span>01</div>
      <div className="research-copy">
        <Pill>SECURITY MODEL</Pill>
        <h2>FROM INTENT<br />TO <em>EFFECT.</em></h2>
        <p>
          A2E treats the original authorization as a security boundary and checks
          whether transformations preserve it all the way to execution.
        </p>
        <div className="model-line">
          <span>AUTHORIZED ACTION</span><ChevronRight />
          <span>TRANSFORMED ACTION</span><ChevronRight />
          <span>ACTUAL EFFECT</span>
        </div>
      </div>
      <ActionVisual compact />
    </section>
  );
}

function Footer() {
  return (
    <footer>
      <div className="footer-top">
        <div className="footer-brand">A2E<span>.</span></div>
        <div className="footer-tag">AUTHORIZATION<br />TO EXECUTION<br />INTEGRITY</div>
        <a href="#verify" className="footer-link">OPEN VERIFIER <ArrowUpRightIcon /></a>
      </div>
      <div className="footer-bottom">
        <span>OPEN-SOURCE SECURITY TOOLING</span>
        <span>AGENTLOCK FOUNDATION + A2E VERIFICATION LAYER</span>
        <span>2026</span>
      </div>
    </footer>
  );
}

function ArrowUpRightIcon() {
  return <ArrowDownRight size={17} style={{ transform: "rotate(-90deg)" }} />;
}

function App() {
  return (
    <main>
      <Hero />
      <div className="marquee">
        <div className="marquee-track">
          <span>AUTHORIZATION</span><b>✳</b><span>TRANSFORMATION</span><b>✳</b><span>PROVENANCE</span><b>✳</b><span>EXECUTION</span><b>✳</b>
          <span>AUTHORIZATION</span><b>✳</b><span>TRANSFORMATION</span><b>✳</b><span>PROVENANCE</span><b>✳</b><span>EXECUTION</span>
        </div>
      </div>
      <Flow />
      <Verify />
      <Research />
      <Footer />
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);

import { ArrowDown, Cloud, Database, FileKey2, GitBranch, Layers3, LockKeyhole, ShieldCheck } from "lucide-react";

const stages = [
  { label: "Consola de operaciones React", icon: <Layers3 size={17} /> },
  { label: "API Gateway · HTTPS", icon: <Cloud size={17} /> },
  { label: "Lambda API · autorización prefirmada", icon: <LockKeyhole size={17} /> },
  { label: "Amazon S3 · input/", icon: <Database size={17} /> },
  { label: "Lambda ETL existente", icon: <GitBranch size={17} /> },
  { label: "Bronze · Calidad · Silver", icon: <ShieldCheck size={17} /> },
  { label: "Gold · Cuarentena · Metadatos", icon: <FileKey2 size={17} /> },
];

export function AboutPage() {
  return <section className="page-section about-page"><div className="section-heading"><div><span className="eyebrow">DISEÑO DEL SISTEMA</span><h1>Arquitectura</h1><p>La consola expone el pipeline de ingeniería de datos existente sin mover archivos a través del API.</p></div></div><div className="architecture-layout"><div className="architecture-flow">{stages.map((stage, index) => <div className="architecture-node-wrap" key={stage.label}><div className="architecture-node"><span>{stage.icon}</span><strong>{stage.label}</strong></div>{index < stages.length - 1 && <ArrowDown className="flow-arrow" size={16} />}</div>)}</div><div className="principles"><div><span>Frontera</span><strong>Subida directa a S3</strong><p>El backend firma un POST de corta duración. El navegador nunca recibe credenciales de AWS.</p></div><div><span>Cómputo</span><strong>Una Lambda API + Lambda ETL existente</strong><p>Las ejecuciones siguen siendo asíncronas. El API lee metadatos de S3 y Parquet solo después del procesamiento.</p></div><div><span>Controles</span><strong>10 MB · URLs de 5 minutos · logs de 14 días</strong><p>Las operaciones prefirmadas están acotadas y el stack no usa concurrencia aprovisionada.</p></div></div></div><div className="stack-band"><span className="eyebrow">TECNOLOGÍAS</span><div className="stack-list"><span>React</span><span>TypeScript</span><span>Python 3.12</span><span>Lambda</span><span>HTTP API</span><span>S3</span><span>CloudWatch</span><span>Parquet</span><span>SAM</span></div></div></section>;
}

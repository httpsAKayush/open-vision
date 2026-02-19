const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? 'http://localhost:8000/api';

export async function getHealth() {
  const res = await fetch(`${API_BASE}/matching/health/`);
  return res.json();
}

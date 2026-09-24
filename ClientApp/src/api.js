const API_BASE = import.meta.env.VITE_API_BASE || "/api/records";

export async function listRecords() {
  const res = await fetch(API_BASE);
  if (!res.ok) throw new Error(`Failed to load records: ${res.status}`);
  return res.json();
}

export async function createRecord(record) {
  const res = await fetch(API_BASE, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(record),
  });
  if (!res.ok) throw new Error(`Failed to create record: ${res.status}`);
  return res.json();
}

export async function deleteRecord(id) {
  const res = await fetch(`${API_BASE}/${id}`, { method: "DELETE" });
  if (!res.ok && res.status !== 204) throw new Error(`Failed to delete record: ${res.status}`);
}

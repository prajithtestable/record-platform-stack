// In-memory "records" store. This is a full-stack reference app (no external
// database is part of this stack), so state lives in module scope for the
// lifetime of the Node process — real reads/writes/CRUD, just not persisted
// across restarts. Kept in a Node global so it survives Next.js dev-server
// hot-reload / route-module re-evaluation.

export interface RecordDto {
  id: string;
  title: string;
  description: string;
  createdAt: string;
}

type Store = Map<string, RecordDto>;

const globalForStore = globalThis as unknown as { __recordsStore?: Store };

function getStore(): Store {
  if (!globalForStore.__recordsStore) {
    globalForStore.__recordsStore = new Map();
  }
  return globalForStore.__recordsStore;
}

export function listRecords(): RecordDto[] {
  return Array.from(getStore().values()).sort((a, b) =>
    b.createdAt.localeCompare(a.createdAt),
  );
}

export function getRecord(id: string): RecordDto | undefined {
  return getStore().get(id);
}

export function createRecord(title: string, description: string): RecordDto {
  const record: RecordDto = {
    id: crypto.randomUUID(),
    title,
    description,
    createdAt: new Date().toISOString(),
  };
  getStore().set(record.id, record);
  return record;
}

export function deleteRecord(id: string): boolean {
  return getStore().delete(id);
}

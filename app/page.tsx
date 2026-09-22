import { listRecords } from "@/lib/records-store";
import { deleteRecordAction } from "./actions";
import { RecordsForm } from "./records-form";

// The records list changes on every create/delete, so always render fresh
// rather than serving a build-time static snapshot.
export const dynamic = "force-dynamic";

export default function Home() {
  const records = listRecords();

  return (
    <main className="records-page">
      <h1>Digital Sippoy — Records</h1>
      <RecordsForm />

      {records.length === 0 ? (
        <p>No records yet.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Title</th>
              <th>Description</th>
              <th>Created</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {records.map((record) => (
              <tr key={record.id}>
                <td>{record.title}</td>
                <td>{record.description}</td>
                <td>{record.createdAt}</td>
                <td>
                  <form action={deleteRecordAction.bind(null, record.id)}>
                    <button type="submit">Delete</button>
                  </form>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </main>
  );
}

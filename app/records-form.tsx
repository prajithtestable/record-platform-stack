"use client";

import { useActionState } from "react";
import { createRecordAction, type FormState } from "./actions";

const initialState: FormState = { error: null };

export function RecordsForm() {
  const [state, formAction, isPending] = useActionState(
    createRecordAction,
    initialState,
  );

  return (
    <form action={formAction} className="record-form">
      <input name="title" placeholder="Title" required disabled={isPending} />
      <input name="description" placeholder="Description" disabled={isPending} />
      <button type="submit" disabled={isPending}>
        {isPending ? "Creating..." : "Create record"}
      </button>
      {state.error && <p className="error">{state.error}</p>}
    </form>
  );
}

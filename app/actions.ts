"use server";

import { revalidatePath } from "next/cache";
import { createRecord, deleteRecord } from "@/lib/records-store";

export interface FormState {
  error: string | null;
}

export async function createRecordAction(
  _prevState: FormState,
  formData: FormData,
): Promise<FormState> {
  const title = String(formData.get("title") ?? "").trim();
  const description = String(formData.get("description") ?? "").trim();

  if (!title) {
    return { error: "Title is required" };
  }

  createRecord(title, description);
  revalidatePath("/");
  return { error: null };
}

export async function deleteRecordAction(id: string): Promise<void> {
  deleteRecord(id);
  revalidatePath("/");
}

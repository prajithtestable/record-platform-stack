import { NextRequest, NextResponse } from "next/server";
import { createRecord, listRecords } from "@/lib/records-store";

export async function GET() {
  return NextResponse.json(listRecords());
}

export async function POST(request: NextRequest) {
  const body = await request.json().catch(() => null);
  const title = typeof body?.title === "string" ? body.title.trim() : "";
  const description =
    typeof body?.description === "string" ? body.description.trim() : "";

  if (!title) {
    return NextResponse.json({ error: "title is required" }, { status: 400 });
  }

  const record = createRecord(title, description);
  return NextResponse.json(record, { status: 201 });
}

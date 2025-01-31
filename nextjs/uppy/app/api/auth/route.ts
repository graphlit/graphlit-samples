import { NextResponse } from "next/server";
import { Graphlit } from "graphlit-client";

export async function GET() {
  try {
    const client = new Graphlit();
    const jwt = client.token;
    return NextResponse.json({ token: jwt });
  } catch (error) {
    return NextResponse.json({ error: "Failed to generate JWT" }, { status: 500 });
  }
}
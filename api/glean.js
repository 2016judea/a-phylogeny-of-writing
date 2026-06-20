// GLEAN landing-page form handler.
// One endpoint, two jobs: save a contributed piece, or save a free-by-mail subscriber.
// Writes straight to Notion. No deps — Node 18+ has global fetch on Vercel.

const NOTION_TOKEN = process.env.NOTION_TOKEN;
const DB_CONTRIBUTIONS = "6718839c-6bb3-4173-870c-9ae3fde1a5a0";
const DB_SUBSCRIBERS = "3a33565a-4853-47c8-adb1-c9e0e3a1615b";

// Notion caps a single rich_text item at 2000 chars; split long pieces.
function richText(str) {
  const s = String(str || "");
  const chunks = [];
  for (let i = 0; i < s.length; i += 1900) {
    chunks.push({ text: { content: s.slice(i, i + 1900) } });
  }
  return chunks.length ? chunks : [{ text: { content: "" } }];
}

async function createPage(databaseId, properties) {
  const res = await fetch("https://api.notion.com/v1/pages", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${NOTION_TOKEN}`,
      "Notion-Version": "2022-06-28",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ parent: { database_id: databaseId }, properties }),
  });
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(`Notion ${res.status}: ${detail}`);
  }
}

export default async function handler(req, res) {
  // Safe diagnostic: never returns the secret, only whether it's present.
  if (req.method === "GET") {
    return res.status(200).json({
      hasToken: !!NOTION_TOKEN,
      tokenLen: NOTION_TOKEN ? NOTION_TOKEN.length : 0,
      notionKeys: Object.keys(process.env).filter((k) => /notion/i.test(k)),
      vercelEnv: process.env.VERCEL_ENV || null,
    });
  }
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }
  if (!NOTION_TOKEN) {
    return res.status(500).json({ error: "Server not configured (missing NOTION_TOKEN)" });
  }

  // Vercel parses JSON bodies automatically; fall back for safety.
  let body = req.body;
  if (typeof body === "string") {
    try { body = JSON.parse(body); } catch { body = {}; }
  }
  body = body || {};

  try {
    if (body.type === "contribute") {
      const piece = (body.piece || "").trim();
      if (!piece) return res.status(400).json({ error: "Nothing to submit." });
      await createPage(DB_CONTRIBUTIONS, {
        Name: { title: [{ text: { content: (body.name || "Anonymous").slice(0, 200) } }] },
        Email: { email: (body.email || "").slice(0, 200) || null },
        Piece: { rich_text: richText(piece) },
        Status: { select: { name: "New" } },
      });
      return res.status(200).json({ ok: true });
    }

    if (body.type === "subscribe") {
      const name = (body.name || "").trim();
      const address = (body.address || "").trim();
      if (!name || !address) {
        return res.status(400).json({ error: "Name and mailing address are required." });
      }
      await createPage(DB_SUBSCRIBERS, {
        Name: { title: [{ text: { content: name.slice(0, 200) } }] },
        Email: { email: (body.email || "").slice(0, 200) || null },
        Address: { rich_text: richText(address) },
        Status: { select: { name: "New" } },
      });
      return res.status(200).json({ ok: true });
    }

    return res.status(400).json({ error: "Unknown form type." });
  } catch (err) {
    console.error(err);
    return res.status(502).json({ error: "Could not save right now. Try again in a moment." });
  }
}

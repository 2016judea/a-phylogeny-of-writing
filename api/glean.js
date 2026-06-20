// GLEAN landing-page form handler.
// Jobs: save a contributed piece (+ optional photos), save a free-by-mail subscriber,
// and broker Dropbox temporary-upload links so the browser uploads photos directly to
// Dropbox (bypassing Vercel's ~4.5MB request-body cap).
// No deps — Node 18+ has global fetch on Vercel.

const NOTION_TOKEN = process.env.NOTION_TOKEN;
const DB_CONTRIBUTIONS = "6718839c-6bb3-4173-870c-9ae3fde1a5a0";
const DB_SUBSCRIBERS = "3a33565a-4853-47c8-adb1-c9e0e3a1615b";

const DBX_KEY = process.env.DROPBOX_APP_KEY;
const DBX_SECRET = process.env.DROPBOX_APP_SECRET;
const DBX_REFRESH = process.env.DROPBOX_REFRESH_TOKEN;
const DBX_ROOT = "/Glean/contributions";

// ---- Notion -----------------------------------------------------------------

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
  if (!res.ok) throw new Error(`Notion ${res.status}: ${await res.text()}`);
}

// ---- Dropbox ----------------------------------------------------------------

let dbxToken = null;
let dbxTokenExp = 0;

async function dropboxToken() {
  if (dbxToken && Date.now() < dbxTokenExp) return dbxToken;
  const res = await fetch("https://api.dropbox.com/oauth2/token", {
    method: "POST",
    headers: {
      Authorization: `Basic ${Buffer.from(`${DBX_KEY}:${DBX_SECRET}`).toString("base64")}`,
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `grant_type=refresh_token&refresh_token=${encodeURIComponent(DBX_REFRESH)}`,
  });
  if (!res.ok) throw new Error(`Dropbox token ${res.status}: ${await res.text()}`);
  const json = await res.json();
  dbxToken = json.access_token;
  dbxTokenExp = Date.now() + (json.expires_in - 120) * 1000; // refresh a little early
  return dbxToken;
}

// Keep path components filesystem-safe.
function safe(part) {
  return String(part || "").replace(/[^\w.\- ]+/g, "_").replace(/\s+/g, " ").trim().slice(0, 120);
}

async function tempUploadLink(folder, filename) {
  const token = await dropboxToken();
  const path = `${DBX_ROOT}/${safe(folder)}/${safe(filename) || "file"}`;
  const res = await fetch("https://api.dropboxapi.com/2/files/get_temporary_upload_link", {
    method: "POST",
    headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
    body: JSON.stringify({ commit_info: { path, mode: "add", autorename: true }, duration: 3600 }),
  });
  if (!res.ok) throw new Error(`Dropbox upload-link ${res.status}: ${await res.text()}`);
  return (await res.json()).link;
}

async function folderShareUrl(folder) {
  const token = await dropboxToken();
  const path = `${DBX_ROOT}/${safe(folder)}`;
  const mk = await fetch("https://api.dropboxapi.com/2/sharing/create_shared_link_with_settings", {
    method: "POST",
    headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
    body: JSON.stringify({ path }),
  });
  if (mk.ok) return (await mk.json()).url;
  // 409 = a shared link already exists for this folder; fetch it.
  if (mk.status === 409) {
    const list = await fetch("https://api.dropboxapi.com/2/sharing/list_shared_links", {
      method: "POST",
      headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
      body: JSON.stringify({ path, direct_only: true }),
    });
    if (list.ok) {
      const links = (await list.json()).links || [];
      if (links[0]) return links[0].url;
    }
  }
  throw new Error(`Dropbox share ${mk.status}: ${await mk.text()}`);
}

// ---- Handler ----------------------------------------------------------------

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }
  if (!NOTION_TOKEN) {
    return res.status(500).json({ error: "Server not configured (missing NOTION_TOKEN)" });
  }

  let body = req.body;
  if (typeof body === "string") {
    try { body = JSON.parse(body); } catch { body = {}; }
  }
  body = body || {};

  try {
    // Step 1 (photos): hand the browser a direct-to-Dropbox upload link.
    if (body.type === "upload-link") {
      if (!DBX_REFRESH) return res.status(500).json({ error: "Uploads not configured." });
      if (!body.folder || !body.filename) {
        return res.status(400).json({ error: "Missing folder or filename." });
      }
      const link = await tempUploadLink(body.folder, body.filename);
      return res.status(200).json({ link });
    }

    if (body.type === "contribute") {
      const piece = (body.piece || "").trim();
      const photoCount = Math.max(0, parseInt(body.photoCount, 10) || 0);
      if (!piece && !photoCount) {
        return res.status(400).json({ error: "Add a piece or some photos." });
      }

      let photosUrl = null;
      if (photoCount > 0 && body.folder) {
        try { photosUrl = await folderShareUrl(body.folder); } catch (e) { console.error(e); }
      }

      const properties = {
        Name: { title: [{ text: { content: (body.name || "Anonymous").slice(0, 200) } }] },
        Email: { email: (body.email || "").slice(0, 200) || null },
        Piece: { rich_text: richText(piece) },
        Status: { select: { name: "New" } },
      };
      if (photoCount > 0) properties["Photo count"] = { number: photoCount };
      if (photosUrl) properties.Photos = { url: photosUrl };

      await createPage(DB_CONTRIBUTIONS, properties);
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

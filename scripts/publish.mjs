// Publishes due posts: Telegram directly (Bot API), Instagram/X via Buffer API.
// Env: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, BUFFER_API_KEY, IMAGE_BASE_URL (public raw URL base; needed for ig/x)
import { readFile, writeFile } from "node:fs/promises";

const {
  TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, BUFFER_API_KEY, IMAGE_BASE_URL,
  BUFFER_API_URL = "https://api.buffer.com",
  DRY_RUN,
} = process.env;

const BUFFER_LEAD_MS = 36 * 3600e3;   // hand posts to Buffer up to 36h ahead
const BUFFER_MIN_MS = 5 * 60e3;       // Buffer needs a future dueAt
const TG_WAIT_MAX_MS = 5.5 * 3600e3;  // a run may sleep up to 5.5h to send Telegram exactly on time
const TG_MAX_LATE_MS = 24 * 3600e3;   // don't send Telegram posts later than 24h after schedule

const schedule = JSON.parse(await readFile("schedule.json", "utf8"));
const state = JSON.parse(await readFile("state.json", "utf8"));
const now = Date.now();
let failed = false, changed = false;

const log = (...a) => console.log(...a);
const fail = (id, p, e) => { failed = true; console.error(`✗ ${id}/${p}: ${e}`); };

const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const tgHtml = (s) => esc(s).replace(/\*\*(.+?)\*\*/gs, "<b>$1</b>");

async function sendTelegram(p) {
  const fd = new FormData();
  fd.set("chat_id", TELEGRAM_CHAT_ID);
  fd.set("caption", tgHtml(p.tg.caption));
  fd.set("parse_mode", "HTML");
  let method = "sendPhoto";
  if (p.tg.video) {
    method = "sendVideo";
    fd.set("video", new Blob([await readFile(p.tg.video)], { type: "video/mp4" }), "post.mp4");
    fd.set("supports_streaming", "true");
    if (p.tg.width) fd.set("width", String(p.tg.width));
    if (p.tg.height) fd.set("height", String(p.tg.height));
    if (p.tg.image) fd.set("thumbnail", new Blob([await readFile(p.tg.image)], { type: "image/jpeg" }), "thumb.jpg");
  } else {
    fd.set("photo", new Blob([await readFile(p.tg.image)], { type: "image/png" }), "post.png");
  }
  const r = await fetch(`https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/${method}`, { method: "POST", body: fd });
  const j = await r.json();
  if (!j.ok) throw new Error(j.description || r.status);
  return { messageId: j.result.message_id, at: new Date().toISOString() };
}

const MUTATION = `mutation($input: CreatePostInput!){
  createPost(input:$input){
    __typename
    ... on PostActionSuccess { post { id dueAt status } }
    ... on MutationError { message }
  }
}`;

async function scheduleBuffer(p, key) {
  const v = p[key];
  const input = {
    channelId: schedule.channels[key],
    text: v.caption,
    assets: [v.video
      ? { video: { url: `${IMAGE_BASE_URL.replace(/\/$/, "")}/${v.video}`, ...(v.image ? { thumbnailUrl: `${IMAGE_BASE_URL.replace(/\/$/, "")}/${v.image}` } : {}) } }
      : { image: { url: `${IMAGE_BASE_URL.replace(/\/$/, "")}/${v.image}` } }],
    mode: "customScheduled",
    schedulingType: "automatic",
    dueAt: new Date(p.when).toISOString(),
    saveToDraft: false,
  };
  if (key === "ig") input.metadata = { instagram: { type: v.video ? "reel" : "post", shouldShareToFeed: true } };
  const r = await fetch(BUFFER_API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${BUFFER_API_KEY}` },
    body: JSON.stringify({ query: MUTATION, variables: { input } }),
  });
  const j = await r.json();
  if (j.errors) throw new Error(JSON.stringify(j.errors));
  const res = j.data.createPost;
  if (res.__typename !== "PostActionSuccess") throw new Error(`${res.__typename}: ${res.message}`);
  return { bufferId: res.post.id, dueAt: res.post.dueAt, status: res.post.status };
}

// Pass 1: hand Instagram/X posts to Buffer (it publishes them itself at dueAt).
for (const p of schedule.posts) {
  const when = Date.parse(p.when);
  state[p.id] ??= {};
  const s = state[p.id];
  for (const key of ["ig", "x"]) {
    if (!p[key] || s[key]) continue;
    if (when - now > BUFFER_LEAD_MS) continue;
    if (when - now < BUFFER_MIN_MS) { s[key] = { skipped: "missed window" }; changed = true; log(`- ${p.id}/${key} skipped (missed window)`); continue; }
    if (!IMAGE_BASE_URL || !BUFFER_API_KEY) { log(`- ${p.id}/${key} waiting: IMAGE_BASE_URL / BUFFER_API_KEY not set`); continue; }
    try {
      if (DRY_RUN) log(`[dry] ${key} ${p.id}`);
      else { s[key] = await scheduleBuffer(p, key); changed = true; log(`✓ ${p.id}/${key} scheduled in Buffer`); }
    } catch (e) { fail(p.id, key, e.message); }
  }
}

// Pass 2: Telegram. GitHub cron runs are often hours late, so if a post is due soon,
// this run waits until its exact time instead of leaving it for the next (late) run.
for (const p of schedule.posts) {
  const when = Date.parse(p.when);
  const s = state[p.id];
  if (!p.tg || s.tg) continue;
  if (when > Date.now()) {
    if (DRY_RUN || when - Date.now() > TG_WAIT_MAX_MS) continue;
    log(`… waiting until ${p.when} to send ${p.id}/tg`);
    await new Promise((r) => setTimeout(r, when - Date.now()));
  }
  if (Date.now() - when > TG_MAX_LATE_MS) { s.tg = { skipped: "too late" }; changed = true; log(`- ${p.id}/tg skipped (too late)`); continue; }
  try {
    if (DRY_RUN) log(`[dry] tg ${p.id}`);
    else { s.tg = await sendTelegram(p); changed = true; log(`✓ ${p.id}/tg sent`); }
  } catch (e) { fail(p.id, "tg", e.message); }
}

if (changed) await writeFile("state.json", JSON.stringify(state, null, 2) + "\n");
process.exit(failed ? 1 : 0);

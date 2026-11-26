/* script.js - all page interactions. Data always comes from the Flask backend. */

const $ = (id) => document.getElementById(id);
const history = [];                       // classification history (this visit)

/* Build one species card (used in Explore and in results) */
function card(s, extra = "") {
  const photo = `<img src="${s.image}" alt="${s.name}" onerror="this.replaceWith(document.createTextNode('${s.emoji}'))">`;
  return `<article class="card">
    <div class="pic">${photo}</div>
    <div class="body">
      <h4>${s.name}</h4><div class="sci">${s.scientific_name}</div>
      <div class="tags"><span class="tag type">${s.type}</span><span class="tag">${s.habitat}</span></div>
      <p>${s.description}</p>${extra}
    </div></article>`;
}

/* Extra block on result cards: compatibility + matched features */
function matchInfo(s) {
  const tags = s.matched_features.map((f) => `<span class="tag match">✓ ${f}</span>`).join("");
  return `<div class="tags">${tags}</div>
    <b>${s.compatibility}% compatible</b><div class="bar"><i style="width:${s.compatibility}%"></i></div>
    <div class="sci">Temp: ${s.temperature} · Pollution: ${s.pollution} · Water: ${s.water} · Climate: ${s.climate}</div>`;
}

function showMsg(text, kind) {
  const m = $("formMsg");
  m.textContent = text; m.className = "msg " + kind; m.hidden = false;
}

/* ---------- stats, counters and linked list drawing ---------- */
async function loadStats() {
  const st = await (await fetch("/stats")).json();
  $("cTotal").textContent = st.total;
  $("cPlants").textContent = st.plants;
  $("cAnimals").textContent = st.animals;
  // Draw the first 6 nodes: HEAD -> [name|next] -> ... -> None
  const nodes = st.names.slice(0, 6).map((n) => `<div class="node"><span>${n}</span><em>next</em></div><span class="arrow">→</span>`).join("");
  $("chain").innerHTML = `<span class="head">HEAD&nbsp;→&nbsp;</span>${nodes}<span class="none">… ${st.total - 6} more nodes → None</span>`;
}

/* ---------- classification ---------- */
$("classifyForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const env = Object.fromEntries(new FormData(e.target).entries());
  $("formMsg").hidden = true; $("results").hidden = true;

  const missing = ["type", "habitat", "temperature", "pollution", "water", "climate"].filter((k) => !env[k]);
  if (missing.length) { showMsg("Please choose: " + missing.join(", ") + ".", "error"); return; }

  $("loader").hidden = false;
  try {
    await new Promise((r) => setTimeout(r, 600));            // short pause so the loader is visible
    const res = await fetch("/classify", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(env) });
    const data = await res.json();
    if (!res.ok) { showMsg(data.error, "error"); return; }
    showResults(env, data);
  } catch (err) {
    showMsg("Could not reach the server. Is Flask running?", "error");
  } finally {
    $("loader").hidden = true;
  }
});

function showResults(env, d) {
  $("results").hidden = false;
  const headings = document.querySelectorAll("#results h3");
  if (!d.best) {
    $("summary").className = "summary msg error";
    $("summary").textContent = `No suitable species found after visiting ${d.nodes_traversed} nodes. Try changing one or two conditions.`;
    $("bestCard").innerHTML = ""; $("otherCards").innerHTML = "";
    headings.forEach((h) => (h.hidden = true));
    addHistory(env, "No match", d.nodes_traversed);
  } else {
    headings.forEach((h) => (h.hidden = false));
    $("summary").className = "summary msg ok";
    $("summary").textContent = `Found ${d.total_matches} matching species. Linked list nodes traversed: ${d.nodes_traversed}.`;
    $("bestCard").innerHTML = card(d.best, matchInfo(d.best)).replace('class="card"', 'class="card best"');
    $("otherCards").innerHTML = d.others.map((s) => card(s, matchInfo(s))).join("");
    $("othersTitle").hidden = d.others.length === 0;
    addHistory(env, `${d.best.name} (${d.best.compatibility}%)`, d.nodes_traversed);
  }
  $("results").scrollIntoView({ behavior: "smooth" });
}

function addHistory(env, outcome, nodes) {
  history.unshift(`<li><b>${outcome}</b> — ${env.type}, ${env.habitat}, ${env.temperature}, pollution ${env.pollution}, water ${env.water}, ${env.climate} <span class="muted">(${nodes} nodes)</span></li>`);
  $("historyList").innerHTML = history.join("");
}

$("resetForm").addEventListener("click", () => {
  $("classifyForm").reset(); $("results").hidden = true; $("formMsg").hidden = true;
});

/* ---------- explore: search + filters (via backend) ---------- */
async function loadSpecies() {
  const res = await fetch("/filter", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query: $("searchBox").value, type: $("fType").value, habitat: $("fHabitat").value }),
  });
  const list = await res.json();
  $("exploreCount").textContent = `${list.length} species found`;
  $("speciesGrid").innerHTML = list.length ? list.map((s) => card(s)).join("")
    : `<p class="muted">No species match these filters. Press “Reset filters” to see everything.</p>`;
}
["searchBox", "fType", "fHabitat"].forEach((id) => $(id).addEventListener("input", loadSpecies));
$("resetFilters").addEventListener("click", () => { $("searchBox").value = ""; $("fType").value = ""; $("fHabitat").value = ""; loadSpecies(); });

/* ---------- mobile menu ---------- */
$("menuBtn").addEventListener("click", () => $("navLinks").classList.toggle("open"));
$("navLinks").addEventListener("click", () => $("navLinks").classList.remove("open"));

loadStats(); loadSpecies();

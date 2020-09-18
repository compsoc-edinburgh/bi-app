import YAML from "yaml";
const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, HEAD, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization"
};
addEventListener("fetch", (event) => {
  event.respondWith(handleRequest(event.request));
});
/**
 * Respond with hello worker text
 * @param {Request} request
 */
async function handleRequest(request) {
  if (request.method == "OPTIONS") {
    return new Response(JSON.stringify({}), {
      status: 200,
      headers: corsHeaders
    });
  }
  try {
    const json = await request.json();
    const blob = await fetch(
      "https://git-gateway.api-server.comp-soc.com/github/git/blobs",
      {
        headers: {
          Authorization: `Bearer ${JWT_TOKEN}`,
          "Content-Type": "application/json; charset=utf-8",
          "User-Agent": "Cloudflare Worker"
        },
        body: JSON.stringify({
          content: btoa(
            `
---
${YAML.stringify(json.data)}
---
${json.content}`
          ),
          encoding: "base64"
        }),
        method: "POST"
      }
    ).then((r) => r.json());

    const master = await fetch(
      "https://git-gateway.api-server.comp-soc.com/github/branches/master",
      {
        headers: {
          Authorization: `Bearer ${JWT_TOKEN}`,
          "Content-Type": "application/json; charset=utf-8",
          "User-Agent": "Cloudflare Worker"
        }
      }
    ).then((r) => r.json());

    const tree = await fetch(
      "https://git-gateway.api-server.comp-soc.com/github/git/trees",
      {
        headers: {
          Authorization: `Bearer ${JWT_TOKEN}`,
          "Content-Type": "application/json; charset=utf-8",
          "User-Agent": "Cloudflare Worker"
        },
        body: JSON.stringify({
          base_tree: master.commit.sha,
          tree: [
            {
              path: `_sections/${json.page}/${json.section}.md`,
              mode: "100644",
              type: "blob",
              sha: blob.sha
            }
          ]
        }),
        method: "POST"
      }
    ).then((r) => r.json());
    const commit = await fetch(
      "https://git-gateway.api-server.comp-soc.com/github/git/commits",
      {
        headers: {
          Authorization: `Bearer ${JWT_TOKEN}`,
          "Content-Type": "application/json; charset=utf-8",
          "User-Agent": "Cloudflare Worker"
        },
        body: JSON.stringify({
          message: `Modify ${json.page}/${json.section}`,
          tree: tree.sha,
          parents: [master.commit.sha],
          author: {
            name: "Website User",
            email: "user@betterinformatics.com",
            date: new Date().toISOString()
          }
        }),
        method: "POST"
      }
    ).then((r) => r.json());
    const toMaster = await fetch(
      "https://git-gateway.api-server.comp-soc.com/github/git/refs/heads/master",
      {
        headers: {
          Authorization: `Bearer ${JWT_TOKEN}`,
          "Content-Type": "application/json; charset=utf-8",
          "User-Agent": "Cloudflare Worker"
        },
        body: JSON.stringify({ sha: commit.sha, force: false }),
        method: "PATCH"
      }
    );
    return new Response("OK", {
      status: 200,
      headers: corsHeaders
    });
  } catch (e) {
    return new Response(e.stack, {
      status: 500,
      headers: corsHeaders
    });
  }
}

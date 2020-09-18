import { promises } from "fs";
import md from "markdown-it";
import matter from "gray-matter";
import anchor from "markdown-it-anchor";
import mk from "@neilsustc/markdown-it-katex";
let mark = md({ typographer: true, html: true });
mark.use(mk).use(anchor);
const getSections = async (slug) => {
  try {
    await promises.access(
      `./src/sections/${slug == "inf5" ? "masters" : slug}`
    );
    const sections = await promises.readdir(
      `./src/sections/${slug == "inf5" ? "masters" : slug}`
    );
    return await Promise.all(
      sections.map(async (s) => {
        const markdown = await promises.readFile(
          `./src/sections/${slug == "inf5" ? "masters" : slug}/${s}`,
          "utf-8"
        );
        const { content, data } = matter(markdown);
        return {
          content: mark.render(content),
          markdown,
          data
        };
      })
    );
  } catch (error) {
    return [];
  }
};
export async function get(req, res, next) {
  let { slug } = req.params;
  res.writeHead(200, {
    "Content-Type": "application/json"
  });
  let parsedSections = await getSections(slug);

  const pages = await promises.readdir(`./src/sections`);

  const allSections = (
    await Promise.all(
      pages.map(async (p) => {
        return getSections(p);
      })
    )
  )
    .flat()
    .map((s) => s.data);

  const markdown = await promises.readFile(`./src/pages/${slug}.md`, "utf-8");
  const { content, data } = matter(markdown);
  res.end(
    JSON.stringify({
      data,
      content: mark.render(content),
      markdown,
      sections: parsedSections,
      allSections
    })
  );
}

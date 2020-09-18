<script context="module">
  export async function preload({ params, query }) {
    // the `slug` parameter is available because
    // this file is called [slug].svelte
    const res = await this.fetch(`${params.slug}.json`);
    const data = await res.json();
    if (res.status === 200) {
      return {
        content: data.content,
        frontmatter: data.data,
        sections: data.sections,
        markdown: data.markdown,
        allSections: data.allSections
      };
    } else {
      this.error(res.status, data.message);
    }
  }
</script>

<script>
  export let content;
  export let frontmatter;
  export let sections;
  export let markdown;
  export let allSections;
  import Nav from "../components/Nav.svelte";
  import Section from "../components/Section.svelte";
  import OtherCourses from "../components/OtherCourses.svelte";
  import { key } from "../data.js";
  import { getContext } from "svelte";
  const { data } = getContext(key);
  $: pinned = sections
    .filter((s) => !!s.data.year && !!s.data.pinned)
    .sort((a, b) => a.data.title.localeCompare(b.data.title));
  $: nonPinned = sections
    .filter((s) => !!s.data.year && !s.data.pinned)
    .sort((a, b) => a.data.title.localeCompare(b.data.title));
</script>

<Nav navigation={data.navigation} />

<div style="margin: 10px; display: flex; justify-content: center">
  <!--small style="text-align: center; padding: 10px; background-color: rgba(200, 200, 200, 0.2); border-radius: 10px; margin-bottom: 10px; margin-top: 10px;">
    <a href="https://exams.is.ed.ac.uk/">Resit timetable is out!</a>
    <strong style="color:red">Interactivity down due to power outage in Edinburgh.</strong> Existing users can access the Drive from drive.google.com.
    >
</small-->
</div>
{#if frontmatter.year && frontmatter.year != 'start'}
  {#if frontmatter.levels}
    <OtherCourses page={frontmatter} sections={nonPinned} {allSections} />
  {/if}
{/if}

{@html content}
<!-- 
{% assign len =  page.path.size | minus: 3 | minus: 7 %}
{% assign name = page.path | slice: 7, len %}

{% if site.data.settings.examSeason and page.year and page.year != "start" %}
<section id="exams">
    <h3>
        <span>
            Exams
            <small>
                | <a href="https://exams.is.ed.ac.uk">official list</a>    
            </small>
        </span>
    </h3>
    {% include exams.html %}
</section>
{% endif %} -->

<!-- First show pinned sections -->

{#each pinned as section}
  <Section
    section={section.data}
    content={section.content}
    markdown={section.markdown}
    page={frontmatter} />
{/each}

<!-- Then show non-pinned sections -->

<!-- {% assign sections = site.sections | where: "year", page.year | where: "pinned", false | sort: "title" %}
{% if page.show-archived == false %}
{% assign sections = sections | where: "archived", "false" %}
{% endif %} -->

{#each nonPinned as section}
  <Section
    section={section.data}
    content={section.content}
    markdown={section.markdown}
    page={frontmatter} />
{/each}

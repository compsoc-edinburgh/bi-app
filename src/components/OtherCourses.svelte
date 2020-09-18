<script>
  export let sections;
  export let page;
  export let allSections;
  import { key } from "../data.js";
  import { getContext } from "svelte";
  const { data } = getContext(key);
  let contentsWritten = false;
  const slugify = (section) =>
    section["course-acronym"] !== ""
      ? section["course-acronym"]
      : section.title.toLowerCase().replace(/[^a-z0-9]+/g, "-");
  $: filtered = allSections.filter(
    (section) =>
      section["course-acronym"] &&
      data.courses.list[section["course-acronym"].toLowerCase()] &&
      page.levels.includes(
        data.courses.list[section["course-acronym"].toLowerCase()].level
      ) &&
      section["course-acronym"] != "proj"
  );
</script>

<p>
  {#each filtered as section, idx}
    {#if idx !== 0}&nbsp;{/if}
    {#if page.year == section.year}
      <strong>
        <a href="/inf{section.year}#{slugify(section)}">
          {section['course-acronym'].toUpperCase()}</a></strong>
    {:else}
      <a href="/inf{section.year}#{slugify(section)}">
        {section['course-acronym'].toUpperCase()}</a>
    {/if}
  {/each}
</p>

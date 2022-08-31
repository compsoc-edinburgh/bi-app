<script>
  import md from "markdown-it";
  import anchor from "markdown-it-anchor";
  import mk from "@neilsustc/markdown-it-katex";
  let mark = md({ typographer: true, html: true });
  mark.use(mk).use(anchor);

  export let section;
  export let content;
  export let markdown;
  export let page;
  import CodeMirror from "./CodeMirror.svelte";
  import { stores } from "@sapper/app";
  const { preloading, page: rpage, session } = stores();
  let textarea;

  let localMarkdown;
  import { key } from "../data.js";
  import { getContext, onMount } from "svelte";
  import Renderer from "markdown-it/lib/renderer";
  const { data } = getContext(key);
  let editing = false;
  let editor;
  $: course = data.courses.list[section["course-acronym"]];
  $: semester = course ? course.delivery_ordinal : section.semester;
  $: hideSection = section.archived;
  $: sectionID =
    section["course-acronym"] && section["course-acronym"] !== ""
      ? section["course-acronym"]
      : section.title.toLowerCase().replace(/[^a-z0-9]+/g, "-");
  const loadEditor = async () => {
    // Wait for editor to be mounted
    setTimeout(() => {
      editor.set(localMarkdown || markdown, "md");
    }, 0);
  };
  $: if (editing) {
    loadEditor();
  }
  let highlight = "";
  onMount(() => {
    const local = sessionStorage.getItem(`${$rpage.params.slug}/${sectionID}`);
    if (local && local != markdown) {
      localMarkdown = local;
      highlight = "rgba(255,255,0,0.2)";
    } else {
      sessionStorage.removeItem(`${$rpage.params.slug}/${sectionID}`);
    }
  });
  const save = async () => {
    sessionStorage.setItem(`${$rpage.params.slug}/${sectionID}`, localMarkdown);
    console.log(sectionID);
    editing = false;
    highlight = "rgba(255,255,0,0.2)";

    fetch("https://save-section.compsoc.workers.dev", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        page: $rpage.params.slug,
        section: sectionID,
        content: localMarkdown,
        data: section
      })
    });
  };
</script>

<section
  id={sectionID}
  data-semester={semester}
  style="{hideSection ? 'display: none' : ''}; background-color: {highlight}">
  <h3>
    <span>
      {#if section.link}
        <a href={section.link}>{section.title}</a>
      {:else if section['course-acronym'] != ''}
        {#if section.learn}
          <a
            href="https://course.inf.ed.ac.uk/{section['course-acronym']}/">{section.title}</a>
        {:else}
          <a
            href="https://www.inf.ed.ac.uk/teaching/courses/{section['course-acronym']}/">{section.title}</a>
        {/if}
      {/if}

      <small>
        {#if section.links}
          {#each section.links as link, index}
            {index !== 0 ? ',' : ''}
            <a href={link.url}>{link.name}</a>
          {/each}
        {/if}
        {#if course}
          | <a href={course.euclid_url}>drps</a>, <a href="http://course.inf.ed.ac.uk/{section['course-acronym']}">info</a>
          {#if course.cw_exam_ratio.first != 100}
            ,<a href="https://exampapers.ed.ac.uk/search/{course.euclid_code}">papers</a>
          {/if}
          {#if course.year != page.year}
            This course is misplaced. It should be on the year {course.year} page.
          {/if}
        {/if}
      </small>

      <a class="link-icon" href="#{sectionID}"><i
          class="fa fa-link"
          aria-hidden="true" /></a>
    </span>

    <span>
      {#if course && course.diet && course.diet != ''}
        <span style="color: gray; font-size: .6rem;">{course.diet} exam</span>
      {/if}
      {#if !editing}
        <small><button class="edit-pencil" on:click={() => (editing = true)}><i
              class="fa fa-pencil"
              aria-hidden="true" /> Edit</button></small>
      {:else}
        <small><button class="edit-pencil" on:click={() => save()}><i
              class="fa fa-save"
              aria-hidden="true" /> Save</button></small>
      {/if}
    </span>
  </h3>
  {#if !editing}
    {#if highlight}
      <small><i>This is a preview of edits you've made. Your changes should be
          visible for everyone within a minute or two</i></small>
    {/if}
    {@html localMarkdown ? mark.render(localMarkdown) : content}
  {:else}
    <CodeMirror
      bind:this={editor}
      on:change={(e) => (localMarkdown = e.detail.value)}
      lineNumbers={false} />
  {/if}
</section>

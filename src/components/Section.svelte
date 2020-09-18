<script>
  export let section;
  export let content;
  export let markdown;
  export let page;
  import CodeMirror from "./CodeMirror.svelte";
  import { stores } from "@sapper/app";
  const { preloading, page: rpage, session } = stores();
  let textarea;

  $: localMarkdown = markdown;
  import { key } from "../data.js";
  import { getContext, onMount } from "svelte";
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
      editor.set(markdown, "md");
    }, 0);
  };
  $: if (editing) {
    loadEditor();
  }
  const save = async () => {
    console.log(sectionID);
    fetch("https://save-section.compsoc.workers.dev", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        page: $rpage.params.slug,
        section: sectionID,
        content: localMarkdown
      })
    });
  };
</script>

<section
  id={sectionID}
  data-semester={semester}
  style={hideSection ? 'display: none' : ''}>
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
    {@html content}
  {:else}
    <CodeMirror
      bind:this={editor}
      on:change={(e) => (localMarkdown = e.detail.value)}
      lineNumbers={false} />
  {/if}
</section>

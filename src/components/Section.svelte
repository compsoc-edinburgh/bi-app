<script>
  export let section;
  export let content;
  export let page;
  import { key } from "../data.js";
  import { getContext } from "svelte";
  const { data } = getContext(key);

  $: course = data.courses.list[section["course-acronym"]];
  $: semester = course ? course.delivery_ordinal : section.semester;
  $: hideSection = section.archived;
  $: sectionID =
    section["course-acronym"] !== ""
      ? section["course-acronym"]
      : section.title.toLowerCase().replace(/[^a-z0-9]+/g, "-");
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
      <small><a
          class="edit-pencil"
          href="https://github.com/{data.repo}/edit/master/{section.path}"><i
            class="fa fa-pencil"
            aria-hidden="true" /> Edit on GitHub</a></small>
    </span>
  </h3>
  {@html content}
</section>

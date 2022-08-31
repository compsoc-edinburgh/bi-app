<script>
  export let navigation;
  import { stores } from "@sapper/app";
  const { preloading, page, session } = stores();
</script>

<nav id="menu" class="hide-on-small">
  {#each navigation as nav}
    <a
      href="/{nav.url || ''}"
      id="btn_{nav.url || ''}"
      class="ir {$page.path === `/${nav.url || ''}` ? 'active' : ''}"><h2>
        {nav.title}
      </h2></a>
  {/each}
</nav>

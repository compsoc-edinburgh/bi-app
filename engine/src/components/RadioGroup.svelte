<script>
  export let options;
  export let name;
  export let value = "";
</script>

<style>
  input[type="radio"]:checked + label {
    background-color: #d3371e;
    color: white;
  }
</style>

<div class="flex flex-row flex-wrap">
  {#each options as option}
    <input
      type="radio"
      {name}
      value={option.label}
      bind:group={value}
      id="{name}-{option.label}"
      class="hidden" />
    <label
      for="{name}-{option.label}"
      class="appearance-none block bg-gray-200 text-gray-700 rounded py-3 px-4
        leading-tight m-1 hover:bg-gray-400 flex-grow focus:outline-none
        focus:bg-white text-center cursor-pointer font-bold">{option.display}</label>
  {/each}
</div>

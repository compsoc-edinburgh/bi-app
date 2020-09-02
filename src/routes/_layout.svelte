<style global>
  @tailwind base;
  @tailwind components;
  @tailwind utilities;
  html,
  body,
  #sapper {
    height: 100%;
    background: #fafafa;
  }
  body * {
    border-color: initial;
  }
</style>

<nav class="absolute h-16 top-0 left-0 m-2 flex flex-row items-center group">
  <img
    src="compsoc-profile-white-nomargin.png"
    alt="Logo"
    class="object-contain w-16 h-16" />
  <svg
    class="w-6 h-6 ml-2 transition-all transform scale-100 group-hover:scale-125
      duration-200 ease-in-out"
    viewBox="0 0 72 72"
    xmlns="http://www.w3.org/2000/svg">
    <g id="color">
      <path
        class="text-gray-700 group-hover:text-primary transition-colors
          duration-200"
        fill="currentColor"
        d="M59.5,25c0-6.9036-5.5964-12.5-12.5-12.5c-4.7533,0-8.8861,2.6536-11,6.5598 C33.8861,15.1536,29.7533,12.5,25,12.5c-6.9036,0-12.5,5.5964-12.5,12.5c0,2.9699,1.0403,5.6942,2.7703,7.8387l-0.0043,0.0034 L36,58.5397l20.7339-25.6975l-0.0043-0.0034C58.4597,30.6942,59.5,27.9699,59.5,25z" />
    </g>
    <g id="line">
      <path
        fill="none"
        class="text-gray-800 group-hover:text-primary"
        stroke="currentColor"
        stroke-linejoin="round"
        stroke-miterlimit="10"
        stroke-width="2"
        d="M59.5,25 c0-6.9036-5.5964-12.5-12.5-12.5c-4.7533,0-8.8861,2.6536-11,6.5598C33.8861,15.1536,29.7533,12.5,25,12.5 c-6.9036,0-12.5,5.5964-12.5,12.5c0,2.9699,1.0403,5.6942,2.7703,7.8387l-0.0043,0.0034L36,58.5397l20.7339-25.6975l-0.0043-0.0034 C58.4597,30.6942,59.5,27.9699,59.5,25z" />
    </g>
  </svg>
  <div class="ml-1 text-xl text-gray-800">you</div>
</nav>
<slot />

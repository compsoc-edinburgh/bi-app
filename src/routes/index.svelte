<script>
  import RadioGroup from "../components/RadioGroup.svelte";
  let name;
  let email;
  let studentNumber;
  let year;
  let dataConsent;
  let needsMatch;
  const years = [
    { label: "year-2", display: "2nd" },
    { label: "year-3", display: "3rd" },
    { label: "year-4", display: "4th" },
    { label: "year-5", display: "5th" }
  ];
</script>

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
<main class="overflow-x-hidden">
  <h1 class="font-display text-4xl sm:text-5xl text-center text-primary mt-20">
    Ac<span class="text-gray-900">Fams</span>
  </h1>
  <div class="grid grid-cols-1 lg:grid-cols-2">
    <section
      class="prose sm:prose-md md:prose-lg p-4 pt-16 max-w-2xl mx-auto lg:m-0
        lg:sticky lg:top-0 w-full lg:ml-auto">
      <h2 class="text-center">
        CompSoc family, we have a big announcement for you!
      </h2>
      <p class="text-gray-600 text-sm mt-2">
        Are you in 1st year? Go to <a
          href="/children"
          rel="prefetch">family.comp-soc.com/children</a> instead
      </p>
      <p>
        We’ve been working hard to make plans for the upcoming year that
        accommodate all of you, and part of this plan is to introduce Academic
        Families!
      </p>
      <p>
        This is where students in older years ‘adopt’ freshers, and it’s a great
        way of helping the community, meeting new people, and having a good time
        together! We’re keeping it simple for now, with students in year 2 or
        above as the parents, and freshers as the children - but from next year
        we’ll have this year’s parents as grandparents.
      </p>
      <p>
        Once we have all of you who want to get involved in, we’ll be asking you
        to create a ‘bio’ to encourage freshers; this won’t be compulsory but it
        will really help the scheme to take off, and we’ll even have some of our
        committee members posting theirs to inspire you.
      </p>
      <p>
        Anyone in CompSoc is welcome to join, and you can even propose to your
        AcFam spouse-to-be!
      </p>
      <p>
        To sign up as a parent all you need to do is fill out this form by the <strong>7th
          of September<strong /></strong>
      </p>
      <p>
        If you would like to ask any questions about becoming a parent or for
        help with the form please email <a
          href="mailto:hello@comp-soc.com">hello@comp-soc.com</a>.
      </p>
    </section>
    <section
      class="p-4 pt-4 lg:pt-16 max-w-2xl mx-auto w-full lg:m-0 lg:mr-auto pb-32">
      <form
        class="w-full"
        data-netlify="true"
        name="parent"
        method="POST"
        action="/success">
        <div class="w-full px-3 mb-6">
          <label
            class="block text-gray-700 text-lg mb-2 focus:font-bold
              active:font-bold"
            for="name">
            What's your name?
          </label>
          <input
            class="appearance-none block w-full bg-gray-200 text-gray-700
              border-2 border-gray-200 rounded py-3 px-4 mb-3 leading-tight
              focus:outline-none focus:bg-white focus:border-gray-500"
            id="name"
            type="text"
            placeholder="Ada Lovelace" />
        </div>
        <div class="w-full px-3 mb-6">
          <label class="block text-gray-700 text-lg mb-2" for="email">
            What's your email?
          </label>
          <input
            class="appearance-none block w-full bg-gray-200 text-gray-700
              border-2 border-gray-200 rounded py-3 px-4 mb-3 leading-tight
              focus:outline-none focus:bg-white focus:border-gray-500"
            id="email"
            type="email"
            placeholder="ada@lovelace.com" />
        </div>
        <div class="w-full px-3 mb-6">
          <label class="block text-gray-700 text-lg mb-2" for="student-number">
            What's your student number?
          </label>
          <input
            class="appearance-none block w-full bg-gray-200 text-gray-700
              border-2 border-gray-200 rounded py-3 px-4 mb-3 leading-tight
              focus:outline-none focus:bg-white focus:border-gray-500"
            id="student-number"
            type="email"
            placeholder="s1234567" />
        </div>
        <div class="w-full px-3 mb-6">
          <label class="block text-gray-700 text-lg mb-2">
            Which year will you be in <strong>September 2020</strong>?
          </label>
          <RadioGroup name="year-select" options={years} />
          <p class="text-gray-600 text-xs mt-2">
            Are you in 1st year? Sign up as an academic child at <a
              href="/children"
              rel="prefetch"
              class="text-primary">family.comp-soc.com/children</a> instead
          </p>
        </div>
        <div class="w-full px-3 mb-6">
          <label class="block text-gray-700 text-lg mb-2">
            Have you already found a spouse?
          </label>
          <RadioGroup
            name="needs-match"
            bind:value={needsMatch}
            options={[{ label: 'yes', display: 'Yes' }, { label: 'no', display: 'No' }]} />
          <p class="text-gray-600 text-xs mt-2">
            If you haven't found a spouse yet we'll find you a match
          </p>
        </div>
        {#if needsMatch === 'yes'}
          <div class="w-full px-3 mb-6">
            <label
              class="block text-gray-700 text-lg mb-2 focus:font-bold
                active:font-bold"
              for="spouse-name">
              What's your spouse's name?
            </label>
            <input
              class="appearance-none block w-full bg-gray-200 text-gray-700
                border-2 border-gray-200 rounded py-3 px-4 mb-3 leading-tight
                focus:outline-none focus:bg-white focus:border-gray-500"
              id="spouse-name"
              type="text"
              placeholder="Grace Hopper" />
            <p class="text-gray-600 text-xs mt-2">
              Remember, they'll need to fill in this form as well
            </p>
          </div>
        {/if}
        <div class="w-full px-3 mb-6">
          <label
            class="block text-gray-700 text-lg mb-2 focus:font-bold
              active:font-bold"
            for="bio">
            Tell us a bit about yourself
          </label>
          <textarea
            class="appearance-none block w-full bg-gray-200 text-gray-700
              border-2 border-gray-200 rounded py-3 px-4 mb-3 leading-tight
              focus:outline-none focus:bg-white focus:border-gray-500
              resize-none h-32"
            id="bio"
            placeholder="Hobbies, interests, academic focus etc..." />
          <p class="text-gray-600 text-xs mt-2">
            This won't be public, it's just for our information
          </p>
        </div>
        <div class="w-full px-3 mb-6">
          <label class="block text-gray-700 text-lg mb-2">
            With the COVID-19 pandemic, we know that many students are studying
            virtually this year. So we can support you with this, what types of
            events would you be willing to attend or organise?
          </label>
          <RadioGroup
            name="needs-match"
            bind:value={needsMatch}
            options={[{ label: 'in-person', display: 'In person' }, { label: 'virtual', display: 'Virtual' }, { label: 'both', display: 'Both' }]} />
          <p class="text-gray-600 text-xs mt-2">
            Don't worry, this isn't a final commitment &mdash; if your
            circumstances change just let us know
          </p>
        </div>
        <div class="prose px-3">
          <h3>Your data</h3>
          <p>
            We'll store your data for the duration of the academic families
            program this year
          </p>
          <h4>Your name, email and student number</h4>
          <ul>
            <li>
              We'll use these to verify your CompSoc membership, contact you
              about academic families, and to match you with your spouse
            </li>
            <li>
              We'll also provide your <strong>name</strong> and <strong>email</strong>
              to your academic child (or children) once matched
            </li>
            <li>
              We won't use your details to send marketing emails, or any other
              emails unrelated to academic families
            </li>
          </ul>
          <h4>Your year of study and other information you've provided us</h4>
          <ul>
            <li>
              We'll use this information to help us match you with a spouse,
              and/or children
            </li>
            <li>
              This won't be provided to your academic children &mdash; you'll
              have an opportunity at a later stage to provide a bio for them
            </li>
          </ul>
          <h4>Your rights</h4>
          Under the GDPR, you have certain rights with regards to your data (See <a
            href="https://gdpr.eu/tag/chapter-3/">Rights of the Data Subject</a>
          for a full list). Some important ones are the right to:
          <ul>
            <li><strong>request a copy of your data</strong></li>
            <li><strong>correct any of your data that's innacurate</strong></li>
            <li>
              <strong>request deletion of your data</strong> (although that will
              prevent you participating in academic families this year)
            </li>
          </ul>
          <p>
            Please contact <a
              href="mailto:techsec@comp-soc.com"
              class="text-primary">techsec@comp-soc.com</a> with any queries
          </p>
        </div>
        <div class="w-full px-3 mb-6 mt-8">
          <label class="block text-gray-700 text-lg mb-2">
            Do you consent to us using your data as outlined above?
          </label>
          <RadioGroup
            name="data-consent"
            bind:value={dataConsent}
            options={[{ label: 'yes', display: 'Yes' }, { label: 'no', display: 'No' }]} />
          <p class="text-gray-600 text-xs mt-2">
            If you have any questions or concerns, please email <a href="mailto:techsec@comp-soc.com" class="text-primary">techsec@comp-soc.com</a>
          </p>
        </div>
        <div class="w-full px-3 mb-6 mt-8 flex">
          <button
            type="submit"
            disabled={dataConsent !== 'yes'}
            class="{dataConsent !== 'yes' ? 'bg-gray-400 cursor-not-allowed' : 'bg-primary cursor-pointer'}
              appearance-none block rounded py-3 px-4 leading-tight flex-grow focus:outline-none
              text-center font-bold text-white">Submit</button>
        </div>
      </form>
      <!-- <iframe
        src="https://docs.google.com/forms/d/e/1FAIpQLSeTxbQA0XTukP3NuEZfb5rHCGR2EXEOtnDSYq-nZS7hBcCQ_w/viewform?embedded=true"
        width="100%"
        title="AcFam Parent Signup"
        height="3000"
        frameborder="0"
        marginheight="0"
        marginwidth="0">Loading…</iframe> -->
    </section>
  </div>
</main>

<script>
  import RadioGroup from "../components/RadioGroup.svelte";
  import { flip } from "svelte/animate";
  import { goto } from "@sapper/app";
  import Success from "./success.svelte";
  let name;
  let email;
  let studentNumber;
  let degreeProgram;
  let bio;
  let eventsPreference;
  let dataConsent;

  let submitting = false;
  const submit = async () => {
    submitting = true;

    const r = await fetch("https://child-slack-injest.compsoc.workers.dev", {
      method: "POST",

      body: JSON.stringify({
        text: `
  *Picture*: ${picture}
  *Name*: ${name}
  *Email*: ${email}
  *Student Number*: ${studentNumber}
  *Degree Program*: ${degreeProgram}
  *Bio*: ${bio}
  *Events*: ${eventsPreference}
          `,
        icon_url: picture,
        username: name,
        attachments: [
          {
            fallback: "JSON",
            color: "good", // Can either be one of 'good', 'warning', 'danger', or any hex color code

            // Fields are displayed in a table on the message
            fields: [
              {
                title: "JSON", // The title may not contain markup and will be escaped for you
                value: JSON.stringify({
                  picture,
                  name,
                  email,
                  studentNumber,
                  degreeProgram,
                  bio,
                  eventsPreference
                }),
                short: false // Optional flag indicating whether the `value` is short enough to be displayed side-by-side with other values
              }
            ]
          }
        ]
      })
    });
    if (r.ok) {
      submitting = false;
      goto("/success");
    }
  };
  let file;
  let cls;
  let percentage = 0;
  let picture = "";
  const chooseFile = (e) => {
    cls = "border-blue-500";
    console.log(e);
    file.click();
  };
  const dropFile = (e) => {
    const dt = e.dataTransfer;
    const files = dt.files;
    uploadFile({ target: { files } });
  };
  const uploadFile = async (e) => {
    let file = e.target.files[0];
    if (!file) return;
    const upload = await (
      await fetch("https://image-worker.compsoc.workers.dev", {
        headers: {
          "Content-Type": file.type
        }
      })
    ).json();
    const reader = new FileReader();
    const xhr = new XMLHttpRequest();
    xhr.upload.addEventListener(
      "progress",
      (e) => {
        if (e.lengthComputable) {
          percentage = Math.round((e.loaded * 100) / e.total);
          console.log(percentage);
        }
      },
      false
    );

    xhr.upload.addEventListener(
      "load",
      (e) => {
        percentage = 100;
        picture = upload.access;
      },
      false
    );
    xhr.open("PUT", upload.signed);
    xhr.setRequestHeader("x-amz-acl", "public-read");
    xhr.setRequestHeader("Content-Type", file.type);
    xhr.overrideMimeType(file.type);
    reader.onload = function (evt) {
      xhr.send(evt.target.result);
    };
    reader.readAsArrayBuffer(file);
  };
  const dragenter = (e) => {
    console.log(e);
    cls = "border-blue-500";
  };

  $: submissionEnabled =
    dataConsent === "yes" &&
    name &&
    picture &&
    email &&
    studentNumber &&
    yearOfStudy &&
    degreeProgram &&
    bio;
</script>

<svelte:head>
  <meta property="og:url" content="https://family.comp-soc.com/children" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="CompSoc AcFams" />
  <meta property="og:image" content="https://family.comp-soc.com/social.png" />
  <meta property="og:image:alt" content="CompSoc AcFams" />
  <meta property="og:description" content="CompSoc AcFams" />

  <meta name="twitter:card" content="summary" />

  <meta name="twitter:url" content="https://family.comp-soc.com/children" />
  <meta name="twitter:title" content="CompSoc AcFams" />
  <meta name="twitter:description" content="CompSoc AcFams" />
  <meta name="twitter:image" content="https://family.comp-soc.com/social.png" />
</svelte:head>
<main class="overflow-x-hidden">
  <h1 class="font-display text-4xl sm:text-5xl text-center text-primary mt-20">
    Ac<span class="text-gray-900">Fams</span>
  </h1>
  <div class="grid grid-cols-1 lg:grid-cols-2">
    <section
      class="prose sm:prose-md md:prose-lg p-4 pt-16 max-w-2xl mx-auto lg:m-0
        lg:sticky lg:top-0 w-full lg:ml-auto">
      <h2 class="text-center">Calling all Freshers!</h2>
      <p>
        You can now sign up for CompSoc AcFams! These academic families are
        being introduced this year to help you settle into university life, and
        to give you more opportunities to socialise with fellow students
        (especially considering the current variations in studying
        arrangements).
      </p>
      <p>
        This is where students in older years ‘adopt’ freshers, and it’s a great
        way of helping the community, meeting new people, and having a good time
        together! We’re keeping it simple for now, with students in year 2 or
        above as the parents, and freshers as the children.
      </p>
      <p>
        We’ve had an amazing number of aspiring academic parents sign up so far,
        but now it’s your turn to sign up and complete your academic family.
      </p>

      <p>
        To sign up as an AcFam child all you need to do is fill out this form by
        the <strong>27th of September<strong />, so you've got plenty of time!
        </strong>
      </p>
      <p>
        If you would like to ask any questions or need help with the form please
        email <a href="mailto:hello@comp-soc.com">hello@comp-soc.com</a>.
      </p>
    </section>
    <section
      class="p-4 pt-4 lg:pt-16 max-w-2xl mx-auto w-full lg:m-0 lg:mr-auto pb-32">
      <form class="w-full" name="parent">
        <div
          class="bg-white shadow rounded-full sm:mx-auto grid h-40 w-40
            justify-center items-center mb-6 border-white cursor-pointer {cls} relative"
          on:click={chooseFile}
          on:dragenter|preventDefault|stopPropagation={dragenter}
          on:dragover|preventDefault|stopPropagation={dragenter}
          on:dragleave|preventDefault|stopPropagation={() => (cls = '')}
          on:drop|preventDefault|stopPropagation={dropFile}>
          <input
            bind:this={file}
            on:change={uploadFile}
            type="file"
            accept="image/*"
            class="hidden" />
          <img
            class="rounded-full w-40 h-40 object-cover"
            src={picture || '/avatar.svg'}
            alt="{name}'s image'"
            on:load={() => (percentage === 100 ? setTimeout(() => (percentage = 0), 500) : null)} />
          <div
            class="absolute bg-blue-500 h-40 w-40 top-0 left-0 rounded-full"
            style="transform: scale({percentage / 100}); transition: transform .2s" />
          <div
            class="text-white bg-gray-600 rounded-full h-10 w-10 z-10 absolute
              bottom-0 right-0">
            <div>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
            </div>
          </div>
          <p class="text-gray-600 text-xs mt-2">We require a picture of you</p>
        </div>
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
            bind:value={name}
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
            bind:value={email}
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
            type="text"
            bind:value={studentNumber}
            placeholder="s1234567" />
        </div>

        <div class="w-full px-3 mb-6">
          <label class="block text-gray-700 text-lg mb-2" for="degree-program">
            What's your degree program?
          </label>
          <input
            class="appearance-none block w-full bg-gray-200 text-gray-700
              border-2 border-gray-200 rounded py-3 px-4 mb-3 leading-tight
              focus:outline-none focus:bg-white focus:border-gray-500"
            id="degree-program"
            type="text"
            bind:value={degreeProgram}
            placeholder="BSc Computer Science" />
        </div>

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
            bind:value={bio}
            placeholder="Hobbies, interests, academic focus etc..." />
          <p class="text-gray-600 text-xs mt-2">
            This will help us match you with parents, and it'll be send to your
            future parents to help them get to know you
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
            bind:value={eventsPreference}
            options={[{ label: 'Physical', display: 'In person' }, { label: 'Virtual', display: 'Virtual' }, { label: 'Physical or Virtual', display: 'Both' }]} />
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
          <h4>Your name, email, picture, and student number</h4>
          <ul>
            <li>
              We'll use these to verify your CompSoc membership and contact you
              about academic families
            </li>
            <li>
              We'll also provide your <strong>name</strong>, <strong>email</strong>,
              and <strong>picture</strong> to your academic parents once matched,
              so the can contact you
            </li>
            <li>
              We won't use your details to send marketing emails, or any other
              emails unrelated to academic families
            </li>
          </ul>
          <h4>
            Your year of study, degree program and other information you've
            provided us
          </h4>
          <ul>
            <li>
              We'll use this information to help us match you with academic
              parents
            </li>
            <li>
              Your <strong>degree program</strong> and <strong>bio</strong> will
              also be provided to your future academic parents to help them get to
              know you
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
            on:click|preventDefault={submit}
            disabled={!submissionEnabled}
            class="{submissionEnabled ? 'bg-primary cursor-pointer' : 'bg-gray-400 cursor-not-allowed'}
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
{#if submitting}
  <div
    class="fixed w-full h-full top-0 left-0 bg-gray-900 bg-opacity-75 grid
      items-center justify-center align-middle z-20">
    <h2>
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        class="w-8 h-8 inline-block text-white"
        stroke="currentColor">
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
      </svg>
      <span class="text-2xl ml-2 align-middle text-white">Saving...</span>
    </h2>
  </div>
{/if}

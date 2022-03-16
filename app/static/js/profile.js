const avatar_input = document.getElementById("avatar");
const submit_btn = document.getElementById("submit");

submit_btn.addEventListener("click", () => {
  const { files } = avatar_input;
  console.log(files);
});

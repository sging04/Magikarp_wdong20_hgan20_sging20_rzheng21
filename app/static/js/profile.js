const avatar_input = document.getElementById("avatar");
const submit_btn = document.getElementById("submit");

const reader = new FileReader();

submit_btn.addEventListener("click", () => {
  const { files } = avatar_input;
  if (files.length == 0) return;

  reader.readAsDataURL(files[0]);
});

reader.addEventListener("load", () => {
  fetch(document.URL, {
    method: "POST",
    body: reader.result,
  })
    .then((res) => {
      console.log("Success", res);
      location.reload();
    })
    .catch((err) => console.log("Error", err));
});

document.addEventListener("DOMContentLoaded", function () {
  const searchIcon = document.getElementById("searchIcon");
  const searchContainer = document.getElementById("searchContainer");

  searchIcon.addEventListener("click", function () {
    searchContainer.classList.toggle("show");
    if (searchContainer.classList.contains("show")) {
      document.getElementById("searchInput").focus(); // Focus on the input field when shown
    }
  });
});

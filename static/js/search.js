document.addEventListener("DOMContentLoaded", () => {
  const input = document.querySelector("#searchInput");
  const cards = Array.from(document.querySelectorAll(".event-card"));
  const noResult = document.querySelector("#searchNoResult");

  // Kolom pencarian menyaring kartu event pada halaman beranda.
  if (!input || !cards.length) return;

  function filterEvents() {
    const query = input.value.trim().toLocaleLowerCase("id-ID");
    let visible = 0;

    cards.forEach((card) => {
      const searchableText = (card.dataset.search || "").toLocaleLowerCase("id-ID");
      const matches = !query || searchableText.includes(query);
      card.hidden = !matches;
      if (matches) visible += 1;
    });

    noResult.hidden = visible !== 0;
  }

  input.addEventListener("input", filterEvents);
});

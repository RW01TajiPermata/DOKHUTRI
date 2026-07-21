document.addEventListener("DOMContentLoaded", () => {
  const hero = document.querySelector(".hero");
  if (!hero) return;

  const slides = Array.from(hero.querySelectorAll(".hero-slide"));
  const dots = Array.from(hero.querySelectorAll("[data-hero-dot]"));
  if (slides.length < 2) return;

  let current = 0;
  let timer;

  function showSlide(index) {
    current = (index + slides.length) % slides.length;
    slides.forEach((slide, position) => slide.classList.toggle("is-active", position === current));
    dots.forEach((dot, position) => dot.classList.toggle("is-active", position === current));
  }

  function restartTimer() {
    window.clearInterval(timer);
    timer = window.setInterval(() => showSlide(current + 1), 2000);
  }

  hero.querySelector("[data-hero-prev]").addEventListener("click", () => { showSlide(current - 1); restartTimer(); });
  hero.querySelector("[data-hero-next]").addEventListener("click", () => { showSlide(current + 1); restartTimer(); });
  dots.forEach((dot) => dot.addEventListener("click", () => { showSlide(Number(dot.dataset.heroDot)); restartTimer(); }));

  hero.addEventListener("mouseenter", () => window.clearInterval(timer));
  hero.addEventListener("mouseleave", restartTimer);
  restartTimer();
});

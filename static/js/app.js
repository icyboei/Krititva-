/**
 * Krititva Application JavaScript
 * Core UI interactions, navigation, and input handling
 */

document.addEventListener("DOMContentLoaded", () => {
  // 1. Mobile Menu Toggle
  const mobileMenuBtn = document.getElementById("mobile-menu-toggle");
  const navLinks = document.querySelector(".nav-links");

  if (mobileMenuBtn && navLinks) {
    mobileMenuBtn.addEventListener("click", () => {
      const isVisible = navLinks.style.display === "flex";
      navLinks.style.display = isVisible ? "none" : "flex";
      if (!isVisible) {
        navLinks.style.flexDirection = "column";
        navLinks.style.position = "absolute";
        navLinks.style.top = "70px";
        navLinks.style.left = "0";
        navLinks.style.right = "0";
        navLinks.style.backgroundColor = "var(--color-paper-ivory)";
        navLinks.style.padding = "var(--space-md) var(--space-lg)";
        navLinks.style.boxShadow = "var(--shadow-elevated)";
        navLinks.style.borderBottom = "1px solid var(--color-soft-border)";
      }
    });
  }

  // 2. Example Repository Chip Selection
  const exampleChips = document.querySelectorAll(".example-repo-chip");
  const repoInput = document.getElementById("repo-url-input");

  if (exampleChips && repoInput) {
    exampleChips.forEach((chip) => {
      chip.addEventListener("click", () => {
        const url = chip.getAttribute("data-repo");
        if (url) {
          repoInput.value = url;
          repoInput.focus();
        }
      });
    });
  }

  // 3. Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      const targetId = this.getAttribute("href");
      if (targetId && targetId !== "#" && document.querySelector(targetId)) {
        e.preventDefault();
        document.querySelector(targetId).scrollIntoView({
          behavior: "smooth",
        });
      }
    });
  });
});

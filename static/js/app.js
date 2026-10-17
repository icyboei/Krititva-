/**
 * Krititva Application JavaScript
 * Core UI interactions, navigation, modal management, and workspace collaboration
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

  // 2. Modals: Post Project Brief (Client) & List Capability (Provider)
  const btnOpenBriefModal = document.getElementById("btn-open-brief-modal");
  const btnOpenServiceModal = document.getElementById("btn-open-service-modal");
  const modalBrief = document.getElementById("modal-project-brief");
  const modalService = document.getElementById("modal-list-service");
  const closeButtons = document.querySelectorAll(".btn-close-modal");

  function openModal(modal) {
    if (modal) modal.style.display = "flex";
  }

  function closeModal(modal) {
    if (modal) modal.style.display = "none";
  }

  if (btnOpenBriefModal) {
    btnOpenBriefModal.addEventListener("click", () => openModal(modalBrief));
  }
  if (btnOpenServiceModal) {
    btnOpenServiceModal.addEventListener("click", () => openModal(modalService));
  }

  closeButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      closeModal(modalBrief);
      closeModal(modalService);
    });
  });

  window.addEventListener("click", (e) => {
    if (e.target === modalBrief) closeModal(modalBrief);
    if (e.target === modalService) closeModal(modalService);
  });

  // 3. Post a Project Brief Form Submission
  const formPostBrief = document.getElementById("form-post-brief");
  if (formPostBrief) {
    formPostBrief.addEventListener("submit", (e) => {
      e.preventDefault();
      const title = document.getElementById("brief-title").value;
      alert(`Project brief "${title}" successfully published! Providers in this category will be notified.`);
      closeModal(modalBrief);
      window.location.href = "/workspace";
    });
  }

  // 4. List Capability (Provider) Form Submission
  const formListService = document.getElementById("form-list-service");
  if (formListService) {
    formListService.addEventListener("submit", async (e) => {
      e.preventDefault();
      const payload = {
        title: document.getElementById("service-title").value,
        provider_name: document.getElementById("provider-name").value,
        provider_title: document.getElementById("provider-title").value,
        category: document.getElementById("service-category").value,
        description: document.getElementById("service-desc").value,
        indicative_pricing: document.getElementById("service-price").value,
        typical_duration: document.getElementById("service-duration").value,
        deliverables: [
          "Complete Architectural Blueprint",
          "Production Codebase Delivery",
          "Verified Verification Tests & Documentation"
        ]
      };

      try {
        const resp = await fetch("/api/services", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        if (resp.ok) {
          alert("Your capability listing has been published to the exchange!");
          closeModal(modalService);
          window.location.reload();
        }
      } catch (err) {
        console.error("Error creating service:", err);
      }
    });
  }

  // 5. Bilateral Collaboration Chat (Workspace)
  let activeRole = "client";
  const roleButtons = document.querySelectorAll(".btn-role-switch");
  const chatForm = document.getElementById("chat-input-form");
  const chatInput = document.getElementById("chat-message-input");
  const messageStream = document.getElementById("message-stream");

  roleButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      roleButtons.forEach((b) => {
        b.style.background = "var(--color-paper-ivory)";
        b.style.color = "var(--color-deep-espresso)";
        b.style.fontWeight = "600";
      });
      btn.style.background = "var(--color-deep-espresso)";
      btn.style.color = "#ffffff";
      btn.style.fontWeight = "700";
      activeRole = btn.getAttribute("data-role");
    });
  });

  if (chatForm && chatInput && messageStream) {
    chatForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const content = chatInput.value.trim();
      if (!content) return;

      try {
        const resp = await fetch("/api/workspace/message", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ role: activeRole, content })
        });

        if (resp.ok) {
          const result = await resp.json();
          const msg = result.message;

          const bubble = document.createElement("div");
          bubble.className = `chat-bubble chat-${msg.sender}`;
          bubble.style.maxWidth = "85%";
          bubble.style.alignSelf = msg.sender === "client" ? "flex-start" : "flex-end";
          bubble.style.background = msg.sender === "client" ? "var(--color-cream-light)" : "#fdf8f4";
          bubble.style.border = `1px solid ${msg.sender === "client" ? "var(--color-soft-border)" : "#e8c8b5"}`;
          bubble.style.borderRadius = "var(--radius-md)";
          bubble.style.padding = "0.7rem 0.95rem";

          bubble.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: baseline; gap: var(--space-sm); margin-bottom: 0.25rem;">
              <span style="font-size: 0.78rem; font-weight: 700; color: ${msg.sender === "client" ? "var(--color-deep-espresso)" : "var(--color-terracotta)"};">
                ${msg.author}
              </span>
              <span style="font-size: 0.7rem; color: var(--color-muted-text);">${msg.timestamp}</span>
            </div>
            <p style="font-size: 0.88rem; color: var(--color-deep-espresso); line-height: 1.45; margin: 0;">
              ${msg.content}
            </p>
          `;

          messageStream.appendChild(bubble);
          messageStream.scrollTop = messageStream.scrollHeight;
          chatInput.value = "";
        }
      } catch (err) {
        console.error("Error sending message:", err);
      }
    });
  }

  // 6. Milestone Approval & Release Action (Client Role)
  const approveButtons = document.querySelectorAll(".btn-approve-milestone");
  approveButtons.forEach((btn) => {
    btn.addEventListener("click", async () => {
      const milestoneId = btn.getAttribute("data-id");
      if (!confirm(`Are you sure you want to approve Milestone ${milestoneId} and release the milestone funds from escrow?`)) {
        return;
      }

      try {
        const resp = await fetch(`/api/workspace/milestone/${milestoneId}/approve`, {
          method: "POST"
        });
        if (resp.ok) {
          const badge = document.querySelector(`.badge-${milestoneId}`);
          if (badge) {
            badge.textContent = "Approved & Released";
            badge.style.background = "#e8f5e9";
            badge.style.color = "#2e7d32";
          }
          btn.parentElement.innerHTML = `<span style="color: #2e7d32; font-weight: 700; font-size: 0.85rem;">&#10004; Milestone Approved & Escrow Released</span>`;
          
          // Also post notification into the chat
          if (messageStream) {
            const notif = document.createElement("div");
            notif.style.textAlign = "center";
            notif.style.margin = "var(--space-xs) 0";
            notif.innerHTML = `<span style="background: #e8f5e9; color: #2e7d32; font-size: 0.78rem; font-weight: 700; padding: 0.3rem 0.8rem; border-radius: var(--radius-pill);">&#10004; Client approved Milestone ${milestoneId} & released funds</span>`;
            messageStream.appendChild(notif);
            messageStream.scrollTop = messageStream.scrollHeight;
          }
        }
      } catch (err) {
        console.error("Error approving milestone:", err);
      }
    });
  });

  // 7. Example Repository Chip Selection (for OpenSource Buddy)
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
});

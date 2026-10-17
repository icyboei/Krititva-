/**
 * Krititva Application JavaScript
 * Fully functional logic for Exchange, Bilateral Workspace, and OpenSource Buddy
 */

document.addEventListener("DOMContentLoaded", () => {
  // ==========================================
  // 1. GLOBAL MODAL HELPER FUNCTIONS
  // ==========================================
  function openModal(modal) {
    if (modal) modal.style.display = "flex";
  }

  function closeModal(modal) {
    if (modal) modal.style.display = "none";
  }

  document.querySelectorAll(".btn-close-modal").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".modal-backdrop").forEach((m) => closeModal(m));
    });
  });

  window.addEventListener("click", (e) => {
    if (e.target.classList.contains("modal-backdrop")) {
      closeModal(e.target);
    }
  });

  // Mobile Menu Toggle
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

  // ==========================================
  // 2. EXCHANGE: POST BRIEF, LIST SERVICE, & ENGAGE
  // ==========================================
  const btnOpenBriefModal = document.getElementById("btn-open-brief-modal");
  const btnOpenBriefEmpty = document.getElementById("btn-open-brief-modal-empty");
  const btnOpenServiceModal = document.getElementById("btn-open-service-modal");
  const modalBrief = document.getElementById("modal-project-brief");
  const modalService = document.getElementById("modal-list-service");
  const modalEngage = document.getElementById("modal-engage-provider");

  if (btnOpenBriefModal) {
    btnOpenBriefModal.addEventListener("click", () => openModal(modalBrief));
  }
  if (btnOpenBriefEmpty) {
    btnOpenBriefEmpty.addEventListener("click", () => openModal(modalBrief));
  }
  if (btnOpenServiceModal) {
    btnOpenServiceModal.addEventListener("click", () => openModal(modalService));
  }

  // Post Brief Form Submission
  const formPostBrief = document.getElementById("form-post-brief");
  if (formPostBrief) {
    formPostBrief.addEventListener("submit", async (e) => {
      e.preventDefault();
      const payload = {
        title: document.getElementById("brief-title").value.trim(),
        client_name: document.getElementById("brief-client-name").value.trim(),
        category: document.getElementById("brief-category").value,
        scope: document.getElementById("brief-scope").value.trim(),
        budget: document.getElementById("brief-budget").value.trim(),
        timeline: document.getElementById("brief-timeline").value.trim()
      };

      try {
        const resp = await fetch("/api/briefs", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        if (resp.ok) {
          closeModal(modalBrief);
          window.location.href = "/exchange?tab=briefs";
        }
      } catch (err) {
        alert("Failed to submit project brief: " + err.message);
      }
    });
  }

  // List Capability Form Submission
  const formListService = document.getElementById("form-list-service");
  if (formListService) {
    formListService.addEventListener("submit", async (e) => {
      e.preventDefault();
      const payload = {
        title: document.getElementById("service-title").value.trim(),
        provider_name: document.getElementById("provider-name").value.trim(),
        provider_title: document.getElementById("provider-title").value.trim(),
        category: document.getElementById("service-category").value,
        skills: document.getElementById("service-skills").value.trim(),
        description: document.getElementById("service-desc").value.trim(),
        indicative_pricing: document.getElementById("service-price").value.trim(),
        typical_duration: document.getElementById("service-duration").value.trim()
      };

      try {
        const resp = await fetch("/api/services", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        if (resp.ok) {
          closeModal(modalService);
          window.location.href = "/exchange?tab=services";
        }
      } catch (err) {
        alert("Failed to publish capability listing: " + err.message);
      }
    });
  }

  // Engage & Open Brief Modal Trigger on Service Cards
  document.querySelectorAll(".btn-trigger-engage").forEach((btn) => {
    btn.addEventListener("click", () => {
      const srvId = btn.getAttribute("data-service-id");
      const srvTitle = btn.getAttribute("data-service-title");
      const providerName = btn.getAttribute("data-provider-name");
      const pricing = btn.getAttribute("data-pricing");

      document.getElementById("engage-service-id").value = srvId;
      document.getElementById("engage-provider-name").textContent = providerName;
      document.getElementById("engage-service-title").textContent = srvTitle;
      document.getElementById("engage-project-title").value = srvTitle;
      document.getElementById("engage-budget").value = pricing;

      openModal(modalEngage);
    });
  });

  // Engage Form Submit (Creates a real bilateral engagement workspace)
  const formEngage = document.getElementById("form-engage-provider");
  if (formEngage) {
    formEngage.addEventListener("submit", async (e) => {
      e.preventDefault();
      const payload = {
        service_id: document.getElementById("engage-service-id").value,
        client_name: document.getElementById("engage-client-name").value.trim(),
        title: document.getElementById("engage-project-title").value.trim(),
        budget: document.getElementById("engage-budget").value.trim(),
        scope: document.getElementById("engage-scope").value.trim()
      };

      try {
        const resp = await fetch("/api/engagements/create", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        if (resp.ok) {
          const res = await resp.json();
          window.location.href = `/workspace?id=${res.engagement_id}`;
        }
      } catch (err) {
        alert("Failed to create engagement: " + err.message);
      }
    });
  }

  // ==========================================
  // 3. COLLABORATION WORKSPACE (MESSAGES & MILESTONES)
  // ==========================================
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
    const currentEngId = chatForm.getAttribute("data-eng-id") || "eng-8042";

    chatForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const content = chatInput.value.trim();
      if (!content) return;

      try {
        const resp = await fetch("/api/workspace/message", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ engagement_id: currentEngId, role: activeRole, content })
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

  // Client Milestone Approval
  document.querySelectorAll(".btn-approve-milestone").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const milestoneId = btn.getAttribute("data-id");
      const engId = btn.getAttribute("data-eng-id") || "eng-8042";

      if (!confirm(`Are you sure you want to approve Milestone ${milestoneId} and release milestone funds from verified escrow?`)) {
        return;
      }

      try {
        const resp = await fetch(`/api/workspace/milestone/${milestoneId}/approve?engagement_id=${engId}`, {
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
          
          if (messageStream) {
            const notif = document.createElement("div");
            notif.style.textAlign = "center";
            notif.style.margin = "var(--space-xs) 0";
            notif.innerHTML = `<span style="background: #e8f5e9; color: #2e7d32; font-size: 0.78rem; font-weight: 700; padding: 0.3rem 0.8rem; border-radius: var(--radius-pill);">&#10004; Client approved Milestone ${milestoneId} & released escrow funds</span>`;
            messageStream.appendChild(notif);
            messageStream.scrollTop = messageStream.scrollHeight;
          }
        }
      } catch (err) {
        console.error("Error approving milestone:", err);
      }
    });
  });

  // Provider Submit Deliverable Modal Trigger
  const modalDeliverable = document.getElementById("modal-submit-deliverable");
  const formSubmitDeliverable = document.getElementById("form-submit-deliverable");

  document.querySelectorAll(".btn-submit-deliverable-modal").forEach((btn) => {
    btn.addEventListener("click", () => {
      const mId = btn.getAttribute("data-id");
      const mTitle = btn.getAttribute("data-title");

      document.getElementById("submit-milestone-id").value = mId;
      document.getElementById("submit-milestone-title").textContent = `Milestone ${mId}: ${mTitle}`;
      openModal(modalDeliverable);
    });
  });

  if (formSubmitDeliverable) {
    formSubmitDeliverable.addEventListener("submit", async (e) => {
      e.preventDefault();
      const mId = document.getElementById("submit-milestone-id").value;
      const engId = document.getElementById("submit-eng-id").value;
      const deliverableUrl = document.getElementById("deliverable-url").value.trim();
      const notes = document.getElementById("deliverable-notes").value.trim();

      try {
        const resp = await fetch(`/api/workspace/milestone/${mId}/submit`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ engagement_id: engId, deliverable: deliverableUrl, notes })
        });
        if (resp.ok) {
          closeModal(modalDeliverable);
          window.location.reload();
        }
      } catch (err) {
        alert("Failed to submit deliverable: " + err.message);
      }
    });
  }

  // ==========================================
  // 4. OPENSOURCE BUDDY: GITHUB ANALYSIS & AI ROADMAP
  // ==========================================
  const repoForm = document.getElementById("repo-analysis-form");
  const repoInput = document.getElementById("repo-url-input");
  const repoLoading = document.getElementById("repo-loading");
  const repoErrorBox = document.getElementById("repo-error-box");
  const repoErrorMessage = document.getElementById("repo-error-message");
  const repoResults = document.getElementById("repo-results-container");
  const issuesListContainer = document.getElementById("issues-list-container");
  const modalRoadmap = document.getElementById("modal-ai-roadmap");

  let currentRepoData = null;
  let currentIssues = [];

  // Example chips auto-fill and submit
  document.querySelectorAll(".example-repo-chip").forEach((chip) => {
    chip.addEventListener("click", () => {
      if (repoInput) {
        repoInput.value = chip.getAttribute("data-repo");
        if (repoForm) repoForm.dispatchEvent(new Event("submit"));
      }
    });
  });

  if (repoForm && repoInput) {
    repoForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const repoUrl = repoInput.value.trim();
      if (!repoUrl) return;

      repoLoading.style.display = "block";
      repoErrorBox.style.display = "none";
      repoResults.style.display = "none";

      try {
        const resp = await fetch("/api/analyze-repo", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ repo_url: repoUrl })
        });

        const data = await resp.json();
        repoLoading.style.display = "none";

        if (!resp.ok) {
          repoErrorMessage.textContent = data.error || "Failed to analyze repository.";
          repoErrorBox.style.display = "block";
          return;
        }

        currentRepoData = data.repository;
        currentIssues = data.issues || [];

        // Fill overview
        document.getElementById("repo-full-name").textContent = currentRepoData.full_name;
        document.getElementById("repo-description").textContent = currentRepoData.description;
        document.getElementById("repo-lang-badge").textContent = currentRepoData.language;
        document.getElementById("repo-license-badge").textContent = currentRepoData.license;
        document.getElementById("repo-stars-count").textContent = currentRepoData.stars.toLocaleString();
        document.getElementById("repo-forks-count").textContent = currentRepoData.forks.toLocaleString();
        document.getElementById("repo-open-issues-count").textContent = currentRepoData.open_issues_count.toLocaleString();
        document.getElementById("repo-github-link").href = currentRepoData.html_url;

        // Fill README preview
        document.getElementById("repo-readme-content").textContent = data.readme;

        // Render issues
        renderIssues(currentIssues);
        repoResults.style.display = "flex";
      } catch (err) {
        repoLoading.style.display = "none";
        repoErrorMessage.textContent = "Network or server connection error: " + err.message;
        repoErrorBox.style.display = "block";
      }
    });
  }

  function renderIssues(issues) {
    if (!issuesListContainer) return;
    issuesListContainer.innerHTML = "";

    if (issues.length === 0) {
      issuesListContainer.innerHTML = `
        <div style="background: var(--color-white); border: 1.5px dashed var(--color-soft-border); border-radius: var(--radius-md); padding: var(--space-xl); text-align: center; color: var(--color-muted-text);">
          No open issues found matching the selected label criteria.
        </div>
      `;
      return;
    }

    issues.forEach((issue) => {
      const card = document.createElement("article");
      card.className = "handcrafted-card";
      card.style.minHeight = "auto";
      card.style.background = "var(--color-white)";
      card.style.padding = "var(--space-lg)";

      const labelsHtml = issue.labels.map(l => 
        `<span style="background: #${l.color || 'e0e0e0'}; color: #000000; padding: 0.15rem 0.5rem; border-radius: var(--radius-pill); font-size: 0.72rem; font-weight: 600;">${l.name}</span>`
      ).join(" ");

      card.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: var(--space-sm); flex-wrap: wrap;">
          <div>
            <div style="display: flex; align-items: center; gap: 0.4rem; margin-bottom: 0.25rem;">
              <span style="font-size: 0.8rem; font-weight: 700; color: var(--color-terracotta);">#${issue.number}</span>
              <span style="font-size: 0.78rem; color: var(--color-muted-text);">Opened ${issue.created_at} &bull; ${issue.comments_count} comments</span>
            </div>
            <h3 style="font-family: var(--font-editorial); font-size: 1.45rem; color: var(--color-deep-espresso); margin-bottom: 0.4rem;">
              ${issue.title}
            </h3>
          </div>
          <div>
            <a href="${issue.html_url}" target="_blank" rel="noopener noreferrer" style="font-size: 0.82rem; color: var(--color-burnished-copper); font-weight: 600;">
              View on GitHub ↗
            </a>
          </div>
        </div>

        <div style="display: flex; flex-wrap: wrap; gap: 0.3rem; margin: 0.3rem 0 var(--space-sm);">
          ${labelsHtml}
        </div>

        <p style="font-size: 0.9rem; color: var(--color-muted-text); line-height: 1.5; margin-bottom: var(--space-md);">
          ${issue.body_preview}
        </p>

        <div style="display: flex; justify-content: flex-end;">
          <button type="button" class="btn-hand-drawn btn-generate-roadmap" style="font-size: 0.85rem; padding: 0.5rem 1.1rem;">
            ✨ Explain Issue &amp; Plan Roadmap &rarr;
          </button>
        </div>
      `;

      // Roadmap button click
      const btnRoadmap = card.querySelector(".btn-generate-roadmap");
      btnRoadmap.addEventListener("click", async () => {
        openModal(modalRoadmap);
        document.getElementById("roadmap-modal-title").textContent = `#${issue.number} ${issue.title}`;
        const contentBox = document.getElementById("roadmap-content-body");
        contentBox.textContent = "Analyzing issue with Gemma mentorship engine...";

        try {
          const resp = await fetch("/api/explain-issue", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ issue, repository: currentRepoData })
          });
          if (resp.ok) {
            const res = await resp.json();
            contentBox.textContent = res.roadmap.explanation_markdown;
            document.getElementById("roadmap-disclaimer").textContent = res.roadmap.disclaimer;
          } else {
            contentBox.textContent = "Failed to generate roadmap at this time.";
          }
        } catch (err) {
          contentBox.textContent = "Error: " + err.message;
        }
      });

      issuesListContainer.appendChild(card);
    });
  }

  // Issue label filter buttons
  document.querySelectorAll(".issue-filter-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".issue-filter-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      const filter = btn.getAttribute("data-filter");

      if (filter === "all") {
        renderIssues(currentIssues);
      } else if (filter === "first") {
        renderIssues(currentIssues.filter(i => i.is_good_first_issue));
      } else if (filter === "help") {
        renderIssues(currentIssues.filter(i => i.is_help_wanted));
      }
    });
  });

  // Copy Roadmap to Clipboard
  const btnCopyRoadmap = document.getElementById("btn-copy-roadmap");
  if (btnCopyRoadmap) {
    btnCopyRoadmap.addEventListener("click", () => {
      const text = document.getElementById("roadmap-content-body").textContent;
      navigator.clipboard.writeText(text).then(() => {
        alert("Contribution roadmap copied to clipboard!");
      });
    });
  }
});

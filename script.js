document.addEventListener("DOMContentLoaded", () => {
    // Theme Toggle
    const themeSwitcher = document.getElementById("theme-switcher");
    if (themeSwitcher) {
        themeSwitcher.addEventListener("change", (e) => {
            document.body.classList.toggle("dark-mode", e.target.checked);
            localStorage.setItem("darkMode", e.target.checked);
        });

        // Apply saved theme preference
        if (localStorage.getItem("darkMode") === "true") {
            document.body.classList.add("dark-mode");
            themeSwitcher.checked = true;
        }
    }

    // Smooth Scroll for CTA Buttons
    const ctaButtons = document.querySelectorAll(".cta-button");
    ctaButtons.forEach(btn => {
        btn.addEventListener("click", (e) => {
            const href = btn.getAttribute("href");
            if (href && href.startsWith("#")) {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({ behavior: "smooth" });
                }
            }
        });
    });

    // File Upload Hover Effect
    const fileUploader = document.querySelector(".file-uploader");
    if (fileUploader) {
        fileUploader.addEventListener("dragover", (e) => {
            e.preventDefault();
            fileUploader.classList.add("drag-active");
        });

        fileUploader.addEventListener("dragleave", (e) => {
            e.preventDefault();
            fileUploader.classList.remove("drag-active");
        });

        fileUploader.addEventListener("drop", (e) => {
            e.preventDefault();
            fileUploader.classList.remove("drag-active");
        });
    }

    // Card Animation on Scroll
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("animate");
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.2 });

    // Observe cards with retry for dynamic Streamlit content
    const observeCards = () => {
        document.querySelectorAll(".feature-card, .stat-card, .result-card").forEach(card => {
            if (!card.classList.contains("animate")) {
                observer.observe(card);
            }
        });
    };
    observeCards();

    // Re-observe on Streamlit DOM updates
    const mutationObserver = new MutationObserver(() => {
        observeCards();
        initializeTooltips();
    });
    mutationObserver.observe(document.body, { childList: true, subtree: true });

    // Initialize Tooltips
    const initializeTooltips = () => {
        document.querySelectorAll("[data-tooltip]").forEach(elem => {
            // Remove existing event listeners to prevent duplicates
            const clonedElem = elem.cloneNode(true);
            elem.parentNode.replaceChild(clonedElem, elem);

            clonedElem.addEventListener("mouseenter", () => {
                const tooltip = document.createElement("span");
                tooltip.className = "tooltip";
                tooltip.textContent = clonedElem.dataset.tooltip;
                clonedElem.appendChild(tooltip);
                setTimeout(() => tooltip.classList.add("active"), 100);
            });

            clonedElem.addEventListener("mouseleave", () => {
                const tooltip = clonedElem.querySelector(".tooltip");
                if (tooltip) {
                    tooltip.classList.remove("active");
                    setTimeout(() => tooltip.remove(), 200);
                }
            });
        });
    };
    initializeTooltips();

    // Console Greeting
    console.log("%c🩺 PneumoAI System Initialized", "color: #6b46c1; font-size: 16px; font-weight: bold");
    console.log("%cAdvanced Pneumonia Detection v2.1", "color: #38b2ac");
});

// CSS for tooltips and animations
const style = document.createElement("style");
style.textContent = `
    .tooltip {
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        background: #2d3748;
        color: #f7fafc;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-size: 0.9rem;
        white-space: nowrap;
        z-index: 10;
        margin-bottom: 0.5rem;
        opacity: 0;
        transition: opacity 0.2s ease;
    }
    .tooltip.active {
        opacity: 1;
    }
    .file-uploader.drag-active {
        background: rgba(107, 70, 193, 0.1);
        transform: scale(1.02);
        box-shadow: 0 10px 25px -5px rgba(107, 70, 193, 0.3);
    }
    .animate {
        animation: slideIn 0.5s ease forwards;
    }
`;
document.head.appendChild(style);
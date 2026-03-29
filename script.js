const header = document.querySelector(".site-header");
const menuToggle = document.querySelector(".menu-toggle");
const navLinks = document.querySelectorAll(".site-nav a");
const topButton = document.querySelector(".go-to-top");
const sections = document.querySelectorAll("main section[id]");
const currentPath = window.location.pathname.split("/").pop() || "index.html";
const revealItems = document.querySelectorAll(".hero, .section, .page-intro, .site-footer");
const themeToggle = document.querySelector(".theme-toggle");
const savedTheme = window.localStorage.getItem("site-theme");
const newsItems = document.querySelectorAll("[data-news-page]");
const newsPageButtons = document.querySelectorAll("[data-news-target]");

const applyTheme = (theme) => {
  document.body.classList.toggle("theme-dark", theme === "dark");
  if (themeToggle) {
    themeToggle.setAttribute("aria-label", `Switch to ${theme === "dark" ? "light" : "dark"} theme`);
    themeToggle.setAttribute("title", `Switch to ${theme === "dark" ? "light" : "dark"} theme`);
  }
};

applyTheme(savedTheme === "dark" ? "dark" : "light");

window.addEventListener("load", () => {
  document.body.classList.add("is-loaded");
});

if (themeToggle) {
  themeToggle.addEventListener("click", () => {
    const nextTheme = document.body.classList.contains("theme-dark") ? "light" : "dark";
    applyTheme(nextTheme);
    window.localStorage.setItem("site-theme", nextTheme);
  });
}

if (menuToggle) {
  menuToggle.addEventListener("click", () => {
    const isOpen = header.classList.toggle("is-open");
    menuToggle.setAttribute("aria-expanded", String(isOpen));
  });
}

navLinks.forEach((link) => {
  link.addEventListener("click", () => {
    header.classList.remove("is-open");
    if (menuToggle) {
      menuToggle.setAttribute("aria-expanded", "false");
    }
  });
});

const updateActiveLink = () => {
  const pageLinks = Array.from(navLinks).filter((link) => !link.getAttribute("href").startsWith("#"));
  pageLinks.forEach((link) => {
    const href = link.getAttribute("href");
    const normalizedHref = href.split("#")[0];
    link.classList.toggle("is-active", normalizedHref === currentPath);
  });

  if (!sections.length) {
    return;
  }

  let currentId = "";

  sections.forEach((section) => {
    const sectionTop = section.offsetTop - 140;
    if (window.scrollY >= sectionTop) {
      currentId = section.id;
    }
  });

  navLinks.forEach((link) => {
    const href = link.getAttribute("href");
    if (href.startsWith("#")) {
      const isActive = href === `#${currentId}`;
      link.classList.toggle("is-active", isActive);
    }
  });
};

const updateTopButton = () => {
  topButton.classList.toggle("is-visible", window.scrollY > 320);
};

revealItems.forEach((item) => {
  item.classList.add("reveal");
});

const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        revealObserver.unobserve(entry.target);
      }
    });
  },
  {
    threshold: 0.12,
    rootMargin: "0px 0px -40px 0px",
  }
);

revealItems.forEach((item) => {
  revealObserver.observe(item);
});

window.addEventListener("scroll", () => {
  updateActiveLink();
  updateTopButton();
});

if (topButton) {
  topButton.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
}

const setNewsPage = (page) => {
  if (!newsItems.length || !newsPageButtons.length) {
    return;
  }

  newsItems.forEach((item) => {
    item.hidden = item.dataset.newsPage !== page;
  });

  newsPageButtons.forEach((button) => {
    const isActive = button.dataset.newsTarget === page;
    button.classList.toggle("is-active", isActive);
    button.setAttribute("aria-pressed", String(isActive));
  });
};

if (newsItems.length && newsPageButtons.length) {
  setNewsPage("1");

  newsPageButtons.forEach((button) => {
    ["mouseenter", "focus", "click"].forEach((eventName) => {
      button.addEventListener(eventName, () => {
        setNewsPage(button.dataset.newsTarget);
      });
    });
  });
}

updateActiveLink();
updateTopButton();

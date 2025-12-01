document.addEventListener("DOMContentLoaded", () => {
  // =================================================
  // 1) UPLOAD + PREVIEW + (PLACEHOLDER) BACKEND LOGIC
  // =================================================

  const uploadForm = document.getElementById("upload-form");
  const imageInput = document.getElementById("image-input");
  const previewBox = document.getElementById("preview");
  const previewImg = document.getElementById("preview-img");
  const errorMsg = document.getElementById("error");
  const resultBox = document.getElementById("result");
  const landmarkName = document.getElementById("landmark-name");
  const landmarkDesc = document.getElementById("landmark-desc");
  const videoContainer = document.getElementById("video-container");

  // Show preview when image selected
  if (imageInput && previewBox && previewImg) {
    imageInput.addEventListener("change", () => {
      const file = imageInput.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = (e) => {
        previewImg.src = e.target.result;
        previewBox.classList.remove("hidden");
      };
      reader.readAsDataURL(file);
    });
  }

  // Handle upload submit
  if (uploadForm) {
    uploadForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      if (!imageInput || !errorMsg || !resultBox || !landmarkName || !landmarkDesc || !videoContainer) {
        return;
      }

      const file = imageInput.files[0];
      if (!file) {
        errorMsg.textContent = "Please select an image first.";
        errorMsg.classList.remove("hidden");
        return;
      }

      errorMsg.classList.add("hidden");

      const formData = new FormData();
      formData.append("image", file);

      // When backend is ready, replace null with real URL:
      // const BACKEND_URL = "https://your-backend-url.com/api/predict";
      const BACKEND_URL = null;

      try {
        let data;

        if (BACKEND_URL) {
          const res = await fetch(BACKEND_URL, {
            method: "POST",
            body: formData,
          });

          if (!res.ok) {
            throw new Error("Backend error");
          }

          data = await res.json();
        } else {
          // Placeholder data for demo (no backend yet)
          data = {
            name: "Sample landmark (demo)",
            description:
              "This is a placeholder result. Once the backend is connected, you will see the real landmark name and description here.",
            videoUrl: null, // e.g. "assets/demo-video.mp4"
          };
        }

        // Fill UI
        landmarkName.textContent = data.name || "";
        landmarkDesc.textContent = data.description || "";

        if (data.videoUrl) {
          videoContainer.innerHTML = `
            <video controls class="w-full h-full rounded-xl">
              <source src="${data.videoUrl}" type="video/mp4" />
              Your browser does not support the video tag.
            </video>
          `;
        } else {
          videoContainer.innerHTML =
            "The video will appear here once the backend is connected and returns a video URL.";
        }

        resultBox.classList.remove("hidden");
      } catch (err) {
        console.error(err);
        errorMsg.textContent = "Failed to connect to the server.";
        errorMsg.classList.remove("hidden");
      }
    });
  }

  // ==========================
  // 2) IMAGE SLIDER (ABOUT)
  // ==========================

  const slides = document.querySelectorAll(".about-slide");
  const prevBtn = document.getElementById("about-prev");
  const nextBtn = document.getElementById("about-next");

  if (slides.length > 0) {
    let currentIndex = 0;
    let autoplayId = null;

    // Initial styles for smooth fade
    slides.forEach((slide, i) => {
      slide.style.transition = "opacity 0.6s ease";
      slide.style.opacity = i === 0 ? "1" : "0";
    });

    function showSlide(index) {
      slides.forEach((slide, i) => {
        slide.style.opacity = i === index ? "1" : "0";
      });
      currentIndex = index;
    }

    function nextSlide() {
      const nextIndex = (currentIndex + 1) % slides.length;
      showSlide(nextIndex);
    }

    function prevSlideFun() {
      const prevIndex = (currentIndex - 1 + slides.length) % slides.length;
      showSlide(prevIndex);
    }

    function startAutoplay() {
      stopAutoplay();
      autoplayId = setInterval(nextSlide, 3500);
    }

    function stopAutoplay() {
      if (autoplayId) clearInterval(autoplayId);
    }

    // Start
    showSlide(0);
    startAutoplay();

    if (nextBtn) {
      nextBtn.addEventListener("click", () => {
        nextSlide();
        startAutoplay();
      });
    }

    if (prevBtn) {
      prevBtn.addEventListener("click", () => {
        prevSlideFun();
        startAutoplay();
      });
    }
  }

  // ==========================
  // 3) TEAM DROPDOWN (SLIDE)
  // ==========================

  const teamToggle = document.getElementById("team-toggle");
  const teamContent = document.getElementById("team-content");
  const teamArrow = document.getElementById("team-arrow");

  if (teamToggle && teamContent && teamArrow) {
    // Start closed
    teamContent.style.maxHeight = "0px";

    teamToggle.addEventListener("click", () => {
      const isOpen =
        teamContent.style.maxHeight && teamContent.style.maxHeight !== "0px";

      if (isOpen) {
        // Close
        teamContent.style.maxHeight = "0px";
        teamArrow.style.transform = "rotate(0deg)";
      } else {
        // Open
        teamContent.style.maxHeight = teamContent.scrollHeight + "px";
        teamArrow.style.transform = "rotate(90deg)";
      }
    });
  }
});

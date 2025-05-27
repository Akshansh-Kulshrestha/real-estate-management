/*-----------------------------------------------------------------------------------
 Template Name: Admiro
 Template URI: themes.pixelstrap.com/Admiro
 Description: This is Admin Template
 Author: Pixelstrap
 Author URI: https://themeforest.net/user/pixelstrap
 ----------------------------------------------------------------------------------- */
// 01. Loader js
// 02. Tap to top js
// 03. Header DropDown Toggle js
// 04. Full screen js
// 05. Header search js
document.addEventListener("DOMContentLoaded", function () {
  const body = document.querySelector("body");
  const html = document.querySelector("html");
    /*=====================
        01 Loader Js
    ==========================*/
    $(".loader-wrapper").fadeOut("slow", function () {
      $(this).remove();
    });
  /*=====================
        02 Tap to top js
    ==========================*/
  const button = document.querySelector(".tap-top");
  const displayButton = () => {
    window.addEventListener("scroll", () => {
      if (window.scrollY > 100) {
        button.style.display = "block";
      } else {
        button.style.display = "none";
      }
    });
  };
  const scrollToTop = () => {
    button.addEventListener("click", () => {
      window.scroll({
        top: 0,
        left: 0,
        behavior: "smooth",
      });
      console.log(event);
    });
  };
  displayButton();
  scrollToTop();
  /*=====================
      03 Header DropDown Toggle
  ==========================*/
  body.addEventListener("click", function (event) {
    const headerDropdownMenu = document.querySelectorAll(".custom-menu");
    const dropdownEl = event.target.closest(".custom-dropdown");
    const visible = dropdownEl
      ?.querySelector(".custom-menu")
      .classList.contains("show");
    const dropdownMenuElement = event.target.closest(".custom-menu");
    if (!dropdownMenuElement) {
      headerDropdownMenu.forEach((item) => {
        item.classList.remove("show");
      });
    }
    if (!dropdownEl) return;
    const dropdownMenu = dropdownEl.querySelector(".custom-menu");
    if (!visible) dropdownMenu.classList.add("show");
  });
  /*=====================
      04 Full screen js
  ==========================*/
  $(document).ready(function () {
    $(".full-screen").click(function (event) {
      var elem = document.documentElement;
  
      if (
        (document.fullScreenElement && document.fullScreenElement !== null) ||
        (!document.mozFullScreen && !document.webkitIsFullScreen)
      ) {
        if (elem.requestFullScreen) {
          elem.requestFullScreen();
        } else if (elem.mozRequestFullScreen) {
          elem.mozRequestFullScreen();
        } else if (elem.webkitRequestFullScreen) {
          elem.webkitRequestFullScreen(Element.ALLOW_KEYBOARD_INPUT);
        }
      } else {
        if (document.cancelFullScreen) {
          document.cancelFullScreen();
        } else if (document.mozCancelFullScreen) {
          document.mozCancelFullScreen();
        } else if (document.webkitCancelFullScreen) {
          document.webkitCancelFullScreen();
        }
      }
    });
  });
  
  /*=====================
       05. Header search js
     ==========================*/
  const filterSidebarToggle = document.querySelector(".md-sidebar-toggle");
  const filterSidebarAside = document.querySelector(".md-sidebar-aside");
  filterSidebarToggle?.addEventListener("click", function () {
    filterSidebarAside.classList.toggle("open");
  });
  $(".search").click(function () {
    $(".search-full").addClass("open");
  });
  $(".close-search").click(function () {
    $(".search-full").removeClass("open");
    $("body").removeClass("offcanvas");
  });
  /*=====================
       05. Dark Mode js
    ==========================*/
    if(window.location.pathname.includes("layout-dark.html")){
      $("body").removeClass("light");
      $("body").addClass("dark-only");
      }else{
      $(".dark-mode").on("click", function () {
      const bodyModeDark = $("body").hasClass("dark-only");
      if(!window.location.pathname.includes("layout-dark.html")){
      if (!bodyModeDark) {
      $(".dark-mode").addClass("active");
      localStorage.setItem("mode", "dark-only");
      $("body").addClass("dark-only");
      $("body").removeClass("light");
      }
      else{
      $(".dark-mode").removeClass("active");
      localStorage.setItem("mode", "light");
      $("body").removeClass("dark-only");
      $("body").addClass("light");
      }
      }
      });
      $("body").addClass(
      localStorage.getItem("mode")
      ? localStorage.getItem("mode")
      : "light"
      );
      $(".dark-mode").addClass(
      localStorage.getItem("mode") === "dark-only" ? "active" : " "
      )}
  // product-page-js-start
  var toggleDataElements = document.querySelectorAll(".toggle-data");
  toggleDataElements.forEach(function (element) {
    element.addEventListener("click", function () {
      var productWrapperElements =
        document.querySelectorAll(".product-wrapper");
      productWrapperElements.forEach(function (wrapperElement) {
        wrapperElement.classList.toggle("sidebaron");
      });
    });
  });
  // product-page-js-end
  $(".prooduct-details-box .close").on("click", function (e) {
    var tets = $(this).parent().parent().parent().parent().addClass("d-none");
    console.log(tets);
  });
  /*=====================
    00. Background Image js
    ==========================*/
  $(".bg-center").parent().addClass("b-center");
  $(".bg-img-cover").parent().addClass("bg-size");
  $(".bg-img-cover").each(function () {
    var el = $(this),
      src = el.attr("src"),
      parent = el.parent();
    parent.css({
      "background-image": "url(" + src + ")",
      "background-size": "cover",
      "background-position": "center",
      display: "block",
    });
    el.hide();
  });
  /*=====================
    00. Language js
    ==========================*/
  var tnum = "en";

  $(document).ready(function () {
    if (localStorage.getItem("primary") != null) {
      var primary_val = localStorage.getItem("primary");
      $("#ColorPicker1").val(primary_val);
      var secondary_val = localStorage.getItem("secondary");
      $("#ColorPicker2").val(secondary_val);
    }

    $(document).click(function (e) {
      $(".translate_wrapper, .more_lang").removeClass("active");
    });
    $(".translate_wrapper .current_lang").click(function (e) {
      e.stopPropagation();
      $(this).parent().toggleClass("active");

      setTimeout(function () {
        $(".more_lang").toggleClass("active");
      }, 5);
    });

    /*TRANSLATE*/
    translate(tnum);

    $(".more_lang .lang").click(function () {
      $(this).addClass("selected").siblings().removeClass("selected");
      $(".more_lang").removeClass("active");

      var i = $(this).find("i").attr("class");
      var lang = $(this).attr("data-value");
      var tnum = lang;
      translate(tnum);

      $(".current_lang .lang-txt").text(lang);
      $(".current_lang i").attr("class", i);
    });
  });

  function translate(tnum) {
    $(".lan-1").text(trans[0][tnum]);
    $(".lan-2").text(trans[1][tnum]);
    $(".lan-3").text(trans[2][tnum]);
  }

  var trans = [
    {
      en: "General",
      es: "Paneloj",
      fr: "GÃ©nÃ©rale",
    },
    {
      en: "Widgets",
      es: "Vidin",
      fr: "widgets",
    },
    {
      en: "Page layout",
      es: "Paneloj",
      fr: "Tableaux",
    },
  ];
});

 document.getElementById('property_images').addEventListener('change', function(event) {
    const preview = document.getElementById('imagePreview');
    preview.innerHTML = ''; // Clear existing previews

    Array.from(event.target.files).forEach(file => {
      const reader = new FileReader();
      reader.onload = function(e) {
        const img = document.createElement('img');
        img.src = e.target.result;
        img.classList.add('img-thumbnail');
        img.style.height = '100px';
        img.style.marginRight = '10px';
        preview.appendChild(img);
      };
      reader.readAsDataURL(file);
    });
  });

    const sliderWrapper = document.getElementById('sliderWrapper');
  const slides = document.querySelectorAll('.slide');
  const totalSlides = slides.length;
  let currentIndex = 0;

  document.querySelector('.slider-btn.next').addEventListener('click', () => {
    if (currentIndex < totalSlides - 1) {
      currentIndex++;
      sliderWrapper.style.transform = `translateX(-${220 * currentIndex}px)`;
    }
  });

  document.querySelector('.slider-btn.prev').addEventListener('click', () => {
    if (currentIndex > 0) {
      currentIndex--;
      sliderWrapper.style.transform = `translateX(-${220 * currentIndex}px)`;
    }
  });

  document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('propertyForm');
    const goBackBtn = document.getElementById('goBackBtn');

    // Save initial form state
    const initialFormData = new FormData(form);
    const getFormSnapshot = (formData) => {
      let snapshot = '';
      for (const [key, value] of formData.entries()) {
        snapshot += `${key}:${value}|`;
      }
      return snapshot;
    };
    const initialSnapshot = getFormSnapshot(initialFormData);

    goBackBtn.addEventListener('click', function (e) {
      const currentSnapshot = getFormSnapshot(new FormData(form));
      if (currentSnapshot !== initialSnapshot) {
        const confirmLeave = confirm("You have unsaved changes. Do you still want to leave?");
        if (!confirmLeave) {
          e.preventDefault();  // Stop the navigation
        }
      }
      // else allow normal navigation
    });
  });


document.getElementById('imageUploadInput').addEventListener('change', function(event) {
    const previewContainer = document.getElementById('preview-container');
    previewContainer.innerHTML = '';  // Clear old previews

    Array.from(event.target.files).forEach(file => {
        const reader = new FileReader();
        reader.onload = e => {
            const img = document.createElement('img');
            img.src = e.target.result;
            img.style.width = '100px';
            img.style.height = 'auto';
            img.style.border = '1px solid #ccc';
            img.style.borderRadius = '4px';
            previewContainer.appendChild(img);
        };
        reader.readAsDataURL(file);
    });
});
/* ============================================================
    [Master Scripts]

    Theme Name:     Imagiax 
    Theme URL:      
    Description:    Imagiax Ai Image Generate html template
    Author:         PhotoClerks           
    Version:        1.0.0

============================================================== */
/*
========================================
*********** TABLE OF CONTENTS **********
 
  1. Navbar Shrink JS
  2. Navbar Links Active JS
  3. Banner Two Trigger JS
  4. Card Grid JS
  5. Progress JS
  6. Odometer Counter Up JS
  7. Scroll Back to Top JS
  8. Testimonials Slider JS
  9. Testimonials Slider Two JS
  10. Blog Slider JS
  11. We Do Slide JS
  12. Company Slide JS
  13. Text Slide JS
  14. Follow Slide JS
  15. Scroll Reveal JS
  16. Video Popup JS
  17. Gallery Popup JS
  18. Portfolio Grid JS
  19. Background Image JS
  20. Preloader JS
 
========================================*/

'use strict';
(function ($) {
  gsap.registerPlugin(ScrollTrigger);

  /* ========================================
   Navbar shrink Js
  ======================================== */
  $(window).on('scroll', function () {
    var wScroll = $(this).scrollTop();
    if (wScroll > 1) {
      $('.navbar-main').addClass('navbar-shrink');
    } else {
      $('.navbar-main').removeClass('navbar-shrink');
    };
  });

  /* ========================================
     Navbar Links Active  Js
  ======================================== */
  if ($('.navbar-nav').length > 0) {
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link, .dropdown-menu .dropdown-item');

    const removeActiveClass = () => {
      navLinks.forEach((link) => link.classList.remove('active'));
    };

    const setActiveLink = () => {
      const currentPath = window.location.pathname;
      removeActiveClass();

      navLinks.forEach((link) => {
        const linkPath = link.getAttribute('href');
        if (linkPath && currentPath.endsWith(linkPath)) {
          link.classList.add('active');

          const parentDropdown = link.closest('.dropdown-menu')?.previousElementSibling;
          if (parentDropdown) {
            parentDropdown.classList.add('active');
          }
        }
      });
    };
    setActiveLink();
  }

  /* ========================================
   Banner two trigger Js
  ======================================== */
  if ($('.banner-two-section').length > 0) {
    const bannerTimeline = gsap.timeline({
      scrollTrigger: {
        trigger: ".banner-two-section",
        start: "98% 90%",
        end: "100% 50%",
        scrub: true,
      }
    })

    bannerTimeline.to(".banner-img-one", {
      top: "95%",
      left: "31%",
      scale: 0.5,
      rotate: 0,
    }, 'imgs')

    bannerTimeline.to(".banner-img-two", {
      top: "95%",
      right: "31%",
      scale: 0.5,
      rotate: 0,
    }, 'imgs')
  }

  /* ========================================
      Card grid Js
  ======================================== */
  if ($('#container').length > 0) {
    $('#container').imagesLoaded(function () {
      const $grid = $('.card-grid');
      if ($grid.length > 0) {
        $grid.isotope({
          itemSelector: '.card-grid-item',
          percentPosition: true,
          masonry: {
            columnWidth: '.card-grid-item',
          }
        });
      }

      const $portfolioNav = $('.portfolio-nav');
      if ($portfolioNav.length > 0) {
        const indicator = $('<div class="nav-indicator"></div>');
        $portfolioNav.append(indicator);

        function updateIndicator(el) {
          if (indicator.length > 0 && el) {
            indicator.css({
              width: `${el.offsetWidth}px`,
              left: `${el.offsetLeft}px`,
              transition: 'all 0.6s ease'
            });
          }
        }

        $('.portfolio-nav').on('mouseenter', 'button', function () {
          $('.portfolio-nav button').removeClass('active');
          $(this).addClass('active');
          const filterValue = $(this).attr('data-filter');
          $grid.isotope({ filter: filterValue });
          updateIndicator(this);
        });

        const activeLink = $portfolioNav.find('button.active');
        if (activeLink.length > 0) updateIndicator(activeLink[0]);
      }
    });
  }


  /* ========================================
    Progress Js
  ======================================== */
  if ($('.skill-progress').length > 0) {
    function animateNumbers(element) {
      const target = +element.getAttribute('data-target');
      const duration = 1500; // 1.5 second
      const step = target / (duration / 20);

      let current = 0;
      const interval = setInterval(() => {
        current += step;
        if (current >= target) {
          current = target;
          clearInterval(interval);
        }
        element.textContent = Math.round(current) + "%";
      }, 20);
    }
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const progressBar = entry.target.querySelector('.progress-bar');
            const percentageText = entry.target.querySelector('.percentage');

            const targetWidth = percentageText.getAttribute('data-target') + '%';
            progressBar.style.width = targetWidth;
            progressBar.setAttribute('aria-valuenow', targetWidth);

            animateNumbers(percentageText);
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.5 }
    );
    document.querySelectorAll('.skill-progress').forEach((item) => observer.observe(item));
  }

  /* ========================================
    Odometer Counter Up Js
  ======================================== */
  // data-odometer-final
  if ($('.odometer').length > 0) {
    $(window).on('scroll', function () {
      $('.odometer').each(function () {
        if ($(this).isInViewport()) {
          if (!$(this).data('odometer-started')) {
            $(this).data('odometer-started', true);
            this.innerHTML = $(this).data('odometer-final');
          }
        }
      });
    });
  }
  // isInViewport helper function
  $.fn.isInViewport = function () {
    let elementTop = $(this).offset().top;
    let elementBottom = elementTop + $(this).outerHeight();
    let viewportTop = $(window).scrollTop();
    let viewportBottom = viewportTop + $(window).height();
    return elementBottom > viewportTop && elementTop < viewportBottom;
  };

  /* ========================================
     Scroll back to top  Js
   ======================================== */
  if ($('.progress-wrap').length > 0) {
    const progressPath = document.querySelector('.progress-wrap path');
    const pathLength = progressPath.getTotalLength();

    // Set up the initial stroke styles
    progressPath.style.transition = 'none';
    progressPath.style.strokeDasharray = `${pathLength} ${pathLength}`;
    progressPath.style.strokeDashoffset = pathLength;
    progressPath.getBoundingClientRect();

    // Set transition for stroke-dashoffset
    progressPath.style.transition = 'stroke-dashoffset 10ms linear';

    const updateProgress = () => {
      const scroll = $(window).scrollTop();
      const height = $(document).height() - $(window).height();
      const progress = pathLength - (scroll * pathLength / height);
      progressPath.style.strokeDashoffset = progress;
    };

    updateProgress();
    $(window).on('scroll', updateProgress);

    const offset = 50;
    const duration = 550;

    $(window).on('scroll', () => {
      $('.progress-wrap').toggleClass('active-progress', $(window).scrollTop() > offset);
    });

    $('.progress-wrap').on('click', (event) => {
      event.preventDefault();
      $('html, body').animate({ scrollTop: 0 }, duration);
    });
  }

  /* ========================================
    Testimonials slider Js
  ======================================== */
  if ($('.testimonials-slider').length > 0) {
    const testimonialsSwiper = new Swiper('.testimonials-slider', {
      slidesPerView: 2,
      spaceBetween: 24,
      speed: 700,
      autoplay: {
        delay: 4500,
        disableOnInteraction: false,
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      breakpoints: {
        0: { slidesPerView: 1 },
        768: { slidesPerView: 1 },
        1024: { slidesPerView: 2 },
      },
    });
  }

  /* ========================================
    Testimonials slider two Js
  ======================================== */
  if ($('.testimonials-slider-two').length > 0) {
    const testimonialsTwoSwiper = new Swiper('.testimonials-slider-two', {
      loop: true,
      slidesPerView: 3,
      spaceBetween: 24,
      speed: 800,
      autoplay: {
        delay: 4500,
        disableOnInteraction: false,
      },
      pagination: false,
      navigation: {
        nextEl: ".swiper--next",
        prevEl: ".swiper--prev",
      },
      breakpoints: {
        0: { slidesPerView: 1 },
        768: { slidesPerView: 2 },
        1024: { slidesPerView: 2 },
        1200: { slidesPerView: 3 },
      },
    });
  }

  /* ========================================
    blog slider Js
  ======================================== */
  if ($('.blog-slider').length > 0) {
    const blogSwiper = new Swiper('.blog-slider', {
      slidesPerView: 3,
      spaceBetween: 24,
      speed: 700,
      autoplay: {
        delay: 4000,
        disableOnInteraction: false,
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      breakpoints: {
        0: { slidesPerView: 1 },
        768: { slidesPerView: 2 },
        1024: { slidesPerView: 2 },
        1200: { slidesPerView: 3 },
      },
    });
  }

  /* ========================================
    we do slide Js
  ======================================== */
  if ($('.we-do-slide').length > 0) {
    const blogSwiper = new Swiper('.we-do-slide', {
      slidesPerView: 3,
      spaceBetween: 24,
      speed: 700,
      autoplay: {
        delay: 4000,
        disableOnInteraction: false,
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      breakpoints: {
        0: { slidesPerView: 1 },
        768: { slidesPerView: 2 },
        1024: { slidesPerView: 3 },
      },
    });
  }

  /* ========================================
    Company slide Js
  ======================================== */
  if ($('.company-slide').length > 0) {
    const partnersSwiper = new Swiper('.company-slide', {
      loop: true,
      slidesPerView: 'auto',
      centeredSlides: true,
      allowTouchMove: false,
      spaceBetween: 24,
      speed: 4000,
      autoplay: {
        delay: 0,
        disableOnInteraction: false,
      },
    });
  }

  /* ========================================
    Text slide Js
  ======================================== */
  if ($('.text-slide').length > 0) {
    const textSwiper = new Swiper('.text-slide', {
      loop: true,
      slidesPerView: 'auto',
      centeredSlides: true,
      allowTouchMove: false,
      spaceBetween: 0,
      speed: 6500,
      autoplay: {
        delay: 0,
        disableOnInteraction: false,
      },
    });
  }

  /* ========================================
    Follow slide Js
  ======================================== */
  if ($('.follow-slide').length > 0) {
    const followSwiper = new Swiper('.follow-slide', {
      loop: true,
      slidesPerView: 'auto',
      centeredSlides: true,
      allowTouchMove: false,
      spaceBetween: 0,
      speed: 6500,
      autoplay: {
        delay: 0,
        disableOnInteraction: false,
      },
    });
  }

  /* ========================================
    Best Selling Js
  ======================================== */
  if ($('.best-selling-slide').length > 0) {
    const bestSellingSwiper = new Swiper('.best-selling-slide', {
      loop: true,
      slidesPerView: 3,
      spaceBetween: 24,
      speed: 800,
      autoplay: {
        delay: 4500,
        disableOnInteraction: false,
      },
      pagination: false,
      navigation: {
        nextEl: ".swiper--next",
        prevEl: ".swiper--prev",
      },
      breakpoints: {
        0: { slidesPerView: 1 },
        768: { slidesPerView: 2 },
        1024: { slidesPerView: 3 },
        1200: { slidesPerView: 4 },
      },
    });
  }

  /* ========================================
    Scroll Reveal Js
  ======================================== */
  const scrollReveal = ScrollReveal({
    origin: 'top', distance: '60px', duration: 1300, delay: 100, mobile: false,
  })
  scrollReveal.reveal('.top-reveal, .category-content__item', {
    delay: 60, distance: '60px', origin: 'top', interval: 100
  })
  scrollReveal.reveal('.left-reveal, .services-item ', {
    delay: 60, origin: 'left', interval: 100
  })
  scrollReveal.reveal('.right-reveal ', {
    delay: 60, origin: 'right', interval: 100
  })
  scrollReveal.reveal('.bottom-reveal', {
    delay: 60, origin: 'bottom', interval: 100
  })
  scrollReveal.reveal('.scaleUp ', {
    scale: 0.85
  })

  /* ========================================
     Video Popup Js
  ======================================== */
  $('.popup-youtube').magnificPopup({
    disableOn: 700,
    type: 'iframe',
    mainClass: 'mfp-fade',
    removalDelay: 160,
    preloader: false,
    fixedContentPos: false
  });

  /* ========================================
    Gallery Popup Js
  ======================================== */
  $('.card-grid, .view-modal').magnificPopup({
    delegate: 'a',
    type: 'image',
    tLoading: 'Loading image #%curr%...',
    mainClass: 'mfp-img-mobile',
    gallery: {
      enabled: true,
      navigateByImgClick: true,
      preload: [0, 1]
    },
    image: {
      tError: '<a href="%url%">The image #%curr%</a> could not be loaded.',
      titleSrc: function (item) {
        return item.el.attr('title');
      }
    }
  });

  /* ========================================
      Portfolio grid Js
  ======================================== */
  if ($('#container').length > 0) {
    $('#container').imagesLoaded(function () {
      const $grid = $('.card-grid, .card-grid_content');
      if ($grid.length > 0) {
        $grid.isotope({
          itemSelector: '.card-grid-item',
          percentPosition: true,
          masonry: {
            columnWidth: '.card-grid-item',
          }
        });
      }

      const $portfolioNav = $('.portfolio-nav');
      if ($portfolioNav.length > 0) {
        const indicator = $('<div class="nav-indicator"></div>');
        $portfolioNav.append(indicator);

        function updateIndicator(el) {
          if (indicator.length > 0 && el) {
            indicator.css({
              width: `${el.offsetWidth}px`,
              left: `${el.offsetLeft}px`,
              transition: 'all 0.6s ease'
            });
          }
        }

        $('.portfolio-nav').on('mouseenter', 'button', function () {
          $('.portfolio-nav button').removeClass('active');
          $(this).addClass('active');
          const filterValue = $(this).attr('data-filter');
          $grid.isotope({ filter: filterValue });
          updateIndicator(this);
        });

        const activeLink = $portfolioNav.find('button.active');
        if (activeLink.length > 0) updateIndicator(activeLink[0]);
      }
    });
  }

  /* ========================================
      Background image Js
  ======================================== */
  $('.bg-img').css('background-image', function () {
    var bg = 'url(' + $(this).data('background-image') + ')';
    return bg;
  });


  /* ========================================
      Preloader Js
  ======================================== */
  window.addEventListener('load', () => {
    const preloader = document.getElementById('preloader');
    preloader.style.transition = 'height 0.5s, opacity 1s';
    preloader.style.opacity = '0';
    preloader.style.height = '0';
    preloader.style.borderBottomLeftRadius = '100%';
    preloader.style.borderBottomRightRadius = '100%';
    setTimeout(() => {
      preloader.style.display = 'none';
    }, 500);
  });

  /* ========================================
      Preloader Js
  ======================================== */
  if ($('.product-image').length > 0) {
    const detailsMain = new Swiper(".details-main", {
      loop: true,
      spaceBetween: 10,
      slidesPerView: 4,
      freeMode: true,
      watchSlidesProgress: true,
    });  
    const detailsList = new Swiper(".details-list", {
      loop: true,
      spaceBetween: 10,
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      thumbs: {
        swiper: detailsMain,
      },
    });
  }
 

  /* ========================================
    filter btn Js
  ======================================== */
  if ($('.filter-content').length > 0) {
    const filterContent = document.querySelector('.filter-content');
    const filterBtn = document.querySelector('.filter-btn');

    if (!filterContent || !filterBtn) return;

    const mainContent = document.querySelector('.main-content');
    const contentBoxes = document.querySelectorAll('.content-box');

    filterBtn.addEventListener('click', function () {
      const isFilterHidden = filterContent.classList.contains('d-none');

      // Toggle filter visibility using Bootstrap classes
      filterContent.classList.toggle('d-none', !isFilterHidden);

      // Update main content grid classes
      const mainCols = isFilterHidden ? ['col-xl-9', 'col-lg-8'] : ['col-xl-12', 'col-lg-12'];
      mainContent.classList.remove(...mainContent.classList);
      mainContent.classList.add(...mainCols);

      // Update content box columns
      const boxCols = isFilterHidden ? ['col-xl-4', 'col-lg-4'] : ['col-xl-3', 'col-lg-3'];
      contentBoxes.forEach(box => {
        box.classList.remove('col-xl-4', 'col-lg-4', 'col-xl-3', 'col-lg-3');
        box.classList.add(...boxCols);
      });
    });
  }

  /* ========================================
      Range pricing Js
  ======================================== */
  if (document.querySelector('.range_container')) {
    function initRangeSlider() {
      const fromSlider = document.querySelector('.fromSlider');
      const toSlider = document.querySelector('.toSlider');
      const fromInput = document.querySelector('.fromInput');
      const toInput = document.querySelector('.toInput');
      const min = parseInt(fromSlider.min, 10);
      const max = parseInt(toSlider.max, 10);

      function updateSliderFill() {
        const fromVal = parseInt(fromSlider.value, 10);
        const toVal = parseInt(toSlider.value, 10);
        const fromPos = ((fromVal - min) / (max - min)) * 100;
        const toPos = ((toVal - min) / (max - min)) * 100;

        toSlider.style.background = `linear-gradient(
          to right, #141b13 0%, #141b13 ${fromPos}%, #ffffff ${fromPos}%, #ffffff ${toPos}%, #141b13 ${toPos}%, #141b13 100%)`;
      }

      function syncValues() {
        let fromVal = parseInt(fromSlider.value, 10);
        let toVal = parseInt(toSlider.value, 10);

        if (fromVal > toVal) {
          fromVal = toVal;
          fromSlider.value = fromVal;
        }
        if (toVal < fromVal) {
          toVal = fromVal;
          toSlider.value = toVal;
        }

        fromInput.textContent = fromVal;
        toInput.textContent = toVal;
        updateSliderFill();
      }

      function addListeners() {
        const sync = () => syncValues();
        fromSlider.addEventListener('input', sync);
        toSlider.addEventListener('input', sync);
      }

      syncValues();
      addListeners();
    }

    initRangeSlider();
  }


  /* ========================================
      Quantity Controls Js
  ======================================== */
  if ($('.cart-table-item').length > 0) {
    function calculateTotals() {
      let subtotal = 0;

      document.querySelectorAll(".cart-table-item").forEach((item) => {
        let quantityElement = item.querySelector(".quantity-number");
        let itemPrice = parseFloat(item.querySelector(".item-price").textContent);
        let totalPriceElement = item.querySelector(".total-price");

        let quantity = parseInt(quantityElement.textContent, 10);
        let totalPrice = itemPrice * quantity;
        totalPriceElement.textContent = totalPrice.toFixed(2);

        subtotal += totalPrice;
      });

      document.querySelector(".cart-summary p:nth-child(1) span").textContent = `$${subtotal.toFixed(2)}`;

      let tax = subtotal * 0.10;
      document.querySelector(".cart-summary p:nth-child(3) span").textContent = `$${tax.toFixed(2)}`;

      let finalTotal = subtotal + tax;
      document.querySelector(".cart-summary p:nth-child(5) span").textContent = `$${finalTotal.toFixed(2)}`;
    }

    document.querySelectorAll(".cart-table-item").forEach((item) => {
      let incrementBtn = item.querySelector(".quantity-increment");
      let decrementBtn = item.querySelector(".quantity-decrement");
      let quantityElement = item.querySelector(".quantity-number");
      let removeBtn = item.querySelector(".remove-item");

      incrementBtn.addEventListener("click", () => {
        quantityElement.textContent = parseInt(quantityElement.textContent, 10) + 1;
        calculateTotals();
      });

      decrementBtn.addEventListener("click", () => {
        if (parseInt(quantityElement.textContent, 10) > 1) {
          quantityElement.textContent = parseInt(quantityElement.textContent, 10) - 1;
          calculateTotals();
        }
      });

      removeBtn.addEventListener("click", () => {
        item.remove();
        calculateTotals();
      });
    });

    calculateTotals();
  }
 

})(jQuery);

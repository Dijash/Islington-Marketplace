document.addEventListener('DOMContentLoaded', function () {

  /* ── Theme Toggle ────────────────────────────────── */
  var toggle = document.getElementById('themeToggle');
  var html = document.documentElement;

  function setTheme(dark) {
    if (dark) {
      html.classList.add('dark-mode');
    } else {
      html.classList.remove('dark-mode');
    }
    localStorage.setItem('theme', dark ? 'dark' : 'light');
  }

  if (localStorage.getItem('theme') === 'dark') {
    setTheme(true);
  }

  if (toggle) {
    toggle.addEventListener('click', function () {
      setTheme(!html.classList.contains('dark-mode'));
    });
  }

  /* ── Hero Carousel ───────────────────────────────── */
  var carousel = document.querySelector('.hero-carousel');
  if (carousel) {
    var slides = carousel.querySelectorAll('.carousel-slide');
    var dots   = carousel.querySelectorAll('.carousel-dot');
    var prevBtn = carousel.querySelector('.carousel-btn-prev');
    var nextBtn = carousel.querySelector('.carousel-btn-next');
    var current = 0;
    var total   = slides.length;
    var autoplayInterval = null;
    var autoplayDelay = 4000;
    var isPaused = false;

    function goToSlide(index) {
      slides[current].classList.remove('active');
      dots[current].classList.remove('active');
      current = (index + total) % total;
      slides[current].classList.add('active');
      dots[current].classList.add('active');
    }

    function nextSlide() { goToSlide(current + 1); }
    function prevSlide() { goToSlide(current - 1); }

    prevBtn.addEventListener('click', function () {
      prevSlide();
      resetAutoplay();
    });

    nextBtn.addEventListener('click', function () {
      nextSlide();
      resetAutoplay();
    });

    dots.forEach(function (dot) {
      dot.addEventListener('click', function () {
        goToSlide(parseInt(this.dataset.index));
        resetAutoplay();
      });
    });

    /* Autoplay */
    function startAutoplay() {
      stopAutoplay();
      autoplayInterval = setInterval(function () {
        if (!isPaused) nextSlide();
      }, autoplayDelay);
    }

    function stopAutoplay() {
      if (autoplayInterval) {
        clearInterval(autoplayInterval);
        autoplayInterval = null;
      }
    }

    function resetAutoplay() {
      stopAutoplay();
      startAutoplay();
    }

    carousel.addEventListener('mouseenter', function () { isPaused = true; });
    carousel.addEventListener('mouseleave', function () { isPaused = false; });

    startAutoplay();

    /* Touch / Swipe support */
    var touchStartX = 0;
    var touchEndX = 0;
    var swipeThreshold = 50;

    carousel.addEventListener('touchstart', function (e) {
      touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    carousel.addEventListener('touchend', function (e) {
      touchEndX = e.changedTouches[0].screenX;
      var diff = touchStartX - touchEndX;
      if (Math.abs(diff) > swipeThreshold) {
        if (diff > 0) {
          nextSlide();
        } else {
          prevSlide();
        }
        resetAutoplay();
      }
    }, { passive: true });

    /* Keyboard support */
    carousel.setAttribute('tabindex', '0');
    carousel.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft')  { prevSlide(); resetAutoplay(); }
      if (e.key === 'ArrowRight') { nextSlide(); resetAutoplay(); }
    });
  }

  /* ── Ad Carousel (hero left div) ───────────────── */
  var adCarousel = document.querySelector('.ad-carousel');
  if (adCarousel) {
    var adSlides = adCarousel.querySelectorAll('.ad-slide');
    var adDots   = adCarousel.querySelectorAll('.ad-dot');
    var adPrev   = adCarousel.querySelector('.ad-btn-prev');
    var adNext   = adCarousel.querySelector('.ad-btn-next');
    var adCurrent = 0;
    var adTotal   = adSlides.length;
    var adInterval = null;
    var adDelay = 3500;
    var adPaused = false;

    function goToAd(index) {
      adSlides[adCurrent].classList.remove('active');
      adDots[adCurrent].classList.remove('active');
      adCurrent = (index + adTotal) % adTotal;
      adSlides[adCurrent].classList.add('active');
      adDots[adCurrent].classList.add('active');
    }

    function nextAd() { goToAd(adCurrent + 1); }
    function prevAd() { goToAd(adCurrent - 1); }

    adPrev.addEventListener('click', function () {
      prevAd();
      resetAdAutoplay();
    });

    adNext.addEventListener('click', function () {
      nextAd();
      resetAdAutoplay();
    });

    adDots.forEach(function (dot) {
      dot.addEventListener('click', function () {
        goToAd(parseInt(this.dataset.index));
        resetAdAutoplay();
      });
    });

    function startAdAutoplay() {
      stopAdAutoplay();
      adInterval = setInterval(function () {
        if (!adPaused) nextAd();
      }, adDelay);
    }

    function stopAdAutoplay() {
      if (adInterval) {
        clearInterval(adInterval);
        adInterval = null;
      }
    }

    function resetAdAutoplay() {
      stopAdAutoplay();
      startAdAutoplay();
    }

    adCarousel.addEventListener('mouseenter', function () { adPaused = true; });
    adCarousel.addEventListener('mouseleave', function () { adPaused = false; });

    startAdAutoplay();

    /* Touch / Swipe */
    var adTouchStart = 0;
    var adTouchEnd = 0;

    adCarousel.addEventListener('touchstart', function (e) {
      adTouchStart = e.changedTouches[0].screenX;
    }, { passive: true });

    adCarousel.addEventListener('touchend', function (e) {
      adTouchEnd = e.changedTouches[0].screenX;
      var diff = adTouchStart - adTouchEnd;
      if (Math.abs(diff) > 50) {
        if (diff > 0) nextAd(); else prevAd();
        resetAdAutoplay();
      }
    }, { passive: true });
  }

  /* ── Side Ad Carousel (hero right div, auto only) ── */
  var sideCarousel = document.querySelector('.side-ad-carousel');
  if (sideCarousel) {
    var sideSlides = sideCarousel.querySelectorAll('.side-ad-slide');
    var sideCurrent = 0;
    var sideTotal = sideSlides.length;
    var sideInterval = null;
    var sideDelay = 3000;

    function goToSide(index) {
      sideSlides[sideCurrent].classList.remove('active');
      sideCurrent = (index + sideTotal) % sideTotal;
      sideSlides[sideCurrent].classList.add('active');
    }

    function startSideAutoplay() {
      sideInterval = setInterval(function () {
        goToSide(sideCurrent + 1);
      }, sideDelay);
    }

    startSideAutoplay();
  }

  /* ── Category Slider Navigation ────────────────── */
  var catSlider = document.querySelector('.category-slider');
  var catPrev = document.querySelector('.category-prev');
  var catNext = document.querySelector('.category-next');
  if (catSlider && catPrev && catNext) {
    var scrollAmount = 300;

    catPrev.addEventListener('click', function () {
      catSlider.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    });

    catNext.addEventListener('click', function () {
      catSlider.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    });
  }

  /* ── Mobile Menu ────────────────────────────────── */
  var hamburger = document.getElementById('navHamburger');
  var mobileMenu = document.getElementById('navMobileMenu');
  var mobileClose = document.getElementById('navMobileClose');
  var mobileThemeToggle = document.getElementById('themeToggleMobile');

  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', function () {
      mobileMenu.classList.add('open');
      document.body.style.overflow = 'hidden';
    });
    function closeMobileMenu() {
      mobileMenu.classList.remove('open');
      document.body.style.overflow = '';
    }
    if (mobileClose) {
      mobileClose.addEventListener('click', closeMobileMenu);
    }
    mobileMenu.addEventListener('click', function (e) {
      if (e.target === mobileMenu) closeMobileMenu();
    });
    mobileMenu.querySelectorAll('.nav-mobile-link').forEach(function (link) {
      link.addEventListener('click', closeMobileMenu);
    });
    if (mobileThemeToggle) {
      mobileThemeToggle.addEventListener('click', function () {
        var isDark = html.classList.contains('dark-mode');
        if (isDark) {
          html.classList.remove('dark-mode');
        } else {
          html.classList.add('dark-mode');
        }
        localStorage.setItem('theme', isDark ? 'light' : 'dark');
      });
    }
  }

  /* ── Banner Ad Carousel ───────────────────────── */
  var bannerCarousel = document.querySelector('[data-banner-carousel]');
  if (bannerCarousel) {
    var bannerSlides = bannerCarousel.querySelectorAll('.ad-banner-slide');
    var bannerCurrent = 0;
    var bannerTotal   = bannerSlides.length;
    var bannerInterval = null;
    var bannerDelay = 4000;
    var bannerPaused = false;

    function goToBanner(index) {
      bannerSlides[bannerCurrent].classList.remove('active');
      bannerCurrent = (index + bannerTotal) % bannerTotal;
      bannerSlides[bannerCurrent].classList.add('active');
    }

    function nextBanner() { goToBanner(bannerCurrent + 1); }

    function startBannerAutoplay() {
      stopBannerAutoplay();
      if (bannerTotal < 2) return;
      bannerInterval = setInterval(function () {
        if (!bannerPaused) nextBanner();
      }, bannerDelay);
    }

    function stopBannerAutoplay() {
      if (bannerInterval) {
        clearInterval(bannerInterval);
        bannerInterval = null;
      }
    }

    bannerCarousel.addEventListener('mouseenter', function () { bannerPaused = true; });
    bannerCarousel.addEventListener('mouseleave', function () { bannerPaused = false; });

    startBannerAutoplay();

    /* Touch / Swipe */
    var bannerTouchStart = 0;
    var bannerTouchEnd = 0;

    bannerCarousel.addEventListener('touchstart', function (e) {
      bannerTouchStart = e.changedTouches[0].screenX;
    }, { passive: true });

    bannerCarousel.addEventListener('touchend', function (e) {
      bannerTouchEnd = e.changedTouches[0].screenX;
      var diff = bannerTouchStart - bannerTouchEnd;
      if (Math.abs(diff) > 50) {
        if (diff > 0) nextBanner();
        stopBannerAutoplay();
        startBannerAutoplay();
      }
    }, { passive: true });
  }

  /* ── Product Carousel Navigation ────────────────── */
  document.querySelectorAll('.home-products-section').forEach(function (section) {
    var grid = section.querySelector('[data-product-carousel]');
    var prev = section.querySelector('.home-products-prev, .newest-prev, .budget-prev');
    var next = section.querySelector('.home-products-next, .newest-next, .budget-next');
    if (!grid || !prev || !next) return;

    function getCardWidth() {
      var card = grid.querySelector('.product-card');
      if (!card) return 280;
      var gap = parseFloat(window.getComputedStyle(grid).gap) || 20;
      return card.offsetWidth + gap;
    }

    function updateButtons() {
      var maxScroll = grid.scrollWidth - grid.clientWidth;
      prev.disabled = grid.scrollLeft <= 1;
      next.disabled = grid.scrollLeft >= maxScroll - 1;
    }

    prev.addEventListener('click', function () {
      grid.scrollBy({ left: -getCardWidth(), behavior: 'smooth' });
    });

    next.addEventListener('click', function () {
      grid.scrollBy({ left: getCardWidth(), behavior: 'smooth' });
    });

    grid.addEventListener('scroll', updateButtons);
    window.addEventListener('resize', updateButtons);
    updateButtons();

    /* Touch / Swipe support */
    var touchStart = 0;
    var touchEnd = 0;

    grid.addEventListener('touchstart', function (e) {
      touchStart = e.changedTouches[0].screenX;
    }, { passive: true });

    grid.addEventListener('touchend', function (e) {
      touchEnd = e.changedTouches[0].screenX;
      var diff = touchStart - touchEnd;
      if (Math.abs(diff) > 50) {
        if (diff > 0) {
          grid.scrollBy({ left: getCardWidth(), behavior: 'smooth' });
        } else {
          grid.scrollBy({ left: -getCardWidth(), behavior: 'smooth' });
        }
      }
    }, { passive: true });
  });
});

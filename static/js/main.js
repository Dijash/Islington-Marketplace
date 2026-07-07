document.addEventListener('DOMContentLoaded', function () {
  var toggle = document.getElementById('themeToggle');
  if (toggle) {
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

    toggle.addEventListener('click', function () {
      setTheme(!html.classList.contains('dark-mode'));
    });
  }

  var track = document.getElementById('heroTrack');
  if (!track) return;

  var slides = track.querySelectorAll('.hero-slide');
  var prevBtn = document.getElementById('heroArrowPrev');
  var nextBtn = document.getElementById('heroArrowNext');
  var dotsContainer = document.getElementById('heroDots');
  var current = 0;
  var interval;

  function buildDots() {
    slides.forEach(function (_, i) {
      var dot = document.createElement('button');
      dot.className = 'hero-dot' + (i === 0 ? ' active' : '');
      dot.setAttribute('aria-label', 'Go to slide ' + (i + 1));
      dot.addEventListener('click', function () {
        goTo(i);
      });
      dotsContainer.appendChild(dot);
    });
  }

  function goTo(index) {
    slides.forEach(function (s) { s.classList.remove('active'); });
    dotsContainer.querySelectorAll('.hero-dot').forEach(function (d) { d.classList.remove('active'); });
    current = (index + slides.length) % slides.length;
    slides[current].classList.add('active');
    dotsContainer.children[current].classList.add('active');
    resetInterval();
  }

  function next() { goTo(current + 1); }
  function prev() { goTo(current - 1); }

  function resetInterval() {
    clearInterval(interval);
    interval = setInterval(next, 5000);
  }

  buildDots();
  resetInterval();

  if (prevBtn) prevBtn.addEventListener('click', prev);
  if (nextBtn) nextBtn.addEventListener('click', next);

  document.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') prev();
    if (e.key === 'ArrowRight') next();
  });


});

/*
 * Sets the payment-rails carousel's scroll duration from the *actual* rendered
 * track width so the linear speed (~50px/s) stays consistent regardless of
 * viewport size or how many rails get added later.
 */
(function () {
  var track = document.getElementById('railsTrustStripTrack');
  if (!track) return;

  var SPEED_PX_PER_SEC = 52; // within the requested 40-60px/s band

  function setDuration() {
    var halfWidth = track.scrollWidth / 2;
    if (halfWidth > 0) {
      var seconds = halfWidth / SPEED_PX_PER_SEC;
      track.style.setProperty('--rails-duration', seconds.toFixed(2) + 's');
    }
  }

  setDuration();

  var resizeTimer;
  window.addEventListener('resize', function () {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(setDuration, 150);
  });
})();

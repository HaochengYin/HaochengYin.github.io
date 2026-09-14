// More content

var moreContent = document.getElementById("more-content");
moreContent.addEventListener("shown.bs.collapse", function() {
  this.scrollIntoView();
});

// Profile

var counter = 0;
var hoverImages = [
  "assets/profile/horseshoe_bend.webp",
  "assets/profile/bryce_canyon.webp"
];

var profile_credit = document.getElementById("profile-credit");
var profile = document.getElementById("profile");

function profile_enter() {
  profile.src = hoverImages[counter];
  counter = (counter + 1) % hoverImages.length;
}

function profile_leave() {
  profile.src = "assets/profile/profile_img.webp";
}

// Touch taps fire mouseenter but never mouseleave, leaving the photo stuck
var canHover = window.matchMedia &&
               window.matchMedia("(hover: hover) and (pointer: fine)").matches;

if (canHover) {
  profile_credit.addEventListener("mouseenter", profile_enter);
  profile_credit.addEventListener("mouseleave", profile_leave);
}

profile_leave();

// Footer year

var d = new Date();
document.getElementById('year').innerHTML = d.getFullYear();

// Clipboard

var snippets = document.querySelectorAll('.snippet');

snippets.forEach(function(snippet) {
  snippet.insertAdjacentHTML(
    'afterbegin',
    '<button class="btn" data-bs-toggle="tooltip" data-bs-title="Copy to clipboard" data-clipboard-snippet><i class="bi bi-clipboard"></i></button>'
  );
});

const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

var clipboardSnippets = new ClipboardJS('[data-clipboard-snippet]', {
  target: function(trigger) {
    return trigger.nextElementSibling;
  }
});

clipboardSnippets.on('success', function(e) {
  e.clearSelection();
  var icon = e.trigger.querySelector('i');
  icon.className = 'bi bi-check2';
  var tooltip = bootstrap.Tooltip.getInstance(e.trigger);
  tooltip.setContent({'.tooltip-inner': 'Copied!'});
  tooltip.show();
  setTimeout(function() {
    icon.className = 'bi bi-clipboard';
    tooltip.setContent({'.tooltip-inner': 'Copy to clipboard'});
    tooltip.hide();
  }, 2000);
});


// Demo videos: load on demand, then hold on the last frame before looping

var delayedLoopVideos = document.querySelectorAll('video[data-loop-delay]');

function playDemo(video) {
  // play() rejects when the browser blocks playback (backgrounded tab, power-save)
  var played = video.play();
  if (played) {
    played.catch(function() {});
  }
}

delayedLoopVideos.forEach(function(video) {
  var delay = parseInt(video.dataset.loopDelay, 10) || 1000;
  video.addEventListener('ended', function() {
    setTimeout(function() {
      video.currentTime = 0;
      playDemo(video);
    }, delay);
  });
});

// Only fetch a demo once it is close to the viewport, so the page does not pull
// every clip at load. Browsers without IntersectionObserver just play immediately.
if ('IntersectionObserver' in window) {
  var demoObserver = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (!entry.isIntersecting) {
        return;
      }
      var video = entry.target;
      demoObserver.unobserve(video);
      video.preload = 'auto';
      video.load();
      playDemo(video);
    });
  }, { rootMargin: '200px' });

  delayedLoopVideos.forEach(function(video) {
    demoObserver.observe(video);
  });
} else {
  delayedLoopVideos.forEach(function(video) {
    video.preload = 'auto';
    video.load();
    playDemo(video);
  });
}


// External links

document.addEventListener("DOMContentLoaded", function() {
  // Select all anchor tags with an href attribute
  const links = document.querySelectorAll('a[href]');

  // Iterate through each link
  links.forEach(function(link) {
    // Check if the href attribute does not start with '#'
    if (!link.getAttribute('href').startsWith('#')) {
        // Set the target and rel attributes
        link.setAttribute('target', '_blank');
        link.setAttribute('rel', 'noopener noreferrer');
    }
  });
});
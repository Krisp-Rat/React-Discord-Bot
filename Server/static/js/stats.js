document.addEventListener('DOMContentLoaded', function () {
  const tabs = document.querySelectorAll('.tab');
  const tabContents = document.querySelectorAll('.tab-content');

  tabs.forEach((tab) => {
    tab.addEventListener('click', function () {
      // Remove active class from all tabs and hide all content panels
      tabs.forEach((t) => t.classList.remove('active'));
      tabContents.forEach((content) => content.classList.remove('active'));

      // Activate the clicked tab and its corresponding content
      this.classList.add('active');
      const tabId = this.getAttribute('data-tab');
      document.getElementById(tabId).classList.add('active');
    });
  });
});

document.querySelectorAll('.filter-usr').forEach(function(element) {
    element.addEventListener('click', function() {
      const selectedUser = element.getAttribute('data-usr');
      const reactions = document.querySelectorAll('.reaction');

      reactions.forEach(function(reaction) {
        if (reaction.getAttribute('data-usr') === selectedUser) {
          reaction.style.display = 'block'; // Show reactions for the selected user
        } else {
          reaction.style.display = 'none'; // Hide other reactions
        }
      });

      // Optional: Add a reset button to remove the filter
      const resetButton = document.getElementById('reset-filter');
      if (resetButton) resetButton.style.display = 'inline';
    });
  });

  // Function to reset the filter and show all reactions again
  function resetFilter() {
    document.querySelectorAll('.reaction').forEach(function(reaction) {
      reaction.style.display = 'block';
    });
    document.getElementById('reset-filter').style.display = 'none';
  }
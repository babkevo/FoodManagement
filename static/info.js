// Get the plus icon and information elements
const plusIcon = document.getElementById('plus-icon');
const information = document.getElementById('information');

// Add a click event listener to the plus icon
plusIcon.addEventListener('click', function() {
  // Toggle the visibility of the information section
  if (information.style.display === 'none') {
    information.style.display = 'block';
  } else {
    information.style.display = 'none';
  }
});

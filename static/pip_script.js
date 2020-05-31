const video = document.getElementById('video_player');
  const togglePipButton = document.getElementById('togglePipButton');

  // Hide button if Picture-in-Picture is not supported or disabled.
  togglePipButton.hidden = !document.pictureInPictureEnabled ||
    video.disablePictureInPicture;

  togglePipButton.addEventListener('click', function() {
    // If there is no element in Picture-in-Picture yet, let’s request
    // Picture-in-Picture for the video, otherwise leave it.
    if (!document.pictureInPictureElement) {
      video.requestPictureInPicture()
      .catch(error => {
        // Video failed to enter Picture-in-Picture mode.
      });
    } else {
      document.exitPictureInPicture()
      .catch(error => {
        // Video failed to leave Picture-in-Picture mode.
      });
    }
  });

document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('webcam');
    const videoContainer = document.getElementById('video-container');
    const videoIcon = document.getElementById('video-icon');
    const captureButton = document.getElementById('capture-button');

    videoIcon.addEventListener('click', () => {
        videoContainer.classList.remove('d-none');
        startWebcam();
    });

    captureButton.addEventListener('click', () => {
        // Add your capture logic here
        alert('Capture button clicked!');
    });

    function startWebcam() {
        if (navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({ video: true })
                .then((stream) => {
                    video.srcObject = stream;
                })
                .catch((error) => {
                    console.error("Error accessing webcam: ", error);
                });
        }
    }
});

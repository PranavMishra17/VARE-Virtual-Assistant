document.addEventListener('DOMContentLoaded', function () {
    // Initialize Speech SDK Configuration with your subscription details
    const speechConfig = SpeechSDK.SpeechConfig.fromSubscription("c897d534a33b4dd7a31e73026200226b", "westus2");
    speechConfig.speechSynthesisVoiceName = "en-US-AvaMultilingualNeural";

    // Initialize Avatar Configuration
    const avatarConfig = new SpeechSDK.AvatarConfig("lisa", "casual-sitting");

    // Initialize the WebRTC peer connection with ICE server configuration
    const peerConnection = new RTCPeerConnection({
        iceServers: [{
            urls: "https://commservicesrsc.unitedstates.communication.azure.com", // Replace with your ICE server URL
            username: "Your ICE server username", // Replace with your ICE username
            credential: "Your ICE server credential" // Replace with your ICE credential
        }]
    });

    // Handle incoming tracks and mount them to HTML elements
    peerConnection.ontrack = function (event) {
        const player = document.createElement(event.track.kind);
        player.srcObject = event.streams[0];
        player.autoplay = true;
        document.getElementById('mediaContainer').appendChild(player);
    };

    // Add video and audio transceivers
    peerConnection.addTransceiver('video', { direction: 'sendrecv' });
    peerConnection.addTransceiver('audio', { direction: 'sendrecv' });

    // Create avatar synthesizer
    var avatarSynthesizer = new SpeechSDK.AvatarSynthesizer(speechConfig, avatarConfig);

    // Start avatar and establish WebRTC connection
    avatarSynthesizer.startAvatarAsync(peerConnection).then(
        () => console.log("Avatar started.")
    ).catch(
        (error) => console.log("Avatar failed to start. Error: " + error)
    );

    // Function to send text to the avatar synthesizer
    window.speakText = function (text) {
        avatarSynthesizer.speakTextAsync(text).then(
            (result) => {
                if (result.reason === SpeechSDK.ResultReason.SynthesizingAudioCompleted) {
                    console.log("Speech and avatar synthesized to video stream.");
                } else {
                    console.log("Unable to speak. Result ID: " + result.resultId);
                    if (result.reason === SpeechSDK.ResultReason.Canceled) {
                        let cancellationDetails = SpeechSDK.CancellationDetails.fromResult(result);
                        console.log(cancellationDetails.reason);
                        if (cancellationDetails.reason === SpeechSDK.CancellationReason.Error) {
                            console.log(cancellationDetails.errorDetails);
                        }
                    }
                }
            }).catch((error) => {
                console.log(error);
                avatarSynthesizer.close();
            });
    };
});
